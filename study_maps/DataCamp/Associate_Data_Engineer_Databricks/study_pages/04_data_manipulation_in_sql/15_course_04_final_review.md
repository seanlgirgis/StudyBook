# Course 4: Data Manipulation in SQL - Final Review

Status: final review drafted from captured transcripts

## Course 4 one-screen summary
Course 4 focused on SQL data manipulation patterns across four major areas:
CASE logic, subqueries, CTEs, and window functions. The main throughline was
how to transform row-level data into decision-ready outputs while keeping query
logic readable and correct.

## Chapter 1: CASE statements
- CASE statements for categorization and comparison across columns.
- CASE in WHERE as a filtering expression with `IS NOT NULL`.
- Conditional aggregation patterns using `COUNT`, `SUM`, and `AVG`.
- Sean's key breakthrough: CASE in WHERE behaves like a calculated expression
  used for filtering, not only display labeling.

## Chapter 2: Simple subqueries
- Simple subqueries in `WHERE`, `FROM`, and `SELECT`.
- Scalar subqueries for benchmark comparison.
- List subqueries with `IN` for filtering sets.
- Subqueries in `FROM` for multi-step reshaping before final filtering.
- Readability practices: formatting, indentation, comments, and subquery filter
  placement.

## Chapter 3: Correlated subqueries, nested subqueries, and CTEs
- Correlated subqueries depend on outer-row values and are evaluated in loops.
- Nested subqueries for layered transformations.
- CTEs (`WITH`) as named subqueries to improve readability and structure.
- Choosing technique by problem shape, clarity, and performance needs.

## Chapter 4: Window functions
- `OVER()` for aggregate comparisons without collapsing detail rows.
- `RANK()` for ordered ranking logic.
- `PARTITION BY` for grouped windows inside one result set.
- Sliding windows with `ROWS BETWEEN` for running and framed calculations.
- Final case-study framing: combine CTE + CASE + ranking for match outcomes.

## Final mental model
- CASE: derive categories and conditional values.
- Subqueries: pull benchmarks/lists or stage data transformations.
- CTEs: name steps, reduce cognitive load, improve maintainability.
- Window functions: keep detail rows while adding aggregate/rank context.

## Fast-review list
- `CASE WHEN ... THEN ... ELSE ... END`
- `COUNT(CASE WHEN ...)`
- `SUM(CASE WHEN ...)`
- `AVG(CASE WHEN ... THEN 1 ELSE 0 END)`
- Scalar subquery in `WHERE`
- `IN (subquery)`
- `AVG(...) OVER()`
- `RANK() OVER(ORDER BY ... DESC)`

## Slow-down list
- CASE inside `WHERE` with alias timing and `IS NOT NULL` logic.
- Correlated subquery evaluation model and performance tradeoff.
- Nested subquery flow (inner result -> outer use).
- Sliding window frame boundaries (`PRECEDING`, `FOLLOWING`, `CURRENT ROW`).
- Correct filter placement in both main query and subqueries.

## Interview-important list
- CASE statements
- Conditional aggregation
- Simple subqueries in `SELECT`, `FROM`, `WHERE`
- Correlated subqueries and performance caveats
- CTEs for readable multi-step transformations
- Window functions with `OVER()`, `PARTITION BY`, and `RANK()`
- Sliding window frames with `ROWS BETWEEN`
- Home/away match logic with reversed win/loss checks
