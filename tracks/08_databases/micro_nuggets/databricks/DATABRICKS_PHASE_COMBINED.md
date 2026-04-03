# Databricks Combined Phase Guide

This file consolidates the four source phase documents into one reference.

## Included Sources
- summary.md
- DATABRICKS_SPEEDY_STORY_AND_INTERVIEW.md
- PHASE2_PLAN.md
- DATABRICKS_PHASE2_INTERVIEW_Q_PACK.md

## Quick Definitions
- [ACID](../../../../docs/concepts/foundations/acid.md)
- [OLTP vs OLAP](../../../../docs/concepts/foundations/oltp_vs_olap.md)
- [Delta Lake](../../../../docs/concepts/databases/delta_lake.md)
- [MERGE](../../../../docs/concepts/databases/merge.md)
- [Time Travel](../../../../docs/concepts/databases/time_travel.md)
- [Medallion Architecture](../../../../docs/concepts/databases/medallion_architecture.md)
- [Unity Catalog](../../../../docs/concepts/databases/unity_catalog.md)
- [Idempotency](../../../../docs/concepts/foundations/idempotency.md)
- [CDC](../../../../docs/concepts/foundations/cdc.md)
- [Partitioning](../../../../docs/concepts/performance/partitioning.md)
- [Z-ORDER](../../../../docs/concepts/performance/z_order.md)
- [Small Files Problem](../../../../docs/concepts/performance/small_files_problem.md)
- [OPTIMIZE and Compaction](../../../../docs/concepts/performance/optimize_and_compaction.md)
- [RBAC](../../../../docs/concepts/governance/rbac.md)
- [Least Privilege](../../../../docs/concepts/governance/least_privilege.md)
- [Row-Level Security](../../../../docs/concepts/governance/row_level_security.md)
- [Column Masking](../../../../docs/concepts/governance/column_masking.md)
- [SQL Warehouse vs Compute Cluster](../../../../docs/concepts/platform/sql_warehouse_vs_compute_cluster.md)
- [SLO and Freshness](../../../../docs/concepts/operations/slo_and_freshness.md)
- [All Definitions Index](../../../../docs/concepts/README.md)

---


## Source: summary.md

```text
D:\StudyBook\tracks\08_databases\micro_nuggets\databricks\summary.md
```

---

# Databricks Micro-Nuggets

Quick, focused, runnable lessons on Databricks + Unity Catalog + Delta Lake.

Each nugget is a standalone Python script that:
- **Teaches one concept** with inline comments
- **Runs end-to-end** — no setup beyond prerequisites
- **Prints expected output** in the docstring so you can study without running
- **Builds on previous nuggets** — run them in order

---

## Structure

```
databricks/
│
├── _db_connect.py                      ← shared connection helper (all nuggets import this)
│
├── 00_setup/
│   ├── 00_prereq_check.py              ← Python version, packages, credentials, live ping
│   ├── 01_connection.py                ← minimal open/query/close pattern + CURRENT_* functions
│   └── 02_session_context.py           ← USE CATALOG, SHOW SCHEMAS, DESCRIBE CATALOG
│
├── 01_workspace_and_catalog/
│   └── 01_create_catalog_schema.py     ← CREATE CATALOG, CREATE SCHEMA, INFORMATION_SCHEMA
│
├── 02_tables_and_delta/
│   ├── 01_create_table.py              ← Delta Lake tables, column types, MANAGED vs EXTERNAL
│   ├── 02_insert_select.py             ← INSERT VALUES, INSERT SELECT, JOINs, aggregations
│   └── 03_merge.py                     ← MERGE upsert, CDC pattern, SCD Type 2
│
├── 03_queries_and_optimization/
│   ├── 01_time_travel.py               ← VERSION AS OF, DESCRIBE HISTORY, RESTORE, VACUUM
│   └── 02_optimize.py                  ← OPTIMIZE, Z-ORDER, data skipping, DESCRIBE DETAIL
│
└── 04_mini_capstone/
    └── 01_mini_capstone.py             ← Bronze→Silver→Gold pipeline, dedup, audit, optimize

├── 05_ingestion_and_streaming/
│   ├── 01_ingestion_control_table.py   ← ingestion ledger for replay/idempotency
│   ├── 02_file_ingest_idempotency.py   ← merge-based dedupe of repeated file loads
│   ├── 03_cdc_pattern_apply_changes.py ← CDC apply-changes pattern with MERGE
│   └── 04_streaming_readiness_check.py ← API readiness checks (clusters/sql/jobs)
│
├── 06_governance_and_security/
│   ├── 01_role_and_grants_basics.py    ← least-privilege grant model
│   ├── 02_row_filter_policy_demo.py    ← row-level filtering pattern via secured view
│   └── 03_column_masking_demo.py       ← masking policy pattern for PII
│
├── 07_operations_and_cost/
│   ├── 01_job_run_audit_queries.py     ← operational run-audit model and summary queries
│   ├── 02_warehouse_cost_guardrails.py ← warehouse inventory + cost guard checks
│   └── 03_pipeline_slo_checks.py       ← freshness/error SLO breach detection
```

