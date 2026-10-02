# Data Engineering & Analytics: Zero to Hero — authoring guide

This is the contract every lesson follows. It is not published.

## What the course is

A free, bilingual (English/Arabic) course that takes a reader from zero to "hero" in **building and running the data systems organisations depend on**: SQL and data modelling, warehouses, lakes and lakehouses, ingestion and orchestration, streaming, transformations as code, data quality, metrics and dashboards people trust, experiments, taking data science and ML into production, data for LLM applications (retrieval, embeddings, evaluation), and data governance, privacy and security.

- **Audience:** data science, CS and engineering graduates aiming at data engineer, analytics engineer, data analyst or ML/data scientist roles; software engineers moving into data; analysts who want to engineer; GCC bank, government and enterprise staff who own data. Basic Python and some SQL help; nothing else assumed.
- **Hands-on and runnable on a laptop.** Prefer open, free tools that a learner can run locally: **PostgreSQL**, **DuckDB**, **Python** (pandas, Polars), **dbt Core**, **Apache Airflow** or **Dagster**, **Apache Kafka** or Redpanda (in Docker), **Great Expectations** or dbt tests, **Metabase** or **Apache Superset**, **pgvector**. Mention the managed cloud equivalents (Snowflake, BigQuery, Databricks, Amazon Redshift, Microsoft Fabric) neutrally, never as endorsements, and never invent their prices or limits.
- **Engineering judgement over tool tours:** every lesson must leave the reader able to make a design decision (model it this way, load it incrementally, test this, define the metric so) or produce an artefact.
- **Companion courses** (relative links; catalogue in `LIBRARY.md`): *System Design for Vibe Coders* (databases, backups, indexes, analytics events), *SaaS Building Blocks* (2.1 data layer, 6.2 analytics pipeline), *AI Governance: Zero to Hero* (privacy law, data governance for AI), *AI Product Management: Zero to Hero* (data readiness, evaluation, experiments), *Secure AI & Application Security* (5.3 personal data, 9.3 securing RAG), *Cloud & DevOps: Zero to Hero* (being written now: link by module — 2 containers, 3 infrastructure as code, 4 CI/CD, 5 observability), *From Graduate to Hired* (being written now: 2.3 is the data role path). Point to them in one line where they go deeper and stay on the data decision here.

## The running case: Najm Bank's Data Platform team

**Najm Bank** is the fictional mid-sized Gulf bank (retail, SME and corporate lending; customers in Qatar, the UAE and the EU) used across the library. Say it is fictional in lesson 0.3. Here we sit in its **Data Platform & Analytics** team.

Data and systems (use consistently):
- **Core banking database** (OLTP, PostgreSQL in the examples): customers, accounts, transactions, loans.
- **Card transactions stream**: card authorisations as events (Kafka in the examples).
- **Najm Mobile** app events (screens, taps, feature usage) and **Najm Assist** (the LLM assistant) conversation logs.
- **The warehouse/lakehouse**: raw → staging → marts layers; the **customer 360** mart; the **credit-risk mart**; regulatory reporting extracts.
- **Smart Alerts**: the fraud-detection ML model (features, training data, drift).
- **Credit Memo Copilot**: internal GenAI with retrieval (RAG) over credit policies and memos — the data-for-LLM example.
- Dashboards for the retail, risk and finance teams.

