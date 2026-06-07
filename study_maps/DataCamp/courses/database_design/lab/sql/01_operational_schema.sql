SET search_path TO database_design_lab, public;

CREATE TABLE customer (
  customer_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_name text NOT NULL,
  email text NOT NULL UNIQUE,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE product (
  product_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  product_name text NOT NULL,
  current_price numeric(10,2) NOT NULL CHECK (current_price >= 0)
);

CREATE TABLE sales_order (
  order_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id bigint NOT NULL REFERENCES customer(customer_id),
  ordered_at timestamptz NOT NULL DEFAULT now(),
  status text NOT NULL CHECK (status IN ('NEW','PAID','SHIPPED','CANCELLED'))
);

CREATE TABLE sales_order_item (
  order_id bigint NOT NULL REFERENCES sales_order(order_id),
  line_number integer NOT NULL CHECK (line_number > 0),
  product_id bigint NOT NULL REFERENCES product(product_id),
  quantity integer NOT NULL CHECK (quantity > 0),
  unit_price numeric(10,2) NOT NULL CHECK (unit_price >= 0),
  PRIMARY KEY (order_id, line_number)
);
