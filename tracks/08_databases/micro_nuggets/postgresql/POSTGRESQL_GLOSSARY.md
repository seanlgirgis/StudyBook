# PostgreSQL Glossary

Plain-English definitions for every key term used in the micro-nuggets.

---

## A

**ACID** — Four properties that guarantee reliable transactions:
Atomicity (all or nothing), Consistency (valid state transitions),
Isolation (no interference between concurrent transactions),
Durability (committed data survives crashes).
→ *Demonstrated in:* `06_transactions_and_concurrency/01_transactions.py`

**ANALYZE** — Updates table statistics so the query planner can make good decisions.
Run after large data changes. AUTOVACUUM does this automatically.

**AUTOVACUUM** — Background process that runs VACUUM and ANALYZE automatically.
Prevents table bloat from dead rows and keeps planner statistics fresh.

---

## B

**B-tree** — Default index type in PostgreSQL. Balanced tree structure optimized
for equality and range comparisons (=, <, >, BETWEEN, LIKE 'prefix%').
→ *Demonstrated in:* `05_performance_tuning/01_explain_and_indexes.py`

**Bitmap Heap Scan** — Query plan node. Uses an index to find matching blocks,
then reads those blocks. Faster than Seq Scan for moderate selectivity.

---

## C

**CTE (Common Table Expression)** — Named subquery using WITH clause.
Makes complex queries readable by breaking them into named steps.
→ *Demonstrated in:* `02_cte_and_windowing/01_ctes.py`

**CHECK constraint** — Validates data at insert/update time.
Example: `CHECK (price > 0)` prevents negative prices.
→ *Demonstrated in:* `03_data_modeling/01_keys_and_constraints.py`

**Composite index** — Index on multiple columns. Follows leftmost prefix rule:
an index on (a, b) can serve queries on (a) or (a, b) but not (b) alone.

**Covering index** — Index that includes all columns needed by a query,
enabling index-only scans without reading the table.

---

## D

**Deadlock** — Two transactions each hold a lock the other needs.
PostgreSQL detects and aborts one. Prevention: lock in consistent order.
→ *Demonstrated in:* `06_transactions_and_concurrency/01_transactions.py`

