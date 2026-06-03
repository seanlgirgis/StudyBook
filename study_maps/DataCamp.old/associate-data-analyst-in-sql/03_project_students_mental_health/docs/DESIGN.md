# Design

## Scope
- Build a local SQL learning lab around one exported DataCamp project dataset.
- Keep loading repeatable by dropping and recreating `students` each run.
- Keep exploration and final solution SQL separate for practice.

## Components
- `sql/00_create_schema.sql`: table definition.
- `sql/01_load_data.sql`: psql-based load flow.
- `sql/02_explore_table.sql`: exploratory queries.
- `sql/03_project_solution.sql`: final grouped answer query.
- `scripts/load_students_csv.py`: Python loader for repeatable local ingestion.

## Data Typing Strategy
- Integer fields stay integer (`index`, `age`, `stay`, `japanese`, `english`, `todep`, `tosc`, `toas`).
- Text fields remain text for flexibility and easier raw inspection.
- Binary-like columns are kept as text first to avoid coercion mistakes during initial learning passes.

## Repeatability
- Loader executes `DROP TABLE IF EXISTS students` then `CREATE TABLE students`.
- CSV loads from `data/raw/students.csv` by default.
- Loader prints row count and a short preview after ingestion.
