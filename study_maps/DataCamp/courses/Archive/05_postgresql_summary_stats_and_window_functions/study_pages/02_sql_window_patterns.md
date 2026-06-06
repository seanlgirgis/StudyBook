# Course 05 SQL Window Patterns

## Pattern 1 — Detail rows plus group total
```sql
SELECT
  region,
  sale_date,
  event_id,
  revenue,
  SUM(revenue) OVER (
    PARTITION BY region
  ) AS region_total_revenue
FROM sales_events;
```

Use when you need both detail and group context.

## Pattern 2 — Running total
```sql
SELECT
  region,
  sale_date,
  event_id,
  revenue,
  SUM(revenue) OVER (
    PARTITION BY region
    ORDER BY sale_date, event_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_region_revenue
FROM sales_events;
```

`ORDER BY` inside `OVER` makes it cumulative.

## Pattern 3 — Moving average / moving total
```sql
SELECT
  region,
  sale_date,
  event_id,
  revenue,
  AVG(revenue) OVER (
    PARTITION BY region
    ORDER BY sale_date, event_id
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS revenue_ma_3,
  SUM(revenue) OVER (
    PARTITION BY region
    ORDER BY sale_date, event_id
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS revenue_mt_3
FROM sales_events;
```

`AVG` = moving average.  
`SUM` = moving total.

## Pattern 4 — Previous-row comparison with LAG
```sql
WITH lagged_sales AS (
  SELECT
    region,
    sale_date,
    event_id,
    revenue,
    LAG(revenue) OVER (
      PARTITION BY region
      ORDER BY sale_date, event_id
    ) AS previous_revenue
  FROM sales_events
)
SELECT
  region,
  sale_date,
  event_id,
  revenue,
  previous_revenue,
  revenue - previous_revenue AS revenue_diff,
  ROUND(
    100.0 * (revenue - previous_revenue) / NULLIF(previous_revenue, 0),
    2
  ) AS revenue_pct_change
FROM lagged_sales;
```

