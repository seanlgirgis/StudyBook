# Course 05 Muscle-Memory Lab (PostgreSQL)

## Purpose
Local practice lab for Course 05 concepts:
- window functions
- summary stats
- pivoting
- ROLLUP/CUBE
- COALESCE
- STRING_AGG
- interview-style ranking drills

## Schema safety
All objects are created under:
`course05_muscle`

No `public` table drops are used in this lab.

## Tables and training focus
- `course05_muscle.sales_events`
  - running totals, moving averages/totals, NTILE buckets, percent of total
- `course05_muscle.employee_sales`
  - ROW_NUMBER/RANK/DENSE_RANK, third salesperson per department
- `course05_muscle.server_telemetry`
  - percentile_cont/percentile_disc, NTILE(100), time-window analysis
- `course05_muscle.olympic_medals_practice`
  - event champion LAG, medal ranking, CROSSTAB, ROLLUP/CUBE, STRING_AGG
- `course05_muscle.support_tickets`
  - LAG/LEAD, moving averages, priority-based resolution ranking

## Run order
1. `00_create_schema.sql`
2. `01_create_tables.sql`
3. `02_seed_sales_events.sql`
4. `03_seed_employee_sales.sql`
5. `04_seed_server_telemetry.sql`
6. `05_seed_olympic_medals_practice.sql`
7. `06_seed_support_tickets.sql`
8. `07_validation_queries.sql`

## Notes
- Seed data is synthetic and training-focused.
- Data includes realistic variation, ties, and outliers for robust window-function behavior.
