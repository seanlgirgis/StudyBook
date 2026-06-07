SET search_path TO dc_functions, public;

-- Normalize names and email addresses.
SELECT customer_id,
       INITCAP(TRIM(first_name) || ' ' || TRIM(last_name)) AS display_name,
       LOWER(email) AS normalized_email
FROM customer
ORDER BY customer_id;

-- Parse only rows containing the delimiter.
SELECT customer_id, email,
       SUBSTRING(LOWER(email) FROM 1 FOR POSITION('@' IN LOWER(email)) - 1) AS username,
       SUBSTRING(LOWER(email) FROM POSITION('@' IN LOWER(email)) + 1) AS domain
FROM customer
WHERE POSITION('@' IN email) > 0
ORDER BY customer_id;

-- Surface malformed rows instead of slicing them blindly.
SELECT customer_id, email
FROM customer
WHERE POSITION('@' IN email) = 0;

-- Build a padded display label.
SELECT LPAD(customer_id::text, 6, '0') || ' - ' ||
       INITCAP(TRIM(first_name) || ' ' || TRIM(last_name)) AS customer_label
FROM customer
ORDER BY customer_id;

-- Reformat descriptions.
SELECT title,
       LEFT(description, 35) AS preview,
       REPLACE(description, 'A Astounding', 'An Astounding') AS corrected_description
FROM film
ORDER BY title;