**DENSE_RANK()** — Window function. Like RANK() but without gaps:
1, 2, 2, 3 (vs RANK's 1, 2, 2, 4).
→ *Demonstrated in:* `02_cte_and_windowing/02_window_functions.py`

**Denormalization** — Duplicating data across tables to avoid JOINs.
Faster reads, risk of inconsistency. Tradeoff vs normalization.
→ *Demonstrated in:* `03_data_modeling/02_normalization.py`

**DROP** — Removes a database object (table, index, schema) entirely.
Different from DELETE (removes rows) and TRUNCATE (removes all rows).

---

## E

**EXPLAIN** — Shows the query execution plan without running the query.
**EXPLAIN ANALYZE** — Runs the query and shows actual timing and row counts.
The #1 tool for query optimization in PostgreSQL.
→ *Demonstrated in:* `05_performance_tuning/01_explain_and_indexes.py`

**EXCLUDED** — Pseudo-table in ON CONFLICT clauses. Holds the values that
were attempted to insert. Used in upsert: `SET col = EXCLUDED.col`.

---

## F

**Foreign Key (FK)** — Enforces referential integrity. A value in one table
must exist as a primary key in another table. Prevents orphaned records.
→ *Demonstrated in:* `03_data_modeling/01_keys_and_constraints.py`

**FULL OUTER JOIN** — Returns all rows from both tables, matching where possible,
NULL where no match exists. Rarely used but important for completeness.

---

## G

**GIN index** — Generalized Inverted Index. Used for JSONB, arrays, full-text.
Enables fast key/value lookups within JSONB columns.

**GROUPING SETS** — Multiple GROUP BY aggregations in one query.
More efficient than UNION ALL of separate GROUP BY queries.
→ *Demonstrated in:* `01_sql_core/02_aggregation.py`

---

## H

**Hash Join** — Query plan node. Builds a hash table for one input, probes with
the other. Efficient for large equi-joins.

**HAVING** — Filters groups after aggregation (like WHERE but for GROUP BY).
`WHERE` filters rows before aggregation; `HAVING` filters groups after.

---

## I

**Index** — Data structure that speeds up row lookups. Like a book's index —
you find the page number without reading every page.
→ *Demonstrated in:* `05_performance_tuning/01_explain_and_indexes.py`

**Isolation Level** — Controls how concurrent transactions interact.
Read Committed (default), Repeatable Read, Serializable.
→ *Demonstrated in:* `06_transactions_and_concurrency/01_transactions.py`

---

## J

**JOIN** — Combines rows from two tables based on a condition.
INNER (matching only), LEFT (all from left + matching from right),
RIGHT (all from right + matching from left), FULL (all from both).
→ *Demonstrated in:* `01_sql_core/01_joins.py`

**JSONB** — Binary JSON storage in PostgreSQL. Indexed, queryable, modifiable.
Used for semi-structured data: event payloads, config, API responses.
→ *Demonstrated in:* `09_mini_capstone/01_mini_capstone.py`

---

## L

**LAG()** — Window function. Returns the value from N rows before the current row.
Used for period-over-period comparisons.
→ *Demonstrated in:* `02_cte_and_windowing/02_window_functions.py`

**LEFT JOIN** — Returns all rows from the left table, plus matching rows from
the right. Non-matching right columns are NULL.

---

## M

**Materialized View** — Pre-computed query result stored as a table.
Fast reads, but must be refreshed manually: `REFRESH MATERIALIZED VIEW`.
→ *Demonstrated in:* `03_data_modeling/02_normalization.py`

**MVCC (Multi-Version Concurrency Control)** — PostgreSQL's concurrency model.
Each transaction sees a consistent snapshot. Old row versions are kept until
VACUUM removes them.

---

## N

**Nested Loop** — Query plan node. Joins by iterating through one table and
looking up matches in the other. Fine for small inputs, slow for large ones.

**Normalization** — Organizing data to minimize redundancy. 3NF (Third Normal
Form) means: no repeating groups, no partial dependencies, no transitive
dependencies. Tradeoff: more JOINs needed for queries.
→ *Demonstrated in:* `03_data_modeling/02_normalization.py`

**NTILE(n)** — Window function. Divides rows into n roughly equal buckets.
Used for quartile/percentile grouping.

---

## O

**ON CONFLICT** — PostgreSQL's upsert syntax. `INSERT ... ON CONFLICT (col)
DO UPDATE SET ...` — insert or update atomically.
→ *Demonstrated in:* `04_de_patterns/01_de_patterns.py`

---

## P

**Partial index** — Index on a subset of rows. `CREATE INDEX ... WHERE status = 'active'`.
Smaller, faster, and more selective than a full index.

**Primary Key (PK)** — Uniquely identifies each row. Automatically creates a
unique index. Cannot be NULL. Every table should have one.
→ *Demonstrated in:* `03_data_modeling/01_keys_and_constraints.py`

---

## R

**RANK()** — Window function. Assigns rank with gaps for ties: 1, 2, 2, 4.
→ *Demonstrated in:* `02_cte_and_windowing/02_window_functions.py`

**Recursive CTE** — CTE that references itself. `WITH RECURSIVE cte AS (...)`.
Used for hierarchical data, date series, graph traversal.

**ROLLBACK** — Undoes all changes in the current transaction. The "A" in ACID.

**ROLLUP** — GROUP BY extension that adds hierarchical subtotals.
`GROUP BY ROLLUP (a, b)` produces: (a,b), (a), () groupings.

**ROW_NUMBER()** — Window function. Unique rank — no ties: 1, 2, 3, 4.
Most commonly used window function.

---

## S

**SCD Type 2** — Slowly Changing Dimension Type 2. Keeps full history by adding
new rows with date ranges. Current row has valid_to = NULL.
→ *Demonstrated in:* `04_de_patterns/01_de_patterns.py`

**Schema** — Namespace within a database. Groups related tables.
Like a folder for database objects.

**Seq Scan** — Sequential scan. Reads every row in the table. Slow for large
tables. The optimizer chooses this when no useful index exists.

**Subquery** — Query nested inside another query. Can be correlated (references
outer query) or uncorrelated (independent).
→ *Demonstrated in:* `01_sql_core/03_subqueries.py`

---

## T

**Transaction** — A unit of work that is atomic, consistent, isolated, and durable.
`BEGIN ... COMMIT` or `BEGIN ... ROLLBACK`.
→ *Demonstrated in:* `06_transactions_and_concurrency/01_transactions.py`

**TRUNCATE** — Removes all rows from a table instantly. Faster than DELETE.
Can be rolled back within a transaction.

---

## U

**Unique constraint** — Ensures no duplicate values in a column.
Different from PK: allows NULL, multiple per table.

**Upsert** — Insert or update in one atomic operation.
PostgreSQL: `INSERT ... ON CONFLICT DO UPDATE`.

---

## V

**VACUUM** — Reclaims space from dead rows (updated/deleted but kept for MVCC).
Without VACUUM, tables grow indefinitely. `VACUUM FULL` reclaims space to OS
but requires an exclusive lock.

---

## W

**Window Function** — Computes across a set of rows without collapsing them.
`function() OVER (PARTITION BY ... ORDER BY ... frame)`.
→ *Demonstrated in:* `02_cte_and_windowing/02_window_functions.py`

**Write-Ahead Log (WAL)** — PostgreSQL's durability mechanism. Changes are
written to the WAL before data files. If the server crashes, the WAL is
replayed to recover committed transactions.

---

Last updated: 2026-04-02
