# Interview Questions — SQL for Data Engineering

> Topics covered: window functions · QUALIFY · merge/upsert · recursive CTEs · pivot/unpivot · JSON/array functions · dynamic SQL
> Levels: Starter | Mid | Senior | Architect

---

## Window Functions

### Level 1 — Starter

**Q1: In c098_window_functions_demo.py, the demo contrasts `group_by_total` with window-style calculations. What is the fundamental difference between GROUP BY and a window function?**
What a good answer covers:
- GROUP BY collapses rows into one row per group; window functions return one row per original row
- Window functions compute across a "window" of related rows without reducing the result set
- Aggregates can be used in both, but only window functions let you keep all detail rows alongside the aggregate
Why this is asked: tests whether the candidate understands the row-collapsing behavior that is the most common source of confusion when learning window functions.

**Q2: Using the customer transaction data in c098_window_functions_demo.py (Ava, Ben, Cara with amounts and dates), write a query that assigns each transaction a sequential row number within each customer, ordered by date.**
What a good answer covers:
- `ROW_NUMBER() OVER (PARTITION BY customer ORDER BY date)`
- Explains that PARTITION BY is the window equivalent of GROUP BY
- Notes that ties in ORDER BY can produce non-deterministic results without a tiebreaker
Why this is asked: ROW_NUMBER with PARTITION BY is the single most common window function question in DE interviews.

**Q3: What does the ORDER BY clause inside an OVER() clause control, and how does it differ from the ORDER BY at the end of a SELECT statement?**
What a good answer covers:
- ORDER BY inside OVER controls the ordering of rows within each partition for the window computation
- The final ORDER BY controls the order of the result set returned to the caller
- They are independent; you can window-order by date and return results ordered by customer
Why this is asked: candidates often conflate the two and this reveals whether they have actually written window queries.

**Q4: What is the difference between RANK(), DENSE_RANK(), and ROW_NUMBER()?**
What a good answer covers:
- ROW_NUMBER gives a unique sequential integer regardless of ties
- RANK skips numbers after ties (1, 2, 2, 4)
- DENSE_RANK does not skip numbers after ties (1, 2, 2, 3)
- Which to use depends on whether gaps in ranking are acceptable downstream
Why this is asked: a fast litmus test for familiarity with the window function family.

### Level 2 — Mid

**Q1: Given the customer transaction data in c098_window_functions_demo.py, write a query that computes the running total of `amount` for each customer ordered by date, and explain what frame specification controls it.**
What a good answer covers:
- `SUM(amount) OVER (PARTITION BY customer ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`
- The default frame when ORDER BY is present is RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW, which can behave unexpectedly with ties
- ROWS BETWEEN is usually safer for running totals because it counts physical rows
Why this is asked: frame specification is where most mid-level candidates have gaps.

**Q2: Write a query against the demo data that returns the previous transaction amount for each customer (i.e., the amount of the immediately preceding row ordered by date).**
What a good answer covers:
- `LAG(amount, 1) OVER (PARTITION BY customer ORDER BY date)`
- LAG returns NULL for the first row in each partition; a default value can be supplied as a third argument
- LEAD is the forward-looking equivalent
Why this is asked: LAG/LEAD are workhorses in event analysis and pipeline QA.

**Q3: How would you find the single highest-amount transaction per customer using a window function, without using a subquery or CTE?**
What a good answer covers:
- `FIRST_VALUE(amount) OVER (PARTITION BY customer ORDER BY amount DESC)` or `MAX(amount) OVER (PARTITION BY customer)`
- Distinguishes between FIRST_VALUE (needs explicit frame) and MAX as a window aggregate
- Notes QUALIFY (covered in c099) as an alternative for filtering to just those rows
Why this is asked: bridges window functions to filtering, which leads naturally to QUALIFY.

**Q4: What is the performance implication of using many window functions with different PARTITION BY or ORDER BY clauses in a single query?**
What a good answer covers:
- Each distinct window specification may require a separate sort pass over the data
- Grouping compatible windows together or using named WINDOW clauses can reduce passes
- Some engines (BigQuery, Snowflake) optimize compatible windows; others do not
Why this is asked: DE candidates must think about query cost, not just correctness.

### Level 3 — Senior

**Q1: A pipeline ingests the transaction data from c098_window_functions_demo.py daily. A late-arriving record arrives after the daily run closes. How does this affect running totals computed with window functions, and what patterns mitigate it?**
What a good answer covers:
- Running totals already written to a target table are stale; you cannot easily patch one row
- Options: recompute the entire partition, use an incremental merge that recomputes only affected partitions, or use a snapshot approach
- Event-time vs. processing-time distinction; idempotent recomputation is usually safest
Why this is asked: window functions in production must handle late data — a purely academic understanding breaks here.

**Q2: Explain how you would implement a 7-day rolling average in a warehouse where the data has gaps (some days have no transactions for a customer).**
What a good answer covers:
- A simple ROWS BETWEEN 6 PRECEDING AND CURRENT ROW counts physical rows, not calendar days, which gives wrong results with gaps
- Solution: generate a spine of all dates for each customer (cross join or calendar table) and then apply the window function
- Alternative: RANGE BETWEEN INTERVAL 6 DAY PRECEDING AND CURRENT ROW if the engine supports date-based range frames (BigQuery, DuckDB)
Why this is asked: reveals whether the candidate understands the difference between logical and physical window frames in real data.

**Q3: A colleague proposes computing percentile ranks by nesting window functions: `RANK() OVER (...) / COUNT(*) OVER (...)`. What are the risks and what is the idiomatic alternative?**
What a good answer covers:
- Division of integers may truncate in some SQL dialects; requires explicit casting
- PERCENT_RANK() and CUME_DIST() are the idiomatic built-ins and avoid the division pitfall
- NTILE(n) is appropriate when bucketing into equal-sized groups is the goal
Why this is asked: tests knowledge of the full window function family and awareness of type-casting traps.

### Level 4 — Architect

**Q1: Your team is building a real-time leaderboard that requires window-function-style ranked results refreshed every 30 seconds. The source data lives in Kafka (see c001_kafka_concepts_demo.py in the streaming track). Walk through the architectural options and trade-offs.**
What a good answer covers:
- Batch SQL window functions on a warehouse are too slow for 30-second SLAs
- Streaming SQL engines (Flink, Spark Structured Streaming, ksqlDB) support window functions over event-time windows
- Stateful aggregation in a stream processor replaces PARTITION BY; late-data handling requires watermarks
- Results can be materialized to a serving layer (Redis, Postgres) and the warehouse is updated asynchronously for historical accuracy
Why this is asked: connects SQL semantics to streaming architecture, the defining challenge for senior DE architects.

**Q2: In a medallion lakehouse (Bronze → Silver → Gold), at which layer do window functions typically belong, and what governance concerns arise when window function results are persisted as Gold-layer facts?**
What a good answer covers:
- Window functions typically execute at the Silver-to-Gold boundary where business logic is applied
- Persisted window results (running totals, rankings) become derived facts; any change to partitioning logic or source data invalidates them
- Lineage tooling must track that a Gold column is a window aggregate, not a raw value, to avoid double-aggregation downstream
- Time-travel / versioning of Gold tables is essential so stakeholders can reproduce historical rankings
Why this is asked: forces the candidate to think about data governance, not just query authoring.

