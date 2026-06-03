
# Chapter 2: ORDER BY inside OVER and LAG

- ORDER BY inside OVER controls how ROW_NUMBER assigns row numbers.
- ORDER BY Year DESC assigns row number 1 to the most recent year.
- ORDER BY inside OVER can use multiple columns such as Year and Event.
- ORDER BY inside OVER controls calculation order, while final ORDER BY controls display order.
- ORDER BY inside OVER happens before the final ORDER BY display sort.
- LAG(column, 1) brings the previous row value into the current row.
- LAG is useful for reigning-champion style comparisons.
- CTE first builds the current champions row set.
- Outer query applies LAG to place current and previous champions on the same row.
- First row in the ordered set has NULL as previous value.
