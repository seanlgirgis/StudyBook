-- 07_validation_queries.sql
-- Basic validation checks for row counts, ranges, categories, and sanity.

-- Row counts
SELECT 'sales_events' AS table_name, COUNT(*) AS row_count FROM course05_muscle.sales_events
UNION ALL
SELECT 'employee_sales', COUNT(*) FROM course05_muscle.employee_sales
UNION ALL
SELECT 'server_telemetry', COUNT(*) FROM course05_muscle.server_telemetry
UNION ALL
SELECT 'olympic_medals_practice', COUNT(*) FROM course05_muscle.olympic_medals_practice
UNION ALL
SELECT 'support_tickets', COUNT(*) FROM course05_muscle.support_tickets;

-- Samples
SELECT * FROM course05_muscle.sales_events LIMIT 10;
SELECT * FROM course05_muscle.employee_sales LIMIT 10;
SELECT * FROM course05_muscle.server_telemetry LIMIT 10;
SELECT * FROM course05_muscle.olympic_medals_practice LIMIT 10;
SELECT * FROM course05_muscle.support_tickets LIMIT 10;

-- Date/time ranges
SELECT MIN(sale_date) AS min_sale_date, MAX(sale_date) AS max_sale_date FROM course05_muscle.sales_events;
SELECT MIN(sale_month) AS min_sale_month, MAX(sale_month) AS max_sale_month FROM course05_muscle.employee_sales;
SELECT MIN(sample_ts) AS min_sample_ts, MAX(sample_ts) AS max_sample_ts FROM course05_muscle.server_telemetry;
SELECT MIN(year) AS min_year, MAX(year) AS max_year FROM course05_muscle.olympic_medals_practice;
SELECT MIN(opened_ts) AS min_opened_ts, MAX(opened_ts) AS max_opened_ts FROM course05_muscle.support_tickets;

-- Distinct category checks
SELECT DISTINCT region FROM course05_muscle.sales_events ORDER BY region;
SELECT DISTINCT product_category FROM course05_muscle.sales_events ORDER BY product_category;
SELECT DISTINCT channel FROM course05_muscle.sales_events ORDER BY channel;

SELECT DISTINCT department FROM course05_muscle.employee_sales ORDER BY department;

SELECT DISTINCT environment FROM course05_muscle.server_telemetry ORDER BY environment;
SELECT DISTINCT service_name FROM course05_muscle.server_telemetry ORDER BY service_name;

SELECT DISTINCT country FROM course05_muscle.olympic_medals_practice ORDER BY country;
SELECT DISTINCT event FROM course05_muscle.olympic_medals_practice ORDER BY event;

SELECT DISTINCT priority FROM course05_muscle.support_tickets ORDER BY priority;
SELECT DISTINCT assigned_team FROM course05_muscle.support_tickets ORDER BY assigned_team;

-- Sanity queries
SELECT region, ROUND(AVG(revenue),2) AS avg_rev, COUNT(*) AS rows_n
FROM course05_muscle.sales_events
GROUP BY region
ORDER BY region;

SELECT department, ROUND(AVG(sales_amount),2) AS avg_sales
FROM course05_muscle.employee_sales
GROUP BY department
ORDER BY department;

SELECT environment, ROUND(percentile_cont(0.95) WITHIN GROUP (ORDER BY cpu_pct)::numeric,2) AS p95_cpu
FROM course05_muscle.server_telemetry
GROUP BY environment
ORDER BY environment;

SELECT year, country, COUNT(*) AS medals
FROM course05_muscle.olympic_medals_practice
WHERE medal = 'Gold'
GROUP BY year, country
ORDER BY year, medals DESC
LIMIT 20;

SELECT priority, ROUND(AVG(resolution_minutes),2) AS avg_resolution
FROM course05_muscle.support_tickets
GROUP BY priority
ORDER BY priority;
