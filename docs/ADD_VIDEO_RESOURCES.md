# Add and maintain video resources

The YouTube links are stored in two places:

- [`docs/RESOURCES.md`](RESOURCES.md) is the human-readable catalog people browse on GitHub.
- [`data/video-resources.csv`](../data/video-resources.csv) is the sortable/indexable catalog with IDs, phases and practice notes.

The CSV is the source of truth for the structured list. Keep both files in sync when adding or renaming a resource.

## Suggested learning order

1. **Phase 0:** Network Fundamentals, Operating Systems Fundamentals, Linux for Data Engineers.
2. **Phase 1:** Database Fundamentals, then the Relational Model lesson alongside hands-on SQL.
3. **Phase 2:** Programming Fundamentals first, followed by Python for Data Work.
4. **Phase 6:** Shell Scripting, after basic programming and terminal use.
5. **Phase 7:** Docker Fundamentals. Take Linux System Administration I and II only if you need deeper operating-system skills or your target role requires them.
6. **Phase 8:** Hadoop and Big Data Engineering after you are comfortable with SQL, Python, and basic data pipelines.
7. **Phase 9:** Java and MongoDB are electives; choose them for a project or target role rather than doing both by default.

Do not treat this as a requirement to finish every video. Select only the lessons needed to learn the phase's skill and complete its deliverable.

## Add another resource

1. Open `data/video-resources.csv` in a spreadsheet editor or text editor.
2. Add a row using the existing columns: `Resource ID`, `Title`, `Skill Area`, `Format`, `Recommended Phase`, `Priority`, `URL`, `How to Use It`.
3. Give the resource a unique ID such as `V015`.
4. Use a clean canonical URL when possible. For YouTube playlists, preserve the playlist ID (`list=...`) and remove only optional tracking parameters such as `si=...`.
5. Add the link under the matching phase in `docs/RESOURCES.md`, with a short note about how to use it.
6. If the resource changes the recommended learning order, update `ROADMAP.md` as well.
7. Check that the links open and that repository files contain no personal tokens, private URLs or private data.

## Publish your updates

### If you have not created the GitHub repository yet

1. Download and extract the updated ZIP bundle.
2. Create a new GitHub repository named `data-engineering-learning-roadmap`.
3. Upload the contents of the extracted folder, not the ZIP file itself. Preserve the `data/` and `docs/` folders.
4. Commit with the message `Add curated video learning resources`.

### If your GitHub repository already exists

Open a terminal in the local clone of `data-engineering-learning-roadmap` and copy the changed files into it. Then run:

```bash
git status
git add README.md ROADMAP.md docs/RESOURCES.md docs/ADD_VIDEO_RESOURCES.md data/video-resources.csv data/learning-roadmap.csv
git commit -m "Add curated video learning resources"
git push
```

If this is a newly initialized folder rather than an existing clone, follow [`PUBLISH_TO_GITHUB.md`](PUBLISH_TO_GITHUB.md) first. Do not run `git init` or `git remote add origin` again in an already connected repository.
