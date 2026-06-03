# Analyzing Students' Mental Health

This lab mirrors a DataCamp SQL project in a local PostgreSQL workflow so we can practice loading, exploring, and solving with repeatable scripts.

## Project Goal
Load the exported project CSV into local PostgreSQL, explore the dataset with SQL, and run the final project query.

## CSV Location
Put the CSV at:

`data/raw/students.csv`

If your export file is named differently, either rename it to `students.csv` or pass `--csv` to the loader.

## Run the Loader
From this project folder:

```powershell
python .\scripts\load_students_csv.py
```

Optional custom CSV path:

```powershell
python .\scripts\load_students_csv.py --csv .\data\raw\students.csv
```

## Database Connection Defaults
The loader reads environment variables and falls back to:

- host: `localhost`
- port: `5432`
- database: `postgres`
- user: `postgres`
- password: `postgres`

Supported environment variables:

- `PGHOST`
- `PGPORT`
- `PGDATABASE`
- `PGUSER`
- `PGPASSWORD`

## Run SQL Files

```powershell
psql -h localhost -p 5432 -U postgres -d postgres -f .\sql\00_create_schema.sql
psql -h localhost -p 5432 -U postgres -d postgres -f .\sql\01_load_data.sql
psql -h localhost -p 5432 -U postgres -d postgres -f .\sql\02_explore_table.sql
psql -h localhost -p 5432 -U postgres -d postgres -f .\sql\03_project_solution.sql
```

## Final Project Question
Analyze how social connectedness and acculturative stress indicators vary for international students based on length of stay, using grouped SQL aggregations.

## Troubleshooting: Password Authentication Failed
If you get `password authentication failed`, your local Docker Postgres may be running with different credentials than the defaults.

On this machine, active container `obs_pg` uses:
- `PGDATABASE=observability`
- `PGUSER=obs_user`
- `PGPASSWORD=obs_pass`

Use:

```powershell
$env:PGHOST="localhost"
$env:PGPORT="5432"
$env:PGDATABASE="observability"
$env:PGUSER="obs_user"
$env:PGPASSWORD="obs_pass"
python .\scripts\load_students_csv.py
```
