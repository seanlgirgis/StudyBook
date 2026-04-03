# Databricks Bridge: Speedy Story and Interview Pack

A story from PostgreSQL practitioner to Databricks Data Engineer,
plus 30+ interview Q&A you can answer confidently.

---

## Part 1: The Story (PostgreSQL -> Databricks)

### Chapter 1: You Already Know More Than You Think

If you know PostgreSQL, you know 70% of Databricks SQL already.
The same `SELECT`, `JOIN`, `GROUP BY`, `HAVING`, `WITH`, `WINDOW OVER`
syntax works identically. The commands look familiar because they
follow the SQL standard (SQL:2003) that PostgreSQL helped define.

What changes is the *engine beneath the SQL*:
- PostgreSQL: row-oriented heap storage on a single machine (or small cluster)
- Databricks: columnar Parquet files distributed across many machines (Spark)

### Chapter 2: The Storage Revolution

PostgreSQL stores data in 8 KB heap pages on disk. A table with 100 million rows
is a large sequential file on one server. If the server runs out of memory or
disk, you're stuck.

Databricks stores data as Parquet files in object storage (S3, ADLS, GCS).
Parquet is *columnar*: scanning `SUM(revenue)` reads only the revenue column,
not all 9 columns in the row. For analytics queries (aggregations, scans),
this is 5-10x faster than a row store.

Delta Lake adds a transaction log on top of Parquet:
```
table/
  _delta_log/       <- JSON transaction log (the WAL equivalent)
    00000001.json
    00000002.json
  part-00001.parquet  <- actual data
  part-00002.parquet
```

Every commit writes a new log file. Readers find the latest consistent state
by reading the log. Old Parquet files are kept until VACUUM, enabling Time Travel.

### Chapter 3: The Compute Revolution

PostgreSQL is always-on. You pay for the server 24/7 whether you query or not.

Databricks uses a SQL Warehouse: compute that **auto-starts** when you query
and **auto-suspends** when idle. You pay only for seconds of actual execution.
For intermittent workloads, this is dramatically cheaper.

The trade-off: a stopped warehouse has a cold start time of 30-90 seconds.
For production pipelines, keep a small warehouse warm. For ad-hoc analysis,
accept the cold start.

### Chapter 4: Scaling What PostgreSQL Can't

PostgreSQL runs on one machine (leader + replicas). A 1 TB table on PostgreSQL
requires a very large single machine. Adding replicas helps reads but not writes.

Databricks runs Spark, which splits tables into partitions and processes them
on hundreds of machines in parallel. A 1 TB table becomes 8,000 x 128 MB
Parquet files processed across 50 executors simultaneously.

The developer experience is the same: you write SQL. Spark handles distribution.

### Chapter 5: The Three New Concepts to Master

1. **Delta ACID via log, not WAL**
   - Same ACID guarantees as PostgreSQL; different mechanism
   - `DESCRIBE HISTORY` shows every transaction (like `pg_xact`)
   - Time Travel queries any past version (PostgreSQL has no equivalent)

2. **MERGE replaces ON CONFLICT**
   - PostgreSQL: `INSERT ... ON CONFLICT DO UPDATE` (INSERT + UPDATE only)
   - Databricks MERGE: INSERT + UPDATE + DELETE in one atomic statement
   - MERGE is the foundation of SCD2, CDC processing, and deduplication

3. **OPTIMIZE is a manual operation**
   - PostgreSQL VACUUM runs automatically in the background
   - Delta OPTIMIZE must be scheduled or triggered manually
   - OPTIMIZE + ZORDER BY = compaction + data clustering in one command

---

## Part 2: 30+ Interview Q&A

### Foundations

**Q1: What is Delta Lake and how does it differ from plain Parquet?**
Delta Lake adds a transaction log (`_delta_log/`) on top of Parquet files.
This gives you: ACID transactions, schema enforcement, Time Travel, MERGE support,
and OPTIMIZE/ZORDER. Plain Parquet is just files -- no ACID, no history, no upserts.

**Q2: How does Delta ensure ACID compliance?**
Atomicity: writes are committed by creating a log entry. If the process dies
before the log entry is written, the Parquet files exist but are invisible to readers.
Isolation: readers see a consistent snapshot from the log. Writers use optimistic
concurrency (retry on conflict).

**Q3: What is snapshot isolation in Delta?**
Every reader gets a consistent point-in-time view of the table from the transaction log.
No dirty reads. Multiple readers can run concurrently with writers without blocking.
PostgreSQL achieves this via MVCC; Delta achieves it via immutable Parquet files +
transaction log.

