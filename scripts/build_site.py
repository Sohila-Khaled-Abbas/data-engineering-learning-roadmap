#!/usr/bin/env python3
"""Build a static, styled HTML site from every Markdown document in the repository.

Run from the repository root:
    python scripts/build_site.py

GitHub Pages project sites should set PAGES_BASEURL=/data-engineering-learning-roadmap.
The generated site is written to _site/ and is safe to delete/rebuild.
"""
from __future__ import annotations

import html
import os
import re
import shutil
from pathlib import Path
from urllib.parse import quote

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
BASEURL = os.environ.get("PAGES_BASEURL", "").rstrip("/")

EXTENSIONS = ["tables", "fenced_code", "toc", "attr_list", "md_in_html", "sane_lists"]

STYLE = r"""
:root{color-scheme:light;--bg:#f4f7fb;--surface:#fff;--text:#122033;--muted:#596a80;--line:#dce4ef;--blue:#165dca;--navy:#10213c;--soft:#eaf2ff;--green:#13795b;--shadow:0 16px 38px rgba(18,32,51,.07)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.7 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:var(--blue);text-decoration-thickness:1px;text-underline-offset:3px}a:hover{color:#0b3e91}header{background:linear-gradient(120deg,#0d1e37,#173d6c);color:#fff}.shell{width:min(1200px,calc(100% - 32px));margin:auto}.top{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:16px 0;flex-wrap:wrap}.brand{color:#fff;font-weight:850;letter-spacing:.05em;text-decoration:none}.nav{display:flex;gap:8px;flex-wrap:wrap}.nav a{color:#eaf2ff;text-decoration:none;border:1px solid #ffffff42;border-radius:999px;padding:6px 11px;font-size:.9rem}.nav a:hover{background:#ffffff18}.hero{padding:25px 0 42px}.eyebrow{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:#9dd8ff;font-weight:900}.hero h1{font-size:clamp(2rem,5vw,3.8rem);line-height:1.12;letter-spacing:-.04em;margin:.4em 0}.hero p{max-width:820px;color:#d8e6fa;font-size:1.08rem}.badge-row{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}.badge{display:inline-flex;align-items:center;gap:6px;border:1px solid #d5e3f5;background:#f5f9ff;color:#173e75;border-radius:8px;padding:5px 9px;font-size:.78rem;font-weight:850}.hero .badge{background:#183e69;color:#e5f2ff;border-color:#ffffff35}.page{display:grid;grid-template-columns:250px minmax(0,1fr);gap:24px;padding:28px 0 56px}.sidebar{align-self:start;position:sticky;top:16px;max-height:calc(100vh - 32px);overflow:auto;background:var(--surface);border:1px solid var(--line);border-radius:15px;padding:17px;box-shadow:var(--shadow)}.sidebar h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin:0 0 9px}.sidebar a{display:block;text-decoration:none;color:#22364e;padding:6px 8px;border-radius:8px;font-size:.91rem}.sidebar a:hover{background:var(--soft)}main{min-width:0;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:clamp(18px,4vw,42px);box-shadow:var(--shadow)}main h1{line-height:1.16;letter-spacing:-.035em;font-size:clamp(1.8rem,3.5vw,2.8rem);margin-top:0}main h2{margin-top:1.9em;padding-bottom:.35em;border-bottom:1px solid var(--line);line-height:1.3}main h3{margin-top:1.5em;line-height:1.4}main h4{margin-top:1.4em}p,li{overflow-wrap:anywhere}img{max-width:100%;height:auto;border-radius:10px}blockquote{border-left:4px solid #79aef9;background:#f1f6ff;margin:1.4em 0;padding:.8em 1.2em;color:#324963;border-radius:0 10px 10px 0}pre{overflow:auto;background:#101d31;color:#e8f1ff;padding:16px;border-radius:12px;font-size:.9rem}code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;background:#edf2fa;padding:.12em .32em;border-radius:5px;font-size:.92em}pre code{background:transparent;padding:0;color:inherit}table{width:100%;border-collapse:collapse;display:block;overflow-x:auto;font-size:.93rem}th,td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}th{background:#eef4fc;font-weight:850}tr:nth-child(even) td{background:#fafcff}hr{border:0;border-top:1px solid var(--line);margin:2em 0}.toc{background:#f6f9fe;border:1px solid var(--line);border-radius:12px;padding:12px 16px}footer{border-top:1px solid var(--line);color:var(--muted);padding:24px 0 36px;font-size:.9rem}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:14px}.card{display:block;background:#fff;border:1px solid var(--line);border-radius:14px;padding:17px;text-decoration:none;color:var(--text);box-shadow:0 5px 16px #12203308}.card:hover{border-color:#8db9f7;box-shadow:var(--shadow);transform:translateY(-1px)}.card h2{border:0;margin:0 0 7px;padding:0;font-size:1.08rem}.card p{margin:.2em 0;color:var(--muted);font-size:.93rem}.section-label{font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:900;margin:28px 0 12px}.callout{border:1px solid #bcd5fa;border-left:4px solid var(--blue);border-radius:10px;padding:13px 16px;background:#f1f7ff}.file-links{display:flex;gap:10px;flex-wrap:wrap}.file-link{display:inline-flex;padding:9px 13px;border:1px solid #bdd3f1;background:#f3f8ff;border-radius:9px;text-decoration:none;font-weight:800}@media(max-width:850px){.page{grid-template-columns:1fr}.sidebar{position:static;max-height:none}.nav{width:100%}}@media(max-width:480px){.shell{width:min(100% - 20px,1200px)}.top{padding:13px 0}.nav a{font-size:.82rem;padding:5px 8px}main{padding:17px}}
"""

