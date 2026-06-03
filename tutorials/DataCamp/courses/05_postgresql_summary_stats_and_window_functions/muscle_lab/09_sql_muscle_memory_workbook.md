# Course 05 SQL Muscle-Memory Workbook

This workbook is hands-on memory training from the local practice session.
It focuses on:
- exercise prompt
- SQL pattern
- result meaning
- mistake/discovery
- corrected pattern
- memory nugget
- interview translation

## 1) Training Mode Rules
- One exercise at a time.
- Sean writes SQL first.
- Review the query before final answer.
- Explain the mistake and corrected pattern.
- Preserve important discoveries as nuggets.

## How to Use This Workbook

This workbook is meant for rehearsal, not passive reading.
For each exercise:

1. Read the business question.
2. Try writing the SQL from memory.
3. Compare against the final SQL.
4. Read the mistake/correction notes.
5. Repeat the memory nugget out loud.

## 2) Exercise 01 — GROUP BY Baseline

Prompt:
Using `sales_events`, show total revenue by region.
Columns: `region`, `total_revenue`.
Sort highest first.

Final SQL:
```sql
SELECT
  region,
  SUM(revenue) AS total_revenue
FROM sales_events
GROUP BY region
ORDER BY total_revenue DESC;
```

Result meaning:
`GROUP BY` collapses many sales rows into one row per region.

Memory nugget:
`GROUP BY` = collapse rows into summary rows.

## 3) Exercise 02 — PARTITION BY Full Region Total

Prompt:
Show each sale row with region total beside it.

Correct SQL:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  SUM(revenue) OVER (
    PARTITION BY region
  ) AS region_total_revenue
FROM sales_events
ORDER BY
  region ASC,
  sale_date ASC,
  sale_id ASC
LIMIT 20;
```

Discovery:
Adding `ORDER BY` inside `OVER` changed the result into a running total.
Removing `ORDER BY` gave the full region total repeated on every row.

Memory nugget:
No `ORDER BY` inside `OVER` = full partition value.
`ORDER BY` inside `OVER` = running value.

## 4) Exercise 03 — COUNT and SUM Full vs Running

Final SQL:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,

  COUNT(*) OVER (
    PARTITION BY region
  ) AS region_row_count,

  COUNT(*) OVER (
    PARTITION BY region
    ORDER BY sale_date, sale_id
  ) AS running_region_row_count,

  SUM(revenue) OVER (
    PARTITION BY region
  ) AS region_total_revenue,

  SUM(revenue) OVER (
    PARTITION BY region
    ORDER BY sale_date, sale_id
  ) AS running_region_revenue

FROM sales_events
ORDER BY
  region ASC,
  sale_date ASC,
  sale_id ASC
LIMIT 20;
```

Result meaning:
- `COUNT` without `ORDER BY` showed one repeated partition count (for example 90 for East).
- `COUNT` with `ORDER BY` showed 1, 2, 3...
- `SUM` without `ORDER BY` showed one repeated partition total.
- `SUM` with `ORDER BY` showed cumulative revenue.

Memory nugget:
`PARTITION BY` chooses the group.
`ORDER BY` inside `OVER` creates a row-by-row journey.

## 5) Named Windows Nugget

A named window is a shortcut for repeated logic inside `OVER()`.

Example:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,

  SUM(revenue) OVER region_window AS region_total_revenue,
  SUM(revenue) OVER region_ordered_window AS running_region_revenue

FROM sales_events

WINDOW
  region_window AS (
    PARTITION BY region
  ),

  region_ordered_window AS (
    PARTITION BY region
    ORDER BY sale_date, sale_id
  )

ORDER BY
  region,
  sale_date,
  sale_id;
```

Explain:
The named window does not store the function.
It stores row grouping and order.

Memory nugget:
`WINDOW` names the window definition, not the calculation.

## 6) Exercise 04 — MAX/MIN Full Region vs So Far

Final SQL:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  MAX(revenue) OVER region_window AS region_max_revenue,
  MAX(revenue) OVER region_ordered_window AS max_revenue_so_far,
  MIN(revenue) OVER region_window AS region_min_revenue,
  MIN(revenue) OVER region_ordered_window AS min_revenue_so_far
FROM sales_events

WINDOW
  region_window AS (
    PARTITION BY region
  ),

  region_ordered_window AS (
    PARTITION BY region
    ORDER BY sale_date, sale_id
  )

ORDER BY
  region ASC,
  sale_date ASC,
  sale_id ASC
LIMIT 20;
```

Memory nugget:
`MAX` with `ORDER BY` = max so far.
`MIN` with `ORDER BY` = min so far.
Without `ORDER BY`, they show full partition max/min.

## 7) Exercise 05 — ROW_NUMBER Inside Region

Final SQL:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  salesperson,
  revenue,
  ROW_NUMBER() OVER (
    PARTITION BY region
    ORDER BY revenue DESC, sale_id ASC
  ) AS region_revenue_row_number
FROM sales_events
ORDER BY
  region ASC,
  region_revenue_row_number ASC
LIMIT 20;
```

Memory nugget:
`ROW_NUMBER` gives exact positions.
It never ties.
Use a tie-breaker for stable output.

## 8) Exercise 06 — ROW_NUMBER vs RANK vs DENSE_RANK

Initial confusion:
- top revenues were mostly unique
- putting `sale_id` in the same window for `RANK`/`DENSE_RANK` broke ties

Corrected pattern:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  salesperson,
  revenue,

  ROW_NUMBER() OVER row_number_window AS row_number_rank,
  RANK() OVER rank_window AS rank_rank,
  DENSE_RANK() OVER rank_window AS dense_rank_rank

FROM sales_events

WINDOW
  row_number_window AS (
    PARTITION BY region
    ORDER BY revenue DESC, sale_id ASC
  ),

  rank_window AS (
    PARTITION BY region
    ORDER BY revenue DESC
  )

ORDER BY
  region ASC,
  revenue DESC,
  sale_id ASC
LIMIT 20;
```

Note:
`ROW_NUMBER` can use tie-breaker.
`RANK`/`DENSE_RANK` should not include a unique tie-breaker when preserving ties.

Artificial tie example:
```sql
WITH sample_scores AS (
  SELECT *
  FROM (
    VALUES
      ('East', 'A', 900),
      ('East', 'B', 700),
      ('East', 'C', 700),
      ('East', 'D', 400)
  ) AS v(region, salesperson, revenue)
)
SELECT
  region,
  salesperson,
  revenue,
  ROW_NUMBER() OVER (
    PARTITION BY region
    ORDER BY revenue DESC, salesperson ASC
  ) AS row_number_rank,
  RANK() OVER (
    PARTITION BY region
    ORDER BY revenue DESC
  ) AS rank_rank,
  DENSE_RANK() OVER (
    PARTITION BY region
    ORDER BY revenue DESC
  ) AS dense_rank_rank
FROM sample_scores
ORDER BY
  region,
  revenue DESC,
  salesperson;
```

Expected behavior:
- 900 -> 1,1,1
- 700 -> 2,2,2
- 700 -> 3,2,2
- 400 -> 4,4,3

Memory nugget:
- `ROW_NUMBER` counts rows.
- `RANK` counts competition positions and leaves gaps.
- `DENSE_RANK` counts distinct value tiers without gaps.

## 9) Forced Tie Data Update

Training-only update used to make ranking differences obvious:
```sql
BEGIN;

UPDATE sales_events
SET revenue = 2000.00
WHERE sale_id = 351;

UPDATE sales_events
SET revenue = 1800.00
WHERE sale_id IN (263, 175);

UPDATE sales_events
SET revenue = 1600.00
WHERE sale_id = 19;

UPDATE sales_events
SET revenue = 1500.00
WHERE sale_id IN (159, 171);

COMMIT;
```

Explain:
This was a training-data adjustment to make differences visible.

## 10) Exercise 07 — Third Salesperson by Department

Journey:
Raw table has sales records.
Business question asks for salesperson totals.
So aggregate first.

Final SQL:
```sql
WITH salesperson_totals AS (
  SELECT
    department,
    salesperson,
    SUM(sales_amount) AS total_sales
  FROM employee_sales
  GROUP BY
    department,
    salesperson
),

ranked_salespeople AS (
  SELECT
    department,
    salesperson,
    total_sales,
    ROW_NUMBER() OVER (
      PARTITION BY department
      ORDER BY total_sales DESC, salesperson ASC
    ) AS sales_rank
  FROM salesperson_totals
)

SELECT
  department,
  salesperson,
  total_sales,
  sales_rank
FROM ranked_salespeople
WHERE sales_rank = 3
ORDER BY department ASC;
```

Memory nugget:
Before ranking, ask what one row should represent.
Here: one salesperson total inside one department.

Interview translation:
Aggregate first, rank second, filter third.

## 11) Exercise 08 — Top 2 Salespeople per Department

Final SQL:
```sql
WITH salesperson_totals AS (
  SELECT
    department,
    salesperson,
    SUM(sales_amount) AS total_sales
  FROM employee_sales
  GROUP BY
    department,
    salesperson
),

ranked_salespeople AS (
  SELECT
    department,
    salesperson,
    total_sales,
    ROW_NUMBER() OVER (
      PARTITION BY department
      ORDER BY total_sales DESC, salesperson ASC
    ) AS sales_rank
  FROM salesperson_totals
)

SELECT
  department,
  salesperson,
  total_sales,
  sales_rank
FROM ranked_salespeople
WHERE sales_rank <= 2
ORDER BY
  department ASC,
  sales_rank ASC;
```

Memory nugget:
Top N per group:
- aggregate to correct grain
- rank inside group
- filter `rank <= N`

## 12) Checkpoint Summary After Exercise 08
- `GROUP BY` collapses.
- `PARTITION BY` keeps detail rows.
- `ORDER BY` inside `OVER` turns aggregates into running calculations.
- Named windows reduce repeated `PARTITION BY` / `ORDER BY` code.
- `ROW_NUMBER` gives exact row positions.
- `RANK` and `DENSE_RANK` preserve ties when no unique tie-breaker is added.
- For business ranking, aggregate to the correct grain before ranking.
- Top N per group = CTE aggregate + CTE rank + outer filter.

## Exercise 09 to 11 — ROW_NUMBER vs RANK vs DENSE_RANK with real ties

Context:
Sean was practicing the interview-style question:
"Find the third salesperson by sales volume per department."

The important learning point:
This question is ambiguous. It can mean:
1. exact third row
2. everyone holding competition rank 3
3. everyone in the third distinct sales tier

Database table used:
`employee_sales`

Important database state:
A controlled tie was created in Data Engineering so the difference is visible.

The forced tie made these totals appear:

