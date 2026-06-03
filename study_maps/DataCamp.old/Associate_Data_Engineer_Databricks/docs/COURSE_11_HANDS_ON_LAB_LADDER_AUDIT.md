# Course 11 Hands-On Lab Ladder Audit

## Lab Ladder Purpose
Create a runnable, small-step PySpark lab ladder for Course 11 concepts while keeping runnable content under `tutorials` only.

## Labs Created
1. 01_sparksession_dataframe_basics
2. 02_reading_data_and_schemas
3. 03_missing_data_and_columns
4. 04_filtering_and_aggregations
5. 05_joins_and_unions
6. 06_udfs_and_pandas_udfs
7. 07_rdds_vs_dataframes
8. 08_spark_sql_temp_views
9. 09_scale_explain_cache_broadcast
10. 10_production_support_checks

## Files Created
- tutorials/DataCamp/Associate_Data_Engineer_Databricks/index.html
- tutorials/DataCamp/Associate_Data_Engineer_Databricks/README.md
- tutorials/DataCamp/Associate_Data_Engineer_Databricks/course_11_intro_pyspark/LAB_SEQUENCE.md
- For each of 10 labs:
  - README.md
  - lab_<short_name>.py
  - expected_output.md
  - troubleshooting.md

## Files Changed
- study_pages/11_intro_pyspark/index.html (Hands-On Labs section and links)
- docs/COURSE_11_HANDS_ON_LAB_LADDER_AUDIT.md
- STUDYBUBBLE_SESSION_STATE.md

## Why Runnable Files Are Under Tutorials
`study_maps` is the study product/doc space; `tutorials` is the runnable lab bench. This keeps architecture clean and avoids mixing narrative with executable practice artifacts.

## Study Manager Links Added
Course 11 manager now links to:
- tutorials lab bench index
- LAB_SEQUENCE.md
- all 10 lab README files

## Tutorials Index Updated
- Labeled as hands-on lab bench
- linked back to Course 11 study manager
- linked to LAB_SEQUENCE and each lab README

## Run Commands
Preferred per lab:
- `python lab_<short_name>.py`
Alternate:
- `spark-submit lab_<short_name>.py`

## Labs Run
- Attempted only Lab 01 per instruction.
- Command:
  - `python lab_sparksession_dataframe_basics.py`
- Result:
  - failed with `ModuleNotFoundError: No module named 'pyspark'`

## Known PySpark/Java Issues
- Java variables were present via env setup.
- Current blocker is missing `pyspark` module in active Python runtime.

## Guardrails
- No runnable files placed under study_maps (confirmed)
- Tutorials used for lab bench (confirmed)
- Study_bubbles engine untouched (confirmed)
- Generated outputs not edited (confirmed)

## 2026-05-21 Docker Finalization Pass
- Labs 01-10 marked PASS in Docker.
- Docker shell workflow documented in `tutorials/DataCamp/Associate_Data_Engineer_Databricks/course_11_intro_pyspark/HOW_TO_RUN_DOCKER_LABS.md`.
- `LAB_SEQUENCE.md` updated to Docker canonical flow and PASS status.
- All lab `README.md`, `troubleshooting.md`, and `expected_output.md` files updated for labs 01-10.
