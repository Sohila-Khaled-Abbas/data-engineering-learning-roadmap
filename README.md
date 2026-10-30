# Data Engineering Learning Navigator

A practical learning website by Sohila Khaled Abbas: 12 stages, original resource links, embedded YouTube lessons, SQL practice, networking, OS, databases, analytics engineering and end-to-end project work.

## Start learning

1. Choose a stage and read its practice task and evidence checklist.
2. Search resources or filter by topic, suggested level and format.
3. Save useful links and use **Watch here** to load a video or playlist.
4. Complete the lab, keep evidence, then mark the stage complete.
5. Resume the earliest incomplete core stage, or explore optional electives.

Progress is local to each browser and origin. Export/import a backup to move it between deployments.

## Current release

The repository source is updated. The deployed website is still under private review; GitHub Pages automatic publishing is paused. Public website rollout and the portfolio production embed require the owner's approval.

- Private Sites review: https://sohila-learning-navigator.supertiger512.chatgpt.site
- Updated website: [Open the learning navigator on Vercel](https://sohila-learning-navigator.vercel.app/) — protected by Vercel Authentication.
- Direct deployment: https://sohila-learning-navigator-d8ur216fo.vercel.app/
- Vercel project: `sohila-learning-navigator`, authentication enabled for all deployments.
- Portfolio integration review: `portfolio-preview/` in either private deployment.

## Build and validate

```sh
python3 -m pip install -r requirements.txt
npm run check
npm run build
```

Serve `dist/` with any static server. The build uses the repository CSVs and Markdown; it does not fetch external content. Vercel accepts the prebuilt `dist/` as static files. See [Navigator engineering notes](docs/NAVIGATOR.md) for content maintenance, storage, build paths, deployment boundaries and portfolio integration.

## Project layout

| Path | Purpose |
| --- | --- |
| `web/` | Navigator UI, interaction logic and styles |
| `data/` | Original roadmap, technology and resource catalogs |
| `scripts/build_navigator.py` | Catalog normalization and full site build |
| `scripts/build_site.py` | Existing full documentation renderer |
| `tests/` | Source link preservation and catalog integrity |
| `docs/` | Roadmap guides, references and engineering notes |
| `integration/portfolio-site/` | Prepared portfolio source replacements |
| `dist/` | Generated static deployment output |

The recognizable resource catalogs, detailed roadmap, contributor guide, license, learning templates and original documentation remain intact. Duplicate conflict-marker blocks in the roadmap and technology CSVs were resolved without dropping rows.

Read the [full roadmap](ROADMAP.md), [resource guide](docs/RESOURCES.md), [capstone brief](docs/CAPSTONE.md), or the [previous repository guide](docs/REPOSITORY_GUIDE.md).
