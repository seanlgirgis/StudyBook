# PostgreSQL Summary Stats and Window Functions Field Guide

## Course status

- Platform status: COMPLETE
- Documentation status: DEVELOPING
- Lab status: LIGHT / COURSE-WIDE DECISION PENDING
- Recall confidence: DEVELOPING
- Interview readiness: NEEDS REPETITION

## Course map

1. [Chapter 1 — Introduction to Window Functions](chapter_01_introduction_to_window_functions_field_guide.html)
2. [Chapter 2 — Fetching, Ranking, and Paging](chapter_02_fetching_ranking_and_paging_field_guide.html)
3. [Chapter 3 — Aggregate Window Functions and Frames](chapter_03_aggregate_window_functions_and_frames_field_guide.html)
4. [Chapter 4 — Beyond Window Functions](chapter_04_beyond_window_functions_field_guide.html)
5. [SQL Quick Lookup](sql_quick_lookup.html)
6. [Lab Run Book](../lab/lab_run_book.md)

## Core mental model

A window function calculates across rows related to the current row while preserving one output row for every input row.

```text
GROUP BY
→ collapses detail rows

Window function
→ preserves detail rows
→ adds an analytical value beside each row
```

## Essential syntax

```sql
function_expression OVER (
    PARTITION BY grouping_column
    ORDER BY ordering_column
    ROWS BETWEEN frame_start AND frame_end
)
```

Not every window function needs every subclause:

```sql
COUNT(*) OVER ()

ROW_NUMBER() OVER (
    ORDER BY year
)

DENSE_RANK() OVER (
    PARTITION BY country
    ORDER BY medals DESC
)

AVG(medals) OVER (
    PARTITION BY country
    ORDER BY year
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
```

---

## Chapter 1 — Window-Function Foundations

### Main ideas

- `OVER()` marks a function as a window calculation.
- `ORDER BY` inside `OVER()` controls calculation sequence.
- Final query `ORDER BY` controls display order.
- `PARTITION BY` restarts the calculation for each group.
- `ROW_NUMBER()` always assigns a unique sequence.

### Core pattern

```sql
SELECT
    year,
    event,
    country,
    ROW_NUMBER() OVER (
        PARTITION BY gender, event
        ORDER BY year
    ) AS row_n
FROM summer_medals
WHERE medal = 'Gold';
```

### Memory rule

```text
ORDER BY inside OVER()
= order used by the calculation

ORDER BY at the end of the query
= order used to display the result
```

---

## Chapter 2 — Fetching, Ranking, and Paging

### Fetching functions

```sql
LAG(value, offset)  OVER (...)
LEAD(value, offset) OVER (...)

FIRST_VALUE(value) OVER (...)
LAST_VALUE(value)  OVER (...)
```

`LAG()` looks backward. `LEAD()` looks forward.

The second argument is a row offset:

```sql
LEAD(athlete, 3) OVER (ORDER BY year)
```

This means three rows ahead, not three years ahead.

### LAST_VALUE frame rule

```sql
LAST_VALUE(city) OVER (
    ORDER BY year
    RANGE BETWEEN
        UNBOUNDED PRECEDING AND
        UNBOUNDED FOLLOWING
)
```

Without `UNBOUNDED FOLLOWING`, `LAST_VALUE()` may return the current row’s value.

### Ranking decision table

| Function | Ties | Gap after ties |
|---|---|---|
| `ROW_NUMBER()` | No | Not applicable |
| `RANK()` | Yes | Yes |
| `DENSE_RANK()` | Yes | No |

Example values:

```text
27, 26, 26, 25

ROW_NUMBER → 1, 2, 3, 4
RANK       → 1, 2, 2, 4
DENSE_RANK → 1, 2, 2, 3
```

### Paging with NTILE

```sql
NTILE(3) OVER (
    ORDER BY medals DESC
) AS third
```

`NTILE()` balances row counts, not numeric ranges.

### Reusable CTE pattern

```text
CTE 1: aggregate raw rows
CTE 2: calculate the window function
Outer query: filter, group, or summarize the window result
```

---

## Chapter 3 — Aggregate Window Functions and Frames

### Aggregate windows

Traditional aggregates become window functions when followed by `OVER()`:

```sql
SUM(medals) OVER ()
AVG(medals) OVER ()
MIN(medals) OVER ()
MAX(medals) OVER ()
```

These preserve detail rows.

### Running total

