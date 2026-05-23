# Course 4: Data Manipulation in SQL - Mistakes and Breakthroughs

Status: learning breakthroughs captured

## Core breakthroughs
- CASE in WHERE behaves like a calculated expression used for filtering.
- WHERE happens before SELECT aliases are available at the same query level.
- HAVING can sometimes work after aggregation, but is not the same tool as
  row-level WHERE filtering.
- Main query filters do not automatically filter subqueries.

## Subquery and CTE understanding
- Correlated subqueries depend on the outer row.
- Correlated subqueries can be slower because they are evaluated repeatedly.
- CTEs are named subqueries and improve readability for multi-step logic.

## Window function understanding
- Window functions keep detail rows while adding aggregate/rank calculations.
- PARTITION BY is standard SQL window-function logic, not Spark-only.
- Sliding windows are useful for running totals and rolling-style calculations.

## Match-logic pitfall
- Home/away team logic must reverse win/loss conditions depending on team side.
  If this reversal is wrong, outcome labels and margins become incorrect.
