SET search_path TO database_design_lab, public;

CREATE VIEW v_customer_sales AS
SELECT dc.customer_name,
       count(DISTINCT f.order_id) AS orders,
       sum(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_customer dc USING (customer_key)
GROUP BY dc.customer_name;

CREATE MATERIALIZED VIEW mv_product_sales AS
SELECT dp.product_name,
       sum(f.quantity) AS units,
       sum(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_product dp USING (product_key)
GROUP BY dp.product_name;

CREATE ROLE database_design_analyst NOLOGIN;
GRANT USAGE ON SCHEMA database_design_lab TO database_design_analyst;
GRANT SELECT ON v_customer_sales, mv_product_sales TO database_design_analyst;

CREATE TABLE operational_event (
  event_id bigint GENERATED ALWAYS AS IDENTITY,
  event_time timestamptz NOT NULL,
  event_type text NOT NULL,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb
) PARTITION BY RANGE (event_time);

CREATE TABLE operational_event_2026_06
PARTITION OF operational_event
FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');

CREATE TABLE operational_event_2026_07
PARTITION OF operational_event
FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');

INSERT INTO operational_event (event_time,event_type,payload) VALUES
('2026-06-05','ORDER_PAID','{"order_id":1}'),
('2026-07-02','ORDER_SHIPPED','{"order_id":2}');
