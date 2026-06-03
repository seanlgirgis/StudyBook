-- 03_window_function_practice_queries.sql

-- 1) Inspect the table
SELECT *
FROM course05_sales_events
ORDER BY event_id
LIMIT 25;

-- 2) GROUP BY revenue by region (summary)
SELECT
    region,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(*) AS sales_rows
FROM course05_sales_events
GROUP BY region
ORDER BY region;

-- 3) Count rows per region while keeping each original row
SELECT
    event_id,
    region,
    revenue,
    COUNT(*) OVER (PARTITION BY region) AS region_row_count
FROM course05_sales_events
ORDER BY event_id;

-- 4) Add row number over sale_date order
SELECT
    event_id,
    sale_date,
    region,
    revenue,
    ROW_NUMBER() OVER (ORDER BY sale_date, event_id) AS row_num_by_date
FROM course05_sales_events
ORDER BY sale_date, event_id;

-- 5) Row number inside each region by highest revenue first
SELECT
    event_id,
    region,
    revenue,
    ROW_NUMBER() OVER (PARTITION BY region ORDER BY revenue DESC, event_id) AS revenue_row_num_in_region
FROM course05_sales_events
ORDER BY region, revenue_row_num_in_region;

-- 6) Compare RANK and DENSE_RANK for revenue inside each region
SELECT
    event_id,
    region,
    revenue,
    RANK() OVER (PARTITION BY region ORDER BY revenue DESC) AS revenue_rank,
    DENSE_RANK() OVER (PARTITION BY region ORDER BY revenue DESC) AS revenue_dense_rank
FROM course05_sales_events
ORDER BY region, revenue DESC, event_id;

-- 7) Compare each sale revenue with the previous sale in same region by date
SELECT
    event_id,
    region,
    sale_date,
    revenue,
    LAG(revenue) OVER (PARTITION BY region ORDER BY sale_date, event_id) AS previous_revenue,
    ROUND(
        revenue - LAG(revenue) OVER (PARTITION BY region ORDER BY sale_date, event_id),
        2
    ) AS revenue_change
FROM course05_sales_events
ORDER BY region, sale_date, event_id;

-- 8) Running total revenue by date
SELECT
    event_id,
    sale_date,
    revenue,
    ROUND(
        SUM(revenue) OVER (
            ORDER BY sale_date, event_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS running_total_revenue
FROM course05_sales_events
ORDER BY sale_date, event_id;

-- 9) Moving average revenue by date (3-row window)
SELECT
    event_id,
    sale_date,
    revenue,
    ROUND(
        AVG(revenue) OVER (
            ORDER BY sale_date, event_id
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moving_avg_3_rows
FROM course05_sales_events
ORDER BY sale_date, event_id;

-- 10) Percent of regional total revenue for each row
SELECT
    event_id,
    region,
    revenue,
    ROUND(
        100.0 * revenue / SUM(revenue) OVER (PARTITION BY region),
        2
    ) AS pct_of_region_revenue
FROM course05_sales_events
ORDER BY region, pct_of_region_revenue DESC, event_id;