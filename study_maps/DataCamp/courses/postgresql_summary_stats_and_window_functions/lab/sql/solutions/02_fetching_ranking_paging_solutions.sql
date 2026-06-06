\set ON_ERROR_STOP on
SET search_path TO dc_window_lab, public;

-- 1. Future women’s discus champions.
WITH discus_medalists AS (
    SELECT DISTINCT year, athlete
    FROM summer_medals
    WHERE medal = 'Gold'
      AND event = 'Discus Throw'
      AND gender = 'Women'
      AND year >= 2000
)
SELECT
    year,
    athlete,
    LEAD(athlete, 3) OVER (
        ORDER BY year ASC
    ) AS future_champion
FROM discus_medalists
ORDER BY year ASC;

-- 2. First male Gold medalist alphabetically.
WITH all_male_medalists AS (
    SELECT DISTINCT athlete
    FROM summer_medals
    WHERE medal = 'Gold'
      AND gender = 'Men'
)
SELECT
    athlete,
    FIRST_VALUE(athlete) OVER (
        ORDER BY athlete ASC
    ) AS first_athlete
FROM all_male_medalists
ORDER BY athlete;

-- 3. True last Olympic host city.
WITH hosts AS (
    SELECT DISTINCT year, city
    FROM summer_medals
)
SELECT
    year,
    city,
    LAST_VALUE(city) OVER (
        ORDER BY year ASC
        RANGE BETWEEN
            UNBOUNDED PRECEDING AND
            UNBOUNDED FOLLOWING
    ) AS last_city
FROM hosts
ORDER BY year ASC;

-- 4. Rank athletes by medals.
WITH athlete_medals AS (
    SELECT athlete, COUNT(*) AS medals
    FROM summer_medals
    GROUP BY athlete
)
SELECT
    athlete,
    medals,
    RANK() OVER (
        ORDER BY medals DESC
    ) AS rank_n
FROM athlete_medals
ORDER BY medals DESC, athlete;

-- 5. Dense ranking inside Japan and Korea.
WITH athlete_medals AS (
    SELECT
        country,
        athlete,
        COUNT(*) AS medals
    FROM summer_medals
    WHERE country IN ('JPN', 'KOR')
      AND year >= 2000
    GROUP BY country, athlete
    HAVING COUNT(*) > 1
)
SELECT
    country,
    athlete,
    medals,
    DENSE_RANK() OVER (
        PARTITION BY country
        ORDER BY medals DESC
    ) AS rank_n
FROM athlete_medals
ORDER BY country ASC, rank_n ASC, athlete;

-- 6. Events split into 111 pages.
WITH events AS (
    SELECT DISTINCT event
    FROM summer_medals
)
SELECT
    event,
    NTILE(111) OVER (
        ORDER BY event ASC
    ) AS page
FROM events
ORDER BY event ASC;

-- 7. Athletes split into medal thirds.
WITH athlete_medals AS (
    SELECT athlete, COUNT(*) AS medals
    FROM summer_medals
    GROUP BY athlete
    HAVING COUNT(*) > 1
)
SELECT
    athlete,
    medals,
    NTILE(3) OVER (
        ORDER BY medals DESC
    ) AS third
FROM athlete_medals
ORDER BY medals DESC, athlete ASC;

-- 8. Average medals within each third.
WITH athlete_medals AS (
    SELECT athlete, COUNT(*) AS medals
    FROM summer_medals
    GROUP BY athlete
    HAVING COUNT(*) > 1
),
thirds AS (
    SELECT
        athlete,
        medals,
        NTILE(3) OVER (
            ORDER BY medals DESC
        ) AS third
    FROM athlete_medals
)
SELECT
    third,
    AVG(medals) AS avg_medals
FROM thirds
GROUP BY third
ORDER BY third ASC;
