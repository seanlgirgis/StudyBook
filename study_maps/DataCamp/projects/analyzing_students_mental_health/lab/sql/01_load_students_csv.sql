-- DataCamp Project: Analyzing Students' Mental Health
-- File: lab/sql/01_load_students_csv.sql
--
-- Purpose:
--   Load source_material/students.csv into the local PostgreSQL students table.
--
-- Run from psql with:
--   \i 01_load_students_csv.sql
--
-- This uses \copy, so PostgreSQL reads the CSV through the psql client.
-- The CSV columns are loaded by position, not by header name.

\echo 'Clearing existing rows from students...'
TRUNCATE TABLE students;

\echo 'Loading students.csv...'
\copy students FROM 'D:/Workarea/StudyBook/study_maps/DataCamp/projects/analyzing_students_mental_health/source_material/students.csv' WITH (FORMAT csv, HEADER true, NULL '');

\echo 'Load complete. Validating row count...'

SELECT COUNT(*) AS loaded_rows
FROM students;

\echo 'Previewing project columns...'

SELECT
    inter_dom,
    stay,
    todep,
    tosc,
    toas
FROM students
ORDER BY stay NULLS LAST
LIMIT 10;
