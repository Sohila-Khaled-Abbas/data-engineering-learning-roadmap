#!/usr/bin/env python3
"""Build a static, styled HTML site from every Markdown document in the repository.

Run from the repository root:
    python scripts/build_site.py

GitHub Pages project sites should set PAGES_BASEURL=/data-engineering-learning-roadmap.
The generated site is written to _site/ and is safe to delete/rebuild.
"""
from __future__ import annotations

import csv
import html
import os
import re
import shutil
from pathlib import Path
from urllib.parse import parse_qs, quote, urlsplit

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
BASEURL = os.environ.get("PAGES_BASEURL", "").rstrip("/")

def csv_count(filename: str) -> int:
    path = ROOT / "data" / filename
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return max(0, sum(1 for _ in csv.reader(handle)) - 1)
    except (OSError, csv.Error):
        return 0

EXTENSIONS = ["tables", "fenced_code", "toc", "attr_list", "md_in_html", "sane_lists"]

STYLE = r"""
:root{color-scheme:light;--bg:#f4f7fb;--surface:#fff;--text:#122033;--muted:#596a80;--line:#dce4ef;--blue:#165dca;--navy:#10213c;--soft:#eaf2ff;--green:#13795b;--shadow:0 16px 38px rgba(18,32,51,.07)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.7 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:var(--blue);text-decoration-thickness:1px;text-underline-offset:3px}a:hover{color:#0b3e91}header{background:linear-gradient(120deg,#0d1e37,#173d6c);color:#fff}.shell{width:min(1200px,calc(100% - 32px));margin:auto}.top{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:16px 0;flex-wrap:wrap}.brand{color:#fff;font-weight:850;letter-spacing:.05em;text-decoration:none}.nav{display:flex;align-items:center;gap:7px;flex-wrap:wrap}.nav a,.nav-more summary{color:#eaf2ff;text-decoration:none;border:1px solid #ffffff42;border-radius:999px;padding:6px 11px;font-size:.88rem;font-weight:750;white-space:nowrap}.nav a:hover,.nav a.active,.nav-more summary:hover,.nav-more[open] summary{background:#ffffff1d;border-color:#ffffff82}.nav a.active{box-shadow:inset 0 0 0 1px #ffffff32}.nav-more{position:relative}.nav-more summary{cursor:pointer;list-style:none;user-select:none}.nav-more summary::-webkit-details-marker{display:none}.nav-dropdown{position:absolute;z-index:60;right:0;top:calc(100% + 8px);min-width:225px;display:grid;gap:4px;padding:8px;background:#fff;border:1px solid var(--line);border-radius:13px;box-shadow:var(--shadow)}.nav .nav-dropdown a{display:block;color:var(--text);border:0;border-radius:8px;padding:9px 11px;white-space:normal;font-size:.91rem}.nav .nav-dropdown a:hover,.nav .nav-dropdown a.active{background:var(--soft);color:var(--blue)}.skip-link{position:absolute;left:12px;top:-60px;z-index:1000;padding:10px 14px;background:#fff;color:var(--navy);border-radius:8px}.skip-link:focus{top:12px}.page-top-link{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 18px}.page-top-link a{font-weight:800;text-decoration:none;border:1px solid var(--line);border-radius:9px;padding:8px 11px;background:#f8fbff}.hero{padding:25px 0 42px}.eyebrow{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:#9dd8ff;font-weight:900}.hero h1{font-size:clamp(2rem,5vw,3.8rem);line-height:1.12;letter-spacing:-.04em;margin:.4em 0}.hero p{max-width:820px;color:#d8e6fa;font-size:1.08rem}.badge-row{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}.badge{display:inline-flex;align-items:center;gap:6px;border:1px solid #d5e3f5;background:#f5f9ff;color:#173e75;border-radius:8px;padding:5px 9px;font-size:.78rem;font-weight:850}.hero .badge{background:#183e69;color:#e5f2ff;border-color:#ffffff35}.page{display:grid;grid-template-columns:250px minmax(0,1fr);gap:24px;padding:28px 0 56px}.sidebar{align-self:start;position:sticky;top:16px;max-height:calc(100vh - 32px);overflow:auto;background:var(--surface);border:1px solid var(--line);border-radius:15px;padding:17px;box-shadow:var(--shadow)}.sidebar h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin:0 0 9px}.sidebar a{display:block;text-decoration:none;color:#22364e;padding:6px 8px;border-radius:8px;font-size:.91rem}.sidebar a:hover{background:var(--soft)}main{min-width:0;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:clamp(18px,4vw,42px);box-shadow:var(--shadow)}main h1{line-height:1.16;letter-spacing:-.035em;font-size:clamp(1.8rem,3.5vw,2.8rem);margin-top:0}main h2{margin-top:1.9em;padding-bottom:.35em;border-bottom:1px solid var(--line);line-height:1.3}main h3{margin-top:1.5em;line-height:1.4}main h4{margin-top:1.4em}p,li{overflow-wrap:anywhere}img{max-width:100%;height:auto;border-radius:10px}blockquote{border-left:4px solid #79aef9;background:#f1f6ff;margin:1.4em 0;padding:.8em 1.2em;color:#324963;border-radius:0 10px 10px 0}pre{overflow:auto;background:#101d31;color:#e8f1ff;padding:16px;border-radius:12px;font-size:.9rem}code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;background:#edf2fa;padding:.12em .32em;border-radius:5px;font-size:.92em}pre code{background:transparent;padding:0;color:inherit}table{width:100%;border-collapse:collapse;display:block;overflow-x:auto;font-size:.93rem}th,td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}th{background:#eef4fc;font-weight:850}tr:nth-child(even) td{background:#fafcff}hr{border:0;border-top:1px solid var(--line);margin:2em 0}.toc{background:#f6f9fe;border:1px solid var(--line);border-radius:12px;padding:12px 16px}footer{border-top:1px solid var(--line);color:var(--muted);padding:24px 0 36px;font-size:.9rem}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:14px}.card{display:block;background:#fff;border:1px solid var(--line);border-radius:14px;padding:17px;text-decoration:none;color:var(--text);box-shadow:0 5px 16px #12203308}.card:hover{border-color:#8db9f7;box-shadow:var(--shadow);transform:translateY(-1px)}.card h2{border:0;margin:0 0 7px;padding:0;font-size:1.08rem}.card p{margin:.2em 0;color:var(--muted);font-size:.93rem}.section-label{font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:900;margin:28px 0 12px}.callout{border:1px solid #bcd5fa;border-left:4px solid var(--blue);border-radius:10px;padding:13px 16px;background:#f1f7ff}.file-links{display:flex;gap:10px;flex-wrap:wrap}.file-link{display:inline-flex;padding:9px 13px;border:1px solid #bdd3f1;background:#f3f8ff;border-radius:9px;text-decoration:none;font-weight:800}
.journey{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,245px),1fr));gap:13px}.journey-step{display:flex;flex-direction:column;gap:9px;padding:17px;background:linear-gradient(145deg,#fff,#f7faff);border:1px solid var(--line);border-radius:15px;box-shadow:0 7px 22px #16365b08;min-height:194px}.journey-step:before{counter-increment:journey;content:counter(journey,decimal-leading-zero);display:grid;place-items:center;width:38px;height:38px;border-radius:12px;background:var(--navy);color:#fff;font-weight:900}.journey-step h3{margin:0;font-size:1.05rem;line-height:1.35}.journey-step p{margin:0;color:var(--muted);font-size:.91rem}.journey-link{display:inline-flex;align-items:center;gap:6px;margin-top:auto;font-weight:850;text-decoration:none}.journey-rail{display:grid;grid-template-columns:repeat(11,minmax(0,1fr));gap:5px;margin:16px 0}.journey-rail span{height:6px;border-radius:99px;background:linear-gradient(90deg,#165dca,#73b0fa)}.home-start{display:grid;grid-template-columns:1.3fr .7fr;gap:15px}.home-start .card{height:100%}.filter-panel{display:grid;grid-template-columns:minmax(220px,1.4fr) repeat(2,minmax(160px,.8fr));gap:12px;background:#f7faff;border:1px solid var(--line);border-radius:14px;padding:15px;margin:16px 0}.filter-field label{display:block;font-size:.78rem;font-weight:850;color:var(--muted);margin-bottom:5px}.filter-field input,.filter-field select{width:100%;padding:11px 12px;border:1px solid #c8d6e9;border-radius:9px;background:#fff;color:var(--text);font:inherit}.resource-results{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;color:var(--muted);font-size:.9rem;margin:14px 0}.resource-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:13px}.resource-card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:9px;min-width:0;box-shadow:0 6px 20px #10213c07}.resource-card[hidden]{display:none}.resource-card h2,.resource-card h3{border:0;padding:0;margin:0;font-size:1.03rem;line-height:1.4}.resource-title{color:var(--blue);text-decoration:underline;text-underline-offset:3px;font-weight:850}.gallery-video-preview{margin:2px 0 8px}.phase-resources{margin:24px 0;padding:18px 0;border-top:1px solid var(--line)}.phase-resource-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:11px}.phase-resource-card{min-width:0;border:1px solid var(--line);border-radius:12px;background:#fbfdff;padding:13px;display:flex;flex-direction:column;gap:8px}.phase-resource-card h3{margin:2px 0;font-size:1rem;line-height:1.4}.phase-resource-card p{margin:0;font-size:.9rem;color:var(--muted)}.phase-resource-source{font-size:.78rem!important}.resource-action{align-items:center}.resource-card p{margin:0;color:var(--muted);font-size:.91rem}.resource-card .resource-meta{display:flex;gap:6px;flex-wrap:wrap}.resource-tag{display:inline-flex;align-items:center;background:#edf4ff;color:#244875;border:1px solid #d8e7fa;border-radius:999px;padding:3px 8px;font-size:.73rem;font-weight:850}.resource-tag.priority{background:#e8f8ee;border-color:#c2ecd1;color:#176645}.resource-tag.optional{background:#fff7e6;border-color:#f2dfb4;color:#80520c}.resource-card details{border-top:1px solid var(--line);padding-top:9px;font-size:.85rem;color:var(--muted)}.resource-card summary{cursor:pointer;font-weight:800;color:#284b77}.resource-action{margin-top:auto;display:flex;gap:8px;align-items:center;flex-wrap:wrap}.resource-action a{font-weight:850;text-decoration:none}.preview-trigger{font:inherit;font-size:.86rem;font-weight:850;color:#164c91;border:1px solid #bdd3f1;background:#f0f6ff;border-radius:8px;padding:7px 10px;cursor:pointer}.preview-trigger:hover{background:#e3efff}.inline-preview{aspect-ratio:16/9;background:#07111f;border-radius:10px;overflow:hidden;margin:6px 0}.inline-preview iframe{width:100%;height:100%;border:0;display:block}.empty-state{display:none;border:1px dashed #b7c8df;border-radius:12px;text-align:center;padding:28px;color:var(--muted)}
@media(max-width:850px){.page{grid-template-columns:1fr}.sidebar{position:static;max-height:none}.nav{width:100%}.nav-more{margin-left:auto}.nav-dropdown{right:0}.filter-panel{grid-template-columns:1fr 1fr}.filter-field:first-child{grid-column:1/-1}}@media(max-width:480px){.shell{width:min(100% - 20px,1200px)}.top{padding:13px 0}.nav{gap:5px}.nav>a,.nav-more summary{font-size:.78rem;padding:5px 8px}.nav-more{margin-left:0}.nav-dropdown{position:fixed;right:10px;left:10px;top:auto;min-width:0}.filter-panel{grid-template-columns:1fr}.filter-field:first-child{grid-column:auto}main{padding:17px}}
"""

