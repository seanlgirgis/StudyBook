SET search_path TO dc_functions, public;

CREATE TABLE customer (
  customer_id integer PRIMARY KEY,
  first_name text,
  last_name text,
  email text,
  create_date date NOT NULL
);

CREATE TABLE film (
  film_id integer PRIMARY KEY,
  title text NOT NULL,
  description text NOT NULL,
  rental_duration integer NOT NULL CHECK (rental_duration > 0),
  rental_rate numeric(5,2) NOT NULL,
  special_features text[] NOT NULL DEFAULT ARRAY[]::text[]
);

CREATE TABLE rental (
  rental_id integer PRIMARY KEY,
  customer_id integer NOT NULL REFERENCES customer(customer_id),
  film_id integer NOT NULL REFERENCES film(film_id),
  rental_date timestamp NOT NULL,
  return_date timestamp
);