Cast:
- **Faisal** — Head of Data Platform; the reader's mentor.
- **Huda** — new graduate data engineer (data-science degree; the reader's peer; makes the mistakes the reader should avoid).
- **Lina** — analytics engineer (dbt, metrics, dashboards).
- **Dana** — lead data scientist (also in the security course): Smart Alerts, experiments.
- **Kareem** — data analyst for the retail business.
- **Sara** — Data Protection Officer (DPO); **Layla** — Head of AI Governance; **Tariq** — engineering lead; **Salem** — Head of Platform Engineering.

## Stages (the lesson tag)

Every lesson is tagged with one or two stages of the data life cycle, in English, in both languages: **Ingest · Store · Model · Transform · Serve · Analyse · Operate · Govern**. Header: `*Stage: Model*` or `*Stage: Transform, Operate*`.

## Module and lesson plan (numbers are fixed)

| Module | File | Lessons |
|---|---|---|
| 0 Orientation | 00-orientation.md | 0.1 What data engineering, analytics and data science are — and how they fit together · 0.2 The modern data stack end to end: from a tap in the app to a number on a dashboard · 0.3 Meet Najm Bank's data platform team, and how to use this course |
| 1 SQL and data modelling | 01-sql-modelling.md | 1.1 SQL that answers business questions: joins, aggregation, CTEs and window functions · 1.2 Data modelling: normalisation, star schemas, grain and slowly changing dimensions · 1.3 Where data lives: OLTP vs OLAP, warehouses, lakes, lakehouses and open table formats |
| 2 Ingestion and pipelines | 02-pipelines.md | 2.1 Getting data in: ETL vs ELT, connectors, incremental loads and change data capture · 2.2 Orchestration: DAGs, idempotency, retries and backfills · 2.3 Streaming: events, Kafka, windows and the exactly-once myth |
| 3 Transformation and quality | 03-transform-quality.md | 3.1 Transformations as code: dbt, layers, tests and version control · 3.2 Data quality: tests, contracts and observability · 3.3 Performance and cost: partitioning, clustering, incremental models and query plans |
| 4 Analytics people trust | 04-analytics.md | 4.1 Defining metrics: one definition, a semantic layer and a metrics catalogue · 4.2 Dashboards and data storytelling that lead to decisions · 4.3 Experiments and statistics for analysts: A/B tests and the traps that fool smart people |
| 5 Data science and ML in production | 05-ml.md | 5.1 From notebook to pipeline: features, training, reproducibility and feature stores · 5.2 Evaluating models and monitoring drift (MLOps basics) · 5.3 Data for LLM applications: documents, chunking, embeddings, vector search and evaluation |
| 6 Governance, privacy and security | 06-governance.md | 6.1 Data governance that works: ownership, catalogue, lineage and data contracts · 6.2 Personal data: classification, masking, minimisation, retention and the law · 6.3 Securing the data platform: access control, secrets, audit and sharing safely |
| 7 Hero: capstone and practice exam | 07-capstone.md | 7.1 Capstone: build Najm's credit-risk data mart end to end · 7.2 The data career: roles, interviews, portfolio and growth · 7.3 Practice exam: 60 scenario questions |

Levels: 🟢 Beginner for Modules 0–1, 🟡 Intermediate for 2–5, 🔴 Advanced for 6–7 (use judgement per lesson).

## Facts to get right (and how to hedge)

State only what you are confident is true; name versions; hedge anything that changes "at the time of writing (2026)"; never invent benchmarks, prices, statistics, quotes or dates.
- **Modelling:** Codd's normal forms; Kimball dimensional modelling (facts, dimensions, grain, conformed dimensions, SCD types 1/2/3 — The Data Warehouse Toolkit); Inmon's enterprise warehouse; Data Vault exists (one line). Medallion (bronze/silver/gold) is Databricks' naming of raw/clean/curated layers.
- **Storage:** row vs columnar storage; Parquet and ORC; open table formats **Apache Iceberg**, **Delta Lake**, **Apache Hudi** (ACID tables on object storage; time travel); OLTP vs OLAP; lakehouse term popularised by Databricks (2020).
- **Pipelines:** ETL vs ELT; change data capture (Debezium reads database logs); idempotent loads (MERGE/upsert, partition overwrite); backfills; Airflow (Apache, DAGs of tasks), Dagster (asset-based), Prefect; schedule vs event triggers.
- **Streaming:** Kafka topics, partitions, consumer groups, offsets, retention; at-most/at-least/exactly-once semantics (Kafka offers exactly-once within Kafka via idempotent producers and transactions; end-to-end exactly-once needs idempotent sinks); event time vs processing time, watermarks, tumbling/sliding/session windows (Flink, Spark Structured Streaming, Kafka Streams).
- **Transformation & quality:** dbt models, refs, sources, tests (unique, not_null, accepted_values, relationships), snapshots for SCD2, incremental materialisations, docs and lineage; data contracts (schema + semantics + SLAs agreed with producers); data observability (freshness, volume, schema, distribution); Great Expectations / Soda (name only).
- **Analytics:** metric definitions and semantic layers (dbt Semantic Layer/MetricFlow, Cube, LookML — neutral); Simpson's paradox; survivorship bias; A/B testing: randomisation, sample size and power, p-values and confidence intervals, peeking/optional stopping, multiple comparisons, novelty effects, guardrail metrics, SRM (sample ratio mismatch). Point to *AI Product Management* 6.3 for product experiments.
- **ML/MLOps:** train/validation/test splits; data leakage (target leakage, temporal leakage); feature stores (Feast as open-source example); experiment tracking (MLflow); model registry; data drift vs concept drift; PSI as a common drift statistic in banking (hedge thresholds as conventions); model risk management in banks (SR 11-7 in the US as the classic reference — hedge; GCC regulators expect model governance — no invented clause numbers).
- **LLM data:** chunking, embeddings, vector indexes (HNSW), pgvector, hybrid search (BM25 + vectors), re-ranking, retrieval evaluation (recall@k, precision, MRR), groundedness/faithfulness checks; permission-aware retrieval (point to *Secure AI* 9.3).
- **Governance & privacy (one line each, hedge, point to *AI Governance*):** GDPR principles (Art. 5), pseudonymisation vs anonymisation, data subject rights; Qatar PDPPL (Law No. 13 of 2016); data residency expectations in GCC banking (hedge); DAMA-DMBOK as the reference body of knowledge; data catalogues (OpenMetadata, DataHub, Amundsen as open-source examples); column-level lineage; role-based and attribute-based access control; row-level security; dynamic masking; audit logs.

Real cases you may use (well documented only; hedge figures): the legacy XLS row limit that truncated COVID-19 case data in England in 2020 (widely reported); Simpson's paradox in the 1973 UC Berkeley admissions data (classic). Otherwise use clearly hypothetical Najm scenarios.

## File format (the build parses this — follow exactly)

```
# Module 1 — SQL and data modelling

*One-paragraph italic module intro: what the module covers and why, tied to Najm Bank.*

> **Stages:** Model, Store — …(one line in the course's words)

---

# 1.1 — SQL that answers business questions: joins, aggregation, CTEs and window functions
*Level: 🟢 Beginner* · *Prerequisites: 0.1, 0.2* · *Stage: Model, Analyse*

## ⚡ In 60 seconds
- 4–6 bullets: what it is, the rule that matters most, the decision cue, the biggest trap.

## 🧭 Why it matters
A Najm Bank scenario (or a widely reported public case) that makes the topic unavoidable. 1–3 paragraphs.

## 📐 How it works
### 🟢 The essentials
### 🟡 Going deeper
### 🔴 Expert view
(Plain explanations first; define every term on first use; short runnable SQL/Python/YAML snippets in fenced blocks — show the wrong way and the right way side by side where it helps; small example tables; one mermaid diagram where it genuinely helps. Mermaid: flowchart or sequence only, `flowchart LR` or `TD`, short labels in double quotes, no parentheses inside labels.)

## 🧰 The toolkit
| Tool, pattern or standard | What it is and does | When to reach for it |
|---|---|---|
| **Window functions** | … | … |
(3–8 rows. The first cell MUST start with the name in bold — e.g. **dbt**, **Star schema**, **Slowly changing dimension (Type 2)**, **Apache Iceberg**, **Change data capture (CDC)**, **Great Expectations**, **pgvector** — optionally followed by a short credit in parentheses. Keep bold names identical wherever the same item appears; they build the toolkit catalogue.)

## 🏛️ In practice at Najm Bank
The artefact this lesson produces: a model diagram and grain statement, a pipeline design note, a dbt model with tests, a data contract, a metric definition card, a dashboard spec, an experiment plan, a drift-monitoring checklist, a data-classification table, an access policy. Concrete, reusable, in a table or a short template.

## 🛠️ Exercises
Three graded exercises: 🟢 …, 🟡 …, 🔴 …, each with a "*Done when:*" line. Exercises run locally on free tools (PostgreSQL, DuckDB, dbt Core, Airflow/Dagster, Kafka/Redpanda in Docker) with synthetic or public open data — never real personal data.

## ⚠️ Mistakes and traps
4–6 bullets: the trap, then what to do instead.

## 🧾 Recap
4–6 bullets.

## ✍️ Check yourself
Five multiple-choice questions (at least three scenario-based, set at Najm Bank or a neutral company). Format:

**1. Question text?**

- A. …
- B. …
- C. …
- D. …

<details><summary>Answer</summary>

**B.** Why B is right, and why the tempting distractor is wrong. (Pointer to the section.)

</details>

## 📚 References
Official docs and primary sources only (postgresql.org, duckdb.org, docs.getdbt.com, airflow.apache.org, dagster.io, kafka.apache.org, iceberg.apache.org, delta.io, parquet.apache.org, mlflow.org, feast.dev, github.com/pgvector/pgvector, eur-lex.europa.eu, papers on arxiv.org, classic books by title and author). Plain links; no invented URLs — link to a top-level page if unsure of the deep link.
```

- Separate lessons with a `---` line.
- Lesson 7.3 (practice exam) follows the same outer format but its body is: ⚡ (how to take it), then `## ✍️ Practice exam` with 60 questions numbered 1–60 in the same Q/A format, spread across the stages and modules, each answer ending with its stage and the lesson to review, e.g. *(Model · 1.2)*; then 🧾 and 📚. Its 🧰/🏛️/🛠️/⚠️ sections may be short.

## Style

- Plain, direct English; short sentences; define jargon on first use; no hype, no filler. Explain *why*, not just *what*.
- Code: short, correct, runnable (PostgreSQL or DuckDB SQL, Python 3.11+, dbt YAML). Show the safe/correct version.
- Lengths: 2,000–3,500 words per lesson (7.3 excepted). Every lesson's five questions must be answerable from that lesson.
- Use the running cast consistently. Do not start any non-quiz line with `**N.` (bold number + dot).
