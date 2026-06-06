# How to Run

## psql

```powershell
psql -U postgres -d observability
```

Then:

```sql
\i 'D:/Workarea/StudyBook/study_maps/DataCamp/courses/data_manipulation_in_sql/lab/sql/00_create_lab_schema.sql'
\i 'D:/Workarea/StudyBook/study_maps/DataCamp/courses/data_manipulation_in_sql/lab/sql/01_create_tables.sql'
\i 'D:/Workarea/StudyBook/study_maps/DataCamp/courses/data_manipulation_in_sql/lab/sql/02_insert_sample_data.sql'
```

Run the chapter scripts afterward.

## DBeaver

Open each SQL file in order and execute it against your PostgreSQL connection.

## Reset

Run `00_create_lab_schema.sql` again. It drops and recreates the lab schema.
