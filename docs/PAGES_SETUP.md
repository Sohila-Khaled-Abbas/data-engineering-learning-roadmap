# Enable the interactive video gallery

The resource list is readable directly in GitHub. To use embedded YouTube players, search/filter controls, and the full responsive gallery, publish the `docs/` folder through GitHub Pages. The workflow is committed, but Pages needs one manual repository setting before it can deploy. The previous first-run attempt returned `Get Pages site failed (404)`; using `enablement: true` also returned `Resource not accessible by integration`, so the workflow no longer attempts to change repository-level settings automatically.

## One-time repository setting

1. Open [the repository's Pages settings](https://github.com/Sohila-Khaled-Abbas/data-engineering-learning-roadmap/settings/pages).
2. Under **Build and deployment**, set **Source** to **GitHub Actions**. If the setting offers a save button, save it.
3. Open the [Actions tab](https://github.com/Sohila-Khaled-Abbas/data-engineering-learning-roadmap/actions) and choose **Deploy learning resource site**.
4. Click **Run workflow** for the `main` branch, or push a new change under `docs/` to trigger it.
5. Wait for the workflow to complete successfully.

## Open the gallery

After successful deployment, use:

- [Interactive video library](https://sohila-khaled-abbas.github.io/data-engineering-learning-roadmap/VIDEO_LIBRARY.html)
- [GitHub Pages home](https://sohila-khaled-abbas.github.io/data-engineering-learning-roadmap/)

The repository README and source files remain hosted on GitHub; the static site publishes only `docs/`. Links in the player page send visitors back to the GitHub versions of the README, roadmap, and CSV index.

## Notes about embeds

- The gallery uses privacy-enhanced YouTube embed URLs and lazy-loading iframes.
- A playlist player allows viewers to browse a playlist; a video player embeds one lesson.
- GitHub Markdown does not render arbitrary HTML iframes on a README or normal Markdown page. Use the GitHub Pages gallery for working players.
- YouTube playback, embedded-cookie behavior, and playlist availability remain controlled by YouTube and each video's settings.
- The workflow uses GitHub-maintained Actions to publish the static files from `docs/`. Review action versions and repository policies periodically.
