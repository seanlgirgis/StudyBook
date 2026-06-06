# How to Run the Lab

## Option A — run from psql

```powershell
cd D:\Workarea\StudyBook\study_maps\DataCamp\courses\postgresql_summary_stats_and_window_functions\lab
psql -U postgres -d studybook -f .\sql\00_create_schema.sql
psql -U postgres -d studybook -f .\sql\01_create_tables.sql
psql -U postgres -d studybook -f .\sql\02_load_summer_data.sql
psql -U postgres -d studybook -f .\sql\03_window_function_practice.sql
psql -U postgres -d studybook -f .\sql\04_advanced_summary_practice.sql
```

Change the PostgreSQL user or database if your local environment uses different values.

## Option B — from inside psql

```sql
\i 'D:/Workarea/StudyBook/study_maps/DataCamp/courses/postgresql_summary_stats_and_window_functions/lab/sql/00_create_schema.sql'
\i 'D:/Workarea/StudyBook/study_maps/DataCamp/courses/postgresql_summary_stats_and_window_functions/lab/sql/01_create_tables.sql'
\i 'D:/Workarea/StudyBook/study_maps/DataCamp/courses/postgresql_summary_stats_and_window_functions/lab/sql/02_load_summer_data.sql'
```
