# Hosting the unified learning website

The same `dist/` build contains the interactive roadmap, resource library, videos, all documentation, templates, and original CSV downloads. Every page shares the Learning Studio design. The historical GitHub Pages URLs redirect to their matching pages in the unified website.

## Current protected website

[Open the updated website on Vercel](https://data-engineering-learning-roadmap.vercel.app/). Vercel Authentication is enabled for every deployment. The private Sites copy is available at https://data-engineering-learning-roadmap.supertiger512.chatgpt.site.

The public GitHub source is updated. Public website rollout is awaiting the owner's approval. The GitHub Pages workflow runs manually and only when `public_release_approved` is checked. Source pushes cannot publish the website automatically.

## Build locally

```sh
python3 -m pip install -r requirements.txt
npm run check
npm run build
```

This emits the full website in `dist/`. Serve this directory with a static web server. Vercel uses a prebuilt deployment and does not install Python or build the source remotely.

## GitHub Pages release after approval

1. In repository Settings → Pages, use GitHub Actions as the deployment source.
2. In Actions, open the build-and-deploy documentation workflow.
3. Run it on `main` and check the public-release approval input only after the owner has approved release.
4. The workflow sets `NAVIGATOR_BASEURL=/data-engineering-learning-roadmap`, builds the unified site, and uploads `dist/`.
5. Verify the roadmap, guides, original video-library URLs and resource downloads.

The existing Pages URL remains https://sohila-khaled-abbas.github.io/data-engineering-learning-roadmap/. Updating the repository does not itself replace that deployed version.

## Portfolio integration

Copy a navigator build made with `NAVIGATOR_BASEURL=/learning-navigator` into the portfolio's `learning-navigator-dist/` directory. The prepared portfolio build-script replacement copies that into its own output. The `/learn/` page embeds this same-origin app and includes a full-page link.

## Videos and learning progress

YouTube players load after **Watch here** is clicked. Original source links remain available when a creator prevents embedding. Progress and bookmarks are local to each origin; use export/import when switching hosts.
