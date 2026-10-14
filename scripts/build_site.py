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
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.7 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:var(--blue);text-decoration-thickness:1px;text-underline-offset:3px}a:hover{color:#0b3e91}header{background:linear-gradient(120deg,#0d1e37,#173d6c);color:#fff}.shell{width:min(1200px,calc(100% - 32px));margin:auto}.top{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:16px 0;flex-wrap:wrap}.brand{color:#fff;font-weight:850;letter-spacing:.05em;text-decoration:none}.nav{display:flex;gap:8px;flex-wrap:wrap}.nav a{color:#eaf2ff;text-decoration:none;border:1px solid #ffffff42;border-radius:999px;padding:6px 11px;font-size:.9rem}.nav a:hover{background:#ffffff18}.hero{padding:25px 0 42px}.eyebrow{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:#9dd8ff;font-weight:900}.hero h1{font-size:clamp(2rem,5vw,3.8rem);line-height:1.12;letter-spacing:-.04em;margin:.4em 0}.hero p{max-width:820px;color:#d8e6fa;font-size:1.08rem}.badge-row{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}.badge{display:inline-flex;align-items:center;gap:6px;border:1px solid #d5e3f5;background:#f5f9ff;color:#173e75;border-radius:8px;padding:5px 9px;font-size:.78rem;font-weight:850}.hero .badge{background:#183e69;color:#e5f2ff;border-color:#ffffff35}.page{display:grid;grid-template-columns:250px minmax(0,1fr);gap:24px;padding:28px 0 56px}.sidebar{align-self:start;position:sticky;top:16px;max-height:calc(100vh - 32px);overflow:auto;background:var(--surface);border:1px solid var(--line);border-radius:15px;padding:17px;box-shadow:var(--shadow)}.sidebar h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin:0 0 9px}.sidebar a{display:block;text-decoration:none;color:#22364e;padding:6px 8px;border-radius:8px;font-size:.91rem}.sidebar a:hover{background:var(--soft)}main{min-width:0;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:clamp(18px,4vw,42px);box-shadow:var(--shadow)}main h1{line-height:1.16;letter-spacing:-.035em;font-size:clamp(1.8rem,3.5vw,2.8rem);margin-top:0}main h2{margin-top:1.9em;padding-bottom:.35em;border-bottom:1px solid var(--line);line-height:1.3}main h3{margin-top:1.5em;line-height:1.4}main h4{margin-top:1.4em}p,li{overflow-wrap:anywhere}img{max-width:100%;height:auto;border-radius:10px}blockquote{border-left:4px solid #79aef9;background:#f1f6ff;margin:1.4em 0;padding:.8em 1.2em;color:#324963;border-radius:0 10px 10px 0}pre{overflow:auto;background:#101d31;color:#e8f1ff;padding:16px;border-radius:12px;font-size:.9rem}code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;background:#edf2fa;padding:.12em .32em;border-radius:5px;font-size:.92em}pre code{background:transparent;padding:0;color:inherit}table{width:100%;border-collapse:collapse;display:block;overflow-x:auto;font-size:.93rem}th,td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}th{background:#eef4fc;font-weight:850}tr:nth-child(even) td{background:#fafcff}hr{border:0;border-top:1px solid var(--line);margin:2em 0}.toc{background:#f6f9fe;border:1px solid var(--line);border-radius:12px;padding:12px 16px}footer{border-top:1px solid var(--line);color:var(--muted);padding:24px 0 36px;font-size:.9rem}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:14px}.card{display:block;background:#fff;border:1px solid var(--line);border-radius:14px;padding:17px;text-decoration:none;color:var(--text);box-shadow:0 5px 16px #12203308}.card:hover{border-color:#8db9f7;box-shadow:var(--shadow);transform:translateY(-1px)}.card h2{border:0;margin:0 0 7px;padding:0;font-size:1.08rem}.card p{margin:.2em 0;color:var(--muted);font-size:.93rem}.section-label{font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:900;margin:28px 0 12px}.callout{border:1px solid #bcd5fa;border-left:4px solid var(--blue);border-radius:10px;padding:13px 16px;background:#f1f7ff}.file-links{display:flex;gap:10px;flex-wrap:wrap}.file-link{display:inline-flex;padding:9px 13px;border:1px solid #bdd3f1;background:#f3f8ff;border-radius:9px;text-decoration:none;font-weight:800}
.journey{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,245px),1fr));gap:13px}.journey-step{display:flex;flex-direction:column;gap:9px;padding:17px;background:linear-gradient(145deg,#fff,#f7faff);border:1px solid var(--line);border-radius:15px;box-shadow:0 7px 22px #16365b08;min-height:194px}.journey-step:before{counter-increment:journey;content:counter(journey,decimal-leading-zero);display:grid;place-items:center;width:38px;height:38px;border-radius:12px;background:var(--navy);color:#fff;font-weight:900}.journey-step h3{margin:0;font-size:1.05rem;line-height:1.35}.journey-step p{margin:0;color:var(--muted);font-size:.91rem}.journey-link{display:inline-flex;align-items:center;gap:6px;margin-top:auto;font-weight:850;text-decoration:none}.journey-rail{display:grid;grid-template-columns:repeat(11,minmax(0,1fr));gap:5px;margin:16px 0}.journey-rail span{height:6px;border-radius:99px;background:linear-gradient(90deg,#165dca,#73b0fa)}.home-start{display:grid;grid-template-columns:1.3fr .7fr;gap:15px}.home-start .card{height:100%}.filter-panel{display:grid;grid-template-columns:minmax(220px,1.4fr) repeat(2,minmax(160px,.8fr));gap:12px;background:#f7faff;border:1px solid var(--line);border-radius:14px;padding:15px;margin:16px 0}.filter-field label{display:block;font-size:.78rem;font-weight:850;color:var(--muted);margin-bottom:5px}.filter-field input,.filter-field select{width:100%;padding:11px 12px;border:1px solid #c8d6e9;border-radius:9px;background:#fff;color:var(--text);font:inherit}.resource-results{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;color:var(--muted);font-size:.9rem;margin:14px 0}.resource-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:13px}.resource-card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:9px;min-width:0;box-shadow:0 6px 20px #10213c07}.resource-card[hidden]{display:none}.resource-card h2{border:0;padding:0;margin:0;font-size:1.03rem;line-height:1.4}.resource-card p{margin:0;color:var(--muted);font-size:.91rem}.resource-card .resource-meta{display:flex;gap:6px;flex-wrap:wrap}.resource-tag{display:inline-flex;align-items:center;background:#edf4ff;color:#244875;border:1px solid #d8e7fa;border-radius:999px;padding:3px 8px;font-size:.73rem;font-weight:850}.resource-tag.priority{background:#e8f8ee;border-color:#c2ecd1;color:#176645}.resource-tag.optional{background:#fff7e6;border-color:#f2dfb4;color:#80520c}.resource-card details{border-top:1px solid var(--line);padding-top:9px;font-size:.85rem;color:var(--muted)}.resource-card summary{cursor:pointer;font-weight:800;color:#284b77}.resource-action{margin-top:auto;display:flex;gap:8px;align-items:center;flex-wrap:wrap}.resource-action a{font-weight:850;text-decoration:none}.preview-trigger{font:inherit;font-size:.86rem;font-weight:850;color:#164c91;border:1px solid #bdd3f1;background:#f0f6ff;border-radius:8px;padding:7px 10px;cursor:pointer}.preview-trigger:hover{background:#e3efff}.inline-preview{aspect-ratio:16/9;background:#07111f;border-radius:10px;overflow:hidden;margin:6px 0}.inline-preview iframe{width:100%;height:100%;border:0;display:block}.empty-state{display:none;border:1px dashed #b7c8df;border-radius:12px;text-align:center;padding:28px;color:var(--muted)}
@media(max-width:850px){.page{grid-template-columns:1fr}.sidebar{position:static;max-height:none}.nav{width:100%}}@media(max-width:480px){.shell{width:min(100% - 20px,1200px)}.top{padding:13px 0}.nav a{font-size:.82rem;padding:5px 8px}main{padding:17px}}
"""

NAV_ITEMS = [
    ("Home", "index.html"),
    ("Guided roadmap", "ROADMAP.html"),
    ("Resource Explorer", "learning-resources.html"),
    ("Resource guide", "docs/RESOURCES.html"),
    ("Video gallery", "VIDEO_LIBRARY.html"),
    ("Community resources", "docs/COMMUNITY_RESOURCES.html"),
    ("Companion roadmaps", "docs/REFERENCE_ROADMAPS.html"),
    ("Capstone", "docs/CAPSTONE.html"),
    ("PDF materials", "docs/LEARNING_MATERIALS.html"),
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
    nav = "".join(f'<a href="{site_url(url)}">{html.escape(label)}</a>' for label, url in NAV_ITEMS)
    sidebar = "".join(f'<a href="{site_url(Path(src).with_suffix(".html").as_posix())}">{html.escape(label)}</a>' for src, label in DOCS)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#10213c"><title>{html.escape(title)} | Data Engineering Learning Roadmap</title>
<meta name="description" content="A practical, skill-first data engineering learning roadmap, resources, projects, and documentation.">
<link rel="stylesheet" href="{site_url('assets/site.css')}"></head>
<body><header><div class="shell"><div class="top"><a class="brand" href="{site_url('index.html')}">DATA ENGINEERING LEARNING ROADMAP</a><nav class="nav" aria-label="Primary navigation">{nav}</nav></div>
<div class="hero"><div class="eyebrow">Learn · Practise · Build</div><h1>{html.escape(title)}</h1><p>Skill-first learning path with hands-on deliverables, curated resources, project documentation, and reusable study templates.</p>
<div class="badge-row"><span class="badge">Self-paced</span><span class="badge">{csv_count("video-resources.csv")} video resources</span><span class="badge">{csv_count("community-learning-resources.csv")} community resources</span><span class="badge">{csv_count("roadmap-references.csv")} roadmap references</span><span class="badge">Projects and practice</span></div></div></div></header>
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

def normalise_phase(value: str) -> str:
    text = (value or "").strip()
    lower = text.lower()
    if not text or "roadmap reference" in lower or lower == "reference" or "companion" in lower:
        return "Companion roadmaps"
    rules = [
        ("Phase 0", "Foundations & setup"), ("Phase 1", "SQL & databases"),
        ("Phase 2", "Python & data work"), ("Phase 3", "Data quality"),
        ("Phase 4", "Modeling & warehousing"), ("Phase 5", "BI & storytelling"),
        ("Phase 6", "Pipelines & orchestration"), ("Phase 7", "Engineering & deployment"),
        ("Phase 8", "Big data"), ("Phase 9", "Electives"),
        ("Phase 10", "Capstone & career"),
    ]
    for prefix, label in rules:
        if text.startswith(prefix):
            return label
    return text if text else "Additional resources"

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

def load_resource_rows() -> list[dict[str, str]]:
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
    rows = load_resource_rows()
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
                f'aria-expanded="false">Preview here ▶</button>'
            )
        cards.append(
            f'<article class="resource-card" data-phase="{html.escape(row["phase"], quote=True)}" '
            f'data-type="{html.escape(row["type"], quote=True)}" data-search="{html.escape(query, quote=True)}">'
            f'<div class="resource-meta"><span class="resource-tag">{html.escape(row["phase"])}</span>'
            f'<span class="resource-tag">{html.escape(row["type"])}</span>'
            f'<span class="resource-tag {priority_class}">{html.escape(row["priority"])}</span></div>'
            f'<h2>{html.escape(row["title"])}</h2><p><strong>{html.escape(row["skill"])}</strong></p>'
            f'<p>{html.escape(row["summary"])}</p>'
            f'<details><summary>Source and access notes</summary>'
            f'<p><strong>Source:</strong> {html.escape(row["source"])}</p>'
            f'<p><strong>Format:</strong> {html.escape(row["format"])}</p>'
            f'<p>{html.escape(row["access"])}</p></details>'
            f'<div class="resource-action"><a href="{html.escape(row["url"], quote=True)}" target="_blank" rel="noopener noreferrer">Open resource ↗</a>{preview_button}</div>'
            '</article>'
        )
    body = f"""
<div class="callout"><strong>How to choose:</strong> follow the primary roadmap in order. Filter by your current phase, choose one lesson or course, then complete a practical deliverable before adding another resource. “Core” items are a suggested priority, not a requirement to finish every course.</div>
<div class="badge-row"><span class="badge">{len(rows)} indexed resources</span><span class="badge">{len(phases)} learning phases / tracks</span><span class="badge">Videos · courses · docs · project ideas</span>
<a class="badge" href="{site_url('data/community-learning-resources.csv')}">Download community CSV ↓</a>
<a class="badge" href="{site_url('data/video-resources.csv')}">Download video CSV ↓</a>
<a class="badge" href="{site_url('data/roadmap-references.csv')}">Download reference CSV ↓</a></div>
<div class="filter-panel">
<div class="filter-field"><label for="resource-search">Search titles, skills, sources or notes</label><input id="resource-search" type="search" placeholder="Try Airflow, SQL, dimensional modeling…" autocomplete="off"></div>
<div class="filter-field"><label for="phase-filter">Learning phase</label><select id="phase-filter"><option value="all">All phases</option>{phase_options}</select></div>
<div class="filter-field"><label for="type-filter">Resource type</label><select id="type-filter"><option value="all">All types</option>{type_options}</select></div></div>
<div class="resource-results"><span id="resource-count" aria-live="polite">Showing {len(rows)} resources</span><a href="{site_url('ROADMAP.html')}">Return to the step-by-step roadmap →</a></div>
<div class="resource-grid" id="resource-grid">{''.join(cards)}</div>
<div class="empty-state" id="resource-empty">No resources match those filters. Clear the search or choose “All phases” and “All types”.</div>
<script>
(function () {{
  var search = document.getElementById("resource-search");
  var phase = document.getElementById("phase-filter");
  var type = document.getElementById("type-filter");
  var cards = Array.prototype.slice.call(document.querySelectorAll(".resource-card"));
  var count = document.getElementById("resource-count");
  var empty = document.getElementById("resource-empty");
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
  document.querySelectorAll(".preview-trigger").forEach(function (button) {{
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
      frame.title = "YouTube preview: " + card.querySelector("h2").textContent;
      frame.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      frame.referrerPolicy = "strict-origin-when-cross-origin";
      frame.allowFullscreen = true;
      frameBox.appendChild(frame);
      button.parentNode.insertBefore(frameBox, button);
      button.setAttribute("aria-expanded", "true");
      button.textContent = "Hide preview ✕";
    }});
  }});
}})();
</script>
"""
    return page_shell("Resource Explorer", body, "learning-resources.html")

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
        '<div class="section-label">Choose your next action</div><div class="home-start"><div class="card"><span class="badge">Start here</span><h2 style="margin-top:10px">Follow the guided roadmap</h2><p>Work through eleven phases in dependency order. Each phase has a practical outcome so you know when to move forward.</p><a class="journey-link" href="' + site_url("ROADMAP.html") + '">Open the roadmap →</a></div><div class="card"><span class="badge">Need a resource?</span><h2 style="margin-top:10px">Search the library</h2><p>Filter community and official resources by phase, type, skill, or source. Choose one resource and put it to work.</p><a class="journey-link" href="' + site_url("learning-resources.html") + '">Open Resource Explorer →</a></div></div>',
        '<div class="section-label">Your learning path</div><div class="journey-rail" role="img" aria-label="Learning path progresses from fundamentals to capstone">' + ''.join("<span></span>" for _ in phases) + '</div>',
        '<div class="journey">' + "".join(journey) + '</div>',
        '<div class="section-label">Learn with multiple formats</div><div class="cards">',
        f'<a class="card" href="{site_url("learning-resources.html")}"><h2>Resource Explorer</h2><p>Search the community catalog alongside video and companion-roadmap indexes.</p><span class="badge">{csv_count("community-learning-resources.csv")} community resources</span></a>',
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
        title = dict(DOCS).get(rel.as_posix(), rel.stem.replace("_", " ").title())
        (target).write_text(page_shell(title, body, rel.as_posix()), encoding="utf-8")

    (OUT / "index.html").write_text(create_home(), encoding="utf-8")
    (OUT / "learning-resources.html").write_text(create_resource_explorer(), encoding="utf-8")
    # The gallery is already styled and interactive; expose a root alias for stable links.
    gallery = ROOT / "docs" / "VIDEO_LIBRARY.html"
    if gallery.exists():
        shutil.copy2(gallery, OUT / "VIDEO_LIBRARY.html")
    # A source file named docs/index.html may redirect to the gallery; keep the HTML resource in docs.
    print(f"Built site at {OUT} with {len(seen)} Markdown documents and {len(list((OUT/'data').glob('*.csv')))} CSV indexes.")

if __name__ == "__main__":
    build()
