# Learning navigator

The interactive entry point is built from the existing roadmap and resource catalogs. All original catalog URLs remain available. All 19 guides and templates are rendered with the shared Learning Studio design under `guides/`. The documentation hub includes search and the five original CSV downloads. Historical Pages URLs redirect to corresponding unified pages; video and resource entry points lead to the same resource library.

## Use it

Choose a stage from the path. Read its practice task and required evidence. Search and combine topic, level and format filters, or switch to the full resource library. Save resources with the star. Click **Watch here** to load a YouTube privacy-enhanced embed; the original link remains available if embedding is blocked.

Mark a stage complete when you can explain it, complete the lab, and save reproducible evidence. Resume opens the earliest incomplete core stage. Stage 9 is an elective and does not block the capstone or career stage. Completion is self-reported, not a certification.

Progress and bookmarks use localStorage on the current origin/browser. Export/import a JSON backup to transfer them between the private Site, Vercel or portfolio. Imported IDs and stage numbers are validated before replacing progress. No server account or cloud progress sync is used.

## Content and maintenance

- `data/learning-roadmap.csv`: 12 ordered stages, 0–11.
- `data/video-resources.csv`, `community-learning-resources.csv`, `roadmap-references.csv`: original resource catalogs.
- `docs/RESOURCES.md`: additional source links.
- `scripts/build_navigator.py`: deduplication by exact URL; suggested topic/level/format classification.
- `web/`: buildless browser application. Assets use relative URLs to support a portfolio subdirectory.
- `tests/`: catalog preservation, phase integrity and video allowlist checks.

Levels are suggested stage groupings: foundations (0–2), intermediate (3–7), advanced (8–10), career (11). They are not independent assessments of course difficulty. Resource availability, third-party costs, and actual playback have not all been verified. Access notes are preserved from the source.

## Build

```sh
python3 -m pip install -r requirements.txt
npm run check
npm run build
```

The build emits `dist/`, including the original documentation under `guides/`. For a subdirectory, set `NAVIGATOR_BASEURL=/learning-navigator` before building. Vercel deploys the already-built `dist/`; the checked-in configuration intentionally runs no remote build or install.

## Release boundaries

This version is under private review. The owner approved updating the public GitHub source. GitHub Pages automatic publishing is paused, and the public portfolio remains unchanged until website-release approval. Do not deploy the portfolio production branch or change website audience before that approval. The private Vercel project requires Vercel Authentication on every deployment.

## Portfolio integration

The prepared `integration/portfolio-site/` files update the existing portfolio's `/learn/` page to embed the navigator at `/learning-navigator/`. Copy the navigator's prebuilt dist into `portfolio-site/learning-navigator-dist/`; the modified build script copies it to output. Same-origin embedding avoids third-party authentication/cookie issues. The private `portfolio-preview/` page demonstrates the integration with the current portfolio styling.
