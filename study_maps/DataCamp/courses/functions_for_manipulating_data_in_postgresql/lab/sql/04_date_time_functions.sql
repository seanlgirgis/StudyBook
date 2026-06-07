SET search_path TO dc_functions, public;

-- Elapsed rental time.
SELECT rental_id, return_date - rental_date AS elapsed
FROM rental
WHERE return_date IS NOT NULL
ORDER BY rental_id;

-- Expected return timestamp.
SELECT r.rental_id, r.rental_date, f.rental_duration,
       r.rental_date + f.rental_duration * INTERVAL '1 day' AS expected_return
FROM rental AS r
JOIN film AS f USING (film_id)
ORDER BY r.rental_id;

-- Static overdue check for reproducibility.
SELECT r.rental_id, f.title,
       r.rental_date + f.rental_duration * INTERVAL '1 day' AS expected_return
FROM rental AS r
JOIN film AS f USING (film_id)
WHERE r.return_date IS NULL
  AND TIMESTAMP '2026-04-15 00:00' >
      r.rental_date + f.rental_duration * INTERVAL '1 day';

-- Components and reporting buckets.
SELECT rental_id,
       EXTRACT(YEAR FROM rental_date) AS rental_year,
       DATE_PART('month', rental_date) AS rental_month_number,
       DATE_TRUNC('month', rental_date) AS rental_month
FROM rental
ORDER BY rental_date;

SELECT DATE_TRUNC('month', rental_date) AS rental_month, COUNT(*) AS rentals
FROM rental
GROUP BY rental_month
ORDER BY rental_month;