---

## Prerequisites

1. **Python ≥ 3.8**
2. **Packages:**
   ```bash
   pip install databricks-sql-connector requests
   ```
3. **Credentials** (one of):
   - Environment variables: `DATABRICKS_HOST` + `DATABRICKS_TOKEN`
   - Encrypted secrets: `config/secrets/asuspc.secrets.enc.json`
   - Local env file: `_infra/env/.env.local`

4. **Run prerequisite check:**
   ```bash
   cd D:\StudyBook\tracks\08_databases\micro_nuggets\databricks
   python 00_setup/00_prereq_check.py
   ```

---

## What's Embedded in Every Nugget

- **Concept explanations** — the *why*, not just the *what*
- **Expected output** — exact sample output in the docstring so you can study without running
- **DE context** — how each feature is used in real pipelines
- **Common pitfalls** — e.g. FLOAT vs DECIMAL for money, SELECT * in production
- **Cross-references** — "covered in depth in nugget 06" links the curriculum together

---

## Key Concepts Covered

| Nugget | Concept | Real-World Use |
|--------|---------|----------------|
| 00-00 | Prerequisite check | Validate environment before any work |
| 00-01 | Basic connection | Minimal working program |
| 00-02 | Session context | USE CATALOG/SCHEMA, SHOW/DESCRIBE |
| 01-01 | Create catalog/schema | Namespace design, INFORMATION_SCHEMA |
| 02-01 | Delta tables | Column types, MANAGED vs EXTERNAL, COMMENT |
| 02-02 | INSERT/SELECT/JOIN | ETL patterns, aggregations, fact-dimension joins |
| 02-03 | MERGE (Upsert/CDC) | Incremental pipelines, SCD Type 2, CDC replication |
| 03-01 | Time Travel | Audit, debugging, disaster recovery, compliance |
| 03-02 | OPTIMIZE/Z-ORDER | Query performance, small files problem, data skipping |
| 04-01 | Mini Capstone | Bronze→Silver→Gold pipeline, end-to-end workflow |
| 05-01 | Ingestion control table | Replay-safe ingestion and run traceability |
| 05-02 | File idempotency | Deduplicate repeat drops/retries using ledger merge |
| 05-03 | CDC apply changes | Insert/update/delete pattern with MERGE |
| 05-04 | Streaming readiness | Validate API surface before stream/job rollout |
| 06-01 | Role and grants basics | Least-privilege access model |
| 06-02 | Row filter pattern | Region/persona-aware row visibility |
| 06-03 | Column masking pattern | PII protection at query surface |
| 07-01 | Job run audit queries | Operational observability for pipelines |
| 07-02 | Warehouse guardrails | Cost hygiene and warehouse governance |
| 07-03 | Pipeline SLO checks | Freshness/error monitoring and alert logic |

---

## Running Order

