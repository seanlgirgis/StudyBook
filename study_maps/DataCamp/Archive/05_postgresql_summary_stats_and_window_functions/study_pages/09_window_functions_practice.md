# Window Functions Practice (From Local Lab)

## 1) ROW_NUMBER by sale_date
```sql
SELECT
    sale_date,
    event_id,
    revenue,
    ROW_NUMBER() OVER (
        PARTITION BY sale_date
        ORDER BY revenue DESC, event_id
    ) AS row_num_inside_day
FROM course05_sales_events
ORDER BY sale_date, row_num_inside_day;
```

## 2) ROW_NUMBER vs RANK vs DENSE_RANK (2025-01-01)
```sql
SELECT
    sale_date,
    event_id,
    revenue,
    ROW_NUMBER() OVER (
        PARTITION BY sale_date
        ORDER BY revenue DESC, event_id
    ) AS row_num,
    RANK() OVER (
        PARTITION BY sale_date
        ORDER BY revenue DESC
    ) AS rank_num,
    DENSE_RANK() OVER (
        PARTITION BY sale_date
        ORDER BY revenue DESC
    ) AS dense_rank_num
FROM course05_sales_events
WHERE sale_date = '2025-01-01'
ORDER BY revenue DESC, event_id;
```

## 3) LAG and LEAD
```sql
SELECT
    region,
    sale_date,
    event_id,
    revenue,
    LAG(revenue) OVER (PARTITION BY region ORDER BY sale_date, event_id) AS prev_revenue,
    LEAD(revenue) OVER (PARTITION BY region ORDER BY sale_date, event_id) AS next_revenue
FROM course05_sales_events
ORDER BY region, sale_date, event_id;
```

## 4) LAG with CTE and percent change
```sql
WITH lagged AS (
    SELECT
        region,
        sale_date,
        event_id,
        revenue,
        LAG(revenue) OVER (
            PARTITION BY region
            ORDER BY sale_date, event_id
        ) AS previous_revenue
    FROM course05_sales_events
)
SELECT
    region,
    sale_date,
    event_id,
    revenue,
    previous_revenue,
    ROUND(
        100.0 * (revenue - previous_revenue) / NULLIF(previous_revenue, 0),
        2
    ) AS pct_change_from_previous
FROM lagged
ORDER BY region, sale_date, event_id;
```

## 5) Running total
```sql
SELECT
    sale_date,
    event_id,
    revenue,
    SUM(revenue) OVER (
        ORDER BY sale_date, event_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_revenue
FROM course05_sales_events
ORDER BY sale_date, event_id;
```

## 6) Moving average
```sql
SELECT
    sale_date,
    event_id,
    revenue,
    AVG(revenue) OVER (
        ORDER BY sale_date, event_id
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3_rows
FROM course05_sales_events
ORDER BY sale_date, event_id;
```

## 7) Named WINDOW example
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
)
ORDER BY sale_date, event_id;
```

## 8) NTILE example
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
FROM course05_sales_events
WHERE region = 'South'
ORDER BY sale_date, event_id;
```

## Lab data corrections we made
- Initial table had one event per day, which weakened `PARTITION BY sale_date`.
- Seed was fixed to 25 dates with 4 events per date.
- Ranking ties were added inside same-day partitions.
- Revenue distribution was made less smooth so NTILE looked realistic.
## Practice Queries We Actually Used

### ROW_NUMBER inside sale_date
What question this answers: Which row is 1st, 2nd, 3rd, 4th inside each day by revenue?
What to look for in the output: Row numbers restart for each sale date.
Plain-English nugget: numbering is per bucket, not global.

```sql
SELECT
    sale_date,
    event_id,
    revenue,
    ROW_NUMBER() OVER (
        PARTITION BY sale_date
        ORDER BY revenue DESC, event_id
    ) AS row_num_inside_day
FROM course05_sales_events
ORDER BY sale_date, row_num_inside_day;
```

