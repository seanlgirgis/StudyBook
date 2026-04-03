# Cross-Engine SQL Map: PostgreSQL -> Databricks SQL -> Snowflake

This document maps equivalent SQL patterns across the three engines
so you can transfer knowledge between them quickly.

Each mapping links to the runnable nugget where the pattern is demonstrated.

---

## 1. CTE and Windowing

| Pattern | PostgreSQL | Databricks SQL | Snowflake |
|---------|-----------|----------------|-----------|
| Basic CTE | `WITH cte AS (SELECT ...)` | Identical | Identical |
| Chained CTEs | `WITH a AS (...), b AS (SELECT ... FROM a)` | Identical | Identical |
| Recursive CTE | `WITH RECURSIVE cte AS (...)` | **NOT SUPPORTED** -- use Spark API | **NOT SUPPORTED** |
| Materialized CTE | `WITH cte AS MATERIALIZED (...)` | No syntax; optimizer decides | No syntax; optimizer decides |
| ROW_NUMBER | `ROW_NUMBER() OVER (PARTITION BY x ORDER BY y)` | Identical | Identical |
| RANK / DENSE_RANK | `RANK() OVER (...)` | Identical | Identical |
| LAG / LEAD | `LAG(col, 1, default) OVER (ORDER BY y)` | Identical | Identical |
| Running SUM | `SUM(col) OVER (ORDER BY y ROWS UNBOUNDED PRECEDING)` | Identical | Identical |
| NTILE | `NTILE(4) OVER (ORDER BY col)` | Identical | Identical |
| FIRST_VALUE / LAST_VALUE | `FIRST_VALUE(col) OVER (PARTITION BY x ...)` | Identical | Identical |
| PERCENTILE_CONT | `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY col)` | Identical | Identical |
| FILTER on aggregate | `SUM(col) FILTER (WHERE cond)` | Identical | Identical |

**Runnable demos:** `02_cte_and_windowing/01_ctes.py`, `02_cte_and_windowing/02_window_functions.py`, `02_cte_and_windowing/03_advanced_analytics.py`

---

## 2. Upsert / MERGE and SCD Type 2

| Pattern | PostgreSQL | Databricks SQL | Snowflake |
|---------|-----------|----------------|-----------|
| Upsert (INSERT or UPDATE) | `INSERT INTO t ... ON CONFLICT (key) DO UPDATE SET col = EXCLUDED.col` | `MERGE INTO t USING src ON key WHEN MATCHED THEN UPDATE WHEN NOT MATCHED THEN INSERT` | Same as Databricks MERGE |
| Upsert with DELETE | Not in ON CONFLICT; requires separate DELETE | `MERGE ... WHEN MATCHED AND cond THEN DELETE` | Same as Databricks |
| SCD Type 2 expire | `BEGIN; UPDATE old; INSERT new; COMMIT;` | Two-step MERGE: expire + insert new version | Same two-step MERGE |
| Point-in-time query | `WHERE date BETWEEN effective_from AND COALESCE(effective_to, '9999-12-31')` | Identical | Identical |

**Key difference:** PostgreSQL `ON CONFLICT` only handles INSERT + UPDATE. Delta MERGE adds DELETE and multiple WHEN clauses in one atomic statement.

**Runnable demos:** `04_de_patterns/02_merge_upsert.py`, `04_de_patterns/03_scd_type2.py`

---

## 3. Transactions and Isolation Caveats

| Concept | PostgreSQL | Databricks SQL | Snowflake |
|---------|-----------|----------------|-----------|
| Transaction scope | Multi-table: `BEGIN; DML on t1; DML on t2; COMMIT;` | **Single table only** -- no multi-table COMMIT | **Single table only** |
| Isolation level | READ COMMITTED (default), SERIALIZABLE | **Snapshot isolation** (optimistic concurrency) | **Serializable** (Snowflake enforces) |
| Dirty reads | Prevented by MVCC | Prevented by Delta snapshot reads | Prevented |
| Concurrent write conflict | Last writer wins (with SERIALIZABLE: error) | Optimistic: conflict detected at commit, writer retries | Serializable: conflict -> retry |
| WAL / Transaction log | WAL (redo log) | `_delta_log/` JSON entries | Hidden micro-partition log |
| ROLLBACK | Full multi-table rollback | No ROLLBACK keyword; partial writes discarded automatically | No explicit ROLLBACK |
| SAVEPOINT | Supported | Not supported | Not supported |