| Department       | Salesperson | Total Sales | ROW_NUMBER | RANK | DENSE_RANK |
| ---------------- | ----------: | ----------: | ---------: | ---: | ---------: |
| Data Engineering |   Mila Tran |   260440.00 |          1 |    1 |          1 |
| Data Engineering |    Leah Kim |   253536.00 |          2 |    2 |          2 |
| Data Engineering |   Nora Diaz |   253536.00 |          3 |    2 |          2 |
| Data Engineering |  Evan Stone |   250248.00 |          4 |    4 |          3 |
| Data Engineering |   Avi Gupta |   249152.00 |          5 |    5 |          4 |
| Data Engineering |    Omar Ali |   236632.00 |          6 |    6 |          5 |

ROW_NUMBER:
- Counts physical rows.
- It does not preserve ties.
- Leah and Nora tie in sales, but ROW_NUMBER still gives Leah 2 and Nora 3.
- Use ROW_NUMBER when the business wants exactly one row.

RANK:
- Preserves ties.
- Leaves gaps after ties.
- Leah and Nora both get rank 2.
- Evan gets rank 4, because rank 3 is skipped.
- Use RANK when the business wants competition-style ranking.

DENSE_RANK:
- Preserves ties.
- Does not leave gaps.
- Leah and Nora both get dense rank 2.
- Evan gets dense rank 3.
- Use DENSE_RANK when the business wants the third distinct value tier.

### Forced-tie update statements used
```sql
BEGIN;

WITH target_row AS (
    SELECT
        sale_id
    FROM employee_sales
    WHERE department = 'Data Engineering'
      AND salesperson = 'Leah Kim'
    ORDER BY sale_id
    LIMIT 1
)
UPDATE employee_sales AS e
SET sales_amount = sales_amount + 2192.00
FROM target_row AS t
WHERE e.sale_id = t.sale_id;

COMMIT;
```

This was a training-data adjustment to make Leah Kim tie Nora Diaz at 253536.00 total sales.

### Ranking comparison query
```sql
WITH salesperson_totals AS (
    SELECT
        department,
        salesperson,
        SUM(sales_amount) AS total_sales
    FROM employee_sales
    GROUP BY
        department,
        salesperson
),

ranked_salespeople AS (
    SELECT
        department,
        salesperson,
        total_sales,
        ROW_NUMBER() OVER row_number_window AS row_number_rank,
        RANK()       OVER rank_window       AS rank_rank,
        DENSE_RANK() OVER rank_window       AS dense_rank_rank
    FROM salesperson_totals

    WINDOW
        row_number_window AS (
            PARTITION BY department
            ORDER BY total_sales DESC, salesperson ASC
        ),

        rank_window AS (
            PARTITION BY department
            ORDER BY total_sales DESC
        )
)

SELECT
    department,
    salesperson,
    total_sales,
    row_number_rank,
    rank_rank,
    dense_rank_rank
FROM ranked_salespeople
ORDER BY
    department ASC,
    total_sales DESC,
    salesperson ASC;
```

Important lesson:
Use two named windows:
- row_number_window includes salesperson as a tie-breaker.
- rank_window does not include salesperson, because adding a unique tie-breaker would destroy tie behavior for RANK and DENSE_RANK.

Memory nugget:
Use one window for exact row position.
Use another window for tie-aware ranking.

### Exercise 11A — Exact third row per department
Business meaning:
Return exactly one third salesperson per department.

Filter:
`WHERE row_number_rank = 3`

Observed result meaning:
For Data Engineering, this returned Nora Diaz.

Why:
Nora is the exact third physical row after sorting by total_sales descending and salesperson ascending. But she is not competition rank 3. She is tied with Leah at rank 2.

### Exercise 11B — Competition rank 3
Business meaning:
Return everyone who holds competition rank 3.

Filter:
`WHERE rank_rank = 3`

Observed result:
Data Engineering returned no row.

Why:
Data Engineering ranks were:
Mila = 1
Leah = 2
Nora = 2
Evan = 4

Rank 3 was skipped because Leah and Nora tied at rank 2.

Nugget:
RANK can skip rank numbers.
So WHERE rank_rank = 3 may return no row for some departments.

### Exercise 11C — Third distinct sales tier
Business meaning:
Return everyone in the third distinct sales tier.

Filter:
`WHERE dense_rank_rank = 3`

Observed result:
For Data Engineering, this returned Evan Stone.

Why:
Distinct sales tiers were:
Tier 1: 260440.00 -> Mila Tran
Tier 2: 253536.00 -> Leah Kim and Nora Diaz
Tier 3: 250248.00 -> Evan Stone

### Final comparison table
| Filter used         | Business meaning          | Data Engineering result |
| ------------------- | ------------------------- | ----------------------- |
| row_number_rank = 3 | exact third row           | Nora Diaz               |
| rank_rank = 3       | competition rank 3        | no Data Engineering row |
| dense_rank_rank = 3 | third distinct sales tier | Evan Stone              |

### Interview translation
If the business asks for exactly one third salesperson, use ROW_NUMBER.

If the business wants everyone tied at third place, use RANK.

If the business wants the third distinct sales tier, use DENSE_RANK.

### Final memory nugget
ROW_NUMBER answers:
Which exact row is third?

RANK answers:
Who holds competition rank 3?

DENSE_RANK answers:
Who is in the third distinct value tier?

### SQL-order lesson
Sean tried to filter on row_number_rank in the same SELECT where alias was created. That failed because WHERE runs before SELECT aliases exist.

Correct pattern:
1. CTE 1: aggregate to salesperson totals.
2. CTE 2: calculate ranking columns.
3. Outer SELECT: filter on row_number_rank, rank_rank, or dense_rank_rank.

Nugget:
Window function result first goes into a CTE.
Then the outer query can filter it.

## Exercise 12 to 18 — LAG and LEAD row-to-row comparison

Context:
Sean moved from ranking functions into offset/fetching functions.

Main mental model:
- `LAG` = bring a value from a previous row into the current row.
- `LEAD` = bring a value from a future row into the current row.

Memory line:
LAG = rearview mirror.
LEAD = windshield.

Interview-safe sentence:
I use LAG and LEAD when I need row-to-row comparison. They let the current row see a previous or future row without doing a self-join.

### Exercise 12 — Previous sale in the same region

Prompt:
Using `sales_events`, show each sale with the previous sale revenue inside the same region.

Final SQL:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  LAG(revenue) OVER (
    PARTITION BY region
    ORDER BY sale_date, sale_id
  ) AS previous_region_revenue
FROM sales_events
ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Explain:
`PARTITION BY region` keeps each region separate.
`ORDER BY sale_date, sale_id` defines which row counts as previous.
The first row in each region has `NULL` because no previous row exists.

Memory nugget:
LAG does not summarize.
LAG copies a value from a previous row into the current row.

### LAG default value discussion

`LAG` can take a default:

```sql
LAG(revenue, 1, 0)
```

Meaning:
- `revenue` = value to fetch
- `1` = go back one row
- `0` = default when no previous row exists

In this training, `NULL` was preferred because `NULL` is truthful:
no previous row means no comparison can be calculated.

Memory nugget:
`NULL` is truthful.
Default `0` is convenient.
Use `0` only when the business meaning really is zero.

### Exercise 13 — Difference and percent change from previous sale

Prompt:
Calculate previous revenue, dollar change, and percent change.

Final SQL:
```sql
WITH sales_with_previous AS (
  SELECT
    sale_id,
    sale_date,
    region,
    revenue,
    LAG(revenue) OVER (
      PARTITION BY region
      ORDER BY sale_date, sale_id
    ) AS previous_region_revenue
  FROM sales_events
)

SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  previous_region_revenue,
  revenue - previous_region_revenue AS revenue_change,
  ROUND(
    100.0 * (revenue - previous_region_revenue)
    / NULLIF(previous_region_revenue, 0),
    2
  ) AS revenue_pct_change
FROM sales_with_previous
ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Explain:
`LAG` creates the previous value.
The outer `SELECT` calculates the change.
`NULLIF` protects against divide-by-zero.
The first row remains `NULL` because no previous comparison exists.

Correction note:
Sean first put `ORDER BY` and `LIMIT` inside the CTE.
The cleaner pattern is:
CTE calculates for all rows.
Outer query handles display, sorting, limiting, and filtering.

Memory nugget:
Calculate first.
Display/filter second.

### Exercise 14 — Direction label with CASE

Prompt:
Add a readable business label for movement.

Final SQL:
```sql
WITH sales_with_previous AS (
  SELECT
    sale_id,
    sale_date,
    region,
    revenue,
    LAG(revenue) OVER (
      PARTITION BY region
      ORDER BY sale_date, sale_id
    ) AS previous_region_revenue
  FROM sales_events
)

SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  previous_region_revenue,

  ROUND(
    100.0 * (revenue - previous_region_revenue)
    / NULLIF(previous_region_revenue, 0),
    2
  ) AS revenue_pct_change,

  CASE
    WHEN previous_region_revenue IS NULL THEN 'First sale in region'
    WHEN revenue > previous_region_revenue THEN 'Up'
    WHEN revenue < previous_region_revenue THEN 'Down'
    ELSE 'No change'
  END AS revenue_direction

FROM sales_with_previous
ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Explain:
LAG gives the old value.
Math gives the change.
CASE gives the meaning.

Memory nugget:
LAG gives the old value.
Math gives the change.
CASE gives the meaning.

### Exercise 15 — LEAD current row vs next row

Prompt:
Compare each sale to the next sale inside the same region.

Important correction:
Sean first reused `previous_region_revenue` as the alias while using `LEAD`.
That was confusing because `LEAD` fetches the next value, not the previous value.

Correct naming:
- `next_region_revenue`
- `next_revenue_change`
- `next_revenue_direction`

Final SQL:
```sql
WITH sales_with_next AS (
  SELECT
    sale_id,
    sale_date,
    region,
    revenue,
    LEAD(revenue) OVER (
      PARTITION BY region
      ORDER BY sale_date, sale_id
    ) AS next_region_revenue
  FROM sales_events
)

SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  next_region_revenue,

  next_region_revenue - revenue AS next_revenue_change,

  CASE
    WHEN next_region_revenue IS NULL THEN 'Last sale in region'
    WHEN next_region_revenue > revenue THEN 'Next is up'
    WHEN next_region_revenue < revenue THEN 'Next is down'
    ELSE 'No change'
  END AS next_revenue_direction

FROM sales_with_next
ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Explain:
`LAG` formula is current - previous.
`LEAD` formula is next - current.

Memory nugget:
LAG looks backward.
LEAD looks forward.

### Exercise 16 — Previous and next together

Prompt:
Use `LAG` and `LEAD` together so each row can see both neighbors.

Final SQL:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  LAG(revenue) OVER by_region AS previous_region_revenue,
  LEAD(revenue) OVER by_region AS next_region_revenue
FROM sales_events

WINDOW
  by_region AS (
    PARTITION BY region
    ORDER BY sale_date, sale_id
  )

ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Explain:
A named window is useful when `LAG` and `LEAD` use the same path.
Define the path once, then reuse it.

Memory nugget:
previous row <- current row -> next row

### Exercise 17 — Local peak and local valley

Prompt:
Use previous and next revenue to classify the current row.

Rules:
- If previous or next is `NULL`: Edge row
- If revenue is greater than both previous and next: Local peak
- If revenue is less than both previous and next: Local valley
- Otherwise: Middle

Final SQL:
```sql
WITH sales_with_compared AS (
  SELECT
    sale_id,
    sale_date,
    region,
    revenue,
    LAG(revenue) OVER by_region AS previous_region_revenue,
    LEAD(revenue) OVER by_region AS next_region_revenue
  FROM sales_events

  WINDOW
    by_region AS (
      PARTITION BY region
      ORDER BY sale_date, sale_id
    )
)

SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  previous_region_revenue,
  next_region_revenue,

  CASE
    WHEN next_region_revenue IS NULL
      OR previous_region_revenue IS NULL
      THEN 'Edge row'
    WHEN revenue > next_region_revenue
      AND revenue > previous_region_revenue
      THEN 'Local peak'
    WHEN revenue < next_region_revenue
      AND revenue < previous_region_revenue
      THEN 'Local valley'
    ELSE 'Middle'
  END AS local_shape

FROM sales_with_compared
ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Explain:
`LAG` gives the left neighbor.
`LEAD` gives the right neighbor.
`CASE` labels the shape of the current row.

Memory nugget:
LAG gives left neighbor.
LEAD gives right neighbor.
CASE gives the business label.

### Exercise 18 — Count local shapes by region

Prompt:
Summarize how many rows per region are Local peak, Local valley, Middle, and Edge row.

Final SQL:
```sql
WITH sales_with_compared AS (
  SELECT
    sale_id,
    sale_date,
    region,
    revenue,
    LAG(revenue) OVER by_region AS previous_region_revenue,
    LEAD(revenue) OVER by_region AS next_region_revenue
  FROM sales_events

  WINDOW
    by_region AS (
      PARTITION BY region
      ORDER BY sale_date, sale_id
    )
),

classified_sales AS (
  SELECT
    region,
    CASE
      WHEN next_region_revenue IS NULL
        OR previous_region_revenue IS NULL
        THEN 'Edge row'
      WHEN revenue > next_region_revenue
        AND revenue > previous_region_revenue
        THEN 'Local peak'
      WHEN revenue < next_region_revenue
        AND revenue < previous_region_revenue
        THEN 'Local valley'
      ELSE 'Middle'
    END AS local_shape
  FROM sales_with_compared
)

SELECT
  region,
  local_shape,
  COUNT(*) AS shape_count
FROM classified_sales
GROUP BY
  region,
  local_shape
ORDER BY
  region ASC,
  shape_count DESC;
```

Observed result:
Each region showed:
- Local peak: 35
- Local valley: 34
- Middle: 19
- Edge row: 2

Explain:
Each region has two edge rows:
first row has no previous row,
last row has no next row.

Important pattern:
row-level window analysis
-> CASE business label
-> GROUP BY summary

Memory nugget:
LAG/LEAD can classify each row.
Then GROUP BY can summarize the classifications.

### CTE chaining vs nested WITH

Sean asked:
Can you have a WITH within a WITH?

Answer:
PostgreSQL can nest `WITH` clauses, but normal training/interview SQL should prefer chained CTEs.

Preferred pattern:
```sql
WITH first_cte AS (...),
     second_cte AS (...),
     third_cte AS (...)
SELECT ...
FROM third_cte;
```

Memory nugget:
You can nest WITH,
but most training/interview SQL should chain CTEs instead.

### SQL order and placement notes from this cluster

- Window `ORDER BY` inside `OVER` defines row sequence for `LAG`/`LEAD`.
- Final `ORDER BY` controls display order.
- `ORDER BY` inside a CTE is usually unnecessary unless paired with `LIMIT` or used for a specific supported purpose.
- CTE 1 can calculate previous/next values.
- CTE 2 can classify rows.
- Final `SELECT` can summarize or filter.

### Final cluster summary
- `LAG` = previous row
- `LEAD` = next row
- `LAG`/`LEAD` are for row-to-row comparison
- Use CTEs when calculation needs to be reused
- Use `NULL` honestly for missing previous/next rows
- Use `NULLIF` for safe percent-change math
- Use `CASE` to turn numeric comparisons into business labels
- Use `GROUP BY` after classification to summarize patterns

## Exercise 19 to 20 — FIRST_VALUE and LAST_VALUE

Context:
Sean moved from `LAG`/`LEAD` into `FIRST_VALUE` and `LAST_VALUE`.

Mental model:
- `LAG` = previous row
- `LEAD` = next row
- `FIRST_VALUE` = first value in the ordered window
- `LAST_VALUE` = last visible value in the ordered window

Important trap:
`LAST_VALUE` without an explicit full frame often returns the current row's value, because the default frame usually ends at the current row.

Memory nugget:
`FIRST_VALUE` usually behaves as expected.
`LAST_VALUE` needs a full frame if you want the true last row in the partition.

### Exercise 19 — FIRST_VALUE and the LAST_VALUE default trap

Prompt:
Using `sales_events`, show:
- `sale_id`
- `sale_date`
- `region`
- `revenue`
- `first_region_revenue`
- `last_value_default`

Trap query:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,

  FIRST_VALUE(revenue) OVER by_region AS first_region_revenue,

  LAST_VALUE(revenue) OVER by_region AS last_value_default

FROM sales_events

WINDOW
  by_region AS (
    PARTITION BY region
    ORDER BY sale_date, sale_id
  )

ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Observed behavior:
For East rows:
- `first_region_revenue` stayed `673.00`
- `last_value_default` matched the current row revenue

Explain:
`FIRST_VALUE` shows the first value in the partition.
`LAST_VALUE` by default only sees from the first row through the current row.
So the last visible row is the current row.

Mental model:
- Default frame: first row -> current row
- Full frame: first row -> last row

### Exercise 19B — Correct LAST_VALUE with full frame

Final SQL:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,

  FIRST_VALUE(revenue) OVER by_region AS first_region_revenue,

  LAST_VALUE(revenue) OVER by_region AS last_value_default,

  LAST_VALUE(revenue) OVER by_region_full AS last_region_revenue

FROM sales_events

WINDOW
  by_region AS (
    PARTITION BY region
    ORDER BY sale_date, sale_id
  ),

  by_region_full AS (
    PARTITION BY region
    ORDER BY sale_date, sale_id
    ROWS BETWEEN UNBOUNDED PRECEDING
      AND UNBOUNDED FOLLOWING
  )

ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Observed behavior:
For East:
- `first_region_revenue = 673.00`
- `last_value_default = current row revenue`
- `last_region_revenue = 869.00`

Explain:
The full frame:

`ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`

lets `LAST_VALUE` see the whole partition, so it returns the true last regional revenue.

Interview-safe sentence:
`FIRST_VALUE` is straightforward, but `LAST_VALUE` has a common frame trap.
If I need the true last value in a partition, I explicitly use a full frame:
`ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.

### Exercise 20 — Compare each row to first and last region revenue

Prompt:
Use `FIRST_VALUE` and full-frame `LAST_VALUE` as benchmarks.
Show:
- `sale_id`
- `sale_date`
- `region`
- `revenue`
- `first_region_revenue`
- `last_region_revenue`
- `change_from_first`
- `change_to_last`

Final SQL:
```sql
WITH revenue_with_first_last AS (
  SELECT
    sale_id,
    sale_date,
    region,
    revenue,

    FIRST_VALUE(revenue) OVER by_region AS first_region_revenue,

    LAST_VALUE(revenue) OVER by_region_full AS last_region_revenue

  FROM sales_events

  WINDOW
    by_region AS (
      PARTITION BY region
      ORDER BY sale_date, sale_id
    ),

    by_region_full AS (
      PARTITION BY region
      ORDER BY sale_date, sale_id
      ROWS BETWEEN UNBOUNDED PRECEDING
        AND UNBOUNDED FOLLOWING
    )
)

SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  first_region_revenue,
  last_region_revenue,
  revenue - first_region_revenue AS change_from_first,
  last_region_revenue - revenue AS change_to_last
FROM revenue_with_first_last
ORDER BY
  region ASC,
  sale_date ASC,
  sale_id ASC
