# Databricks Bridge Glossary

Plain-English definitions for every term you need to understand
before your interview. Each entry links to the nugget where the
concept is used.

---

## ACID

**What it means:**
Four guarantees that every database transaction must provide:
- **A**tomicity: a write either fully succeeds or fully fails (no partial writes)
- **C**onsistency: every write leaves the data in a valid state (schema enforced)
- **I**solation: readers see a consistent snapshot; concurrent writers don't interfere
- **D**urability: once committed, the data survives crashes

**How Delta implements it:**
Delta uses the `_delta_log/` transaction log. Each write creates a new JSON entry.
If a write crashes mid-way, no log entry is created, so the partial Parquet files
are invisible to readers -- automatic rollback.

**Nugget:** `03_delta_core/01_acid_and_transactions.py`

---

## Adaptive Query Execution (AQE)

**What it means:**
A Spark feature (3.0+) that re-optimizes the query plan at runtime using actual
statistics collected during execution. It can automatically:
- Switch from sort-merge join to broadcast join if a table turns out to be small
- Coalesce shuffle partitions to avoid tiny tasks

**PostgreSQL analogy:** The planner in PG uses statistics collected by ANALYZE.
AQE is like re-planning mid-query with live statistics.

**Nugget:** `05_performance_and_optimization/01_explain_and_profiling.py`

---

## Bronze / Silver / Gold (Medallion Architecture)

**What it means:**
A three-layer data lake design pattern:
- **Bronze:** raw data exactly as received (no transformations, keeps duplicates and errors)
- **Silver:** cleaned, deduplicated, validated data ready for analysis
- **Gold:** highly-aggregated, business-optimized tables for BI / ML

**Why it matters:** Separates concerns. Bronze gives you full data lineage and
auditability. Silver gives analysts clean data. Gold gives BI tools fast reads.

**Nugget:** `09_mini_capstone/01_mini_capstone.py`

---

## Change Data Capture (CDC)

**What it means:**
The process of detecting and capturing changes (INSERT, UPDATE, DELETE) from a
source database and delivering them to a target system. CDC events typically
include an operation type field (`_op`: 'I', 'U', 'D') and a timestamp.

**In Databricks:** Processed using MERGE (handles all three operation types
in one atomic statement). Delta also has Change Data Feed (CDF) for native CDC output.

**Nugget:** `04_de_patterns/02_merge_upsert.py`

---

## Delta Log (`_delta_log/`)

**What it means:**
A directory of JSON files that records every transaction against a Delta table.
Each commit creates a new numbered JSON file (e.g., `000000000000000001.json`).
The log is what gives Delta its ACID properties, Time Travel capability,
and schema versioning.

**PostgreSQL analogy:** The Write-Ahead Log (WAL). Both are append-only logs
that record every change and enable crash recovery.

**Snowflake analogy:** Snowflake's hidden micro-partition change history.
Users cannot read it directly; Delta's log is user-readable.

**Nugget:** `03_delta_core/01_acid_and_transactions.py`

---

## MERGE Semantics

**What it means:**
A single SQL statement that atomically performs INSERT, UPDATE, and/or DELETE
based on whether rows match between a source and a target table.

```sql
MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED AND source._op = 'U' THEN UPDATE SET ...
WHEN MATCHED AND source._op = 'D' THEN DELETE
WHEN NOT MATCHED                  THEN INSERT ...
```

**Key property:** The entire MERGE is one atomic Delta transaction.
Either all operations commit or none do.

**PostgreSQL comparison:** PG 15+ has MERGE with identical syntax.
Earlier PG: use `INSERT ... ON CONFLICT` (INSERT + UPDATE only).

**Nugget:** `04_de_patterns/02_merge_upsert.py`

---

## OPTIMIZE

**What it means:**
A Databricks SQL command that rewrites small Parquet files into larger
target files (default 128 MB). Solves the "small files problem" caused by
frequent incremental writes.

```sql
OPTIMIZE nugget_lab.bridge_lab.sales_orders
ZORDER BY (customer_id, product_id)
```

**Why it matters:** A table with 10,000 x 1 MB files is 100x slower to scan
than the same data in 78 x 128 MB files, because each file requires an open/close
system call.

**PostgreSQL analogy:** `VACUUM` (reclaims dead tuples and reorganizes pages).
Also similar to `CLUSTER` (one-time physical sort, not recurring).

**Snowflake analogy:** Snowflake's automatic clustering (no manual command needed).

**Nugget:** `03_delta_core/04_optimize_and_zorder.py`

---

## Partition Pruning

**What it means:**
When a query filter matches the partition column, the query engine skips
all partition directories that cannot contain matching data. This dramatically
reduces I/O for large partitioned tables.

**Example:**
```sql
-- Table is PARTITIONED BY (region)
SELECT * FROM sales_orders WHERE region = 'North'
-- Delta reads only the region=North/ directory, skips East/South/West
```

**PostgreSQL analogy:** Partition pruning on declarative partitioned tables
(PG 10+). Same concept, different physical layout.

**Nugget:** `05_performance_and_optimization/02_partitioning_strategy.py`

---

## Schema Enforcement

**What it means:**
Delta rejects any write that does not match the table's current schema.
If you try to insert an extra column or a wrong data type, the write fails
with an `AnalysisException`.

**How to evolve the schema:** Use `ALTER TABLE ADD COLUMN` for new columns,
or set `mergeSchema = true` option for more complex evolution.

**PostgreSQL analogy:** Table-level `CHECK` constraints and `NOT NULL`
constraints enforce data rules at write time. Delta's enforcement is
at the schema (column type) level.

**Nugget:** `03_delta_core/02_schema_enforcement_evolution.py`

---

## Schema Evolution