**Q4: What is the difference between a SQL Warehouse and an All-Purpose Cluster?**
SQL Warehouse: optimized for SQL queries, auto-suspend/resume, cost-efficient for
analytics. All-Purpose Cluster: general-purpose Spark cluster for notebooks, Python,
Scala -- always billable while running. Use SQL Warehouse for production SQL pipelines.

**Q5: How do you authenticate to Databricks programmatically?**
With a Personal Access Token (PAT). Set `DATABRICKS_HOST` and `DATABRICKS_TOKEN`
as environment variables (or in a secrets manager). The Python connector uses
these via `databricks-sql-connector`.

---

### Delta Lake Deep Dive

**Q6: Walk me through the Delta transaction log structure.**
Each commit creates a numbered JSON file in `_delta_log/`.
The JSON lists which Parquet files were added (`add`) and which were removed (`remove`).
Readers reconstruct the current state by replaying all log entries.
Every 10 commits, Delta creates a checkpoint file (Parquet) to speed up log reading.

**Q7: What is Time Travel and when would you use it?**
Time Travel lets you query any past version: `SELECT * FROM t VERSION AS OF 5`.
Use cases: (1) Audit queries ("what did the table look like yesterday?"),
(2) Recovery from accidental deletes (`RESTORE TABLE`),
(3) ML reproducibility (always train on version N),
(4) Debugging ("which commit caused the anomaly?").

**Q8: What happens after VACUUM? Can you still time-travel?**
VACUUM removes Parquet files older than the retention period (default 7 days).
After vacuum, time travel before that retention window is GONE permanently.
Never run `VACUUM RETAIN 0 HOURS` in production.

**Q9: How does schema enforcement work in Delta?**
Delta stores the schema in the transaction log. On every write, Spark validates
the incoming data against the stored schema. Extra columns or wrong types cause
an `AnalysisException` and the write is rejected entirely.
To evolve the schema: `ALTER TABLE ADD COLUMN` (metadata-only) or use `mergeSchema`.

**Q10: Explain OPTIMIZE and when you should run it.**
OPTIMIZE rewrites small Parquet files into 128 MB target files to solve the
"small files problem". Run it when: (1) you do many small incremental writes
(streaming or hourly batches), (2) query scan times are degrading,
(3) `DESCRIBE DETAIL` shows a high file count. Schedule it as a daily job
or use Databricks Auto-Optimize (on supported cluster types).

---

### Performance

**Q11: What is the difference between PARTITION BY and ZORDER BY?**
`PARTITION BY`: physical directory split by column (good for low-cardinality:
date, country). Each value gets its own directory. Queries filter on that column
read only the matching directory (partition pruning).
`ZORDER BY` (in OPTIMIZE): within-partition data clustering by column(s),
good for high-cardinality (customer_id, product_id). Enables data skipping
within files. Rule: never ZORDER a column you already PARTITION BY.

**Q12: When should you add a BROADCAST hint to a join?**
When one table is small enough to fit in memory (typically < 10 MB, configurable).
`SELECT /*+ BROADCAST(small_table) */ ...` forces the planner to broadcast
the small table to all executors instead of shuffling both sides.
Spark AQE does this automatically for very small tables; the hint overrides
the size threshold.

**Q13: How do you read an EXPLAIN plan in Databricks?**
Plans read bottom-up. Key operators to look for:
- `FileScan with pushedFilters`: predicate push-down working
- `Exchange`: shuffle (expensive, try to minimize)
- `BroadcastHashJoin`: small table broadcast (good, no shuffle)
- `HashAggregate`: fast in-memory aggregation
- `SortMergeJoin`: shuffle-based join (acceptable for large tables)

**Q14: A query is slow. What is your debugging checklist?**
1. EXPLAIN: look for Exchange nodes (shuffles)
2. Check WHERE clause uses partition column (partition pruning)
3. ANALYZE TABLE: ensure optimizer has fresh statistics
4. OPTIMIZE + ZORDER on join/filter key columns
5. Add BROADCAST hint for small lookup tables
6. Check DESCRIBE DETAIL for file count (small files problem)
7. Check Data Skew: one partition much larger than others

---

### DE Patterns

**Q15: How do you build an idempotent incremental pipeline?**
1. Use a watermark control table (stores last processed date/version)
2. Query source WHERE event_date > watermark
3. Load to target using MERGE (not INSERT -- MERGE handles duplicates)
4. Update watermark ONLY AFTER successful load
5. On failure: watermark stays old value; next run re-processes safely

