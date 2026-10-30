"""Build the navigator and the existing documentation using repository catalogs."""
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from style_guides import style_guides

ROOT = Path(__file__).resolve().parents[1]

def rows(name):
    with (ROOT / 'data' / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def phases(text):
    if 'all phases' in text.lower():
        return list(range(12))
    found = re.findall(r'Phase\s+(\d+)', text, re.I)
    return [int(p) for p in found if int(p) < 12]

def topic_for(text, phase_ids):
    s = text.lower()
    for pattern, label in [
        (r'network|\bdns\b|http|tcp', 'Networking'),
        (r'operating system|linux|shell|powershell|bash', 'OS & Linux'),
        (r'\bsql\b|database|postgres|oracle|mongo', 'SQL & databases'),
        (r'python|pandas|programming|java|scala', 'Programming'),
        (r'modeling|modelling|warehouse|dimensional|\bdbt\b', 'Modeling & warehousing'),
        (r'quality|statistics|profiling', 'Data quality'),
        (r'power bi|tableau|visual|storytelling|\bdax\b', 'BI & storytelling'),
        (r'airflow|orchestrat|pipeline|\betl\b|\bapi\b', 'Pipelines & orchestration'),
        (r'spark|hadoop|kafka|big data|distributed|cloud', 'Big data & cloud'),
        (r'docker|git|testing|ci/cd|engineering|deploy', 'Engineering'),
        (r'career|communication|interview|portfolio|capstone', 'Portfolio & career')
    ]:
        if re.search(pattern, s):
            return label
    return {0:'Engineering',1:'SQL & databases',2:'Programming',3:'Data quality',4:'Modeling & warehousing',5:'BI & storytelling',6:'Pipelines & orchestration',7:'Engineering',8:'Big data & cloud',9:'Specialized tools',10:'Portfolio & career',11:'Portfolio & career'}.get(phase_ids[0] if phase_ids else 0,'Engineering')

def embed_url(url):
    u = urlparse(url)
    if u.hostname not in ('youtube.com','www.youtube.com','youtu.be','m.youtube.com'):
        return None
    q = parse_qs(u.query)
    if q.get('list'):
        return 'https://www.youtube-nocookie.com/embed/videoseries?list=' + q['list'][0]
    video = u.path.strip('/') if u.hostname == 'youtu.be' else q.get('v', [''])[0]
    return 'https://www.youtube-nocookie.com/embed/' + video if re.fullmatch(r'[A-Za-z0-9_-]{11}', video) else None

def catalog():
    stages = []
    for row in rows('learning-roadmap.csv'):
        i = int(row['Phase'])
        stages.append(dict(id=i, title=row['Focus'], duration=row['Suggested Duration'], tools=row['Primary Technologies'], skills=row['Skills to Practice'], task=row['Build Task'], evidence=row['Evidence / Definition of Done'], priority=row['Priority'], level='Foundations' if i<=2 else 'Intermediate' if i<=7 else 'Career' if i==11 else 'Advanced'))
    resources = {}
    def add(title,url,pids,skill='',kind='',description='',note='',source='',priority='Supplementary'):
        if not url.startswith(('https://','http://')):
            return
        if url in resources:
            resources[url]['phases'] = sorted(set(resources[url]['phases']+pids))
            return
        embed = embed_url(url)
        fmt = 'Video' if embed else 'Practice' if re.search(r'practice|exercise|interactive sql|problem',kind,re.I) else 'Documentation' if re.search(r'doc|reference',kind,re.I) else 'Roadmap' if 'roadmap' in kind.lower() else 'Website'
        resources[url] = dict(id=hashlib.sha256(url.encode()).hexdigest()[:12],title=title,url=url,phases=pids,topic=topic_for(title+' '+skill,pids),format=fmt,originalFormat=kind,description=description or 'Use alongside a hands-on exercise in the relevant stage.',note=note,source=source,priority=priority,embed=embed)
    for name in ['video-resources.csv','community-learning-resources.csv']:
        for r in rows(name):
            add(r['Title'],r['URL'],phases(r['Recommended Phase']),r['Skill Area'],r['Format'],r['How to Use It'],r.get('Access / Cost Note',''),name,r['Priority'])
    for r in rows('roadmap-references.csv'):
        add(r['Title'],r['URL'],list(range(12)),r['Focus Areas'],'Roadmap',r['How to Use It'],r['Access / Verification'],'roadmap-references.csv')
    phase_ids = []
    for line in (ROOT/'docs/RESOURCES.md').read_text().splitlines():
        if line.startswith('#'):
            phase_ids = phases(line)
        for title,url in re.findall(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',line):
            if 'github.io/data-engineering-learning-roadmap' in url:
                continue
            add(title,url,phase_ids or list(range(12)),kind='Documentation' if re.search(r'docs\.|learn.microsoft|documentation|reference',url+' '+title,re.I) else 'Website',description=line.split(') — ',1)[-1] if ') — ' in line else '',source='docs/RESOURCES.md')
    for r in resources.values():
        r['levels']=sorted(set(stages[i]['level'] for i in r['phases']))
    return dict(stages=stages,resources=list(resources.values()),sourceCommit='93cd1afba565a97938e5628b16569d8790ee6d6c')

def build():
    subprocess.run([sys.executable,str(ROOT/'scripts/build_site.py')],cwd=ROOT,env={**os.environ,'PAGES_BASEURL':os.environ.get('NAVIGATOR_BASEURL','')+'/guides'},check=True)
    out=ROOT/'dist'
    if out.exists(): shutil.rmtree(out)
    out.mkdir()
    shutil.copytree(ROOT/'_site',out/'guides')
    for p in (ROOT/'web').iterdir():
        if p.is_dir(): shutil.copytree(p,out/p.name)
        else: shutil.copy(p,out/p.name)
    data=catalog()
    (out/'catalog.js').write_text('window.ROADMAP = '+json.dumps(data,ensure_ascii=False).replace('</',r'<\/')+';\n')
    (out/'catalog.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    # Preserve recognizable historical entry points while making the navigator primary.
    for name in ['VIDEO_LIBRARY.html','learning-resources.html']:
        (out/name).write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=./?view=library"><a href="./?view=library">Open the resource library</a>')
    style_guides(ROOT,out,data)
    if os.environ.get('PUBLIC_RELEASE_APPROVED')=='true':
        p=out/'index.html';p.write_text(p.read_text().replace('noindex,nofollow','index,follow'))
    public=os.environ.get('PUBLIC_RELEASE_APPROVED')=='true'
    (out/'robots.txt').write_text('User-agent: *\n'+('Allow: /' if public else 'Disallow: /')+'\nSitemap: https://data-engineering-learning-roadmap.vercel.app/sitemap.xml\n')
    pages=['']+['guides/']+['guides/'+str(p.relative_to(out/'guides')) for p in (out/'guides').rglob('*.html') if p.name not in ['index.html','VIDEO_LIBRARY.html','learning-resources.html']]
    (out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>https://data-engineering-learning-roadmap.vercel.app/'+p+'</loc></url>' for p in pages)+'</urlset>')
    print(f"Built {len(data['stages'])} stages and {len(data['resources'])} unique resources.")

if __name__=='__main__': build()
