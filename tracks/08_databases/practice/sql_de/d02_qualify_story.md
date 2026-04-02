# QUALIFY - Story Map

## 1. Story
You want the latest order per customer. The row_number shows it, but you only want row_number = 1. WHERE cannot see that window result yet.

## 2. Core Concepts (street version)
- WHERE filters before window logic.
- QUALIFY filters after window logic.
- QUALIFY is great for top-1-per-group.

## 3. Why WHERE is not enough
The window values do not exist when WHERE runs.

## 4. What QUALIFY is
A post-window filter: compute window columns, then keep the rows you want.

## 5. QUALIFY vs WHERE intuition
WHERE = pre-window. QUALIFY = post-window.

## 6. Top-1-per-group example
Compute row_number by customer and keep only row_number = 1.

## 7. Why QUALIFY feels cleaner than subqueries
Without QUALIFY you wrap the window in a subquery and filter outside it.

## 8. What QUALIFY is great at
- Latest row per group
- Top-N per group

## 9. What QUALIFY is bad at
- Engines that do not support it
- Complex filtering that still needs subqueries

## 10. Final mental model
QUALIFY is WHERE for window outputs.

## 11. Run Order
1. c099_qualify_demo.py

Note: QUALIFY exists in engines like Snowflake and BigQuery. If not supported, use a subquery/CTE.
