# Expected Outputs

This folder documents the expected results for the local PostgreSQL version of:

```text
Analyzing Students' Mental Health
```

## Final project output

Run:

```sql
\i ../sql/02_project_solution.sql
```

Expected result:

```text
 stay | count_int | average_phq | average_scs | average_as
------+-----------+-------------+-------------+------------
   10 |         1 |       13.00 |       32.00 |      50.00
    8 |         1 |       10.00 |       44.00 |      65.00
    7 |         1 |        4.00 |       48.00 |      45.00
    6 |         3 |        6.00 |       38.00 |      58.67
    5 |         1 |        0.00 |       34.00 |      91.00
    4 |        14 |        8.57 |       33.93 |      87.71
    3 |        46 |        9.09 |       37.13 |      78.00
    2 |        39 |        8.28 |       37.08 |      77.67
    1 |        95 |        7.48 |       38.11 |      72.80
(9 rows)
```

## Validation outputs

Expected complete international rows:

```text
 international_rows
--------------------
                201
(1 row)
```

Expected number of stay groups:

```text
 stay_groups
-------------
           9
(1 row)
```

## Source load validation

Run:

```sql
SELECT COUNT(*) AS loaded_rows
FROM students;
```

Expected:

```text
 loaded_rows
-------------
         286
(1 row)
```

## Acceptance criteria

The local project is considered correctly reproduced when all of the following are true:

```text
[ ] public.students exists
[ ] 286 source rows are loaded
[ ] 201 complete international rows are analyzed
[ ] 9 distinct stay groups are returned
[ ] the final result contains 5 columns
[ ] result aliases match the DataCamp project
[ ] rows are ordered by stay descending
[ ] averages are rounded to 2 decimal places
```

## Required output columns

```text
stay
count_int
average_phq
average_scs
average_as
```

## Important interpretation note

These outputs are descriptive summaries.

Groups with only one or a few students should not be used to support strong conclusions about mental-health trends.

## Related files

```text
..\sql\00_create_students_table.sql
..\sql\01_load_students_csv.sql
..\sql\02_project_solution.sql
..\lab_guide.html
..\..\study_pages\project_field_guide.html
```
