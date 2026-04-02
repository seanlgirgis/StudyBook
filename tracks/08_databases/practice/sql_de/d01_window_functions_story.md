# Window Functions - Story Map

## 1. Story
You track orders by customer over time. You need each order row, plus the rank, last order, and running total. GROUP BY removes the row detail you still need.

## 2. Core Concepts (street version)
- Window functions look sideways across related rows.
- They keep every row, then add extra context.
- GROUP BY collapses rows; windows do not.

## 3. Why GROUP BY is not enough
You lose per-row detail like the exact order that caused a jump.

## 4. What a window function is
A calculation across a window of related rows while keeping the current row.

## 5. PARTITION BY intuition
Partition is the neighborhood: rows are grouped into small communities (like each customer).

## 6. ORDER BY inside the window
Order is the timeline inside the neighborhood, so the window can rank or run totals.

## 7. Ranking example
ROW_NUMBER shows each order’s position within a customer’s history.

## 8. Previous/next row example
LAG lets you compare this order to the prior order in the same customer partition.

## 9. Running total example
SUM OVER accumulates spending over time per customer.

## 10. What window functions are great at
- Ranking within groups
- Trend and change analysis
- Running totals without losing rows

## 11. What window functions are bad at
- Reducing data to one row per group
- Replacing aggregation tables

## 12. Final mental model
GROUP BY squashes rows. Window functions keep rows and add context.

## 13. Run Order
1. c098_window_functions_demo.py
