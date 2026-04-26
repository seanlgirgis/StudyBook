# StudyBook Tutorials - Roadmap Status Matrix
Last updated: 2026-04-26
Source: direct repo scan + user-provided run status

## Legend

- `yes/no` in artifact columns reflects current files in repo.
- `Status` values: `tested_working`, `ready_to_paste_only`, `not_started`.
- Verification values: `user_reported_working`, `repo_evidence_only`, `not_available`.

## Core Topics (01-47)

| # | Topic | Folder | Folder exists | prompt.md | prompt_READY_TO_PASTE.md | setup/tutorial .py exists | capstone files exist | tests exist | Status | Verification |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | AWS Kinesis | `01_aws_kinesis` | yes | yes | yes | yes | yes | yes | tested_working | user_reported_working |
| 02 | PySpark (canonical local[*]) | `02_pyspark` | yes | yes | yes | yes | no | no | tested_working | user_reported_working |
| 03 | Apache Airflow | `03_apache_airflow` | yes | yes | yes | no | no | no | ready_to_paste_only | repo_evidence_only |
| 04 | AWS Step Functions | `04_aws_step_functions` | yes | yes | yes | no | no | no | ready_to_paste_only | repo_evidence_only |
| 05 | Delta Lake | `05_delta_lake` | yes | yes | yes | no | no | no | ready_to_paste_only | repo_evidence_only |
| 06 | AWS EMR | `06_aws_emr` | yes | yes | yes | no | no | no | ready_to_paste_only | repo_evidence_only |
| 07 | AWS Glue | `07_aws_glue` | yes | yes | yes | no | no | no | ready_to_paste_only | repo_evidence_only |
| 08 | AWS S3 | `08_aws_s3` | yes | yes | no | yes | yes | yes | tested_working | user_reported_working |
| 09 | AWS CloudWatch | `09_aws_cloudwatch` | yes | yes | yes | yes | yes | yes | tested_working | user_reported_working |
| 10 | Python Logging | `10_python_logging` | yes | yes | yes | yes | yes | yes | tested_working | user_reported_working |
| 11 | dbt | `11_dbt` | yes | yes | yes | no | no | no | ready_to_paste_only | repo_evidence_only |
| 12 | Parquet | `12_parquet` | yes | yes | yes | yes | yes | yes | tested_working | user_reported_working |
| 13 | Python Concurrency | `13_python_concurrency` | yes | yes | yes | yes | yes | yes | tested_working | user_reported_working |
| 14 | Encryption | `14_encryption` | yes | no | yes | yes | yes | yes | tested_working | user_reported_working |
| 15 | Data Anonymization / PII | `15_data_anonymization_pii` | no | no | no | no | no | no | not_started | not_available |
| 16 | AWS IAM | `16_aws_iam` | no | no | no | no | no | no | not_started | not_available |
| 17 | PostgreSQL | `17_postgresql` | no | no | no | no | no | no | not_started | not_available |
| 18 | SQL Patterns | `18_sql_patterns` | no | no | no | no | no | no | not_started | not_available |
| 19 | Python Testing | `19_python_testing` | no | no | no | no | no | no | not_started | not_available |
| 20 | Pydantic | `20_pydantic` | no | no | no | no | no | no | not_started | not_available |
| 21 | AWS Redshift | `21_aws_redshift` | no | no | no | no | no | no | not_started | not_available |
| 22 | AWS Athena | `22_aws_athena` | no | no | no | no | no | no | not_started | not_available |
| 23 | SQLAlchemy | `23_sqlalchemy` | no | no | no | no | no | no | not_started | not_available |
| 24 | Pandas | `24_pandas` | yes | no | yes | no | no | no | ready_to_paste_only | repo_evidence_only |
| 25 | NumPy | `25_numpy` | no | no | no | no | no | no | not_started | not_available |
| 26 | Polars | `26_polars` | yes | no | yes | no | no | no | ready_to_paste_only | repo_evidence_only |
| 27 | DuckDB | `27_duckdb` | yes | no | yes | no | no | no | ready_to_paste_only | repo_evidence_only |
| 28 | Data Stubbing | `28_data_stubbing` | no | no | no | no | no | no | not_started | not_available |
| 29 | Streamlit | `29_streamlit` | no | no | no | no | no | no | not_started | not_available |
| 30 | FastAPI | `30_fastapi` | no | no | no | no | no | no | not_started | not_available |
| 31 | AWS Lambda | `31_aws_lambda` | no | no | no | no | no | no | not_started | not_available |
| 32 | AWS DynamoDB | `32_aws_dynamodb` | no | no | no | no | no | no | not_started | not_available |
| 33 | AWS MSK / Kafka | `33_aws_msk_kafka` | yes | no | yes | no | no | no | ready_to_paste_only | repo_evidence_only |
| 34 | AWS Bedrock | `34_aws_bedrock` | no | no | no | no | no | no | not_started | not_available |
| 35 | Terraform | `35_terraform` | no | no | no | no | no | no | not_started | not_available |
| 36 | Docker | `36_docker` | yes | no | yes | no | no | no | ready_to_paste_only | repo_evidence_only |
| 37 | CI/CD | `37_cicd` | no | no | no | no | no | no | not_started | not_available |
| 38 | AWS ECS | `38_aws_ecs` | no | no | no | no | no | no | not_started | not_available |
| 39 | AWS CloudFormation | `39_aws_cloudformation` | no | no | no | no | no | no | not_started | not_available |
| 40 | OpenSearch | `40_opensearch` | no | no | no | no | no | no | not_started | not_available |
| 41 | Snowflake / PyIceberg | `41_snowflake_pyiceberg` | no | no | no | no | no | no | not_started | not_available |
| 42 | AWS Lambda (DE patterns) | `42_aws_lambda_de` | no | no | no | no | no | no | not_started | not_available |
| 43 | Terraform for DE | `43_terraform_de` | no | no | no | no | no | no | not_started | not_available |
| 44 | Apache Iceberg (PyIceberg) | `44_pyiceberg` | no | no | no | no | no | no | not_started | not_available |
| 45 | Great Expectations | `45_great_expectations` | no | no | no | no | no | no | not_started | not_available |
| 46 | CI/CD for Data Pipelines | `46_cicd_data` | no | no | no | no | no | no | not_started | not_available |
| 47 | Redis for Data Engineers | `47_redis_de` | no | no | no | no | no | no | not_started | not_available |

## Additional Variant Track (Intentional)

| Topic | Folder | Role | prompt.md | prompt_READY_TO_PASTE.md | code | tests | Status | Verification |
|---|---|---|---|---|---|---|---|---|
| PySpark Docker variant | `02_PySpark_Docker` | Docker/Spark-cluster variant of topic 02; keep alongside canonical local track | no | no | yes | no | tested_working | user_reported_working |

## Current Totals

- `tested_working`: 9 folders (all user-reported working in this sync)
- `ready_to_paste_only`: 11 folders
- `not_started`: 28 topics (folders missing)
