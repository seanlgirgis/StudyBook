# Data Manipulation in SQL Field Guide

## Course status

- **Platform status:** COMPLETE
- **Documentation:** COMPLETE
- **Lab coverage:** DEVELOPING
- **Recall confidence:** DEVELOPING
- **Interview readiness:** NEEDS REPETITION

## Course purpose

This course develops intermediate SQL patterns for transforming, filtering, organizing, and analyzing relational data without losing sight of query readability.

The course progresses through four layers:

1. Use `CASE` to create conditional values and conditional aggregates.
2. Use subqueries in `WHERE`, `FROM`, and `SELECT`.
3. Use correlated subqueries, nested queries, and common table expressions.
4. Use window functions to preserve detail rows while adding group and running calculations.

## Chapter guides

1. [We'll Take the CASE](chapter_01_well_take_the_case_field_guide.html)
2. [Short and Simple Subqueries](chapter_02_short_and_simple_subqueries_field_guide.html)
3. [Correlated Queries, Nested Queries, and Common Table Expressions](chapter_03_correlated_queries_nested_queries_and_common_table_expressions_field_guide.html)
4. [Window Functions](chapter_04_window_functions_field_guide.html)

Other course resources:

- [HTML Field Guide](field_guide.html)
- [SQL Quick Lookup](sql_quick_lookup.html)
- [Lab Guide](../lab/lab_guide.html)

---

## Chapter 1 — CASE expressions

### Basic pattern

```sql
CASE
    WHEN condition_1 THEN result_1
    WHEN condition_2 THEN result_2
    ELSE fallback_result
END
```

`CASE` evaluates conditions from top to bottom and returns the first matching result.

### Conditional count

```sql
SUM(
    CASE
        WHEN condition THEN 1
        ELSE 0
    END
) AS matching_rows
```

### Conditional fraction

```sql
AVG(
    CASE
        WHEN condition THEN 1.0
        ELSE 0.0
    END
) AS matching_fraction
```

### Important distinction

- `CASE` creates values.
- `WHERE` removes rows.

### Chapter memory rule

```text
SUM(flag) = count
AVG(flag) = fraction
```

---

## Chapter 2 — Subqueries

A subquery is a query nested inside another query.

### Scalar subquery

Returns one value.

```sql
SELECT id, date
FROM match
WHERE home_goal + away_goal > (
    SELECT AVG(home_goal + away_goal)
    FROM match
);
```

### List subquery

Returns one column with multiple rows.

```sql
SELECT team_long_name
FROM team
WHERE team_api_id IN (
    SELECT hometeam_id
    FROM match
    WHERE home_goal >= 5
);
```

### Subquery in `FROM`

Creates a derived table.

```sql
SELECT country, avg_goals
FROM (
    SELECT
        country_id AS country,
        AVG(home_goal + away_goal) AS avg_goals
    FROM match
    GROUP BY country_id
) AS country_summary;
```

### Subquery in `SELECT`

Usually returns one scalar benchmark.

```sql
SELECT
    stage,
    AVG(home_goal + away_goal) AS stage_avg,
    (
        SELECT AVG(home_goal + away_goal)
        FROM match
    ) AS overall_avg
FROM match
GROUP BY stage;
```

### Shape rule

```text
one value            → =, >, <, >=, <=
one column/many rows → IN, NOT IN, ANY, ALL
table result         → FROM
one display value    → SELECT
```

### `NOT IN` caution

A `NULL` returned by a `NOT IN` subquery can cause unexpected results. Filter `NULL` values or prefer `NOT EXISTS`.

---

## Chapter 3 — Correlated queries, nesting, and CTEs

### Correlated subquery

A correlated subquery references the current outer row.

```sql
SELECT
    main.id,
    main.country_id,
    main.home_goal,
    main.away_goal
FROM match AS main
WHERE main.home_goal + main.away_goal > (
    SELECT 3 * AVG(sub.home_goal + sub.away_goal)
    FROM match AS sub
    WHERE sub.country_id = main.country_id
);
```

The inner query cannot run independently because it references `main.country_id`.

### Multiple correlation conditions

```sql
WHERE sub.country_id = main.country_id
  AND sub.season = main.season
```

This compares a row with its own country-season group.

### Common table expression

```sql
WITH match_list AS (
    SELECT country_id, id
    FROM match
    WHERE home_goal + away_goal >= 10
)
SELECT
    l.name,
    COUNT(ml.id)
FROM league AS l
LEFT JOIN match_list AS ml
  ON l.country_id = ml.country_id
GROUP BY l.name;
```

### CTE decision rule

Use a CTE when:

- the query has meaningful stages,
- the same prepared result is reused,
- nested SQL becomes hard to read,
- individual steps need testing.

A CTE is not automatically faster. Its primary benefit is structure and readability.

### Join-key reminder

When joining `league` and `match` in the soccer dataset, use their shared country key:

```sql
ON l.country_id = m.country_id
```

---

## Chapter 4 — Window functions

Window functions calculate across related rows while preserving row-level detail.

### Overall aggregate beside every row

```sql
AVG(home_goal + away_goal) OVER ()
```

### Partitioned average

```sql
AVG(home_goal + away_goal)
OVER (PARTITION BY country_id, season)
```

### Running total

```sql
SUM(goals_for) OVER (
    PARTITION BY team_id, season
    ORDER BY date, id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

### Moving average

```sql
AVG(total_goals) OVER (
    PARTITION BY country_id, season
    ORDER BY date, id
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
```

### Ranking

```sql
RANK() OVER (
    PARTITION BY season
    ORDER BY goal_difference DESC
)
```

### Important distinction

- `GROUP BY` reduces rows.
- `PARTITION BY` defines calculation groups but preserves rows.
- Window `ORDER BY` controls calculation sequence.
- Final query `ORDER BY` controls display order.

---

## Technique decision guide

| Need | Best starting technique |
|---|---|
| Create categories or flags | `CASE` |
| Filter using one calculated value | Scalar subquery |
| Filter using a generated list | `IN` or `EXISTS` |
| Build a temporary summarized table | Subquery in `FROM` |
| Compare every row with its own group | Correlated subquery or window function |
| Organize several processing stages | CTE |
| Preserve detail rows while adding group metrics | Window function |
| Look up descriptive columns from another table | Join |
| Exclude matching rows safely | `NOT EXISTS` |

---

## Common mistakes

### Counting with `COUNT(CASE...)`

Correct:

```sql
COUNT(CASE WHEN condition THEN id END)
```

Incorrect:

```sql
COUNT(CASE WHEN condition THEN 1 ELSE 0 END)
```

`COUNT()` counts zero because zero is not `NULL`.

### Turning a `LEFT JOIN` into an inner join

This removes unmatched rows:

```sql
LEFT JOIN match AS m
  ON l.country_id = m.country_id
WHERE m.season = '2014/2015'
```

To preserve every league, move the season condition into `ON`.

### Confusing scalar and list subqueries

- `=` expects one value.
- `IN` accepts multiple values.

### Unstable window ordering

Use a deterministic tie-breaker:

```sql
ORDER BY date, id
```

### Assuming CTE means faster

CTEs improve readability. Validate performance with the execution plan.

---

## Interview translation

### What is conditional aggregation?

Conditional aggregation places a `CASE` expression inside an aggregate so one grouped query can calculate metrics for selected rows.

### What is a correlated subquery?

A correlated subquery references values from the current outer row and is evaluated in that row's context.

### When would you use a CTE?

Use a CTE to name intermediate logic, separate a complex query into testable stages, and make the final query easier to understand.

### What is a window function?

A window function calculates across related rows while preserving one output row for every input row.

### How is `PARTITION BY` different from `GROUP BY`?

`GROUP BY` collapses rows into summaries. `PARTITION BY` defines calculation groups without collapsing the detail rows.

---

## Lab coverage

The course-local lab includes:

- schema and sample soccer data,
- CASE classification and conditional aggregation,
- scalar, list, `FROM`, and `SELECT` subqueries,
- correlated queries and CTEs,
- partitioned averages and sliding windows,
- a Manchester United course challenge using `CASE`, CTEs, `UNION ALL`, `RANK()`, and running points.

Open the [Lab Guide](../lab/lab_guide.html).

---

## Quick memory nuggets

```text
CASE creates values.
WHERE removes rows.
```

```text
Scalar subquery = one value.
List subquery = one column, many rows.
FROM subquery = temporary table.
```

```text
Correlated = references outer row.
CTE = named query step.
Window = group context without losing detail.
```

```text
GROUP BY collapses.
PARTITION BY preserves.
```
