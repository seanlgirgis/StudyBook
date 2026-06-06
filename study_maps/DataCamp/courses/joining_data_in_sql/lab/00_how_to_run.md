# How to Run the Lab

## Option 1 — psql

```powershell
psql -U postgres -d studybook
```

Then run:

```sql
\i sql/00_create_schema.sql
\i sql/01_create_tables.sql
\i sql/02_insert_sample_data.sql
\i sql/03_inner_and_outer_joins.sql
\i sql/04_cross_and_self_joins.sql
\i sql/05_set_operations.sql
\i sql/06_subqueries.sql
\i sql/07_course_challenges.sql
```

## Option 2 — DBeaver

Open each SQL file in order and execute it against your PostgreSQL database.

## Reset

Rerun:

```sql
\i sql/00_create_schema.sql
```

The script drops and recreates the lab schema.
