\set ON_ERROR_STOP on
SET search_path TO dc_window_lab, public;

SELECT
    COUNT(*) AS row_count,
    COUNT(DISTINCT year) AS distinct_years,
    MIN(year) AS first_year,
    MAX(year) AS last_year,
    COUNT(DISTINCT country) AS distinct_countries,
    COUNT(DISTINCT athlete) AS distinct_athletes,
    COUNT(DISTINCT event) AS distinct_events,
    COUNT(DISTINCT discipline) AS distinct_disciplines,
    COUNT(DISTINCT sport) AS distinct_sports,
    COUNT(DISTINCT city) AS distinct_cities
FROM summer_medals;

SELECT medal, COUNT(*) AS rows_per_medal
FROM summer_medals
GROUP BY medal
ORDER BY medal;

SELECT gender, COUNT(*) AS rows_per_gender
FROM summer_medals
GROUP BY gender
ORDER BY gender;
