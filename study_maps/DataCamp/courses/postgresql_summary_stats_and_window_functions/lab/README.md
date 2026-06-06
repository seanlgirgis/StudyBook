# PostgreSQL Summary Stats and Window Functions Lab

A complete local PostgreSQL practice package built around the Summer Olympics medal dataset.

## What this lab covers

- Window functions versus `GROUP BY`
- `ROW_NUMBER()`
- `ORDER BY` inside `OVER()`
- `PARTITION BY`
- `LAG()` and `LEAD()`
- `FIRST_VALUE()` and `LAST_VALUE()`
- `RANK()` and `DENSE_RANK()`
- `NTILE()`
- Aggregate window functions
- Running totals
- Moving averages and moving totals
- Window frames
- `ROWS` versus `RANGE`
- `ROLLUP`
- `CUBE`
- `COALESCE()`
- `STRING_AGG()`
- PostgreSQL `tablefunc` and `CROSSTAB()`

## Package layout

```text
postgresql_summary_stats_and_window_functions_lab/
  README.md
  00_how_to_run.md
  lab_run_book.md
  run_lab.ps1
  data/
    summer.csv
  sql/
    00_create_schema.sql
    01_create_table.sql
    02_load_data.sql
    03_validate_data.sql
    exercises/
      01_window_foundations_exercises.sql
      02_fetching_ranking_paging_exercises.sql
      03_aggregate_frames_exercises.sql
      04_beyond_window_functions_exercises.sql
    solutions/
      01_window_foundations_solutions.sql
      02_fetching_ranking_paging_solutions.sql
      03_aggregate_frames_solutions.sql
      04_beyond_window_functions_solutions.sql
  expected_outputs/
    README.md
  notes/
    troubleshooting.md
```

## Recommended learning order

1. Run the setup scripts.
2. Run the validation script.
3. Work through each exercise file without opening the matching solution.
4. Compare your results with the solution file.
5. Record mistakes and observations in `lab_run_book.md`.

## Database objects

The lab creates:

```text
schema: dc_window_lab
table:  dc_window_lab.summer_medals
```

The setup script drops and recreates the schema, making the lab repeatable.