```bash
# 1. Check prerequisites
python 00_setup/00_prereq_check.py

# 2. Learn the connection pattern
python 00_setup/01_connection.py

# 3. Understand session context
python 00_setup/02_session_context.py

# 4. Create your workspace
python 01_workspace_and_catalog/01_create_catalog_schema.py

# 5. Create tables
python 02_tables_and_delta/01_create_table.py

# 6. Load and query data
python 02_tables_and_delta/02_insert_select.py

# 7. Master MERGE (upserts, CDC, SCD Type 2)
python 02_tables_and_delta/03_merge.py

# 8. Time Travel (audit, recovery)
python 03_queries_and_optimization/01_time_travel.py

# 9. OPTIMIZE and Z-ORDER (performance)
python 03_queries_and_optimization/02_optimize.py

# 10. Mini Capstone (end-to-end pipeline)
python 04_mini_capstone/01_mini_capstone.py

# 11. Ingestion + streaming readiness
python 05_ingestion_and_streaming/01_ingestion_control_table.py
python 05_ingestion_and_streaming/02_file_ingest_idempotency.py
python 05_ingestion_and_streaming/03_cdc_pattern_apply_changes.py
python 05_ingestion_and_streaming/04_streaming_readiness_check.py

# 12. Governance + security
python 06_governance_and_security/01_role_and_grants_basics.py
python 06_governance_and_security/02_row_filter_policy_demo.py
python 06_governance_and_security/03_column_masking_demo.py

# 13. Operations + cost
python 07_operations_and_cost/01_job_run_audit_queries.py
python 07_operations_and_cost/02_warehouse_cost_guardrails.py
python 07_operations_and_cost/03_pipeline_slo_checks.py
```

---

## Databricks vs Snowflake — Key Differences

| Feature | Snowflake | Databricks |
|---------|-----------|------------|
| **Compute** | Virtual Warehouse | SQL Warehouse |
| **Table format** | Native (proprietary) | Delta Lake (open-source, Parquet-based) |
| **3-level namespace** | Database.Schema.Table | Catalog.Schema.Table |
| **Auto-increment** | AUTOINCREMENT / IDENTITY | IDENTITY() (Runtime 11.3+) or ETL-generated |
| **Semi-structured** | VARIANT | VARIANT (Runtime 13.3+) or STRING + from_json() |
| **Time Travel** | Built-in (up to 90 days) | Built-in via Delta log (default 30 days) |
| **FK constraints** | Enforced | Documentation-only (not enforced) |
| **Connection auth** | Password or key-pair | Personal Access Token (PAT) |
| **Protocol** | Native binary driver | HTTPS + Thrift (DB-API 2.0) |

---

## Phase 2 Artifacts

- `PHASE2_PLAN.md` — concrete implementation plan and run order
- `DATABRICKS_PHASE2_INTERVIEW_Q_PACK.md` — focused interview prep for ingestion/governance/ops

## Next Steps (Future Nuggets)

