# PostgreSQL Speedy Story & Interview Guide

## The 30-Second Story

> "PostgreSQL is the most advanced open-source relational database. It's the default
> choice for startups and increasingly for enterprises replacing Oracle. It supports
> full ACID transactions, complex joins, window functions, CTEs, JSONB (with GIN indexes),
> full-text search, and extensions like PostGIS. For data engineers, it's both a source
> system and a transformation engine — many ELT pipelines use PostgreSQL as the staging
> and serving layer."

---

## Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PostgreSQL Server                         │
│  (Single process with background workers)                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Shared      │  │  Background  │  │  Backend     │      │
│  │  Buffers     │  │  Writers     │  │  Processes   │      │
│  │  (RAM)       │  │  (WAL, etc)  │  │  (per conn)  │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │               │
│         └─────────────────┼─────────────────┘               │
│                           │                                 │
│                    ┌──────▼───────┐                         │
│                    │  Write-Ahead │                         │
│                    │  Log (WAL)   │                         │
│                    │  (durability)│                         │
│                    └──────┬───────┘                         │
│                           │                                 │
│                    ┌──────▼───────┐                         │
│                    │  Data Files  │                         │
│                    │  (on disk)   │                         │
│                    └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Concepts for Interviews

### 1. ACID Transactions

**Atomicity:** All or nothing — ROLLBACK undoes everything.
**Consistency:** Database moves from one valid state to another (constraints enforced).
**Isolation:** Concurrent transactions don't interfere (controlled by isolation levels).
**Durability:** Committed data survives crashes (Write-Ahead Log ensures this).

### 2. Isolation Levels

| Level | Phenomenon Prevented | Use Case |
|-------|---------------------|----------|
| Read Committed (default) | Dirty reads | Most OLTP workloads |
| Repeatable Read | Non-repeatable reads | Reporting, analytics |
| Serializable | All anomalies | Financial systems |

PostgreSQL doesn't have Read Uncommitted — it maps to Read Committed.

### 3. Indexes

**B-tree (default):** =, <, >, BETWEEN, LIKE 'prefix%'
**GIN:** JSONB, arrays, full-text search
**GiST:** Geometric, full-text, custom types
**BRIN:** Large tables with natural ordering (time-series)
**Hash:** Only = (rarely used — B-tree is almost always better)

### 4. JSONB

- Binary JSON storage — indexed, queryable, modifiable.
- GIN index on JSONB columns enables fast key/value lookups.
- Used for semi-structured data: event payloads, config, API responses.
- `data->>'key'` returns text, `data->'key'` returns JSONB.

---

## Deep Interview Questions

### Q: "What's the difference between DELETE, TRUNCATE, and DROP?"

> "DELETE removes rows one at a time, fires triggers, can be rolled back,
> and is slow for large tables. TRUNCATE removes all rows instantly by
> deallocating data pages — no triggers, minimal WAL, but can be rolled back
> within a transaction. DROP removes the entire table definition and data —
> it's a DDL command, not DML."

### Q: "How does PostgreSQL handle upserts?"

> "PostgreSQL uses INSERT ... ON CONFLICT (unique_column) DO UPDATE SET ...
> This is atomic — no race conditions between check and insert. The EXCLUDED
> pseudo-table holds the values that were attempted. This is cleaner than
> SQL Server's MERGE syntax and avoids the 'merge instability' bugs."

### Q: "Explain VACUUM and why PostgreSQL needs it."

> "PostgreSQL uses MVCC (Multi-Version Concurrency Control). When you UPDATE
> or DELETE, old row versions aren't physically removed — they're marked dead
> but kept for running transactions. VACUUM reclaims this dead space so it
> can be reused. Without VACUUM, tables grow indefinitely. AUTOVACUUM runs
> automatically but may need tuning for write-heavy tables."

### Q: "What's the difference between a CTE and a subquery in PostgreSQL?"

> "In PostgreSQL < 12, CTEs were always materialized — they ran fully even
> if the outer query didn't need all rows. This made them 'optimization
> fences.' In PostgreSQL 12+, the optimizer can inline CTEs when safe,
> making them equivalent to subqueries. Use MATERIALIZED keyword to force
> materialization, or NOT MATERIALIZED to hint inlining."

