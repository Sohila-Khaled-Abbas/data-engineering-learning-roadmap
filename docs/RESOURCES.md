# Learning Resources

Start with free, official documentation and focused practice. A paid course is optional; the deliverables are not.

[![Curated videos](https://img.shields.io/badge/video_library-16_resources-red?style=for-the-badge&logo=youtube)](../data/video-resources.csv)
[![Step-by-step roadmap](https://img.shields.io/badge/learning_order-step_by_step-2563eb?style=for-the-badge)](../ROADMAP.md)

> **Interactive previews:** [Open the HTML video gallery](VIDEO_LIBRARY.html). The gallery uses YouTube iframes for playlists and individual lessons. GitHub sanitizes iframe embeds in Markdown, so the interactive gallery must be served by GitHub Pages to render as a player. See [`PAGES_SETUP.md`](PAGES_SETUP.md) for the one-time GitHub Pages setting.

[![Companion roadmaps](https://img.shields.io/badge/companion_roadmaps-11_sources-7c3aed?style=for-the-badge)](REFERENCE_ROADMAPS.md)

[![Community learning catalog](https://img.shields.io/badge/community_catalog-100%20resources-2563eb?style=for-the-badge)](../data/community-learning-resources.csv)
[![Resource Explorer](https://img.shields.io/badge/open-resource%20explorer-0f766e?style=for-the-badge)](../learning-resources.html)
[![Companion roadmap references](https://img.shields.io/badge/companion_roadmaps-11_sources-7c3aed?style=for-the-badge)](REFERENCE_ROADMAPS.md)

## Expanded community learning catalog

Additional links have been extracted from the companion roadmaps and the public [Data Engineering Mentorship repository](https://github.com/ahmedshaaban1999/Data_Engineering_Mentorship). They include SQL practice, Python and pandas courses, dimensional modeling references, ETL/BI tracks, shell and Docker courses, Spark/Hadoop/Kafka/Airflow resources, cloud/dbt electives, and project briefs with source datasets.

**Start with the [Community Learning Resources guide](COMMUNITY_RESOURCES.md)** for a phase-by-phase selection, or open the [searchable Resource Explorer](../learning-resources.html) to filter the full [community resource CSV](../data/community-learning-resources.csv) by phase, type, title, skill, or source. The catalog preserves source attribution and flags paid or account-gated material when known. Verify current availability and pricing before enrolling.

## Curated video playlists and lessons

These community video resources are organized by the phase where they are most useful. They supplement the step-by-step roadmap; they do not replace coding, SQL practice, lab work, or project evidence. The full machine-readable index is [`data/video-resources.csv`](../data/video-resources.csv).

### Roadmap-wide overview

- [Data Engineering Roadmap — Overview Playlist](https://www.youtube.com/playlist?list=PLYkGz4lY93PVQFa1nQRy8lergfAMRevdO) — use as a broad walkthrough; watch the relevant videos alongside each phase rather than treating the playlist as a separate course to binge.
- [Companion roadmaps and references](REFERENCE_ROADMAPS.md) — external GitHub roadmaps, visual maps, an interactive roadmap site, a social post, and shared Notion/Gemini links. Links that could not be independently verified are labelled so.

### 1. Start with the environment and fundamentals — Phase 0

- [Network Fundamentals — video playlist](https://www.youtube.com/playlist?list=PLNFDrRZdysFycCObiCfCeYJx_lZJl7iPc) — IP/DNS/ports and the network path between applications and data services.
- [Operating Systems Fundamentals — video playlist](https://www.youtube.com/playlist?list=PLNFDrRZdysFwsFOnu-XqhemUHeWrPglU7) — processes, filesystems, memory and permissions.
- [Linux for Data Engineers — video lesson](https://youtu.be/gojeTqXdBH0) — practical Linux context; revisit when studying shell scripting and containers.

### 2. Learn relational data and SQL — Phase 1

- [Database Fundamentals — video playlist](https://www.youtube.com/playlist?list=PLO63i1is_Z_A)
- [Relational Model — short video lesson](https://youtu.be/JyCknfVW5uM)
- [SQL Server Fundamentals — video playlist (بشمهندس رامي)](https://youtube.com/playlist?list=PLoRh0POuk1Rw-BZU-DPI6cA_c5W9_2uF_) — an additional focused resource for learning with SQL Server; practise each concept in your own database and save the query scripts.
- [SQLBolt](https://sqlbolt.com/) — interactive SQL exercises.
- [PostgreSQL tutorial](https://www.postgresql.org/docs/current/tutorial.html) — official documentation.
- [Microsoft Learn — SQL Server performance tuning](https://learn.microsoft.com/en-us/sql/relational-databases/performance/monitor-and-tune-for-performance?view=sql-server-ver17)
- [Microsoft Learn — Query processing architecture](https://learn.microsoft.com/en-us/sql/relational-databases/query-processing-architecture-guide?view=sql-server-ver17)
- [Oracle Live SQL](https://livesql.oracle.com/) — optional Oracle practice.
- [Oracle PL/SQL Language Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/index.html)

### 3. Programming and Python — Phase 2

- [Programming Fundamentals — video playlist](https://www.youtube.com/playlist?list=PLPJ4DGyaHe1hxIQGFXxt-9_0PZzFXtkPM) — complete basic programming exercises first.
- [Python for Data Work — video playlist](https://www.youtube.com/playlist?list=PLNFDrRZdysFzSkNWqHZof7NxFHtGNC6bf) — focus on scripting and file handling before pandas/API work.
- [Python official tutorial](https://docs.python.org/3/tutorial/)
- [pandas getting started tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/)
- [OpenIntro Statistics](https://www.openintro.org/book/os/)

### 4. Shell scripting, pipelines and orchestration — Phase 6

- [Shell Scripting — video playlist](https://www.youtube.com/playlist?list=PLNFDrRZdysFyANzEXxzztUlGiCDxZs4Kp)
- [GNU Bash Reference Manual](https://www.gnu.org/s/bash/manual/bash.html)
- [Apache Airflow tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html)
- [GitHub Actions quickstart](https://docs.github.com/en/actions/writing-workflows/quickstart)

### 5. Containers and Linux operations — Phase 7

- [Docker Fundamentals — video playlist](https://www.youtube.com/playlist?list=PLNFDrRZdysFxkEsOLeJYBSisFAB65vbXe)
- [Docker Get Started](https://docs.docker.com/get-started/)
- [Linux System Administration I — video playlist](https://www.youtube.com/playlist?list=PLNFDrRZdysFwIftRRR9GM5ui5oM7HoqVA) — optional; use a disposable lab.
- [Linux System Administration II — video playlist](https://www.youtube.com/playlist?list=PLNFDrRZdysFyJSwqdEdZi_7S0r-JlVe3H) — optional continuation.
- [Red Hat documentation](https://docs.redhat.com/)

### 6. Big data and distributed processing — Phase 8

- [Hadoop and Big Data Engineering — video playlist](https://www.youtube.com/playlist?list=PLrooD4hY1QqAK5pbBpcthLuMa-cXnXJLE)
- [Apache Spark quick start](https://spark.apache.org/docs/latest/quick-start.html)
- [Apache Kafka quickstart](https://kafka.apache.org/quickstart/)
- [Apache Hadoop MapReduce tutorial](https://hadoop.apache.org/docs/stable1/mapred_tutorial.html)
- [Apache Hive tutorial](https://hive.apache.org/docs/latest/user/tutorial/)
- [Apache HBase documentation](https://hbase.apache.org/docs/)
- [Apache Pig documentation](https://pig.apache.org/docs/r0.17.0/)
- [Scala 3 tour](https://docs.scala-lang.org/tour/tour-of-scala.html)
- [AWS big data analytics options](https://docs.aws.amazon.com/whitepapers/latest/big-data-analytics-options/big-data-analytics-options.html)
- [Microsoft Learn — Get started with Fabric](https://learn.microsoft.com/en-us/training/paths/get-started-fabric/)
- [Microsoft Purview documentation](https://learn.microsoft.com/en-us/purview/)

### 7. Optional technology tracks — Phase 9

- [Java Programming — video playlist](https://www.youtube.com/playlist?list=PLNFDrRZdysFwoPGmJdV6GwnuDhoKg8Svw)
- [Dev.java — Learn Java](https://dev.java/learn/)
- [MongoDB Fundamentals — video playlist](https://www.youtube.com/playlist?list=PLesfn4TAj57XGGSmVzzpxY69-lha1EWEI)
- [MongoDB University](https://learn.mongodb.com/)
- [SAP BusinessObjects Web Intelligence help](https://help.sap.com/docs/SAP_BUSINESSOBJECTS_WEB_INTELLIGENCE?locale=en-US)
- [Incorta documentation](https://docs.incorta.com/)
- [IBM DataStage documentation](https://www.ibm.com/docs/en/iis/11.7.0)
- [Informatica PowerCenter documentation](https://docs.informatica.com/data-integration/powercenter/10-5.html)

### 8. Career and delivery skills — throughout the roadmap

- [GitHub Docs — Hello World](https://docs.github.com/en/get-started/start-your-journey/hello-world)
- [Official Scrum Guide](https://scrumguides.org/scrum-guide.html)
- [Purdue OWL — Professional and technical writing](https://owl.purdue.edu/owl/subject_specific_writing/professional_technical_writing/index.html)
- [Harvard FAS Career Services — Resume and cover letter resources](https://careerservices.fas.harvard.edu/resources/create-a-resume-cv-or-cover-letter/)
- [Upwork resources](https://www.upwork.com/resources)

## How to use each video resource

1. Watch one focused lesson or a small group of lessons; do not binge-watch entire playlists without practice.
2. Write three to five notes in your own words.
3. Recreate the concept in a lab or small exercise.
4. Change one input or requirement and test an edge case.
5. Commit evidence to your learning repository: script, SQL file, notes, diagram, test output or screenshot.
6. Mark the relevant phase complete only when you can explain the concept and reproduce the task.

**Link/access note:** video titles, playlists, software access, documentation paths, free tiers and exam requirements may change. Check the source page before relying on a resource. Some system administration exercises require a disposable VM; avoid destructive experiments on your main computer. Specialized or legacy platforms can be learned conceptually first if a compatible lab is unavailable.