LIMIT 10;
```

Correction note:
Sean initially put a semicolon before `ORDER BY` in the outer query:

`FROM revenue_with_first_last ;`
`ORDER BY ...`

That ended the statement too early.

Correct rule:
Only one semicolon goes at the very end of the full query.

Observed East example:
- `first_region_revenue = 673.00`
- `last_region_revenue = 869.00`

For `sale_id 123`:
- `revenue = 1093.00`
- `change_from_first = 1093 - 673 = 420`
- `change_to_last = 869 - 1093 = -224`

Memory nugget:
`FIRST_VALUE` gives the starting benchmark.
`LAST_VALUE` with full frame gives the ending benchmark.
The outer `SELECT` compares each row to those benchmarks.

### SQL order / frame notes

- `ORDER BY` inside `OVER` defines row sequence for `FIRST_VALUE`/`LAST_VALUE`.
- The frame controls how many rows the function can see.
- Default frame often ends at the current row.
- Full frame uses `UNBOUNDED FOLLOWING` to reach the partition end.
- Final `ORDER BY` controls display only.
- Semicolon ends the whole SQL statement; do not place it before `ORDER BY`.

### Final cluster summary
- `FIRST_VALUE` gets the first ordered value in the partition.
- `LAST_VALUE` default can be misleading.
- Use full frame for true last value.
- Use CTE when comparing current row to first/last benchmarks.
- Put semicolon only at the end.

## Exercise 21 to 28 — Window frames and moving calculations

Context:
Sean moved from `FIRST_VALUE`/`LAST_VALUE` frame behavior into practical window frames for moving averages, moving totals, rolling max/min, forward-looking frames, centered frames, and previous-only benchmarks.

Main mental model:
A frame tells a window function which nearby rows are visible for the current row.

Core explanation:
- `PARTITION BY` chooses the group.
- `ORDER BY` lines rows up inside the group.
- `ROWS BETWEEN ...` defines which part of the line the current row can see.

Examples:
- `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`
  means previous 2 rows plus current row.
- `ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING`
  means current row plus next row.
- `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING`
  means previous row, current row, and next row.
- `ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING`
  means previous 3 rows only, excluding the current row.

Memory nugget:
Frame chooses the rows.
Function chooses the calculation.

### Exercise 21 — 3-sale moving average by region

Prompt:
Using `sales_events`, show a moving average of revenue using the current sale and previous 2 sales in the same region.

Final SQL:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  ROUND(
    AVG(revenue) OVER (
      PARTITION BY region
      ORDER BY sale_date, sale_id
      ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ),
    2
  ) AS moving_avg_3_sales
FROM sales_events
ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Observed explanation:
For East:
- Row 1 average uses only row 1.
- Row 2 average uses rows 1 and 2.
- Row 3 average uses rows 1, 2, and 3.
- Row 4 average drops row 1 and uses rows 2, 3, and 4.

Memory nugget:
`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`
= a rolling 3-row window.

### Exercise 22 — 3-sale moving total

Prompt:
Same frame, but use `SUM` instead of `AVG`.

Final SQL:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  SUM(revenue) OVER (
    PARTITION BY region
    ORDER BY sale_date, sale_id
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS moving_total_3_sales
FROM sales_events
ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Explain:
`AVG` + frame = moving average.
`SUM` + frame = moving total.

Memory nugget:
Do not call a `SUM` moving total by an average alias.
Use clear names like `moving_total_3_sales`.

### Exercise 23 — Moving average and moving total together

Prompt:
Use a named window/frame and reuse it for `AVG` and `SUM`.

Final SQL:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  ROUND(AVG(revenue) OVER trailing_3_sales, 2) AS moving_avg_3_sales,
  SUM(revenue) OVER trailing_3_sales AS moving_total_3_sales
FROM sales_events

WINDOW
  trailing_3_sales AS (
    PARTITION BY region
    ORDER BY sale_date, sale_id
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  )

ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Explain:
The named frame defines which rows are visible.
`AVG` and `SUM` decide what calculation to do over those visible rows.

Memory nugget:
Same frame, different aggregate:
`AVG` = moving average
`SUM` = moving total
`MAX` = rolling max
`MIN` = rolling min

### Exercise 24 — Rolling max and rolling min

Prompt:
Use the same `trailing_3_sales` frame with `MAX` and `MIN`.

Final SQL:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  MAX(revenue) OVER trailing_3_sales AS rolling_max_3_sales,
  MIN(revenue) OVER trailing_3_sales AS rolling_min_3_sales
FROM sales_events

WINDOW
  trailing_3_sales AS (
    PARTITION BY region
    ORDER BY sale_date, sale_id
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  )

ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Explain:
`MAX` finds the highest revenue among current row plus previous 2 rows.
`MIN` finds the lowest revenue among current row plus previous 2 rows.

Memory nugget:
Frame chooses the rows.
`MAX`/`MIN` choose the extreme value inside that frame.

### Exercise 25 — Forward-looking frame

Prompt:
Show the highest revenue between current row and next row.

Final SQL:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  MAX(revenue) OVER current_and_next_sale AS max_current_or_next_revenue
FROM sales_events

WINDOW
  current_and_next_sale AS (
    PARTITION BY region
    ORDER BY sale_date, sale_id
    ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING
  )

ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Explain:
`CURRENT ROW AND 1 FOLLOWING` means the current sale and the next sale.
Use `FOLLOWING` when the benchmark looks forward.

Memory nugget:
`PRECEDING` looks backward.
`FOLLOWING` looks forward.
`CURRENT ROW` anchors the frame.

### Exercise 26 — Centered 3-sale moving average

Prompt:
Average previous row, current row, and next row.

Final SQL:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  ROUND(AVG(revenue) OVER centered_3_sales, 2) AS centered_avg_3_sales
FROM sales_events

WINDOW
  centered_3_sales AS (
    PARTITION BY region
    ORDER BY sale_date, sale_id
    ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
  )

ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Explain:
This is a centered frame:
previous row + current row + next row.
At the first row, there is no previous row, so the frame is smaller.

Memory nugget:
Trailing frame = previous rows + current row.
Forward frame = current row + future rows.
Centered frame = previous + current + future.

### Exercise 27 — Previous-only frame, excluding current row

Prompt:
Calculate the average revenue of the previous 3 sales only.

Final SQL:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  ROUND(AVG(revenue) OVER prev_sales_win, 2) AS avg_previous_3_sales
FROM sales_events

WINDOW
  prev_sales_win AS (
    PARTITION BY region
    ORDER BY sale_date, sale_id
    ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
  )

ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Explain:
This frame looks only backward and excludes the current row.
The first row has `NULL` because there are no prior rows.
The second row has one prior row available.
The third row has two prior rows available.
The fourth row onward has up to three prior rows.

Memory nugget:
Use a previous-only frame when the current row should be judged
against history, not included in its own benchmark.

Side discussion:
Weighted moving averages are realistic.
They give more weight to recent values and less weight to older values.
They are used in sales forecasting, stock prices, CPU/memory trend smoothing,
latency monitoring, capacity planning, demand forecasting, and risk signals.

Plain-English explanation:
A normal moving average treats each point equally.
A weighted moving average gives more importance to recent points,
making the trend more responsive while still smoothing noise.

Sean insight:
For complex feature engineering such as weighted moving averages,
exponential smoothing, and many model-ready time-series features,
Pandas or Spark is often cleaner than SQL.
SQL can express these ideas, but the query becomes clunky.

Interview-safe sentence:
SQL is strong for basic moving windows and aggregation.
For richer feature engineering, I would usually move to Pandas or Spark,
especially when preparing model-ready time-series features.

### Exercise 28 — Compare current revenue to previous-3 average

Prompt:
Use previous-only average as a benchmark and label current revenue.

Final SQL:
```sql
WITH sales_with_previous_avg AS (
  SELECT
    sale_id,
    sale_date,
    region,
    revenue,
    ROUND(AVG(revenue) OVER prev_sales_win, 2) AS avg_previous_3_sales
  FROM sales_events

  WINDOW
    prev_sales_win AS (
      PARTITION BY region
      ORDER BY sale_date, sale_id
      ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
    )
)

SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  avg_previous_3_sales,
  CASE
    WHEN avg_previous_3_sales IS NULL THEN 'No prior benchmark'
    WHEN revenue > avg_previous_3_sales THEN 'Above previous avg'
    WHEN revenue < avg_previous_3_sales THEN 'Below previous avg'
    ELSE 'Equal to previous avg'
  END AS vs_previous_3_avg
FROM sales_with_previous_avg
ORDER BY
  region,
  sale_date,
  sale_id
LIMIT 20;
```

Explain:
The CTE calculates a benchmark from prior rows.
The outer query compares current revenue to that benchmark.
`CASE` turns the comparison into a readable label.

Memory nugget:
Window frame creates the benchmark.
`CASE` labels each row.
`GROUP BY` can summarize the labels.

### Exercise 28B — Summarize above/below by region

Prompt:
Count how many sales per region are above or below the previous-3 average.

Final SQL:
```sql
WITH sales_with_previous_avg AS (
  SELECT
    sale_id,
    sale_date,
    region,
    revenue,
    ROUND(AVG(revenue) OVER prev_sales_win, 2) AS avg_previous_3_sales
  FROM sales_events

  WINDOW
    prev_sales_win AS (
      PARTITION BY region
      ORDER BY sale_date, sale_id
      ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
    )
),

above_below AS (
  SELECT
    sale_id,
    sale_date,
    region,
    revenue,
    avg_previous_3_sales,
    CASE
      WHEN avg_previous_3_sales IS NULL THEN 'No prior benchmark'
      WHEN revenue > avg_previous_3_sales THEN 'Above previous avg'
      WHEN revenue < avg_previous_3_sales THEN 'Below previous avg'
      ELSE 'Equal to previous avg'
    END AS vs_previous_3_avg
  FROM sales_with_previous_avg
)

SELECT
  region,
  vs_previous_3_avg,
  COUNT(*) AS row_count
FROM above_below
GROUP BY
  region,
  vs_previous_3_avg
ORDER BY
  region ASC,
  row_count DESC;
```

Observed result summary:
Each region had one `No prior benchmark` row because only the first row has no previous rows in the previous-only frame.

Pattern:
window frame benchmark
-> `CASE` classification
-> `GROUP BY` summary

### ROWS vs RANGE

Context:
Sean compared `ROWS` and `RANGE` using `sale_date`, where each date had multiple sales.

Query:
```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,

  SUM(revenue) OVER (
    PARTITION BY region
    ORDER BY sale_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total_rows,

  SUM(revenue) OVER (
    PARTITION BY region
    ORDER BY sale_date
    RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total_range

FROM sales_events
WHERE region = 'East'
ORDER BY
  sale_date,
  sale_id
LIMIT 20;
```

Observed lesson:
`ROWS` climbed row by row.
`RANGE` jumped by all rows sharing the same `sale_date` because `ORDER BY sale_date` created peer groups.

Example:
For `2026-01-03`, East had revenues `673`, `1093`, and `638`.
`ROWS` produced `673`, `1766`, `2404`.
`RANGE` produced `2404` on all three rows.

Important warning:
The window `ORDER BY` was only `sale_date`, but the final display `ORDER BY` was `sale_date, sale_id`.
For rows with the same `sale_date`, the `ROWS` calculation was not fully deterministic.
To make `ROWS` stable, include `sale_id` in the window `ORDER BY`.

Memory nugget:
`ROWS` = physical row movement.
`RANGE` = value-peer movement.

For moving averages/totals:
prefer `ROWS`.

For date-level cumulative totals:
`RANGE` can be useful, but only when peer grouping is intentional.

## Exercise 29 to 35 — NTILE vs percentile_cont / P95

Context:
Sean moved from frames to buckets and percentiles.

Key distinction:
`NTILE` labels rows into buckets.
`percentile_cont` calculates an actual cutoff value.

Layman explanation:

`NTILE`:
Imagine students lined up by score.
`NTILE(4)` splits the line into 4 roughly equal groups.
It gives each row a bucket number.
It does not tell you the exact score cutoff.

P95 / percentile:
P95 asks:
What value separates the lower 95% from the top 5%?
It returns an actual threshold value.

Memory line:
`NTILE` is a bucket label.
P95 is a cutoff value.

### Exercise 29 — Revenue quartiles by region

Prompt:
For each region, split sales into 4 revenue buckets from highest revenue to lowest revenue.

Final SQL:
```sql
SELECT
  sale_id,
  region,
  salesperson,
  revenue,
  NTILE(4) OVER (
    PARTITION BY region
    ORDER BY revenue DESC
  ) AS revenue_quartile
FROM sales_events
ORDER BY
  region,
  revenue_quartile,
  revenue DESC
LIMIT 40;
```

Explain:
Quartile 1 = highest revenue bucket.
Quartile 4 = lowest revenue bucket.
If a region has 90 rows, `NTILE(4)` creates approximately equal buckets:
`23, 23, 22, 22`.

Memory nugget:
`NTILE` labels rows into buckets.
It does not calculate the actual percentile cutoff value.

### Exercise 30 — Count rows per quartile

Prompt:
Summarize each region/quartile with count, min revenue, and max revenue.

Final SQL:
```sql
WITH revenue_buckets AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,
    NTILE(4) OVER (
      PARTITION BY region
      ORDER BY revenue DESC
    ) AS revenue_quartile
  FROM sales_events
)

SELECT
  region,
  revenue_quartile,
  COUNT(*) AS quartile_row_count,
  MIN(revenue) AS min_revenue_in_quartile,
  MAX(revenue) AS max_revenue_in_quartile
FROM revenue_buckets
GROUP BY
  region,
  revenue_quartile
ORDER BY
  region ASC,
  revenue_quartile ASC;
```

Explain:
`NTILE` assigns the bucket on each row.
`GROUP BY` summarizes the bucket labels into one row per region/quartile.

Memory nugget:
Window first to label rows.
`GROUP BY` second to summarize the labels.

### Exercise 31 — Label the quartiles

Context:
Sean first tried to use `COUNT`/`MIN`/`MAX` as window functions, partitioned only by region, which repeated region-wide values on every row.

Mistake:
`COUNT(*) OVER (PARTITION BY region)` kept all row details and counted all rows in the region.
For this task, one row per region/quartile was needed, so `GROUP BY` was the right tool.

Correct final SQL:
```sql
WITH revenue_buckets AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,
    NTILE(4) OVER (
      PARTITION BY region
      ORDER BY revenue DESC
    ) AS revenue_quartile
  FROM sales_events
)

