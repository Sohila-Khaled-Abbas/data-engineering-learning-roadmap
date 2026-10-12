# Skills and Technology Map

Use this as a lookup table, not as a mandate to install every product. **Core** means learn early; **Elective** means learn only when it serves a role or project.

## Core skills

| Priority | Skill area | Primary tools | What you should be able to do |
|---|---|---|---|
| Core | Computing and networking basics | Windows/PowerShell, Linux/WSL, terminal, curl, DNS tools | Navigate files, inspect processes, understand ports/HTTP, troubleshoot simple connections |
| Core | Version control | Git, GitHub | Commit changes, use branches, write a README, review a change |
| Core | Relational databases | PostgreSQL **or** SQL Server | Create tables/keys, define constraints, query and explain table grain |
| Core | Analytical SQL | SQL, CTEs, window functions | Join, aggregate, rank, deduplicate, handle NULLs and dates |
| Core | SQL performance | EXPLAIN/query plans, indexes | Measure a baseline and explain one safe optimization |
| Core | Python | Python 3, VS Code/Jupyter | Write reusable scripts, validate files, handle errors, log and test |
| Core | Data analysis and quality | pandas, notebook, charts, assertions | Profile, clean, test, reconcile and communicate data defects |
| Core | Statistics | Python/Excel, OpenIntro Statistics | Interpret distribution, variation, correlation and uncertainty |
| Core | Dimensional modeling | ERD tool, SQL, data dictionary | Define grain, facts/dimensions, keys and history |
| Core | BI and storytelling | Power BI, Power Query, DAX | Build a semantic model, reconcile KPIs, create a usable report |
| Core | APIs and ingestion | Python requests, REST/JSON, SQL | Build repeatable ingestion with schema checks and safe credentials |
| Core | Orchestration | Apache Airflow | Build DAGs, schedule tasks, set retries and read logs |
| Core | Shell automation | Bash or PowerShell | Automate repeatable jobs, check exit codes and capture logs |
| Core | Testing and CI | pytest, GitHub Actions | Check data/code automatically and stop a broken change |
| Core | Containers | Docker, Docker Compose | Package and rerun an environment consistently |
| Core | Project delivery | Agile/Scrum concepts, issues, README | Break work into milestones and define acceptance criteria |

## Elective or role-specific skills

| Category | Technologies | Transferable skills to learn |
|---|---|---|
| Additional relational/procedural SQL | Oracle SQL, PL/SQL | Dialect differences, packages, procedures/functions, cursors and exceptions |
| NoSQL/document databases | MongoDB | Document schema design, CRUD, aggregation and indexing |
| Java ecosystem | Java SE, OOP, Scala | Types, collections, interfaces, immutable transformations and tests |
| Distributed data processing | Spark, PySpark, Hadoop, HDFS | Partitioning, shuffle, distributed storage, batch jobs and fault tolerance |
| Streaming | Kafka | Topics, partitions, offsets, producers/consumers, event contracts and delivery trade-offs |
| SQL on large data | Hive, Impala | Partitioning, columnar formats, table layout and query planning |
| Specialized distributed storage | HBase | Wide-column models, row-key design and access patterns |
| Legacy data-flow scripting | Apache Pig | Data-flow operators and how they translate to SQL/dataframes |
| Enterprise ETL | IBM DataStage, Informatica PowerCenter | Source/target mapping, transformations, parameters, reject paths, jobs/workflows and logs |
| Enterprise reporting/semantic layer | SAP BusinessObjects Web Intelligence/Universe, Incorta | Semantic models, measures/dimensions, report validation and analytics workflows |
| Cloud data platforms | AWS, Azure, Microsoft Fabric, Databricks | Cloud storage/compute, IAM, cost, security, monitoring and managed data services |
| Visualization alternative | Tableau | Chart choice, calculated fields, dashboard actions and explanatory storytelling |
| Business context | Financial accounting, communication, presentations, career preparation | KPI definitions, stakeholder updates, clear demos and evidence-based portfolio writing |

## Role-based focus

- **BI Developer / Analyst:** SQL → data modeling → Power BI/DAX → storytelling → performance → capstone. Tableau may be an alternative.
- **Data Engineer:** SQL → Python → data quality → modeling → APIs → orchestration → Git/tests/Docker → Spark/Kafka → capstone.
- **ETL / Integration Specialist:** SQL → Python → data modeling → pipeline design → choose DataStage or Informatica if required by employer access.
- **Big Data Engineer:** SQL/Python → modeling → Spark/PySpark → distributed storage/query concepts → Kafka if the workload is streaming → cloud/platform tools.

You do not need to study all roles in depth at once. Start with the Core skills, finish one capstone, and then expand toward a target role.
