SET search_path TO database_design_lab, public;

-- Operational row counts and integrity
SELECT 'customer' AS object_name, count(*) FROM customer
UNION ALL SELECT 'sales_order', count(*) FROM sales_order
UNION ALL SELECT 'sales_order_item', count(*) FROM sales_order_item;

-- Analytical summaries
SELECT * FROM v_customer_sales ORDER BY customer_name;
SELECT * FROM mv_product_sales ORDER BY revenue DESC;

-- Freshness responsibility
REFRESH MATERIALIZED VIEW mv_product_sales;

-- Partition routing
SELECT tableoid::regclass AS physical_partition, count(*)
FROM operational_event
GROUP BY tableoid
ORDER BY physical_partition::text;

-- Planner evidence
EXPLAIN
SELECT *
FROM operational_event
WHERE event_time >= '2026-07-01'
  AND event_time <  '2026-08-01';

-- Effective privilege inspection
SELECT grantee, table_name, privilege_type
FROM information_schema.role_table_grants
WHERE grantee = 'database_design_analyst'
ORDER BY table_name, privilege_type;
