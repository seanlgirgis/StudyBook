# SQL Patterns

## ROW_NUMBER basics
`ROW_NUMBER()` numbers rows uniquely. `ORDER BY` inside `OVER()` controls numbering order. Use `event_id` as a tie breaker for stable results.

```sql
SELECT
    sale_date,
    event_id,
    revenue,
    ROW_NUMBER() OVER (
        PARTITION BY sale_date
        ORDER BY revenue DESC, event_id
    ) AS row_num_inside_day
FROM course05_sales_events;
```

## PARTITION BY bucket pattern
`PARTITION BY` creates buckets for calculations but keeps all rows visible.

```sql
SELECT
    event_id,
    sale_date,
    revenue,
    SUM(revenue) OVER (PARTITION BY sale_date) AS daily_total
FROM course05_sales_events;
```

## Rank patterns
`RANK()` leaves gaps after ties. `DENSE_RANK()` does not.

```sql
SELECT
    sale_date,
    event_id,
    revenue,
    RANK() OVER (PARTITION BY sale_date ORDER BY revenue DESC) AS rank_num,
    DENSE_RANK() OVER (PARTITION BY sale_date ORDER BY revenue DESC) AS dense_rank_num
FROM course05_sales_events;
```

## LAG/LEAD pattern
`LAG()` looks backward. `LEAD()` looks forward. Both require `ORDER BY` in the window.

```sql
SELECT
    sale_date,
    event_id,
    revenue,
    LAG(revenue) OVER (PARTITION BY region ORDER BY sale_date, event_id) AS prev_revenue,
    LEAD(revenue) OVER (PARTITION BY region ORDER BY sale_date, event_id) AS next_revenue
FROM course05_sales_events;
```

## Running total pattern

```sql
SELECT
    sale_date,
    event_id,
    revenue,
    SUM(revenue) OVER (
        ORDER BY sale_date, event_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_revenue
FROM course05_sales_events;
```

## Moving average pattern

```sql
SELECT
    sale_date,
    event_id,
    revenue,
    AVG(revenue) OVER (
        ORDER BY sale_date, event_id
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3_rows
FROM course05_sales_events;
```

## Percent of group total pattern

```sql
SELECT
    sale_date,
    event_id,
    revenue,
    revenue / SUM(revenue) OVER (PARTITION BY sale_date) AS pct_of_daily_total
FROM course05_sales_events;
```

## Named WINDOW pattern
Named windows save partition/order/frame rules, not the function itself.

```sql
SELECT
    sale_date,
    event_id,
    revenue,
    SUM(revenue) OVER daily_window AS daily_running_total,
    AVG(revenue) OVER daily_window AS daily_running_avg
FROM course05_sales_events
WINDOW daily_window AS (
    PARTITION BY sale_date
    ORDER BY event_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
);
```

## NTILE pattern
`NTILE(4)` creates quartile-style buckets inside each partition.

```sql
SELECT
    region,
    sale_date,
    event_id,
    revenue,
    NTILE(4) OVER (
        PARTITION BY region
        ORDER BY revenue DESC
    ) AS revenue_quartile_in_region
FROM course05_sales_events;
```
## Window Function Cheat Sheet
- `ROW_NUMBER` = unique row position
- `RANK` = ties share rank, gaps happen
- `DENSE_RANK` = ties share rank, no gaps
- `LAG` = previous row
- `LEAD` = next row
- `SUM OVER` = total or running total (depends on frame)
- `AVG OVER` = average or moving average (depends on frame)
- `NTILE` = bucket assignment
- `percentile_cont` = actual percentile value

## DataCamp Pattern: ORDER BY inside OVER

```sql
SELECT
    Year,
    Event,
    ROW_NUMBER() OVER (ORDER BY Year DESC) AS row_num_recent_first
FROM Summer_Medals;
```

```sql
SELECT
    Year,
    Event,
    ROW_NUMBER() OVER (ORDER BY Year DESC, Event ASC) AS row_num_recent_event
FROM Summer_Medals;
```

## DataCamp Pattern: LAG with CTE

```sql
WITH champions AS (
    SELECT
        Year,
        Athlete AS champion
    FROM Summer_Medals
    WHERE Event = 'Discus Throw'
      AND Medal = 'Gold'
)
SELECT
    Year,
    champion,
    LAG(champion, 1) OVER (
        ORDER BY Year ASC
    ) AS last_champion
FROM champions
ORDER BY Year ASC;
```

## Pattern: Summarize First, Then Rank

```sql
WITH Athlete_Medals AS (
SELECT
Athlete,
COUNT(*) AS Medals
FROM Summer_Medals
GROUP BY Athlete
)
SELECT
Athlete,
Medals,
RANK() OVER (
ORDER BY Medals DESC
) AS Rank_N
FROM Athlete_Medals
ORDER BY Medals DESC;
```

## Pattern: NTILE Then GROUP BY Bucket Summary

```sql
WITH Athlete_Medals AS (
SELECT
Athlete,
COUNT(*) AS Medals
FROM Summer_Medals
GROUP BY Athlete
HAVING COUNT(*) > 1
),
Thirds AS (
SELECT
Athlete,
Medals,
NTILE(3) OVER (
ORDER BY Medals DESC
) AS Third
FROM Athlete_Medals
)
SELECT
Third,
ROUND(AVG(Medals), 2) AS Avg_Medals
FROM Thirds
GROUP BY Third
ORDER BY Third ASC;
```

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

## Pattern: CROSSTAB Pivot (tablefunc)
```sql
CREATE EXTENSION IF NOT EXISTS tablefunc;

SELECT *
FROM CROSSTAB($$
  SELECT
    Gender,
    Year,
    Country
  FROM Summer_Medals
  WHERE Year IN (2008, 2012)
    AND Medal = 'Gold'
    AND Event = 'Pole Vault'
  ORDER BY Gender ASC, Year ASC
$$) AS ct (
  Gender VARCHAR,
  "2008" VARCHAR,
  "2012" VARCHAR
)
ORDER BY Gender ASC;
```

## Pattern: ROLLUP with COALESCE Labels
```sql
SELECT
  COALESCE(Country, 'All countries') AS Country,
  COALESCE(Gender, 'All genders') AS Gender,
  COUNT(*) AS Awards
FROM Summer_Medals
WHERE Year = 2004
  AND Medal = 'Gold'
  AND Country IN ('DEN', 'NOR', 'SWE')
GROUP BY ROLLUP(Country, Gender);
```

## Pattern: Rank Then STRING_AGG
```sql
WITH Country_Medals AS (
  SELECT Country, COUNT(*) AS Medals
  FROM Summer_Medals
  WHERE Year = 2000 AND Medal = 'Gold'
  GROUP BY Country
),
Country_Ranks AS (
  SELECT Country, RANK() OVER (ORDER BY Medals DESC) AS Rank
  FROM Country_Medals
)
SELECT STRING_AGG(Country, ', ' ORDER BY Rank) AS Top_Countries
FROM Country_Ranks
WHERE Rank <= 3;
```

## Pattern: FILTER Pivot (Multi-measure)
Use FILTER/CASE when CROSSTAB needs more than one cell value.

