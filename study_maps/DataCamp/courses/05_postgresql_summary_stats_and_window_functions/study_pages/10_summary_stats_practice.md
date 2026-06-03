# Summary Stats Practice (From Local Lab)

## 1) Daily average with GROUP BY
```sql
SELECT
    sale_date,
    ROUND(AVG(revenue), 2) AS avg_daily_revenue,
    SUM(revenue) AS total_daily_revenue,
    COUNT(*) AS events_that_day
FROM course05_sales_events
GROUP BY sale_date
ORDER BY sale_date;
```

## 2) Moving average across daily averages
```sql
WITH daily AS (
    SELECT
        sale_date,
        AVG(revenue) AS avg_daily_revenue
    FROM course05_sales_events
    GROUP BY sale_date
)
SELECT
    sale_date,
    ROUND(avg_daily_revenue, 2) AS avg_daily_revenue,
    ROUND(
        AVG(avg_daily_revenue) OVER (
            ORDER BY sale_date
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moving_avg_of_daily_avg_3d
FROM daily
ORDER BY sale_date;
```

## 3) Percent of daily revenue
```sql
SELECT
    sale_date,
    event_id,
    revenue,
    ROUND(
        100.0 * revenue / SUM(revenue) OVER (PARTITION BY sale_date),
        2
    ) AS pct_of_daily_revenue
FROM course05_sales_events
ORDER BY sale_date, event_id;
```

## 4) Percent of region revenue
```sql
SELECT
    region,
    sale_date,
    event_id,
    revenue,
    ROUND(
        100.0 * revenue / SUM(revenue) OVER (PARTITION BY region),
        2
    ) AS pct_of_region_revenue
FROM course05_sales_events
ORDER BY region, sale_date, event_id;
```

## 5) P95 telemetry-style example
`NTILE(100)` can label percentile-style buckets, but true P95 should use percentile functions.

```sql
SELECT
    percentile_cont(0.95) WITHIN GROUP (ORDER BY revenue) AS p95_revenue_cont,
    percentile_disc(0.95) WITHIN GROUP (ORDER BY revenue) AS p95_revenue_disc
FROM course05_sales_events;
```
## Two-Level Analytics Pattern

### Idea
- Step 1: use `GROUP BY` to create daily summaries.
- Step 2: run window functions on those daily summaries.
- Example: daily average revenue, then 3-day moving average of daily averages.

### Complete SQL
```sql
WITH daily_summary AS (
    SELECT
        sale_date,
        AVG(revenue) AS avg_daily_revenue,
        SUM(revenue) AS total_daily_revenue,
        COUNT(*) AS events_that_day
    FROM course05_sales_events
    GROUP BY sale_date
)
SELECT
    sale_date,
    ROUND(avg_daily_revenue, 2) AS avg_daily_revenue,
    total_daily_revenue,
    events_that_day,
    ROUND(
        AVG(avg_daily_revenue) OVER (
            ORDER BY sale_date
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moving_avg_of_daily_avg_3d,
    SUM(total_daily_revenue) OVER (
        ORDER BY sale_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_of_daily_revenue
FROM daily_summary
ORDER BY sale_date;
```

## Completion Note
- percentile_cont/disc are true percentile value tools; NTILE is bucket labeling.

