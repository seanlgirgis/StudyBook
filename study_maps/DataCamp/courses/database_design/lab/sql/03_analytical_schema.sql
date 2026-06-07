SET search_path TO database_design_lab, public;

CREATE TABLE dim_customer (
  customer_key bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  source_customer_id bigint NOT NULL UNIQUE,
  customer_name text NOT NULL
);

CREATE TABLE dim_product (
  product_key bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  source_product_id bigint NOT NULL UNIQUE,
  product_name text NOT NULL
);

CREATE TABLE dim_date (
  date_key integer PRIMARY KEY,
  calendar_date date NOT NULL UNIQUE,
  month_name text NOT NULL,
  calendar_year integer NOT NULL
);

CREATE TABLE fact_sales (
  order_id bigint NOT NULL,
  line_number integer NOT NULL,
  date_key integer NOT NULL REFERENCES dim_date(date_key),
  customer_key bigint NOT NULL REFERENCES dim_customer(customer_key),
  product_key bigint NOT NULL REFERENCES dim_product(product_key),
  quantity integer NOT NULL,
  revenue numeric(12,2) NOT NULL,
  PRIMARY KEY (order_id, line_number)
);

INSERT INTO dim_customer (source_customer_id, customer_name)
SELECT customer_id, customer_name FROM customer;

INSERT INTO dim_product (source_product_id, product_name)
SELECT product_id, product_name FROM product;

INSERT INTO dim_date VALUES
(20260601,'2026-06-01','June',2026),
(20260602,'2026-06-02','June',2026);

INSERT INTO fact_sales
SELECT o.order_id, i.line_number,
       to_char(o.ordered_at,'YYYYMMDD')::integer,
       dc.customer_key, dp.product_key,
       i.quantity, i.quantity * i.unit_price
FROM sales_order o
JOIN sales_order_item i ON i.order_id=o.order_id
JOIN dim_customer dc ON dc.source_customer_id=o.customer_id
JOIN dim_product dp ON dp.source_product_id=i.product_id;
