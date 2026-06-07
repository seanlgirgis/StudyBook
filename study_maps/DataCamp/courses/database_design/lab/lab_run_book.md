# Database Design Lab Run Book

## Purpose

Practice translating workload requirements into an operational schema, an analytical schema, managed views, privileges, and a partitioned table.

## Checkpoints

1. **Operational design:** create normalized customer, product, order, and order-item tables.
2. **Integrity:** verify primary keys, foreign keys, checks, and transaction-friendly grain.
3. **Analytical design:** create dimensions and a sales fact table with one row per order line.
4. **Views:** expose a reporting summary and a stored materialized result.
5. **Access:** create an analyst role and grant read-only access to reporting objects.
6. **Partitioning:** create monthly event partitions and confirm rows route correctly.
7. **Validation:** answer the questions in `sql/05_validation_queries.sql`.

## Evidence to record

- PostgreSQL version
- commands run
- row counts
- `EXPLAIN` output for the partition-filter query
- materialized-view refresh result
- privilege test using an analyst login or `SET ROLE`
- mistakes and corrections

## Completion rule

The lab becomes **STRONG** only after all scripts run cleanly and evidence is captured under `expected_outputs/`.
