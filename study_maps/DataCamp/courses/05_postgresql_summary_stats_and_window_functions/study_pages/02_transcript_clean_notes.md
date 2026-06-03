# Window Functions Clean Notes

- Window functions operate across rows related to the current row.
- They are similar to `GROUP BY` because they can calculate across multiple rows.
- They are different from `GROUP BY` because they keep the original rows in the output.
- Window functions help with running totals, previous-row comparisons, ranking, and moving averages.
- `ROW_NUMBER()` assigns a position number to each row.
- `OVER()` marks the function as a window function.
- `OVER` can later contain `ORDER BY`, `PARTITION BY`, `ROWS`, `RANGE`, `PRECEDING`, `FOLLOWING`, and `UNBOUNDED`.
## Chapter 2 Clean Notes: ORDER BY inside OVER and LAG

- `ORDER BY` inside `OVER` controls how `ROW_NUMBER` assigns numbers.
- `ORDER BY Year DESC` gives row number `1` to the most recent year.
- `ORDER BY` can use multiple columns, such as `Year` and `Event`.
- `ORDER BY` inside `OVER` controls calculation order.
- `ORDER BY` outside `OVER` controls final display order.
- `ORDER BY` inside `OVER` happens before final `ORDER BY`.
- `LAG(column, 1)` brings the previous row value.
- `LAG` is useful for "reigning champion" style comparisons.
- CTE first creates the current champions row set.
- Outer query uses `LAG` to put current champion and previous champion on the same row.
- First row has `NULL` for previous value.

## Transcript Notes: PARTITION BY and Fetching Functions

### PARTITION BY transcript
- `PARTITION BY` separates independent histories.
- Without `PARTITION BY`, `LAG`/`LEAD` can cross from one event to another.
- `PARTITION BY event` fixes Discus Throw vs Triple Jump crossover.
- `PARTITION BY` multiple columns creates partitions by combinations.
- `ROW_NUMBER` resets inside each partition.
- `LAG` fetches previous values only inside the same partition.

### Fetching transcript
- `LAG` and `LEAD` are relative fetching functions.
- `FIRST_VALUE` and `LAST_VALUE` are absolute fetching functions.
- `LEAD(column, 1)` fetches next row.
- `LEAD(column, 2)` fetches the row after next.
- `FIRST_VALUE` returns first value in table/partition.
- `LAST_VALUE` needs explicit full frame to return the true last value.
- Partitioning also applies to fetching functions.

## Transcript Notes: Ranking and Paging (NTILE)

### Ranking transcript notes
- `ROW_NUMBER` gives unique row numbers, even for ties.
- `RANK` gives ties same rank and leaves gaps.
- `DENSE_RANK` gives ties same rank without gaps.
- For medal-count ranking, summarize first (`GROUP BY Athlete`) then rank.
- Use `PARTITION BY` for in-group ranking, such as ranking athletes inside each country.
- Without `PARTITION BY`, ranking is global even if final display order looks grouped.

### Paging / NTILE transcript notes
- `NTILE(n)` splits rows into approximately equal pages/buckets.
- `NTILE(111)` can page distinct events alphabetically.
- `NTILE(3)` can create top/middle/bottom thirds from medal counts.
- `NTILE` does not preserve ties like `RANK`/`DENSE_RANK`.
- `NTILE` labels buckets, not true percentile threshold values.
- After assigning NTILE labels, `GROUP BY` bucket labels can summarize each bucket.

## Transcript Notes: CROSSTAB, ROLLUP/CUBE, COALESCE, STRING_AGG
- `CROSSTAB` is pivoting/report reshaping via `tablefunc`; not a window function.
- Enable extension with `CREATE EXTENSION IF NOT EXISTS tablefunc;`.
- Simple `CROSSTAB` source shape is row/category/value, with manual output columns.
- `ROLLUP` is hierarchical subtotaling; order of grouped columns matters.
- `CUBE` creates all subtotal combinations.
- `COALESCE` cleans subtotal labels but does not create totals.
- `STRING_AGG` compresses rows into one ordered list.
- Rank first in a CTE, filter top rows, then aggregate with `STRING_AGG`.

## Deep Completion Notes
- Added CROSSTAB, ROLLUP/CUBE, COALESCE, STRING_AGG, and FILTER pivot distinctions.
- Added sample data realism lesson and moving total alias correction.

