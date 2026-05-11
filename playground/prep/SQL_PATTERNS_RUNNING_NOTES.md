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
- [8. Running Totals and Moving Averages](#pattern-08-running-totals-moving-averages)
- [9. LAG() and LEAD()](#pattern-09-lag-lead)
- [10. CASE Classification / Bucketing](#pattern-10-case-classification-bucketing)
- [11. NULL Handling](#pattern-11-null-handling)
- [12. WHERE vs HAVING](#pattern-12-where-vs-having)

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

---

<a id="pattern-08-running-totals-moving-averages"></a>
## 8. Running Totals and Moving Averages

What it is:
A window-function pattern for calculating values across ordered rows while keeping row-level detail.

When to use it:
Use it for time-series, telemetry, cost, sales, capacity, and reporting trends.

Examples:
- running total sales by day
- month-to-date cloud cost
- moving average CPU usage
- moving average memory usage
- cumulative order count by customer
- trend smoothing for telemetry metrics

Mental model:
GROUP BY collapses rows.
Window functions keep rows and add calculations beside them.

Running total template:

```sql
SELECT
    entity_id,
    event_time,
    value_column,
    SUM(value_column) OVER (
        PARTITION BY entity_id
        ORDER BY event_time
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM source_table
ORDER BY entity_id, event_time;
```

Meaning:
- PARTITION BY entity_id restarts the calculation for each entity.
- ORDER BY event_time defines the time sequence.
- UNBOUNDED PRECEDING means start at the first row in the partition.
- CURRENT ROW means calculate up to this row.

Moving average template:

```sql
SELECT
    entity_id,
    event_time,
    value_column,
    AVG(value_column) OVER (
        PARTITION BY entity_id
        ORDER BY event_time
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_average_3_rows
FROM source_table
ORDER BY entity_id, event_time;
```

Meaning:
- 2 PRECEDING AND CURRENT ROW means use this row plus the previous 2 rows.
- That creates a 3-row moving average.

Telemetry example:

```sql
SELECT
    server_id,
    sampled_at,
    cpu_percent,
    AVG(cpu_percent) OVER (
        PARTITION BY server_id
        ORDER BY sampled_at, sample_id
        ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
    ) AS cpu_moving_avg_5_samples
FROM telemetry_samples
ORDER BY server_id, sampled_at;
```

Cost example:

```sql
SELECT
    account_id,
    usage_date,
    daily_cost,
    SUM(daily_cost) OVER (
        PARTITION BY account_id
        ORDER BY usage_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS month_to_date_cost
FROM daily_cloud_cost
ORDER BY account_id, usage_date;
```

Common mistakes:
- Forgetting ORDER BY. Running totals need a sequence.
- Forgetting PARTITION BY. Different entities get mixed together.
- Using GROUP BY when row-level output is needed.
- Not specifying the window frame.
- Ordering by a non-unique timestamp without a tie-breaker.

Tie breaker:
If timestamps can tie, order by a second stable column.

```sql
ORDER BY sampled_at, sample_id
```

Memorize:
For running totals and moving averages, I partition by the entity, order by time, and define the window frame that says how many rows to look back.

Strong practical sentence:
I use window frames for time-series analysis because they let me keep row-level detail while calculating cumulative totals, recent averages, and trend indicators over ordered events.

[Back to TOC](#toc)

---

<a id="pattern-09-lag-lead"></a>
## 9. LAG() and LEAD()

What it is:
LAG and LEAD are window functions used to compare the current row
to a previous or next row.

When to use it:
Use it when records are ordered over time or sequence and you need
to compare neighboring rows.

Examples:
- compare current CPU to previous CPU sample
- compare today's cost to yesterday's cost
- detect order status changes
- calculate change from prior day
- calculate time between events

Mental model:
LAG looks backward.
LEAD looks forward.

Basic LAG template:

```sql
SELECT
    entity_id,
    event_time,
    value_column,
    LAG(value_column) OVER (
        PARTITION BY entity_id
        ORDER BY event_time
    ) AS previous_value
FROM source_table
ORDER BY entity_id, event_time;
```

Meaning:
- PARTITION BY entity_id keeps each entity separate.
- ORDER BY event_time defines the sequence.
- LAG(value_column) brings the previous row's value into the current row.

Change calculation template:

```sql
WITH with_previous AS (
    SELECT
        entity_id,
        event_time,
        value_column,
        LAG(value_column) OVER (
            PARTITION BY entity_id
            ORDER BY event_time
        ) AS previous_value
    FROM source_table
)
SELECT
    entity_id,
    event_time,
    value_column,
    previous_value,
    value_column - previous_value AS value_change
FROM with_previous
ORDER BY entity_id, event_time;
```

Trend label template:

```sql
WITH with_previous AS (
    SELECT
        entity_id,
        event_time,
        value_column,
        LAG(value_column) OVER (
            PARTITION BY entity_id
            ORDER BY event_time
        ) AS previous_value
    FROM source_table
)
SELECT
    entity_id,
    event_time,
    value_column,
    previous_value,
    value_column - previous_value AS value_change,
    CASE
        WHEN previous_value IS NULL THEN 'FIRST_ROW'
        WHEN value_column > previous_value THEN 'INCREASED'
        WHEN value_column < previous_value THEN 'DECREASED'
        ELSE 'UNCHANGED'
    END AS value_direction
FROM with_previous
ORDER BY entity_id, event_time;
```

Basic LEAD template:

```sql
SELECT
    entity_id,
    event_time,
    value_column,
    LEAD(value_column) OVER (
        PARTITION BY entity_id
        ORDER BY event_time
    ) AS next_value
FROM source_table
ORDER BY entity_id, event_time;
```

Meaning:
- LEAD(value_column) brings the next row's value into the current row.

Status-change example:

```sql
WITH status_steps AS (
    SELECT
        order_id,
        status,
        status_time,
        LAG(status) OVER (
            PARTITION BY order_id
            ORDER BY status_time
        ) AS previous_status
    FROM order_status_history
)
SELECT
    order_id,
    previous_status,
    status AS current_status,
    status_time
FROM status_steps
WHERE previous_status IS NULL
   OR previous_status <> status
ORDER BY order_id, status_time;
```

Common mistakes:
- Forgetting PARTITION BY, which mixes different entities.
- Forgetting ORDER BY, which makes "previous" meaningless.
- Not handling the first row, where previous value is NULL.
- Ordering only by timestamp when ties are possible.
- Using LAG when ROW_NUMBER is needed for latest-record selection.

Tie breaker:
If timestamps can tie, add a stable second ordering column.

```sql
ORDER BY event_time, event_id
```

Memorize:
I use LAG to compare the current row to the previous row,
and LEAD to compare the current row to the next row.

Strong practical sentence:
For trend and status-change analysis, I partition by the entity,
order by event time, use LAG or LEAD to bring neighboring values
onto the current row, and then calculate differences or change flags.

[Back to TOC](#toc)

---

<a id="pattern-10-case-classification-bucketing"></a>
## 10. CASE Classification / Bucketing

What it is:
CASE classification turns raw values into readable labels or buckets.

When to use it:
Use it when raw values need to become business-friendly categories.

Examples:
- CPU percent -> NORMAL / WATCH / HIGH / CRITICAL
- order amount -> SMALL / MEDIUM / LARGE
- data quality score -> PASS / WARNING / FAIL
- latency -> FAST / SLOW / DEGRADED
- null or invalid values -> MISSING / INVALID

Mental model:
CASE checks WHEN conditions from top to bottom.
SQL stops at the first true condition.

Basic template:

```sql
SELECT
    entity_id,
    value_column,
    CASE
        WHEN value_column >= 95 THEN 'CRITICAL'
        WHEN value_column >= 85 THEN 'HIGH'
        WHEN value_column >= 70 THEN 'WATCH'
        ELSE 'NORMAL'
    END AS status_label
FROM source_table;
```

Order matters:
Put the most specific or highest-priority condition first.

Correct:

```sql
CASE
    WHEN cpu_percent >= 95 THEN 'CRITICAL'
    WHEN cpu_percent >= 85 THEN 'HIGH'
    WHEN cpu_percent >= 70 THEN 'WATCH'
    ELSE 'NORMAL'
END AS cpu_status
```

Wrong:

```sql
CASE
    WHEN cpu_percent >= 70 THEN 'WATCH'
    WHEN cpu_percent >= 85 THEN 'HIGH'
    WHEN cpu_percent >= 95 THEN 'CRITICAL'
    ELSE 'NORMAL'
END AS cpu_status
```

Why wrong:
A value like 99 is also >= 70, so it gets labeled WATCH first.
SQL stops at the first match.

Production-safe template with NULL handling:

```sql
CASE
    WHEN value_column IS NULL THEN 'MISSING'
    WHEN value_column >= critical_threshold THEN 'CRITICAL'
    WHEN value_column >= high_threshold THEN 'HIGH'
    WHEN value_column >= warning_threshold THEN 'WATCH'
    ELSE 'NORMAL'
END AS status_label
```

Data quality example:

```sql
SELECT
    batch_id,
    total_rows,
    missing_customer_id_count,
    duplicate_order_count,
    CASE
        WHEN missing_customer_id_count > 0 THEN 'FAIL'
        WHEN duplicate_order_count > 0 THEN 'WARNING'
        ELSE 'PASS'
    END AS quality_status
FROM batch_quality_summary;
```

Bucketing example:

```sql
SELECT
    order_id,
    order_total,
    CASE
        WHEN order_total IS NULL THEN 'MISSING'
        WHEN order_total < 0 THEN 'INVALID'
        WHEN order_total >= 1000 THEN 'LARGE'
        WHEN order_total >= 250 THEN 'MEDIUM'
        ELSE 'SMALL'
    END AS order_size_bucket
FROM orders;
```

CASE inside aggregation:

```sql
SELECT
    service_name,
    COUNT(*) AS total_samples,
    SUM(CASE WHEN cpu_percent >= 90 THEN 1 ELSE 0 END) AS high_cpu_samples,
    SUM(CASE WHEN cpu_percent IS NULL THEN 1 ELSE 0 END) AS missing_cpu_samples
FROM telemetry_samples
GROUP BY service_name;
```

Common mistakes:
- Putting broad conditions before specific conditions.
- Forgetting NULL handling.
- Forgetting ELSE, which can create unexpected NULL labels.
- Creating labels that business users do not understand.
- Duplicating classification logic in many places instead of standardizing it.

Memorize:
CASE turns raw values into business-friendly categories, and the order of WHEN conditions matters because SQL stops at the first match.

Strong practical sentence:
I use CASE expressions to make pipeline outputs more operationally useful, such as classifying records into PASS, WARNING, FAIL, or NORMAL, WATCH, HIGH, and CRITICAL categories.

[Back to TOC](#toc)

---

<a id="pattern-11-null-handling"></a>
## 11. NULL Handling

What it is:
NULL means unknown or missing.
It is not zero and not an empty string.

When to use it:
Use this in filtering, reconciliation, comparisons, and fallback-value logic.

Mental model:
NULL is special in SQL.
Normal comparison operators do not behave the same way with NULL.

Why this fails:

```sql
column = NULL
```

Reason:
NULL is unknown, so `=` and `<>` are not the right checks.

Correct checks:

```sql
column IS NULL
column IS NOT NULL
```

Filtering examples:

```sql
SELECT *
FROM customers
WHERE email IS NULL;
```

```sql
SELECT *
FROM customers
WHERE email IS NOT NULL;
```

NULL with comparisons:

```sql
SELECT *
FROM payments
WHERE amount <> 100;
```

Meaning:
Rows where `amount` is NULL are not returned by `amount <> 100`.

NULL-safe comparison (PostgreSQL):

```sql
source_amount IS DISTINCT FROM target_amount
```

Meaning:
- `NULL` vs non-`NULL` is different.
- `NULL` vs `NULL` is not different.

COALESCE:

```sql
COALESCE(value1, value2, fallback_value)
```

Meaning:
Return the first non-NULL value.

Example:

```sql
SELECT
    customer_id,
    COALESCE(phone_number, email, 'NO CONTACT') AS best_contact
FROM customers;
```

Reconciliation pattern with FULL OUTER JOIN:

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
    business_key,
    source_amount,
    target_amount,
    CASE
        WHEN source_key IS NULL THEN 'MISSING_IN_SOURCE'
        WHEN target_key IS NULL THEN 'MISSING_IN_TARGET'
        WHEN source_amount IS DISTINCT FROM target_amount THEN 'AMOUNT_MISMATCH'
        ELSE 'MATCH'
    END AS comparison_status
FROM comparison;
```

Tiny memorize block:

- Use `IS NULL`, not `= NULL`.
- Use `IS NOT NULL`, not `<> NULL`.
- `COALESCE` gives the first non-NULL value.
- Be careful: NULL comparisons do not behave like normal values.

Memorize:
Handle NULLs explicitly in filters, joins, and comparisons so missing values do not hide data-quality issues.

Strong practical sentence:
In SQL reconciliation and reporting, I use IS NULL checks, COALESCE fallback logic, and NULL-safe comparisons so missing values are handled deliberately instead of accidentally ignored.

[Back to TOC](#toc)

---
<a id="pattern-12-where-vs-having"></a>
## 12. WHERE vs HAVING

What it is:
WHERE and HAVING both filter data, but they happen at different stages.

When to use it:
Use WHERE to filter raw rows before grouping.
Use HAVING to filter grouped results after aggregation.

Mental model:
WHERE filters rows.
HAVING filters groups.

Main rule:

WHERE happens before GROUP BY.
HAVING happens after GROUP BY.

Template:

```sql
SELECT
    group_column,
    COUNT(*) AS row_count,
    AVG(value_column) AS avg_value
FROM table_name
WHERE row_level_condition
GROUP BY group_column
HAVING aggregate_condition;
```

Example:

```sql
SELECT
    service_name,
    COUNT(*) AS sample_count,
    AVG(cpu_percent) AS avg_cpu
FROM telemetry_samples
WHERE sampled_at >= '2026-05-01'
GROUP BY service_name
HAVING AVG(cpu_percent) >= 80
ORDER BY avg_cpu DESC;
```

Meaning:
- WHERE sampled_at >= '2026-05-01' keeps only recent raw rows.
- GROUP BY service_name summarizes rows by service.
- HAVING AVG(cpu_percent) >= 80 keeps only service groups with high average CPU.

Wrong example:

```sql
SELECT
    service_name,
    AVG(cpu_percent) AS avg_cpu
FROM telemetry_samples
WHERE AVG(cpu_percent) >= 80
GROUP BY service_name;
```

Why wrong:
WHERE happens before GROUP BY, so AVG(cpu_percent) does not exist yet.

Use WHERE for row-level filters:

```sql
WHERE cpu_percent IS NOT NULL
WHERE sampled_at >= '2026-05-01'
WHERE service_name = 'checkout'
```

Use HAVING for aggregate filters:

```sql
HAVING COUNT(*) > 10
HAVING AVG(cpu_percent) >= 80
HAVING SUM(error_count) > 0
```

Data quality example:

```sql
SELECT
    batch_id,
    COUNT(*) AS total_rows,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS missing_customer_id
FROM orders_raw
WHERE load_date = '2026-05-01'
GROUP BY batch_id
HAVING SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) > 0;
```

Meaning:
- WHERE checks only today's loaded rows.
- GROUP BY summarizes by batch.
- HAVING keeps only batches with missing customer IDs.

Common mistakes:
- Trying to use aggregate functions in WHERE.
- Using HAVING for simple row filters that belong in WHERE.
- Forgetting that WHERE happens before GROUP BY.
- Forgetting that HAVING happens after GROUP BY.

Memorize:
WHERE filters raw rows before grouping. HAVING filters grouped results after aggregation.

Strong practical sentence:
I use WHERE to reduce raw input rows before aggregation, and HAVING to filter grouped results based on counts, averages, sums, or other aggregate conditions.

[Back to TOC](#toc)