```sql
SUM(medals) OVER (
    PARTITION BY country
    ORDER BY year
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
) AS running_total
```

### Moving average

```sql
AVG(medals) OVER (
    PARTITION BY country
    ORDER BY year
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
) AS moving_avg
```

`2 PRECEDING AND CURRENT ROW` can contain up to three rows.

### Frame boundaries

- `UNBOUNDED PRECEDING`
- `n PRECEDING`
- `CURRENT ROW`
- `n FOLLOWING`
- `UNBOUNDED FOLLOWING`

### ROWS versus RANGE

```text
ROWS
= physical row positions

RANGE
= logical peer groups based on ORDER BY values
```

Use `ROWS` when you mean an exact number of records.

---

## Chapter 4 — Beyond Window Functions

### Pivoting with CROSSTAB

Enable the PostgreSQL extension:

```sql
CREATE EXTENSION IF NOT EXISTS tablefunc;
```

Basic pattern:

```sql
SELECT *
FROM CROSSTAB(
  $$
    SELECT row_key, category, value
    FROM source_data
    ORDER BY row_key, category
  $$
) AS ct (
  row_key text,
  "category_1" integer,
  "category_2" integer
);
```

PostgreSQL requires the pivot output columns and data types in advance.

### ROLLUP

Use for hierarchical subtotals:

```sql
GROUP BY ROLLUP(year, quarter)
```

### CUBE

Use for all subtotal combinations:

```sql
GROUP BY CUBE(country, medal)
```

### COALESCE

Replace structural subtotal nulls with readable labels:

```sql
COALESCE(country, 'All countries')
```

### STRING_AGG

Compress multiple rows into one ordered string:

```sql
STRING_AGG(country, ', ' ORDER BY rank_n)
```

### Chapter 4 pattern

```text
Aggregate first
→ rank second
→ pivot or summarize third
```

---

## Common mistakes

### Confusing GROUP BY and window functions

`GROUP BY` reduces rows. Window functions retain rows.

### Omitting a meaningful window order

`ROW_NUMBER()`, `LAG()`, `LEAD()`, and frame-based aggregates need a clear `ORDER BY`.

### Forgetting PARTITION BY

The calculation may continue across unrelated countries, events, or categories.

### Trusting LAST_VALUE with the default frame

Extend the frame through `UNBOUNDED FOLLOWING` when you need the true final value.

### Choosing the wrong ranking function

Decide whether ties should be unique, tied with gaps, or tied without gaps.

### Miscounting a frame

```text
2 PRECEDING + CURRENT ROW = up to 3 rows
3 PRECEDING + CURRENT ROW = up to 4 rows
```

### Treating NTILE as equal value ranges

It creates approximately equal row-count buckets.

### Confusing ROLLUP and CUBE

`ROLLUP` follows a hierarchy. `CUBE` returns every subtotal combination.

---

## Interview translation

### What is a window function?

A window function calculates across rows related to the current row while preserving every input row in the output.

### How is it different from GROUP BY?

`GROUP BY` collapses rows into summaries. Window functions preserve detailed rows and add analytical values beside them.

### What does PARTITION BY do?

It divides rows into independent groups and restarts the window calculation for each group.

### What is the difference between RANK and DENSE_RANK?

Both assign the same rank to ties. `RANK()` leaves gaps after ties; `DENSE_RANK()` does not.

### What is a window frame?

A window frame is the subset of ordered rows used for the current row’s calculation.

### What is the difference between ROWS and RANGE?

`ROWS` counts physical records. `RANGE` groups peer rows that share the same ordering value.

### What does NTILE do?

It divides ordered rows into a requested number of approximately equal buckets.

### How do ROLLUP and CUBE differ?

`ROLLUP` produces hierarchical subtotals. `CUBE` produces every possible subtotal combination.

---

## Quick memory nuggets

```text
Window function
= calculate across related rows
= preserve detail rows
```

```text
LAG  → previous row
LEAD → next row
```

```text
ROW_NUMBER → unique
RANK       → ties with gaps
DENSE_RANK → ties without gaps
```

```text
Running total
= UNBOUNDED PRECEDING → CURRENT ROW
```

```text
Moving 3-row average
= 2 PRECEDING → CURRENT ROW
```

```text
ROLLUP → hierarchy
CUBE   → all combinations
```

## Reusable interview sentence

Window functions let me calculate rankings, row-to-row comparisons, running totals, moving statistics, and grouped analytical measures without collapsing the detailed result set as `GROUP BY` would.