---

## QUALIFY

### Level 1 — Starter

**Q1: The story comment in c099_qualify_demo.py says "QUALIFY filters rows after window functions are computed." What problem does this solve that WHERE cannot?**
What a good answer covers:
- WHERE is evaluated before window functions, so you cannot filter on a window function result in the WHERE clause
- QUALIFY is evaluated after the window computation, allowing predicates like `QUALIFY ROW_NUMBER() OVER (...) = 1`
- Without QUALIFY you need a subquery or CTE to wrap the window and then filter
Why this is asked: the order-of-SQL-clause-execution is fundamental knowledge for DE roles.

**Q2: Rewrite this two-step query as a single statement using QUALIFY: first compute ROW_NUMBER() OVER (PARTITION BY customer ORDER BY date DESC) as rn, then select only rows where rn = 1 from the data in c099_qualify_demo.py.**
What a good answer covers:
- `SELECT * FROM transactions QUALIFY ROW_NUMBER() OVER (PARTITION BY customer ORDER BY date DESC) = 1`
- QUALIFY eliminates the need for a subquery or CTE wrapper
- Supported in Snowflake, BigQuery, DuckDB, Teradata; not in standard PostgreSQL or MySQL as of 2025
Why this is asked: demonstrates practical knowledge of a modern SQL feature that reduces query complexity.

**Q3: Which SQL engines support QUALIFY natively, and what is the equivalent pattern in engines that do not?**
What a good answer covers:
- Native support: Snowflake, BigQuery, DuckDB, Teradata
- Engines without native support: PostgreSQL, MySQL, SQL Server (as of 2025)
- Equivalent pattern: wrap the window in a subquery or CTE, then filter with WHERE on the aliased column
Why this is asked: DE engineers work across multiple engines and must know portability boundaries.

**Q4: Using the Ava/Ben/Cara data in c099_qualify_demo.py, write a QUALIFY statement that returns the two most recent transactions per customer.**
What a good answer covers:
- `QUALIFY ROW_NUMBER() OVER (PARTITION BY customer ORDER BY date DESC) <= 2`
- Can use RANK instead if ties should both be included
- Notes that sorting on date alone may be non-deterministic if two dates are equal; add a secondary sort key
Why this is asked: slight variation from rn=1 to rn<=N tests whether the candidate understands the general pattern.

### Level 2 — Mid

**Q1: What is the difference between using QUALIFY with ROW_NUMBER versus RANK for deduplication? When would each produce different results?**
What a good answer covers:
- ROW_NUMBER always produces unique integers; QUALIFY ROW_NUMBER() = 1 returns exactly one row per partition
- RANK assigns the same rank to tied rows; QUALIFY RANK() = 1 may return multiple rows if there are ties at the top
- For true deduplication use ROW_NUMBER; for "all rows tied for best" use RANK or DENSE_RANK
Why this is asked: deduplication is one of the most common QUALIFY use cases and ties are a frequent edge case.

**Q2: Can you use QUALIFY with aggregate window functions like SUM or AVG? Give an example using the transaction data.**
What a good answer covers:
- Yes: `QUALIFY SUM(amount) OVER (PARTITION BY customer) > 200` returns only rows for customers whose total exceeds 200
- This is more readable than a subquery that computes aggregates and joins back
- Useful for filtering on partition-level aggregates while retaining row-level detail
Why this is asked: candidates who only know QUALIFY for ranking miss half its utility.

**Q3: How does QUALIFY interact with WHERE and HAVING in the SQL logical order of execution?**
What a good answer covers:
- Logical order: FROM → WHERE → GROUP BY → HAVING → SELECT (including window computation) → QUALIFY → ORDER BY → LIMIT
- WHERE filters raw rows before any aggregation or windowing
- HAVING filters grouped rows after GROUP BY
- QUALIFY filters after window functions; it sees the post-SELECT window results
Why this is asked: understanding execution order prevents subtle bugs when combining QUALIFY with other clauses.

**Q4: A table has duplicate customer records and you need to keep the latest record per customer using QUALIFY. What column choices for ORDER BY matter, and what happens if dates are equal?**
What a good answer covers:
- Primary sort: `ORDER BY updated_at DESC` or `ORDER BY date DESC`
- If dates can be equal, add a surrogate tiebreaker: a monotonically increasing id, a checksum, or an ingestion timestamp
- Without a tiebreaker, ROW_NUMBER is non-deterministic among tied rows — the "latest" record is arbitrary
- In practice, use the record's natural primary key or sequence as a secondary sort
Why this is asked: deduplication failures due to ties are a real production bug class.

### Level 3 — Senior

**Q1: You need to implement "keep the latest version of each record" deduplication in a streaming pipeline that uses micro-batches. How does QUALIFY in a batch SQL context relate to stateful deduplication in a streaming engine?**
What a good answer covers:
- Batch QUALIFY is a full-partition scan; it sees all historical data and picks the winner deterministically
- Streaming deduplication must maintain state (last-seen key → value) across micro-batches with a TTL
- The SQL expression `QUALIFY ROW_NUMBER() OVER (PARTITION BY key ORDER BY event_time DESC) = 1` maps conceptually to the streaming state store keeping only the latest event per key
- Late data handling differs: batch QUALIFY reprocesses; streaming needs watermarks or explicit reprocessing triggers
Why this is asked: connects SQL semantics to streaming architecture, a key competency for senior DEs.

**Q2: A Gold-layer table is built by running a QUALIFY-based deduplication daily. Stakeholders discover that for one customer, the "latest" record flipped between two runs even though no new data arrived. What are the likely causes and how do you fix them?**
What a good answer covers:
- Non-deterministic tie-breaking: two rows share the same sort key, so the engine picks arbitrarily
- Partition pruning or parallelism changes between runs can alter row ordering within a tie
- Fix: add a stable secondary sort key (row hash, insertion sequence) so the result is deterministic
- Longer term: enforce uniqueness constraints upstream so deduplication is never needed
Why this is asked: production-grade data quality requires deterministic deduplication.

**Q3: How would you unit-test a QUALIFY-based deduplication query to ensure it handles ties, NULL sort keys, and single-row partitions correctly?**
What a good answer covers:
- Build a test dataset that explicitly covers each edge case: tied dates, NULL dates, partitions with one row, partitions with many rows
- Use dbt tests or a pytest-based SQL test framework to run the query against the fixture and assert exact output
- NULL sort key behavior varies by engine (NULLS FIRST vs NULLS LAST) — test both orderings
- Snapshot the expected output so regressions are caught on engine upgrades
Why this is asked: senior DEs are expected to own the quality of their transformations, not just write them.

### Level 4 — Architect

