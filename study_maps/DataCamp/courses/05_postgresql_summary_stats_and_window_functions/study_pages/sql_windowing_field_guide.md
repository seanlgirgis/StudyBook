# SQL Window Functions Field Guide (Markdown Twin)

> Markdown is the editable source of truth.  
> HTML is the polished reading version.

Source HTML used: `sql_windowing_guide.html`

## Table of Contents
1. The Big Idea — What is a Window?
2. OVER() — The Magic Clause
3. GROUP BY vs PARTITION BY
4. ORDER BY Inside OVER
5. ROW_NUMBER()
6. RANK()
7. DENSE_RANK()
8. Ranking Comparison
9. LAG() — Look Backward
10. LEAD() — Look Forward
11. LAG/LEAD with CTE Pattern
12. FIRST_VALUE / LAST_VALUE *(Advanced/Preview)*
13. SUM / AVG / MIN / MAX / COUNT
14. Running Totals
15. Moving Averages
16. Percent of Total
17. ROWS vs RANGE *(Advanced/Preview)*
18. Frame Boundaries Explained
19. Named WINDOW Clause
20. NTILE() — Bucketing
21. percentile_cont vs percentile_disc *(Advanced/Preview)*
21A. CUME_DIST and PERCENT_RANK
21B. P95 Cutoff vs CUME_DIST Coverage
21C. Percentile Banding and Review Queues
21D. Owner Priority Scoring Pipeline
22. CTE and Subquery Patterns
23. NULLIF and Safe Division
24. Interview Cheatsheet
36. Final Oral Defense Q&A

## 1) The Big Idea — What is a Window?
A window function calculates across related rows while keeping original rows visible.

> **Nugget**  
> GROUP BY collapses rows. Window functions keep rows and add context.

## 2) OVER() — The Magic Clause
`OVER()` turns aggregate/ranking/offset functions into window functions.

```sql
SELECT
    sale_date,
    event_id,
    revenue,
    SUM(revenue) OVER (PARTITION BY sale_date) AS daily_total
FROM sales;
```

> **Nugget**  
> `OVER()` defines the window context: partition, order, and optional frame.

## 3) GROUP BY vs PARTITION BY
- `GROUP BY`: summarize and collapse rows.
- `PARTITION BY`: bucket rows for calculation but keep all rows.

```sql
-- GROUP BY collapses
SELECT sale_date, SUM(revenue) AS total_rev
FROM sales
GROUP BY sale_date;

-- PARTITION BY keeps detail rows
SELECT
    sale_date,
    event_id,
    revenue,
    SUM(revenue) OVER (PARTITION BY sale_date) AS total_rev_that_day
FROM sales;
```

## 4) ORDER BY Inside OVER
`ORDER BY` inside `OVER()` controls calculation order.
Final `ORDER BY` controls display order.

```sql
SELECT
    sale_date,
    event_id,
    revenue,
    SUM(revenue) OVER (
        PARTITION BY sale_date
        ORDER BY event_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_in_day
FROM sales
ORDER BY sale_date, event_id;
```

## 5) ROW_NUMBER()
```sql
SELECT
    sale_date,
    event_id,
    revenue,
    ROW_NUMBER() OVER (
        PARTITION BY sale_date
        ORDER BY revenue DESC, event_id
    ) AS row_num_inside_day
FROM sales;
```

## 6) RANK()
```sql
SELECT
    sale_date,
    event_id,
    revenue,
    RANK() OVER (
        PARTITION BY sale_date
        ORDER BY revenue DESC
    ) AS rank_num
FROM sales;
```

## 7) DENSE_RANK()
```sql
SELECT
    sale_date,
    event_id,
    revenue,
    DENSE_RANK() OVER (
        PARTITION BY sale_date
        ORDER BY revenue DESC
    ) AS dense_rank_num
FROM sales;
```

## 8) Ranking Comparison
```sql
SELECT
    sale_date,
    event_id,
    revenue,
    ROW_NUMBER() OVER (PARTITION BY sale_date ORDER BY revenue DESC, event_id) AS row_num,
    RANK() OVER (PARTITION BY sale_date ORDER BY revenue DESC) AS rank_num,
    DENSE_RANK() OVER (PARTITION BY sale_date ORDER BY revenue DESC) AS dense_rank_num
FROM sales
WHERE sale_date = '2025-01-01'
ORDER BY revenue DESC, event_id;
```

