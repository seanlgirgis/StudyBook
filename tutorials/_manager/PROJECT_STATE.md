# Tutorials Project State
Last updated: 2026-04-26
Scope: `D:\Workarea\StudyBook\tutorials`

## Current Reality Snapshot

- Existing tutorial topic folders: `20`
- Tested/working topics: `9` (all marked as user-reported working in this sync)
- READY_TO_PASTE only topics: `11`
- Not-started planned topics (missing folders): `28`
- Intentional variant track: `02_PySpark_Docker` (not an accidental duplicate)

## User-Reported Working Topics

- `01_aws_kinesis`
- `02_pyspark` (canonical local `local[*]`)
- `02_PySpark_Docker` (Docker/Spark-cluster variant)
- `08_aws_s3`
- `09_aws_cloudwatch`
- `10_python_logging`
- `12_parquet`
- `13_python_concurrency`
- `14_encryption`

## READY_TO_PASTE Only (Code Not Generated Yet)

- `03_apache_airflow`
- `04_aws_step_functions`
- `05_delta_lake`
- `06_aws_emr`
- `07_aws_glue`
- `11_dbt`
- `24_pandas`
- `26_polars`
- `27_duckdb`
- `33_aws_msk_kafka`
- `36_docker`

## Not Started (Missing Topic Folders)

- `15_data_anonymization_pii`
- `16_aws_iam`
- `17_postgresql`
- `18_sql_patterns`
- `19_python_testing`
- `20_pydantic`
- `21_aws_redshift`
- `22_aws_athena`
- `23_sqlalchemy`
- `25_numpy`
- `28_data_stubbing`
- `29_streamlit`
- `30_fastapi`
- `31_aws_lambda`
- `32_aws_dynamodb`
- `34_aws_bedrock`
- `35_terraform`
- `37_cicd`
- `38_aws_ecs`
- `39_aws_cloudformation`
- `40_opensearch`
- `41_snowflake_pyiceberg`
- `42_aws_lambda_de`
- `43_terraform_de`
- `44_pyiceberg`
- `45_great_expectations`
- `46_cicd_data`
- `47_redis_de`

## File-Pattern Gaps To Keep In Mind

- `08_aws_s3` has code/tests but no `prompt_READY_TO_PASTE.md`.
- `14_encryption` has code/tests and READY_TO_PASTE but no `prompt.md`.
- `24/26/27/33/36` have `prompt_READY_TO_PASTE.md` only (no `prompt.md` yet).

## Immediate Priority Order

1. Generate `.py` files from READY_TO_PASTE topics (`03,04,05,06,07,11,24,26,27,33,36`).
2. Add missing folders/prompts for not-started topics.
3. Capture independent test evidence for user-reported-working tutorials.
