# Course 4: Data Manipulation in SQL - SQL Examples Library

Status: reusable pattern library from Course 4 transcript material

## Basic CASE categorization
What question it answers: How do I label outcomes into categories?
SQL pattern:
```sql
CASE
  WHEN home_goal > away_goal THEN 'home win'
  WHEN away_goal > home_goal THEN 'away win'
  ELSE 'tie'
END
```
Why it matters: Converts raw values into analysis-friendly categories.
Common trap: Missing `ELSE`, then getting unexpected NULL outcomes.

## CASE comparing two columns
What question it answers: Which side wins based on two score columns?
SQL pattern:
```sql
CASE
  WHEN hometeam_id = 9857 AND home_goal > away_goal THEN 'Bologna win'
  WHEN awayteam_id = 9857 AND away_goal > home_goal THEN 'Bologna win'
  ELSE 'not Bologna win'
END
```
Why it matters: Supports side-dependent logic.
Common trap: Forgetting to reverse conditions for home vs away rows.

## CASE inside WHERE with IS NOT NULL
What question it answers: Keep rows only when CASE returns target category.
SQL pattern:
```sql
SELECT date, season, home_goal, away_goal
FROM matches_italy
WHERE
  CASE
    WHEN hometeam_id = 9857 AND home_goal > away_goal THEN 'Bologna win'
    WHEN awayteam_id = 9857 AND away_goal > home_goal THEN 'Bologna win'
  END IS NOT NULL;
```
Why it matters: Enables category-based filtering without extra temp tables.
Common trap: Expecting SELECT alias to be available in same-level WHERE.

## COUNT(CASE WHEN ...)
What question it answers: How many times did an event happen?
SQL pattern:
```sql
COUNT(
  CASE
    WHEN hometeam_id = 8455 AND home_goal > away_goal THEN id
  END
) AS home_wins
```
Why it matters: Standard conditional counting.
Common trap: Counting text literals inconsistently across engines.

## SUM(CASE WHEN ...)
What question it answers: What is the conditional total value?
SQL pattern:
```sql
SUM(
  CASE
    WHEN hometeam_id = 8455 THEN home_goal
  END
) AS total_home_goals
```
Why it matters: Conditional totals in one pass.
Common trap: Unexpected NULL handling when ELSE omitted.

## AVG(CASE WHEN ... THEN 1 ELSE 0 END) for percentages
What question it answers: What percentage of games meet condition?
SQL pattern:
```sql
AVG(
  CASE
    WHEN hometeam_id = 8455 AND home_goal > away_goal THEN 1
    WHEN awayteam_id = 8455 AND away_goal > home_goal THEN 1
    WHEN hometeam_id = 8455 OR awayteam_id = 8455 THEN 0
  END
) AS win_pct
```
Why it matters: Efficient percentage logic.
Common trap: Not excluding non-relevant rows as NULL.

## Scalar subquery in WHERE
What question it answers: Which rows are above/below a benchmark?
SQL pattern:
```sql
SELECT id, home_goal
FROM match
WHERE home_goal > (
  SELECT AVG(home_goal)
  FROM match
);
```
Why it matters: Dynamic benchmark filtering.
Common trap: Subquery returns multiple rows instead of one scalar.

## IN / NOT IN list subquery
What question it answers: Which rows belong to a derived ID set?
SQL pattern:
```sql
SELECT team_long_name
FROM team
WHERE team_api_id IN (
  SELECT hometeam_id
  FROM match
  WHERE country_id = 15722
);
```
Why it matters: Set-based filtering from related tables.
Common trap: `NOT IN` with NULLs can remove too many rows.

## FROM subquery
What question it answers: How do I reshape data before final query?
SQL pattern:
```sql
SELECT s.team, s.home_avg
FROM (
  SELECT t.team_long_name AS team, AVG(m.home_goal) AS home_avg
  FROM match AS m
  LEFT JOIN team AS t ON m.hometeam_id = t.team_api_id
  WHERE m.season = '2011/2012'
  GROUP BY t.team_long_name
) AS s
ORDER BY s.home_avg DESC
LIMIT 3;
```
Why it matters: Multi-step transformation.
Common trap: Forgetting alias for subquery table.

## SELECT subquery
What question it answers: How do I attach one benchmark value to each row?
SQL pattern:
```sql
SELECT
  date,
  (home_goal + away_goal) AS goals,
  (
    SELECT AVG(home_goal + away_goal)
    FROM match
  ) AS overall_avg
FROM match;
```
Why it matters: Benchmark comparison without regrouping.
Common trap: Wrong filter scope in subquery benchmark.