**Q1: Your CDC pipeline (see c003_cdc_demo.py in the streaming track) streams INSERT, UPDATE, and DELETE events into a landing table. You want to use QUALIFY to reconstruct the current state of each record. Design the query and identify the failure modes.**
What a good answer covers:
- Assign ROW_NUMBER partitioned by primary key, ordered by CDC sequence number descending; QUALIFY = 1 gives the latest event per key
- DELETE events must be handled explicitly: after QUALIFY, filter out rows where op = 'DELETE'
- Out-of-order delivery from the CDC stream means sequence numbers may not reflect true order; use event timestamps as a secondary sort
- Compaction: periodically compact the landing table so QUALIFY scans do not grow unbounded
Why this is asked: directly connects SQL (QUALIFY) to CDC streaming architecture, the canonical DE integration challenge.

**Q2: Compare the trade-offs of using QUALIFY for deduplication versus MERGE statements (c100) for upsert-based deduplication in a lakehouse context.**
What a good answer covers:
- QUALIFY is read-time deduplication: fast to implement, but the table still stores duplicates; query cost grows with table size
- MERGE is write-time deduplication: the table is kept clean, query cost is stable, but MERGE has higher write amplification and locking costs
- QUALIFY is better for exploratory or infrequently queried data; MERGE is better for frequently queried Gold-layer tables
- In Delta Lake / Iceberg, MERGE triggers file rewrites; QUALIFY on a large partitioned table can be cheaper if queries are rare
Why this is asked: architects must choose the right deduplication strategy based on query patterns and cost, not just correctness.

---

## Merge / Upsert

### Level 1 — Starter

**Q1: What is the purpose of a MERGE statement, and what three operations can it perform in a single pass?**
What a good answer covers:
- MERGE synchronizes a target table with a source dataset in one atomic operation
- The three clauses are: WHEN MATCHED (update or delete), WHEN NOT MATCHED BY TARGET (insert), WHEN NOT MATCHED BY SOURCE (delete or update)
- A traditional ETL alternative would be separate DELETE + INSERT or UPDATE + INSERT steps, which are not atomic
Why this is asked: MERGE is foundational for upsert patterns in data warehousing.

**Q2: Write a MERGE statement that upserts customer transaction records: update the amount if the customer and date already exist, otherwise insert a new row.**
What a good answer covers:
- `MERGE target USING source ON target.customer = source.customer AND target.date = source.date WHEN MATCHED THEN UPDATE SET amount = source.amount WHEN NOT MATCHED THEN INSERT (customer, date, amount) VALUES (source.customer, source.date, source.amount)`
- The ON clause is the join key; its correctness determines whether rows are matched
- INSERT must list all non-nullable columns
Why this is asked: every DE candidate should be able to write a basic MERGE from memory.

**Q3: What happens if the source dataset in a MERGE has duplicate rows matching the same target row?**
What a good answer covers:
- Most engines (SQL Server, Snowflake, BigQuery) raise a runtime error when a single target row is matched more than once
- The source must be deduplicated before being used in MERGE — typically with a CTE using QUALIFY or ROW_NUMBER
- This is a common production bug when MERGE sources are not pre-cleaned
Why this is asked: the duplicate-source problem is the most common MERGE pitfall and breaks pipelines silently in some engines.

**Q4: What is the difference between UPSERT and MERGE?**
What a good answer covers:
- UPSERT is a general term for "insert or update if exists"; MERGE is the SQL standard syntax to implement it
- Some engines provide shorthand upsert syntax (INSERT ... ON CONFLICT in PostgreSQL, INSERT OVERWRITE in Hive) that are simpler but less flexible
- MERGE can also handle deletes in the same statement, making it more powerful than a simple upsert
Why this is asked: terminology clarity is expected at the junior level.

### Level 2 — Mid

**Q1: How do you handle soft deletes in a MERGE pattern — records that exist in the target but are absent from the source and should be flagged as deleted rather than physically removed?**
What a good answer covers:
- Use `WHEN NOT MATCHED BY SOURCE THEN UPDATE SET is_deleted = TRUE, deleted_at = CURRENT_TIMESTAMP`
- This requires including the `WHEN NOT MATCHED BY SOURCE` clause, which is not supported in all engines (BigQuery requires a workaround)
- Soft-deleted rows remain queryable for audit; physical DELETE removes the audit trail
Why this is asked: soft deletes are standard in regulated industries and many candidates miss the BY SOURCE clause.

**Q2: Explain the difference between SCD Type 1 and SCD Type 2, and how MERGE is used to implement each.**
What a good answer covers:
- SCD Type 1: overwrite old values; implemented with a standard WHEN MATCHED THEN UPDATE
- SCD Type 2: keep history by closing the old row (set end_date, is_current = FALSE) and inserting a new row; requires MERGE plus an INSERT or a two-step process
- SCD Type 2 is harder because a single MERGE cannot easily both update and insert for the same matched key
- Common pattern: MERGE for closing old rows, then INSERT for new versions
Why this is asked: SCDs are a core data warehousing concept tested heavily in DE interviews.

**Q3: What locking and concurrency implications does MERGE have in a transactional database versus a columnar warehouse like Snowflake or BigQuery?**
What a good answer covers:
- In transactional databases, MERGE acquires row-level or page-level locks; concurrent writes can cause deadlocks
- In Snowflake, MERGE is atomic but locks the entire target table for the duration; parallel MERGEs on the same table serialize
- BigQuery MERGE uses optimistic concurrency on table metadata; conflicts cause the statement to fail and retry
- In lakehouses (Delta, Iceberg), MERGE rewrites affected files; file-level optimistic concurrency is used
Why this is asked: understanding concurrency is required for designing reliable high-frequency upsert pipelines.

**Q4: How would you test that a MERGE statement is idempotent — that running it twice on the same source produces the same target state?**
What a good answer covers:
- Run the MERGE once, snapshot the target, run the MERGE again with the same source, compare snapshots — they must be identical
- For idempotency to hold, WHEN MATCHED must be a pure SET (no increment-style expressions like `count = count + 1`)
- Use a unit test framework (dbt, pytest-dbt, or custom SQL harness) with deterministic fixture data
- Idempotency is critical for retry-safe pipelines; a non-idempotent MERGE will corrupt data on reruns
Why this is asked: pipeline idempotency is a senior expectation even at the mid level for DE roles.

### Level 3 — Senior

**Q1: You are merging 10 million CDC events per day (INSERT/UPDATE/DELETE) into a 500 million row Gold table in Snowflake. Walk through your MERGE strategy for performance and cost.**
What a good answer covers:
- Pre-aggregate the source: deduplicate to one event per key using QUALIFY before the MERGE
- Cluster the target table on the join key columns to minimize micro-partition scans
- Consider splitting MERGE into separate UPDATE and INSERT passes if the UPDATE path is rare (avoids full table scan for matched rows)
- Monitor credits consumed per MERGE; evaluate whether micro-batch MERGEs are cheaper than one large daily MERGE
- Use transient staging tables for the source to avoid Fail-safe costs
Why this is asked: real-world MERGE at scale requires cost-aware design, not just correct SQL.