NAV_ITEMS = [
    ("Home", "index.html"),
    ("Roadmap", "ROADMAP.html"),
    ("Resources", "docs/RESOURCES.html"),
    ("Video gallery", "VIDEO_LIBRARY.html"),
    ("Companion roadmaps", "docs/REFERENCE_ROADMAPS.html"),
    ("Skill map", "docs/SKILL_MAP.html"),
    ("Capstone", "docs/CAPSTONE.html"),
    ("PDF materials", "docs/LEARNING_MATERIALS.html"),
]

DOCS = [
    ("README.md", "Project overview"),
    ("ROADMAP.md", "Step-by-step learning roadmap"),
    ("CONTRIBUTING.md", "Contributing"),
    ("docs/RESOURCES.md", "Learning resources"),
    ("docs/REFERENCE_ROADMAPS.md", "External roadmaps and references"),
    ("docs/SKILL_MAP.md", "Skills and technology map"),
    ("docs/PROJECTS.md", "Practice projects"),
    ("docs/CAPSTONE.md", "Capstone project"),
    ("docs/CERTIFICATIONS.md", "Certification guide"),
    ("docs/ADD_VIDEO_RESOURCES.md", "Maintaining video resources"),
    ("docs/PAGES_SETUP.md", "GitHub Pages setup"),
    ("docs/PUBLISH_TO_GITHUB.md", "Publishing to GitHub"),
    ("docs/LEARNING_MATERIALS.md", "PDF learning materials"),
    ("templates/LEARNING_NOTE.md", "Learning note template"),
    ("templates/PROJECT_README.md", "Project README template"),
    ("templates/WEEKLY_REVIEW.md", "Weekly review template"),
]

DESCRIPTIONS = {
    "README.md": "Project goals, learning order, repository structure, and ways to use the roadmap.",
    "ROADMAP.md": "Follow the learning phases in dependency order, with deliverables and completion checks.",
    "CONTRIBUTING.md": "How to suggest corrections, improvements, or learning resources.",
    "docs/RESOURCES.md": "Official documentation, video playlists, and focused tutorials.",
    "docs/REFERENCE_ROADMAPS.md": "External roadmaps, community examples, diagrams, and shared references.",
    "docs/SKILL_MAP.md": "Core skills, technologies, optional tools, and role-oriented priorities.",
    "docs/PROJECTS.md": "Small hands-on projects that turn lessons into portfolio evidence.",
    "docs/CAPSTONE.md": "Milestones for an end-to-end data engineering project.",
    "docs/CERTIFICATIONS.md": "Certification options and preparation resources.",
    "docs/ADD_VIDEO_RESOURCES.md": "How to keep the video resource index consistent.",
    "docs/PAGES_SETUP.md": "One-time setup for the hosted documentation website.",
    "docs/PUBLISH_TO_GITHUB.md": "Repository publishing guidance.",
    "docs/LEARNING_MATERIALS.md": "The supplied PDFs and their source links.",
    "templates/LEARNING_NOTE.md": "Reusable note template for a topic or study session.",
    "templates/PROJECT_README.md": "Reusable README structure for a portfolio project.",
    "templates/WEEKLY_REVIEW.md": "Weekly review and progress reflection template.",
}