## 9) LAG() — Look Backward
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
FROM sales;
```

## 10) LEAD() — Look Forward
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
FROM sales;
```

## 11) LAG/LEAD with CTE Pattern
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
    FROM sales
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
FROM lagged;
```

## 12) FIRST_VALUE / LAST_VALUE *(Advanced/Preview)*
```sql
SELECT
    sale_date,
    event_id,
    revenue,
    FIRST_VALUE(revenue) OVER (
        PARTITION BY sale_date
        ORDER BY revenue DESC
    ) AS first_rev,
    LAST_VALUE(revenue) OVER (
        PARTITION BY sale_date
        ORDER BY revenue DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_rev
FROM sales;
```

## 13) SUM / AVG / MIN / MAX / COUNT
```sql
SELECT
    region,
    sale_date,
    event_id,
    revenue,
    SUM(revenue) OVER (PARTITION BY region) AS sum_for_region,
    AVG(revenue) OVER (PARTITION BY region) AS avg_for_region,
    MIN(revenue) OVER (PARTITION BY region) AS min_for_region,
    MAX(revenue) OVER (PARTITION BY region) AS max_for_region,
    COUNT(*) OVER (PARTITION BY region) AS count_for_region
FROM sales;
```

## 14) Running Totals
```sql
SELECT
    sale_date,
    event_id,
    revenue,
    SUM(revenue) OVER (
        ORDER BY sale_date, event_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_revenue
FROM sales;
```

## 15) Moving Averages
```sql
SELECT
    sale_date,
    event_id,
    revenue,
    AVG(revenue) OVER (
        ORDER BY sale_date, event_id
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3_rows
FROM sales;
```

## 16) Percent of Total
```sql
SELECT
    sale_date,
    event_id,
    revenue,
    100.0 * revenue / SUM(revenue) OVER (PARTITION BY sale_date) AS pct_of_daily_total
FROM sales;
```

## 17) ROWS vs RANGE *(Advanced/Preview)*
- `ROWS`: physical row-count frame.
- `RANGE`: value-based frame from ORDER BY value.

```sql
-- ROWS (physical)
SUM(revenue) OVER (
  ORDER BY sale_date, event_id
  ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)

-- RANGE (value-based)
SUM(revenue) OVER (
  ORDER BY sale_date
  RANGE BETWEEN INTERVAL '2 day' PRECEDING AND CURRENT ROW
)
```

## 18) Frame Boundaries Explained
```sql
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
```

## 19) Named WINDOW Clause
```sql
SELECT
    region,
    sale_date,
    event_id,
    revenue,
    SUM(revenue)   OVER region_window         AS sum_for_region,
    AVG(revenue)   OVER region_window         AS avg_for_region,
    COUNT(*)       OVER region_window         AS count_for_region,
    RANK()         OVER region_ordered_window AS rank_in_region
FROM sales
WINDOW
    region_window AS (
        PARTITION BY region
    ),
    region_ordered_window AS (
        PARTITION BY region
        ORDER BY revenue DESC
    )
ORDER BY region, revenue DESC;
```

> **Nugget**  
> WINDOW stores the reusable window definition, not the function itself.

## 20) NTILE() — Bucketing
```sql
SELECT
    region,
    sale_date,
    event_id,
    revenue,
    NTILE(4) OVER (
        PARTITION BY region
        ORDER BY revenue DESC
    ) AS revenue_quartile
FROM sales
WHERE region = 'South'
ORDER BY sale_date, event_id;
```

> **Nugget**  
> `NTILE` assigns bucket labels. It does not compute true percentile threshold values.

## 21) percentile_cont vs percentile_disc *(Advanced/Preview)*
```sql
SELECT
    percentile_cont(0.95) WITHIN GROUP (ORDER BY cpu_pct) AS cpu_p95_cont,
    percentile_disc(0.95) WITHIN GROUP (ORDER BY cpu_pct) AS cpu_p95_disc
FROM telemetry_cpu_raw;
```

```sql
SELECT
    region,
    env,
    COUNT(*) AS sample_count,
    ROUND(percentile_cont(0.95) WITHIN GROUP (ORDER BY cpu_pct)::numeric, 2) AS cpu_p95,
    ROUND(percentile_cont(0.50) WITHIN GROUP (ORDER BY cpu_pct)::numeric, 2) AS cpu_median
FROM lab.telemetry_cpu_raw
GROUP BY region, env
ORDER BY cpu_p95 DESC;
```

## 21A) CUME_DIST and PERCENT_RANK — Row Position Functions
`CUME_DIST` and `PERCENT_RANK` are row-position functions. They use `OVER()` because they label every row with a relative position inside a partition.

- `CUME_DIST` = fraction of rows at or below the current value.
- `PERCENT_RANK` = where the current value starts on the ranking ladder.
- Both are useful when every row needs a relative position inside its own group.

> **Memory lines**
> - `CUME_DIST = coverage so far`
> - `PERCENT_RANK = rank-start position`
> - `CUME_DIST looks after the tie group`
> - `PERCENT_RANK looks at where the tie group starts`

```sql
WITH revenue_positions AS (
    SELECT
        region,
        sale_date,
        event_id,
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
    region,
    sale_date,
    event_id,
    revenue,
    ROUND(revenue_cume_dist::numeric, 4) AS revenue_cume_dist,
    ROUND(revenue_percent_rank::numeric, 4) AS revenue_percent_rank
FROM revenue_positions
ORDER BY region ASC, revenue DESC, event_id ASC;
```

Tie reminder: `CUME_DIST` counts through the end of a tie group. `PERCENT_RANK` uses where the tie group starts. That is why they can disagree around tied values without either one being wrong.

Interview line: `CUME_DIST` is coverage-based row positioning. `PERCENT_RANK` is rank-start positioning.

## 21B) P95 Cutoff vs CUME_DIST Coverage
These tools answer different questions:

- P95 = one cutoff value per group.
- `CUME_DIST` = row-level relative coverage.
- `PERCENT_RANK` = row-level rank-start position.
- `NTILE` = bucket label, not a true percentile value.

| Method | Output | Best for |
| --- | --- | --- |
| `P95 / percentile_cont` | one threshold value per group | SLA cutoffs, telemetry thresholds, join-back labeling |
| `CUME_DIST` | one relative-coverage value per row | row-by-row top-percent flags |
| `PERCENT_RANK` | one rank-start value per row | ranking ladder position |
| `NTILE` | one bucket label per row | quartiles, thirds, paging |

> **Nugget**  
> Percentile gives the cutoff. Join attaches the cutoff. CASE labels the row.

```sql
WITH region_p95 AS (
    SELECT
        region,
        percentile_cont(0.95) WITHIN GROUP (ORDER BY revenue) AS p95_revenue
    FROM sales_events
    GROUP BY region
)
SELECT
    s.region,
    s.sale_date,
    s.event_id,
    s.revenue,
    p.p95_revenue,
    CASE
        WHEN s.revenue >= p.p95_revenue THEN 'At or above P95'
        ELSE 'Below P95'
    END AS p95_band
FROM sales_events AS s
JOIN region_p95 AS p
  ON s.region = p.region
ORDER BY s.region ASC, s.revenue DESC, s.event_id ASC;
```

```sql
WITH revenue_positions AS (
    SELECT
        region,
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
        percentile_cont(0.95) WITHIN GROUP (ORDER BY revenue) AS p95_revenue
    FROM sales_events
    GROUP BY region
),
compare_methods AS (
    SELECT
        r.region,
        CASE
            WHEN r.revenue_cume_dist >= 0.95 THEN 'Top 5%'
            ELSE 'Below Top 5%'
        END AS cume_dist_band,
        CASE
            WHEN r.revenue >= p.p95_revenue THEN 'Top 5%'
            ELSE 'Below Top 5%'
        END AS p95_band
    FROM revenue_positions AS r
    JOIN region_p95 AS p
      ON r.region = p.region
)
SELECT
    cume_dist_band,
    p95_band,
    COUNT(*) AS row_count
FROM compare_methods
GROUP BY cume_dist_band, p95_band
ORDER BY cume_dist_band, p95_band;
```

If the disagreement count is zero, that is fine. It means the business definition and the observed data lined up cleanly.

## 21C) Percentile Banding and Review Queues
This is the business flow:

`raw value -> relative position -> business band -> review queue`

```sql
WITH revenue_positions AS (
    SELECT
        region,
        sale_date,
        event_id,
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
        region,
        sale_date,
        event_id,
        salesperson,
        revenue,
        revenue_cume_dist,
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
    sale_date,
    event_id,
    salesperson,
    revenue,
    revenue_band
FROM revenue_bands
WHERE revenue_band IN ('Top 5%', 'High')
ORDER BY
    region ASC,
    CASE
        WHEN revenue_band = 'Top 5%' THEN 1
        WHEN revenue_band = 'High' THEN 2
        ELSE 3
    END,
    revenue DESC,
    event_id ASC;
```

- `CASE` creates the bands.
- `WHERE` selects the review queue.
- Final `ORDER BY` controls urgency on screen.

Summary report vs review queue:
- Summary report = `GROUP BY revenue_band` and count rows.
- Review queue = `WHERE revenue_band IN (...)` and keep detail rows.

Interview line: I turned row-level percentile positions into business bands, then filtered the bands that deserved attention into a review queue.

## 21D) Owner Priority Scoring Pipeline
This is the owner-priority pipeline:

`raw rows -> CUME_DIST -> revenue_band -> review queue -> owner summary -> weighted priority_score -> priority_rank -> recommended_action`

```sql
WITH revenue_positions AS (
    SELECT
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
        region,
        salesperson,
        revenue,
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
        SUM(
            CASE
                WHEN revenue_band = 'Top 5%' THEN 3
                WHEN revenue_band = 'High' THEN 1
                ELSE 0
            END
        ) AS weighted_priority_score
    FROM revenue_bands
    WHERE revenue_band IN ('Top 5%', 'High')
    GROUP BY region, salesperson
),
ranked_priority AS (
    SELECT
        region,
        salesperson,
        top_5_count,
        high_count,
        weighted_priority_score,
        RANK() OVER (
            PARTITION BY region
            ORDER BY weighted_priority_score DESC, salesperson ASC
        ) AS priority_rank
    FROM priority_by_salesperson
)
SELECT
    region,
    salesperson,
    top_5_count,
    high_count,
    weighted_priority_score,
    priority_rank,
    CASE
        WHEN weighted_priority_score >= 20 THEN 'Immediate focus'
        WHEN weighted_priority_score >= 15 THEN 'High priority'
        ELSE 'Monitor'
    END AS recommended_action
FROM ranked_priority
ORDER BY region ASC, priority_rank ASC, salesperson ASC;
```

- Conditional `SUM` counts signals by band.
- Weights create urgency.
- `GROUP BY` turns row-level urgency into owner-level priority.
- `RANK` orders owners inside each region.
- `CASE at the end turns analytics into a business recommendation.`

> **Memory lines**
> - `Banding creates categories.`
> - `Weights create urgency.`
> - `GROUP BY turns row-level urgency into owner-level priority.`
> - `CASE at the end turns analytics into a business recommendation.`
> - `Raw rows -> signals -> scores -> ranked recommendations.`

This same pattern can translate to sales performance, fraud, customer risk, observability alerts, incident triage, and capacity prioritization.

## 22) CTE and Subquery Patterns
```sql
WITH years AS (
    SELECT DISTINCT year
    FROM summer_medals
)
SELECT
    year,
    ROW_NUMBER() OVER (ORDER BY year ASC) AS row_n
FROM years
ORDER BY year;
```

```sql
WITH daily AS (
    SELECT sale_date, SUM(revenue) AS daily_rev
    FROM sales
    GROUP BY sale_date
)
SELECT
    sale_date,
    daily_rev,
    AVG(daily_rev) OVER (
        ORDER BY sale_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7d_avg
FROM daily;
```

## 23) NULLIF and Safe Division
```sql
ROUND(
    100.0 * (revenue - previous_revenue)
        / NULLIF(previous_revenue, 0),
    2
) AS pct_change
```

> **Nugget**  
> `NULLIF(x, 0)` is a divide-by-zero airbag.

## 24) Interview Cheatsheet
- `OVER()` activates window behavior
- `PARTITION BY` buckets rows
- `ORDER BY` in `OVER` controls calculation order
- `ROW_NUMBER` unique sequence
- `RANK` ties with gaps
- `DENSE_RANK` ties without gaps
- `LAG` previous row, `LEAD` next row
- `ROWS BETWEEN` controls frame
- `WINDOW` names reusable definition
- `NTILE` bucket label
- `percentile_cont` percentile value
- `NULLIF` safe division

> **Sean sentence**  
> "Window functions let me calculate rankings, previous/next comparisons, running totals, moving averages, and percent-of-total metrics while keeping the original detail rows visible. GROUP BY collapses rows, but window functions add analytical context to each row without losing granularity."
## DataCamp Note: ORDER BY inside OVER
In DataCamp Course 05 examples, `ORDER BY` inside `OVER` determines calculation sequence (for example, recent year first), while final `ORDER BY` only changes display order.

## DataCamp Note: LAG
In the reigning champion pattern, `LAG(champion, 1)` returns the previous year's champion so current and prior values appear on the same row.

## DataCamp Note: CTE and Subquery Patterns
The `champions` CTE prepares the row set first, then the outer query applies window logic. This keeps the logic readable and avoids repeating filters.

## Milestone Status Before Fetching Functions
Before the fetching-functions section, Sean has already covered:
- `ORDER BY` inside `OVER`
- `PARTITION BY`
- `ROW_NUMBER`
- `RANK` and `DENSE_RANK`
- `LAG` and `LEAD`
- CTE/subquery preparation patterns
- `CASE` after `LAG` for business labels
- named `WINDOW` clause
- `NTILE`
- P95 concept (`percentile_cont` vs row buckets)

Fetching-functions section adds: `FIRST_VALUE` and `LAST_VALUE` with frame behavior details.

## PARTITION BY prevents wrong crossover
Without `PARTITION BY`, `LAG` can pull previous champions from unrelated events.

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

> **Nugget**  
> `PARTITION BY` tells `LAG` where not to cross boundaries.

## Multiple-column PARTITION BY
Use multiple columns when history must be split by combinations.

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

`PARTITION BY gender, event` creates separate histories for each gender/event combination.

## Reigning champion CASE pattern (one CTE)

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

`LAG` creates the previous-row value. `CASE` turns that comparison into a business label.

## Fetching functions family
- `LAG` = relative fetching, previous row
- `LEAD` = relative fetching, next row
- `FIRST_VALUE` = absolute fetching, first value in partition
- `LAST_VALUE` = absolute fetching, last value in partition (needs full frame)

## LAST_VALUE trap

```sql
LAST_VALUE(city) OVER (
    ORDER BY year
    ROWS BETWEEN UNBOUNDED PRECEDING
        AND UNBOUNDED FOLLOWING
) AS last_city
```

Without a full frame, `LAST_VALUE` often returns the current row because the default frame ends at `CURRENT ROW`.

## DataCamp Milestone: Ranking Section Completed

### Ranking recap from this milestone
- `ROW_NUMBER` gives unique row numbers even when values tie.
- `RANK` gives tied values the same rank and skips the next rank.
- `DENSE_RANK` gives tied values the same rank and does not skip.
- Ranking often needs summarize-first logic (for example: medal counts per athlete) before ranking.
- Use `PARTITION BY` when ranking inside multiple groups; otherwise ranking is global.

### Example: Rank athletes by medal count
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

### Example: Dense-rank athletes inside country
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

## DataCamp Milestone: NTILE / Paging Section Completed

### NTILE recap from this milestone
- `NTILE(n)` splits ordered rows into `n` approximately equal buckets/pages.
- With `ORDER BY Event ASC`, page labels follow alphabetical event ordering.
- `NTILE(3)` over medals can label top/middle/bottom third.
- `NTILE` does not preserve ties like ranking functions.
- `NTILE` labels buckets; it does not calculate a true percentile value.

### Example: Page distinct events
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

### Example: Split athletes into thirds by medals
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

### Example: Average medals in each third
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

## Interview Pattern: Nth Person per Group

Pattern:
1. Aggregate first by department and salesperson.
2. Rank inside each department.
3. Filter to rank = 3.

```sql
WITH salesperson_sales AS (
SELECT
department,
salesperson,
SUM(sales_amount) AS total_sales
FROM sales
GROUP BY department, salesperson
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
FROM salesperson_sales
)

SELECT
department,
salesperson,
total_sales
FROM ranked_salespeople
WHERE sales_rank = 3
ORDER BY department;
```

Use `RANK` instead of `ROW_NUMBER` if the business wants all tied third-place salespeople.

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

## CROSSTAB / Pivoting
`CROSSTAB` is PostgreSQL pivoting via the `tablefunc` extension. It reshapes tall rows into wide report columns. It is not a window function.

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

Notes:
- Simple CROSSTAB source query shape is `row id`, `category`, `cell value`.
- Output columns are declared manually in `AS ct (...)`.
- Year values like `2008`/`2012` do not auto-create columns.
- In simple form, source ordering must match declared output-column order.
- StudyBook style: no semicolon inside `$$`; semicolon after outer query.
- DataCamp accepted semicolon inside `$$`, but we avoid it here.
- One cell-value limitation: if you need medals + rank, use separate pivots or manual pivot (`FILTER`/`CASE`).

### Ranking pivot example
```sql
CREATE EXTENSION IF NOT EXISTS tablefunc;

SELECT *
FROM CROSSTAB($$
  WITH Country_Awards AS (
    SELECT
      Country,
      Year,
      COUNT(*) AS Awards
    FROM Summer_Medals
    WHERE Country IN ('FRA', 'GBR', 'GER')
      AND Year IN (2004, 2008, 2012)
      AND Medal = 'Gold'
    GROUP BY Country, Year
  )

  SELECT
    Country,
    Year,
    RANK() OVER (
      PARTITION BY Year
      ORDER BY Awards DESC
    )::INTEGER AS rank_n
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

## ROLLUP
`ROLLUP` is a `GROUP BY` extension, not a window function. It adds subtotal rows and can add a grand total. It is hierarchical, so column order matters.

```sql
SELECT
  Country,
  Gender,
  COUNT(*) AS Gold_Awards
FROM Summer_Medals
WHERE Year = 2004
  AND Medal = 'Gold'
  AND Country IN ('DEN', 'NOR', 'SWE')
GROUP BY Country, ROLLUP(Gender)
ORDER BY Country ASC, Gender ASC;
```

- `GROUP BY Country, ROLLUP(Gender)` => detail + subtotal per country.
- `GROUP BY ROLLUP(Country, Gender)` => detail + country subtotal + grand total.
- `NULL` in rollup output often means subtotal/grand total, not missing data.

## CUBE
`CUBE` is a `GROUP BY` extension, not a window function. It creates all subtotal combinations.

```sql
SELECT
  Gender,
  Medal,
  COUNT(*) AS Awards
FROM Summer_Medals
WHERE Year = 2012
  AND Country = 'RUS'
GROUP BY CUBE(Gender, Medal)
ORDER BY Gender ASC, Medal ASC;
```

Use `CUBE` when all subtotal angles are meaningful. Use `ROLLUP` when dimensions are hierarchical.

## COALESCE
`COALESCE` returns the first non-null value. In `ROLLUP`/`CUBE`, it labels subtotal `NULL`s. It cleans labels; it does not create totals.

```sql
SELECT
  COALESCE(Country, 'All countries') AS Country,
  COALESCE(Gender, 'All genders') AS Gender,
  COUNT(*) AS Awards
FROM Summer_Medals
WHERE Year = 2004
  AND Medal = 'Gold'
  AND Country IN ('DEN', 'NOR', 'SWE')
GROUP BY ROLLUP(Country, Gender)
ORDER BY Country ASC, Gender ASC;
```

```sql
ORDER BY
  CASE WHEN Country IS NULL THEN 2 ELSE 1 END,
  Country ASC,
  CASE
    WHEN Gender = 'Men' THEN 1
    WHEN Gender = 'Women' THEN 2
    WHEN Gender IS NULL THEN 3
  END;
```

## STRING_AGG
`STRING_AGG` compresses many rows into one list. Best pattern: rank first, then aggregate top rows. Use `ORDER BY` inside `STRING_AGG` to preserve rank order.

```sql
WITH Country_Medals AS (
  SELECT
    Country,
    COUNT(*) AS Medals
  FROM Summer_Medals
  WHERE Year = 2000
    AND Medal = 'Gold'
  GROUP BY Country
),

Country_Ranks AS (
  SELECT
    Country,
    RANK() OVER (
      ORDER BY Medals DESC
    ) AS Rank
  FROM Country_Medals
)

SELECT
  STRING_AGG(Country, ', ' ORDER BY Rank) AS Top_Countries
FROM Country_Ranks
WHERE Rank <= 3;
```

- `RANK` creates order.
- `WHERE Rank <= 3` filters top countries.
- `STRING_AGG` compresses to one row.

## Course 05 Final Map
- Window functions: keep detail rows and add context.
- CROSSTAB: reshape rows into report columns.
- ROLLUP/CUBE: add subtotal rows.
- COALESCE: clean NULL subtotal labels.
- STRING_AGG: compress rows into a list.
- FILTER/CASE manual pivot: use when multiple cell values are needed.

## Deep Completion Addendum (Full Learning Session)

### Foundation refresh
- Window functions keep detail rows visible.
- `GROUP BY` collapses rows.
- `OVER()` activates window behavior.
- `PARTITION BY` creates calculation groups without collapsing.
- `ORDER BY` inside `OVER` controls calculation order.
- Final `ORDER BY` controls display only.

### Unique years pattern (prepare rows first)
```sql
WITH Years AS (
  SELECT DISTINCT Year
  FROM Summer_Medals
)
SELECT
  Year,
  ROW_NUMBER() OVER (
    ORDER BY Year ASC
  ) AS Row_N
FROM Years
ORDER BY Year ASC;
```
Lesson: `ROW_NUMBER` numbers the rows it receives.

### Ranking tie warning
Do not add unique tie-breakers to `RANK`/`DENSE_RANK` when you want true ties.

### LAG / LEAD partition safety
Use `PARTITION BY` to stop crossover between unrelated groups.

### Fetching functions family
- `LAG` = relative previous row
- `LEAD` = relative next row
- `FIRST_VALUE` = absolute first value in partition/frame
- `LAST_VALUE` = absolute last value (needs full frame)

### LAST_VALUE trap reminder
```sql
LAST_VALUE(city) OVER (
  ORDER BY year
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
) AS last_city
```

### Moving average vs moving total
- `AVG` + sliding frame = moving average.
- `SUM` + sliding frame = moving total.
- Do not name `SUM` output `Medals_MA`.
- Better aliases: `Medals_MT`, `Moving_Total`, `Medals_3_Game_Total`.

### Country 3-game moving total
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

### Sample data realism
If sample data is too polished, correct SQL can look fake (for example NTILE labels).

### CROSSTAB details
`CROSSTAB` uses dollar-quoted SQL (`$$ ... $$`) and simple source shape:
- row identifier
- pivot category
- cell value

```sql
CREATE EXTENSION IF NOT EXISTS tablefunc;
```

### Multi-measure pivot preferred pattern (FILTER)
```sql
WITH country_medals AS (
  SELECT
    year,
    country,
    COUNT(*) AS medals
  FROM summer_medals
  WHERE country IN ('CHN', 'KOR', 'JPN')
    AND medal = 'Gold'
    AND year IN (2004, 2008, 2012)
  GROUP BY year, country
),
country_ranks AS (
  SELECT
    year,
    country,
    medals,
    RANK() OVER (
      PARTITION BY year
      ORDER BY medals DESC
    ) AS rank_n
  FROM country_medals
)
SELECT
  country,
  MAX(medals) FILTER (WHERE year = 2004) AS medals_2004,
  MAX(rank_n) FILTER (WHERE year = 2004) AS rank_2004,
  MAX(medals) FILTER (WHERE year = 2008) AS medals_2008,
  MAX(rank_n) FILTER (WHERE year = 2008) AS rank_2008,
  MAX(medals) FILTER (WHERE year = 2012) AS medals_2012,
  MAX(rank_n) FILTER (WHERE year = 2012) AS rank_2012
FROM country_ranks
GROUP BY country
ORDER BY country;
```

### CASE in ORDER BY
Use `CASE in ORDER BY` to force business display order for totals.

### Interview-safe line
For third salesperson: aggregate first, rank inside department, filter rank = 3.

## Interview Translation
> **CUME_DIST / P95 interview box**  
> `CUME_DIST` gives every row a relative position inside its own group. P95 gives one cutoff value for the group. If I need a row-by-row flag, `CUME_DIST` is often the simpler first move. If I need the actual 95th percentile threshold, I calculate `percentile_cont(0.95)` and join that value back to the detail rows.

> **Owner-priority pipeline interview box**  
> I started with raw sales rows, used `CUME_DIST` to place each sale relative to other sales in the same region, converted those positions into business bands, filtered a review queue, grouped the queue by salesperson, applied a weighted priority score, ranked owners inside each region, and added a final recommended action.

> **Final memory line**  
> `Raw rows -> signals -> scores -> ranked recommendations.`

## Common Traps
| Trap | Correction |
| --- | --- |
| Confusing `NTILE` with P95 | `NTILE creates bucket labels`. `P95 creates a cutoff value`. |
| Using `NTILE(100)` on fewer than 100 rows per group | Some bucket labels may never appear. Use it only when row count supports the question. |
| Thinking `percentile_cont` labels each row | It returns an aggregate cutoff value. Join it back, then use `CASE`. |
| Treating `CUME_DIST` and `PERCENT_RANK` as identical | Tie behavior differs. `CUME_DIST` looks after the tie group. `PERCENT_RANK` looks at where the tie group starts. |
| Forgetting the business definition | Top-percent logic depends on what the business means by top, flagged, urgent, or high risk. |
| Creating a score but not translating it | Add `recommended_action` with `CASE` so business readers know what to do next. |

## Flashcard Review
- `CUME_DIST`: coverage-based row position.
- `PERCENT_RANK`: rank-start row position.
- `P95`: true percentile cutoff value.
- `review queue`: detail rows filtered from the important bands.
- `weighted priority_score`: score that values stronger signals more heavily.
- `recommended_action`: business label such as `Immediate focus`, `High priority`, or `Monitor`.
- `Oral defense`: explain why the pipeline shape matters, not just the SQL syntax.

## 36) Final Oral Defense Q&A
**Q1. GROUP BY vs PARTITION BY?**  
`GROUP BY` collapses rows. `PARTITION BY` keeps detail rows and calculates inside buckets.

**Q2. What does ORDER BY inside OVER do?**  
It controls calculation order. Final `ORDER BY` controls display order.

**Q3. Why do ranking aliases often need a CTE before filtering?**  
Because the window result is created after the select list. Calculate first, filter in an outer query.

**Q4. Why avoid unique tie-breakers in RANK and DENSE_RANK?**  
Because a unique tie-breaker destroys ties and turns the ranking into fake uniqueness.

**Q5. What is the LAST_VALUE trap?**  
Default frame often ends at the current row, so `LAST_VALUE` can return the current row instead of the true last row.

**Q6. ROWS vs RANGE?**  
`ROWS` = physical rows. `RANGE` = value peers. `ROWS` is usually clearer for moving windows.

**Q7. NTILE vs P95?**  
`NTILE creates bucket labels`. `P95 creates a cutoff value`.

**Q8. Why does percentile_cont use WITHIN GROUP?**  
Because it is an ordered-set aggregate. It needs an ordered value list to compute the percentile threshold.

**Q9. What does CUME_DIST mean?**  
It means coverage so far: what fraction of rows are at or below this value.

**Q10. What does PERCENT_RANK mean?**  
It means rank-start position: where the current value starts on the ranking ladder.

**Q11. Why do CUME_DIST and PERCENT_RANK differ around ties?**  
`CUME_DIST` looks after the tie group. `PERCENT_RANK` looks at where the tie group starts.

**Q12. What was the final owner-priority pipeline?**  
Use row-level percentile signals, band them, filter a review queue, summarize by owner, weight the signals, rank the owners, and add a recommendation label.

**Q13. Shortest memory line?**  
`Raw rows -> signals -> scores -> ranked recommendations.`
