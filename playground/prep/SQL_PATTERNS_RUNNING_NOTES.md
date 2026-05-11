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
