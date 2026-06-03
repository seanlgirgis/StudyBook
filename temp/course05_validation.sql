SELECT to_regclass('public.course05_sales_events') AS table_exists;
SELECT COUNT(*) AS row_count FROM course05_sales_events;
SELECT
  SUM(CASE WHEN event_id IS NULL THEN 1 ELSE 0 END) AS null_event_id,
  SUM(CASE WHEN sale_date IS NULL THEN 1 ELSE 0 END) AS null_sale_date,
  SUM(CASE WHEN region IS NULL THEN 1 ELSE 0 END) AS null_region,
  SUM(CASE WHEN store_id IS NULL THEN 1 ELSE 0 END) AS null_store_id,
  SUM(CASE WHEN salesperson IS NULL THEN 1 ELSE 0 END) AS null_salesperson,
  SUM(CASE WHEN product_category IS NULL THEN 1 ELSE 0 END) AS null_product_category,
  SUM(CASE WHEN revenue IS NULL THEN 1 ELSE 0 END) AS null_revenue,
  SUM(CASE WHEN units_sold IS NULL THEN 1 ELSE 0 END) AS null_units_sold
FROM course05_sales_events;
SELECT COUNT(DISTINCT region) AS distinct_regions FROM course05_sales_events;
SELECT region, COUNT(DISTINCT store_id) AS stores_per_region FROM course05_sales_events GROUP BY region ORDER BY region;
SELECT salesperson, COUNT(*) AS rows_per_salesperson FROM course05_sales_events GROUP BY salesperson HAVING COUNT(*) > 1 ORDER BY rows_per_salesperson DESC, salesperson;
SELECT revenue, COUNT(*) AS freq FROM course05_sales_events GROUP BY revenue HAVING COUNT(*) > 1 ORDER BY freq DESC, revenue LIMIT 20;

-- Smoke tests
SELECT event_id, region, COUNT(*) OVER (PARTITION BY region) AS region_row_count FROM course05_sales_events ORDER BY event_id LIMIT 10;
SELECT event_id, sale_date, ROW_NUMBER() OVER (ORDER BY sale_date, event_id) AS rn FROM course05_sales_events ORDER BY sale_date, event_id LIMIT 10;
SELECT event_id, region, revenue, RANK() OVER (PARTITION BY region ORDER BY revenue DESC) AS rnk FROM course05_sales_events ORDER BY region, rnk, event_id LIMIT 12;
SELECT event_id, region, revenue, DENSE_RANK() OVER (PARTITION BY region ORDER BY revenue DESC) AS drnk FROM course05_sales_events ORDER BY region, drnk, event_id LIMIT 12;
SELECT event_id, region, sale_date, revenue, LAG(revenue) OVER (PARTITION BY region ORDER BY sale_date, event_id) AS prev_rev FROM course05_sales_events ORDER BY region, sale_date, event_id LIMIT 12;
SELECT event_id, sale_date, revenue, SUM(revenue) OVER (ORDER BY sale_date, event_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total FROM course05_sales_events ORDER BY sale_date, event_id LIMIT 12;
SELECT event_id, sale_date, revenue, AVG(revenue) OVER (ORDER BY sale_date, event_id ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3 FROM course05_sales_events ORDER BY sale_date, event_id LIMIT 12;
SELECT event_id, region, revenue, 100.0 * revenue / SUM(revenue) OVER (PARTITION BY region) AS pct_region FROM course05_sales_events ORDER BY region, pct_region DESC, event_id LIMIT 12;
