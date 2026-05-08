# Python Side Study Guide

## 1. Purpose

The Python side of this PostgreSQL telemetry/capacity interview lab connects to PostgreSQL, runs SELECT-only telemetry queries, loads the results into Pandas, summarizes service-level capacity metrics, exports reports, and validates the logic with pytest.

The goal is to show the full workflow:

1. Connect to the database.
2. Run safe telemetry queries.
3. Load SQL results into Pandas DataFrames.
4. Calculate capacity summaries.
5. Classify service capacity status.
6. Export CSV and Markdown reports.
7. Use tests to prove the logic works.

This gives you a practical story for interviews: you can move from raw telemetry data to a stakeholder-ready capacity report.

---

## 2. Folder Layout

### `src`

Reusable Python code lives here.

This folder contains database helpers, SQL query builders, Pandas capacity logic, and reporting utilities.

### `scripts`

Runnable Python scripts live here.

These are the command-line entry points you can run during practice or demonstration.

### `tests`

Pytest files live here.

These tests validate database connectivity, SQL safety, and Pandas capacity calculations.

### `outputs\csv`

Generated CSV files live here.

Example:

```text
outputs\csv\capacity_summary.csv
```

### `outputs\reports`

Generated Markdown reports live here.

Example:

```text
outputs\reports\capacity_summary.md
```

### `outputs\logs`

This folder is reserved for log files if future scripts need to write execution logs.

---

## 3. Source Files

### `src\db.py`

Database helper module.

It is responsible for:

- building the PostgreSQL connection URL
- creating the SQLAlchemy engine
- running SQL queries
- returning query results as Pandas DataFrames
- running a smoke test query

Main idea:

```text
Python connects to PostgreSQL once through a reusable helper instead of repeating connection code in every script.
```

### `src\telemetry_queries.py`

SQL query library.

It contains functions that return SELECT-only SQL strings for common telemetry questions, such as:

- listing public tables
- previewing telemetry samples
- calculating service average CPU and memory
- finding threshold-risk samples
- rolling up service metrics by hour
- previewing JSONB tags

Main idea:

```text
Keep SQL query text organized in one place so scripts stay clean and readable.
```

### `src\capacity_analysis.py`

Pandas capacity analysis module.

It contains helper functions that work on DataFrames after SQL results are loaded into Python.

It handles:

- capacity flags such as high CPU, high memory, high latency, and high error rate
- service-level summaries
- capacity status classification

Main idea:

```text
SQL retrieves telemetry data. Pandas adds business logic and capacity interpretation.
```

### `src\reporting.py`

Reporting helper module.

It handles:

- creating output directories
- exporting DataFrames to CSV
- writing Markdown text reports

Main idea:

```text
The final output should be something reviewable, shareable, and useful for decisions.
```

---

## 4. Scripts

### `scripts\01_smoke_test_db.py`

Use this first.

It verifies that Python can connect to the PostgreSQL database.

Run it when:

- starting a practice session
- checking whether Docker/Postgres is reachable
- debugging connection issues

Expected behavior:

```text
Returns current_database, current_user, and now().
```

### `scripts\02_run_basic_queries.py`

Runs basic telemetry queries.

It demonstrates:

- listing tables
- previewing telemetry rows
- calculating simple service averages
- finding threshold-risk rows
- previewing JSONB tags

Run it when:

```text
You want to confirm the database has data and the query layer works.
```

### `scripts\03_run_capacity_rollups.py`

Runs capacity rollup logic.

It demonstrates:

- hourly service rollups from SQL
- Pandas service-level summarization
- capacity status classification

Run it when:

```text
You want to practice explaining how telemetry becomes a capacity summary.
```

### `scripts\04_export_capacity_summary.py`

Exports final report outputs.

It creates:

```text
outputs\csv\capacity_summary.csv
outputs\reports\capacity_summary.md
```

Run it when:

```text
You want a stakeholder-style output file from the telemetry analysis.
```

---

## 5. Tests

### `tests\test_db_connection.py`

Validates that the database smoke test returns a result.

What it proves:

```text
Python can reach PostgreSQL and execute a simple SELECT query.
```

### `tests\test_capacity_analysis.py`

Validates Pandas capacity logic.

It checks:

- capacity flags
- service-level summary calculations
- capacity status classification

What it proves:

```text
The Python business logic behaves as expected on controlled sample data.
```

### `tests\test_telemetry_queries.py`

Validates SQL query safety.

It checks that query functions return SELECT statements and do not contain destructive SQL keywords such as:

- DROP
- DELETE
- UPDATE
- INSERT
- ALTER
- TRUNCATE

What it proves:

```text
The Python query layer is read-only and safe for this practice lab.
```

---

## 6. Commands To Run

Run these from the project folder:

```powershell
cd D:\Workarea\StudyBook\playground\prep
```

### Smoke test database connection

```powershell
python scripts\01_smoke_test_db.py
```

### Run basic queries

```powershell
python scripts\02_run_basic_queries.py
```

### Run capacity rollups

```powershell
python scripts\03_run_capacity_rollups.py
```

### Export capacity summary report

```powershell
python scripts\04_export_capacity_summary.py
```

### Run tests

```powershell
python -m pytest tests -v
```

### If connection fails from Windows

Try:

```powershell
$env:DB_HOST="localhost"
```

Then rerun the script.

---

## 7. Output Files

### `outputs\csv\capacity_summary.csv`

CSV version of the service-level capacity summary.

This is useful for:

- opening in Excel
- sharing tabular results
- feeding another reporting process

### `outputs\reports\capacity_summary.md`

Markdown version of the capacity summary.

This is useful for:

- interview review
- stakeholder-style explanation
- quick documentation
- turning analysis into a readable report

---

## 8. Interview Explanation

I built a small Python layer on top of the PostgreSQL telemetry lab. The Python code connects to Postgres, runs SELECT-only telemetry queries, loads the result into Pandas, calculates service-level capacity summaries, classifies capacity status, and exports CSV and Markdown reports. This shows the full path from database telemetry to an action-oriented capacity report.

---

## 9. What To Say About Tests

The pytest tests verify that the database connection works, query functions remain SELECT-only, and Pandas capacity calculations produce expected flags and summaries.

A good interview explanation:

```text
I added tests because capacity reporting needs trust. The database test proves connectivity, the query tests make sure the SQL layer stays read-only, and the Pandas tests verify the capacity calculations and classifications on controlled sample data.
```

---

## 10. Current Validation Snapshot

Current successful validation:

- `scripts\01_smoke_test_db.py` passed
- `scripts\02_run_basic_queries.py` passed
- `scripts\03_run_capacity_rollups.py` passed
- `scripts\04_export_capacity_summary.py` passed
- `python -m pytest tests -v` passed with 6 tests

This means the Python side is currently stable enough for interview practice and cheat-sheet creation.