**Q2: Delta Lake and Apache Iceberg both support MERGE. What are the key differences in how each table format handles the file rewrites triggered by a MERGE?**
What a good answer covers:
- Delta Lake: MERGE identifies affected files via the transaction log, rewrites only those files, adds new files, and writes a new commit entry; uses optimistic concurrency
- Iceberg: similar file-level approach but uses snapshot isolation with a metadata tree; concurrent writers can proceed in parallel and conflicts are resolved at commit time
- Both formats support time travel via the transaction log / snapshot history
- File compaction (OPTIMIZE / REWRITE DATA FILES) is needed after many small MERGEs to prevent read amplification
Why this is asked: open table format knowledge is now expected for senior DE roles.

**Q3: A MERGE pipeline fails halfway through. How do each of the following handle partial failure: (a) a transactional RDBMS, (b) Snowflake, (c) Delta Lake?**
What a good answer covers:
- (a) RDBMS: MERGE is wrapped in a transaction; partial failure triggers automatic rollback, leaving the target unchanged
- (b) Snowflake: MERGE is atomic by design; it either commits fully or rolls back, no partial state
- (c) Delta Lake: a failed MERGE does not commit to the transaction log; the target table is unchanged, but orphan data files may be written and require VACUUM to clean up
- All three support retry-safe reruns when idempotent; only Delta requires explicit file cleanup after failure
Why this is asked: failure handling reveals whether the candidate understands atomicity guarantees across platforms.

### Level 4 — Architect

**Q1: Design a CDC-to-Gold merge pipeline (connecting c003_cdc_demo.py) that handles out-of-order events, exactly-once semantics, and schema evolution without downtime.**
What a good answer covers:
- Land CDC events in a Bronze table with the full event envelope (seq, op, before, after, schema version)
- Silver layer: deduplicate and order by sequence number using QUALIFY; apply schema mapping per version
- Gold layer: MERGE from Silver using the business key; DELETE events set is_deleted flag
- Out-of-order: use a reprocessing window (last N hours) rather than trusting arrival order
- Exactly-once: track the last processed CDC sequence in a watermark table; idempotent MERGE ensures reruns are safe
- Schema evolution: use a schema registry; Silver handles field addition gracefully with NULL defaults
Why this is asked: end-to-end CDC pipeline design is the canonical senior/architect DE interview question.

**Q2: Your organization is moving from a nightly full-load ETL to a continuous MERGE-based pipeline. What organizational and architectural risks must you address beyond the technical SQL changes?**
What a good answer covers:
- Data consumers expect a daily "fresh" snapshot; continuous updates change SLA communication
- Monitoring shifts from job success/failure to data freshness and lag metrics
- Cost model changes: continuous small MERGEs may cost more than one large nightly batch on some platforms
- Schema change governance becomes harder — a full-load can absorb schema changes at load time; MERGE pipelines require coordinated schema migrations
- Rollback strategy: full-load can reload from source; MERGE pipelines need time-travel or a parallel shadow table for rollback
Why this is asked: architecture decisions have organizational and operational dimensions that pure SQL knowledge does not cover.

---

## Recursive CTEs

### Level 1 — Starter

**Q1: What is a recursive CTE and what type of data structure is it typically used to query?**
What a good answer covers:
- A recursive CTE is a CTE that references itself, allowing iterative query execution
- It is used to query hierarchical or graph-structured data: org charts, category trees, bill of materials, network paths
- Standard SQL requires the RECURSIVE keyword; some engines (Snowflake, BigQuery) use WITH RECURSIVE
Why this is asked: establishes baseline knowledge before probing depth.

**Q2: A recursive CTE has two parts: the anchor member and the recursive member. What does each part do?**
What a good answer covers:
- Anchor member: the base case — returns the starting rows (e.g., root nodes of a tree)
- Recursive member: references the CTE itself and joins to expand one level at a time
- The two parts are combined with UNION ALL; the engine iterates until the recursive member returns no rows
- UNION (without ALL) is sometimes used to prevent infinite loops but is much slower
Why this is asked: candidates who cannot name the two parts have likely never written a recursive CTE.

**Q3: Write a recursive CTE that traverses an employee hierarchy, starting from a given manager ID and returning all direct and indirect reports.**
What a good answer covers:
- Anchor: `SELECT id, name, manager_id FROM employees WHERE id = :root_id`
- Recursive: `SELECT e.id, e.name, e.manager_id FROM employees e JOIN cte ON e.manager_id = cte.id`
- Add a `depth` column in each member to track the level in the hierarchy
- Include a cycle guard (depth limit or visited-set check) to handle data with circular references
Why this is asked: the employee hierarchy is the canonical recursive CTE example and every DE should be able to write it.

**Q4: What happens if a recursive CTE has a cycle in the data (an employee who is their own manager transitively)?**
What a good answer covers:
- The CTE will loop infinitely unless a termination condition is added
- Most engines have a default recursion depth limit (e.g., Snowflake: 100 iterations) that raises an error
- Mitigation: add a `depth <= N` condition in the WHERE clause, or track visited IDs using an array (supported in PostgreSQL)
- Data quality checks upstream are the real fix — circular references indicate bad data
Why this is asked: infinite loops from cycles are a real production failure mode.

### Level 2 — Mid

**Q1: How would you use a recursive CTE to generate a date spine — a sequence of consecutive dates between two bounds?**
What a good answer covers:
- Anchor: `SELECT CAST('2024-01-01' AS DATE) AS dt`
- Recursive: `SELECT DATEADD(day, 1, dt) FROM date_spine WHERE dt < '2024-12-31'`
- Date spines are used to fill gaps in time-series data before applying window functions
- Some engines (BigQuery, DuckDB) have built-in `GENERATE_DATE_ARRAY` or `GENERATE_SERIES` that are faster alternatives
Why this is asked: date spine generation is a practical everyday DE task.

**Q2: Compare the performance of a recursive CTE versus a pre-built calendar table for date spine operations in a large warehouse.**
What a good answer covers:
- Recursive CTE generates rows at query time; for short ranges it is negligible, but it serializes and cannot be parallelized
- A pre-built calendar table is a simple scan that the query optimizer can join efficiently and push predicates into
- For daily ETL jobs that join to dates millions of times, a calendar table is significantly faster
- Calendar tables also store fiscal calendars, holidays, and business-day flags that a recursive CTE cannot
Why this is asked: practical performance awareness separates mid from junior candidates.

**Q3: Explain how to compute the full path from root to leaf for each node in a tree using a recursive CTE.**
What a good answer covers:
- Maintain a `path` string column in the CTE, concatenating node identifiers at each level: `path || '/' || id`
- The anchor initializes path to the root node's identifier
- The recursive member appends the child's identifier to the parent's path
- String concatenation is engine-specific; some engines support array accumulation instead
Why this is asked: path computation is a common requirement for taxonomy and category systems.

**Q4: What is the maximum recursion depth in Snowflake, BigQuery, and PostgreSQL, and how do you handle data that exceeds it?**
What a good answer covers:
- Snowflake: 100 iterations by default, configurable per session
- BigQuery: no explicit recursion limit documented, but query timeout applies
- PostgreSQL: configurable via `max_recursion_depth` parameter (default often 100)
- Handling deep hierarchies: flatten the hierarchy into a closure table at load time; recursive CTEs are then replaced by simple range queries on the closure table
Why this is asked: production hierarchies can be deep; knowing the limits and workarounds is a senior signal even at the mid level.