### Q: "How would you optimize a slow query?"

> "1. EXPLAIN ANALYZE — see the actual execution plan, not estimates.
> 2. Look for Seq Scan on large tables — add an index.
> 3. Check for functions on indexed columns (WHERE UPPER(name)) — can't use index.
> 4. Check for implicit type conversion — WHERE int_col = '123' prevents index use.
> 5. Consider composite indexes for multi-column WHERE clauses.
> 6. Use partial indexes for filtered subsets: WHERE status = 'active'.
> 7. Run ANALYZE to update statistics — the planner needs accurate row estimates."

### Q: "What are window functions and when would you use them?"

> "Window functions compute across a set of rows related to the current row,
> but unlike GROUP BY, they don't collapse rows. Each input row produces
> one output row. I use them for:
> - Ranking: ROW_NUMBER(), RANK(), DENSE_RANK()
> - Time series: LAG(), LEAD() for period-over-period change
> - Running totals: SUM() OVER (ORDER BY date ROWS UNBOUNDED PRECEDING)
> - Moving averages: AVG() OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
> - Top-N per group: ROW_NUMBER() PARTITION BY category ORDER BY revenue DESC"

### Q: "What's SCD Type 2 and how do you implement it?"

> "SCD Type 2 (Slowly Changing Dimension) keeps full history of changes.
> Each row has valid_from and valid_to dates, and an is_current flag.
> When data changes:
> 1. UPDATE the current row: SET valid_to = today, is_current = false
> 2. INSERT a new row: valid_from = today, valid_to = NULL, is_current = true
> This lets you query the state of any dimension at any point in time."

### Q: "How do you handle deadlocks in PostgreSQL?"

> "PostgreSQL automatically detects deadlocks and aborts one transaction
> with a 'deadlock detected' error. Prevention is better than detection:
> 1. Always lock resources in the same order (e.g., ascending primary key).
> 2. Keep transactions short — less time holding locks = less chance of deadlock.
> 3. Use lower isolation levels when possible — fewer locks = fewer conflicts.
> 4. Retry aborted transactions — the application should handle deadlock errors gracefully."

---

## Quick Reference Commands

```sql
-- Session info
SELECT version();
SELECT current_database(), current_schema(), current_user;

-- List objects
\dt              -- list tables (psql meta-command)
\di              -- list indexes
\dv              -- list views

-- Query planning
EXPLAIN SELECT * FROM table WHERE col = 1;
EXPLAIN ANALYZE SELECT * FROM table WHERE col = 1;

-- Index management
CREATE INDEX idx_name ON table(col);
CREATE INDEX idx_composite ON table(col1, col2);
CREATE INDEX idx_partial ON table(col) WHERE status = 'active';
CREATE INDEX idx_jsonb ON table USING GIN (jsonb_col);

-- Maintenance
VACUUM ANALYZE table;
VACUUM FULL table;  -- reclaims space, exclusive lock

-- Materialized views
CREATE MATERIALIZED VIEW mv AS SELECT ...;
REFRESH MATERIALIZED VIEW mv;
REFRESH MATERIALIZED VIEW CONCURRENTLY mv;  -- requires UNIQUE index

-- Upsert
INSERT INTO table (id, name) VALUES (1, 'Alice')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;

-- Window functions
SELECT name, salary,
       RANK() OVER (ORDER BY salary DESC) AS rank,
       LAG(salary) OVER (ORDER BY hire_date) AS prev_salary
FROM employees;
```

---

## Citi Narrative Hook

> "At Citi, PostgreSQL was our workhorse for telemetry data ingestion and
> transformation. We used it as both the landing zone for raw events and the
> transformation engine for our capacity forecasting pipelines. The JSONB
> column type was critical — it let us ingest semi-structured event payloads
> without a rigid schema, then parse and validate them into structured tables.
> EXPLAIN ANALYZE was our daily debugging tool for slow pipeline queries."

---

Last updated: 2026-04-02
