-- Course 06 PostgreSQL Functions Lab
-- Purpose:
-- Create small local practice tables for PostgreSQL data functions.

SET search_path TO course06_functions_lab;

CREATE TABLE lab_customers (
    customer_id integer PRIMARY KEY,
    first_name varchar(50),
    last_name varchar(50),
    email varchar(120),
    create_date date,
    favorite_tags text[]
);

CREATE TABLE lab_films (
    film_id integer PRIMARY KEY,
    title varchar(120),
    description text,
    rating varchar(10),
    rental_duration integer,
    special_features text[]
);

CREATE TABLE lab_rentals (
    rental_id integer PRIMARY KEY,
    customer_id integer REFERENCES lab_customers(customer_id),
    film_id integer REFERENCES lab_films(film_id),
    rental_date timestamp,
    return_date timestamp
);

CREATE TABLE lab_payments (
    payment_id integer PRIMARY KEY,
    customer_id integer REFERENCES lab_customers(customer_id),
    rental_id integer REFERENCES lab_rentals(rental_id),
    amount decimal(6,2),
    payment_date timestamp
);

CREATE TABLE lab_dirty_text (
    dirty_id integer PRIMARY KEY,
    raw_text text,
    raw_code text,
    comparison_text text
);