**What it means:**
The ability to add or modify columns in a Delta table without rewriting
existing data. Adding a column is metadata-only (old rows show NULL for the new column).
Renaming or dropping columns requires column mapping mode (Delta 2.0+).

**Nugget:** `03_delta_core/02_schema_enforcement_evolution.py`

---

## SCD Type 2 (Slowly Changing Dimension Type 2)

**What it means:**
A data warehousing pattern for tracking the full history of a dimension
(e.g., customer's region over time). Each change creates a new row instead of
overwriting the old one:
- Old row: `is_current = FALSE`, `effective_to = change_date`
- New row: `is_current = TRUE`,  `effective_from = change_date`

**Why Type 2 (not Type 1)?**
Type 1 overwrites (no history). Type 2 keeps full history for point-in-time
analysis: "What was the customer's region when this order was placed?"

**Nugget:** `04_de_patterns/03_scd_type2.py`

---

## Snapshot Isolation

**What it means:**
A transaction isolation level where each reader sees a consistent point-in-time
snapshot of the data, regardless of concurrent writes. Readers never block writers
and writers never block readers.

**How Delta implements it:** When you query a Delta table, Spark reads the
latest committed version from `_delta_log/`. Any in-progress writes to new files
are not visible until their log entry is committed.

**PostgreSQL:** Uses MVCC (Multi-Version Concurrency Control) for the same effect.

**Nugget:** `03_delta_core/01_acid_and_transactions.py`

---

## Time Travel

**What it means:**
The ability to query any historical version of a Delta table using either a
version number or a timestamp.

```sql
-- By version number
SELECT * FROM table VERSION AS OF 5

-- By timestamp
SELECT * FROM table TIMESTAMP AS OF '2024-01-15 14:30:00'

-- Restore to a version
RESTORE TABLE table TO VERSION AS OF 5
```

**How it works:** Historical Parquet files are preserved until `VACUUM` cleans them.
The `_delta_log/` maps versions to file sets.

**PostgreSQL:** No native equivalent. Requires manual audit tables or point-in-time
backup restore.

**Snowflake:** `AT(VERSION => N)` or `AT(TIMESTAMP => ...)` syntax. Max 90 days
on Enterprise.

**Nugget:** `03_delta_core/03_time_travel.py`

---

## Unity Catalog

**What it means:**
Databricks' unified governance layer that manages access control, data lineage,
and auditing across all workspaces in an organization. Introduces a 3-level
namespace: `catalog.schema.table`.

**The 3-level namespace:**
```
nugget_lab        <- CATALOG  (top level, like a PostgreSQL cluster/database)
  .bridge_lab     <- SCHEMA   (like a PostgreSQL schema)
    .sales_orders <- TABLE
```

**Grant hierarchy:** You must grant permissions at each level:
1. `GRANT USE CATALOG ON CATALOG c TO group`
2. `GRANT USE SCHEMA ON SCHEMA c.s TO group`
3. `GRANT SELECT ON TABLE c.s.t TO group`

**PostgreSQL analogy:** `database.schema.table` with `GRANT` at each level.

**Nugget:** `06_governance_and_security/01_unity_catalog_and_grants.py`

---

## Watermark (Incremental Load)

**What it means:**
A high-water mark timestamp or version number that tracks the last successfully
processed batch. On each pipeline run:
1. Read watermark from control table
2. Query source for records AFTER the watermark
3. Process and load to target
4. Update watermark **only on success**

**Why idempotency matters:** If the pipeline fails after step 3 but before step 4,
the next run re-processes the same records (safe duplicate handling via MERGE).

**Nugget:** `04_de_patterns/04_incremental_and_late_events.py`

---

## Z-ORDER

**What it means:**
A multi-dimensional data clustering technique used with `OPTIMIZE`. Z-ORDER
sorts data within each Parquet file by the specified columns using a
space-filling curve, so that rows with similar values end up in the same file.
This enables data skipping: queries that filter on Z-ORDERed columns need to
read fewer files.

```sql
OPTIMIZE table ZORDER BY (customer_id, product_id)
```

**When to use:** High-cardinality columns that appear in WHERE clauses.
Maximum 4 columns (diminishing returns beyond 2-3).

**Do NOT:** Z-ORDER a partition column (already separated into directories).

**PostgreSQL analogy:** `CLUSTER TABLE t USING index` performs a one-time physical
sort. Z-ORDER is a recurring operation (re-applied during OPTIMIZE).

**Snowflake analogy:** `CLUSTER BY (col1, col2)` -- Snowflake maintains clustering
automatically; Databricks requires periodic `OPTIMIZE ZORDER BY`.

**Nugget:** `03_delta_core/04_optimize_and_zorder.py`

---

## Personal Access Token (PAT)

**What it means:**
A long-lived authentication token (starts with `dapi`) used to authenticate
Databricks API calls and SQL Warehouse connections. Equivalent to an
application password for non-interactive authentication.

**Where to create:** Databricks UI -> User Settings -> Developer -> Access Tokens

**Security best practice:** Use a service principal (service account) PAT for
production pipelines, not a personal user PAT.

**Nugget:** `00_setup/00_prereq_check.py`

---

## SQL Warehouse

**What it means:**
Databricks' serverless compute endpoint for SQL queries. Replaces the older
"All-Purpose Cluster" for pure SQL workloads. Key properties:
- Auto-starts on first query (cold start: 30-90s)
- Auto-suspends after inactivity (saves cost)
- Multiple concurrent users share one warehouse
- HTTP path format: `/sql/1.0/warehouses/<id>`

**PostgreSQL analogy:** The PostgreSQL server process. But unlike PG, a SQL
Warehouse bills per second of actual compute use.

**Snowflake analogy:** Virtual Warehouse (same auto-suspend concept).

**Nugget:** `00_setup/00_prereq_check.py`
