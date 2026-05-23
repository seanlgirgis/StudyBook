# Course 4: Data Manipulation in SQL - Interview Translation

Status: interview translation drafted

## CASE logic for business categorization
Safe language:
I refreshed CASE patterns to classify outcomes and to build conditional logic
for filters and derived columns.

## Conditional aggregation
Safe language:
I used conditional aggregation patterns like COUNT/SUM/AVG with CASE to produce
event counts, totals, and percentage-style metrics.

## Subqueries for benchmark comparison
Safe language:
I used scalar and list subqueries to compare row-level results against overall
or grouped benchmarks and to build filter lists.

## CTEs for readable multi-step transformations
Safe language:
I use CTEs for readable multi-step transformations, especially when logic has
multiple preparation steps before final selection or ranking.

## Window functions for ranking, running totals, and partitioned comparisons
Safe language:
I applied `OVER()` patterns with `PARTITION BY`, ranking functions, and
`ROWS BETWEEN` frames for running totals and contextual comparisons while
preserving detail rows.

## How this maps to data engineering work
- Turning raw event rows into consistent analytical categories.
- Building reusable SQL transformations for reporting and QA checks.
- Comparing local metrics to broader baselines by time/entity partitions.
- Producing readable query pipelines that other engineers can maintain.

## How this maps to capacity forecasting / telemetry style work
- CASE can label telemetry states (over target, under target, on target).
- Conditional aggregation can measure incident rates and threshold breaches.
- Window functions can track running usage, rolling behavior, and rank hotspots.
- CTE pipelines help break forecasting logic into auditable transformation steps.

## Scope-safe summary
This course work reflects refreshed SQL patterns and reusable analytics logic.
It should be presented as practice-backed pattern fluency, not as a claim of
building production systems from this course alone.
