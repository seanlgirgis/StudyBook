-- 01_create_sales_events_table.sql
-- Create the table used in Course 05 window function practice.

DROP TABLE IF EXISTS course05_sales_events;

CREATE TABLE course05_sales_events (
    event_id INTEGER PRIMARY KEY,
    sale_date DATE,
    region TEXT,
    store_id INTEGER,
    salesperson TEXT,
    product_category TEXT,
    revenue NUMERIC,
    units_sold INTEGER,
    customer_score INTEGER
);