NAV_ITEMS = [
    ("Home", "index.html"),
    ("Guided roadmap", "ROADMAP.html"),
    ("Resource & video gallery", "VIDEO_LIBRARY.html"),
    ("Community guide", "docs/COMMUNITY_RESOURCES.html"),
]
MORE_NAV_ITEMS = [
    ("Learning resources guide", "docs/RESOURCES.html"),
    ("Companion roadmaps", "docs/REFERENCE_ROADMAPS.html"),
    ("Capstone project", "docs/CAPSTONE.html"),
    ("PDF materials", "docs/LEARNING_MATERIALS.html"),
    ("Skills & technology map", "docs/SKILL_MAP.html"),
    ("Practice projects", "docs/PROJECTS.html"),
]

DOCS = [
    ("README.md", "Project overview"),
    ("ROADMAP.md", "Step-by-step learning roadmap"),
    ("CONTRIBUTING.md", "Contributing"),
    ("docs/RESOURCES.md", "Learning resources"),
    ("docs/COMMUNITY_RESOURCES.md", "Community learning resources"),
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
    "docs/COMMUNITY_RESOURCES.md": "One hundred curated learning links from community roadmaps and project briefs, organised by phase.",
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
    current_path = Path(current).with_suffix(".html").as_posix() if current else ""
    def nav_link(label: str, url: str) -> str:
        active = current_path == url
        active_class = "active" if active else ""
        aria_current = ' aria-current="page"' if active else ""
        return f'<a class="{active_class}" href="{site_url(url)}"{aria_current}>{html.escape(label)}</a>'
    nav = "".join(nav_link(label, url) for label, url in NAV_ITEMS)
    more_active = current_path in {url for _, url in MORE_NAV_ITEMS}
    more_links = "".join(nav_link(label, url) for label, url in MORE_NAV_ITEMS)
    sidebar = "".join(f'<a href="{site_url(Path(src).with_suffix(".html").as_posix())}">{html.escape(label)}</a>' for src, label in DOCS)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#10213c"><title>{html.escape(title)} | Data Engineering Learning Roadmap</title>
<meta name="description" content="A practical, skill-first data engineering learning roadmap, resources, projects, and documentation.">
<link rel="stylesheet" href="{site_url('assets/site.css')}"></head>
<body><a class="skip-link" href="#main-content">Skip to main content</a>
<header><div class="shell"><div class="top"><a class="brand" href="{site_url('index.html')}">DATA ENGINEERING LEARNING ROADMAP</a><nav class="nav" aria-label="Primary navigation">{nav}<details class="nav-more{" active" if more_active else ""}"><summary aria-label="More pages">More <span aria-hidden="true">⌄</span></summary><div class="nav-dropdown" aria-label="More pages">{more_links}</div></details></nav></div>
<div class="hero"><div class="eyebrow">Learn · Practise · Build</div><h1>{html.escape(title)}</h1><p>One connected learning hub: follow the roadmap, discover resources, preview videos, and turn each topic into portfolio evidence.</p>
<div class="badge-row"><span class="badge">Self-paced</span><span class="badge">{csv_count("video-resources.csv")} video resources</span><span class="badge">{csv_count("community-learning-resources.csv")} community resources</span><span class="badge">{csv_count("roadmap-references.csv")} roadmap references</span><span class="badge">Projects and practice</span></div></div></div></header>
<div class="shell page"><aside class="sidebar"><h2>Explore the hub</h2><a href="{site_url('index.html')}">Home and learning path</a><a href="{site_url('ROADMAP.html')}">Step-by-step roadmap</a><a href="{site_url('VIDEO_LIBRARY.html')}">All videos, docs & resources</a><a href="{site_url('docs/COMMUNITY_RESOURCES.html')}">Community learning resources</a><h2 style="margin-top:18px">All documentation</h2>{sidebar}</aside><main id="main-content" tabindex="-1"><div class="page-top-link"><a href="{site_url('index.html')}">← Hub home</a><a href="{site_url('VIDEO_LIBRARY.html')}">Search videos & resources ↗</a><a href="{site_url('ROADMAP.html')}">Learning roadmap ↗</a></div>{body}</main></div>
<footer><div class="shell">A practical learning guide. External tools and resources may change; verify access, licensing, and version-specific instructions on their official sites.
<div class="file-links" style="margin-top:10px"><a class="file-link" href="{site_url('README.html')}">Repository README</a><a class="file-link" href="{site_url('data/community-learning-resources.csv')}">Download community CSV</a><a class="file-link" href="{site_url('data/video-resources.csv')}">Download video index CSV</a><a class="file-link" href="{site_url('data/roadmap-references.csv')}">Download references CSV</a><a class="file-link" href="https://github.com/Sohila-Khaled-Abbas/data-engineering-learning-roadmap" target="_blank" rel="noopener noreferrer">GitHub repository ↗</a></div></div></footer>
<script>
document.addEventListener("click", function(event) {{
  document.querySelectorAll(".nav-more[open]").forEach(function(menu) {{
    if (!menu.contains(event.target)) menu.removeAttribute("open");
  }});
}});
</script>
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

def normalise_phase(value: str) -> str:
    text = (value or "").strip()
    lower = text.lower()
    match = re.match(r"^phase\s+(\d+)\b", text, re.IGNORECASE)
    phase_labels = {
        0: "Foundations & setup",
        1: "SQL & databases",
        2: "Python & data work",
        3: "Data quality",
        4: "Modeling & warehousing",
        5: "BI & storytelling",
        6: "Pipelines & orchestration",
        7: "Engineering & deployment",
        8: "Big data",
        9: "Electives",
        10: "Capstone & career",
    }
    if match:
        return phase_labels.get(int(match.group(1)), text)
    if not text or "roadmap reference" in lower or lower == "reference" or "companion" in lower:
        return "Companion roadmaps"
    return text

def youtube_embed_url(url: str) -> str:
    try:
        parsed = urlsplit(url)
        params = parse_qs(parsed.query)
        host = parsed.netloc.lower()
        if "youtu.be" in host:
            video_id = parsed.path.strip("/").split("/")[0]
            return "https://www.youtube-nocookie.com/embed/" + video_id if video_id else ""
        if "youtube.com" not in host:
            return ""
        playlist_id = params.get("list", [""])[0]
        video_id = params.get("v", [""])[0]
        if video_id:
            return "https://www.youtube-nocookie.com/embed/" + video_id + (("?list=" + playlist_id) if playlist_id else "")
        if "playlist" in parsed.path and playlist_id:
            return "https://www.youtube-nocookie.com/embed/videoseries?list=" + playlist_id
    except (ValueError, IndexError):
        return ""
    return ""

def classify_resource_type(fmt: str, url: str) -> str:
    text = (fmt + " " + url).lower()
    if "youtube.com" in text or "youtu.be" in text or "playlist" in text or "video" in text:
        return "Video"
    if "kaggle.com" in text or "/projects/" in text or "dataset" in text or "drawsql.app" in text:
        return "Project / dataset"
    if "github.com" in text and ("repository" in text or "/tree/" in text or "/blob/" in text):
        return "GitHub / project"
    if any(term in text for term in ["course", "learning path", "online course", "skill track", "certification"]):
        return "Course / learning path"
    if any(term in text for term in ["documentation", "official", "article", "tutorial site", "technical article", "reference"]):
        return "Docs / article"
    return "Reference"

def load_resource_rows(catalogs: tuple[str, ...] = ("community", "video", "references")) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(title: str, skill: str, fmt: str, phase: str, priority: str, url: str,
            source: str, access: str, summary: str) -> None:
        url = (url or "").strip()
        title = (title or "").strip()
        if not url.startswith(("https://", "http://")) or not title or url in seen:
            return
        seen.add(url)
        rows.append({
            "title": title, "skill": skill or "General learning", "format": fmt or "Reference",
            "type": classify_resource_type(fmt, url), "phase": normalise_phase(phase),
            "priority": priority or "Supplementary", "url": url, "embed": youtube_embed_url(url), "source": source or "Community catalog",
            "access": access or "Check source for current access and pricing.",
            "summary": summary or "Open the source resource and practise the related skill.",
        })

    sources = [
        ("community-learning-resources.csv", "community"),
        ("video-resources.csv", "video"),
        ("roadmap-references.csv", "references"),
    ]
    for filename, kind in sources:
        if kind not in catalogs:
            continue
        path = ROOT / "data" / filename
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if kind == "community":
                    add(row.get("Title", ""), row.get("Skill Area", ""), row.get("Format", ""),
                        row.get("Recommended Phase", ""), row.get("Priority", ""), row.get("URL", ""),
                        row.get("Source", ""), row.get("Access / Cost Note", ""), row.get("How to Use It", ""))
                elif kind == "video":
                    add(row.get("Title", ""), row.get("Skill Area", ""), row.get("Format", ""),
                        row.get("Recommended Phase", ""), row.get("Priority", ""), row.get("URL", ""),
                        "Video library", "YouTube or external course access; check the source page.",
                        row.get("How to Use It", ""))
                else:
                    add(row.get("Title", ""), row.get("Focus Areas", ""), row.get("Resource Type", ""),
                        "Companion roadmaps", "Reference", row.get("URL", ""), "Companion roadmap index",
                        row.get("Access / Verification", ""), row.get("How to Use It", ""))
    return rows

def create_resource_explorer() -> str:
    """Backward-compatible route to the merged video and resource gallery."""
    return create_unified_gallery()


def create_community_resource_section() -> str:
    rows = load_resource_rows(("community",))
    phases = sorted({row["phase"] for row in rows})
    types = sorted({row["type"] for row in rows})
    phase_options = "".join(f'<option value="{html.escape(p, quote=True)}">{html.escape(p)}</option>' for p in phases)
    type_options = "".join(f'<option value="{html.escape(t, quote=True)}">{html.escape(t)}</option>' for t in types)
    cards: list[str] = []
    for row in rows:
        query = " ".join([row["title"], row["skill"], row["format"], row["phase"],
                          row["source"], row["access"], row["summary"], row["priority"]]).lower()
        priority_class = "priority" if row["priority"].lower() == "core" else "optional"
        preview_button = ""
        if row.get("embed"):
            preview_button = (
                f'<button class="preview-trigger" type="button" data-embed="{html.escape(row["embed"], quote=True)}" '
                f'aria-expanded="false" aria-label="Preview {html.escape(row["title"], quote=True)}">Preview here ▶</button>'
            )
        cards.append(
            f'<article class="resource-card" data-phase="{html.escape(row["phase"], quote=True)}" '
            f'data-type="{html.escape(row["type"], quote=True)}" data-search="{html.escape(query, quote=True)}">'
            f'<div class="resource-meta"><span class="resource-tag">{html.escape(row["phase"])}</span>'
            f'<span class="resource-tag">{html.escape(row["type"])}</span>'
            f'<span class="resource-tag {priority_class}">{html.escape(row["priority"])}</span></div>'
            f'<h3>{html.escape(row["title"])}</h3><p><strong>{html.escape(row["skill"])}</strong></p>'
            f'<p>{html.escape(row["summary"])}</p>'
            f'<details><summary>Source and access notes</summary>'
            f'<p><strong>Source:</strong> {html.escape(row["source"])}</p>'
            f'<p><strong>Format:</strong> {html.escape(row["format"])}</p>'
            f'<p>{html.escape(row["access"])}</p></details>'
            f'<div class="resource-action"><a href="{html.escape(row["url"], quote=True)}" target="_blank" rel="noopener noreferrer">Open resource ↗</a>{preview_button}</div>'
            '</article>'
        )
    return f"""
<section class="community-catalog" aria-labelledby="community-catalog-title">
  <div class="section-label">Explore the full community catalog</div>
  <h2 id="community-catalog-title">Search, open, and preview resources</h2>
  <p>Every card links directly to its original source. Video and playlist entries include an on-page preview; other resources open at their source. Filter the list instead of scrolling through the entire catalog.</p>
  <div class="callout"><strong>Keep learning practical:</strong> choose one resource for your current phase, do the exercise, and save the result as evidence. Access and pricing notes are listed on each card when available.</div>
  <div class="badge-row"><span class="badge">{len(rows)} community resources</span><span class="badge">{len(phases)} phases / tracks</span><a class="badge" href="{site_url('data/community-learning-resources.csv')}">Download CSV ↓</a><a class="badge" href="{site_url('learning-resources.html')}">Explore all resource collections ↗</a></div>
  <div class="filter-panel">
    <div class="filter-field"><label for="community-search">Search titles, skills, sources, or notes</label><input id="community-search" type="search" placeholder="Try SQL, Airflow, pandas, Kafka…" autocomplete="off"></div>
    <div class="filter-field"><label for="community-phase-filter">Learning phase</label><select id="community-phase-filter"><option value="all">All phases</option>{phase_options}</select></div>
    <div class="filter-field"><label for="community-type-filter">Resource type</label><select id="community-type-filter"><option value="all">All types</option>{type_options}</select></div>
  </div>
  <div class="resource-results"><span id="community-resource-count" aria-live="polite">Showing {len(rows)} resources</span><a href="{site_url('learning-resources.html')}">Open the combined Resource Explorer →</a></div>
  <div class="resource-grid" id="community-resource-grid">{''.join(cards)}</div>
  <div class="empty-state" id="community-resource-empty">No resources match those filters. Clear the search or choose “All phases” and “All types”.</div>
</section>
<script>
(function () {{
  var search = document.getElementById("community-search");
  var phase = document.getElementById("community-phase-filter");
  var type = document.getElementById("community-type-filter");
  var cards = Array.prototype.slice.call(document.querySelectorAll("#community-resource-grid .resource-card"));
  var count = document.getElementById("community-resource-count");
  var empty = document.getElementById("community-resource-empty");
  if (!search || !phase || !type || !count || !empty) return;
  function refresh() {{
    var term = search.value.trim().toLowerCase();
    var wantedPhase = phase.value;
    var wantedType = type.value;
    var visible = 0;
    cards.forEach(function (card) {{
      var textMatch = !term || card.getAttribute("data-search").indexOf(term) !== -1;
      var phaseMatch = wantedPhase === "all" || card.getAttribute("data-phase") === wantedPhase;
      var typeMatch = wantedType === "all" || card.getAttribute("data-type") === wantedType;
      var show = textMatch && phaseMatch && typeMatch;
      card.hidden = !show;
      if (show) visible++;
    }});
    count.textContent = "Showing " + visible + " of " + cards.length + " community resources";
    empty.style.display = visible ? "none" : "block";
  }}
  search.addEventListener("input", refresh);
  phase.addEventListener("change", refresh);
  type.addEventListener("change", refresh);
  document.querySelectorAll("#community-resource-grid .preview-trigger").forEach(function (button) {{
    button.addEventListener("click", function () {{
      var card = button.closest(".resource-card");
      var preview = card.querySelector(".inline-preview");
      if (preview) {{
        preview.remove();
        button.setAttribute("aria-expanded", "false");
        button.textContent = "Preview here ▶";
        return;
      }}
      var frameBox = document.createElement("div");
      frameBox.className = "inline-preview";
      var frame = document.createElement("iframe");
      frame.loading = "lazy";
      frame.src = button.getAttribute("data-embed");
      frame.title = "Video preview: " + card.querySelector("h3").textContent;
      frame.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      frame.referrerPolicy = "strict-origin-when-cross-origin";
      frame.allowFullscreen = true;
      frameBox.appendChild(frame);
      var actions = button.closest(".resource-action");
      actions.parentNode.insertBefore(frameBox, actions);
      button.setAttribute("aria-expanded", "true");
      button.textContent = "Hide preview ✕";
    }});
  }});
  refresh();
}})();
</script>
"""


def create_unified_gallery() -> str:
    """Render all catalogues in one searchable page: YouTube embeds, direct links for everything else."""
    rows = load_resource_rows()
    phases = sorted({row["phase"] for row in rows})
    types = sorted({row["type"] for row in rows})
    video_count = sum(1 for row in rows if row.get("embed"))
    phase_options = "".join(f'<option value="{html.escape(phase, quote=True)}">{html.escape(phase)}</option>' for phase in phases)
    type_options = "".join(f'<option value="{html.escape(resource_type, quote=True)}">{html.escape(resource_type)}</option>' for resource_type in types)
    cards: list[str] = []
    for row in rows:
        query = " ".join([row["title"], row["skill"], row["format"], row["phase"], row["source"], row["access"], row["summary"], row["priority"], row["type"]]).lower()
        priority_class = "priority" if row["priority"].lower() == "core" else "optional"
        video_preview = ""
        if row.get("embed"):
            video_preview = (
                f'<div class="inline-preview gallery-video-preview">'
                f'<iframe loading="lazy" src="{html.escape(row["embed"], quote=True)}" '
                f'title="Embedded video: {html.escape(row["title"], quote=True)}" '
                f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
                f'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>'
            )
        direct_link = html.escape(row["url"], quote=True)
        title = html.escape(row["title"])
        action_label = "Watch / open source ↗" if row.get("embed") else "Open documentation / website ↗"
        cards.append(
            f'<article class="resource-card" data-phase="{html.escape(row["phase"], quote=True)}" data-type="{html.escape(row["type"], quote=True)}" data-search="{html.escape(query, quote=True)}">'
            f'<div class="resource-meta"><span class="resource-tag">{html.escape(row["phase"])}</span><span class="resource-tag">{html.escape(row["type"])}</span><span class="resource-tag {priority_class}">{html.escape(row["priority"])}</span></div>'
            f'{video_preview}'
            f'<h2><a class="resource-title" href="{direct_link}" target="_blank" rel="noopener noreferrer">{title} ↗</a></h2>'
            f'<p><strong>{html.escape(row["skill"])}</strong></p><p>{html.escape(row["summary"])}</p>'
            f'<details><summary>Source, format and access notes</summary>'
            f'<p><strong>Source:</strong> {html.escape(row["source"])}</p><p><strong>Format:</strong> {html.escape(row["format"])}</p><p>{html.escape(row["access"])}</p></details>'
            f'<div class="resource-action"><a class="file-link" href="{direct_link}" target="_blank" rel="noopener noreferrer">{action_label}</a></div>'
            '</article>'
        )
    body = f"""
<div class="callout"><strong>One library, end to end.</strong> This gallery combines the community catalog, curated video library, and companion-roadmap index. YouTube videos and playlists are embedded in their cards. Documentation, courses, practice sites, datasets, GitHub projects, and websites link to their original sources.</div>
<div class="badge-row"><span class="badge">{len(rows)} unique resource URLs</span><span class="badge">{video_count} embedded video resources</span><span class="badge">{len(types)} resource types</span><a class="badge" href="{site_url('data/community-learning-resources.csv')}">Community CSV ↓</a><a class="badge" href="{site_url('data/video-resources.csv')}">Video CSV ↓</a><a class="badge" href="{site_url('data/roadmap-references.csv')}">Roadmap references CSV ↓</a></div>
<div class="filter-panel">
<div class="filter-field"><label for="gallery-search">Search all titles, skills, sources or notes</label><input id="gallery-search" type="search" placeholder="Try SQL, Airflow, pandas, Kafka, dbt…" autocomplete="off"></div>
<div class="filter-field"><label for="gallery-phase">Learning phase</label><select id="gallery-phase"><option value="all">All phases</option>{phase_options}</select></div>
<div class="filter-field"><label for="gallery-type">Resource type</label><select id="gallery-type"><option value="all">All types</option>{type_options}</select></div></div>
<div class="resource-results"><span id="gallery-count" aria-live="polite">Showing {len(rows)} resources</span><a href="{site_url('ROADMAP.html')}">Return to the end-to-end roadmap →</a></div>
<div class="resource-grid" id="gallery-grid">{''.join(cards)}</div><div class="empty-state" id="gallery-empty">No resources match those filters. Clear search or choose “All phases” and “All types”.</div>
<script>
(function () {{
  var search = document.getElementById("gallery-search");
  var phase = document.getElementById("gallery-phase");
  var type = document.getElementById("gallery-type");
  var cards = Array.prototype.slice.call(document.querySelectorAll("#gallery-grid .resource-card"));
  var count = document.getElementById("gallery-count");
  var empty = document.getElementById("gallery-empty");
  if (!search || !phase || !type || !count || !empty) return;
  var params = new URLSearchParams(window.location.search);
  var phaseParam = params.get("phase");
  var searchParam = params.get("q");
  if (phaseParam && Array.prototype.some.call(phase.options, function (option) {{ return option.value === phaseParam; }})) phase.value = phaseParam;
  if (searchParam) search.value = searchParam;
  function refresh() {{
    var term = search.value.trim().toLowerCase();
    var wantedPhase = phase.value;
    var wantedType = type.value;
    var visible = 0;
    cards.forEach(function (card) {{
      var textMatch = !term || card.getAttribute("data-search").indexOf(term) !== -1;
      var phaseMatch = wantedPhase === "all" || card.getAttribute("data-phase") === wantedPhase;
      var typeMatch = wantedType === "all" || card.getAttribute("data-type") === wantedType;
      var show = textMatch && phaseMatch && typeMatch;
      card.hidden = !show;
      if (show) visible++;
    }});
    count.textContent = "Showing " + visible + " of " + cards.length + " resources";
    empty.style.display = visible ? "none" : "block";
  }}
  search.addEventListener("input", refresh);
  phase.addEventListener("change", refresh);
  type.addEventListener("change", refresh);
  refresh();
}})();
</script>
"""
    return page_shell("Resource & Video Gallery", body, "VIDEO_LIBRARY.html")


def add_roadmap_resource_sections(body: str) -> str:
    """Attach curated, clickable resource cards and a phase-filtered gallery link to each roadmap phase."""
    rows = load_resource_rows()
    keywords = {
        0: ["network", "operating system", "linux", "git", "workspace", "bash", "terminal"],
        1: ["sql", "database", "relational", "query", "postgres", "sql server"],
        2: ["python", "pandas", "programming", "importing data", "cleaning data"],
        3: ["data quality", "quality", "statistics", "profiling", "validation", "cleaning data"],
        4: ["modeling", "warehouse", "star schema", "data model", "dimensional"],
        5: ["power bi", "business intelligence", "tableau", "dashboard", "storytelling"],
        6: ["airflow", "pipeline", "orchestration", "etl", "api", "bash", "kafka"],
        7: ["docker", "github actions", "git", "testing", "linux", "deployment", "ci/cd"],
        8: ["spark", "pyspark", "kafka", "hadoop", "hive", "parquet", "avro", "big data"],
        9: ["mongodb", "snowflake", "dbt", "oracle", "datastage", "informatica", "scala", "incorta"],
        10: ["capstone", "project", "dataset", "zoomcamp", "kaggle", "github repos", "airbnb", "e-commerce", "tmdb"],
    }
    phase_titles = {0: "Workspace and fundamentals", 1: "SQL and relational databases", 2: "Python for data work", 3: "Data quality and statistics", 4: "Data modeling and warehousing", 5: "BI and data storytelling", 6: "Pipelines and orchestration", 7: "Engineering and deployment", 8: "Big data and distributed processing", 9: "Role-specific electives", 10: "Portfolio capstone"}
    headings = list(re.finditer(r'<h2\b[^>]*>.*?</h2>', body, flags=re.IGNORECASE | re.DOTALL))
    insertions: list[tuple[int, str]] = []
    for index, heading in enumerate(headings):
        phase_match = re.search(r'\bid="phase-(\d+)-', heading.group(0))
        if not phase_match:
            continue
        number = int(phase_match.group(1))
        phase_label = normalise_phase(f"Phase {number}")
        matches = [row for row in rows if row["phase"] == phase_label]
        matches.sort(key=lambda row: (0 if row["priority"].lower() == "core" else 1, 0 if row.get("embed") else 1, row["title"].lower()))
        selected = matches[:4]
        if len(selected) < 3:
            terms = keywords.get(number, [])
            fallback = [row for row in rows if row not in selected and row["phase"] != "Companion roadmaps" and any(term in (row["title"] + " " + row["skill"] + " " + row["summary"]).lower() for term in terms)]
            fallback.sort(key=lambda row: (0 if row["priority"].lower() == "core" else 1, 0 if row.get("embed") else 1, row["title"].lower()))
            for row in fallback:
                if row not in selected:
                    selected.append(row)
                if len(selected) >= 4:
                    break
        if len(selected) < 3:
            for row in rows:
                if row not in selected and row["phase"] != "Companion roadmaps":
                    selected.append(row)
                if len(selected) >= 3:
                    break
        cards = []
        for row in selected[:4]:
            cards.append(f'<article class="phase-resource-card"><span class="resource-tag">{html.escape(row["type"])}</span><h3><a class="resource-title" href="{html.escape(row["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(row["title"])} ↗</a></h3><p>{html.escape(row["summary"])}</p><p class="phase-resource-source">Source: {html.escape(row["source"])}</p></article>')
        gallery_url = site_url("VIDEO_LIBRARY.html") + "?phase=" + quote(phase_label)
        block = (f'<section class="phase-resources" aria-label="Resources for Phase {number}: {html.escape(phase_titles.get(number, phase_label))}">'
                 f'<div class="section-label">Phase {number} learning resources</div>'
                 f'<p>Work through a small number of lessons, open the linked docs or practice site, then finish the deliverable above before moving on.</p>'
                 f'<div class="phase-resource-grid">{"".join(cards)}</div>'
                 f'<p><a class="journey-link" href="{html.escape(gallery_url, quote=True)}">Open the full gallery filtered to {html.escape(phase_label)} →</a></p></section>')
        next_heading_pos = headings[index + 1].start() if index + 1 < len(headings) else len(body)
        insertions.append((next_heading_pos, block))
    for position, block in sorted(insertions, key=lambda item: item[0], reverse=True):
        body = body[:position] + block + body[position:]
    return body

def create_home() -> str:
    groups = [
        ("Start here", ["README.md", "ROADMAP.md", "docs/SKILL_MAP.md"]),
        ("Learning resources", ["docs/RESOURCES.md", "docs/COMMUNITY_RESOURCES.md", "docs/REFERENCE_ROADMAPS.md", "docs/CERTIFICATIONS.md"]),
        ("Build and demonstrate", ["docs/PROJECTS.md", "docs/CAPSTONE.md"]),
        ("Repository and workflow", ["CONTRIBUTING.md", "docs/ADD_VIDEO_RESOURCES.md", "docs/PAGES_SETUP.md", "docs/PUBLISH_TO_GITHUB.md"]),
        ("Reusable templates", ["templates/LEARNING_NOTE.md", "templates/PROJECT_README.md", "templates/WEEKLY_REVIEW.md"]),
    ]
    phases = [
        ("Set up your workspace", "Git, GitHub, terminal, networking and OS basics", "Environment checklist and first commit", "phase-0-prepare-your-workspace"),
        ("SQL and databases", "PostgreSQL or SQL Server; relational modeling", "Schema, joins, CTEs and tested queries", "phase-1-sql-and-relational-databases"),
        ("Python for data work", "Python, pandas, files, APIs and tests", "Reusable data-cleaning script", "phase-2-python-for-data-work"),
        ("Data quality and statistics", "Profiling, validation, distributions and uncertainty", "Quality report and test rules", "phase-3-data-quality-and-basic-statistics"),
        ("Data modeling and warehousing", "Facts, dimensions, grain, keys and lineage", "ERD, data dictionary and star schema", "phase-4-data-modeling-and-warehousing"),
        ("BI and storytelling", "Power BI, Power Query, DAX; Tableau optional", "Report with reconciled KPIs", "phase-5-bi-and-data-storytelling"),
        ("Pipelines and orchestration", "APIs, Python, Airflow, Bash and retries", "Repeatable pipeline with logs", "phase-6-apis-pipelines-and-orchestration"),
        ("Engineering and deployment", "Git, tests, CI, Docker and Linux", "Reproducible environment with automated checks", "phase-7-engineering-practices-and-deployment"),
        ("Big data", "Spark/PySpark first; Kafka, Hadoop and Hive concepts", "Batch pipeline or streaming proof of concept", "phase-8-big-data-and-distributed-processing"),
        ("Choose focused electives", "MongoDB, dbt, Snowflake, Oracle or enterprise tools", "One elective tied to your target role", "phase-9-choose-electives-by-role"),
        ("Build the capstone", "Your core stack end to end", "Tested pipeline, model, dashboard and demo", "phase-10-build-the-portfolio-capstone"),
    ]
    journey = []
    for idx, (title, tools, output, anchor) in enumerate(phases, start=0):
        journey.append(
            f'<article class="journey-step"><span class="badge">Phase {idx:02d}</span>'
            f'<h3>{html.escape(title)}</h3><p class="journey-tools">{html.escape(tools)}</p>'
            f'<p><strong>Build:</strong> {html.escape(output)}</p>'
            f'<a class="journey-link" href="{site_url("ROADMAP.html")}#{anchor}">Open this phase →</a></article>'
        )
    out = [
        '<div class="callout"><strong>Your rule of progress:</strong> study one phase at a time. Read or watch just enough to understand the concept, complete a lab, test an edge case, and save evidence in GitHub. A finished project beats a long playlist checklist.</div>',
        '<div class="section-label">Choose your next action</div><div class="home-start"><div class="card"><span class="badge">Start here</span><h2 style="margin-top:10px">Follow the guided roadmap</h2><p>Work through eleven phases in dependency order. Each phase has a practical outcome so you know when to move forward.</p><a class="journey-link" href="' + site_url("ROADMAP.html") + '">Open the roadmap →</a></div><div class="card"><span class="badge">Need a resource?</span><h2 style="margin-top:10px">Open the resource gallery</h2><p>Search community resources, videos, courses, documentation, datasets and companion roadmaps in one place.</p><a class="journey-link" href="' + site_url("learning-resources.html") + '">Open Resource & Video Gallery →</a></div></div>',
        '<div class="section-label">Your learning path</div><div class="journey-rail" role="img" aria-label="Learning path progresses from fundamentals to capstone">' + ''.join("<span></span>" for _ in phases) + '</div>',
        '<div class="journey">' + "".join(journey) + '</div>',
        '<div class="section-label">Learn with multiple formats</div><div class="cards">',
        f'<a class="card" href="{site_url("VIDEO_LIBRARY.html")}"><h2>Resource & Video Gallery</h2><p>Embedded video players plus direct links to documentation, tutorials, courses, datasets, and project briefs.</p><span class="badge">{csv_count("community-learning-resources.csv") + csv_count("video-resources.csv") + csv_count("roadmap-references.csv")} catalog entries before URL deduplication</span></a>',
        f'<a class="card" href="{site_url("VIDEO_LIBRARY.html")}"><h2>Video learning library</h2><p>Embedded YouTube previews with search and phase filters.</p><span class="badge">{csv_count("video-resources.csv")} curated videos/playlists</span></a>',
        f'<a class="card" href="{site_url("docs/COMMUNITY_RESOURCES.html")}"><h2>Community resource guide</h2><p>Curated picks and project ideas organised by learning stage.</p></a>',
        f'<a class="card" href="{site_url("docs/REFERENCE_ROADMAPS.html")}"><h2>Companion roadmaps</h2><p>Compare external roadmaps without losing your primary learning order.</p></a>',
        f'<a class="card" href="{site_url("docs/LEARNING_MATERIALS.html")}"><h2>PDF learning materials</h2><p>Source links and status for the supplied learning PDFs.</p></a>',
        f'<a class="card" href="{site_url("data/learning-roadmap.csv")}"><h2>Download the roadmap CSV</h2><p>Machine-readable sequence of phases and deliverables.</p></a>',
        '</div>'
    ]
    for group, paths in groups:
        out.append(f'<div class="section-label">{html.escape(group)}</div><div class="cards">')
        for path in paths:
            title = dict(DOCS).get(path, Path(path).stem.replace("_", " ").title())
            url = Path(path).with_suffix(".html").as_posix()
            desc = DESCRIPTIONS.get(path, "Open this document.")
            out.append(f'<a class="card" href="{site_url(url)}"><h2>{html.escape(title)}</h2><p>{html.escape(desc)}</p></a>')
        out.append('</div>')
    out.append(f'<div class="callout" style="margin-top:24px"><strong>Keep the stack small.</strong> Start with one SQL database, Python, a BI tool, orchestration, testing and Docker. Treat specialised or paid tools as electives. <a href="{site_url("docs/SKILL_MAP.html")}">See the skill map →</a></div>')
    return page_shell("Your Data Engineering Learning Hub", "\n".join(out), "index.html")

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
        if rel.as_posix() == "ROADMAP.md":
            body = add_roadmap_resource_sections(body)
        if rel.as_posix() == "docs/COMMUNITY_RESOURCES.md":
            body += create_community_resource_section()
        title = dict(DOCS).get(rel.as_posix(), rel.stem.replace("_", " ").title())
        (target).write_text(page_shell(title, body, rel.as_posix()), encoding="utf-8")

    (OUT / "index.html").write_text(create_home(), encoding="utf-8")
    gallery_html = create_unified_gallery()
    (OUT / "learning-resources.html").write_text(gallery_html, encoding="utf-8")
    (OUT / "VIDEO_LIBRARY.html").write_text(gallery_html, encoding="utf-8")
    # Keep the former docs URL as an alias to the same unified catalogue.
    (OUT / "docs" / "VIDEO_LIBRARY.html").write_text(gallery_html, encoding="utf-8")
    # A source file named docs/index.html may redirect to the gallery; keep the HTML resource in docs.
    print(f"Built site at {OUT} with {len(seen)} Markdown documents and {len(list((OUT/'data').glob('*.csv')))} CSV indexes.")

if __name__ == "__main__":
    build()
