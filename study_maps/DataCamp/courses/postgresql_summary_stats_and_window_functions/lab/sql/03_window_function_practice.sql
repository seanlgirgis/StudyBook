SET search_path TO dc_window_functions, public;

-- 1. Number medals within each Olympic year.
SELECT
    year,
    athlete,
    country,
    medal,
    ROW_NUMBER() OVER (
        PARTITION BY year
        ORDER BY athlete, event, medal_id
    ) AS row_in_year
FROM summer_medals
ORDER BY year, row_in_year
LIMIT 50;

-- 2. Rank countries by Gold medals for each year.
WITH country_gold AS (
    SELECT year, country, COUNT(*) AS gold_medals
    FROM summer_medals
    WHERE medal = 'Gold' AND country IS NOT NULL
    GROUP BY year, country
)
SELECT
    year,
    country,
    gold_medals,
    RANK() OVER (PARTITION BY year ORDER BY gold_medals DESC) AS medal_rank,
    DENSE_RANK() OVER (PARTITION BY year ORDER BY gold_medals DESC) AS dense_medal_rank
FROM country_gold
ORDER BY year, medal_rank, country;

-- 3. Compare each country's Gold medals with its previous Olympics.
WITH country_gold AS (
    SELECT year, country, COUNT(*) AS gold_medals
    FROM summer_medals
    WHERE medal = 'Gold' AND country IS NOT NULL
    GROUP BY year, country
)
SELECT
    year,
    country,
    gold_medals,
    LAG(gold_medals) OVER (PARTITION BY country ORDER BY year) AS previous_gold_medals,
    gold_medals - LAG(gold_medals) OVER (PARTITION BY country ORDER BY year) AS change_from_previous
FROM country_gold
ORDER BY country, year;

-- 4. Running Gold-medal total by country.
WITH country_gold AS (
    SELECT year, country, COUNT(*) AS gold_medals
    FROM summer_medals
    WHERE medal = 'Gold' AND country IS NOT NULL
    GROUP BY year, country
)
SELECT
    year,
    country,
    gold_medals,
    SUM(gold_medals) OVER (
        PARTITION BY country
        ORDER BY year
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_gold_total
FROM country_gold
ORDER BY country, year;

-- 5. Three-Olympics moving average.
WITH country_gold AS (
    SELECT year, country, COUNT(*) AS gold_medals
    FROM summer_medals
    WHERE medal = 'Gold' AND country IS NOT NULL
    GROUP BY year, country
)
SELECT
    year,
    country,
    gold_medals,
    ROUND(
        AVG(gold_medals) OVER (
            PARTITION BY country
            ORDER BY year
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS three_games_moving_avg
FROM country_gold
ORDER BY country, year;

-- 6. Divide athletes into four medal-count buckets.
WITH athlete_medals AS (
    SELECT athlete, COUNT(*) AS medal_count
    FROM summer_medals
    GROUP BY athlete
)
SELECT
    athlete,
    medal_count,
    NTILE(4) OVER (ORDER BY medal_count DESC, athlete) AS medal_quartile
FROM athlete_medals
ORDER BY medal_quartile, medal_count DESC, athlete;
