# PostgreSQL Summary Stats and Window Functions

Canonical DataCamp course package for:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\postgresql_summary_stats_and_window_functions
```

## Course identity

- Course: PostgreSQL Summary Stats and Window Functions
- Platform: DataCamp
- Level: Intermediate
- Platform status: Complete
- Prerequisite: Data Manipulation in SQL
- Canonical slug: `postgresql_summary_stats_and_window_functions`
- Dataset: Summer Olympics medal records
- Dataset rows: 31,165

## Current StudyBook status

```text
Platform status:        COMPLETE
Documentation coverage: STRONG
Lab package:            READY
Recall confidence:      DEVELOPING
Interview readiness:    NEEDS REPETITION
```

Passing the platform course means the DataCamp pass is complete. It does not mean permanent mastery. This course now moves into repetition, lab practice, and interview-review mode.

## Course chapters

1. Introduction to Window Functions
2. Fetching, Ranking, and Paging
3. Aggregate Window Functions and Frames
4. Beyond Window Functions

## Main course artifacts

### Course front door

```text
index.html
```

The course landing page links to the chapter guides, accumulated guide, quick lookup, lab, README, and documentation files.

### Accumulated course guides

```text
study_pages\field_guide.html
study_pages\field_guide.md
```

These provide the whole-course memory map and cross-chapter synthesis.

### Chapter guides

```text
study_pages\chapter_01_introduction_to_window_functions_field_guide.html
study_pages\chapter_02_fetching_ranking_and_paging_field_guide.html
study_pages\chapter_03_aggregate_window_functions_and_frames_field_guide.html
study_pages\chapter_04_beyond_window_functions_field_guide.html
```

### Quick reference

```text
study_pages\sql_quick_lookup.html
```

The Quick Lookup is a searchable syntax and decision reference for:

- `OVER()`
- `ORDER BY` inside `OVER()`
- `PARTITION BY`
- `ROW_NUMBER()`
- `LAG()` and `LEAD()`
- `FIRST_VALUE()` and `LAST_VALUE()`
- `RANK()` and `DENSE_RANK()`
- `NTILE()`
- aggregate window functions
- running totals
- moving averages and totals
- `ROWS` and `RANGE`
- `CROSSTAB()`
- `ROLLUP`
- `CUBE`
- `COALESCE()`
- `STRING_AGG()`

## Complete local lab

The course-local lab lives under:

```text
lab\
```

Main lab files:

```text
lab\lab_guide.html
lab\00_how_to_run.md
lab\lab_run_book.md
lab\run_lab.ps1
lab\data\summer.csv
lab\expected_outputs\README.md
lab\notes\troubleshooting.md
```

Setup and validation SQL:

```text
lab\sql\00_create_schema.sql
lab\sql\01_create_table.sql
lab\sql\02_load_data.sql
lab\sql\03_validate_data.sql
```

Exercise SQL:

```text
lab\sql\exercises\01_window_foundations_exercises.sql
lab\sql\exercises\02_fetching_ranking_paging_exercises.sql
lab\sql\exercises\03_aggregate_frames_exercises.sql
lab\sql\exercises\04_beyond_window_functions_exercises.sql
```

Solution SQL:

```text
lab\sql\solutions\01_window_foundations_solutions.sql
lab\sql\solutions\02_fetching_ranking_paging_solutions.sql
lab\sql\solutions\03_aggregate_frames_solutions.sql
lab\sql\solutions\04_beyond_window_functions_solutions.sql
```

## Run the lab

From PowerShell:

```powershell
cd D:\Workarea\StudyBook\study_maps\DataCamp\courses\postgresql_summary_stats_and_window_functions\lab

.\run_lab.ps1 -Database studybook -User postgres
```

The runner:

1. drops and recreates the `dc_window_lab` schema
2. creates the `summer_medals` table
3. loads `summer.csv`
4. validates the dataset
5. reports when the lab is ready

To run the solutions automatically after setup:

```powershell
.\run_lab.ps1 `
  -Database studybook `
  -User postgres `
  -RunSolutions
```

## Lab validation targets

Expected dataset checks:

```text
row_count:            31165
distinct_years:          27
first_year:            1896
last_year:             2012
distinct_countries:     147
distinct_athletes:    22762
distinct_events:        666
distinct_disciplines:    67
distinct_sports:         43
distinct_cities:         22
```

## Core course patterns

### Window function versus GROUP BY

```text
GROUP BY
→ collapses detail rows

Window function
→ preserves detail rows
→ adds an analytical value beside each row
```

### Ranking behavior

```text
ROW_NUMBER → unique row numbers
RANK       → ties with gaps
DENSE_RANK → ties without gaps
```

### Fetching behavior

```text
LAG  → previous row
LEAD → following row
```

### Running total

```sql
SUM(value) OVER (
    PARTITION BY group_col
    ORDER BY time_col
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

### Three-row moving average

```sql
AVG(value) OVER (
    PARTITION BY group_col
    ORDER BY time_col
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
```

### LAST_VALUE frame rule

```sql
LAST_VALUE(value) OVER (
    ORDER BY sort_col
    RANGE BETWEEN
        UNBOUNDED PRECEDING AND
        UNBOUNDED FOLLOWING
)
```

### Analytical shaping pattern

```text
aggregate first
→ rank second
→ pivot or summarize third
```

## Important mistakes to review

- confusing window `ORDER BY` with final query `ORDER BY`
- forgetting `PARTITION BY`
- using `LAST_VALUE()` without extending the frame
- choosing the wrong ranking function for ties
- miscounting frame rows
- using `RANGE` when exact physical rows are intended
- treating `NTILE()` as equal numeric ranges
- confusing `ROLLUP` with `CUBE`
- forgetting that `CROSSTAB()` requires `tablefunc` and an explicit output schema

## Interview sentence

> Window functions let me calculate rankings, row-to-row comparisons, running totals, moving statistics, and grouped analytical measures without collapsing the detailed result set as `GROUP BY` would.

## Documentation

```text
docs\BILL_OF_MATERIALS.md
docs\COURSE_SETUP_AUDIT.md
STUDYBUBBLE_SESSION_STATE.md
```

## Recommended review order

1. Open `index.html`.
2. Review `study_pages\field_guide.html`.
3. Revisit one chapter guide at a time.
4. Use `study_pages\sql_quick_lookup.html` for syntax recall.
5. Run the full lab.
6. Record mistakes in `lab\lab_run_book.md`.
7. Repeat the weakest topics without looking at the solutions.

## Ownership

Sean manages Git. Course-building and maintenance should preserve the canonical filenames and the stable number-free course slug.
