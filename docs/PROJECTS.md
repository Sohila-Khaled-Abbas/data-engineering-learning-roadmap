# Mini-Projects by Phase

Complete these in order. Use public or synthetic data and include setup instructions, sample outputs, tests, and a concise explanation of decisions.

## 1. SQL analytics pack

**Build:** a small sales/orders schema plus 20 business questions.  
**Skills:** keys, joins, aggregation, CTEs, window functions, NULL/date handling, query plans.  
**Evidence:** SQL files, ERD, query results, and one measured tuning note.

## 2. Python data-quality CLI

**Build:** a command-line script that reads a CSV/JSON file, validates required columns and keys, profiles missing values and duplicates, and writes a cleaned output plus a quality report.  
**Skills:** Python, pandas, exceptions, logging, tests, file I/O.  
**Evidence:** source code, tests for valid/empty/malformed input, sample input/output, README.

## 3. Warehouse + BI report

**Build:** a fact/dimension model and one report with defined KPIs. Reconcile report totals against SQL.  
**Skills:** modeling, SQL, DAX/Power Query or Tableau, UX, storytelling.  
**Evidence:** data dictionary, model diagram, PBIX/TWB or screenshots, KPI definitions, three findings.

## 4. Orchestrated ETL pipeline

**Build:** ingest two sources, retain raw data, validate and transform them, load a curated output, and schedule the process with Airflow.  
**Skills:** APIs, Python, SQL, schema checks, idempotency, retries, logging.  
**Evidence:** pipeline code, DAG, run logs, failure/recovery test, runbook.

## 5. Distributed processing experiment

**Build:** transform a data set using PySpark, validate it against a SQL or pandas result, and document partitioning/runtime assumptions. Add Kafka only if an event-streaming use case is justified.  
**Skills:** DataFrames, execution trade-offs, file formats, batch vs. streaming.  
**Evidence:** runnable script/notebook, validation comparison, architecture decision note.

## 6. Capstone

Combine the strongest artifacts into one coherent, business-focused product. The goal is depth, not the number of products used. Use [`CAPSTONE.md`](CAPSTONE.md).
