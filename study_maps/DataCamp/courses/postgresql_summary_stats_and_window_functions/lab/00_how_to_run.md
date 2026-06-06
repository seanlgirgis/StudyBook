# How to Run the Lab

## Requirements

- PostgreSQL
- `psql` available in PowerShell
- A database you can create schemas and tables in

The default commands use:

```text
user:     postgres
database: studybook
```

Change those values if your local environment differs.

## Fastest method

From PowerShell:

```powershell
cd D:\Workarea\StudyBook\study_maps\DataCamp\courses\postgresql_summary_stats_and_window_functions\lab

.\run_lab.ps1 -Database studybook -User postgres
```

## Manual setup

Run from the lab root:

```powershell
psql -U postgres -d studybook -v ON_ERROR_STOP=1 -f .\sql\00_create_schema.sql
psql -U postgres -d studybook -v ON_ERROR_STOP=1 -f .\sql\01_create_table.sql
psql -U postgres -d studybook -v ON_ERROR_STOP=1 -f .\sql\02_load_data.sql
psql -U postgres -d studybook -v ON_ERROR_STOP=1 -f .\sql\03_validate_data.sql
```

## Run one exercise file

```powershell
psql -U postgres -d studybook -v ON_ERROR_STOP=1 `
  -f .\sql\exercises\01_window_foundations_exercises.sql
```

## Run the matching solutions

```powershell
psql -U postgres -d studybook -v ON_ERROR_STOP=1 `
  -f .\sql\solutions\01_window_foundations_solutions.sql
```

## Run inside psql

```sql
\i 'D:/Workarea/StudyBook/study_maps/DataCamp/courses/postgresql_summary_stats_and_window_functions/lab/sql/00_create_schema.sql'
\i 'D:/Workarea/StudyBook/study_maps/DataCamp/courses/postgresql_summary_stats_and_window_functions/lab/sql/01_create_table.sql'
\i 'D:/Workarea/StudyBook/study_maps/DataCamp/courses/postgresql_summary_stats_and_window_functions/lab/sql/02_load_data.sql'
\i 'D:/Workarea/StudyBook/study_maps/DataCamp/courses/postgresql_summary_stats_and_window_functions/lab/sql/03_validate_data.sql'
```

Run `\q` to leave psql.