### Level 3 — Senior

**Q1: A product category tree has 8 levels and 200,000 nodes. Queries that traverse the full tree with a recursive CTE are timing out. Propose two alternative modeling strategies.**
What a good answer covers:
- Closure table: store all ancestor-descendant pairs with their path length; queries become a simple join with no recursion
- Nested sets (modified preorder tree traversal): assign left/right bounds to each node; subtree queries become a range scan
- Both approaches trade write complexity (maintaining the structure on updates) for read performance
- Materialized path (storing the full path string per row) is a third option, useful for prefix-based queries
Why this is asked: tree query performance is a real problem that forces candidates to think beyond the naive recursive CTE.

**Q2: You need to detect cycles in a directed graph stored in a SQL table. How would you use a recursive CTE to do this, and what are the limitations?**
What a good answer covers:
- Track visited node IDs in an array column; at each step, check if the current node is already in the array
- If the current node is in the visited array, a cycle is detected; emit the cycle path
- PostgreSQL supports array accumulation in recursive CTEs; Snowflake and BigQuery have more limited support
- For large graphs this approach is memory-intensive; graph databases or Spark GraphX are more appropriate at scale
Why this is asked: graph traversal reveals deep understanding of recursive CTE mechanics and their limits.

**Q3: How do recursive CTEs relate to iterative procedural code, and when should you replace a recursive CTE with a stored procedure or scripting layer?**
What a good answer covers:
- Recursive CTEs are declarative iterations; the engine controls the loop
- Stored procedures or scripting (Python, dbt macros) offer more control: conditional branching, early exit, logging per iteration
- Replace with procedural code when: the number of iterations is data-driven and unpredictable, when you need per-iteration side effects (logging, alerts), or when the recursive CTE exceeds engine limits
- In dbt, recursive CTEs are often replaced with ref-chained models that materialize each level
Why this is asked: knowing when not to use a feature is a senior competency.

### Level 4 — Architect

**Q1: Your data model uses recursive CTEs to compute real-time org chart rollups for 50,000 employees. The query runs on every dashboard load. Design a caching and precomputation strategy that connects to your orchestration layer.**
What a good answer covers:
- Precompute the closure table nightly (or on HR system change events via CDC) using a recursive CTE run by the orchestrator (Airflow, Prefect)
- Store the result in a materialized table; dashboards query the materialized table, not the recursive CTE
- Invalidate the materialized table on HR change events using a webhook or CDC trigger (connecting to c003_cdc_demo.py patterns)
- For very large orgs, partition the closure table by root department to allow partial invalidation
Why this is asked: connects recursive SQL to orchestration and CDC — a cross-track architectural question.

**Q2: Compare recursive CTEs in SQL with graph traversal in a dedicated graph database (Neo4j, Amazon Neptune). When does the complexity of a data product justify migrating from SQL to a graph database?**
What a good answer covers:
- Recursive CTEs work well for shallow, well-structured hierarchies but degrade on multi-hop, variable-depth graph traversals
- Graph databases use index-free adjacency; traversal cost is proportional to the number of hops, not the size of the graph
- Migration is justified when: queries regularly traverse more than 3-4 hops, when relationship properties are as important as node properties, or when the graph structure changes frequently
- Migration cost: data pipeline complexity increases, SQL tooling is lost, BI tools may not connect natively
Why this is asked: architects must know when to use the right data store for the problem, not fit every problem into SQL.

---

## Pivot / Unpivot

### Level 1 — Starter

**Q1: What does PIVOT do to a table, and what is a simple use case for it in a data engineering context?**
What a good answer covers:
- PIVOT rotates rows into columns, turning distinct values of one column into column headers
- Common use cases: turning monthly sales rows into one column per month, cross-tabulating metrics by category
- The result is a wider table with fewer rows and more columns
Why this is asked: establishes the mental model before testing implementation knowledge.

**Q2: What does UNPIVOT do, and why might raw data arrive in a pivoted (wide) format that needs to be unpivoted?**
What a good answer covers:
- UNPIVOT rotates columns into rows, turning column headers into values in a column
- Raw data from spreadsheets, legacy systems, or reporting exports often arrives wide; UNPIVOT normalizes it for analysis
- Normalized (long) format is easier to filter, aggregate, and join in SQL
Why this is asked: data engineers frequently receive wide data that must be normalized.

**Q3: Write a query that pivots the following data — customer, month, amount — so each month becomes a column and each row represents one customer.**
What a good answer covers:
- Engines with native PIVOT syntax (SQL Server, Snowflake): `SELECT * FROM (SELECT customer, month, amount FROM t) PIVOT (SUM(amount) FOR month IN ('Jan', 'Feb', 'Mar'))`
- Engines without native PIVOT (BigQuery, PostgreSQL): use conditional aggregation — `SUM(CASE WHEN month = 'Jan' THEN amount END) AS Jan`
- The month values must be known at query-write time for static PIVOT; dynamic PIVOT requires dynamic SQL
Why this is asked: tests both native syntax knowledge and the portable conditional-aggregation alternative.

**Q4: What is conditional aggregation, and how does it relate to PIVOT?**
What a good answer covers:
- Conditional aggregation uses `SUM(CASE WHEN col = value THEN metric END)` inside a GROUP BY to produce one column per value
- It is functionally equivalent to PIVOT but works in all SQL engines
- It is more verbose but more explicit and portable
Why this is asked: conditional aggregation is the universal fallback for PIVOT and every DE should know it.

### Level 2 — Mid

**Q1: How do you implement a dynamic PIVOT — one where the column names are not known until runtime — in SQL?**
What a good answer covers:
- Build the column list dynamically by first querying the distinct values of the pivot column
- Construct the PIVOT or conditional aggregation SQL as a string using dynamic SQL techniques (stored procedures, scripting, dbt macros)
- Execute the constructed string with EXECUTE or equivalent
- Risk: SQL injection if the pivot column values come from user input; sanitize or whitelist values
Why this is asked: static PIVOT is trivial; dynamic PIVOT is where production complexity lives.

**Q2: You receive a wide dataset with 50 metric columns (metric_1 through metric_50). Write the approach (not necessarily every line) for unpivoting all 50 columns into two columns: metric_name and metric_value.**
What a good answer covers:
- Native UNPIVOT: list all 50 columns in the UNPIVOT clause — verbose but correct
- Dynamic UNPIVOT: generate the column list from INFORMATION_SCHEMA and construct the SQL dynamically
- Modern alternative: DuckDB `UNPIVOT` with wildcard; BigQuery `UNPIVOT`; Snowflake `UNPIVOT`
- Pandas/PySpark `melt` function is often faster to write for wide datasets in a Python pipeline
Why this is asked: 50-column UNPIVOT forces the candidate to think beyond the textbook example.

