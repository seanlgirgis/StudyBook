# Troubleshooting Notes

Project:

```text
Analyzing Students' Mental Health
```

Local database:

```text
Database: observability
Schema: public
Table: students
```

## 1. `\i` reports “No such file or directory”

Example:

```text
02_project_solution.sql: No such file or directory
```

Cause:

`psql` is not currently working from the folder that contains the SQL file.

Fix:

```sql
\cd D:/Workarea/StudyBook/study_maps/DataCamp/projects/analyzing_students_mental_health/lab/sql
```

Then run:

```sql
\i 02_project_solution.sql
```

Alternative:

Use the full path:

```sql
\i D:/Workarea/StudyBook/study_maps/DataCamp/projects/analyzing_students_mental_health/lab/sql/02_project_solution.sql
```

## 2. PowerShell blocks the scaffold script

Example:

```text
The file is not digitally signed.
```

Cause:

Windows marked the downloaded PowerShell script as coming from the internet, or the current execution policy blocks unsigned scripts.

Fix for one file:

```powershell
Unblock-File .\scaffold_analyzing_students_mental_health.ps1
```

Then run:

```powershell
.\scaffold_analyzing_students_mental_health.ps1
```

Alternative one-time bypass:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\scaffold_analyzing_students_mental_health.ps1
```

## 3. The CSV cannot be found

Expected source path:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\projects\analyzing_students_mental_health\source_material\students.csv
```

Check from PowerShell:

```powershell
Test-Path "D:\Workarea\StudyBook\study_maps\DataCamp\projects\analyzing_students_mental_health\source_material\students.csv"
```

Expected result:

```text
True
```

## 4. `\copy` fails on the Windows path

Use forward slashes inside the SQL file:

```sql
\copy students FROM 'D:/Workarea/StudyBook/study_maps/DataCamp/projects/analyzing_students_mental_health/source_material/students.csv'
WITH (FORMAT csv, HEADER true, NULL '');
```

Do not use an unescaped Windows path such as:

```text
D:\Workarea\...
```

inside the SQL string.

## 5. The `students` table does not exist

Run the create script first:

```sql
\i 00_create_students_table.sql
```

Then confirm:

```sql
\d students
```

## 6. The table has duplicate rows after loading

The provided loader starts with:

```sql
TRUNCATE TABLE students;
```

Use:

```sql
\i 01_load_students_csv.sql
```

This clears the current rows before loading the CSV again.

Confirm the total:

```sql
SELECT COUNT(*)
FROM students;
```

Expected:

```text
286
```

## 7. The row count is not 286

Possible causes:

- the wrong CSV was loaded
- the load stopped before completion
- the table contained extra rows
- the source file was edited
- the load script was changed

Recovery:

```sql
\i 00_create_students_table.sql
\i 01_load_students_csv.sql
```

Then validate:

```sql
SELECT COUNT(*) AS loaded_rows
FROM students;
```

Expected:

```text
286
```

## 8. The final query does not return 9 rows

Check the project filter:

```sql
WHERE inter_dom = 'Inter'
```

Check the grouping:

```sql
GROUP BY stay
```

Check the number of groups directly:

```sql
SELECT COUNT(DISTINCT stay) AS stay_groups
FROM students
WHERE inter_dom = 'Inter'
  AND stay IS NOT NULL
  AND todep IS NOT NULL
  AND tosc IS NOT NULL
  AND toas IS NOT NULL;
```

Expected:

```text
9
```

## 9. PostgreSQL rejects a selected column

Example error:

```text
column must appear in the GROUP BY clause or be used in an aggregate function
```

Cause:

A selected column is neither grouped nor aggregated.

Correct pattern:

```sql
SELECT
    stay,
    COUNT(*),
    AVG(todep)
FROM students
GROUP BY stay;
```

## 10. The averages have too many decimal places

Use:

```sql
ROUND(AVG(todep), 2)
```

The `2` means two digits after the decimal point.

## 11. The output order is wrong

Use:

```sql
ORDER BY stay DESC;
```

`DESC` means highest to lowest.

Expected stay order:

```text
10, 8, 7, 6, 5, 4, 3, 2, 1
```

## 12. The local `phone` column differs from the CSV header

The source CSV header contains:

```text
 phone
```

with a leading space.

The local PostgreSQL table intentionally normalizes it to:

```text
phone
```

The CSV load still works because `\copy` loads values by column position.

Do not edit the source CSV just to remove the leading space.

## 13. The result differs from the documented output

Validate the important values:

```sql
SELECT COUNT(*) AS international_rows
FROM students
WHERE inter_dom = 'Inter'
  AND stay IS NOT NULL
  AND todep IS NOT NULL
  AND tosc IS NOT NULL
  AND toas IS NOT NULL;
```

Expected:

```text
201
```

Then rerun:

```sql
\i 02_project_solution.sql
```

Compare against:

```text
..\expected_outputs\README.md
```

## 14. Useful psql commands

```sql
\conninfo
\dt
\d students
\cd D:/Workarea/StudyBook/study_maps/DataCamp/projects/analyzing_students_mental_health/lab/sql
\i 00_create_students_table.sql
\i 01_load_students_csv.sql
\i 02_project_solution.sql
\q
```

## Known validated state

```text
Table creation: successful
CSV load: successful
Rows loaded: 286
International rows analyzed: 201
Stay groups: 9
Final output: 9 rows × 5 columns
```