**Key caveat:** Delta Lake does NOT support multi-table transactions. Design pipelines to use single-table MERGE operations and idempotent re-runs instead of relying on cross-table atomicity.

**Runnable demo:** `03_delta_core/01_acid_and_transactions.py`

---

## 4. EXPLAIN / Profile Tooling Equivalence

| Operation | PostgreSQL | Databricks SQL | Snowflake |
|-----------|-----------|----------------|-----------|
| Show query plan | `EXPLAIN SELECT ...` | `EXPLAIN SELECT ...` | `EXPLAIN USING TABULAR SELECT ...` |
| Show plan + actual stats | `EXPLAIN ANALYZE SELECT ...` | No SQL equivalent -- use Databricks Query Profile UI | `EXPLAIN USING STATISTICS SELECT ...` |
| Identify shuffle/sort | Plan shows `Hash Join`, `Sort` | Plan shows `Exchange`, `SortMergeJoin` | Plan shows `JoinFilter`, `Aggregate` |
| Collect column stats | `ANALYZE table` | `ANALYZE TABLE t COMPUTE STATISTICS` | Automatic (Snowflake manages) |
| Identify predicate push-down | `Seq Scan` vs `Index Scan` | `FileScan pushedFilters` | `TableScan` with `pruning` |
| Force join order | `SET enable_hashjoin=off` | `/*+ BROADCAST(t) */` hint | No manual hint; optimizer decides |

**Key difference:** PostgreSQL `EXPLAIN ANALYZE` shows actual execution time. Databricks `EXPLAIN` shows the logical/physical plan only -- use the Spark UI or Query Profile tab for actual metrics.

**Runnable demo:** `05_performance_and_optimization/01_explain_and_profiling.py`

---

## 5. Null and Type Behavior Gotchas

| Gotcha | PostgreSQL | Databricks SQL | Snowflake |
|--------|-----------|----------------|-----------|
| NULL = NULL | `FALSE` (use `IS NOT DISTINCT FROM`) | `FALSE` (use `IS NOT DISTINCT FROM` or `<=>`) | `FALSE` (use `EQUAL_NULL`) |
| NULL in IN list | `NULL IN (1, NULL)` returns NULL (not TRUE) | Same | Same |
| NOT IN with NULL | `NOT IN (1, NULL)` returns NULL (no rows) | Same -- use NOT EXISTS instead | Same |
| Integer division | `5 / 2 = 2` (integer truncation) | `5 / 2 = 2` (integer truncation) | `5 / 2 = 2.5` (auto-promotes to FLOAT) |
| Implicit cast | Strict -- explicit CAST usually needed | Permissive -- many auto-casts | Permissive |
| BOOLEAN type | Native `BOOLEAN` | Native `BOOLEAN` | Native `BOOLEAN` |
| DECIMAL precision | Up to 131072 digits | Up to DECIMAL(38, N) | Up to DECIMAL(38, N) |
| JSON | `JSONB` column type + `->` operator | `STRING` column + `JSON_OBJECT_KEYS()` or `PARSE_JSON()` | `VARIANT` column + `:field` accessor |
| Auto-increment | `SERIAL` or `IDENTITY` | `BIGINT GENERATED ALWAYS AS IDENTITY` (Runtime 10.4+) | `AUTOINCREMENT` |
| TIMESTAMP with TZ | `TIMESTAMPTZ` | `TIMESTAMP_LTZ` | `TIMESTAMP_LTZ` |