### ROW_NUMBER vs RANK vs DENSE_RANK for 2025-01-01
What question this answers: How do ties change ranking style?
What to look for in the output: `700,700` tie shares rank in `RANK`/`DENSE_RANK`; only `RANK` leaves a gap.
Plain-English nugget: same sort order, different tie behavior.

```sql
SELECT
    sale_date,
    event_id,
    revenue,
    ROW_NUMBER() OVER (
        PARTITION BY sale_date
        ORDER BY revenue DESC, event_id
    ) AS row_num,
    RANK() OVER (
        PARTITION BY sale_date
        ORDER BY revenue DESC
    ) AS rank_num,
    DENSE_RANK() OVER (
        PARTITION BY sale_date
        ORDER BY revenue DESC
    ) AS dense_rank_num
FROM course05_sales_events
WHERE sale_date = '2025-01-01'
ORDER BY revenue DESC, event_id;
```

### LAG previous revenue
What question this answers: What was the previous revenue in this region sequence?
What to look for in the output: first row per region has NULL previous value.
Plain-English nugget: LAG peeks one row back in ordered history.

```sql
SELECT
    region,
    sale_date,
    event_id,
    revenue,
    LAG(revenue) OVER (
        PARTITION BY region
        ORDER BY sale_date, event_id
    ) AS previous_revenue
FROM course05_sales_events
ORDER BY region, sale_date, event_id;
```

### LAG + CTE + percent change using NULLIF
What question this answers: How much did revenue change from previous event?
What to look for in the output: percent change is NULL when previous is NULL or zero-safe guarded.
Plain-English nugget: compute once in CTE, reuse cleanly in final SELECT.

```sql
WITH lagged AS (
    SELECT
        region,
        sale_date,
        event_id,
        revenue,
        LAG(revenue) OVER (
            PARTITION BY region
            ORDER BY sale_date, event_id
        ) AS previous_revenue
    FROM course05_sales_events
)
SELECT
    region,
    sale_date,
    event_id,
    revenue,
    previous_revenue,
    ROUND(
        100.0 * (revenue - previous_revenue) / NULLIF(previous_revenue, 0),
        2
    ) AS pct_change_from_previous
FROM lagged
ORDER BY region, sale_date, event_id;
```

### LEAD next revenue
What question this answers: What is the next revenue in this ordered sequence?
What to look for in the output: last row per region has NULL next value.
Plain-English nugget: LEAD is the forward-looking sibling of LAG.

```sql
SELECT
    region,
    sale_date,
    event_id,
    revenue,
    LEAD(revenue) OVER (
        PARTITION BY region
        ORDER BY sale_date, event_id
    ) AS next_revenue
FROM course05_sales_events
ORDER BY region, sale_date, event_id;
```

### Running total with full history frame
What question this answers: What is cumulative revenue up to this row?
What to look for in the output: value only grows as rows progress.
Plain-English nugget: this is a rolling sum from start to current row.

```sql
SELECT
    sale_date,
    event_id,
    revenue,
    SUM(revenue) OVER (
        ORDER BY sale_date, event_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_revenue
FROM course05_sales_events
ORDER BY sale_date, event_id;
```

### Moving average with 2 preceding rows
What question this answers: What is local short-term smoothing of revenue?
What to look for in the output: first rows use smaller frame until enough prior rows exist.
Plain-English nugget: moving average trades noise for trend.

```sql
SELECT
    sale_date,
    event_id,
    revenue,
    AVG(revenue) OVER (
        ORDER BY sale_date, event_id
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3_rows
FROM course05_sales_events
ORDER BY sale_date, event_id;
```

### Named WINDOW with SUM/AVG/MIN/MAX
What question this answers: Can we reuse one window definition across many metrics?
What to look for in the output: all four metrics share same partition/order/frame logic.
Plain-English nugget: named windows reduce repetition, not functionality.

