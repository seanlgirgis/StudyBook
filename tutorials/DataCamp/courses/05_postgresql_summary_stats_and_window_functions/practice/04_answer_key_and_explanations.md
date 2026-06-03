# Answer Key and Explanations

## 1) Inspect the table
This query previews raw rows so you can confirm data loaded correctly.

## 2) GROUP BY revenue by region
This collapses many rows into one row per region and returns total revenue and row count.

## 3) COUNT(*) OVER (PARTITION BY region)
This keeps every original row, but adds how many rows are in that row's region.

## 4) ROW_NUMBER() OVER (ORDER BY sale_date)
This gives a running row position after sorting by date (and `event_id` as tie-breaker).

## 5) ROW_NUMBER() OVER (PARTITION BY region ORDER BY revenue DESC)
This restarts numbering per region and ranks rows from highest revenue downward.

## 6) RANK() and DENSE_RANK() by revenue inside region
Both rank by revenue within each region.
- `RANK()` leaves gaps after ties.
- `DENSE_RANK()` does not leave gaps.

## 7) LAG(revenue) to compare with previous sale
`LAG` pulls the previous row's revenue (within region and date order), then computes difference from current row.

## 8) Running total revenue by date
This computes cumulative revenue from the first ordered row through the current row.

## 9) Moving average revenue by date
This computes a 3-row moving average: current row plus previous two rows.

## 10) Percent of regional revenue total
This divides each row's revenue by its region's total revenue and shows contribution percentage.