**Q16: What is SCD Type 2 and how do you implement it in Delta?**
SCD Type 2 keeps full history of dimension attribute changes.
Implementation:
- Step 1: MERGE to expire old rows (set `is_current=FALSE`, `effective_to=change_date`)
- Step 2: INSERT new rows (`is_current=TRUE`, `effective_from=change_date`)
- Query: `WHERE date BETWEEN effective_from AND COALESCE(effective_to, '9999-12-31')`

**Q17: How do you deduplicate a Delta table?**
Use ROW_NUMBER() CTE pattern:
```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY business_key ORDER BY updated_at DESC) AS rn
  FROM raw_table
)
INSERT INTO clean_table SELECT * FROM ranked WHERE rn = 1
```
Or use MERGE with NOT MATCHED condition (append-only dedup).

**Q18: What is late-arriving data and how do you handle it?**
A late event arrives after its event window has already been processed.
Strategies: (1) Set a late-arrival tolerance window (process events up to
N hours late). (2) Re-run the affected time window (idempotent pipeline handles this).
(3) Flag late events and correct downstream aggregates on next run.

**Q19: What is CDC and how do you process it in Databricks?**
Change Data Capture captures INSERT/UPDATE/DELETE events from a source database.
In Databricks: use MERGE with a `_op` column:
`WHEN MATCHED AND _op='U' THEN UPDATE`, `WHEN MATCHED AND _op='D' THEN DELETE`,
`WHEN NOT MATCHED AND _op='I' THEN INSERT`.

---

### Governance

**Q20: What is Unity Catalog?**
Unity Catalog is Databricks' unified governance layer. It introduces a 3-level
namespace: `catalog.schema.table`. Access is controlled with GRANT/REVOKE at each
level. It provides row-level security, column masking, data lineage, and
cross-workspace data sharing from one central metastore.

**Q21: What is the minimum grant chain to give an analyst SELECT access?**
Three grants are required:
1. `GRANT USE CATALOG ON CATALOG c TO analyst_group`
2. `GRANT USE SCHEMA ON SCHEMA c.s TO analyst_group`
3. `GRANT SELECT ON TABLE c.s.t TO analyst_group`
Without GRANT 1 and 2, GRANT 3 alone is not sufficient.

**Q22: How does row-level security work in Unity Catalog?**
Using Row Filters: a SQL function is defined that returns a boolean condition.
Attach it to a table: `ALTER TABLE t SET ROW FILTER func ON (user_id)`.
Databricks automatically appends the filter to every query by that user.

---

### PostgreSQL -> Databricks Transfer

**Q23: I know PostgreSQL. What do I need to learn differently for Databricks?**
Same: SELECT, JOIN, GROUP BY, HAVING, WITH, WINDOW OVER, MERGE (PG 15+).
Different: (1) No multi-table transactions (single-table ACID only in Delta).
(2) OPTIMIZE is manual (no auto-vacuum). (3) Time Travel (no equivalent in PG).
(4) No WITH RECURSIVE (use Spark DataFrame API). (5) PARTITION BY creates
physical directories (PG also has this, but managed differently).

**Q24: How does Delta's transaction model compare to PostgreSQL transactions?**
PostgreSQL: `BEGIN; DML on t1; DML on t2; COMMIT;` -- multi-table atomicity.
Delta: each MERGE/INSERT/UPDATE/DELETE on a single table is atomic.
No cross-table transactions. Design pipelines with single-table MERGE operations
and idempotent re-runs instead.

**Q25: What replaces PostgreSQL's INSERT ... ON CONFLICT in Databricks?**
`MERGE INTO target USING source ON key WHEN MATCHED THEN UPDATE WHEN NOT MATCHED THEN INSERT`.
MERGE is more powerful: handles DELETE too, supports multiple WHEN clauses,
and is the SQL:2003 standard (available in PG 15+, Snowflake, BigQuery).

**Q26: How is EXPLAIN different between PostgreSQL and Databricks?**
PostgreSQL `EXPLAIN ANALYZE` shows estimated + actual rows and execution time.
Databricks `EXPLAIN` shows the logical + physical Spark plan but no actual times.
For actual metrics: use the Databricks Query Profile tab in the SQL editor,
or query the Databricks system tables for query history.

