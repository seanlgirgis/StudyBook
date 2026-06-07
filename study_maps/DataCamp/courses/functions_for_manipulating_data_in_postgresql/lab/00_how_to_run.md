# How to Run the Lab

From `psql` while connected to a practice database:

```psql
\i lab/sql/00_create_schema.sql
\i lab/sql/01_create_tables.sql
\i lab/sql/02_insert_sample_data.sql
\i lab/sql/03_data_types_and_arrays.sql
\i lab/sql/04_date_time_functions.sql
\i lab/sql/05_text_functions.sql
\i lab/sql/06_full_text_search_and_extensions.sql
```

Run from the canonical course root so the relative paths resolve. The scripts are rerunnable: the schema setup drops and recreates the lab schema.