SELECT
  region,
  revenue_quartile,

  CASE
    WHEN revenue_quartile = 1 THEN 'Top revenue bucket'
    WHEN revenue_quartile = 2 THEN 'Upper-middle revenue bucket'
    WHEN revenue_quartile = 3 THEN 'Lower-middle revenue bucket'
    ELSE 'Lowest revenue bucket'
  END AS quartile_label,

  COUNT(*) AS quartile_row_count,
  MIN(revenue) AS min_revenue_in_quartile,
  MAX(revenue) AS max_revenue_in_quartile

FROM revenue_buckets
GROUP BY
  region,
  revenue_quartile
ORDER BY
  region ASC,
  revenue_quartile ASC;
```

Observed result:
East quartile 1: 23 rows, 1273 to 2000
East quartile 2: 23 rows, 1085 to 1269
East quartile 3: 22 rows, 853 to 1034
East quartile 4: 22 rows, 417 to 845

Memory nugget:
Use window functions when you want to keep row detail.
Use `GROUP BY` when you want one summary row per group.

Another nugget:
Bucket rows with `NTILE`.
Summarize buckets with `GROUP BY`.

### Exercise 32 — Top bucket only

Prompt:
Show all sales in quartile 1 only.

Final SQL:
```sql
WITH revenue_buckets AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,
    NTILE(4) OVER (
      PARTITION BY region
      ORDER BY revenue DESC
    ) AS revenue_quartile
  FROM sales_events
)

SELECT
  sale_id,
  region,
  salesperson,
  revenue,
  revenue_quartile
FROM revenue_buckets
WHERE revenue_quartile = 1
ORDER BY
  region ASC,
  revenue DESC,
  sale_id ASC
LIMIT 40;
```

Explain:
Window function creates the analytic label in a CTE.
Outer query filters the analytic label.

Memory nugget:
`NTILE` labels the rows.
Outer `WHERE` selects the bucket.

### Layman difference between NTILE and P95

`NTILE` answers:
Which bucket is this row in?

P95 answers:
What is the cutoff value?

For sales:
`NTILE(10)` splits sales into 10 groups.
P95 calculates the revenue value where about 95% of sales are below it.

For observability:
`NTILE` can bucket requests.
P95 latency is the actual latency threshold, such as `420 ms`, that 95% of requests are under.

Memory nugget:
`NTILE` = bucket label.
P95 = cutoff value.

### Is NTILE(10) bucket 10 the same as P90 or above?

Answer:
It is roughly similar, but not exactly.

If ordered ascending:
`NTILE(10)` bucket 10 = top 10% of rows.
P90 = the value cutoff for the top 10%.

They are close ideas, but not identical because:
- `NTILE` is row-count based.
- Percentile is value-threshold based.
- Ties can make them differ.

If ordered descending:
bucket numbers reverse.
Bucket 1 becomes the highest 10%.

Memory nugget:
`NTILE(10)` bucket 10 = top tenth of rows when ordered ascending.
P90 = value cutoff for the top tenth.

### Exercise 33 — P95 revenue by region

Prompt:
Find the 95th percentile revenue per region.

Final SQL:
```sql
SELECT
  region,
  ROUND(
    percentile_cont(0.95) WITHIN GROUP (
      ORDER BY revenue
    )::numeric,
    2
  ) AS p95_revenue
FROM sales_events
GROUP BY region
ORDER BY region;
```

Observed result:
East = 1500.00
North = 1531.80
South = 1499.65
West = 1458.25

Explain:
This calculates one P95 cutoff value per region group.
It is not row-by-row.
`GROUP BY region` creates one group per region.
`percentile_cont` sorts the revenue values inside each group and calculates the 95th percentile cutoff.

Important syntax explanation:
`percentile_cont(0.95) WITHIN GROUP (ORDER BY revenue)`
is an ordered-set aggregate.
`WITHIN GROUP` means:
sort the values inside the aggregate calculation.

This is different from `OVER`:
`OVER` keeps rows visible and adds analytic values to each row.
`WITHIN GROUP` calculates one ordered aggregate value for a group.

Memory nugget:
`OVER` keeps rows visible.
`GROUP BY` collapses rows.
`WITHIN GROUP` sorts values inside an aggregate calculation.

Another memory nugget:
`percentile_cont` gives the group's cutoff value.
It does not label each individual row unless we join that cutoff back to the detail rows.

Plain reminder:
OVER keeps rows visible.
GROUP BY collapses rows.

### Why percentile_cont does not use OVER here

Explain:
`SUM(...) OVER (...)` is a window calculation that keeps every sale row visible.

`percentile_cont(0.95) WITHIN GROUP (ORDER BY revenue)`
is being used as a group-level aggregate. The `ORDER BY` is used to sort revenue values to calculate the percentile, not to create a row-by-row journey.

Comparison:
`NTILE` uses `OVER` because it labels each row.
`percentile_cont` uses `WITHIN GROUP` because it calculates one cutoff value.

### Exercise 34 — NTILE(100) issue with only 90 rows

Context:
Sean tried `NTILE(100)` per region and filtered for bucket 100.
It returned zero rows.

Explain why:
Each region had only 90 rows.
`NTILE(100)` could not populate 100 buckets from only 90 rows.
So bucket 100 did not exist.

Memory nugget:
`NTILE(100)` needs enough rows to populate 100 buckets.
With only 90 rows, bucket 100 may not exist.

Corrected practical exercise:
Use `NTILE(10)` for deciles.

Final SQL:
```sql
WITH revenue_deciles AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,
    NTILE(10) OVER (
      PARTITION BY region
      ORDER BY revenue ASC
    ) AS revenue_decile
  FROM sales_events
)

SELECT
  sale_id,
  region,
  salesperson,
  revenue,
  revenue_decile
FROM revenue_deciles
WHERE revenue_decile = 10
ORDER BY
  region ASC,
  revenue DESC,
  sale_id ASC;
```

Observed result:
Each region had 90 rows, so `NTILE(10)` created 9 rows per decile.
The result returned 36 rows:
`4 regions * 9 top-decile rows`.

Explain:
This gives the top decile bucket, not exact P95.

### Exercise 35 — Flag rows at or above P95

Prompt:
Calculate P95 per region, join it back to each sale row, and flag rows at or above the threshold.

Final SQL:
```sql
WITH region_p95 AS (
  SELECT
    region,
    ROUND(
      percentile_cont(0.95) WITHIN GROUP (
        ORDER BY revenue
      )::numeric,
      2
    ) AS p95_revenue
  FROM sales_events
  GROUP BY region
)

SELECT
  s.sale_id,
  s.region,
  s.salesperson,
  s.revenue,
  p.p95_revenue,

  CASE
    WHEN s.revenue >= p.p95_revenue THEN 'At or above P95'
    ELSE 'Below P95'
  END AS p95_flag

FROM sales_events AS s
INNER JOIN region_p95 AS p
  ON s.region = p.region

ORDER BY
  s.region ASC,
  s.revenue DESC,
  s.sale_id ASC
LIMIT 40;
```

Observed East behavior:
`p95_revenue = 1500.00`

Rows `2000, 1800, 1800, 1600, 1500, 1500` were `At or above P95`.
Rows below `1500` were `Below P95`.

Explain:
Percentile query gives the threshold.
Join attaches the threshold to each detail row.
`CASE` labels the row.

Memory nugget:
Percentile gives the cutoff.
Join attaches the cutoff.
`CASE` labels the row.

### Final section: Cluster summary

- Window frames define visible rows around the current row.
- `ROWS` is usually best for moving calculations.
- `RANGE` groups peers by `ORDER BY` value and can jump by duplicate dates.
- `NTILE` labels rows into buckets.
- `NTILE` is row-count based.
- `percentile_cont` calculates an actual cutoff value.
- P95 is a threshold, not a row label.
- `WITHIN GROUP` sorts values inside an aggregate calculation.
- To label rows by P95, calculate the threshold first, join it back, then use `CASE`.
- For complex weighted moving averages and richer feature engineering,
  Pandas or Spark can be cleaner than SQL.

## Exercise 36 to 42 — CUME_DIST, PERCENT_RANK, and P95 comparison

Purpose:
Document the training cluster where Sean learned how `CUME_DIST`,
`PERCENT_RANK`, `P95`, and `NTILE` relate to percentile-style business flags.

Core mental model:

`NTILE`:
Puts rows into buckets.

`percentile_cont` / `P95`:
Calculates an actual cutoff value for the group.

`CUME_DIST`:
For the current value, tells what fraction of rows are at or below it.

`PERCENT_RANK`:
Tells where the current value's rank starts on the ranking ladder.

Memory nuggets:
- `CUME_DIST` = percent of rows covered so far.
- `PERCENT_RANK` = percent rank position.
- `CUME_DIST` is coverage-based.
- `PERCENT_RANK` is rank-start based.
- `P95` gives a cutoff value.
- `CUME_DIST` flags by row position.
- `P95` flags by cutoff value.
- When methods agree, confidence goes up.
- When methods disagree, investigate ties, row counts, and business definition.

### Exercise 36 — CUME_DIST and PERCENT_RANK by region

Explain:
Sean calculated each sale's relative revenue position inside its region.

Final SQL:
```sql
WITH revenue_positions AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,

    CUME_DIST() OVER (
      PARTITION BY region
      ORDER BY revenue ASC
    ) AS revenue_cume_dist,

    PERCENT_RANK() OVER (
      PARTITION BY region
      ORDER BY revenue ASC
    ) AS revenue_percent_rank

  FROM sales_events
)

SELECT
  sale_id,
  region,
  salesperson,
  revenue,
  ROUND(revenue_cume_dist::numeric, 4) AS revenue_cume_dist,
  ROUND(revenue_percent_rank::numeric, 4) AS revenue_percent_rank
FROM revenue_positions
ORDER BY
  region ASC,
  revenue DESC,
  sale_id ASC
LIMIT 40;
```

Layman explanation:
SQL orders revenue from low to high inside each region.
The final display shows high to low, so the top visible rows have values
near `1.0000`.

`CUME_DIST` asks:
What percent of rows are at or below this value?

`PERCENT_RANK` asks:
How far up the ranking ladder does this value start?

Observed East examples:
- revenue `2000` had `CUME_DIST 1.0000` and `PERCENT_RANK 1.0000`.
- revenue `1500` had `CUME_DIST 0.9556` but `PERCENT_RANK 0.9438`.
- revenue `1800` ties shared the same values.

Important explanation:
`CUME_DIST` counts through the end of a tie group.
`PERCENT_RANK` uses where the tie group starts.

### Exercise 37 — Flag top 5% using CUME_DIST

Final SQL:
```sql
WITH revenue_positions AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,

    CUME_DIST() OVER (
      PARTITION BY region
      ORDER BY revenue ASC
    ) AS revenue_cume_dist

  FROM sales_events
)

