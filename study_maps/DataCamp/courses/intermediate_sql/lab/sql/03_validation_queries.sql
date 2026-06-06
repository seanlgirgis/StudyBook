-- Intermediate SQL course lab
-- Basic checks after loading the schema and sample data.

SET search_path TO intermediate_sql, public;

SELECT *
FROM films
ORDER BY film_id;

SELECT COUNT(*) AS total_films
FROM films;

SELECT COUNT(budget) AS films_with_known_budget
FROM films;

SELECT COUNT(DISTINCT country) AS distinct_countries
FROM films;

SELECT DISTINCT country
FROM films
ORDER BY country;

SELECT title,
       release_year,
       country,
       genre,
       imdb_score
FROM films
ORDER BY release_year, title;