```sql
SELECT
    sale_date,
    event_id,
    revenue,
    SUM(revenue) OVER daily_window AS running_sum,
    AVG(revenue) OVER daily_window AS running_avg,
    MIN(revenue) OVER daily_window AS running_min,
    MAX(revenue) OVER daily_window AS running_max
FROM course05_sales_events
WINDOW daily_window AS (
    PARTITION BY sale_date
    ORDER BY event_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
ORDER BY sale_date, event_id;
```

### NTILE(4) by region
What question this answers: Which quartile bucket is each row in by regional revenue?
What to look for in the output: bucket values 1-4 are mixed when final output is sorted by date.
Plain-English nugget: bucket assignment comes from window order, not display order.

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
FROM course05_sales_events
WHERE region = 'South'
ORDER BY sale_date, event_id;
```

### NTILE(100) telemetry bucket example
What question this answers: Which percentile-like bucket does each event fall into?
What to look for in the output: values from 1 to 100 as bucket labels.
Plain-English nugget: NTILE labels buckets; it does not return the true percentile value.

```sql
SELECT
    event_id,
    revenue,
    NTILE(100) OVER (ORDER BY revenue DESC) AS telemetry_percentile_bucket
FROM course05_sales_events
ORDER BY revenue DESC, event_id;
```

## DataCamp Practice: ORDER BY and LAG

### ROW_NUMBER by descending year
```sql
SELECT
    Year,
    Event,
    ROW_NUMBER() OVER (ORDER BY Year DESC) AS row_num_recent_first
FROM Summer_Medals;
```

### ROW_NUMBER by year and event
```sql
SELECT
    Year,
    Event,
    ROW_NUMBER() OVER (ORDER BY Year DESC, Event ASC) AS row_num_recent_event
FROM Summer_Medals;
```

### LAG champion pattern
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

## Milestone Practice: PARTITION and Fetching Functions

### LAG partitioned by event
```sql
WITH Event_Gold AS (
    SELECT DISTINCT
        event,
        year,
        country AS champion
    FROM summer_medals
    WHERE year >= 2000
      AND event IN ('Discus Throw', 'Triple Jump')
      AND medal = 'Gold'
)
SELECT
    event,
    year,
    champion,
    LAG(champion) OVER (
        PARTITION BY event
        ORDER BY year ASC
    ) AS last_champion
FROM Event_Gold
ORDER BY event, year;
```

### LAG partitioned by gender and event
```sql
WITH Athletics_Gold AS (
    SELECT DISTINCT
        gender,
        year,
        event,
        country
    FROM summer_medals
    WHERE year >= 2000
      AND discipline = 'Athletics'
      AND event IN ('100M', '10000M')
      AND medal = 'Gold'
)
SELECT
    gender,
    year,
    event,
    country AS champion,
    LAG(country) OVER (
        PARTITION BY gender, event
        ORDER BY year ASC
    ) AS last_champion
FROM Athletics_Gold
ORDER BY event, gender, year;
```

### Reigning champion CASE with one CTE
```sql
WITH Weightlifting_Reigning AS (
    SELECT
        year,
        country AS champion,
        LAG(country) OVER (
            ORDER BY year ASC
        ) AS last_champion
    FROM public.summer_medals
    WHERE discipline = 'Weightlifting'
      AND event = '69KG'
      AND gender = 'Men'
      AND medal = 'Gold'
)
SELECT
    year,
    champion,
    CASE
        WHEN champion = last_champion THEN 'Reigning'
        ELSE 'Not reigning'
    END AS reigning
FROM Weightlifting_Reigning
ORDER BY year ASC;
```

### LEAD(city, 1) and LEAD(city, 2)
```sql
SELECT
    year,
    city,
    LEAD(city, 1) OVER (ORDER BY year ASC) AS next_city,
    LEAD(city, 2) OVER (ORDER BY year ASC) AS city_after_next
