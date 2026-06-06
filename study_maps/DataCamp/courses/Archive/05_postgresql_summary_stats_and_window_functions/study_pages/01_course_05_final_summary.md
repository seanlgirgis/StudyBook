# Course 05 Final Summary — PostgreSQL Summary Stats and Window Functions

## What this course became
This course started as PostgreSQL summary statistics and window functions, but it became a practical analytics-pattern course.

- preserve detail rows
- add context columns
- rank within groups
- compare previous/next rows
- calculate running and moving windows
- create percentile cutoffs
- create row-level percentile signals
- turn signals into review queues
- turn review queues into owner-level priority reports

## Core mental model
GROUP BY collapses rows.  
Window functions keep rows visible and add context.  
PARTITION BY defines the calculation group.  
ORDER BY inside OVER defines the calculation sequence.  
Final ORDER BY defines the display sequence.

## Major concepts learned

### GROUP BY vs PARTITION BY
`GROUP BY` changes the output shape and creates summary rows. `PARTITION BY` creates a calculation group for a window function while keeping the original detail rows visible.

### ORDER BY inside OVER vs final ORDER BY
`ORDER BY` inside `OVER` controls calculation order. Final `ORDER BY` controls how rows are displayed on screen.

### ROW_NUMBER vs RANK vs DENSE_RANK
- `ROW_NUMBER` = one exact row position, no ties.
- `RANK` = ties share rank, gaps can happen.
- `DENSE_RANK` = ties share rank, no gaps.

### LAG and LEAD
`LAG` and `LEAD` make row-to-row comparison possible. They let one row pull in the previous or next row value without a self-join.

### FIRST_VALUE and LAST_VALUE
These functions create boundary anchors. `FIRST_VALUE` usually behaves as expected by default. `LAST_VALUE` has a full-frame trap and often needs `UNBOUNDED FOLLOWING`.

### Window frames
Frames decide which rows are visible to the current calculation.

- running total
- moving average
- moving total
- previous-only benchmark
- centered window
- forward-looking window

### ROWS vs RANGE
`ROWS` works with physical rows. `RANGE` works with value peers from the `ORDER BY` expression.

### NTILE vs P95
`NTILE` creates bucket labels. P95 creates a cutoff value.

### CUME_DIST vs PERCENT_RANK
`CUME_DIST` is coverage-based. `PERCENT_RANK` is rank-start based.

### Percentile banding and review queues
This was the shift from raw math to business logic: row-level signal -> business band -> review queue.

### Owner-priority scoring
This was the final pipeline: band counts, weights, `priority_score`, `priority_rank`, and `recommended_action`.

## Final Course 05 pipeline
Raw rows -> signals -> scores -> ranked recommendations.

Final owner-priority pipeline:

raw revenue rows  
-> CUME_DIST  
-> revenue_band  
-> review queue  
-> owner summary  
-> weighted priority_score  
-> priority_rank  
-> recommended_action

## Why this matters for interviews
The value is not just syntax. You can explain:

- what calculation was done
- why it was done
- what business decision it supports

Examples:

- sales performance
- fraud signals
- customer risk
- observability alerts
- incident triage
- capacity prioritization

## What to review before moving on
- field guide
- interview translation
- memory nuggets
- mistakes and corrections
- runnable workbook only if hands-on refresh is needed
