# Course 4: Data Manipulation in SQL - CASE Inside WHERE Story

Status: learning story captured

## Why this story matters

This lesson started from a DataCamp exercise that filtered for matches where
Bologna won.

At first, the SQL looked strange because a full CASE expression appeared inside
the WHERE clause.

The important realization:

CASE can behave like a temporary calculated field.

WHERE can then test the result of that temporary calculation.

## Original CASE-in-WHERE pattern

SQL example:

    SELECT
      date,
      season,
      home_goal,
      away_goal
    FROM matches_italy
    WHERE
      CASE
        WHEN hometeam_id = 9857 AND home_goal > away_goal
          THEN 'Bologna win'
        WHEN awayteam_id = 9857 AND away_goal > home_goal
          THEN 'Bologna win'
      END IS NOT NULL;

## Plain-English explanation

For every row, SQL evaluates this CASE expression:

    CASE
      WHEN hometeam_id = 9857 AND home_goal > away_goal
        THEN 'Bologna win'
      WHEN awayteam_id = 9857 AND away_goal > home_goal
        THEN 'Bologna win'
    END

That CASE expression returns one of two things:

    'Bologna win'

or:

    NULL

Then the WHERE clause checks:

    IS NOT NULL

So the row is kept only when the CASE expression produced a real value.

## Mental model

Think of the CASE expression as a hidden temporary field.

    Row 1: Bologna home and won  -> 'Bologna win' -> keep
    Row 2: Bologna away and won  -> 'Bologna win' -> keep
    Row 3: Bologna lost          -> NULL          -> remove
    Row 4: Bologna tied          -> NULL          -> remove
    Row 5: Bologna not playing   -> NULL          -> remove

## Sean's correct breakthrough

Sean summarized the idea correctly:

    This all becomes a calculated field, and IS NOT NULL is the condition.
    So show only the rows that come out to be Bologna win.

That is the key concept.

## Why not just use the alias in WHERE?

Sean asked whether this could be written like this:

    SELECT
      date,
      season,
      home_goal,
      away_goal,
      CASE
        WHEN hometeam_id = 9857 AND home_goal > away_goal
          THEN 'Bologna win'
        WHEN awayteam_id = 9857 AND away_goal > home_goal
          THEN 'Bologna win'
      END AS bologna_result
    FROM matches_italy
    WHERE bologna_result IS NOT NULL;

Conceptually, the idea is right.

But in standard SQL processing, the WHERE clause usually happens before the
SELECT alias is available.

A useful simplified order is:

    FROM
    WHERE
    SELECT
    ORDER BY

So when WHERE runs, the alias bologna_result usually does not exist yet.

That is why the full CASE expression is repeated inside WHERE.

## Correct alias-friendly version using a subquery

If we want to create the alias first and then filter by it, we can use a
subquery.

    SELECT *
    FROM (
      SELECT
        date,
        season,
        home_goal,
        away_goal,
        CASE
          WHEN hometeam_id = 9857 AND home_goal > away_goal
            THEN 'Bologna win'
          WHEN awayteam_id = 9857 AND away_goal > home_goal
            THEN 'Bologna win'
        END AS bologna_result
      FROM matches_italy
    ) AS results
    WHERE bologna_result IS NOT NULL;

Plain English:

    Inner query creates bologna_result.
    Outer query filters on bologna_result.

## Could HAVING be used?

Sean asked whether HAVING could be used.

Answer:

Sometimes, depending on the SQL engine, but it is not the clean standard
pattern for this exercise.

HAVING is mainly for filtering after grouping or aggregation.

Example:

    SELECT
      season,
      COUNT(*) AS bologna_wins
    FROM matches_italy
    WHERE
      (hometeam_id = 9857 AND home_goal > away_goal)
      OR
      (awayteam_id = 9857 AND away_goal > home_goal)
    GROUP BY season
    HAVING COUNT(*) > 5;

Plain rule:

    WHERE filters rows before SELECT and before grouping.
    HAVING filters grouped results after GROUP BY.
    Subqueries let you filter on a SELECT alias cleanly.

## Most readable production SQL for this exact problem

For this Bologna-win filter, CASE is not actually required.

The most direct production-readable version is:

    SELECT
      date,
      season,
      home_goal,
      away_goal
    FROM matches_italy
    WHERE
      (hometeam_id = 9857 AND home_goal > away_goal)
      OR
      (awayteam_id = 9857 AND away_goal > home_goal);

This is often cleaner because the goal is filtering rows, not creating a
display category.

## Best mental rule

    WHERE is for filtering rows.
    CASE is for calculating labels or categories.
    Use CASE in WHERE only when the filter itself depends on complex category logic.
    Use a subquery when you want to filter by a calculated alias.
    Use HAVING when filtering grouped or aggregated results.

## Data engineering translation

This pattern appears outside soccer data.

Example:

    actual_usage > forecast_usage -> over forecast
    actual_usage < forecast_usage -> under forecast
    actual_usage = forecast_usage -> on target

A data engineer may use CASE to label rows into categories, then filter or group
those categories for reporting.

## Interview-safe explanation

A safe way to explain this:

    In SQL, CASE can be used to create a derived category. If that CASE
    expression is placed inside WHERE, it becomes part of the row-filtering
    logic instead of a visible output column. In this exercise, the CASE
    returned a value only for Bologna wins, and returned NULL otherwise.
    The WHERE condition IS NOT NULL kept only the winning rows. For production
    readability, I would usually write the same filter with direct AND/OR
    conditions, or use a subquery if I need to filter on a calculated alias.

## Keeper summary

    CASE in SELECT = visible calculated column.
    CASE in WHERE = temporary filter calculation.
    WHERE cannot usually see SELECT aliases at the same query level.
    Subquery creates the alias first, then outer WHERE can filter it.
    HAVING is for filtering grouped results.
    Plain AND/OR is often best when the task is just row filtering.
