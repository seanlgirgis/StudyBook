\set ON_ERROR_STOP on
SET search_path TO dc_window_lab, public;

-- 1. Running total of athlete medal counts.
WITH athlete_medals AS (
    SELECT athlete, COUNT(*) AS medals
    FROM summer_medals
    GROUP BY athlete
)
SELECT
    athlete,
    medals,
    SUM(medals) OVER (
        ORDER BY medals DESC, athlete
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_medals
FROM athlete_medals
ORDER BY medals DESC, athlete;

-- 2. Maximum annual Gold medals per country.
WITH country_year_gold AS (
    SELECT
        country,
        year,
        COUNT(*) AS gold_medals
    FROM summer_medals
    WHERE medal = 'Gold'
      AND country IS NOT NULL
    GROUP BY country, year
)
SELECT
    country,
    year,
    gold_medals,
    MAX(gold_medals) OVER (
        PARTITION BY country
    ) AS max_country_gold
FROM country_year_gold
ORDER BY country, year;

-- 3. Minimum annual Gold medals per country.
WITH country_year_gold AS (
    SELECT
        country,
        year,
        COUNT(*) AS gold_medals
    FROM summer_medals
    WHERE medal = 'Gold'
      AND country IS NOT NULL
    GROUP BY country, year
)
SELECT
    country,
    year,
    gold_medals,
    MIN(gold_medals) OVER (
        PARTITION BY country
    ) AS min_country_gold
FROM country_year_gold
ORDER BY country, year;

-- 4. Centered moving maximum for Scandinavian countries.
WITH scandinavian_medals AS (
    SELECT
        country,
        year,
        COUNT(*) AS medals
    FROM summer_medals
    WHERE country IN ('DEN', 'FIN', 'NOR', 'SWE')
    GROUP BY country, year
)
SELECT
    country,
    year,
    medals,
    MAX(medals) OVER (
        PARTITION BY country
        ORDER BY year
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ) AS moving_max
FROM scandinavian_medals
ORDER BY country, year;

-- 5. Moving maximum for China.
WITH china_medals AS (
    SELECT
        year,
        COUNT(*) AS medals
    FROM summer_medals
    WHERE country = 'CHN'
    GROUP BY year
)
SELECT
    year,
    medals,
    MAX(medals) OVER (
        ORDER BY year
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_max
FROM china_medals
ORDER BY year;

-- 6. Three-row moving average for Russia.
WITH russian_medals AS (
    SELECT
        year,
        COUNT(*) AS medals
    FROM summer_medals
    WHERE country = 'RUS'
    GROUP BY year
)
SELECT
    year,
    medals,
    ROUND(
        AVG(medals) OVER (
            ORDER BY year
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moving_avg
FROM russian_medals
ORDER BY year;

-- 7. Three-row moving total per country.
WITH country_medals AS (
    SELECT
        country,
        year,
        COUNT(*) AS medals
    FROM summer_medals
    WHERE country IS NOT NULL
    GROUP BY country, year
)
SELECT
    country,
    year,
    medals,
    SUM(medals) OVER (
        PARTITION BY country
        ORDER BY year
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_total
FROM country_medals
ORDER BY country, year;

-- 8.
-- ROWS counts exact physical records relative to the current row.
-- RANGE includes logical peers sharing the same ORDER BY value.
