# Joining Data in SQL — Integrated Course Lab

This lab reinforces the full DataCamp course with a compact PostgreSQL dataset.

## Main practice areas

- INNER, LEFT, RIGHT, FULL, CROSS, and self joins
- Join cardinality and accidental row multiplication
- `ON` versus `WHERE` with outer joins
- `UNION`, `UNION ALL`, `INTERSECT`, and `EXCEPT`
- Semi joins and anti joins
- `IN`, `EXISTS`, `NOT EXISTS`, and the `NOT IN`/`NULL` trap
- Subqueries in `WHERE`, `SELECT`, and `FROM`
- Conditional aggregation as an alternative to a self join

## Recommended run order

1. `sql/00_create_schema.sql`
2. `sql/01_create_tables.sql`
3. `sql/02_insert_sample_data.sql`
4. `sql/03_inner_and_outer_joins.sql`
5. `sql/04_cross_and_self_joins.sql`
6. `sql/05_set_operations.sql`
7. `sql/06_subqueries.sql`
8. `sql/07_course_challenges.sql`

## PostgreSQL notes

The scripts are written for PostgreSQL and use the schema:

```sql
joining_data_lab
```

Run them from `psql`, DBeaver, or another PostgreSQL client.
