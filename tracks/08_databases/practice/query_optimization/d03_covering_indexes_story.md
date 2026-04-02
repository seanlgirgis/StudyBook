# Covering Indexes — Story Map

## Story
Customer support needs quick order lookups. The query is “indexed,” but still feels slower than expected.

## Scenario
You search orders by customer email and only need `status` and `total_cents`.
There is a normal index on `customer_email`.

## Pain
The index finds the row, but the database still has to fetch the full row from the table.
That extra hop adds latency and IO.

## Diagnosis
A **covering index** includes all columns needed by the query.
Normal index = helps find rows.
Covering index = may answer the query **from the index alone**.

## Fix
Add the needed columns to the index:
`(customer_email) INCLUDE (status, total_cents)`

## Pattern
Covering indexes are for **frequently read** queries that return a few columns.
Avoid `SELECT *` when you care about coverage.

## System
Less table access = fewer page reads = faster response under load.

## Index-Only Scan
If the planner can trust the visibility map, it may use **Index Only Scan**.
Sometimes it still hits the table, even with coverage.
Runtime proof should be checked by the index name in the plan.
Index-only behavior can vary with the visibility map.

## Mental Model
Normal index:
- “I found the row location, now go fetch the row.”

Covering index:
- “Everything needed may already be in the index.”

## Run Order
1. c055_covering_index_vs_normal_index.py
2. c056_index_only_scan_demo.py
