# Easy Explanations

## GROUP BY vs PARTITION BY
- `GROUP BY` collapses rows into summary rows.
- `PARTITION BY` makes buckets but keeps every original row.
- Window functions calculate inside each bucket.

## ROW_NUMBER
- `ROW_NUMBER()` always gives unique row positions.
- The order comes from `ORDER BY` inside `OVER()`.
- Add `event_id` as tie breaker so results are stable.

## RANK vs DENSE_RANK
- `RANK()` leaves gaps after ties.
- `DENSE_RANK()` does not leave gaps.
- Medal example:
  - `ROW_NUMBER`: unique row positions
  - `RANK`: one gold, two silvers, no bronze
  - `DENSE_RANK`: one gold, two silvers, one bronze

## LAG and LEAD
- `LAG` = previous row value.
- `LEAD` = next row value.
- Both need `ORDER BY` to define previous/next.
- We used a CTE pattern to compute `LAG` once and reuse it.
- `NULLIF(previous_revenue, 0)` avoids divide-by-zero in percent change.

## Running totals
- `SUM(revenue) OVER (...)` can accumulate over ordered rows.
- `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` means from first row to current row.

## Moving averages
- `AVG(revenue) OVER (...)` gives rolling averages.
- `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` means current row + previous 2 rows.

## Daily summary then window
- First do `GROUP BY sale_date` to get daily averages.
- Then apply window functions over the daily result.

## Percent of total
- `revenue / SUM(revenue) OVER (PARTITION BY sale_date)` gives row share of daily total.
- Same shape works for region, salesperson, product category.

## Named WINDOW
- `WINDOW daily_window AS (...)` reuses partition/order/frame definitions.
- You still choose function separately (`SUM`, `AVG`, etc.).

## NTILE
- `NTILE(4)` splits ordered rows into 4 buckets.
- `ORDER BY` in `OVER()` decides bucket assignment.
- Final `ORDER BY` in query only controls display.
- We adjusted seed data because smooth revenue made NTILE look fake by date.

## P95 telemetry link
- `NTILE(100)` can label rows into percentile-like buckets.
- True P95 value should use `percentile_cont(0.95)` or `percentile_disc(0.95)`.
- `NTILE` labels rows; percentile functions compute percentile values.
## Sean's Mental Model
- `PARTITION BY` is like bucketing rows, but it does not collapse rows.
- `GROUP BY` summarizes and collapses rows.
- Window functions calculate across related rows while keeping detail rows.
- `ORDER BY` inside `OVER` controls calculation order.
- Final `ORDER BY` controls display order.
- `WINDOW` names reusable `PARTITION BY` / `ORDER BY` / frame rules.
- `LAG` looks backward; `LEAD` looks forward.
- `ROWS BETWEEN` controls exactly which rows are included in the window frame.

## Before Returning to DataCamp
- [ ] I can explain `PARTITION BY` vs `GROUP BY`.
- [ ] I can explain `ORDER BY` inside `OVER`.
- [ ] I can explain `ROW_NUMBER` vs `RANK` vs `DENSE_RANK`.
- [ ] I can explain `LAG` vs `LEAD`.
- [ ] I can explain running total vs moving average.
- [ ] I can explain `NTILE` vs true P95.

## ORDER BY inside OVER vs final ORDER BY
- Inside `OVER` = calculation order.
- Final `ORDER BY` = display order.
- Row number `1` may not appear first on screen if final display sorting is different.

## LAG for Reigning Champion
- `LAG` puts the previous champion beside the current champion.
- Once both values are on one row, we can compare them directly.
- For this learning exercise, this avoids a self-join.

## Alias Correction: Moving Total vs Moving Average
- `SUM` + sliding frame = moving total.
- `AVG` + sliding frame = moving average.
- Do not label `SUM` output as `Medals_MA`.
- Prefer aliases like `Medals_MT`, `Moving_Total`, or `Medals_3_Game_Total`.

```sql
WITH Country_Medals AS (
SELECT
Year,
Country,
COUNT(*) AS Medals
FROM Summer_Medals
GROUP BY Year, Country
)

SELECT
Year,
Country,
Medals,
SUM(Medals) OVER (
PARTITION BY Country
ORDER BY Year ASC
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
) AS Medals_MT
FROM Country_Medals
ORDER BY Country ASC, Year ASC;
```

This is a 3-game moving total per country, not a moving average.
To make it a moving average, replace `SUM()` with `AVG()` and use an MA alias.

## Reporting Tools vs Window Tools
- Window functions keep detail rows and add analytical context.
- `CROSSTAB` reshapes rows into wide report columns.
- `ROLLUP`/`CUBE` add subtotal rows.
- `COALESCE` makes subtotal labels readable.
- `STRING_AGG` compresses many rows into one readable list.

## Final Mental Model Reminder
- Window functions calculate.
- CROSSTAB reshapes.
- ROLLUP/CUBE subtotal.
- COALESCE labels.
- STRING_AGG compresses.

