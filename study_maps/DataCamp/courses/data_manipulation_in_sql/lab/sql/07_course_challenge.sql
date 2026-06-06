SET search_path TO data_manipulation_lab;

-- Course challenge:
-- Build a Manchester United season report using CASE, CTEs, UNION ALL,
-- and a window ranking over goal difference.

WITH home AS (
    SELECT
        m.id,
        m.date,
        m.season,
        m.hometeam_id AS team_id,
        t.team_long_name AS team_name,
        m.home_goal AS goals_for,
        m.away_goal AS goals_against,
        CASE
            WHEN m.home_goal > m.away_goal THEN 'MU Win'
            WHEN m.home_goal < m.away_goal THEN 'MU Loss'
            ELSE 'Tie'
        END AS outcome
    FROM match AS m
    LEFT JOIN team AS t
      ON m.hometeam_id = t.team_api_id
    WHERE t.team_long_name = 'Manchester United'
),
away AS (
    SELECT
        m.id,
        m.date,
        m.season,
        m.awayteam_id AS team_id,
        t.team_long_name AS team_name,
        m.away_goal AS goals_for,
        m.home_goal AS goals_against,
        CASE
            WHEN m.away_goal > m.home_goal THEN 'MU Win'
            WHEN m.away_goal < m.home_goal THEN 'MU Loss'
            ELSE 'Tie'
        END AS outcome
    FROM match AS m
    LEFT JOIN team AS t
      ON m.awayteam_id = t.team_api_id
    WHERE t.team_long_name = 'Manchester United'
),
mu_matches AS (
    SELECT * FROM home
    UNION ALL
    SELECT * FROM away
)
SELECT
    id,
    date,
    season,
    team_name,
    goals_for,
    goals_against,
    outcome,
    ABS(goals_for - goals_against) AS goal_difference,
    RANK() OVER (
        PARTITION BY season
        ORDER BY ABS(goals_for - goals_against) DESC
    ) AS margin_rank,
    SUM(
        CASE
            WHEN outcome = 'MU Win' THEN 3
            WHEN outcome = 'Tie' THEN 1
            ELSE 0
        END
    ) OVER (
        PARTITION BY season
        ORDER BY date, id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_points
FROM mu_matches
WHERE season = '2014/2015'
ORDER BY date, id;