**Q3: After unpivoting, how do you handle NULL metric values — should they be kept or dropped, and what downstream impact does each choice have?**
What a good answer covers:
- NULLs may represent "not applicable" (keep) or "not recorded" (may want to drop or impute)
- Keeping NULLs: downstream aggregations must use `SUM(CASE WHEN value IS NOT NULL THEN value END)` or `COUNT(value)` to avoid inflating counts
- Dropping NULLs: reduces table size but loses the signal that a metric was expected but absent
- Document the NULL policy in the data contract for the table
Why this is asked: NULL handling after UNPIVOT is a common source of downstream aggregation bugs.

**Q4: A reporting table is pivoted with months as columns. A new month arrives each month, requiring a schema change. What is a better long-term design?**
What a good answer covers:
- Store data in unpivoted (long) format as the canonical table; pivot dynamically at the reporting layer
- Use a BI tool or reporting view that applies conditional aggregation, refreshed without schema changes
- If consumers need wide format, generate the pivoted view on a schedule via dynamic SQL
- This avoids DDL changes (ALTER TABLE ADD COLUMN) for each new month, which can be disruptive at scale
Why this is asked: schema-on-write wide tables are an antipattern that many candidates have inherited and should know how to fix.

### Level 3 — Senior

**Q1: A pivot query produces different results when the underlying data has duplicate (customer, month) combinations. Explain why and how to prevent it.**
What a good answer covers:
- If there are multiple rows for the same (customer, month), the aggregate function in the PIVOT determines which value "wins"
- SUM will add them; MAX/MIN will pick one; COUNT will overcount
- The correct fix is to deduplicate before pivoting (using QUALIFY or a CTE) or to use the intended aggregate explicitly
- Silent data issues from unexpected duplicates are a production risk; add a pre-pivot count assertion
Why this is asked: pivot correctness depends on understanding the aggregation semantics and data quality.

**Q2: How do PIVOT and UNPIVOT relate to the ELT pattern for ingesting wide flat files from source systems?**
What a good answer covers:
- Many source systems export wide flat files (one row per entity, many attribute columns)
- ELT lands the file as-is in Bronze; UNPIVOT in Silver normalizes it to the entity-attribute-value model
- This makes downstream transformations engine-agnostic and schema-change-resilient
- The trade-off: entity-attribute-value tables are harder to query (require pivoting back at the Gold layer) but easier to extend
Why this is asked: connects PIVOT/UNPIVOT to the ELT medallion architecture.

**Q3: Compare the performance of native PIVOT syntax versus conditional aggregation for a 100-million-row table with 12 pivot columns in Snowflake.**
What a good answer covers:
- Native PIVOT and conditional aggregation compile to essentially the same execution plan in Snowflake
- Performance is dominated by the GROUP BY scan and the number of partitions pruned, not the PIVOT syntax
- More pivot columns increase memory pressure; very wide pivots (100+ columns) may spill to disk
- Clustering the table on the GROUP BY keys (customer, date) reduces the scan cost regardless of PIVOT method
Why this is asked: candidates should understand that syntax sugar does not change the execution plan.

### Level 4 — Architect

**Q1: Design a self-service reporting system where business users can dynamically pivot any metric by any dimension without DE involvement, while maintaining query governance and cost controls.**
What a good answer covers:
- Expose a semantic layer (dbt metrics, LookML, Cube.js) that encodes valid metrics and dimensions; users select combinations via a BI tool
- The semantic layer generates the conditional aggregation SQL dynamically; DEs control what is pivotable by defining the metric catalog
- Cost controls: query limits, result caching, pre-aggregated rollup tables for common pivots
- Governance: audit log of all generated queries; column-level access controls on sensitive metrics
Why this is asked: architects design systems that empower users without sacrificing control.

**Q2: A downstream ML feature store requires data in wide (feature-per-column) format, but your warehouse stores data in long (entity-attribute-value) format. Design the pipeline that bridges the two, including handling new features added by data scientists.**
What a good answer covers:
- Maintain a feature registry table that maps feature names to source attribute values
- A templated dynamic PIVOT query reads the registry and generates the wide feature table
- When a data scientist adds a new feature, they update the registry; the pipeline automatically includes it in the next run
- Schema evolution in the feature store: use Parquet/Delta with schema merge enabled so new columns are added without rewriting history
- Connect to orchestration: the PIVOT job is triggered after the attribute table is refreshed
Why this is asked: connects PIVOT to ML feature engineering and schema evolution — a cross-track architect question.

---

## JSON / Array Functions

### Level 1 — Starter

**Q1: Why do modern cloud warehouses store semi-structured data (JSON) natively, and what is the basic function for extracting a field from a JSON column?**
What a good answer covers:
- Semi-structured data from APIs, event streams, and NoSQL sources does not always have a fixed schema
- Storing raw JSON avoids upfront schema design and enables schema-on-read
- Basic extraction: `JSON_VALUE(col, '$.field')` (SQL standard), `col:field` (Snowflake), `JSON_EXTRACT_SCALAR(col, '$.field')` (BigQuery)
Why this is asked: JSON handling is now a baseline DE skill as APIs and event sources dominate ingestion.

**Q2: What is the difference between `JSON_VALUE` and `JSON_QUERY` (or their engine equivalents)?**
What a good answer covers:
- `JSON_VALUE` extracts a scalar value (string, number) from a JSON path
- `JSON_QUERY` extracts a JSON fragment (object or array) and returns it as a string
- Trying to use `JSON_VALUE` on a nested object or array returns NULL or an error; `JSON_QUERY` is needed for sub-documents
Why this is asked: using the wrong function is a common source of silent NULLs.

**Q3: How do you "flatten" a JSON array into rows in SQL?**
What a good answer covers:
- Snowflake: `LATERAL FLATTEN(input => col, path => '$.items')`
- BigQuery: `UNNEST(JSON_EXTRACT_ARRAY(col, '$.items'))`
- PostgreSQL: `jsonb_array_elements(col->'items')`
- The result is one row per array element; combined with the original row's columns using a JOIN or LATERAL join
Why this is asked: array flattening is required for almost any event-based data pipeline.

**Q4: What is an ARRAY type in SQL, and what is a common use case for storing arrays in a warehouse column?**
What a good answer covers:
- An ARRAY column stores an ordered list of values of the same type in a single cell
- Common use cases: tags on a product, list of purchased item IDs in an order, multi-value attributes from a form
- Arrays avoid the need for a separate child table for simple one-to-many relationships
- Querying array elements requires UNNEST or FLATTEN, which increases query complexity
Why this is asked: arrays are increasingly common in modern warehouse schemas.

### Level 2 — Mid

**Q1: Write a query that extracts the `event_type` and `user_id` from a JSON column called `payload` for all rows where `payload.status = 'active'`, handling NULLs safely.**
What a good answer covers:
- Extract fields with appropriate functions; filter with a WHERE clause on the extracted scalar
- Use `TRY_CAST` or `TRY_PARSE_JSON` to handle malformed JSON gracefully (returns NULL instead of erroring)
- Filter: `WHERE JSON_VALUE(payload, '$.status') = 'active'` — note that JSON strings compare as strings
- NULL safety: `COALESCE(JSON_VALUE(...), 'unknown')` for reporting columns
Why this is asked: safe JSON extraction with NULL handling is a daily DE task.

