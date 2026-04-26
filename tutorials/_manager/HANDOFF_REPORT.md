# StudyBook Tutorials - Handoff Report
Generated: 2026-04-26
Scope: `D:\Workarea\StudyBook\tutorials`

## Evidence Policy (Used In This Report)

- `independently verified`: proven in this sync by running tests/commands.
- `user-reported working`: provided by user as working; not re-run in this sync.
- `repo evidence only`: inferred from files present (prompts/code/tests/readme), but no run proof in this sync.

## Current Tutorial Folder Inventory

| Folder | Status Class | prompt.md | READY_TO_PASTE | setup/tutorial .py | capstone files | test files | README/notes | Verification note |
|---|---|---|---|---|---|---|---|---|
| `01_aws_kinesis` | Tested / working | yes | yes | yes (5) | yes | yes (1) | yes | user-reported working |
| `02_pyspark` | Tested / working | yes | yes | yes (6) | no | no | yes | user-reported working |
| `02_PySpark_Docker` | Tested / working | no | no | yes (7 + `common/spark_session.py`) | no | no | yes | user-reported working; intentional variant |
| `03_apache_airflow` | READY_TO_PASTE only | yes | yes | no | no | no | no | repo evidence only |
| `04_aws_step_functions` | READY_TO_PASTE only | yes | yes | no | no | no | no | repo evidence only |
| `05_delta_lake` | READY_TO_PASTE only | yes | yes | no | no | no | no | repo evidence only |
| `06_aws_emr` | READY_TO_PASTE only | yes | yes | no | no | no | no | repo evidence only |
| `07_aws_glue` | READY_TO_PASTE only | yes | yes | no | no | no | no | repo evidence only |
| `08_aws_s3` | Tested / working | yes | no | yes (5 in `setup/`) | yes | yes (1) | yes | user-reported working |
| `09_aws_cloudwatch` | Tested / working | yes | yes | yes (5 in `setup/`) | yes | yes (1) | yes | user-reported working |
| `10_python_logging` | Tested / working | yes | yes | yes (5) | yes | yes (1) | yes | user-reported working |
| `11_dbt` | READY_TO_PASTE only | yes | yes | no | no | no | no | repo evidence only |
| `12_parquet` | Tested / working | yes | yes | yes (6) | yes (`06_parquet_capstone_pipeline.py`) | yes (1) | yes | user-reported working |
| `13_python_concurrency` | Tested / working | yes | yes | yes (5) | yes | yes (1) | yes | user-reported working |
| `14_encryption` | Tested / working | no | yes | yes (5) | yes | yes (1) | yes | user-reported working |
| `24_pandas` | READY_TO_PASTE only | no | yes | no | no | no | no | repo evidence only |
| `26_polars` | READY_TO_PASTE only | no | yes | no | no | no | no | repo evidence only |
| `27_duckdb` | READY_TO_PASTE only | no | yes | no | no | no | no | repo evidence only |
| `33_aws_msk_kafka` | READY_TO_PASTE only | no | yes | no | no | no | no | repo evidence only |
| `36_docker` | READY_TO_PASTE only | no | yes | no | no | no | no | repo evidence only |

## PySpark Tracks (Important)

- `02_pyspark` is the canonical local `local[*]` PySpark tutorial track.
- `02_PySpark_Docker` is an intentional Docker/Spark-cluster variant track.
- `02_PySpark_Docker` is **not** marked as duplicate/archive candidate in this report.

## Status Buckets (As Of 2026-04-26)

- Tested / working (user-reported): `01, 02, 02_PySpark_Docker, 08, 09, 10, 12, 13, 14`
- Code exists but untested: none currently identified from available evidence + user updates
- READY_TO_PASTE only: `03, 04, 05, 06, 07, 11, 24, 26, 27, 33, 36`
- Not started (topic folder missing): `15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 28, 29, 30, 31, 32, 34, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47`
- Duplicate/archive candidates: none

## Outstanding Tasks (Priority Order)

1. Generate code from READY_TO_PASTE folders: `03, 04, 05, 06, 07, 11, 24, 26, 27, 33, 36`.
2. Add missing topic folders/prompts for not-started topics (`15-23`, `25`, `28-32`, `34-35`, `37-47`).
3. Run independent verification for user-reported-working tutorials and capture logs/pytest output under each topic README or session log.
4. Normalize prompt coverage gaps where code exists but `prompt.md` is missing (`14_encryption`, plus READY-only tracks without `prompt.md` where desired).