**Q27: I'm used to PostgreSQL VACUUM. What's the equivalent in Databricks?**
Two separate operations:
- `OPTIMIZE`: compacts small files (equivalent to heap reorganization). Manual/scheduled.
- `VACUUM`: removes old Parquet files beyond the retention window. Similar to PG VACUUM
  reclaiming dead tuples, but with a 7-day retention default (don't go lower).

**Q28: Does Databricks support recursive CTEs?**
No. `WITH RECURSIVE` is not supported in Databricks SQL. Use the Spark DataFrame
API (GraphFrames library for graph traversal) or iterative Python processing.
Snowflake also lacks recursive CTE support.

---

### System Design

**Q29: Design an idempotent daily batch pipeline for a sales data feed.**
Architecture:
1. Bronze: land raw CSV files from S3 into Delta (COPY INTO, _batch_id column)
2. Control: insert batch record into `ingestion_control` with status='running'
3. Silver: MERGE deduped+validated data from Bronze using `order_id` as key
4. Gold: `INSERT OVERWRITE` or MERGE aggregates (daily partitions)
5. Control: update batch record to status='success', update watermark
6. OPTIMIZE: compact Silver and Gold tables (daily schedule)
7. On failure: control status stays 'running'; next run detects and retries

**Q30: A senior engineer says "our Delta table has 50,000 small files." What do you do?**
1. Run `OPTIMIZE table ZORDER BY (join_key_column)` immediately to compact.
2. Check the root cause: are there micro-batch writes every minute? Consider
   coalescing batches to hourly.
3. Enable Delta Auto-Optimize on the table (if supported).
4. Set up a recurring OPTIMIZE job (daily, off-peak).
5. Review PARTITION BY strategy: over-partitioned tables generate one file per partition
   per micro-batch.

**Q31: How do you handle schema drift in an incoming data feed?**
1. Catch the schema mismatch exception in your pipeline.
2. Run `DESCRIBE TABLE` to see current schema.
3. Use `ALTER TABLE ADD COLUMN` for new columns (backward-compatible).
4. For type changes: write to a staging table, validate, then CTAS to replace.
5. Log schema changes to an audit table.
6. Alert the upstream team.
7. Never use `mergeSchema=True` silently in production -- require human approval.

**Q32: How would you design a Bronze->Silver->Gold pipeline for streaming events?**
Bronze: Structured Streaming with `writeStream.format("delta")` writing to
`events_bronze`. Use `appendOnly` mode, never dedup in Bronze.
Silver: Streaming MERGE using `foreachBatch` -- dedup by `event_id`,
filter nulls, enrich with dimension tables.
Gold: Triggered streaming job (every hour) that reads Silver and
does `INSERT OVERWRITE` into partition (e.g., `event_date`) for idempotency.
Time Travel: Silver retains 7-day history for late event reprocessing.

---

## Part 3: Quick Reference

### Databricks SQL Cheat Sheet

```sql
-- Time Travel
SELECT * FROM t VERSION AS OF 5
SELECT * FROM t TIMESTAMP AS OF '2024-01-15 14:30:00'
RESTORE TABLE t TO VERSION AS OF 5
DESCRIBE HISTORY t LIMIT 10

-- MERGE (upsert)
MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...
WHEN MATCHED AND _op='D' THEN DELETE

-- OPTIMIZE
OPTIMIZE nugget_lab.bridge_lab.sales_orders
OPTIMIZE nugget_lab.bridge_lab.sales_orders ZORDER BY (customer_id)

-- Schema
ALTER TABLE t ADD COLUMN new_col STRING
DESCRIBE TABLE t
DESCRIBE DETAIL t
ANALYZE TABLE t COMPUTE STATISTICS

-- Namespace
SHOW CATALOGS
SHOW SCHEMAS IN catalog_name
USE CATALOG catalog_name
USE SCHEMA catalog.schema
SELECT CURRENT_USER(), CURRENT_CATALOG(), CURRENT_SCHEMA()

-- Window functions (same as PostgreSQL)
ROW_NUMBER() OVER (PARTITION BY col ORDER BY col)
LAG(col, 1, 0) OVER (PARTITION BY col ORDER BY col)
SUM(col) OVER (PARTITION BY col ORDER BY col ROWS UNBOUNDED PRECEDING)
PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY col)
```

### Key Differences at a Glance

| Topic | PostgreSQL | Databricks SQL |
|-------|-----------|----------------|
| Storage | Row-oriented heap | Columnar Parquet + Delta log |
| Compute | Always-on server | Auto-suspend SQL Warehouse |
| ACID scope | Multi-table | Single-table per statement |
| VACUUM | Automatic | Manual OPTIMIZE (compaction) |
| Time Travel | Not native | Native (7 days default) |
| Upsert | ON CONFLICT | MERGE |
| Recursive CTE | Yes | No -- use Spark API |
| JSON | JSONB with -> operator | STRING with built-in functions |
| Clustering | CLUSTER BY (one-time) | ZORDER BY (recurring with OPTIMIZE) |
