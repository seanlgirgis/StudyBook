SET search_path TO data_manipulation_lab;

-- 1. Correlated subquery: matches above 3x their country average.
SELECT
    main.id,
    main.country_id,
    main.date,
    main.home_goal,
    main.away_goal
FROM match AS main
WHERE main.home_goal + main.away_goal > (
    SELECT 3 * AVG(sub.home_goal + sub.away_goal)
    FROM match AS sub
    WHERE sub.country_id = main.country_id
);

-- 2. Correlated subquery: country-season maximum.
SELECT
    main.id,
    main.country_id,
    main.season,
    main.home_goal + main.away_goal AS total_goals
FROM match AS main
WHERE main.home_goal + main.away_goal = (
    SELECT MAX(sub.home_goal + sub.away_goal)
    FROM match AS sub
    WHERE sub.country_id = main.country_id
      AND sub.season = main.season
)
ORDER BY main.country_id, main.season;

-- 3. CTE: count matches with 10+ goals by league.
WITH match_list AS (
    SELECT country_id, id
    FROM match
    WHERE home_goal + away_goal >= 10
)
SELECT
    l.name AS league,
    COUNT(ml.id) AS matches
FROM league AS l
LEFT JOIN match_list AS ml
ON l.country_id = ml.country_id
GROUP BY l.name
ORDER BY l.name;

-- 4. Compare join and correlated lookup.
SELECT
    m.id,
    t.team_long_name AS home_team
FROM match AS m
LEFT JOIN team AS t
ON m.hometeam_id = t.team_api_id
ORDER BY m.id;

SELECT
    m.id,
    (
        SELECT t.team_long_name
        FROM team AS t
        WHERE t.team_api_id = m.hometeam_id
    ) AS home_team
FROM match AS m
ORDER BY m.id;
