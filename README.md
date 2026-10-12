# Data Engineering Learning Roadmap

A practical, self-paced path from data fundamentals to analytics engineering and data pipelines. Learn in a simple order, build something at every stage, and keep proof of your work in GitHub.

> **The guiding rule:** learn the core skills first. Explore specialized and legacy platforms only after you understand the underlying data concepts or when a target role actually requires them.

## The learning path at a glance

| Step | Focus | Main technologies | Evidence to produce |
|---|---|---|---|
| 0 | Set up your workspace | Git, GitHub, VS Code, terminal, Python | Working environment and first repository |
| 1 | SQL and databases | PostgreSQL or SQL Server; basic Oracle SQL later | Schema, queries, joins, window functions |
| 2 | Python for data work | Python, pandas, requests, pytest | Tested data-cleaning script |
| 3 | Data quality and statistics | pandas, notebooks, SQL, charts | Profiling report and validation rules |
| 4 | Data modeling and warehousing | SQL, dimensional modeling, diagrams | Documented star schema |
| 5 | BI and storytelling | Power BI, Power Query, DAX; Tableau as an alternative | Report with reconciled KPIs |
| 6 | Data pipelines and orchestration | APIs, Python, SQL, Airflow, Bash | Repeatable pipeline with retries and logs |
| 7 | Engineering and deployment | Git, tests, CI, Docker, Linux | Reproducible project with automated checks |
| 8 | Big data fundamentals | Spark/PySpark first; Kafka; Hadoop/Hive concepts | Batch processing project and architecture notes |
| 9 | Specialized tools (optional) | MongoDB, Oracle PL/SQL, DataStage, Informatica, BusinessObjects, Incorta, Scala/HBase/Pig | Targeted labs based on access and career goals |
| 10 | Portfolio capstone | Your chosen core stack | End-to-end data product with documentation and demo |

The recommended order avoids studying many tools that solve similar problems at the same time. Choose **one primary SQL database**, **Python for general-purpose data scripting**, **Power BI for BI**, **Airflow for orchestration**, and **Docker for reproducible environments** before branching out.

## How to use this repository

1. Follow [`ROADMAP.md`](ROADMAP.md) in order. The phase timeboxes are suggestions, not deadlines.
2. Use [`docs/SKILL_MAP.md`](docs/SKILL_MAP.md) to see the skills and technologies grouped by priority.
3. Select resources from [`docs/RESOURCES.md`](docs/RESOURCES.md). Curated video playlists are grouped by phase; the structured index is [`data/video-resources.csv`](data/video-resources.csv). Prefer hands-on practice over collecting courses.
4. Complete at least one deliverable in each phase and record it in your own repository.
5. Build the capstone using [`docs/CAPSTONE.md`](docs/CAPSTONE.md).
6. Track each session by adding a short learning note or GitHub issue; use [`docs/ADD_VIDEO_RESOURCES.md`](docs/ADD_VIDEO_RESOURCES.md) to maintain the resource catalog.

## Suggested pacing

A practical baseline is **8–12 hours per week** for learning, exercises, and mini-projects. The capstone is a separate, larger build; a 300-hour target may take about 15 weeks at 20 hours/week or longer at a lighter pace. Adjust the schedule around your work, machine capability, and goals.

| Timebox | Goal |
|---|---|
| Weeks 1–4 | Workspace, networking/OS basics, SQL foundations |
| Weeks 5–8 | Analytical SQL and Python basics |
| Weeks 9–12 | Data quality, statistics, modeling and warehouse concepts |
| Weeks 13–15 | Power BI and analytical storytelling |
| Weeks 16–19 | APIs, pipeline design, Airflow and shell automation |
| Weeks 20–22 | Testing, Git workflow, CI/CD, Docker and deployment basics |
| Weeks 23–26 | Spark/PySpark, Kafka concepts and distributed data processing |
| Weeks 27 onward | Role-specific electives and capstone work |

This timebox is intentionally flexible. Do not move on because a week ended; move on when you can explain the concept, complete the lab, test an edge case, and show evidence.

## Definition of done

A topic is complete when you can:

- explain the core idea without reading the tutorial;
- complete a small hands-on exercise;
- test at least one edge case or failure path;
- save reproducible evidence (code, SQL, diagram, dashboard, test, or run log);
- document what you learned and what you would improve.

## Core stack vs. electives

**Core stack:** SQL + one relational database, Python + pandas, data modeling, Power BI (or Tableau), APIs, Airflow, Git, tests, Docker, and Spark fundamentals.

**Electives:** Oracle PL/SQL, MongoDB, Scala, Kafka in depth, Hadoop/HDFS, Hive/Impala, HBase, Pig, DataStage, Informatica PowerCenter, SAP BusinessObjects Web Intelligence/Universe, and Incorta. Some are specialized, enterprise-licensed, or legacy technologies. Learn their concepts and seek a suitable lab when required, but do not let tool access block the core path.

## Repository structure

```text
.
├── README.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── data/
│   ├── learning-roadmap.csv
│   ├── technology-map.csv
│   └── video-resources.csv
└── docs/
    ├── SKILL_MAP.md
    ├── RESOURCES.md
    ├── ADD_VIDEO_RESOURCES.md
    ├── PROJECTS.md
    ├── CAPSTONE.md
    └── PUBLISH_TO_GITHUB.md
```

## Publish it to GitHub

Follow [`docs/PUBLISH_TO_GITHUB.md`](docs/PUBLISH_TO_GITHUB.md) to create a repository named `data-engineering-learning-roadmap` and push these files.

## Start here

Open [`ROADMAP.md`](ROADMAP.md), begin with Phase 0, and commit your first evidence. Use [`data/video-resources.csv`](data/video-resources.csv) to match video resources to phases. Keep the process practical: fewer tools, more finished work.
