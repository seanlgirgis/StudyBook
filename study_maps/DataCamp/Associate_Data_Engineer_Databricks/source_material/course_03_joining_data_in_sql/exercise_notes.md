# Course 3: Joining Data in SQL - exercise_notes

Status: placeholder

TODO:
- Paste source material here.


# Chapter 2 Exercise: LEFT JOIN countries and languages

Status: completed

Exercise type:
Drag SQL clauses into correct order.

Correct query:

SELECT c.name AS country,
       local_name,
       l.name AS language,
       percent
FROM countries AS c
LEFT JOIN languages AS l
USING(code)
ORDER BY country DESC;

Key lesson:
LEFT JOIN keeps all rows from the left table, here countries,
and attaches matching rows from languages when code matches.

USING(code) is a shortcut for joining on a same-named column
that exists in both tables.

Sean note:
The order is SELECT, FROM, LEFT JOIN, USING, ORDER BY.

Study marking:
- LEFT JOIN: PRACTICE REQUIRED
- USING(code): NORMAL STUDY
- clause order: PRACTICE REQUIRED

# Chapter 2 Exercise Notes - Self joins

Status: awaiting self join exercise prompts, solutions, mistakes, and confusion points.

Key early note:
A self join joins a table to itself. SQL does not use a SELF JOIN keyword.
Aliases are required so the same table can be referenced as two logical copies.

# Chapter 3 Exercise Notes - UNION and UNION ALL

Status: awaiting UNION / UNION ALL exercise prompts, solutions, mistakes, and confusion points.

Key early notes:
- JOINs connect tables side-by-side using matching keys.
- Set operations stack SELECT results vertically.
- UNION removes exact duplicate rows.
- UNION ALL keeps duplicate rows.
- Set operations do not use ON or USING.
- Each SELECT must return the same number of columns.
- Matching columns must have compatible data types.
- Final column names come from the first SELECT statement.

# Chapter 3 Exercise Notes - INTERSECT

Status: awaiting INTERSECT exercise prompts, solutions, mistakes, and confusion points.

Key early notes:
- INTERSECT returns only records that appear in both SELECT results.
- INTERSECT does not use ON or USING.
- INTERSECT compares the full selected row, not only one key column.
- Each SELECT must return the same number of columns.
- Matching columns must have compatible data types.
- Result column names come from the first SELECT.
- INTERSECT returns common records once.
- INNER JOIN can return duplicate values and can add more columns.

# Chapter 3 Exercise Notes - EXCEPT

Status: awaiting EXCEPT exercise prompts, solutions, mistakes, and confusion points.

Key early notes:
- EXCEPT returns records from the first SELECT that are not found in the
  second SELECT.
- EXCEPT is left-side minus right-side.
- EXCEPT does not use ON or USING.
- EXCEPT compares the full selected row.
- Each SELECT must return the same number of columns.
- Matching columns must have compatible data types.
- Result column names come from the first SELECT.

# Chapter 4 Exercise Notes - Semi joins and anti joins

Status: awaiting semi join / anti join exercise prompts, solutions, mistakes, and confusion points.

Key early notes:
- Regular joins are additive because they add columns to the left table.
- Semi joins and anti joins filter rows instead of adding columns.
- Semi join keeps rows from the first table where a match exists in the
  subquery.
- Anti join keeps rows from the first table where a match does not exist in the
  subquery.
- Semi joins commonly use WHERE ... IN (...).
- Anti joins commonly use WHERE ... NOT IN (...).
- No JOIN keyword is required for the semi/anti join pattern shown here.

# Chapter 4 Exercise Notes - Subqueries inside WHERE and SELECT

Status: awaiting exercise prompts, solutions, mistakes, and confusion points.

Key early notes:
- WHERE is the most common place for subqueries.
- Subqueries inside WHERE are often used for filtering.
- IN can accept a subquery result, not only a manually typed list.
- The subquery result must have a compatible data type with the field being
  filtered.
- Subqueries inside SELECT are used to calculate a value shown as a result
  column.
- A subquery inside SELECT requires an alias.
- Subqueries can read from the same table or a different table.

# Chapter 4 Exercise Notes - Subqueries inside FROM

Status: awaiting FROM subquery exercise prompts, solutions, mistakes, and confusion points.

Key early notes:
- A subquery inside FROM acts like a temporary table.
- The subquery should be aliased.
- The outer query can select from the subquery alias.
- FROM subqueries are useful when you need to aggregate first, then use that
  aggregated result in a larger query.
- Multiple tables or table-like results can appear in FROM, separated by commas,
  but this can create duplicate combinations unless filtered carefully.