SELECT
  sale_id,
  region,
  salesperson,
  revenue,
  ROUND(revenue_cume_dist::numeric, 4) AS revenue_cume_dist,

  CASE
    WHEN revenue_cume_dist >= 0.95 THEN 'Top 5%'
    ELSE 'Below top 5%'
  END AS revenue_band

FROM revenue_positions
ORDER BY
  region ASC,
  revenue DESC,
  sale_id ASC
LIMIT 40;
```

Observed East result:
Rows `2000`, `1800`, `1800`, `1600`, `1500`, `1500` were marked `Top 5%`.
The `1449` row was `Below top 5%`.

Explain:
East had `90` rows.
A pure `5%` would be `4.5` rows, but tied boundary behavior included both
`1500` rows, so East had `6` `Top 5%` rows.

Memory nugget:
`CUME_DIST` gives row position.
`CASE` turns position into a business band.

### Exercise 38 — Summarize CUME_DIST top-5 bands by region

Final SQL:
```sql
WITH revenue_positions AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,

    CUME_DIST() OVER (
      PARTITION BY region
      ORDER BY revenue ASC
    ) AS revenue_cume_dist

  FROM sales_events
),

revenue_bands AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,
    ROUND(revenue_cume_dist::numeric, 4) AS revenue_cume_dist,

    CASE
      WHEN revenue_cume_dist >= 0.95 THEN 'Top 5%'
      ELSE 'Below top 5%'
    END AS revenue_band

  FROM revenue_positions
)

SELECT
  region,
  revenue_band,
  COUNT(*) AS row_count
FROM revenue_bands
GROUP BY
  region,
  revenue_band
ORDER BY
  region ASC,
  row_count DESC;
```

Observed result:
East:
- `Below top 5% = 84`
- `Top 5% = 6`

North/South/West:
- `Below top 5% = 85`
- `Top 5% = 5`

Memory nugget:
`CUME_DIST` finds percentile-like position.
`CASE` creates the band.
`GROUP BY` counts the band.

### Exercise 39 — Compare CUME_DIST top-5 flag to P95 flag

Final SQL:
```sql
WITH revenue_positions AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,

    CUME_DIST() OVER (
      PARTITION BY region
      ORDER BY revenue ASC
    ) AS revenue_cume_dist

  FROM sales_events
),

region_p95 AS (
  SELECT
    region,
    ROUND(
      percentile_cont(0.95) WITHIN GROUP (
        ORDER BY revenue
      )::numeric,
      2
    ) AS p95_revenue
  FROM sales_events
  GROUP BY region
)

SELECT
  rp.sale_id,
  rp.region,
  rp.salesperson,
  rp.revenue,
  ROUND(rp.revenue_cume_dist::numeric, 4) AS revenue_cume_dist,

  CASE
    WHEN rp.revenue_cume_dist >= 0.95 THEN 'Top 5%'
    ELSE 'Below top 5%'
  END AS cume_dist_band,

  p.p95_revenue,

  CASE
    WHEN rp.revenue >= p.p95_revenue THEN 'At or above P95'
    ELSE 'Below P95'
  END AS p95_band

FROM revenue_positions AS rp
INNER JOIN region_p95 AS p
  ON rp.region = p.region

ORDER BY
  rp.region ASC,
  rp.revenue DESC,
  rp.sale_id ASC
LIMIT 40;
```

Observed East result:
`CUME_DIST` and `P95` agreed.
Revenue `1500` and above was `Top 5% / At or above P95`.
Revenue `1449` and below was `Below top 5% / Below P95`.

Memory nugget:
`CUME_DIST` flags by row position.
`P95` flags by cutoff value.

### Exercise 40 — Find rows where CUME_DIST and P95 disagree

Final SQL:
```sql
WITH revenue_positions AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,

    CUME_DIST() OVER (
      PARTITION BY region
      ORDER BY revenue ASC
    ) AS revenue_cume_dist

  FROM sales_events
),

region_p95 AS (
  SELECT
    region,
    ROUND(
      percentile_cont(0.95) WITHIN GROUP (
        ORDER BY revenue
      )::numeric,
      2
    ) AS p95_revenue
  FROM sales_events
  GROUP BY region
),

compare_methods AS (
  SELECT
    rp.sale_id,
    rp.region,
    rp.salesperson,
    rp.revenue,
    ROUND(rp.revenue_cume_dist::numeric, 4) AS revenue_cume_dist,

    CASE
      WHEN rp.revenue_cume_dist >= 0.95 THEN 'Top 5%'
      ELSE 'Below top 5%'
    END AS cume_dist_band,

    p.p95_revenue,

    CASE
      WHEN rp.revenue >= p.p95_revenue THEN 'At or above P95'
      ELSE 'Below P95'
    END AS p95_band

  FROM revenue_positions AS rp
  INNER JOIN region_p95 AS p
    ON rp.region = p.region
)

SELECT
  sale_id,
  region,
  salesperson,
  revenue,
  revenue_cume_dist,
  cume_dist_band,
  p95_revenue,
  p95_band
FROM compare_methods
WHERE
  (
    cume_dist_band = 'Top 5%'
    AND p95_band = 'Below P95'
  )
  OR
  (
    cume_dist_band = 'Below top 5%'
    AND p95_band = 'At or above P95'
  )
ORDER BY
  region ASC,
  revenue DESC,
  sale_id ASC;
```

Observed result:
`0 rows`.

Explain:
A zero-row disagreement query is not a failure.
It means both rules produced the same classification on this dataset.

Memory nugget:
Build method A.
Build method B.
Compare them.
If disagreements are zero, the methods agree.
If disagreements exist, inspect boundary ties, row counts, and business rule.

### Exercise 40B — Summarize method agreement

Final SELECT over the same `compare_methods` CTE:

```sql
SELECT
  cume_dist_band,
  p95_band,
  COUNT(*) AS row_count
FROM compare_methods
GROUP BY
  cume_dist_band,
  p95_band
ORDER BY
  row_count DESC;
```

Observed result:
- `Below top 5% + Below P95 = 339`
- `Top 5% + At or above P95 = 21`

Explain:
Total rows = `360`.
There were no mixed-label rows.
`CUME_DIST` and `P95` agreed across the whole dataset.

### Exercise 41 — Flag and summarize top rank-zone rows using PERCENT_RANK

Final SQL:
```sql
WITH revenue_percent_ranks AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,

    PERCENT_RANK() OVER (
      PARTITION BY region
      ORDER BY revenue ASC
    ) AS revenue_percent_rank

  FROM sales_events
),

revenue_rank_bands AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,
    revenue_percent_rank,

    CASE
      WHEN revenue_percent_rank >= 0.95 THEN 'Top rank zone'
      ELSE 'Below top rank zone'
    END AS percent_rank_band

  FROM revenue_percent_ranks
)

SELECT
  region,
  percent_rank_band,
  COUNT(*) AS row_count
FROM revenue_rank_bands
GROUP BY
  region,
  percent_rank_band
ORDER BY
  region ASC,
  row_count DESC;
```

Observed result:
East:
- `Below top rank zone = 86`
- `Top rank zone = 4`

North/South/West:
- `Below top rank zone = 85`
- `Top rank zone = 5`

Explain:
East differed because the `1500` tie group had `PERCENT_RANK 0.9438`.
That is below `0.95`, so those rows were excluded from `Top rank zone`.

Memory nugget:
`CUME_DIST` sees how much of the group is covered after this value.
`PERCENT_RANK` sees where this value starts on the ranking ladder.

### Exercise 42 — Count top rows by all three methods

Final SQL:
```sql
WITH revenue_positions AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,

    CUME_DIST() OVER (
      PARTITION BY region
      ORDER BY revenue ASC
    ) AS revenue_cume_dist,

    PERCENT_RANK() OVER (
      PARTITION BY region
      ORDER BY revenue ASC
    ) AS revenue_percent_rank

  FROM sales_events
),

region_p95 AS (
  SELECT
    region,
    ROUND(
      percentile_cont(0.95) WITHIN GROUP (
        ORDER BY revenue
      )::numeric,
      2
    ) AS p95_revenue
  FROM sales_events
  GROUP BY region
),

method_flags AS (
  SELECT
    rp.sale_id,
    rp.region,
    rp.salesperson,
    rp.revenue,
    rp.revenue_cume_dist,
    rp.revenue_percent_rank,
    p.p95_revenue,

    CASE
      WHEN rp.revenue_cume_dist >= 0.95 THEN 1
      ELSE 0
    END AS is_cume_dist_top,

    CASE
      WHEN rp.revenue >= p.p95_revenue THEN 1
      ELSE 0
    END AS is_p95_top,

    CASE
      WHEN rp.revenue_percent_rank >= 0.95 THEN 1
      ELSE 0
    END AS is_percent_rank_top

  FROM revenue_positions AS rp
  INNER JOIN region_p95 AS p
    ON rp.region = p.region
)

SELECT
  region,
  SUM(is_cume_dist_top) AS cume_dist_top_count,
  SUM(is_p95_top) AS p95_top_count,
  SUM(is_percent_rank_top) AS percent_rank_top_count,
  COUNT(*) AS total_rows
FROM method_flags
GROUP BY region
ORDER BY region ASC;
```

Observed result:
East:
- `CUME_DIST top count = 6`
- `P95 top count = 6`
- `PERCENT_RANK top count = 4`
- `total rows = 90`

North/South/West:
- all three methods count = `5`
- `total rows = 90` each

Explain:
`CUME_DIST` and `P95` behaved like percentile cutoff tools.
`PERCENT_RANK` behaved like rank-position progress.
East exposed the difference because of tied values at the boundary.

Interview-safe summary:
I compared three ways to mark top revenue rows:
`CUME_DIST`, `P95` threshold, and `PERCENT_RANK`.
`CUME_DIST` and `P95` agreed in this dataset.
`PERCENT_RANK` differed in East because of tied values at the boundary.
That showed why ties and business definition matter when choosing a
percentile-style method.

Final cluster summary:
- `P95` gives the percentile cutoff value.
- `CUME_DIST` gives row-level percentile-like coverage.
- `PERCENT_RANK` gives rank-position progress.
- `NTILE` creates rough buckets.
- `CUME_DIST` and `P95` are usually more intuitive for top-percent flags.
- `PERCENT_RANK` is useful, but can be less intuitive around tied boundary cases.
- For millions of rows, the goal is not manual grading.
  Use thresholds, buckets, or bands to segment the population.

## Exercise 43 to 48 — Percentile bands, review queues, and owner priority scoring

Purpose:
Document the training cluster where Sean converted row-level percentile
positions into business bands, review queues, owner summaries, weighted
priority scores, regional ranks, and final recommended actions.

Core mental model:
raw value
-> relative position
-> business band
-> review queue
-> owner summary
-> weighted priority score
-> rank
-> recommended action

Memory nuggets:
- `CUME_DIST` creates relative position.
- `CASE` creates business bands.
- `GROUP BY` creates the management report.
- `WHERE` selects the review queue.
- Conditional `SUM` counts each band.
- Weights create urgency.
- `RANK` creates management order.
- `CASE` at the end turns analytics into a business recommendation.

Plain reminder:
CUME_DIST creates relative position.
CASE creates business bands.
RANK creates management order.

### Exercise 43 — Create revenue bands with CUME_DIST

Explain:
Sean classified each sale inside its own region using `CUME_DIST`.

Band rules:
- `CUME_DIST >= 0.95` -> `Top 5%`
- `CUME_DIST >= 0.80` -> `High`
- `CUME_DIST >= 0.20` -> `Middle`
- else -> `Low`

Final SQL:
```sql
WITH revenue_positions AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,

    CUME_DIST() OVER (
      PARTITION BY region
      ORDER BY revenue ASC
    ) AS revenue_cume_dist

  FROM sales_events
),

