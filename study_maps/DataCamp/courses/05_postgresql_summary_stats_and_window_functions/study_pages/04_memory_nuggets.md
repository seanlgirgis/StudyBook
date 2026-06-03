# Course 05 Memory Nuggets

## Foundations
- GROUP BY collapses. PARTITION BY keeps detail rows.
- Window ORDER BY calculates. Final ORDER BY displays.
- OVER is the switch that turns a function into a window function.
- PARTITION BY changes the denominator or comparison group.

## Ranking
- ROW_NUMBER never ties.
- RANK ties and leaves gaps.
- DENSE_RANK ties and does not leave gaps.
- ROW_NUMBER can use tie-breakers.
- RANK and DENSE_RANK often should not use unique tie-breakers.

## LAG / LEAD
- LAG is the rearview mirror.
- LEAD is the windshield.
- First LAG row is NULL because there is no previous row.
- Last LEAD row is NULL because there is no next row.
- NULLIF is the divide-by-zero airbag.

## FIRST_VALUE / LAST_VALUE
- FIRST_VALUE is usually safe by default.
- LAST_VALUE needs the full frame.
- UNBOUNDED FOLLOWING lets LAST_VALUE see the true last row.

## Frames
- Running total starts at the beginning.
- Moving average slides with the current row.
- Previous-only frame excludes the current row from its own benchmark.
- ROWS = physical rows.
- RANGE = value peers.

## Percentiles
- NTILE is a bucket label.
- P95 is a cutoff value.
- percentile_cont calculates a threshold, not a row label.
- CUME_DIST = coverage so far.
- PERCENT_RANK = rank-start position.
- CUME_DIST looks after the tie group.
- PERCENT_RANK looks at where the tie group starts.

## Review queues and scoring
- CASE creates business bands.
- WHERE selects the review queue.
- GROUP BY summarizes ownership.
- Conditional SUM counts each signal type.
- Weights create urgency.
- RANK creates management order.
- CASE at the end turns analytics into a business recommendation.
- Raw rows -> signals -> scores -> ranked recommendations.

## Interview
- Explain what the SQL does.
- Explain why it matters.
- Explain what decision it supports.
- Do not just name functions; translate them into business meaning.
