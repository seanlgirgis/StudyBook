# Course 05 Mistakes and Corrections

## Mistake: Using ORDER BY inside OVER accidentally made a running calculation

### What happened
A full-partition total turned into a running total.

### Why it happened
Adding `ORDER BY` inside an aggregate window changes the behavior from whole-partition to cumulative/running.

### Corrected pattern
```sql
SUM(revenue) OVER (PARTITION BY region) AS region_total_revenue
```

Keep `ORDER BY` only when running behavior is intended.

### Memory nugget
No window ORDER BY = whole partition. Window ORDER BY = running behavior.

## Mistake: Confusing final ORDER BY with window ORDER BY

### What happened
Display sorting and calculation sorting got mixed together.

### Why it happened
Both clauses use the words `ORDER BY`, but they do different jobs.

### Corrected pattern
Window `ORDER BY` calculates. Final `ORDER BY` displays.

### Memory nugget
Window ORDER BY calculates. Final ORDER BY displays.

## Mistake: Putting unique tie-breakers into RANK / DENSE_RANK

### What happened
Tied values stopped tying.

### Why it happened
A unique tie-breaker destroys ties.

### Corrected pattern
Use unique tie-breakers for `ROW_NUMBER` unless the business wants ties broken.

### Memory nugget
ROW_NUMBER can break ties. RANK and DENSE_RANK usually should not.

## Mistake: Trying to filter a window alias in the same SELECT

### What happened
The query tried to use a window alias before it existed.

### Why it happened
`WHERE` runs before select aliases exist.

### Corrected pattern
```sql
WITH ranked_rows AS (
  SELECT
    salesperson,
    ROW_NUMBER() OVER (ORDER BY revenue DESC) AS rn
  FROM sales_events
)
SELECT *
FROM ranked_rows
WHERE rn <= 3;
```

### Memory nugget
Calculate first in a CTE. Filter second outside it.

## Mistake: LAST_VALUE returned the current row

### What happened
`LAST_VALUE` did not return the true last row in the partition.

### Why it happened
The default frame ended at `CURRENT ROW`.

### Corrected pattern
```sql
LAST_VALUE(revenue) OVER (
  PARTITION BY region
  ORDER BY sale_date, event_id
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

### Memory nugget
LAST_VALUE needs the full frame.

## Mistake: Semicolon before ORDER BY ended the query too early

### What happened
The SQL statement ended before the final sort.

### Why it happened
The semicolon closed the query too soon.

### Corrected pattern
Keep `ORDER BY` before the final semicolon.

### Memory nugget
The semicolon ends the statement. Do not end it too early.

## Mistake: Naming a SUM moving window as moving average

### What happened
A moving total was labeled like a moving average.

### Why it happened
`SUM` with a sliding frame is a moving total, not an average.

### Corrected pattern
`AVG` = moving average. `SUM` = moving total.

### Memory nugget
SUM moves totals. AVG moves averages.

## Mistake: NTILE(100) with only 90 rows returned no bucket 100

### What happened
Expected bucket labels did not appear.

### Why it happened
There were too few rows to populate 100 buckets.

### Corrected pattern
Use fewer buckets or use a true percentile cutoff.

### Memory nugget
Bucket count must fit row count.

## Mistake: Confusing NTILE with P95

### What happened
A bucket label was treated like a percentile cutoff.

### Why it happened
Both sound percentile-like, but they produce different outputs.

### Corrected pattern
Use `percentile_cont` for threshold values.

### Memory nugget
NTILE labels rows. P95 returns a cutoff.

## Mistake: Thinking percentile_cont labels each row

### What happened
`percentile_cont` was expected to behave like a row-by-row function.

### Why it happened
It is an aggregate-style cutoff calculation.

### Corrected pattern
Calculate cutoff in a CTE, join back, then CASE label rows.

### Memory nugget
Percentile first. Join second. Label third.

## Mistake: Confusing WITHIN GROUP with OVER

### What happened
Two different ordering concepts got mixed together.

### Why it happened
Both involve ordering.

### Corrected pattern
`WITHIN GROUP` orders values inside an ordered aggregate. `OVER` creates row-level window calculations.

### Memory nugget
WITHIN GROUP aggregates. OVER windows.

## Mistake: Treating CUME_DIST and PERCENT_RANK as identical

### What happened
Two 0-to-1 style outputs were treated like the same metric.

### Why it happened
They look similar at first glance.

### Corrected pattern
`CUME_DIST` is coverage-based. `PERCENT_RANK` is rank-start based.

### Memory nugget
CUME_DIST looks after the tie group. PERCENT_RANK looks at where the tie group starts.

## Mistake: Creating a score but not translating it

### What happened
A numeric score was produced without a business label.

### Why it happened
The query stopped at analytics instead of turning analytics into a recommendation.

### Corrected pattern
Use `CASE` to create `recommended_action`.

### Memory nugget
Managers want actions, not just scores.

## Mistake: Overbuilding SQL when Pandas/Spark would be cleaner

### What happened
SQL was pushed toward heavier feature engineering than it handled comfortably.

### Why it happened
SQL can express many ideas, but not every workflow is pleasant in SQL.

### Corrected pattern
Use SQL for clear window patterns. Use Pandas/Spark for heavier feature engineering, weighted averages, smoothing, and model pipelines.

### Memory nugget
Use the right tool for the shape of the work.
