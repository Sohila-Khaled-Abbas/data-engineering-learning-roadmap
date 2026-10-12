# Capstone Project Checklist

## Outcome

Deliver a data product that can be reproduced by another person and that answers a clear business question. A target effort of **300 hours** provides room for data engineering, analytics, validation, documentation and presentation; use a smaller scope if needed, but be honest about what is and is not complete.

## Minimum architecture

```text
Source files / API
       ↓
Raw landing + load metadata
       ↓
Staging + schema validation
       ↓
Quality checks + reject/quarantine path
       ↓
Transformations (SQL / Python)
       ↓
Curated analytical model (facts/dimensions or documented alternative)
       ↓
BI semantic model + report

Orchestrate the flow; add tests, logs, CI and a reproducible run environment.
```

## Milestones

| Milestone | Work | Acceptance evidence |
|---|---|---|
| 1. Scope | Define users, decision, KPIs, sources, constraints and acceptance criteria | Project brief + KPI dictionary |
| 2. Architecture | Design components, data flow, failure paths and delivery plan | Architecture diagram + backlog + risk register |
| 3. Ingestion | Ingest at least one or two sources, retain raw data and metadata | Repeatable ingestion + source contract |
| 4. Staging | Define types, keys, schema checks and load metadata | Staging schemas + data dictionary |
| 5. Data quality | Detect nulls, duplicates, invalid values and inconsistent categories | Test suite + issue log + quality metrics |
| 6. Transform | Build repeatable business transformations and reconciliations | SQL/Python transforms + test output |
| 7. Data model | Define grain, facts/dimensions or suitable alternative and history | ERD/star schema + source-to-target map |
| 8. Orchestrate | Schedule dependencies and handle failures/retries | Airflow DAG or equivalent + runbook |
| 9. Processing choice | Use Spark only if helpful; justify batch/streaming decision | Working experiment or decision record |
| 10. BI | Build a semantic model, report and clear KPI definitions | Dashboard + reconciliation to SQL |
| 11. Reliability | Test normal, empty, malformed and failed runs | Automated tests + failure/recovery demo |
| 12. Delivery | Containerize if useful; set up CI and safe configuration | Setup instructions + CI run + no secrets in repo |
| 13. Deployment | Run from a clean environment and note limits/costs | Demo + runbook + security checklist |
| 14. Documentation | Document architecture, data, testing, operations and trade-offs | Complete README and diagrams |
| 15. Handover | Present findings and share a clean project release | Demo/presentation + portfolio summary |

## Repository acceptance checklist

- [ ] Problem statement and intended users are clear.
- [ ] The data source, license and limitations are documented.
- [ ] Setup instructions work from a clean clone.
- [ ] Secrets and personal/sensitive data are excluded.
- [ ] The pipeline can be rerun and has visible error handling.
- [ ] Quality checks cover relevant failure cases.
- [ ] Data model grain and KPI formulas are documented.
- [ ] Dashboard numbers reconcile to an authoritative query.
- [ ] Tests run locally and, where appropriate, in CI.
- [ ] Architecture diagram, data dictionary and runbook are included.
- [ ] Findings are evidence-based; limitations and next steps are explicit.
- [ ] A 5–7 minute walkthrough explains the problem, design, output and trade-offs.

## Choosing a project

Choose a domain whose data is accessible and safe to publish: public transport, weather, public budgets, retail using synthetic data, energy, public health aggregates, or public event data. Avoid personal or restricted data. Pick tools based on the problem, not to maximize the technology list.
