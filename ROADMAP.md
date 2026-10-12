# Step-by-Step Roadmap

The route below is ordered by dependency: fundamentals first, then analytics, pipelines, engineering practices, distributed systems, electives, and a capstone.

## Quick video resource map

Use the playlists as support material, not as a replacement for labs. Open the [interactive YouTube gallery](https://sohila-khaled-abbas.github.io/data-engineering-learning-roadmap/VIDEO_LIBRARY.html) for lazy-loaded playlist/video previews and search/filter controls. The full catalog is in [`docs/RESOURCES.md`](docs/RESOURCES.md) and [`data/video-resources.csv`](data/video-resources.csv).

| Phase | Recommended video resources |
|---|---|
| 0 — Workspace and fundamentals | [Network Fundamentals](https://www.youtube.com/playlist?list=PLNFDrRZdysFycCObiCfCeYJx_lZJl7iPc), [Operating Systems Fundamentals](https://www.youtube.com/playlist?list=PLNFDrRZdysFwsFOnu-XqhemUHeWrPglU7), [Linux for Data Engineers](https://youtu.be/gojeTqXdBH0) |
| 1 — SQL and databases | [Database Fundamentals](https://www.youtube.com/playlist?list=PLO63i1is_Z_A), [Relational Model](https://youtu.be/JyCknfVW5uM), [SQL Server Fundamentals — بشمهندس رامي](https://www.youtube.com/playlist?list=PLoRh0POuk1Rw-BZU-DPI6cA_c5W9_2uF_) |
| 2 — Programming and Python | [Programming Fundamentals](https://www.youtube.com/playlist?list=PLPJ4DGyaHe1hxIQGFXxt-9_0PZzFXtkPM), then [Python for Data Work](https://www.youtube.com/playlist?list=PLNFDrRZdysFzSkNWqHZof7NxFHtGNC6bf) |
| 6 — Pipelines and orchestration | [Shell Scripting](https://www.youtube.com/playlist?list=PLNFDrRZdysFyANzEXxzztUlGiCDxZs4Kp) |
| 7 — Engineering and deployment | [Docker Fundamentals](https://www.youtube.com/playlist?list=PLNFDrRZdysFxkEsOLeJYBSisFAB65vbXe); optional [Linux Administration I](https://www.youtube.com/playlist?list=PLNFDrRZdysFwIftRRR9GM5ui5oM7HoqVA) and [II](https://www.youtube.com/playlist?list=PLNFDrRZdysFyJSwqdEdZi_7S0r-JlVe3H) |
| 8 — Big data | [Hadoop and Big Data Engineering](https://www.youtube.com/playlist?list=PLrooD4hY1QqAK5pbBpcthLuMa-cXnXJLE) |
| 9 — Electives | Optional [Java Programming](https://www.youtube.com/playlist?list=PLNFDrRZdysFwoPGmJdV6GwnuDhoKg8Svw) and [MongoDB Fundamentals](https://www.youtube.com/playlist?list=PLesfn4TAj57XGGSmVzzpxY69-lha1EWEI) |

## Phase 0 — Prepare your workspace

**Suggested time:** 1 week  
**Tools:** VS Code, Git, GitHub, terminal/PowerShell, Python 3, virtual environments  
**Skills:** files and paths, package installation, environment variables, version control, basic HTTP/networking, OS processes and permissions.

### Do
- Install the tools you need and record versions.
- Learn `cd`, `pwd`, `ls`/`dir`, file operations, environment variables, `git status`, `git add`, `git commit`, and `git push`.
- Understand DNS, IP/ports, HTTP/HTTPS, and how an application connects to a database/API.

**Deliverable:** a repository with a README, a Python script, and a short environment/setup note.

**Exit check:** you can recreate your environment from written instructions and commit a change.

## Phase 1 — SQL and relational databases

**Suggested time:** 3–4 weeks  
**Choose one database first:** PostgreSQL or SQL Server. Learn Oracle SQL later if your target role needs it.  
**Skills:** tables and keys, constraints, normalization, SELECT/WHERE, JOIN, GROUP BY, CASE, subqueries, CTEs, window functions, dates/NULLs, transactions, indexes, query plans.

### Do
- Create a small sales, orders, or library database.
- Answer 20 business questions with SQL.
- Include joins, aggregates, CTEs, and window functions.
- Inspect one query plan and measure one tuning improvement.

**Deliverable:** schema/ERD, SQL scripts, query explanations, and one before/after tuning note.

**Exit check:** you can explain query grain, duplicate risks, NULL handling, and why a query or index helped.

## Phase 2 — Python for data work

**Suggested time:** 3 weeks  
**Tools:** Python, pandas, requests, Jupyter or VS Code, pytest  
**Skills:** functions, collections, modules, files, CSV/JSON, exceptions, logging, data types, joins/aggregations with pandas, HTTP requests, testing.

### Do
- Write a script to read a raw file or public API response.
- Validate required columns, types, keys, nulls and duplicates.
- Clean the data and save a curated CSV or Parquet file.
- Add tests for valid data, empty data, and malformed records.

**Deliverable:** reusable Python ETL script/notebook, tests, sample input/output, and README.

**Exit check:** your script has clear errors, can be rerun, and produces a testable result.

## Phase 3 — Data quality and basic statistics

**Suggested time:** 2 weeks  
**Tools:** SQL, pandas, notebook, spreadsheet, Matplotlib  
**Skills:** completeness, validity, uniqueness, distributions, missingness, outliers, sampling, variability, correlation vs. causation, basic inference, reconciliation.

### Do
- Profile a messy dataset.
- Define measurable data-quality rules.
- Compare row counts and key metrics before/after cleaning.
- Explain findings and limitations in plain language.

**Deliverable:** a data profile, quality scorecard, and remediation log.

**Exit check:** you can distinguish a data defect from a genuine pattern and explain your assumptions.

## Phase 4 — Data modeling and warehousing

**Suggested time:** 2–3 weeks  
**Tools:** PostgreSQL/SQL Server, diagrams.net or dbdiagram.io, data dictionary  
**Skills:** OLTP vs. OLAP, grain, facts/dimensions, star schema, surrogate keys, date dimensions, slowly changing dimensions, conformed dimensions, lineage, ownership, governance.

### Do
- Pick a business process and state the grain before drawing a model.
- Design fact and dimension tables.
- Document keys, definitions, source mappings, and history requirements.
- Add data-quality checks and explain lineage from source to report.

**Deliverable:** ERD/star schema, data dictionary, source-to-target mapping, and quality rules.

**Exit check:** you can explain why each table exists, what one row represents, and how measures are calculated.

## Phase 5 — BI and data storytelling

**Suggested time:** 2 weeks  
**Primary tool:** Power BI with Power Query and DAX. Tableau is a valid alternative; learning both deeply at once is optional.  
**Skills:** semantic modeling, relationships, measures, filter context, visuals, dashboard navigation, accessibility, KPI definitions, narrative.

### Do
- Connect to your curated dataset/model.
- Build measures and reconcile important totals back to SQL.
- Create a report with overview and diagnostic paths.
- Write three evidence-backed business insights and one limitation.

**Deliverable:** PBIX or Tableau workbook, model diagram, KPI dictionary, report screenshots, and insight summary.

**Exit check:** report totals match the source logic and a stakeholder can answer a real question without guidance.

## Phase 6 — APIs, pipelines, and orchestration

**Suggested time:** 3–4 weeks  
**Tools:** Python, REST APIs, SQL database, Apache Airflow, Bash  
**Skills:** ingestion, pagination/rate limits, source contracts, staging/curated layers, idempotency, scheduling, dependencies, retries, backfills, logs, recovery.

### Do
- Ingest data from a file and a public API (or two sample sources).
- Separate raw, staging, and curated outputs.
- Build an Airflow DAG that runs ingest → validate → transform → load.
- Test a bad input and an intentional task failure; show how the pipeline recovers.

**Deliverable:** pipeline code, DAG, logs, tests, data-flow diagram, and runbook.

**Exit check:** the pipeline can rerun without duplicate side effects and failure behavior is documented.

## Phase 7 — Engineering practices and deployment

**Suggested time:** 2–3 weeks  
**Tools:** Git/GitHub, pytest, GitHub Actions, Docker/Compose, Linux/WSL, ShellCheck  
**Skills:** modular code, tests, pull requests, CI, environment configuration, secrets hygiene, container images, volumes, networking, logs, setup documentation.

### Do
- Add automated tests and linting.
- Run checks on pushes/pull requests with GitHub Actions.
- Containerize the pipeline if it improves reproducibility.
- Confirm a clean setup works from the README.

**Deliverable:** test suite, passing CI workflow, Dockerfile/Compose file where useful, and reproducible setup instructions.

**Exit check:** someone else can clone the project, configure it safely, run tests, and reproduce the result.

## Phase 8 — Big data and distributed processing

**Suggested time:** 3–4 weeks for fundamentals; deepen only as needed.  
**Order:** Spark/PySpark → partitioning and file formats → Kafka concepts → Hadoop/HDFS, Hive/Impala, and other ecosystem tools as needed.  
**Skills:** DataFrames, lazy evaluation, transformations/actions, joins, shuffles, partitions, Parquet, topics/partitions/offsets, distributed storage and batch processing trade-offs.

### Do
- Reimplement a familiar transformation using PySpark.
- Compare its output with SQL or pandas on a controlled sample.
- Explain when batch is sufficient and when streaming is justified.
- Build a small Kafka producer/consumer demo only after the processing basics are comfortable.

**Deliverable:** reproducible PySpark job, validation comparison, and a distributed architecture decision note.

**Exit check:** you can explain the data volume, latency, partitioning, operational, and cost trade-offs without relying only on buzzwords.

## Phase 9 — Choose electives by role

**Suggested time:** 1–3 weeks per chosen elective; not all electives are required.

| If you need… | Study… | Key skills |
|---|---|---|
| Oracle-heavy environments | Oracle SQL and PL/SQL | Packages, procedures/functions, cursors, exceptions, query behavior |
| Document databases | MongoDB | Document modeling, CRUD, aggregation, indexing, embedding vs. referencing |
| JVM data processing | Java and Scala | OOP, collections, functions, streams, tests |
| Legacy Hadoop stacks | Pig, Hive/Impala, HBase | Data flow, SQL-on-Hadoop, row-key/access patterns, storage trade-offs |
| Enterprise ETL | IBM DataStage or Informatica PowerCenter | Mappings, transformations, sessions/jobs, parameters, rejects, logging |
| Enterprise BI platforms | SAP BusinessObjects WebI/Universe or Incorta | Semantic layer, business objects, data modeling, reporting, data ingestion |
| Cloud-first engineering | AWS, Azure/Fabric, Databricks | Cloud storage/compute, IAM, orchestration, observability, cost/security |

**Rule:** choose only one or two electives based on a real role description or project requirement. Some platforms need licensed access; some legacy tools may be difficult to run locally. Equivalent practice is useful for transferable concepts but is not the same as completing an official product lab.

**Deliverable:** one focused lab and a short comparison explaining when the technology is appropriate.

## Phase 10 — Build the portfolio capstone

**Suggested effort:** target 300 hours; split it into milestones at your own pace.  
**Full checklist:** [`docs/CAPSTONE.md`](docs/CAPSTONE.md).

Build one end-to-end project that has a real question, repeatable ingestion, quality checks, a well-modeled analytical layer, orchestration, tests, a dashboard, documentation, and a demo. A single polished project is more useful than many half-finished tool demos.

**Final deliverable:** a public-ready repository with architecture diagrams, data dictionary, code, tests, runbook, screenshots/demo, limitations, and business findings.

## Career skills — practice throughout

Keep notes readable, use issue trackers and pull requests, write status updates, explain decisions, practice short demos, and maintain a role-focused CV. At the end, rehearse a 5–7 minute capstone presentation and a technical interview walk-through.