## Multiple subqueries in one query
What question it answers: How do I combine benchmark + reshape + filter?
SQL pattern:
```sql
SELECT ...,
  (SELECT ...) AS metric
FROM (
  SELECT ...
) AS base
WHERE ... > (SELECT ...);
```
Why it matters: Supports complex analytical questions.
Common trap: Readability collapse without formatting/comments.

## Correlated subquery with one correlation condition
What question it answers: How do I compare each row/group to related rows?
SQL pattern:
```sql
SELECT c.name,
  (
    SELECT AVG(m.home_goal + m.away_goal)
    FROM match AS m
    WHERE m.country_id = c.id
  ) AS avg_goals
FROM country AS c;
```
Why it matters: Per-entity derived calculations.
Common trap: Missing correlation gives incorrect global value.

## Correlated subquery with multiple correlation conditions
What question it answers: How do I correlate by entity and period?
SQL pattern:
```sql
SELECT c.name, s.season,
  (
    SELECT AVG(m.home_goal + m.away_goal)
    FROM match AS m
    WHERE m.country_id = c.id
      AND m.season = s.season
  ) AS avg_goals
FROM country AS c
CROSS JOIN (SELECT DISTINCT season FROM match) AS s;
```
Why it matters: Granular benchmarking.
Common trap: Performance degradation on large datasets.

## Nested subquery
What question it answers: How do I calculate aggregate-of-aggregate logic?
SQL pattern:
```sql
SELECT
  month,
  monthly_goals,
  monthly_goals - (
    SELECT AVG(monthly_goals)
    FROM (
      SELECT EXTRACT(MONTH FROM date) AS month,
             SUM(home_goal + away_goal) AS monthly_goals
      FROM match
      GROUP BY EXTRACT(MONTH FROM date)
    ) AS inner_monthly
  ) AS diff_from_monthly_avg
FROM (
  SELECT EXTRACT(MONTH FROM date) AS month,
         SUM(home_goal + away_goal) AS monthly_goals
  FROM match
  GROUP BY EXTRACT(MONTH FROM date)
) AS base;
```
Why it matters: Enables layered transformation.
Common trap: Losing track of which alias belongs to which level.

## CTE replacing a FROM subquery
What question it answers: How do I improve readability of a FROM subquery?
SQL pattern:
```sql
WITH s AS (
  SELECT country_id, id
  FROM match
  WHERE home_goal + away_goal >= 10
)
SELECT c.name, COUNT(s.id) AS high_scoring_matches
FROM country AS c
JOIN s ON c.id = s.country_id
GROUP BY c.name;
```
Why it matters: Named step is easier to debug/reuse.
Common trap: Forgetting that CTE column names must align with later usage.

## Multiple CTEs
What question it answers: How do I stage several transformations clearly?
SQL pattern:
```sql
WITH a AS (...),
b AS (...),
c AS (...)
SELECT ...
FROM c
JOIN b ON ...
JOIN a ON ...;
```
Why it matters: Sequential logic, cleaner structure.
Common trap: Missing comma between CTEs or extra comma at end.

## Home/away team lookup with subqueries
What question it answers: How do I fetch team names for both sides?
SQL pattern:
```sql
SELECT
  m.id,
  (SELECT t.team_long_name FROM team AS t WHERE t.team_api_id = m.hometeam_id)
    AS home_team,
  (SELECT t.team_long_name FROM team AS t WHERE t.team_api_id = m.awayteam_id)
    AS away_team
FROM match AS m;
```
Why it matters: Resolves dual foreign-key lookup pattern.
Common trap: Subquery not guaranteed scalar if key uniqueness is broken.

## Home/away team lookup with correlated subqueries
What question it answers: How do I correlate each match row to team names?
SQL pattern:
```sql
SELECT m.id,
  (SELECT t.team_long_name FROM team AS t WHERE t.team_api_id = m.hometeam_id)
    AS home_team,
  (SELECT t.team_long_name FROM team AS t WHERE t.team_api_id = m.awayteam_id)
    AS away_team
FROM match AS m;
```
Why it matters: Same-row dual lookup without repeated joins.
Common trap: Performance at scale compared to well-structured joins/CTEs.