- **08_streaming_with_dlt/** — production DLT pipeline patterns
- **09_mlflow_and_feature_ops/** — experiment tracking + feature serving basics
- **10_incident_drills/** — rollback, backfill, and on-call troubleshooting drills

---

## Connection Proof

The connection proof script lives at:
`D:\StudyBook\poc\connection_proofs\python\databricks_connection_proof.py`

It validates your credentials and workspace connectivity before you run nuggets.

---

Last updated: 2026-04-02

---


## Source: DATABRICKS_SPEEDY_STORY_AND_INTERVIEW.md

```text
D:\StudyBook\tracks\08_databases\micro_nuggets\databricks\DATABRICKS_SPEEDY_STORY_AND_INTERVIEW.md
```

---

# Databricks Speedy Story & Interview Guide

## The 30-Second Story

> "Databricks is a unified data analytics platform built on Apache Spark.
> It combines data engineering, data science, and machine learning in one platform.
> The key differentiator is **Delta Lake** — an open-source storage layer that adds
> ACID transactions, Time Travel, and schema enforcement to Parquet files.
> Unity Catalog provides centralized governance across all data and AI assets."

---

## Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Databricks Workspace                      │
│  (Your tenant — like a Snowflake account)                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   SQL        │  │   Compute    │  │   Jobs       │      │
│  │  Warehouse   │  │   Clusters   │  │  (Spark)     │      │
│  │  (serverless)│  │  (provisioned)│  │              │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │               │
│         └─────────────────┼─────────────────┘               │
│                           │                                 │
│                    ┌──────▼───────┐                         │
│                    │  Unity       │                         │
│                    │  Catalog     │                         │
│                    │  (governance)│                         │
│                    └──────┬───────┘                         │
│                           │                                 │
│                    ┌──────▼───────┐                         │
│                    │  Delta Lake  │                         │
│                    │  (storage)   │                         │
│                    └──────┬───────┘                         │
│                           │                                 │
│                    ┌──────▼───────┐                         │
│                    │  Cloud       │                         │
│                    │  Storage     │                         │
│                    │  (S3/ADLS/GCS)│                        │
│                    └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Concepts for Interviews

### 1. Delta Lake

**What it is:** Open-source storage layer built on top of Parquet.

**Why it matters:**
- **ACID transactions** — concurrent writes don't corrupt data
- **Time Travel** — query previous versions of your data
- **Schema enforcement** — prevents bad data from breaking pipelines
- **Schema evolution** — add columns without rewriting data
- **OPTIMIZE + Z-ORDER** — physical data layout optimization

### 2. Unity Catalog

**What it is:** Centralized governance layer for data, AI, and analytics.

**3-level namespace:** `catalog.schema.table`

**Permission model:** Hierarchical RBAC
```
Metastore Admin
  └─ CREATE CATALOG → assigns Catalog Owner
       └─ CREATE SCHEMA → assigns Schema Owner
            └─ CREATE TABLE → assigns Table Owner
```

### 3. SQL Warehouse vs. Compute Cluster

| Feature | SQL Warehouse | Compute Cluster |
|---------|--------------|-----------------|
| **Purpose** | SQL queries (BI, analytics) | Spark jobs (ETL, ML) |
| **Interface** | JDBC/ODBC, DB-API 2.0 | Spark API, notebooks |
| **Scaling** | Serverless (auto) or provisioned | Manual or auto-scaling |
| **Cold start** | 30-60 seconds | 2-5 minutes |
| **Pricing** | DBU per second | DBU per second + VM cost |

### 4. Personal Access Token (PAT)

**What it is:** Long-lived authentication token for API/SQL access.

**Created in:** User Settings → Developer → Access Tokens → Generate New Token

**Properties:**
- Starts with `dapi`
- Inherits all permissions of the creating user
- Doesn't expire unless manually revoked
- Best practice: use dedicated service accounts for automation

---

## Deep Interview Questions

### Q: "What is Delta Lake and why would you use it?"

> "Delta Lake is an open-source storage framework built on Parquet that adds
> ACID transactions, Time Travel, and schema enforcement to data lakes.
> I'd use it because plain Parquet files can't handle concurrent writes safely
> and don't support updates or deletes. Delta's transaction log makes data
> lakes reliable enough for production pipelines."

### Q: "How does Databricks handle schema evolution?"

> "Delta Lake supports schema evolution through `MERGE SCHEMA` and
> `overwriteSchema` options. When new data arrives with additional columns,
> Delta can automatically add them to the table definition without rewriting
> existing data. This is critical for pipelines where upstream sources change
> over time. You can also explicitly `ALTER TABLE ADD COLUMN`."

### Q: "What's the difference between MANAGED and EXTERNAL tables?"

> "A MANAGED table is fully managed by Databricks — both the metadata in
> Unity Catalog and the underlying data files. When you DROP a managed table,
> both the catalog entry and the files are deleted.
>
> An EXTERNAL table only tracks metadata in Databricks — the data files are
> managed externally (in S3, ADLS, etc.). Dropping an external table removes
> the catalog entry but leaves the files untouched. Use EXTERNAL when data
> is shared across systems or you need file-level control."

### Q: "How would you optimize a slow Delta query?"

> "Three approaches:
> 1. **OPTIMIZE** — compacts small files into larger ones (reduces file count)
> 2. **Z-ORDER BY** — co-locates related data using multi-dimensional indexing
> 3. **Partition pruning** — ensure WHERE clauses match partition columns
>
> I'd start by checking the query profile to identify the bottleneck, then
> apply the right optimization. Z-ORDER is most effective for multi-column
> filter patterns. OPTIMIZE helps when there are many small files from
> streaming or incremental loads."

### Q: "How does Databricks compare to Snowflake?"

> "Both separate storage from compute and support SQL analytics. Key differences:
> - **Storage**: Snowflake uses proprietary format; Databricks uses open Delta Lake
> - **Compute**: Snowflake has warehouses; Databricks has SQL Warehouses + Spark clusters
> - **Ecosystem**: Databricks integrates ML/AI (MLflow, Feature Store); Snowflake is SQL-focused
> - **Open-source**: Delta Lake is open-source; Snowflake's storage is closed
> - **Pricing**: Both charge compute-seconds, but Databricks also charges DBUs
>
> I'd choose Databricks for ML/AI workloads and open-source flexibility.
> Snowflake for pure SQL/BI with less operational overhead."

### Q: "Explain the MERGE statement and when you'd use it."

> "MERGE INTO is Databricks' most powerful DML command — it combines INSERT,
> UPDATE, and DELETE in a single atomic operation. You use it when:
>
> 1. **Upserting data**: New records get inserted, existing records get updated.
>    This is the standard pattern for incremental data pipelines.
>
> 2. **CDC (Change Data Capture)**: Source systems emit events with operation
>    types (I/U/D). MERGE applies all three in one statement:
>    - WHEN MATCHED AND op = 'D' THEN DELETE
>    - WHEN MATCHED AND op = 'U' THEN UPDATE SET ...
>    - WHEN NOT MATCHED AND op = 'I' THEN INSERT ...
>
> 3. **Slowly Changing Dimensions Type 2**: Expire old rows and insert new ones
>    to maintain a full history of changes.
>
> The key advantage over separate INSERT/UPDATE/DELETE statements is that MERGE
> is atomic — if it fails mid-way, ALL changes are rolled back. Readers never
> see a partially-applied merge."

### Q: "What is Time Travel in Delta Lake and how would you use it?"

> "Time Travel lets you query any previous version of a Delta table by version
> number or timestamp. Every change creates a new commit in the transaction log,
> and old data files are kept for a configurable retention period (default 30 days).
>
> Real use cases:
> - **Audit**: 'What did this table look like yesterday at 3pm?'
>   `SELECT * FROM table TIMESTAMP AS OF '2024-01-15 15:00:00'`
>
> - **Debugging**: 'When did this bad data get introduced?'
>   `DESCRIBE HISTORY table` — shows every commit with operation and timestamp.
>
> - **Recovery**: 'I accidentally deleted 1M rows — restore the table!'
>   `RESTORE TABLE table TO VERSION AS OF 5`
>
> - **Reproducibility**: 'Re-run this report using the data as of Jan 15.'
>   `SELECT * FROM table VERSION AS OF 123`
>
> Important: VACUUM permanently deletes old files. Never set retention to 0
> in production — you lose Time Travel."

### Q: "Describe a typical three-layer data pipeline in Databricks."

> "I use the Bronze-Silver-Gold pattern:
>
> **Bronze (Raw)**: Data exactly as received from source systems.
> - No modifications, no schema enforcement.
> - Schema-on-read — you can re-interpret later.
> - Never delete — it's your source of truth.
>
> **Silver (Cleaned)**: Deduplicated, typed, validated data.
> - One row per business entity (ROW_NUMBER() to deduplicate).
> - Data quality gates: filter negative quantities, null keys, etc.
> - Foreign keys are consistent (no orphaned records).
> - This is the 'single source of truth' for the business.
>
> **Gold (Analytics)**: Business-ready tables optimized for querying.
> - Aggregations, joins, and business logic applied.
> - Z-ORDER'd on the columns analysts filter most.
> - Pre-computed metrics (daily sales, customer lifetime value).
> - This is what BI tools and dashboards query.
>
> Each layer is a Delta table — so you can Time Travel through the entire
> pipeline to audit where any piece of data came from."

### Q: "How do you handle duplicates in a data pipeline?"

> "I use the ROW_NUMBER() window function pattern:
>
> ```sql
> WITH ranked AS (
>     SELECT *,
>         ROW_NUMBER() OVER (
>             PARTITION BY business_key
>             ORDER BY ingested_at ASC
>         ) AS rn
>     FROM bronze.raw_table
> )
> SELECT * FROM ranked WHERE rn = 1
> ```
>
> This assigns rank 1 to the first occurrence of each business key (by ingestion
> timestamp). Everything else is a duplicate and gets filtered out.
>
> For more complex deduplication, I might:
> - Order by a quality score instead of timestamp (keep the 'best' record)
> - Use MERGE to upsert: update existing records with newer data
> - Log duplicates to a separate table for data quality monitoring"

### Q: "What's the small files problem and how do you fix it?"

> "Every INSERT, UPDATE, DELETE, or MERGE creates new data files in Delta Lake.
> Over time, your table accumulates thousands of tiny files. Reading 10,000
> small files is MUCH slower than reading 10 large files because:
> - Each file requires a separate HTTP request to cloud storage
> - Spark has to open and close each file individually
> - File metadata overhead dominates actual data reading
>
> Fix: Run OPTIMIZE regularly. It rewrites many small files into fewer large
> files (target 128 MB each). It's idempotent — running on an already-optimized
> table is a no-op.
>
> Prevention: Batch your writes. Instead of 100 small INSERTs, do one large
> INSERT or MERGE. For streaming, tune the trigger interval to accumulate
> enough data before each write."

### Q: "When would you use PARTITION BY vs Z-ORDER?"

> "PARTITION BY is for low-cardinality columns (date, country, category):
> - Creates separate directories per partition value.
> - Great when you always filter by that column.
> - Too many partitions = too many directories = slow file listing.
> - Rule: aim for partitions in the hundreds, not thousands.
>
> Z-ORDER is for high-cardinality columns (product_id, customer_id):
> - Reorganizes data within files using a Z-order curve.
> - No directory structure change — just co-locates related rows.
> - Can combine multiple columns: ZORDER BY (product_id, sale_date).
> - Max 3-4 columns — more columns dilute the benefit.
>
> Combined approach: PARTITION BY date, ZORDER BY (product_id, customer_id).
> This gives you both directory-level and file-level pruning."

---

## Quick Reference Commands

```sql
-- Session context
SELECT CURRENT_CATALOG(), CURRENT_SCHEMA(), CURRENT_USER();
USE CATALOG main;
USE SCHEMA default;

-- List objects
SHOW CATALOGS;
SHOW SCHEMAS;
SHOW TABLES;

-- Metadata
DESCRIBE CATALOG main;
DESCRIBE TABLE my_table;
SELECT * FROM information_schema.tables;

-- Table operations
CREATE TABLE t (id INT, name STRING) USING DELTA COMMENT 'My table';
INSERT INTO t VALUES (1, 'Alice');
UPDATE t SET name = 'Bob' WHERE id = 1;
DELETE FROM t WHERE id = 1;
MERGE INTO target t USING source s ON t.id = s.id WHEN MATCHED THEN UPDATE SET *;

-- Delta operations
DESCRIBE HISTORY my_table;              -- Time Travel history
RESTORE TABLE my_table TO VERSION AS OF 5;  -- Rollback
OPTIMIZE my_table ZORDER BY (col1, col2);   -- Physical optimization
VACUUM my_table RETAIN 168 HOURS;       -- Clean old versions
```

---

## Citi Narrative Hook

> "At Citi, I worked with large-scale telemetry infrastructure where we needed
> reliable data pipelines for capacity forecasting. Databricks' Delta Lake
> would have been ideal for our use case because it provides ACID guarantees
> on our Parquet-based data lake — something we had to build manually with
> file locking and validation scripts. The Time Travel feature alone would
> have saved us hours of debugging when pipeline updates introduced bad data."

---

Last updated: 2026-04-02

---


## Source: PHASE2_PLAN.md

```text
D:\StudyBook\tracks\08_databases\micro_nuggets\databricks\PHASE2_PLAN.md
```

---

# Databricks Phase 2 Plan (Concrete)

This phase extends the existing speedy lane with platform-ready DE topics.

## Scope

- Add 10 runnable nuggets across three folders.
- Add an interview Q pack focused on mid/senior Databricks scenarios.
- Keep scripts safe for learning environments (read-only where possible; clear notes where permissions vary).

## Folder Plan

1. `05_ingestion_and_streaming`
- `01_ingestion_control_table.py`
- `02_file_ingest_idempotency.py`
- `03_cdc_pattern_apply_changes.py`
- `04_streaming_readiness_check.py`

2. `06_governance_and_security`
- `01_role_and_grants_basics.py`
- `02_row_filter_policy_demo.py`
- `03_column_masking_demo.py`

3. `07_operations_and_cost`
- `01_job_run_audit_queries.py`
- `02_warehouse_cost_guardrails.py`
- `03_pipeline_slo_checks.py`

## Run Order

```powershell
python 05_ingestion_and_streaming/01_ingestion_control_table.py
python 05_ingestion_and_streaming/02_file_ingest_idempotency.py
python 05_ingestion_and_streaming/03_cdc_pattern_apply_changes.py
python 05_ingestion_and_streaming/04_streaming_readiness_check.py

python 06_governance_and_security/01_role_and_grants_basics.py
python 06_governance_and_security/02_row_filter_policy_demo.py
python 06_governance_and_security/03_column_masking_demo.py

python 07_operations_and_cost/01_job_run_audit_queries.py
python 07_operations_and_cost/02_warehouse_cost_guardrails.py
python 07_operations_and_cost/03_pipeline_slo_checks.py
```

## Outcomes

- Better interview readiness for production Databricks work.
- Coverage beyond Delta SQL basics: governance, operations, and platform diagnostics.
- Keeps the same teaching style as Phase 1 (small scripts, deep comments, concrete output).

---


## Source: DATABRICKS_PHASE2_INTERVIEW_Q_PACK.md

```text
D:\StudyBook\tracks\08_databases\micro_nuggets\databricks\DATABRICKS_PHASE2_INTERVIEW_Q_PACK.md
```

---

# Databricks Phase 2 Interview Q Pack

## Ingestion and Streaming

**Q: How do you make file ingestion idempotent in Databricks?**
Use a control/ledger table keyed by file name + checksum + load batch ID, and merge against it before loading.

**Q: When would you use Auto Loader vs COPY INTO?**
Auto Loader for continuous/semi-continuous incremental ingestion at scale; COPY INTO for simpler batch loads and controlled one-off/backfill jobs.

**Q: How do you handle late-arriving updates in CDC pipelines?**
Use MERGE into silver tables with event-time ordering and deterministic tie-breakers (event timestamp + sequence/version).

## Governance and Security

**Q: What does Unity Catalog give you that legacy hive_metastore does not?**
Centralized governance across workspaces, consistent RBAC, lineage, and stronger separation of data ownership and compute.

**Q: How do row filters and column masks help in regulated environments?**
They enforce dynamic data access policies at query time, letting one table serve multiple personas without copying sensitive data.

**Q: What is your minimal grant model for analytics consumers?**
Grant USAGE on catalog/schema + SELECT on required tables/views only; avoid broad ownership grants and wildcard permissions.

## Operations and Cost

**Q: How do you detect pipeline regressions early?**
Track SLO metrics (freshness lag, row count deltas, failure rates, runtime trend), alert on threshold breaches, and gate downstream publish.

**Q: How do you control SQL Warehouse cost without breaking SLAs?**
Separate warehouses by workload, set auto-stop aggressively, right-size based on concurrency, and monitor query history for heavy users.

**Q: What are common causes of slow Databricks SQL queries?**
Small files, poor partition strategy, missing OPTIMIZE/ZORDER cadence, broad scans from weak predicates, and skewed joins.

**Q: How do you answer “How is Databricks productionized?” in interviews?**
Explain standards: layered medallion data model, CI/CD for jobs/notebooks, policy-driven governance in Unity Catalog, observability with SLO dashboards, and cost guardrails by warehouse/job class.

---

