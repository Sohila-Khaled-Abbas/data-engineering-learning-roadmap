# Publish this roadmap to GitHub

The folder/ZIP is ready to upload, but it has not been published to your GitHub account automatically. Use one of the options below.

## Option A — GitHub website (no terminal commands)

1. Open [GitHub](https://github.com/) and sign in.
2. Click **New repository**.
3. Enter repository name: `data-engineering-learning-roadmap`.
4. Add a description such as: `A practical, self-paced roadmap for SQL, Python, analytics engineering, data pipelines, big data, and portfolio projects.`
5. Choose **Public** if you want recruiters to view it, or **Private** while you are still preparing it.
6. Do not initialize another README, license, or `.gitignore` because this bundle already includes them.
7. Create the repository.
8. Extract the downloaded ZIP on your computer.
9. On the new repository page, choose **Add file → Upload files**.
10. Drag the files and folders from the extracted `data-engineering-learning-roadmap` directory into the upload area. Upload the contents of the directory, including hidden `.gitignore` and `.github` files if your browser/file picker supports them.
11. Enter a commit message such as `Add initial data engineering learning roadmap` and click **Commit changes**.
12. Open the README on GitHub and check that the links and folder structure look correct.

If the browser upload does not preserve `.github/ISSUE_TEMPLATE`, use Option B below.

## Option B — Git command line

Prerequisites: Git installed and a GitHub account. Create an **empty** repository named `data-engineering-learning-roadmap` on GitHub first, without adding a README, license, or `.gitignore`.

Open a terminal in the extracted project directory and run:

```bash
git init
git add .
git commit -m "Add initial data engineering learning roadmap"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/data-engineering-learning-roadmap.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. GitHub may ask you to authenticate through a browser or credential manager. Do not paste a personal access token into this README or commit it to the repository.

## Before making the repo public

- [ ] Confirm the README has no private names, personal information, credentials or machine-specific paths.
- [ ] Verify the resource links you intend to keep.
- [ ] Read the license and decide if MIT fits your intended use.
- [ ] Add your own learning logs or project evidence only when it is safe to publish.
- [ ] Make the repository description and topics reflect the skills you actually want to demonstrate.