## Pattern 5 — Next-row comparison with LEAD
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
FROM sales_events;
```

Use `LEAD` when the business question looks forward instead of backward.

## Pattern 6 — FIRST_VALUE / LAST_VALUE
```sql
SELECT
  region,
  sale_date,
  event_id,
  revenue,
  FIRST_VALUE(revenue) OVER (
    PARTITION BY region
    ORDER BY sale_date, event_id
  ) AS first_region_revenue,
  LAST_VALUE(revenue) OVER (
    PARTITION BY region
    ORDER BY sale_date, event_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS last_region_revenue
FROM sales_events;
```

`LAST_VALUE` usually needs a full frame.

## Pattern 7 — Top N per group
```sql
WITH ranked_salespeople AS (
  SELECT
    region,
    salesperson,
    SUM(revenue) AS total_revenue,
    ROW_NUMBER() OVER (
      PARTITION BY region
      ORDER BY SUM(revenue) DESC, salesperson ASC
    ) AS rn
  FROM sales_events
  GROUP BY region, salesperson
)
SELECT
  region,
  salesperson,
  total_revenue
FROM ranked_salespeople
WHERE rn <= 2;
```

## Pattern 8 — Nth person per group / third salesperson pattern
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
WHERE sales_rank = 3;
```

Tie options:

- `ROW_NUMBER` = one exact third row
- `RANK` = all tied at third rank
- `DENSE_RANK` = third distinct sales tier

## Pattern 9 — Local peak / local valley
```sql
WITH region_neighbors AS (
  SELECT
    region,
    sale_date,
    event_id,
    revenue,
    LAG(revenue) OVER (
      PARTITION BY region
      ORDER BY sale_date, event_id
    ) AS previous_revenue,
    LEAD(revenue) OVER (
      PARTITION BY region
      ORDER BY sale_date, event_id
    ) AS next_revenue
  FROM sales_events
)
SELECT
  region,
  sale_date,
  event_id,
  revenue,
  CASE
    WHEN revenue > previous_revenue AND revenue > next_revenue THEN 'Local peak'
    WHEN revenue < previous_revenue AND revenue < next_revenue THEN 'Local valley'
    ELSE 'Neither'
  END AS local_shape
FROM region_neighbors;
```

## Pattern 10 — P95 cutoff and join-back
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
  CASE
    WHEN s.revenue >= p.p95_revenue THEN 'At or above P95'
    ELSE 'Below P95'
  END AS p95_band
FROM sales_events AS s
JOIN region_p95 AS p
  ON s.region = p.region;
```

## Pattern 11 — CUME_DIST banding
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
    ) AS revenue_cume_dist
  FROM sales_events
)
SELECT
  region,
  sale_date,
  event_id,
  revenue,
  CASE
    WHEN revenue_cume_dist >= 0.95 THEN 'Top 5%'
    WHEN revenue_cume_dist >= 0.80 THEN 'High'
    WHEN revenue_cume_dist >= 0.20 THEN 'Middle'
    ELSE 'Low'
  END AS revenue_band
FROM revenue_positions;
```

## Pattern 12 — Review queue
```sql
WITH revenue_bands AS (
  SELECT
    region,
    sale_date,
    event_id,
    salesperson,
    revenue,
    CASE
      WHEN CUME_DIST() OVER (
        PARTITION BY region
        ORDER BY revenue ASC
      ) >= 0.95 THEN 'Top 5%'
      WHEN CUME_DIST() OVER (
        PARTITION BY region
        ORDER BY revenue ASC
      ) >= 0.80 THEN 'High'
      WHEN CUME_DIST() OVER (
        PARTITION BY region
        ORDER BY revenue ASC
      ) >= 0.20 THEN 'Middle'
      ELSE 'Low'
    END AS revenue_band
  FROM sales_events
)
SELECT
  region,
  sale_date,
  event_id,
  salesperson,
  revenue,
  revenue_band
FROM revenue_bands
WHERE revenue_band IN ('Top 5%', 'High');
```

Summary report = `GROUP BY` band.  
Review queue = show detail rows for important bands.

## Pattern 13 — Owner-level weighted priority scoring
```sql
WITH revenue_bands AS (
  SELECT
    region,
    salesperson,
    CASE
      WHEN CUME_DIST() OVER (
        PARTITION BY region
        ORDER BY revenue ASC
      ) >= 0.95 THEN 'Top 5%'
      WHEN CUME_DIST() OVER (
        PARTITION BY region
        ORDER BY revenue ASC
      ) >= 0.80 THEN 'High'
      WHEN CUME_DIST() OVER (
        PARTITION BY region
        ORDER BY revenue ASC
      ) >= 0.20 THEN 'Middle'
      ELSE 'Low'
    END AS revenue_band
  FROM sales_events
),
priority_by_salesperson AS (
  SELECT
    region,
    salesperson,
    SUM(CASE WHEN revenue_band = 'Top 5%' THEN 1 ELSE 0 END) AS top_5_count,
    SUM(CASE WHEN revenue_band = 'High' THEN 1 ELSE 0 END) AS high_count,
    3 * SUM(CASE WHEN revenue_band = 'Top 5%' THEN 1 ELSE 0 END)
      + SUM(CASE WHEN revenue_band = 'High' THEN 1 ELSE 0 END) AS priority_score
  FROM revenue_bands
  WHERE revenue_band IN ('Top 5%', 'High')
  GROUP BY region, salesperson
)
SELECT
  region,
  salesperson,
  top_5_count,
  high_count,
  priority_score,
  RANK() OVER (
    PARTITION BY region
    ORDER BY priority_score DESC, salesperson ASC
  ) AS priority_rank
FROM priority_by_salesperson;
```

## Pattern 14 — Final recommended_action
```sql
SELECT
  region,
  salesperson,
  priority_score,
  CASE
    WHEN priority_score >= 20 THEN 'Immediate focus'
    WHEN priority_score >= 15 THEN 'High priority'
    ELSE 'Monitor'
  END AS recommended_action
FROM ranked_priority;
```

## Pattern 15 — CTE layering pattern
Durable structure:

prepare rows  
-> calculate window values  
-> create labels  
-> aggregate or filter  
-> rank final entities  
-> present result