**Key gotchas:**
1. `NOT IN (subquery)` returns zero rows if subquery has any NULL -- use `NOT EXISTS`.
2. Snowflake auto-promotes integer division; Databricks truncates like PostgreSQL.
3. Never store money as `FLOAT` -- use `DECIMAL(10,2)` in all three engines.

**Runnable demos:** `01_sql_foundations/03_subqueries.py` (NULL safety), `07_data_quality_and_testing/01_data_quality_checks.py` (null checks)

---

## 6. Data Loading Patterns

| Pattern | PostgreSQL | Databricks SQL | Snowflake |
|---------|-----------|----------------|-----------|
| Bulk load from file | `COPY t FROM '/path/file.csv' CSV` | `COPY INTO t FROM 's3://bucket/path' FILEFORMAT=CSV` | `COPY INTO t FROM @stage FILEFORMAT=CSV` |
| CTAS | `CREATE TABLE t AS SELECT ...` | `CREATE TABLE t USING DELTA AS SELECT ...` | `CREATE TABLE t AS SELECT ...` |
| INSERT SELECT | `INSERT INTO t SELECT ...` | Identical | Identical |
| Idempotent insert | `INSERT ... ON CONFLICT DO NOTHING` | `MERGE ... WHEN NOT MATCHED THEN INSERT` | `MERGE ... WHEN NOT MATCHED THEN INSERT` |
| Truncate + reload | `TRUNCATE TABLE t; INSERT INTO t SELECT ...` | `INSERT OVERWRITE t SELECT ...` | Same as Databricks |

---

## 7. Schema and DDL Patterns

| Pattern | PostgreSQL | Databricks SQL | Snowflake |
|---------|-----------|----------------|-----------|
| Create schema | `CREATE SCHEMA name` | `CREATE SCHEMA catalog.name` | `CREATE SCHEMA db.name` |
| Add column | `ALTER TABLE t ADD COLUMN c TYPE` | `ALTER TABLE t ADD COLUMN c TYPE` | `ALTER TABLE t ADD COLUMN c TYPE` |
| Drop column | `ALTER TABLE t DROP COLUMN c` | `ALTER TABLE t DROP COLUMN c` (needs column mapping) | `ALTER TABLE t DROP COLUMN c` |
| Rename column | `ALTER TABLE t RENAME COLUMN old TO new` | Needs column mapping enabled | `ALTER TABLE t RENAME COLUMN old TO new` |
| Table comment | `COMMENT ON TABLE t IS '...'` | `COMMENT 'text' ON TABLE t` or in CREATE TABLE | `COMMENT = 'text'` in CREATE |
| Column comment | `COMMENT ON COLUMN t.col IS '...'` | `COMMENT 'text'` inline in CREATE or ALTER | Inline in CREATE |
| Show table DDL | `\d+ table_name` (psql) | `DESCRIBE TABLE t` or `SHOW CREATE TABLE t` | `GET DDL(TABLE, 't')` |

---

## Engine Summary

| Feature | PostgreSQL | Databricks SQL | Snowflake |
|---------|-----------|----------------|-----------|
| Default storage | Heap (row-oriented) | Delta Lake (Parquet columnar) | Micro-partitions (columnar) |
| Time Travel | Not native (CDC/backup) | Native (DESCRIBE HISTORY, VERSION AS OF) | Native (AT(VERSION => N), up to 90 days) |
| Small file compaction | VACUUM (automatic) | OPTIMIZE (manual or scheduled) | Automatic |
| Data clustering | CLUSTER BY (one-time sort) | ZORDER BY (with OPTIMIZE) | CLUSTER BY (automatic maintenance) |
| MERGE | PG 15+ (SQL standard) | Full MERGE with DELETE | Full MERGE with DELETE |
| Multi-table transactions | Yes (COMMIT/ROLLBACK) | No (single-table only) | No (single-table only) |
| Recursive CTE | Yes (WITH RECURSIVE) | No | No |
| JSON support | JSONB (indexed) | STRING + built-in functions | VARIANT (semi-structured native) |
| Serverless compute | No (always-on) | SQL Warehouse (auto-suspend) | Virtual Warehouse (auto-suspend) |
