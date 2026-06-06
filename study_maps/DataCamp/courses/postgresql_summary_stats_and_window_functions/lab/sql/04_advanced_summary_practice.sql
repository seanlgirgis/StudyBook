SET search_path TO dc_window_functions, public;

-- Hierarchical subtotals with ROLLUP.
SELECT
    year,
    country,
    COUNT(*) AS medal_count
FROM summer_medals
GROUP BY ROLLUP (year, country)
ORDER BY year NULLS LAST, country NULLS LAST;

-- All subtotal combinations with CUBE.
SELECT
    sport,
    medal,
    COUNT(*) AS medal_count
FROM summer_medals
GROUP BY CUBE (sport, medal)
ORDER BY sport NULLS LAST, medal NULLS LAST;

-- Compress event names into one row per sport.
SELECT
    sport,
    STRING_AGG(DISTINCT event, ', ' ORDER BY event) AS events
FROM summer_medals
GROUP BY sport
ORDER BY sport;

-- Optional pivot support.
CREATE EXTENSION IF NOT EXISTS tablefunc;