**Q2: How do you aggregate values from a JSON array column — for example, summing all `amount` values inside a `transactions` array — in Snowflake or BigQuery?**
What a good answer covers:
- FLATTEN/UNNEST the array, then apply a standard SUM with GROUP BY on the parent row's key
- Snowflake: `SUM(f.value:amount::FLOAT)` after `LATERAL FLATTEN(input => col, path => '$.transactions') f`
- BigQuery: `SUM(CAST(item.amount AS FLOAT64))` after `UNNEST(JSON_EXTRACT_ARRAY(col, '$.transactions')) item`
- Casting is required because extracted values are strings by default
Why this is asked: aggregating nested arrays is a core pattern in event-driven data.

**Q3: What are the performance implications of storing large JSON blobs versus extracting columns at ingest time in a columnar warehouse?**
What a good answer covers:
- Columnar warehouses compress and prune by column; JSON blobs are opaque and cannot be pruned or compressed efficiently
- Queries that extract a single field from a large JSON blob must read the entire blob per row
- Extracting columns at ingest (schema-on-write) enables column pruning and predicate pushdown
- Hybrid: store raw JSON in Bronze, extract typed columns in Silver — best of both approaches
Why this is asked: JSON performance is a real cost driver in warehouse environments.

**Q4: How do you handle schema evolution in a JSON column when upstream systems add new fields?**
What a good answer covers:
- JSON columns absorb new fields automatically; no DDL change is needed in Bronze
- Silver/Gold models that explicitly extract fields will miss new fields until the SQL is updated
- Mitigation: use `SELECT * EXCEPT (json_col), JSON_EXTRACT(json_col, '$.new_field') AS new_field` style queries
- Schema change notifications from upstream (via a schema registry or contract) allow proactive model updates
Why this is asked: schema evolution is one of the main reasons JSON is attractive, but it creates downstream fragility.

### Level 3 — Senior

**Q1: A Kafka topic (from c001_kafka_concepts_demo.py) emits JSON events with a nested `metadata` object and a `line_items` array. Design the Silver layer transformation that normalizes this into relational tables.**
What a good answer covers:
- Parse and validate JSON in a Bronze-to-Silver job; reject malformed records to a dead-letter table
- Extract scalars from `metadata` into columns of an `events` Silver table
- FLATTEN `line_items` into a separate `event_line_items` Silver table joined by event ID
- Apply type casting and NULL handling during extraction; document the schema in a data dictionary
- Use schema registry (Confluent, Glue) to version the JSON schema and detect breaking changes
Why this is asked: connects JSON/array functions to the streaming track and medallion architecture.

**Q2: You discover that 5% of JSON payloads in your pipeline have malformed structure — missing required fields or wrong types. What is your defensive coding strategy in SQL?**
What a good answer covers:
- Use `TRY_CAST` / `TRY_PARSE_JSON` to handle type errors gracefully
- Add explicit NULL checks for required fields; route NULL rows to a quarantine table with the original JSON and a failure reason
- Log a COUNT of quarantined rows per batch; alert if the quarantine rate exceeds a threshold
- Reprocess quarantined rows after upstream fixes; keep the original JSON so no data is lost
Why this is asked: production pipelines must handle bad data without failing the entire batch.

**Q3: Compare Snowflake's VARIANT type with BigQuery's JSON type and PostgreSQL's JSONB. What are the key differences for a DE building cross-platform pipelines?**
What a good answer covers:
- Snowflake VARIANT: stores any semi-structured data (JSON, Avro, Parquet); accessed with colon notation; automatically typed on extraction; stores up to 16 MB per cell
- BigQuery JSON: dedicated JSON type added in 2022; uses JSON functions; no schema inference, always returns strings
- PostgreSQL JSONB: binary JSON with GIN index support; rich query operators; supports containment queries (`@>`) not available in warehouse SQL
- Cross-platform portability: the extraction syntax is different enough that abstraction (dbt macros, Jinja) is needed for multi-engine support
Why this is asked: cross-platform JSON handling is a real DE challenge when organizations use multiple cloud platforms.

### Level 4 — Architect

**Q1: Design a pipeline that ingests 10,000 JSON events per second from Kafka (c001_kafka_concepts_demo.py), validates schema, extracts typed columns, and makes data queryable in a warehouse within 5 minutes end-to-end.**
What a good answer covers:
- Stream processor (Flink or Spark Structured Streaming) reads from Kafka, validates against a schema registry
- Invalid records go to a dead-letter Kafka topic; valid records are written to Iceberg/Delta Bronze as micro-batch Parquet files
- A Silver job (triggered by file arrival or on a 1-minute schedule) flattens arrays and extracts typed columns into Silver tables
- Gold layer is a pre-aggregated materialized view refreshed on a 5-minute schedule
- End-to-end latency: Kafka ingestion ~1s, Bronze write ~30s, Silver transform ~2min, Gold refresh ~2min — achieves the 5-minute SLA
Why this is asked: connects JSON/array processing to streaming architecture and end-to-end SLA design.

**Q2: Your organization stores customer profiles as JSON in a data lake. Legal requires that when a customer requests deletion (GDPR right to erasure), all JSON fields containing PII are purged within 24 hours. Design the erasure pipeline.**
What a good answer covers:
- Maintain a PII field registry that lists which JSON paths contain PII for each event type
- On deletion request, identify all Bronze table partitions containing the customer's records using a customer ID index
- Rewrite affected Parquet files with PII JSON paths nulled out or removed; update the table metadata (Delta/Iceberg snapshot)
- Verify erasure by running a scan query against the updated partitions; log the verification result for compliance audit
- JSON makes PII harder to erase than typed columns because PII can be nested anywhere; the field registry must be kept current as schemas evolve
Why this is asked: GDPR erasure in a JSON-heavy lakehouse is a real architect-level challenge connecting data engineering to legal compliance.

---

## Dynamic SQL

### Level 1 — Starter

**Q1: What is dynamic SQL, and what problem does it solve that static SQL cannot?**
What a good answer covers:
- Dynamic SQL constructs a query string at runtime rather than at write time
- It solves problems where table names, column names, or the number of columns are not known until runtime
- Common use cases: dynamic PIVOT (columns from data), parameterized table names for multi-tenant schemas, generating DDL programmatically
Why this is asked: establishes the motivation before testing implementation knowledge.

**Q2: What is SQL injection and why is it the primary risk of dynamic SQL?**
What a good answer covers:
- SQL injection occurs when user-controlled input is concatenated directly into a SQL string without sanitization
- An attacker can inject `'; DROP TABLE users; --` to execute arbitrary SQL
- Mitigation: use parameterized queries / bind variables for values; for identifiers (table/column names), use a whitelist or quoting functions
- Dynamic SQL built from internal metadata (INFORMATION_SCHEMA) rather than user input is lower risk but still requires review
Why this is asked: every DE who writes dynamic SQL must understand the injection risk.

