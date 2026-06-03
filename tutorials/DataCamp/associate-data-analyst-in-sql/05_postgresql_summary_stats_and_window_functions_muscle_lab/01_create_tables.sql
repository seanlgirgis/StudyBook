-- 01_create_tables.sql
-- Defines all tables and useful indexes inside course05_muscle.

CREATE TABLE IF NOT EXISTS course05_muscle.sales_events (
    sale_id INTEGER PRIMARY KEY,
    sale_date DATE,
    region TEXT,
    salesperson TEXT,
    product_category TEXT,
    revenue NUMERIC(12,2),
    units INTEGER,
    channel TEXT
);

CREATE INDEX IF NOT EXISTS idx_sales_events_sale_date
    ON course05_muscle.sales_events (sale_date);

CREATE TABLE IF NOT EXISTS course05_muscle.employee_sales (
    sale_id INTEGER PRIMARY KEY,
    sale_month DATE,
    department TEXT,
    salesperson TEXT,
    sales_amount NUMERIC(12,2),
    deal_count INTEGER
);

CREATE INDEX IF NOT EXISTS idx_employee_sales_sale_month
    ON course05_muscle.employee_sales (sale_month);

CREATE TABLE IF NOT EXISTS course05_muscle.server_telemetry (
    sample_id INTEGER PRIMARY KEY,
    sample_ts TIMESTAMP,
    environment TEXT,
    service_name TEXT,
    host_name TEXT,
    cpu_pct NUMERIC(5,2),
    memory_pct NUMERIC(5,2),
    latency_ms NUMERIC(8,2),
    error_count INTEGER
);

CREATE INDEX IF NOT EXISTS idx_server_telemetry_sample_ts
    ON course05_muscle.server_telemetry (sample_ts);

CREATE TABLE IF NOT EXISTS course05_muscle.olympic_medals_practice (
    medal_id INTEGER PRIMARY KEY,
    year INTEGER,
    city TEXT,
    sport TEXT,
    discipline TEXT,
    athlete TEXT,
    country TEXT,
    gender TEXT,
    event TEXT,
    medal TEXT
);

CREATE INDEX IF NOT EXISTS idx_olympic_medals_year
    ON course05_muscle.olympic_medals_practice (year);

CREATE INDEX IF NOT EXISTS idx_olympic_medals_country
    ON course05_muscle.olympic_medals_practice (country);

CREATE TABLE IF NOT EXISTS course05_muscle.support_tickets (
    ticket_id INTEGER PRIMARY KEY,
    opened_ts TIMESTAMP,
    customer_segment TEXT,
    product_area TEXT,
    priority TEXT,
    status TEXT,
    assigned_team TEXT,
    resolution_minutes INTEGER
);

CREATE INDEX IF NOT EXISTS idx_support_tickets_opened_ts
    ON course05_muscle.support_tickets (opened_ts);