def site_url(path: str) -> str:
    return (BASEURL + "/" + path.lstrip("/")).replace("//", "/") if BASEURL else "/" + path.lstrip("/")

def page_shell(title: str, body: str, current: str = "") -> str:
    nav = "".join(f'<a href="{site_url(url)}">{html.escape(label)}</a>' for label, url in NAV_ITEMS)
    sidebar = "".join(f'<a href="{site_url(Path(src).with_suffix(".html").as_posix())}">{html.escape(label)}</a>' for src, label in DOCS)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#10213c"><title>{html.escape(title)} | Data Engineering Learning Roadmap</title>
<meta name="description" content="A practical, skill-first data engineering learning roadmap, resources, projects, and documentation.">
<link rel="stylesheet" href="{site_url('assets/site.css')}"></head>
<body><header><div class="shell"><div class="top"><a class="brand" href="{site_url('index.html')}">DATA ENGINEERING LEARNING ROADMAP</a><nav class="nav" aria-label="Primary navigation">{nav}</nav></div>
<div class="hero"><div class="eyebrow">Learn · Practise · Build</div><h1>{html.escape(title)}</h1><p>Skill-first learning path with hands-on deliverables, curated resources, project documentation, and reusable study templates.</p>
<div class="badge-row"><span class="badge">Self-paced</span><span class="badge">16 video resources</span><span class="badge">10 companion references</span><span class="badge">Projects and practice</span></div></div></div></header>
<div class="shell page"><aside class="sidebar"><h2>All documentation</h2>{sidebar}</aside><main>{body}</main></div>
<footer><div class="shell">A practical learning guide. External tools and resources may change; verify access, licensing, and version-specific instructions on their official sites.
<div class="file-links" style="margin-top:10px"><a class="file-link" href="{site_url('README.html')}">Repository README</a><a class="file-link" href="{site_url('data/video-resources.csv')}">Download video index CSV</a><a class="file-link" href="{site_url('data/roadmap-references.csv')}">Download references CSV</a><a class="file-link" href="https://github.com/Sohila-Khaled-Abbas/data-engineering-learning-roadmap">GitHub repository</a></div></div></footer>
</body></html>"""

def rewrite_links(document: str) -> str:
    # Convert internal Markdown links to their generated HTML routes. Keep external URLs,
    # anchors, query strings, and non-Markdown downloads unchanged.
    def replace(match: re.Match[str]) -> str:
        prefix, url, suffix = match.group(1), match.group(2), match.group(3)
        if url.startswith(("http://", "https://", "mailto:", "tel:", "data:")) or url.startswith("#"):
            return match.group(0)
        if re.search(r"\.md(?=($|[?#]))", url, re.IGNORECASE):
            url = re.sub(r"\.md(?=($|[?#]))", ".html", url, flags=re.IGNORECASE)
        return f'{prefix}{url}{suffix}'
    return re.sub(r'(\b(?:href|src)=")([^"]+)(")', replace, document)

def create_home() -> str:
    cards = []
    groups = [
        ("Start here", ["README.md", "ROADMAP.md", "docs/SKILL_MAP.md"]),
        ("Learning resources", ["docs/RESOURCES.md", "docs/REFERENCE_ROADMAPS.md", "docs/CERTIFICATIONS.md"]),
        ("Build and demonstrate", ["docs/PROJECTS.md", "docs/CAPSTONE.md"]),
        ("Repository and workflow", ["CONTRIBUTING.md", "docs/ADD_VIDEO_RESOURCES.md", "docs/PAGES_SETUP.md", "docs/PUBLISH_TO_GITHUB.md"]),
        ("Reusable templates", ["templates/LEARNING_NOTE.md", "templates/PROJECT_README.md", "templates/WEEKLY_REVIEW.md"]),
    ]
    out = ['<div class="callout"><strong>Start with one phase at a time.</strong> Learn the concept, reproduce it in a lab, test an edge case, then save your evidence in GitHub. Use the video gallery for embedded previews and the resource pages for direct links.</div>',
           '<div class="section-label">Interactive learning</div><div class="cards">',
           f'<a class="card" href="{site_url("VIDEO_LIBRARY.html")}"><h2>▶ Video learning library</h2><p>Embedded YouTube previews with search and phase filters.</p><span class="badge">16 curated playlists/videos</span></a>',
           f'<a class="card" href="{site_url("docs/LEARNING_MATERIALS.html")}"><h2>PDF learning materials</h2><p>Source links for the two supplied course PDFs, plus the merged downloadable bundle when available.</p></a>',
           f'<a class="card" href="{site_url("data/learning-roadmap.csv")}"><h2>Download the roadmap CSV</h2><p>Machine-readable sequence of learning phases and deliverables.</p></a>',
           f'<a class="card" href="{site_url("data/technology-map.csv")}"><h2>Download the technology map</h2><p>Skills and technologies organised for filtering and planning.</p></a>',
           '</div>']
    for group, paths in groups:
        out.append(f'<div class="section-label">{html.escape(group)}</div><div class="cards">')
        for path in paths:
            title = dict(DOCS).get(path, Path(path).stem.replace("_", " ").title())
            url = Path(path).with_suffix(".html").as_posix()
            desc = DESCRIPTIONS.get(path, "Open this document.")
            out.append(f'<a class="card" href="{site_url(url)}"><h2>{html.escape(title)}</h2><p>{html.escape(desc)}</p></a>')
        out.append('</div>')
    out.append(f'<div class="section-label">Source repository</div><p>This site is generated from the repository, so changes to Markdown files flow into the website when the Pages workflow succeeds. <a href="https://github.com/Sohila-Khaled-Abbas/data-engineering-learning-roadmap">Open the GitHub repository →</a></p>')
    return page_shell("Learning documentation hub", "\n".join(out), "index.html")

def build() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(ROOT / "data", OUT / "data")
    for directory in ["templates"]:
        src = ROOT / directory
        if src.exists():
            shutil.copytree(src, OUT / directory)
    # Copy static assets and source HTML unchanged. Markdown documents get styled HTML siblings.
    if (ROOT / "docs").exists():
        shutil.copytree(ROOT / "docs", OUT / "docs")
    if (ROOT / ".nojekyll").exists():
        shutil.copy2(ROOT / ".nojekyll", OUT / ".nojekyll")
    if (ROOT / "LICENSE").exists():
        shutil.copy2(ROOT / "LICENSE", OUT / "LICENSE")
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "assets" / "site.css").write_text(STYLE, encoding="utf-8")

    markdown_files = [ROOT / name for name in ["README.md", "ROADMAP.md", "CONTRIBUTING.md"]]
    for subdir in ["docs", "templates"]:
        folder = ROOT / subdir
        if folder.exists():
            markdown_files.extend(sorted(folder.rglob("*.md")))
    seen = set()
    for src in markdown_files:
        if not src.exists() or src in seen:
            continue
        seen.add(src)
        rel = src.relative_to(ROOT)
        target = OUT / rel.with_suffix(".html")
        target.parent.mkdir(parents=True, exist_ok=True)
        parser = markdown.Markdown(extensions=EXTENSIONS, output_format="html5")
        body = rewrite_links(parser.convert(src.read_text(encoding="utf-8-sig")))
        title = dict(DOCS).get(rel.as_posix(), rel.stem.replace("_", " ").title())
        (target).write_text(page_shell(title, body, rel.as_posix()), encoding="utf-8")

    (OUT / "index.html").write_text(create_home(), encoding="utf-8")
    # The gallery is already styled and interactive; expose a root alias for stable links.
    gallery = ROOT / "docs" / "VIDEO_LIBRARY.html"
    if gallery.exists():
        shutil.copy2(gallery, OUT / "VIDEO_LIBRARY.html")
    # A source file named docs/index.html may redirect to the gallery; keep the HTML resource in docs.
    print(f"Built site at {OUT} with {len(seen)} Markdown documents and {len(list((OUT/'data').glob('*.csv')))} CSV indexes.")

if __name__ == "__main__":
    build()
