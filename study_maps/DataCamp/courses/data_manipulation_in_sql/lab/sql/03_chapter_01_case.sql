SET search_path TO data_manipulation_lab;

-- 1. Categorize home teams.
SELECT
    CASE
        WHEN hometeam_id = 9823 THEN 'FC Bayern Munich'
        WHEN hometeam_id = 10189 THEN 'FC Schalke 04'
        ELSE 'Other'
    END AS home_team,
    COUNT(*) AS total_matches
FROM match
GROUP BY home_team
ORDER BY total_matches DESC;

-- 2. Label outcomes from the home-team perspective.
SELECT
    id,
    date,
    CASE
        WHEN home_goal > away_goal THEN 'Home win'
        WHEN home_goal < away_goal THEN 'Home loss'
        ELSE 'Tie'
    END AS outcome
FROM match
ORDER BY date;

-- 3. Conditional counts and fractions.
SELECT
    season,
    COUNT(*) AS total_matches,
    SUM(CASE WHEN home_goal > away_goal THEN 1 ELSE 0 END) AS home_wins,
    ROUND(AVG(CASE WHEN home_goal = away_goal THEN 1.0 ELSE 0.0 END), 3) AS tie_fraction
FROM match
GROUP BY season
ORDER BY season;
