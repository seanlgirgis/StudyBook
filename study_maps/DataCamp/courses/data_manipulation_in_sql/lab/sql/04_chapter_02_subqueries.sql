SET search_path TO data_manipulation_lab;

-- 1. Scalar subquery: matches above 3x the average total goals.
SELECT id, date, home_goal, away_goal
FROM match
WHERE home_goal + away_goal > (
    SELECT 3 * AVG(home_goal + away_goal)
    FROM match
);

-- 2. List subquery: teams that scored at least 5 home goals.
SELECT team_long_name, team_short_name
FROM team
WHERE team_api_id IN (
    SELECT hometeam_id
    FROM match
    WHERE home_goal >= 5
);

-- 3. FROM subquery: high-scoring matches by country.
SELECT
    c.name AS country,
    COUNT(s.id) AS matches_10_plus_goals
FROM country AS c
LEFT JOIN (
    SELECT id, country_id
    FROM match
    WHERE home_goal + away_goal >= 10
) AS s
ON c.id = s.country_id
GROUP BY c.name
ORDER BY c.name;

-- 4. SELECT subquery: league average versus overall average.
SELECT
    l.name AS league,
    ROUND(AVG(m.home_goal + m.away_goal), 2) AS league_avg,
    (
        SELECT ROUND(AVG(home_goal + away_goal), 2)
        FROM match
    ) AS overall_avg
FROM league AS l
JOIN match AS m
ON l.country_id = m.country_id
GROUP BY l.name
ORDER BY l.name;
