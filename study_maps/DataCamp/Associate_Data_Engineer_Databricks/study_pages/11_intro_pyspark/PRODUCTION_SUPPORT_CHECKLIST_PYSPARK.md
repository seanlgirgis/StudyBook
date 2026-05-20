# Production Support Checklist - PySpark

## Pre-Run
- Confirm input data arrival and partition/date readiness.
- Confirm scheduler parameters and environment values.
- Confirm upstream dependencies completed.

- collect() safety check: ensure no large distributed dataset is being pulled to driver memory.
- Track stage progress and failed stage ids.
- Watch executor errors and retry churn.
- Watch skew/shuffle-heavy phases.

- UDF/pandas UDF necessity review: can built-in Spark functions replace custom UDF logic?
- Input row counts.
- Output row counts.
- Schema compatibility checks.
- Null/duplicate checks.
- Join row-count checks before/after enrichment.

## Failure Triage
- Identify failing step: read / transform / join / shuffle / write.
- Capture error text, stage id, executor context.
- Check recent schema or parameter changes.
- Check downstream write mode (`overwrite` vs `append`) risk.

## Rerun Safety
- Confirm idempotence expectations.
- Confirm whether rerun duplicates data.
- Confirm checkpoint/target cleanup strategy if needed.
- Communicate rerun decision and impact clearly.

## Interview-Safe Summary
I support PySpark jobs by combining execution diagnostics (logs, stages, executors)
with data controls (counts, schema, nulls, duplicates) and safe rerun decisions.



- Validate row counts before and after Spark SQL filters, joins, and aggregations.
- Confirm whether SQL views are temporary or persisted outputs.


- When using Spark SQL outputs, validate data types and row counts before using summary statistics.


- Validate numeric types before SUM/AVG.
- Check row counts before and after filters.
- Validate grouping columns and unexpected null groups.
- Use explain() when aggregation performance is a concern.


- Use explain() when performance is a concern.
- Watch for shuffles in joins and aggregations.
- Avoid repeated actions that trigger repeated jobs.
- Cache/persist only reused DataFrames.
- Unpersist when done.
- Consider broadcast joins for small lookup DataFrames.


- Foundation completed note: this checklist covers foundational support practice, not advanced Spark administration.

