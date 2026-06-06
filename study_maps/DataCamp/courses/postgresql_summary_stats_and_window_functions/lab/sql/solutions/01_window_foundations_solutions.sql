\set ON_ERROR_STOP on
SET search_path TO dc_window_lab, public;

-- 1. GROUP BY collapses rows.
SELECT country, COUNT(*) AS medals
FROM summer_medals
WHERE country IS NOT NULL
GROUP BY country
ORDER BY medals DESC, country
LIMIT 20;

-- Window count preserves medal-level rows.
SELECT
    year,
    athlete,
    country,
    medal,
    COUNT(*) OVER (
        PARTITION BY country
    ) AS country_medals
FROM summer_medals
WHERE country IS NOT NULL
ORDER BY country, year, athlete
LIMIT 50;

-- 2. Global chronological row numbering.
SELECT
    year,
    event,
    athlete,
    country,
    ROW_NUMBER() OVER (
        ORDER BY year, event, athlete, medal_id
    ) AS row_n
FROM summer_medals
WHERE medal = 'Gold'
ORDER BY row_n
LIMIT 50;

-- 3. Row numbering independently per country.
SELECT
    year,
    event,
    athlete,
    country,
    ROW_NUMBER() OVER (
        PARTITION BY country
        ORDER BY year, event, athlete, medal_id
    ) AS row_n
FROM summer_medals
WHERE medal = 'Gold'
  AND country IS NOT NULL
ORDER BY country, row_n
LIMIT 100;

-- 4. Women’s Discus Throw champions since 2000.
SELECT
    year,
    athlete,
    ROW_NUMBER() OVER (
        ORDER BY year, athlete
    ) AS champion_n
FROM (
    SELECT DISTINCT year, athlete
    FROM summer_medals
    WHERE medal = 'Gold'
      AND event = 'Discus Throw'
      AND gender = 'Women'
      AND year >= 2000
) AS champions
ORDER BY year, athlete;

-- 5.
-- ORDER BY inside OVER() controls the sequence used by the window calculation.
-- The final ORDER BY controls how result rows are displayed.