**Q3: In Snowflake, how do you execute a dynamically constructed SQL string from within a stored procedure?**
What a good answer covers:
- Use Snowflake Scripting: `EXECUTE IMMEDIATE :sql_string` where `sql_string` is a VARCHAR variable
- JavaScript UDFs can also call `snowflake.execute({ sqlText: sqlString })`
- Always build the SQL string using variables and quoting, never by concatenating raw user input
Why this is asked: EXECUTE IMMEDIATE is the primary dynamic SQL mechanism in Snowflake.

**Q4: What are the debugging challenges of dynamic SQL compared to static SQL?**
What a good answer covers:
- The generated SQL string is not visible to a static query analyzer; syntax errors only surface at runtime
- Execution plans cannot be precomputed; plan instability is harder to diagnose
- Logging the generated SQL string before execution is essential for debugging
- Unit testing is harder: you must test the string generation logic and the execution separately
Why this is asked: debugging difficulty is a key reason to use dynamic SQL sparingly.

### Level 2 — Mid

**Q1: Write a Snowflake stored procedure (in pseudocode or outline) that dynamically generates a PIVOT query for a table where the pivot column values are read from a metadata table.**
What a good answer covers:
- Query the metadata table to get the list of pivot values: `SELECT DISTINCT month FROM dim_months ORDER BY month`
- Build a string: `'SELECT customer, ' || LISTAGG('SUM(CASE WHEN month = ''' || month || ''' THEN amount END) AS "' || month || '"', ', ') || ' FROM transactions GROUP BY customer'`
- Execute with `EXECUTE IMMEDIATE`
- Log the generated SQL string for auditability
Why this is asked: dynamic PIVOT is the canonical mid-level dynamic SQL exercise.

**Q2: How do you safely include a table name in a dynamic SQL string to prevent injection when the table name comes from a configuration table?**
What a good answer covers:
- Validate the table name against a whitelist of known tables (query INFORMATION_SCHEMA.TABLES)
- Use the engine's identifier quoting function to wrap the table name (e.g., `IDENTIFIER(:table_name)` in Snowflake)
- Never concatenate a raw string that originated from user input without validation
- Log the table name used for each execution for audit purposes
Why this is asked: identifier injection is less well-known than value injection but equally dangerous.

**Q3: A dbt project uses Jinja macros to generate SQL dynamically. How does this differ from runtime dynamic SQL, and what are the trade-offs?**
What a good answer covers:
- dbt Jinja generates SQL at compile time (before the query runs); the resulting SQL is static at runtime
- This means the generated SQL can be inspected, version-controlled, and analyzed by the query optimizer as static SQL
- Runtime dynamic SQL (EXECUTE IMMEDIATE) generates SQL during execution; the plan cannot be precomputed
- dbt Jinja is safer and more debuggable; runtime dynamic SQL is needed when the structure cannot be known at compile time
Why this is asked: dbt is ubiquitous in DE interviews; distinguishing compile-time from runtime generation is a key concept.

**Q4: What is a "SQL template" pattern and how does it improve maintainability of dynamic SQL in a pipeline?**
What a good answer covers:
- A SQL template stores the query skeleton with placeholders (e.g., `{table_name}`, `{date_column}`) in a separate file or config
- The pipeline reads the template and substitutes values at runtime using a safe substitution method (not string concatenation)
- Benefits: the template is readable and reviewable without understanding the orchestration code; changes to the query do not require code changes
- Jinja2 templates in Python pipelines are a common implementation
Why this is asked: template patterns are a mature approach to dynamic SQL that many candidates have used but few can articulate.

### Level 3 — Senior

**Q1: Design a framework for generating and executing hundreds of similar warehouse tables (one per client in a multi-tenant system) using dynamic SQL, with safeguards against runaway execution.**
What a good answer covers:
- Store the table template and client list in a configuration table; the framework iterates over clients and generates SQL for each
- Safeguards: max-client limit per run, dry-run mode that logs generated SQL without executing, transaction wrapping per client so a failure in one client does not affect others
- Idempotency: check if the table already exists before CREATE; use CREATE OR REPLACE carefully to avoid dropping existing data
- Monitoring: log execution time and row count per client table; alert on outliers
Why this is asked: multi-tenant dynamic table generation is a real production pattern with real failure modes.

**Q2: A dynamic SQL procedure runs nightly and generates different query plans on different nights for the same logical query. What are the likely causes and mitigations?**
What a good answer covers:
- Parameter sniffing / plan caching: the engine caches the plan from the first execution; if the generated SQL string differs slightly (e.g., different whitespace), a new plan is generated
- Statistics staleness: if statistics on the target tables change between nights, the optimizer chooses a different plan
- Non-deterministic column ordering in the generated SQL can cause plan cache misses
- Mitigations: normalize the generated SQL string (sort columns, strip extra whitespace) before execution; update statistics before running; use query hints to pin plans for critical paths
Why this is asked: plan instability in dynamic SQL is a senior-level operational concern.

**Q3: How do you test a dynamic SQL generator to ensure it produces correct SQL across all input variations without executing against the warehouse?**
What a good answer covers:
- Unit test the string generation function in Python/Jinja with a set of known inputs and assert the exact output string
- Use a SQL parser library (sqlglot, sqlparse) to validate that the generated string is syntactically valid SQL
- Snapshot test: store the expected SQL output for each input combination; CI fails if the output changes unexpectedly
- Integration test: execute against a sandboxed dev warehouse with fixture data to validate results
Why this is asked: testing dynamic SQL generators is often neglected and is a senior-level engineering practice.

### Level 4 — Architect

**Q1: Your organization wants to build a self-service ELT framework where analysts define transformations in YAML and the framework generates and executes the SQL. Design the architecture with governance guardrails.**
What a good answer covers:
- YAML schema defines: source table, filters, joins, aggregations, output table name — all validated against a schema before SQL generation
- SQL generation layer (Python + Jinja2) converts YAML to SQL; generated SQL is stored in a review queue before execution
- Governance: generated SQL is logged with the analyst's identity, reviewed by a DE before first execution, then auto-approved on subsequent identical runs
- Cost controls: generated queries are analyzed for estimated scan size before execution; queries over a threshold require approval
- Connects to orchestration: the framework submits jobs to Airflow/Prefect; results are written to sandbox schemas, not production, until promoted
Why this is asked: self-service SQL generation is an architectural pattern that requires balancing democratization with governance.

**Q2: Dynamic SQL is used in your pipeline to generate partition management commands (ALTER TABLE DROP PARTITION, ADD PARTITION). A bug causes the wrong partition to be dropped in production. Design a safer architecture that eliminates this class of error.**
What a good answer covers:
- Dry-run mode: all destructive DDL is logged and requires a human approval step before execution in production
- Partition management via a declarative config: the desired partition state is declared; a reconciliation job computes the diff and generates only the necessary DDL
- Use table formats (Delta Lake, Iceberg) that manage partitions automatically via inserts; explicit partition DDL is not needed
- Audit log: every DDL statement executed is logged with timestamp, generated SQL, and the parameters that produced it — enabling rollback analysis
- Time travel: Delta/Iceberg allow restoring a dropped partition from a previous snapshot within the retention window
Why this is asked: DDL automation failures are catastrophic; architects must design systems that prevent or recover from them.
