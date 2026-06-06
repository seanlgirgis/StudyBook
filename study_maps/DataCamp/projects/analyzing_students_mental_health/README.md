# Analyzing Students' Mental Health

A completed DataCamp SQL project rebuilt locally inside StudyBook.

## Project purpose

This project analyzes whether the length of stay is associated with average mental-health scores for international students.

The analysis:

- filters to international students
- groups students by `stay`
- counts students in each stay group
- calculates average depression, social-connectedness, and acculturative-stress scores
- rounds averages to two decimal places
- sorts the result by longest stay first

## Canonical project path

```text
D:\Workarea\StudyBook\study_maps\DataCamp\projects\analyzing_students_mental_health
```

## Project status

```text
Platform: COMPLETE
StudyBook package: COMPLETE
Documentation: STRONG
Lab: STRONG
Recall: DEVELOPING
Interview readiness: NEEDS REPETITION
```

## Main entry point

Open:

```text
index.html
```

This is the project front door.

## Project structure

```text
analyzing_students_mental_health\
├── index.html
├── README.md
├── docs\
│   └── PROJECT_SETUP_AUDIT.md
├── source_material\
│   ├── README.md
│   └── students.csv
├── study_pages\
│   ├── project_field_guide.html
│   └── sql_quick_lookup.html
└── lab\
    ├── lab_guide.html
    ├── expected_outputs\
    │   └── README.md
    ├── notes\
    │   └── troubleshooting.md
    └── sql\
        ├── 00_create_students_table.sql
        ├── 01_load_students_csv.sql
        ├── 02_project_solution.sql
        └── 03_practice_queries.sql
```

## Study resources

### Project Field Guide

```text
study_pages\project_field_guide.html
```

Use this for:

- the project question
- dataset-column meaning
- query construction
- final SQL
- validated results
- common mistakes
- interpretation cautions
- interview translation

### SQL Quick Lookup

```text
study_pages\sql_quick_lookup.html
```

Use this when you need a compact reminder for:

- `WHERE`
- `IS NOT NULL`
- `GROUP BY`
- `COUNT(*)`
- `AVG()`
- `ROUND()`
- `ORDER BY`
- CTEs
- `HAVING`
- validation queries

### Local Lab Guide

```text
lab\lab_guide.html
```

Use this to recreate the project in PostgreSQL from the original CSV.

## Local database evidence

The project was validated locally with:

```text
Database: observability
Schema: public
Table: students
Source rows: 286
Complete international rows analyzed: 201
Stay groups: 9
Final output: 9 rows × 5 columns
```

## SQL workflow

Run these files in order from `psql`:

```sql
\i 00_create_students_table.sql
\i 01_load_students_csv.sql
\i 02_project_solution.sql
\i 03_practice_queries.sql
```

A convenient `psql` working directory is:

```sql
\cd D:/Workarea/StudyBook/study_maps/DataCamp/projects/analyzing_students_mental_health/lab/sql
```

## Final project query

```sql
WITH clean_students AS (
    SELECT
        inter_dom,
        stay,
        todep,
        tosc,
        toas
    FROM students
    WHERE inter_dom IS NOT NULL
      AND stay IS NOT NULL
      AND todep IS NOT NULL
      AND tosc IS NOT NULL
      AND toas IS NOT NULL
)
SELECT
    stay,
    COUNT(*) AS count_int,
    ROUND(AVG(todep), 2) AS average_phq,
    ROUND(AVG(tosc), 2) AS average_scs,
    ROUND(AVG(toas), 2) AS average_as
FROM clean_students
WHERE inter_dom = 'Inter'
GROUP BY stay
ORDER BY stay DESC;
```

## Core SQL pattern

```sql
SELECT
    group_column,
    COUNT(*) AS group_size,
    ROUND(AVG(metric), 2) AS average_metric
FROM table_name
WHERE row_filter
GROUP BY group_column
ORDER BY group_column DESC;
```

For this project:

```text
group_column = stay
row_filter   = inter_dom = 'Inter'
metrics      = todep, tosc, toas
```

## Interpretation rule

The result is descriptive.

It shows how average scores vary across length-of-stay groups, but it does not prove that length of stay caused any mental-health outcome.

Groups with only one or a few students should not be used for strong conclusions.

## Best review order

```text
1. Open index.html
2. Read project_field_guide.html
3. Run the local lab
4. Use sql_quick_lookup.html during recall practice
5. Complete queries in 03_practice_queries.sql
```

## Navigation

- Project home: `index.html`
- DataCamp root: `..\..\index.html`
- Projects index: `..\index.html`
- SQL Fundamentals track: `..\..\skill_tracks\01_sql_fundamentals\index.html`
