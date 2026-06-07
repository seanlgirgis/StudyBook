SET search_path TO dc_functions, public;

-- Inspect data types and underlying PostgreSQL types.
SELECT column_name, data_type, udt_name, numeric_precision, numeric_scale
FROM information_schema.columns
WHERE table_schema = 'dc_functions'
  AND table_name = 'film'
ORDER BY ordinal_position;

-- Match one scalar against array elements.
SELECT title, special_features
FROM film
WHERE 'Trailers' = ANY (special_features)
ORDER BY title;

-- Require array containment.
SELECT title, special_features
FROM film
WHERE special_features @> ARRAY['Trailers','Commentaries']::text[];

-- Inspect result types.
SELECT pg_typeof(special_features) AS array_type,
       pg_typeof(rental_rate) AS rate_type
FROM film
LIMIT 1;
