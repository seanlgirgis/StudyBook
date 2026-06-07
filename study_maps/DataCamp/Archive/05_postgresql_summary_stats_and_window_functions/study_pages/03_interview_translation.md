# Course 05 Interview Translation

## Explain window functions
Window functions let me calculate rankings, previous/next comparisons, running totals, moving averages, and percent-of-total metrics while keeping the original detail rows visible. GROUP BY collapses rows, but window functions add analytical context without losing granularity.

## Explain GROUP BY vs PARTITION BY
GROUP BY creates summary rows. PARTITION BY creates calculation groups for a window function, but the original rows stay visible.

## Explain ORDER BY inside OVER
ORDER BY inside OVER controls calculation sequence. Final ORDER BY controls display order.

## Explain ranking choices
If the business wants one exact row, I use ROW_NUMBER.  
If tied values should share rank and gaps are acceptable, I use RANK.  
If tied values should share rank but no gaps should appear, I use DENSE_RANK.

## Explain aggregate first, rank second, filter third
I would aggregate sales by department and salesperson first, rank the salespeople inside each department, then filter for rank = 3.

Tie-handling:

- `ROW_NUMBER` gives one exact third row.
- `RANK` includes everyone tied at third place.
- `DENSE_RANK` gives the third distinct performance tier.

## Explain LAG and LEAD
LAG is the rearview mirror. LEAD is the windshield.

## Explain LAST_VALUE trap
LAST_VALUE can return the current row if the frame ends at the current row. If I want the true last value in the partition, I use UNBOUNDED FOLLOWING.

## Explain ROWS vs RANGE
ROWS counts physical rows. RANGE works by ORDER BY value and includes peers.

## Explain NTILE vs P95
NTILE creates bucket labels. P95 creates a cutoff value.

## Explain WITHIN GROUP vs OVER
percentile_cont uses WITHIN GROUP here because it is an ordered aggregate. It sorts values inside the aggregate calculation and returns one cutoff per group. Window functions use OVER when they return values row by row.

## Explain CUME_DIST vs PERCENT_RANK
CUME_DIST tells what fraction of rows are at or below the current value. PERCENT_RANK tells where the current value starts on the ranking ladder. They can differ around ties because CUME_DIST counts through the tie group while PERCENT_RANK uses where the tie group starts.

## Explain owner-priority pipeline
I built a SQL analytics pipeline using window functions and CTEs. I started with raw sales rows, used CUME_DIST to place each sale relative to other sales inside its region, and converted those positions into business bands such as Top 5%, High, Middle, and Low.

Then I filtered the most important bands into a review queue, grouped that queue by salesperson, and applied a weighted priority score where Top 5% signals counted more than High signals. After that, I ranked the salespeople inside each region and added a final recommended action label.

The business value is that raw detail rows became a management-friendly priority report. The same pattern could apply to sales performance, fraud signals, customer risk, observability alerts, incident triage, or capacity prioritization.

## Final short version
Raw rows -> signals -> scores -> ranked recommendations.
