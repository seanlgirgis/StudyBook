SET search_path TO data_manipulation_lab;

-- 1. Detail rows plus overall average.
SELECT
    id,
    date,
    home_goal + away_goal AS total_goals,
    ROUND(AVG(home_goal + away_goal) OVER (), 2) AS overall_avg
FROM match
ORDER BY date;

-- 2. Partition by country and season.
SELECT
    id,
    country_id,
    season,
    date,
    home_goal + away_goal AS total_goals,
    ROUND(
        AVG(home_goal + away_goal)
        OVER (PARTITION BY country_id, season),
        2
    ) AS country_season_avg
FROM match
ORDER BY country_id, season, date;

-- 3. Running and moving averages.
SELECT
    id,
    country_id,
    season,
    date,
    home_goal + away_goal AS total_goals,
    SUM(home_goal + away_goal) OVER (
        PARTITION BY country_id, season
        ORDER BY date, id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_goals,
    ROUND(
        AVG(home_goal + away_goal) OVER (
            PARTITION BY country_id, season
            ORDER BY date, id
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moving_avg_3
FROM match
ORDER BY country_id, season, date, id;
