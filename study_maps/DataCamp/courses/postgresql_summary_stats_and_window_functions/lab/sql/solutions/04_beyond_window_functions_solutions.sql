\set ON_ERROR_STOP on
SET search_path TO dc_window_lab, public;

-- 1. Optional extension. This may require elevated privileges.
CREATE EXTENSION IF NOT EXISTS tablefunc;

-- 2. Basic pivot.
SELECT *
FROM CROSSTAB(
  $$
    SELECT
        country,
        year,
        COUNT(*)::integer AS awards
    FROM dc_window_lab.summer_medals
    WHERE country IN ('CHN', 'RUS', 'USA')
      AND year IN (2008, 2012)
      AND medal = 'Gold'
    GROUP BY country, year
    ORDER BY country, year
  $$
) AS ct (
    country text,
    "2008" integer,
    "2012" integer
)
ORDER BY country;

-- 3. Rank first, then pivot.
DROP TABLE IF EXISTS dc_window_lab.country_rank_source;

CREATE TEMP TABLE country_rank_source AS
WITH country_awards AS (
    SELECT
        country,
        year,
        COUNT(*) AS awards
    FROM summer_medals
    WHERE country IN ('CHN', 'RUS', 'USA')
      AND year IN (2008, 2012)
      AND medal = 'Gold'
    GROUP BY country, year
)
SELECT
    country,
    year,
    RANK() OVER (
        PARTITION BY year
        ORDER BY awards DESC
    )::integer AS rank_n
FROM country_awards;

SELECT *
FROM CROSSTAB(
  $$
    SELECT country, year, rank_n
    FROM country_rank_source
    ORDER BY country, year
  $$
) AS ct (
    country text,
    "2008" integer,
    "2012" integer
)
ORDER BY country;

-- 4. Country-level subtotals with ROLLUP.
SELECT
    country,
    medal,
    COUNT(*) AS awards
FROM summer_medals
WHERE year = 2008
  AND country IN ('CHN', 'RUS')
GROUP BY country, ROLLUP(medal)
ORDER BY country, medal;

-- 5. All subtotal combinations with CUBE.
SELECT
    country,
    medal,
    COUNT(*) AS awards
FROM summer_medals
WHERE year = 2008
  AND country IN ('CHN', 'RUS')
GROUP BY CUBE(country, medal)
ORDER BY country, medal;

-- 6. Readable subtotal labels.
SELECT
    COALESCE(country, 'All countries') AS country,
    COALESCE(medal, 'All medals') AS medal,
    COUNT(*) AS awards
FROM summer_medals
WHERE year = 2008
  AND country IN ('CHN', 'RUS')
GROUP BY ROLLUP(country, medal)
ORDER BY country, medal;

-- 7. Ordered one-row ranking summary.
WITH country_medals AS (
    SELECT
        country,
        COUNT(*) AS medals
    FROM summer_medals
    WHERE year = 2012
      AND country IN ('CHN', 'RUS', 'USA')
      AND medal = 'Gold'
    GROUP BY country
),
country_ranks AS (
    SELECT
        country,
        RANK() OVER (
            ORDER BY medals DESC
        ) AS rank_n
    FROM country_medals
)
SELECT
    STRING_AGG(country, ', ' ORDER BY rank_n, country) AS ranked_countries
FROM country_ranks;
