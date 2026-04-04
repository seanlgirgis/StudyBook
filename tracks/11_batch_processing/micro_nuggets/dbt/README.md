# dbt Micro-Nuggets Learning Lane

## What This Lane Teaches

A complete, hands-on dbt curriculum from first principles to production patterns:

- dbt project structure, profiles.yml, and dbt debug
- Sources and the staging layer (source() vs ref())
- All four materialization types: view, table, incremental, ephemeral
- The ref() DAG and graph operators for lineage exploration
- Generic tests (not_null, unique, relationships, accepted_values)
- Singular (custom) tests and data contracts
- SCD Type 2 snapshots with check and timestamp strategies
- dbt build, docs generate, and artifact parsing (manifest.json)
- Node selectors, graph operators, state:modified for CI/CD
- Bronze → Silver → Gold medallion architecture capstone

**Auto-detected backend:** PostgreSQL (if running) → Snowflake → Databricks → DuckDB (always available)

---

## Prerequisites

| Requirement | Version | Check |
|-------------|---------|-------|
| Python | >= 3.9 | `python --version` |
| dbt-core | >= 1.5 | `python -m dbt --version` |
| dbt-duckdb | >= 1.5 | `pip show dbt-duckdb` |

---

## Beginner Execution Guide

### Step 0: Open the folder

```powershell
cd D:\StudyBook\tracks\11_batch_processing\micro_nuggets\dbt
```

### Step 1: Activate Python environment

```powershell
D:\StudyBook\venv\Scripts\Activate.ps1
```

### Step 2: Install dbt

**Option A: Using uv (recommended — avoids Python 3.14 incompatibility)**
```powershell
# Install uv if not present: winget install astral-sh.uv
# From the dbt lane directory:
uv venv .venv_dbt --python 3.13
uv pip install --python .venv_dbt/Scripts/python.exe dbt-core dbt-duckdb
```

The lane auto-detects `.venv_dbt/Scripts/python.exe` and uses it for all dbt commands.

**Option B: pip (requires Python 3.9-3.12; Python 3.14 NOT supported by dbt)**
```powershell
pip install dbt-core dbt-duckdb
```

For PostgreSQL backend (optional):
```powershell
pip install dbt-postgres
```

### Step 3: Check prerequisites

```powershell
python 00_setup\00_prereq_check.py
```

Expected output: all checks PASS. If any FAIL, follow the exact fix shown.

### Step 4: Seed the lab database

```powershell
python 00_setup\01_seed_lab.py
```

This writes the CSV files, generates `profiles.yml`, runs `dbt deps`, and runs `dbt seed`.
Expected: 5 tables created with 20/30/40/10/25 rows each.

### Step 5: Run a single nugget

```powershell
python 01_dbt_basics\01_project_init_and_profiles.py
```

### Step 6: Run all nuggets

```powershell
python run_all_dbt_nuggets.py
```

With options:
```powershell
# Skip setup scripts (already seeded)
python run_all_dbt_nuggets.py --skip-setup

# Stop on first failure
python run_all_dbt_nuggets.py --stop-on-fail --skip-setup

# Show output for passing scripts too
python run_all_dbt_nuggets.py --show-pass-output --skip-setup

# Longer timeout for slow machines
python run_all_dbt_nuggets.py --timeout 240 --skip-setup
```

### Step 7: Reset the lab (start fresh)

```powershell
python 00_setup\99_reset_lab.py --confirm
```

Then re-seed:
```powershell
python 00_setup\01_seed_lab.py
```

---

## Nugget Execution Order

```
00_setup\00_prereq_check.py          ← Always run first
00_setup\01_seed_lab.py              ← Must run before any nugget
01_dbt_basics\01_project_init_...    ← dbt structure + profiles
01_dbt_basics\02_sources_and_...     ← source() + staging layer
02_modeling...\01_views_tables_...   ← materializations
02_modeling...\02_ephemeral_and_...  ← ref() DAG + ls
03_tests...\01_generic_tests.py      ← built-in tests
03_tests...\02_custom_tests_...      ← singular tests + contracts
04_snapshots...\01_snapshots_scd2.py ← SCD Type 2
05_operations...\01_run_build_...    ← build + docs + artifacts
05_operations...\02_selectors_...    ← selectors + state
06_interview_drills\01_...           ← 15 Q&A review
07_mini_capstone\01_...              ← Bronze→Silver→Gold
```

---

## Backend Selection

The lane auto-detects the best available backend:

| Backend | When selected | Adapter package |
|---------|--------------|-----------------|
| PostgreSQL | `localhost:5432` reachable | `dbt-postgres` |
| Snowflake | `SNOWFLAKE_ACCOUNT/USER/PASSWORD` env vars set | `dbt-snowflake` |
| Databricks | `DATABRICKS_HOST/TOKEN/HTTP_PATH` env vars set | `dbt-databricks` |
| DuckDB | Always available (fallback) | `dbt-duckdb` |

**For most learners:** DuckDB is the default. No server required. The database
is a single file at `lab_dbt_project/lab_dbt.duckdb`.

To use PostgreSQL (local Docker):
```powershell
cd D:\StudyBook\_infra
.\scripts\infra_up.ps1
```

---

## Common Failures and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: dbt` | dbt-core not installed | `pip install dbt-core dbt-duckdb` |
| `ModuleNotFoundError: dbt.adapters.duckdb` | dbt-duckdb not installed | `pip install dbt-duckdb` |
| `profiles.yml not found` | profiles.yml not generated yet | `python 00_setup\01_seed_lab.py` |
| `Could not find profile named 'dbt_lab'` | Wrong profiles.yml location | Use `--profiles-dir` flag (auto-added by lane) |
| `dbt seed failed` | CSV files missing or corrupt | `python 00_setup\01_seed_lab.py` (re-writes CSVs) |
| `Database locked` (DuckDB) | Two scripts running simultaneously | Run scripts one at a time (they share the .duckdb file) |
| `Table not found` in nugget | Setup not run | `python 00_setup\01_seed_lab.py` first |
| Test failures (positive_amounts) | Intentional seed data | Expected — 0-amount refunds are teaching material |
| Test failures (unique email) | Intentional seed data | Expected — duplicate email is teaching material |
| `dbt debug` connection error | profiles.yml has wrong creds | Check auto-detection: `python _dbt_lane_connect.py` |

---

## Key Files

| File | Purpose |
|------|---------|
| `_dbt_lane_connect.py` | Backend detection, profiles.yml generation, dbt runner |
| `lab_dbt_project/dbt_project.yml` | dbt project config (materializations, paths, tags) |
| `lab_dbt_project/profiles.yml` | Generated credentials file (DO NOT commit) |
| `lab_dbt_project/profiles_template.yml` | Template for all backends (safe to commit) |
| `lab_dbt_project/target/manifest.json` | dbt project graph artifact |
| `lab_dbt_project/lab_dbt.duckdb` | DuckDB database file (generated on seed) |

---

## Further Reading

- `DBT_SPEEDY_STORY_AND_INTERVIEW.md` — Narrative learning guide + interview Q&A
- `DBT_GLOSSARY.md` — Plain-English definitions for every dbt term
- [dbt official docs](https://docs.getdbt.com)