FROM summer_medals
GROUP BY year, city
ORDER BY year ASC;
```

### FIRST_VALUE(city)
```sql
SELECT
    year,
    city,
    FIRST_VALUE(city) OVER (
        ORDER BY year ASC
    ) AS first_city
FROM summer_medals
GROUP BY year, city
ORDER BY year ASC;
```

### LAST_VALUE(city) with full frame
```sql
SELECT
    year,
    city,
    LAST_VALUE(city) OVER (
        ORDER BY year ASC
        ROWS BETWEEN UNBOUNDED PRECEDING
            AND UNBOUNDED FOLLOWING
    ) AS last_city
FROM summer_medals
GROUP BY year, city
ORDER BY year ASC;
```

## DataCamp Practice: Ranking and NTILE Paging

### Example 1: Rank athletes by medal count
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

### Example 2: Dense-rank athletes inside country
```sql
WITH Athlete_Medals AS (
SELECT
Country,
Athlete,
COUNT(*) AS Medals
FROM Summer_Medals
WHERE Country IN ('JPN', 'KOR')
AND Year >= 2000
GROUP BY Country, Athlete
HAVING COUNT(*) > 1
)

SELECT
Country,
Athlete,
Medals,
DENSE_RANK() OVER (
PARTITION BY Country
ORDER BY Medals DESC
) AS Rank_N
FROM Athlete_Medals
ORDER BY Country ASC, Rank_N ASC, Athlete ASC;
```

### Example 3: Page distinct events
```sql
WITH Events AS (
SELECT DISTINCT Event
FROM Summer_Medals
)

SELECT
Event,
NTILE(111) OVER (
ORDER BY Event ASC
) AS Page
FROM Events
ORDER BY Event ASC;
```

### Example 4: Split athletes into thirds by medals
```sql
WITH Athlete_Medals AS (
SELECT
Athlete,
COUNT(*) AS Medals
FROM Summer_Medals
GROUP BY Athlete
HAVING COUNT(*) > 1
)

SELECT
Athlete,
Medals,
NTILE(3) OVER (
ORDER BY Medals DESC
) AS Third
FROM Athlete_Medals
ORDER BY Medals DESC, Athlete ASC;
```

### Example 5: Average medals in each third
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

## DataCamp Completion Practice: Pivoting, Totals, and Lists

### CROSSTAB pivot example
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

### CROSSTAB ranking pivot
```sql
CREATE EXTENSION IF NOT EXISTS tablefunc;

SELECT *
FROM CROSSTAB($$
  WITH Country_Awards AS (
    SELECT Country, Year, COUNT(*) AS Awards
    FROM Summer_Medals
    WHERE Country IN ('FRA', 'GBR', 'GER')
      AND Year IN (2004, 2008, 2012)
      AND Medal = 'Gold'
    GROUP BY Country, Year
  )
  SELECT
    Country,
    Year,
    RANK() OVER (PARTITION BY Year ORDER BY Awards DESC)::INTEGER AS rank_n
  FROM Country_Awards
  ORDER BY Country ASC, Year ASC
$$) AS ct (
  Country VARCHAR,
  "2004" INTEGER,
  "2008" INTEGER,
  "2012" INTEGER
)
ORDER BY Country ASC;
```

### ROLLUP and CUBE examples
```sql
SELECT Country, Gender, COUNT(*) AS Gold_Awards
FROM Summer_Medals
WHERE Year = 2004
  AND Medal = 'Gold'
  AND Country IN ('DEN', 'NOR', 'SWE')
GROUP BY Country, ROLLUP(Gender)
ORDER BY Country ASC, Gender ASC;
```

```sql
SELECT Gender, Medal, COUNT(*) AS Awards
FROM Summer_Medals
WHERE Year = 2012
  AND Country = 'RUS'
GROUP BY CUBE(Gender, Medal)
ORDER BY Gender ASC, Medal ASC;
```

### STRING_AGG top-countries list
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

## Added Practice: FILTER multi-measure pivot and CASE ordering
See field guide final sections for exact SQL snippets.

