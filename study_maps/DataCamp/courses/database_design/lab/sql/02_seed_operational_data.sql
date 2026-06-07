SET search_path TO database_design_lab, public;

INSERT INTO customer (customer_name, email) VALUES
('Amina Hassan','amina@example.com'),
('David Lee','david@example.com');

INSERT INTO product (product_name, current_price) VALUES
('Keyboard',49.00),('Monitor',220.00),('Mouse',25.00);

INSERT INTO sales_order (customer_id, ordered_at, status) VALUES
(1,'2026-06-01 09:00-05','PAID'),
(2,'2026-06-02 14:30-05','SHIPPED');

INSERT INTO sales_order_item VALUES
(1,1,1,1,49.00),
(1,2,3,2,25.00),
(2,1,2,1,220.00);