revenue_bands AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,
    ROUND(revenue_cume_dist::numeric, 4) AS revenue_cume_dist,

    CASE
      WHEN revenue_cume_dist >= 0.95 THEN 'Top 5%'
      WHEN revenue_cume_dist >= 0.80 THEN 'High'
      WHEN revenue_cume_dist >= 0.20 THEN 'Middle'
      ELSE 'Low'
    END AS revenue_band

  FROM revenue_positions
)

SELECT
  region,
  revenue_band,
  COUNT(*) AS row_count,
  MIN(revenue) AS min_revenue,
  MAX(revenue) AS max_revenue
FROM revenue_bands
GROUP BY
  region,
  revenue_band
ORDER BY
  region ASC,
  CASE
    WHEN revenue_band = 'Top 5%' THEN 1
    WHEN revenue_band = 'High' THEN 2
    WHEN revenue_band = 'Middle' THEN 3
    WHEN revenue_band = 'Low' THEN 4
  END;
```

Observed summary:
East:
- `Top 5% = 6 rows`, revenue `1500` to `2000`
- `High = 13 rows`, revenue `1345` to `1449`
- `Middle = 54 rows`, revenue `782` to `1341`
- `Low = 17 rows`, revenue `417` to `781`

North/South/West had the same overall band shape except `Top 5%` had `5` rows
and `High` had `14` rows.

Explain:
The bands are relative per region. Each region is judged against its own
distribution, not one global revenue threshold.

### Exercise 44 — Detail review queue for Top 5% and High rows

Explain:
The previous query was a summary report. This query returns the actual rows
to review.

Final SQL:
```sql
WITH revenue_positions AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,

    CUME_DIST() OVER (
      PARTITION BY region
      ORDER BY revenue ASC
    ) AS revenue_cume_dist

  FROM sales_events
),

revenue_bands AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,
    ROUND(revenue_cume_dist::numeric, 4) AS revenue_cume_dist,

    CASE
      WHEN revenue_cume_dist >= 0.95 THEN 'Top 5%'
      WHEN revenue_cume_dist >= 0.80 THEN 'High'
      WHEN revenue_cume_dist >= 0.20 THEN 'Middle'
      ELSE 'Low'
    END AS revenue_band

  FROM revenue_positions
)

SELECT
  sale_id,
  region,
  salesperson,
  revenue,
  revenue_cume_dist,
  revenue_band
FROM revenue_bands
WHERE revenue_band IN ('Top 5%', 'High')
ORDER BY
  region ASC,
  CASE
    WHEN revenue_band = 'Top 5%' THEN 1
    WHEN revenue_band = 'High' THEN 2
  END,
  revenue DESC,
  sale_id ASC;
```

Observed meaning:
This returned the actual `Top 5%` and `High` rows, sorted as a review queue.

Memory distinction:
Summary report = `GROUP BY` band and count rows.
Review queue = `WHERE band IN (...)` and show detail rows.

### Exercise 45 — Count review queue by salesperson

Explain:
Sean summarized the high-priority review queue by owner.

Final SQL:
```sql
WITH revenue_positions AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,

    CUME_DIST() OVER (
      PARTITION BY region
      ORDER BY revenue ASC
    ) AS revenue_cume_dist

  FROM sales_events
),

revenue_bands AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,
    ROUND(revenue_cume_dist::numeric, 4) AS revenue_cume_dist,

    CASE
      WHEN revenue_cume_dist >= 0.95 THEN 'Top 5%'
      WHEN revenue_cume_dist >= 0.80 THEN 'High'
      WHEN revenue_cume_dist >= 0.20 THEN 'Middle'
      ELSE 'Low'
    END AS revenue_band

  FROM revenue_positions
)

SELECT
  region,
  salesperson,
  revenue_band,
  COUNT(*) AS row_count,
  MAX(revenue) AS max_revenue
FROM revenue_bands
WHERE revenue_band IN ('Top 5%', 'High')
GROUP BY
  region,
  salesperson,
  revenue_band
ORDER BY
  region ASC,
  CASE
    WHEN revenue_band = 'Top 5%' THEN 1
    WHEN revenue_band = 'High' THEN 2
  END,
  row_count DESC,
  max_revenue DESC,
  salesperson ASC;
```

Observed examples:
East:
- Casey Nguyen, `Top 5% = 4` rows, max `2000`
- Jordan Lee, `Top 5% = 2` rows, max `1600`
- Jordan Lee, `High = 9` rows, max `1449`
- Casey Nguyen, `High = 4` rows, max `1417`

Memory nugget:
`CUME_DIST` creates relative position.
`CASE` creates business bands.
`WHERE` selects the review queue.
`GROUP BY` summarizes ownership.

### Exercise 46 — Create owner-level priority score

Explain:
Sean assigned weights to row bands:
- `Top 5%` row = `3` points
- `High` row = `1` point

Final SQL:
```sql
WITH revenue_positions AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,

    CUME_DIST() OVER (
      PARTITION BY region
      ORDER BY revenue ASC
    ) AS revenue_cume_dist

  FROM sales_events
),

revenue_bands AS (
  SELECT
    sale_id,
    region,
    salesperson,
    revenue,
    ROUND(revenue_cume_dist::numeric, 4) AS revenue_cume_dist,

    CASE
      WHEN revenue_cume_dist >= 0.95 THEN 'Top 5%'
      WHEN revenue_cume_dist >= 0.80 THEN 'High'
      WHEN revenue_cume_dist >= 0.20 THEN 'Middle'
      ELSE 'Low'
    END AS revenue_band

  FROM revenue_positions
),

priority_by_salesperson AS (
  SELECT
    region,
    salesperson,

    SUM(CASE WHEN revenue_band = 'Top 5%' THEN 1 ELSE 0 END) AS top_5_count,
    SUM(CASE WHEN revenue_band = 'High' THEN 1 ELSE 0 END) AS high_count,

    3 * SUM(CASE WHEN revenue_band = 'Top 5%' THEN 1 ELSE 0 END)
    +
    SUM(CASE WHEN revenue_band = 'High' THEN 1 ELSE 0 END) AS priority_score,

    MAX(revenue) AS max_revenue

  FROM revenue_bands
  WHERE revenue_band IN ('Top 5%', 'High')
  GROUP BY
    region,
    salesperson
)

SELECT
  region,
  salesperson,
  top_5_count,
  high_count,
  priority_score,
  max_revenue
FROM priority_by_salesperson
ORDER BY
  region ASC,
  priority_score DESC,
  top_5_count DESC,
  high_count DESC,
  max_revenue DESC,
  salesperson ASC;
```

Observed examples:
- North / Morgan Diaz = `5 Top 5%` rows and `5 High` rows = `20` score.
- East / Casey Nguyen = `4 Top 5%` rows and `4 High` rows = `16` score.
- East / Jordan Lee = `2 Top 5%` rows and `9 High` rows = `15` score.

Explain:
Casey ranks above Jordan in East because `Top 5%` rows have heavier weight.

Memory nugget:
Banding creates categories.
Weights create urgency.
`GROUP BY` turns row-level urgency into owner-level priority.

### Exercise 47 — Rank owners by priority score

Explain:
Sean ranked salespeople inside each region using `RANK` over the owner-level
priority result.

Final SQL should include a `ranked_priority` CTE:

```sql
ranked_priority AS (
  SELECT
    region,
    salesperson,
    top_5_count,
    high_count,
    priority_score,
    max_revenue,

    RANK() OVER (
      PARTITION BY region
      ORDER BY
        priority_score DESC,
        top_5_count DESC,
        max_revenue DESC
    ) AS priority_rank

  FROM priority_by_salesperson
)
```

Final SELECT:

```sql
SELECT
  region,
  priority_rank,
  salesperson,
  top_5_count,
  high_count,
  priority_score,
  max_revenue
FROM ranked_priority
ORDER BY
  region ASC,
  priority_rank ASC,
  salesperson ASC;
```

Observed result:
East:
- Rank 1 Casey Nguyen, score `16`
- Rank 2 Jordan Lee, score `15`

North:
- Rank 1 Morgan Diaz, score `20`
- Rank 2 Alex Kim, score `9`

South:
- Rank 1 Riley Brooks, score `16`
- Rank 2 Sam Patel, score `13`

West:
- Rank 1 Taylor Chen, score `20`
- Rank 2 Jamie Clark, score `9`

Memory nugget:
Percentile band = row-level signal.
Priority score = owner-level urgency.
`RANK` = management order.

### Exercise 47B — Keep only rank 1 owner per region

Explain:
Sean filtered to the top priority owner per region.

Final SELECT over `ranked_priority`:

```sql
SELECT
  region,
  priority_rank,
  salesperson,
  top_5_count,
  high_count,
  priority_score,
  max_revenue
FROM ranked_priority
WHERE priority_rank = 1
ORDER BY
  region ASC;
```

Observed result:
- East -> Casey Nguyen
- North -> Morgan Diaz
- South -> Riley Brooks
- West -> Taylor Chen

Memory nugget:
Build ranking in a CTE.
Filter the rank in the outer query.

### Exercise 48 — Add final recommended_action label

Explain:
Sean added final business recommendation language to the rank 1 result.

Recommendation rules:
- `priority_score >= 20` -> `Immediate focus`
- `priority_score >= 15` -> `High priority`
- else -> `Monitor`

Final SELECT:

```sql
SELECT
  region,
  priority_rank,
  salesperson,
  top_5_count,
  high_count,
  priority_score,
  max_revenue,
  CASE
    WHEN priority_score >= 20 THEN 'Immediate focus'
    WHEN priority_score >= 15 THEN 'High priority'
    ELSE 'Monitor'
  END AS recommended_action
FROM ranked_priority
WHERE priority_rank = 1
ORDER BY
  region ASC;
