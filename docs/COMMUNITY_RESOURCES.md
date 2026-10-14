# Community Learning Resources

[![Indexed resources](https://img.shields.io/badge/community_catalog-100%20resources-2563eb?style=for-the-badge)](../data/community-learning-resources.csv)
[![Explore resources](https://img.shields.io/badge/open-searchable%20resource%20explorer-0f766e?style=for-the-badge)](../learning-resources.html)
[![Skill-first order](https://img.shields.io/badge/study_order-follow%20the%20roadmap-16a34a?style=for-the-badge)](../ROADMAP.md)

This catalog brings together additional learning resources extracted from the linked community roadmaps and the public [Data Engineering Mentorship repository](https://github.com/ahmedshaaban1999/Data_Engineering_Mentorship). It includes tutorials, official documentation, practice sites, videos, dataset links, and project briefs.

**Use the [searchable resource explorer](../learning-resources.html) to filter the full catalog** by phase, resource type, title, skill, or source. The downloadable index is [data/community-learning-resources.csv](../data/community-learning-resources.csv).

> **Interactive catalog on this page:** after the topic guide, use search and phase/type filters to explore all community entries. Every resource card links to the original source in a new tab; YouTube resources also offer an on-page **Preview here** player. For one search across community links, curated videos, and companion roadmaps, open the [combined Resource Explorer](../learning-resources.html).

## A guided route through these resources

<details>
<summary><strong>01 — SQL and database foundations</strong></summary>

Start with one relational database and combine learning with query practice.

- [DataLemur SQL Tutorial](https://datalemur.com/sql-tutorial) — business-style SQL practice.
- [SQLZoo](https://sqlzoo.net/wiki/SQL_Tutorial) — interactive SQL exercises.
- [Mode SQL Tutorial](https://mode.com/sql-tutorial/introduction-to-sql/) — analytical SQL explanations.
- [HackerRank SQL](https://www.hackerrank.com/domains/sql) and [LeetCode Database Problems](https://leetcode.com/problemset/database/) — structured practice after learning the basics.
- [CMU Introduction to Database Systems](https://www.youtube.com/playlist?list=PLSE8ODhjZXjbj8BMuIrRcacnQh20hmY9g) — deeper database internals.
- [Relational Database playlist](https://www.youtube.com/playlist?list=PLSGEGD0dbMKrvd5ppnyFLm7q3xEH97T-t) — an additional learning path from the IEEE ManCSC roadmap.

**Deliverable:** a small schema, a set of tested queries, and explanations for joins, aggregates, CTEs, and window functions.
</details>

<details>
<summary><strong>02 — Python, pandas, and data preparation</strong></summary>

Pick one structured course, then practise with a real dataset.

- [Python Basics for Data Science — Cognitive Class](https://cognitiveclass.ai/courses/python-for-data-science).
- [CS50's Introduction to Programming with Python](https://pll.harvard.edu/course/cs50s-introduction-programming-python).
- [Data Manipulation with pandas](https://app.datacamp.com/learn/courses/data-manipulation-with-pandas) and [Joining Data with pandas](https://app.datacamp.com/learn/courses/joining-data-with-pandas).
- [Introduction to Importing Data in Python](https://app.datacamp.com/learn/courses/introduction-to-importing-data-in-python) and [Cleaning Data in Python](https://app.datacamp.com/learn/courses/cleaning-data-in-python).
- For Arabic-language alternatives, see the [Python learning playlist](https://www.youtube.com/playlist?list=PL6-3IRz2XF5UM-FWfQeF1_YhMMa12Eg3s).

**Deliverable:** a reusable script that ingests, validates, cleans, and writes a dataset.
</details>

<details>
<summary><strong>03 — Data modeling and warehousing</strong></summary>

Use a business process to practise grain, facts, dimensions and source-to-target mapping.

- [Garage Education — Data Warehouse Concepts and Modeling](https://www.youtube.com/playlist?list=PLxNoJq6k39G_m6DYjpz-V92DkaQEiXxkF).
- [Bank Data Model](https://dwbi1.wordpress.com/2012/04/28/bank-data-model/) — review a concrete domain model.
- [One Big Table vs Kimball vs Relational](https://www.youtube.com/watch?v=ltQgbSs99WU) — compare trade-offs.
- [Data Warehouse Toolkit — publisher page](https://www.oreilly.com/library/view/the-data-warehouse/9781118530801/) — book reference; access may require purchase or subscription.
- [Databricks data warehousing concepts](https://www.databricks.com/discover/data-warehousing-concepts) — concepts and architecture context.

**Deliverable:** a documented star schema, data dictionary, and quality rules. Do not copy another model without explaining the grain and business purpose.
</details>

<details>
<summary><strong>04 — ETL, BI, and data quality</strong></summary>

- [ETL and ELT in Python](https://app.datacamp.com/learn/courses/etl-and-elt-in-python) — Python pipeline concepts.
- [SSIS ETL tutorials — Wise Owl](https://www.youtube.com/playlist?list=PLNIs-AWhQzcmPg_uV2BZi_KRG4LKs6cRs) — optional Microsoft-specific ETL track.
- [Power BI Arabic playlist](https://www.youtube.com/playlist?list=PL69umUTzySPGWMxnmhX9SV5PIEbdnHv63) — free language alternative listed by the weekly roadmap.
- [Seattle Data Guy — data quality](https://www.youtube.com/watch?v=wvUiRHd47M0) and [Understanding Data Quality](https://www.youtube.com/watch?v=MnxE8_FK-Dc) — background for designing validation checks.

**Deliverable:** a pipeline with observable quality checks plus a BI report whose headline metrics reconcile with SQL.
</details>

<details>
<summary><strong>05 — Linux, Git, Docker, and automation</strong></summary>

- [Atlassian Git tutorial](https://www.atlassian.com/git) — commits, branching, merging, and conflict resolution.
- [Getting started with Linux Terminal Commands — Cognitive Class](https://cognitiveclass.ai/courses/course-v1:IBMSkillsNetwork+GPXX06VPEN+v1).
- [Bash Scripting Tutorial — freeCodeCamp](https://www.freecodecamp.org/news/bash-scripting-tutorial-linux-shell-script-and-command-line-for-beginners/).
- [Docker Essentials — Cognitive Class](https://cognitiveclass.ai/courses/docker-essentials) and [Docker practical video course in Arabic](https://www.youtube.com/watch?v=tHP5IWfqPKk&list=PLzNfs-3kBUJnY7Cy1XovLaAkgfjim05RR).

**Deliverable:** a version-controlled pipeline that can be run from written instructions and, where practical, from Docker.
</details>

<details>
<summary><strong>06 — Orchestration, streaming, and big data</strong></summary>

- [Airflow tutorial for beginners](https://www.youtube.com/watch?v=K9AnJ9_ZAXE&list=PLwFJcsJ61oujAqYpMp1kdUBcPG0sE0QMT) and [Introduction to Apache Airflow in Python](https://app.datacamp.com/learn/courses/introduction-to-apache-airflow-in-python).
- [Spark Foundation Training](https://www.learningjournal.guru/courses/spark/spark-foundation-training/) and [SparkByExamples PySpark tutorials](https://sparkbyexamples.com/pyspark-tutorial/).
- [PySpark in Arabic](https://www.youtube.com/playlist?list=PLJM7jJIw2GC2tPeonyPveb7Y9AggQSGuo) and [Apache Spark / Scala tutorials](https://www.youtube.com/playlist?list=PLEiEAq2VkUUK3tuBXyd01meHuDj7RLjHv).
- [Hadoop Foundation Training](https://www.learningjournal.guru/courses/hadoop/hadoop-foundation-training/), [Introduction to Hadoop — Cognitive Class](https://cognitiveclass.ai/courses/introduction-to-hadoop), and [Hive tutorial video](https://www.youtube.com/watch?v=rr17cbPGWGA).
- [Avro overview](https://sqream.com/blog/a-detailed-introduction-to-the-avro-data-format/) and [Parquet format overview](https://towardsdatascience.com/demystifying-the-parquet-file-format-13adb0206705).
- [Kafka Foundation Training](https://www.learningjournal.guru/courses/kafka/kafka-foundation-training/) — pair with the official Kafka quickstart already listed in the main resources.

**Deliverable:** a small Spark transformation and a separate Kafka producer/consumer or Airflow DAG. Specialised cluster setup can wait until these concepts make sense.
</details>

<details>
<summary><strong>07 — Cloud, Snowflake, and dbt electives</strong></summary>

Choose only the track that matches your role or project. Some items below are paid or require accounts.

- [AWS Skill Builder — Cloud Essentials](https://explore.skillbuilder.aws/learn/lp/82/cloud-essentials-knowledge-badge-readiness-path) — cloud concepts.
- [AWS Certified Cloud Practitioner notes on GitHub](https://github.com/kennethleungty/AWS-Certified-Cloud-Practitioner-Notes/tree/main) — community revision aid; compare with current official objectives.
- [Snowflake introduction](https://app.datacamp.com/learn/courses/introduction-to-snowflake) and [data modeling in Snowflake](https://app.datacamp.com/learn/courses/introduction-to-data-modeling-in-snowflake).
- [Introduction to dbt](https://app.datacamp.com/learn/courses/introduction-to-dbt) and [dbt video playlist](https://www.youtube.com/playlist?list=PLy4OcwImJzBLJzLYxpxaPUmCWp8j1esvT).
- [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) — a project-oriented end-to-end course.

**Deliverable:** one justified platform choice, a working project, and notes about cost, identity, storage, and operational trade-offs.
</details>

## Project-based practice from the mentorship repository

These are project briefs and dataset sources found in the public [Data Engineering Mentorship repository](https://github.com/ahmedshaaban1999/Data_Engineering_Mentorship):

- [Airbnb Barcelona warehouse project](https://github.com/ahmedshaaban1999/Data_Engineering_Mentorship/tree/main/level_1/Data_Modeling/projects/airbnb) — source dataset: [Inside Airbnb](http://insideairbnb.com/get-the-data/).
- [E-commerce warehouse and ETL project](https://github.com/ahmedshaaban1999/Data_Engineering_Mentorship/tree/main/level_1/Data_Modeling/projects/ecommerce).
- [PixelFed warehouse modeling project](https://github.com/ahmedshaaban1999/Data_Engineering_Mentorship/tree/main/level_1/Data_Modeling/projects/pixelfed) — schema reference: [DrawSQL PixelFed template](https://drawsql.app/templates/pixelfed).
- [Transfermarkt schema and file-format project](https://github.com/ahmedshaaban1999/Data_Engineering_Mentorship/tree/main/level_1/Data_Modeling/projects/transferMarket) — dataset: [Player scores on Kaggle](https://www.kaggle.com/datasets/davidcariboo/player-scores).
- [Kafka log-reader project](https://github.com/ahmedshaaban1999/Data_Engineering_Mentorship/tree/main/level_1/Kafka/projects/logs_reader) — sample logs: [LogHub Apache access log](https://github.com/logpai/loghub/blob/master/Apache/Apache_2k.log).
- [Spark GitHub repository analytics](https://github.com/ahmedshaaban1999/Data_Engineering_Mentorship/tree/main/level_1/Spark/projects/github_repos) — source dataset: [Top GitHub repositories](https://www.kaggle.com/datasets/anshulmehtakaggl/top-1000-github-repositories-for-multiple-domains?select=Spark.json).
- [Spark NASA Near-Earth Objects project](https://github.com/ahmedshaaban1999/Data_Engineering_Mentorship/tree/main/level_1/Spark/projects/n.e.o) — source dataset: [NASA NEO data on Kaggle](https://www.kaggle.com/datasets/ivansher/nasa-nearest-earth-objects-1910-2024).
- [TMDB genre aggregation project](https://github.com/ahmedshaaban1999/Data_Engineering_Mentorship/tree/main/level_1/Spark/projects/tmdb).

These briefs provide project ideas. Rebuild your own solutions and document your design choices instead of copying another repository's files.

## Catalog and attribution notes

- The full structured list lives in [data/community-learning-resources.csv](../data/community-learning-resources.csv).
- Sources are kept with their entries so you can identify which community roadmap introduced each resource.
- Providers, prices, login requirements, free tiers and course availability can change. Verify them before paying.
- The catalog links to external materials; it does not rehost other repositories' files or copy their roadmaps.
- The added mentorship repository is a public fork of [OmarEhab007/Data_Engineering_Mentorship](https://github.com/OmarEhab007/Data_Engineering_Mentorship). Credit stays with the original publishers and upstream project.
