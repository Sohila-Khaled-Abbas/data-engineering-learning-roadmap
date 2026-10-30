"""Restyle every legacy documentation page and retain historical URLs."""
import html
import json
import os
import re
import shutil
import markdown
from build_site import EXTENSIONS, rewrite_links
from pathlib import Path

def style_guides(root, out, data):
    base=os.environ.get('NAVIGATOR_BASEURL','').rstrip('/')
    def app(path=''): return base+'/'+path
    groups={
        'Start & plan':['ROADMAP.html','docs/SKILL_MAP.html','docs/RESOURCES.html','docs/REFERENCE_ROADMAPS.html'],
        'Practise & build':['docs/PROJECTS.html','docs/CAPSTONE.html','docs/COMMUNITY_RESOURCES.html','docs/LEARNING_MATERIALS.html'],
        'Reflect & share':['templates/LEARNING_NOTE.html','templates/WEEKLY_REVIEW.html','templates/PROJECT_README.html','docs/CERTIFICATIONS.html'],
        'Maintain the hub':['docs/NAVIGATOR.html','docs/ADD_VIDEO_RESOURCES.html','CONTRIBUTING.html','docs/PAGES_SETUP.html','docs/PUBLISH_TO_GITHUB.html','README.html','docs/REPOSITORY_GUIDE.html']
    }
    descriptions={
        'ROADMAP.html':'The complete path: concepts, practical tasks, deliverables and exit checks.',
        'docs/SKILL_MAP.html':'Core skills, dependencies and role-specific technology choices.',
        'docs/RESOURCES.html':'Original learning links, documentation, video playlists and practice tools.',
        'docs/REFERENCE_ROADMAPS.html':'Companion roadmaps and community perspectives, with source notes.',
        'docs/PROJECTS.html':'Small projects that turn a topic into evidence you can show.',
        'docs/CAPSTONE.html':'Scope, build and explain a complete, repeatable data product.',
        'docs/COMMUNITY_RESOURCES.html':'The community catalog, organized around practical learning goals.',
        'docs/LEARNING_MATERIALS.html':'Source materials, original documents and learning references.',
        'templates/LEARNING_NOTE.html':'A reusable template for concepts, experiments and evidence.',
        'templates/WEEKLY_REVIEW.html':'Review what you built and choose the next useful step.',
        'templates/PROJECT_README.html':'Make your project understandable and reproducible.',
        'docs/CERTIFICATIONS.html':'Use credentials to support learning and project work.',
        'docs/NAVIGATOR.html':'Build, content maintenance, local progress and deployment notes.',
        'docs/ADD_VIDEO_RESOURCES.html':'Add recognizable video links and maintain the source catalog.',
        'CONTRIBUTING.html':'Contribute focused, useful improvements to the learning hub.',
        'docs/PAGES_SETUP.html':'How the unified website is built and released on GitHub Pages.',
        'docs/PUBLISH_TO_GITHUB.html':'Repository update and release workflow.',
        'README.html':'The current repository overview, deployed links and build commands.',
        'docs/REPOSITORY_GUIDE.html':'The preserved original repository guide and learning philosophy.'
    }
    titles={}
    bodies={}
    for rel in [r for paths in groups.values() for r in paths]:
        p=out/'guides'/rel
        if not p.exists(): continue
        source=root/Path(rel).with_suffix('.md')
        body=rewrite_links(markdown.Markdown(extensions=EXTENSIONS).convert(source.read_text(encoding='utf-8-sig')))
        # Keep recognizable links while avoiding navigation back to the old skin.
        old='https://sohila-khaled-abbas.github.io/data-engineering-learning-roadmap/'
        body=body.replace(old,app())
        if rel=='docs/REPOSITORY_GUIDE.html':
            body=re.sub(r'href="(?!https?:|#|/)([^"]+)"',lambda m:'href="'+app('guides/'+m[1])+'"',body)
        if rel=='ROADMAP.html':
            body=re.sub(r'(<h2 id="phase-(\d+)-[^\"]+">.*?</h2>)',lambda m:'<span id="stage-'+m[2]+'"></span>'+m[1]+'<p><a class="journey-link" href="'+app('?stage='+m[2])+'">Open this stage in the navigator →</a></p>',body)
        heading=re.search(r'<h1[^>]*>(.*?)</h1>',body,re.S)
        titles[rel]=html.unescape(re.sub('<[^>]+>','',heading[1])) if heading else Path(rel).stem.replace('_',' ').title()
        bodies[rel]=body
    ordered=list(bodies)
    def shell(title,body,active=''):
        canonical='https://data-engineering-learning-roadmap.vercel.app/guides/'+active
        robots='index,follow' if os.environ.get('PUBLIC_RELEASE_APPROVED')=='true' else 'noindex,nofollow'
        nav=''.join('<p class="overline guide-nav-label">'+html.escape(group)+'</p>'+''.join(f'<a class="guide-nav-link {"selected" if rel==active else ""}" href="{app("guides/"+rel)}" {"aria-current=page" if rel==active else ""}>{html.escape(titles[rel])}</a>' for rel in paths if rel in titles) for group,paths in groups.items())
        return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#382b25"><title>{html.escape(title)} | Data Engineering Learning Roadmap</title><link rel="canonical" href="{canonical}"><meta name="robots" content="{robots}"><meta name="description" content="{html.escape(descriptions.get(active,'Explore the complete data engineering roadmap, documentation, practice templates and original resource downloads.'))}"><meta property="og:title" content="{html.escape(title)} | Data Engineering Learning Roadmap"><meta property="og:url" content="{canonical}"><meta property="og:type" content="website"><link rel="icon" href="{app('favicon.svg')}" type="image/svg+xml"><link rel="stylesheet" href="{app('navigator.css')}"><link rel="stylesheet" href="{app('guides.css')}"></head><body class="guide-page"><a class="skip" href="#main">Skip to content</a><aside class="sidebar"><a class="brand" href="{app()}">sohila<span>.</span><small>THE LEARNING STUDIO</small></a><nav class="mode-links" aria-label="Learning sections"><a href="{app()}">↗ The roadmap</a><a href="{app('?view=library')}">▷ Resource library</a><a href="{app('guides/')}">▤ Guides & templates</a></nav><nav aria-label="Documentation">{nav}</nav></aside><div class="workspace"><header class="topbar"><span>THE DATA TEA <span class="slash">/</span> THE FIELD GUIDE</span><a href="{app()}">Back to the navigator ↗</a></header><main id="main"><div class="doc-breadcrumb"><a href="{app('guides/')}">Guides & templates</a><span>/</span><span>{html.escape(title)}</span></div>{body}<footer><span>SOHILA KHALED ABBAS / THE LEARNING STUDIO</span><a href="{app('?view=library')}">Find a resource ↗</a><a href="{app()}">Continue the roadmap →</a></footer></main></div></body></html>'''
    for rel,body in bodies.items():
        headings=re.findall(r'<h[23] id="([^"]+)">(.*?)</h[23]>',body,re.S)
        toc='<details class="guide-toc"><summary>On this page</summary><nav aria-label="On this page">'+''.join(f'<a href="#{html.escape(anchor)}">{re.sub("<[^>]+>","",label)}</a>' for anchor,label in headings)+'</nav></details>' if headings else ''
        # TOC comes after the first heading and intro; no duplicated page title.
        end=body.find('</h1>')+5
        body=body[:end]+toc+body[end:]
        i=ordered.index(rel)
        paging='<nav class="guide-paging" aria-label="Next guide">'+(f'<a href="{app("guides/"+ordered[i-1])}">← {html.escape(titles[ordered[i-1]])}</a>' if i else '<span></span>')+(f'<a href="{app("guides/"+ordered[i+1])}">{html.escape(titles[ordered[i+1]])} →</a>' if i<len(ordered)-1 else f'<a href="{app()}">Return to the roadmap →</a>')+'</nav>'
        (out/'guides'/rel).write_text(shell(titles[rel],'<article class="guide-prose">'+body+'</article>'+paging,rel))
    cards=''
    for group,paths in groups.items():
        cards+=f'<section class="guide-group"><p class="overline">{html.escape(group)}</p><div class="guide-grid">'+''.join(f'<a class="guide-card" href="{app("guides/"+r)}"><span class="format">{"Template" if r.startswith("templates/") else "Guide"}</span><h2>{html.escape(titles[r])}</h2><p>{html.escape(descriptions[r])}</p><span class="guide-arrow">Read the guide ↗</span></a>' for r in paths if r in titles)+'</div></section>'
    downloads='<section class="guide-group"><p class="overline">TAKE THE SOURCE WITH YOU</p><h2>Original catalogs & downloads.</h2><div class="download-grid">'+''.join(f'<a href="{app("data/"+p.name)}" download><span>↓ CSV</span>{html.escape(p.stem.replace("-"," ").title())}</a>' for p in (root/'data').glob('*.csv'))+'</div></section>'
    intro=f'<section class="guide-intro"><p class="overline">THE WHOLE ROADMAP, IN ONE PLACE</p><h1>Understand the idea.<br><em>Keep the useful parts.</em></h1><p>Every guide, source catalog and practice template from the original learning hub, brought together with the interactive roadmap.</p><div class="guide-stats"><span>{len(titles)} guides & templates</span><span>{len(data["resources"])} resources</span><span>{len(data["stages"])} stages</span></div><label class="guide-search-label">Find a guide<input type="search" id="guide-search" placeholder="Modeling, capstone, learning notes…"></label><p id="guide-search-status" role="status" aria-live="polite"></p></section>'
    hub=shell('Guides & templates',intro+cards+downloads+'<script src="'+app('guides.js')+'" defer></script>')
    (out/'guides/index.html').write_text(hub)
    # All legacy page URLs enter the same unified website, preserving fragments.
    def redirect(path,target):
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text('<!doctype html><meta charset="utf-8"><title>Continue learning · Sohila</title><script>location.replace('+json.dumps(target)+'+location.hash)</script><a href="'+html.escape(target)+'">Continue to the learning hub</a>')
    for rel in titles:
        redirect(out/rel,app('guides/'+rel))
    for rel in ['VIDEO_LIBRARY.html','learning-resources.html','docs/VIDEO_LIBRARY.html','guides/VIDEO_LIBRARY.html','guides/learning-resources.html','guides/docs/VIDEO_LIBRARY.html']:
        redirect(out/rel,app('?view=library'))
    redirect(out/'docs/index.html',app('guides/'))
    redirect(out/'guides/docs/index.html',app('guides/'))
    shutil.copytree(root/'data',out/'data',dirs_exist_ok=True)
    for rel in titles:
        source=root/Path(rel).with_suffix('.md')
        if source.exists():
            target=out/Path(rel).with_suffix('.md');target.parent.mkdir(parents=True,exist_ok=True);shutil.copy(source,target)