```

Observed result:
- East / Casey Nguyen = `High priority`
- North / Morgan Diaz = `Immediate focus`
- South / Riley Brooks = `High priority`
- West / Taylor Chen = `Immediate focus`

### Exercise 49 — Interview translation: explain the owner-priority pipeline

Purpose:
Capture the plain-English explanation Sean can use in an interview
or manager conversation.

Full spoken version:

I built a SQL pipeline that starts with raw sales rows and turns them
into a management recommendation.

First, I used CUME_DIST to compare each sale against other sales in
the same region. That means each region is judged fairly against its
own sales distribution, instead of using one global revenue cutoff.

Then I converted each sale into a business band:
Top 5%, High, Middle, or Low.

After that, I filtered only the important bands — Top 5% and High —
into a review queue. That gave me the rows that deserve attention.

Then I grouped those review rows by salesperson and region. I counted
how many Top 5% and High rows each salesperson had.

To make the score more meaningful, I gave Top 5% rows more weight than
High rows. In this case, Top 5% counted as 3 points and High counted
as 1 point.

Then I ranked the salespeople inside each region by that priority
score.

Finally, I added a recommendation label, such as Immediate focus or
High priority.

So the main idea is:

raw sales rows became row-level signals,
row-level signals became owner-level scores,
and owner-level scores became ranked business recommendations.

Shorter interview version:

I used window functions to turn raw sales rows into a priority report.
CUME_DIST gave each sale a relative position within its region. I used
CASE to convert those positions into bands like Top 5% and High. Then
I filtered the important bands, grouped them by salesperson, applied a
weighted score, ranked the owners inside each region, and added a final
recommended action. The result was a management-friendly report showing
who deserved attention first in each region.

Memory line:
Raw rows -> signals -> scores -> ranked recommendations.

Final cluster summary:
- Raw values become percentile positions.
- Percentile positions become business bands.
- Business bands become review queues.
- Review queues can be summarized by owner.
- Weighted scoring turns row-level signals into owner-level urgency.
- `RANK` inside each region creates a management order.
- `CASE` at the end creates readable recommendations.
- Interview translation matters because SQL work must be explainable.
- The pipeline is not just syntax; it is analytics design.
- This pattern applies to sales, finance, fraud, customer risk, observability,
  incident triage, and capacity prioritization.

## Final Oral Defense Q&A — Window Functions, Percentiles, and Priority Scoring

Purpose:
Give Sean a compact interview-style review section he can read out loud.
This should be easy to rehearse when tired.

### A) Window function foundations

Q1. What is the difference between GROUP BY and PARTITION BY?

Answer:
GROUP BY collapses rows into summary rows. PARTITION BY creates groups for
a window calculation but keeps the original detail rows visible.

Memory line:
GROUP BY collapses. PARTITION BY keeps detail rows.

Q2. What does ORDER BY inside OVER do?

Answer:
ORDER BY inside OVER creates the sequence used by the window function.
For aggregate windows like SUM or COUNT, adding ORDER BY usually changes
a full-partition value into a running value.

Memory line:
No ORDER BY inside OVER = whole group.
ORDER BY inside OVER = row-by-row journey.

Q3. What is the difference between ORDER BY inside OVER and final ORDER BY?

Answer:
ORDER BY inside OVER affects the calculation. Final ORDER BY affects only
how the result is displayed.

Memory line:
Window ORDER BY calculates. Final ORDER BY displays.

### B) Ranking functions

Q4. When do I use ROW_NUMBER?

Answer:
Use ROW_NUMBER when the business wants one exact row position, such as the
single third salesperson in each department. ROW_NUMBER never preserves ties.

Q5. When do I use RANK?

Answer:
Use RANK when the business wants competition-style ranking and tied values
should share the same rank. RANK can skip numbers after a tie.

Q6. When do I use DENSE_RANK?

Answer:
Use DENSE_RANK when the business wants distinct value tiers without gaps.
Tied values share the same rank, but the next distinct value gets the next
rank number.

Q7. Why should I avoid adding a unique tie-breaker to RANK or DENSE_RANK?

Answer:
A unique tie-breaker, such as sale_id or salesperson, can destroy the tie.
If the business wants ties preserved, rank only by the value that defines
the tie.

Memory line:
ROW_NUMBER can use tie-breakers. RANK and DENSE_RANK often should not.

### C) LAG and LEAD

Q8. What does LAG do?

Answer:
LAG brings a value from a previous row into the current row. It is useful for
comparing the current value to a prior value.

Q9. What does LEAD do?

Answer:
LEAD brings a value from a future row into the current row. It is useful for
comparing the current value to the next value.

Memory line:
LAG is the rearview mirror. LEAD is the windshield.

Q10. Why does the first LAG row return NULL?

Answer:
The first row in a partition has no previous row, so NULL is the truthful
result.

Q11. Why use NULLIF in percent-change math?

Answer:
NULLIF prevents division by zero. If the previous value is zero, NULLIF turns
it into NULL so the query does not fail or produce misleading math.

### D) FIRST_VALUE and LAST_VALUE

Q12. Why is FIRST_VALUE usually straightforward?

Answer:
FIRST_VALUE returns the first value in the ordered window. The default frame
usually includes the first row, so it behaves as expected.

Q13. Why is LAST_VALUE tricky?

Answer:
LAST_VALUE often returns the current row because the default frame usually
ends at the current row. To get the true last value in the partition, use a
full frame.

Q14. What is the safe full-frame pattern for LAST_VALUE?

Answer:
Use:

ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING

Memory line:
LAST_VALUE needs the full frame when you want the true last row.

### E) Window frames and moving calculations

Q15. What does ROWS BETWEEN 2 PRECEDING AND CURRENT ROW mean?

Answer:
It means the current row plus the previous two physical rows. That creates a
three-row trailing window.

Q16. What is a previous-only frame?

Answer:
A previous-only frame compares the current row against history without
including the current row in its own benchmark. Example:

ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING

Q17. What is the difference between ROWS and RANGE?

Answer:
ROWS moves by physical rows. RANGE moves by peer groups based on the ORDER BY
value. If multiple rows share the same date, RANGE can jump by all rows on
that date.

Memory line:
ROWS = physical rows. RANGE = value peers.

Q18. When would Pandas or Spark be better than SQL?

Answer:
SQL is strong for basic moving windows and aggregation. Pandas or Spark can
be cleaner for richer feature engineering, weighted moving averages,
exponential smoothing, and model-ready time-series features.

### F) NTILE, P95, CUME_DIST, and PERCENT_RANK

Q19. What does NTILE do?

Answer:
NTILE splits ordered rows into roughly equal buckets. It gives each row a
bucket number. It does not calculate an exact cutoff value.

Q20. What does percentile_cont / P95 do?

Answer:
P95 calculates a value cutoff. It answers: what value separates the lower
95 percent from the top 5 percent?

Memory line:
NTILE is a bucket label. P95 is a cutoff value.

Q21. Why does percentile_cont use WITHIN GROUP instead of OVER in this workbook?

Answer:
In this workbook, percentile_cont is used as an ordered aggregate. WITHIN GROUP
sorts values inside the aggregate calculation. GROUP BY region then returns
one P95 cutoff per region.

Q22. Why did NTILE(100) return no bucket 100?

Answer:
Each region had only 90 rows. NTILE(100) cannot populate 100 buckets from
only 90 rows, so bucket 100 may not exist.

Q23. What does CUME_DIST mean?

Answer:
CUME_DIST tells what fraction of rows are at or below the current value. It
is coverage-based.

Q24. What does PERCENT_RANK mean?

Answer:
PERCENT_RANK tells where the current value starts on the ranking ladder. It
is rank-start based.

Q25. Why can CUME_DIST and PERCENT_RANK differ around ties?

Answer:
CUME_DIST counts through the end of the tie group. PERCENT_RANK uses where
the tie group starts.

Memory line:
CUME_DIST looks after the tie group. PERCENT_RANK looks at where the tie
group starts.

Plain reminder:
PERCENT_RANK looks at where the tie group starts.

Q26. Which is easier for top-percent business flags: CUME_DIST, PERCENT_RANK,
or P95?

Answer:
P95 and CUME_DIST are usually easier for top-percent flags. P95 gives a
cutoff value. CUME_DIST gives row-level coverage. PERCENT_RANK is useful,
but it can be less intuitive near tied boundaries.

### G) Owner-priority pipeline

Q27. What was the final owner-priority pipeline?

Answer:
Raw revenue rows were converted into percentile positions. Percentile
positions were converted into bands. The important bands became a review
queue. The review queue was grouped by salesperson. Top 5% rows were weighted
more heavily than High rows. Salespeople were ranked by priority score inside
each region. Finally, a recommended action label was added.

Memory line:
Raw rows -> signals -> scores -> ranked recommendations.

Q28. Why did we use CUME_DIST before creating revenue_band?

Answer:
CUME_DIST gave each row a relative position inside its own region. That let
each region be judged against its own distribution instead of one global
revenue cutoff.

Q29. Why did we filter only Top 5% and High rows?

Answer:
Those rows formed the review queue. They were the rows important enough to
drive management attention.

Q30. Why did Top 5% get 3 points and High get 1 point?

Answer:
Top 5% rows were stronger signals than High rows. The weighting made the
priority score reflect urgency, not just row count.

Q31. Why did Casey rank above Jordan in East even though Jordan had more High
rows?

Answer:
Casey had more Top 5% rows, and Top 5% rows had heavier weight. The score
prioritized stronger signals over simple volume.

Q32. What did recommended_action add?

Answer:
recommended_action translated the numeric priority score into readable
business language such as Immediate focus, High priority, or Monitor.

Memory line:
CASE at the end turns analytics into a business recommendation.

### H) Interview-ready final answer

If an interviewer asks what I built here, I would say:

I built a SQL analytics pipeline using window functions and CTEs. I started
with raw sales rows, used CUME_DIST to place each sale relative to other sales
inside its region, and converted those positions into business bands such as
Top 5%, High, Middle, and Low.

Then I filtered the most important bands into a review queue, grouped that
queue by salesperson, and applied a weighted priority score where Top 5%
signals counted more than High signals. After that, I ranked the salespeople
inside each region and added a final recommended action label.

The business value is that raw detail rows became a management-friendly
priority report. The same pattern could apply to sales performance, fraud
signals, customer risk, observability alerts, incident triage, or capacity
prioritization.

### I) Self-test checklist

Before I call Course 05 stable, I should be able to explain:

* GROUP BY vs PARTITION BY
* ORDER BY inside OVER vs final ORDER BY
* ROW_NUMBER vs RANK vs DENSE_RANK
* why rank aliases need a CTE before filtering
* LAG vs LEAD
* FIRST_VALUE vs LAST_VALUE
* why LAST_VALUE needs a full frame
* moving averages with ROWS BETWEEN
* ROWS vs RANGE
* NTILE vs P95
* WITHIN GROUP vs OVER
* CUME_DIST vs PERCENT_RANK
* P95 cutoff and join-back pattern
* review queue pattern
* weighted owner-priority scoring
* final recommended_action label
