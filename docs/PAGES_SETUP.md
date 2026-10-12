# Enable the interactive video gallery

The resource list is readable directly in GitHub. To use embedded YouTube players, search/filter controls, and the full responsive gallery, publish the `docs/` folder through GitHub Pages.

## One-time repository setting

1. Open [the repository's Settings](https://github.com/Sohila-Khaled-Abbas/data-engineering-learning-roadmap/settings/pages).
2. Under **Build and deployment**, choose **GitHub Actions** as the source.
3. Save the setting if GitHub shows a save button.
4. Open the [Actions tab](https://github.com/Sohila-Khaled-Abbas/data-engineering-learning-roadmap/actions) and open **Deploy learning resource site**.
5. If no run appears yet, use **Run workflow** on the `main` branch. A later push to `docs/` will also trigger deployment.
6. Wait for the workflow to complete successfully.

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