## Home/away team lookup with CTEs
What question it answers: How do I make home/away lookup more readable?
SQL pattern:
```sql
WITH home_map AS (
  SELECT m.id, t.team_long_name AS home_team
  FROM match AS m
  JOIN team AS t ON t.team_api_id = m.hometeam_id
),
away_map AS (
  SELECT m.id, t.team_long_name AS away_team
  FROM match AS m
  JOIN team AS t ON t.team_api_id = m.awayteam_id
)
SELECT m.id, h.home_team, a.away_team
FROM match AS m
JOIN home_map AS h ON m.id = h.id
JOIN away_map AS a ON m.id = a.id;
```
Why it matters: Clear, reusable team lookup stages.
Common trap: Joining on wrong key and duplicating rows.

## AVG(...) OVER()
What question it answers: How do I compare row values to overall average?
SQL pattern:
```sql
SELECT
  date,
  home_goal + away_goal AS goals,
  AVG(home_goal + away_goal) OVER() AS overall_avg
FROM match;
```
Why it matters: Keeps detail rows while adding aggregate context.
Common trap: Expecting OVER result to respect filters not applied yet.

## RANK() OVER(ORDER BY ...)
What question it answers: How do I rank rows by metric?
SQL pattern:
```sql
SELECT
  id,
  home_goal + away_goal AS goals,
  RANK() OVER(ORDER BY home_goal + away_goal DESC) AS goal_rank
FROM match;
```
Why it matters: Ordered ranking with tie behavior.
Common trap: Confusing `RANK` gap behavior with dense ranking.

## OVER(PARTITION BY season)
What question it answers: How does row compare to its season average?
SQL pattern:
```sql
SELECT
  season,
  date,
  home_goal + away_goal AS goals,
  AVG(home_goal + away_goal) OVER(PARTITION BY season) AS season_avg
FROM match;
```
Why it matters: Per-season contextual baseline.
Common trap: Forgetting partition key changes meaning of comparison.

## OVER(PARTITION BY season, EXTRACT(MONTH FROM date))
What question it answers: How does row compare to season-month peer group?
SQL pattern:
```sql
SELECT
  season,
  date,
  home_goal + away_goal AS goals,
  AVG(home_goal + away_goal) OVER(
    PARTITION BY season, EXTRACT(MONTH FROM date)
  ) AS season_month_avg
FROM match;
```
Why it matters: Finer-grained partition comparisons.
Common trap: Misaligned date granularity.

## Running total with ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
What question it answers: What cumulative total do we have up to this row?
SQL pattern:
```sql
SELECT
  date,
  home_goal,
  SUM(home_goal) OVER(
    ORDER BY date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_home_goals
FROM match;
```
Why it matters: Core cumulative metric pattern.
Common trap: Missing ORDER BY makes running logic undefined.

## Reverse running total with ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
What question it answers: What total remains from this row forward?
SQL pattern:
```sql
SELECT
  date,
  home_goal,
  SUM(home_goal) OVER(
    ORDER BY date
    ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
  ) AS remaining_home_goals
FROM match;
```
Why it matters: Useful for forward-looking totals.
Common trap: Assuming reverse frame equals same interpretation as cumulative.

## Final Manchester United case-study pattern
What question it answers: Who defeated Manchester United in 2013/2014?
SQL pattern:
```sql
WITH matches_with_teams AS (
  SELECT
    m.date,
    m.season,
    ht.team_long_name AS home_team,
    at.team_long_name AS away_team,
    m.home_goal,
    m.away_goal
  FROM match AS m
  JOIN team AS ht ON ht.team_api_id = m.hometeam_id
  JOIN team AS at ON at.team_api_id = m.awayteam_id
  WHERE m.season = '2013/2014'
),
outcomes AS (
  SELECT
    *,
    CASE
      WHEN home_team = 'Manchester United' AND home_goal < away_goal
        THEN away_team
      WHEN away_team = 'Manchester United' AND away_goal < home_goal
        THEN home_team
    END AS defeating_team,
    CASE
      WHEN home_team = 'Manchester United' THEN away_goal - home_goal
      WHEN away_team = 'Manchester United' THEN home_goal - away_goal
    END AS goal_margin
  FROM matches_with_teams
)
SELECT
  date,
  defeating_team,
  goal_margin,
  RANK() OVER(ORDER BY goal_margin DESC) AS loss_margin_rank
FROM outcomes
WHERE defeating_team IS NOT NULL;
```
Why it matters: Integrates CTE + CASE + ranking in one readable flow.
Common trap: Not reversing margin logic for home vs away perspective.
