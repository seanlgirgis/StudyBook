# SQL Patterns Running Notes

This is a running side-note document for SQL patterns.
Each section should answer:
- What it is
- When to use it
- Mental model
- SQL template
- Common mistake
- One sentence to memorize

<a id="toc"></a>

## Table of Contents

- [1. CTEs](#pattern-01-ctes)
- [2. Joins](#pattern-02-joins)
- [3. Latest Record Per Entity With ROW_NUMBER()](#pattern-03-latest-record-row-number)
- [4. Window Functions](#pattern-04-window-functions)
- [5. Conditional Aggregation](#pattern-05-conditional-aggregation)
- [6. Source-to-Target Reconciliation](#pattern-06-source-to-target-reconciliation)
- [7. Deduplication With ROW_NUMBER()](#pattern-07-deduplication-row-number)

---

<a id="pattern-01-ctes"></a>
## 1. CTEs

What it is:
A CTE is a temporary named result inside one SQL query.

When to use it:
Use CTEs to break a large query into readable stages.

Mental model:
Break a large query into named steps.

SQL template:

```sql
WITH base AS (
    SELECT ...
    FROM source_table
),
cleaned AS (
    SELECT ...
    FROM base
),
final AS (
    SELECT ...
    FROM cleaned
)
SELECT *
FROM final;
```

Common mistake:
Thinking a CTE is a permanent table. It only lives for that query.

Memorize:
I use CTEs to break complex SQL into clear stages: base, cleaned, enriched, aggregated, and final output.

Alias rule:
When column names repeat, alias the CTE/table and qualify columns.

```sql
FROM service_summary AS ss
JOIN service_info AS si
    ON ss.service_id = si.service_id

SELECT
    si.service_id,
    si.service_name,
    ss.sample_count;
```

[Back to TOC](#toc)

---

<a id="pattern-02-joins"></a>
## 2. Joins

What it is:
A join combines rows from two tables using a matching condition.

When to use it:
Use joins when one table has part of the story and another table has related details.

Mental model:
One table has one part of the story. Another table has another part. JOIN puts the story together.

SQL template:

```sql
SELECT
    a.id,
    a.value,
    b.description
FROM table_a AS a
INNER JOIN table_b AS b
    ON a.id = b.id;
```

Join types:
- INNER JOIN: only matching rows.
- LEFT JOIN: keep all rows from the left/main table.
- RIGHT JOIN: keep all rows from the right table, but often rewrite as LEFT JOIN.
- FULL OUTER JOIN: keep everything from both sides.
- Anti-join: find records in A with no match in B.

LEFT JOIN template:

```sql
SELECT
    a.id,
    a.value,
    b.description
FROM table_a AS a
LEFT JOIN table_b AS b
    ON a.id = b.id;
```

Anti-join template:

```sql
SELECT
    a.*
FROM table_a AS a
LEFT JOIN table_b AS b
    ON a.id = b.id
WHERE b.id IS NULL;
```

Common mistake:
Join explosion. If the join key is duplicated on the right side, rows can multiply.

Duplicate-key check:

```sql
SELECT
    id,
    COUNT(*) AS row_count
FROM table_b
GROUP BY id
HAVING COUNT(*) > 1;
```

Memorize:
Before joining, I check the grain and key uniqueness, then choose the join type based on whether unmatched rows should be preserved.

[Back to TOC](#toc)

---

<a id="pattern-03-latest-record-row-number"></a>
## 3. Latest Record Per Entity With ROW_NUMBER()

What it is:
Use this when many rows exist per entity and you only want the newest row.

When to use it:
- latest telemetry sample per server
- latest order status per order
- latest customer record per customer
- latest pipeline run per job

Mental model:
GROUP BY collapses rows. ROW_NUMBER ranks rows while keeping full rows.

SQL template:

```sql
WITH ranked AS (
    SELECT
        t.*,
        ROW_NUMBER() OVER (
            PARTITION BY t.entity_id
            ORDER BY t.updated_at DESC, t.id DESC
        ) AS rn
    FROM some_table AS t
)
SELECT *
FROM ranked
WHERE rn = 1;
```

Common mistake:
Using MAX(updated_at) only gives the latest timestamp, not the full latest row.

Tie breaker:
If timestamps can tie, add a second ORDER BY column such as id DESC or load_timestamp DESC.

Memorize:
For latest-record logic, I partition by the entity, order by timestamp descending, add a tie-breaker, and keep rn = 1.

[Back to TOC](#toc)

---

<a id="pattern-04-window-functions"></a>
## 4. Window Functions

What it is:
A window function calculates across related rows without collapsing them.

When to use it:
Use it for ranking, running totals, or comparing row values to group context.

Mental model:
Group context plus keep every row.

SQL template:

```sql
SELECT
    customer_id,
    order_date,
    amount,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY order_date DESC
    ) AS rn,
    SUM(amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM orders;
```

Common mistake:
Forgetting PARTITION BY or using the wrong ORDER BY, which changes the result logic.

Memorize:
Window functions give each row group awareness without losing detail.

[Back to TOC](#toc)

---

<a id="pattern-05-conditional-aggregation"></a>
## 5. Conditional Aggregation

What it is:
Conditional aggregation counts or sums rows that meet a condition.

When to use it:
Use it when you need multiple filtered metrics in one grouped query.

Mental model:
Aggregate once, filter inside CASE.

SQL template:

```sql
SELECT
    region,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_orders,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) AS completed_revenue
FROM orders
GROUP BY region;
```

Common mistake:
Putting the condition in WHERE and accidentally removing rows needed for other metrics.

Memorize:
Use CASE inside aggregates to get many metrics from one grouped pass.

[Back to TOC](#toc)

---

<a id="pattern-06-source-to-target-reconciliation"></a>
## 6. Source-to-Target Reconciliation

What it is:
A reconciliation pattern checks whether data in the target matches what came from the source after a pipeline run.

When to use it:
Use it after ETL/ELT jobs to validate that data was loaded correctly.

Mental model:
Do not only ask "did row counts match?"
Ask:
- Did keys match?
- Did counts match?
- Did control totals match?
- Are records missing from target?
- Are extra records present in target?
- Do important fields match?

SQL template 1: count and control total check

```sql
SELECT
    'source' AS dataset_name,
    COUNT(*) AS row_count,
    SUM(amount) AS total_amount
FROM source_table

UNION ALL

SELECT
    'target' AS dataset_name,
    COUNT(*) AS row_count,
    SUM(amount) AS total_amount
FROM target_table;
```

SQL template 2: missing from target

```sql
SELECT
    src.*
FROM source_table AS src
LEFT JOIN target_table AS tgt
    ON src.business_key = tgt.business_key
WHERE tgt.business_key IS NULL;
```

SQL template 3: extra in target

```sql
SELECT
    tgt.*
FROM target_table AS tgt
LEFT JOIN source_table AS src
    ON tgt.business_key = src.business_key
WHERE src.business_key IS NULL;
```

SQL template 4: value mismatch

```sql
SELECT
    src.business_key,
    src.amount AS source_amount,
    tgt.amount AS target_amount
FROM source_table AS src
INNER JOIN target_table AS tgt
    ON src.business_key = tgt.business_key
WHERE src.amount <> tgt.amount;
```

Optional advanced summary pattern:

```sql
WITH comparison AS (
    SELECT
        COALESCE(src.business_key, tgt.business_key) AS business_key,
        src.business_key AS source_key,
        tgt.business_key AS target_key,
        src.amount AS source_amount,
        tgt.amount AS target_amount
    FROM source_table AS src
    FULL OUTER JOIN target_table AS tgt
        ON src.business_key = tgt.business_key
)
SELECT
    COUNT(*) AS compared_keys,

    SUM(CASE
            WHEN source_key IS NOT NULL
             AND target_key IS NOT NULL
            THEN 1 ELSE 0
        END) AS matched_keys,

    SUM(CASE
            WHEN source_key IS NOT NULL
             AND target_key IS NULL
            THEN 1 ELSE 0
        END) AS missing_in_target,

    SUM(CASE
            WHEN source_key IS NULL
             AND target_key IS NOT NULL
            THEN 1 ELSE 0
        END) AS extra_in_target,

    SUM(CASE
            WHEN source_key IS NOT NULL
             AND target_key IS NOT NULL
             AND source_amount <> target_amount
            THEN 1 ELSE 0
        END) AS value_mismatch_count
FROM comparison;
```

Common mistakes:
- Only checking row counts.
- Joining on the wrong key.
- Ignoring duplicate keys before reconciliation.
- Forgetting null-safe comparison rules.
- Not checking business totals or control totals.

Memorize:
For reconciliation, I compare source and target by keys, counts, control totals, missing records, extra records, and field-level mismatches.

Strong practical sentence:
Row count reconciliation is only the first layer. For production confidence, I also reconcile business keys, control totals, and important fields, then investigate missing, extra, or mismatched records.

[Back to TOC](#toc)

---

<a id="pattern-07-deduplication-row-number"></a>
## 7. Deduplication With ROW_NUMBER()

What it is:
A deduplication pattern keeps one best row per duplicate business key.

When to use it:
Use it when many records exist for the same business entity and you need to choose one survivor row.

Examples:
- duplicate customers by customer_id or email
- duplicate orders by order_id
- duplicate telemetry samples by server_id + sampled_at
- duplicate events by event_id
- duplicate files by file_name + batch_id

Mental model:
Latest-record logic asks: which row is newest?
Deduplication asks: which row should survive?

Survivor rule:
Before deduping, define the business rule for the winning row.

Example survivor rule:
Keep the latest updated_at.
If there is a tie, keep the highest record_id.

SQL template:

```sql
WITH ranked AS (
    SELECT
        t.*,
        ROW_NUMBER() OVER (
            PARTITION BY t.business_key
            ORDER BY t.updated_at DESC, t.id DESC
        ) AS rn
    FROM source_table AS t
)
SELECT *
FROM ranked
WHERE rn = 1;
```

Meaning:
- PARTITION BY business_key groups the duplicate records.
- ORDER BY updated_at DESC puts the newest row first.
- ORDER BY id DESC is a deterministic tie-breaker.
- rn = 1 keeps the survivor row.

Find duplicate groups first:

```sql
SELECT
    business_key,
    COUNT(*) AS row_count
FROM source_table
GROUP BY business_key
HAVING COUNT(*) > 1;
```

Rejected duplicates / audit output:

```sql
WITH ranked AS (
    SELECT
        t.*,
        ROW_NUMBER() OVER (
            PARTITION BY t.business_key
            ORDER BY t.updated_at DESC, t.id DESC
        ) AS rn
    FROM source_table AS t
)
SELECT *
FROM ranked
WHERE rn > 1;
```

Data engineering example: deduplicate telemetry samples

```sql
WITH ranked_samples AS (
    SELECT
        ts.*,
        ROW_NUMBER() OVER (
            PARTITION BY ts.server_id, ts.sampled_at
            ORDER BY ts.ingested_at DESC, ts.sample_id DESC
        ) AS rn
    FROM telemetry_samples AS ts
)
SELECT
    sample_id,
    server_id,
    sampled_at,
    cpu_percent,
    memory_percent,
    ingested_at
FROM ranked_samples
WHERE rn = 1;
```

Why not DISTINCT:
DISTINCT removes rows only when all selected columns are identical.
ROW_NUMBER lets you define which duplicate row should survive.

Common mistakes:
- Using DISTINCT when duplicates are not exactly identical.
- Forgetting a deterministic tie-breaker.
- Partitioning by the wrong key.
- Deduping before understanding the business rule.
- Deleting duplicate rows without preserving an audit trail.

Memorize:
For deduplication, I define the duplicate business key, rank records by the survivor rule, add a tie-breaker, and keep rn = 1.

Strong practical sentence:
I do not rely only on DISTINCT for deduplication. I first define the business key and survivor rule, then use ROW_NUMBER to keep the best record and optionally preserve rejected duplicates for audit.

[Back to TOC](#toc)
