# StudyBook — Tutorial Roadmap
# Last updated: 2026-04-25
# 41 topics total | Priority: Toyota → Capital One → Fundamentals → Advanced

---

## STATUS KEY
# ✅ prompt.md written
# 🔨 .py files generated (via ChatGPT)
# ✔️  tested locally
# ⏳ in progress
# ⬜ not started

---

## BATCH 1 — Toyota Interview Prep (01-13)

| # | Topic | Slug | prompt.md | .py files | Tested |
|---|---|---|---|---|---|
| 01 | AWS Kinesis | aws_kinesis | ✅ | ⬜ | ⬜ |
| 02 | PySpark | pyspark | ✅ | ⬜ | ⬜ |
| 03 | Apache Airflow | apache_airflow | ✅ | ⬜ | ⬜ |
| 04 | AWS Step Functions | aws_step_functions | ✅ | ⬜ | ⬜ |
| 05 | Delta Lake | delta_lake | ✅ | ⬜ | ⬜ |
| 06 | AWS EMR | aws_emr | ✅ | ⬜ | ⬜ |
| 07 | AWS Glue | aws_glue | ✅ | ⬜ | ⬜ |
| 08 | AWS S3 | aws_s3 | ✅ | 🔨 | ⬜ |
| 09 | AWS CloudWatch | aws_cloudwatch | ✅ | ⬜ | ⬜ |
| 10 | Python Logging | python_logging | ✅ | ⬜ | ⬜ |
| 11 | dbt | dbt | ✅ | ⬜ | ⬜ |
| 12 | Parquet | parquet | ✅ | ⬜ | ⬜ |
| 13 | Python Concurrency | python_concurrency | ✅ | ⬜ | ⬜ |

---

## BATCH 2 — Capital One Interview Prep (14-23)

| # | Topic | Slug | prompt.md | .py files | Tested |
|---|---|---|---|---|---|
| 14 | Encryption | encryption | ⬜ | ⬜ | ⬜ |
| 15 | Data Anonymization / PII | data_anonymization_pii | ⬜ | ⬜ | ⬜ |
| 16 | AWS IAM | aws_iam | ⬜ | ⬜ | ⬜ |
| 17 | PostgreSQL | postgresql | ⬜ | ⬜ | ⬜ |
| 18 | SQL Patterns | sql_patterns | ⬜ | ⬜ | ⬜ |
| 19 | Python Testing | python_testing | ⬜ | ⬜ | ⬜ |
| 20 | Pydantic | pydantic | ⬜ | ⬜ | ⬜ |
| 21 | AWS Redshift | aws_redshift | ⬜ | ⬜ | ⬜ |
| 22 | AWS Athena | aws_athena | ⬜ | ⬜ | ⬜ |
| 23 | SQLAlchemy | sqlalchemy | ⬜ | ⬜ | ⬜ |

---

## BATCH 3 — Data Engineering Fundamentals (24-30)

| # | Topic | Slug | prompt.md | .py files | Tested |
|---|---|---|---|---|---|
| 24 | Pandas | pandas | ⬜ | ⬜ | ⬜ |
| 25 | NumPy | numpy | ⬜ | ⬜ | ⬜ |
| 26 | Polars | polars | ⬜ | ⬜ | ⬜ |
| 27 | DuckDB | duckdb | ⬜ | ⬜ | ⬜ |
| 28 | Data Stubbing | data_stubbing | ⬜ | ⬜ | ⬜ |
| 29 | Streamlit | streamlit | ⬜ | ⬜ | ⬜ |
| 30 | FastAPI | fastapi | ⬜ | ⬜ | ⬜ |

---

## BATCH 4 — Advanced / Cloud (31-41)

| # | Topic | Slug | prompt.md | .py files | Tested |
|---|---|---|---|---|---|
| 31 | AWS Lambda | aws_lambda | ⬜ | ⬜ | ⬜ |
| 32 | AWS DynamoDB | aws_dynamodb | ⬜ | ⬜ | ⬜ |
| 33 | AWS MSK / Kafka | aws_msk_kafka | ⬜ | ⬜ | ⬜ |
| 34 | AWS Bedrock | aws_bedrock | ⬜ | ⬜ | ⬜ |
| 35 | Terraform | terraform | ⬜ | ⬜ | ⬜ |
| 36 | Docker | docker | ⬜ | ⬜ | ⬜ |
| 37 | CI/CD | cicd | ⬜ | ⬜ | ⬜ |
| 38 | AWS ECS | aws_ecs | ⬜ | ⬜ | ⬜ |
| 39 | AWS CloudFormation | aws_cloudformation | ⬜ | ⬜ | ⬜ |
| 40 | OpenSearch | opensearch | ⬜ | ⬜ | ⬜ |
| 41 | Snowflake / PyIceberg | snowflake_pyiceberg | ⬜ | ⬜ | ⬜ |

---

## MILESTONES

| Milestone | Description | Status |
|---|---|---|
| M1 | All Toyota prompt.md files written (01-13) | ✅ DONE |
| M2 | All Capital One prompt.md files written (14-23) | ⬜ |
| M3 | All Fundamentals + Advanced prompt.md files (24-41) | ⬜ |
| M4 | Toyota .py files generated via ChatGPT (01-13) | ⬜ |
| M5 | Toyota code tested against AWS + Docker | ⬜ |
| M6 | Capital One .py files generated + tested | ⬜ |
| M7 | All 41 topics complete | ⬜ |
| M8 | Tutorial index page on website | ⬜ |

---

## APPROACH — Generating .py Files

1. Open ChatGPT (web) — use Project 3 (Tutorials) once created, or a fresh chat
2. Paste full content of `tutorials/NN_topic/prompt.md`
3. ChatGPT acknowledges — you say "generate file 01"
4. Save output as `tutorials/NN_topic/setup/01_filename.py`
5. Continue: "generate file 02", "generate file 03", etc.
6. Say "generate capstone" — save brief.md, capstone.py, test_capstone.py
7. Run locally: `python 01_filename.py` — fix any issues before moving on
8. Mark .py files column ✅ in this roadmap

---

## APPROACH — Testing Tutorial Code

### AWS topics (Kinesis, S3, Glue, EMR, Step Functions, etc.)
- Real AWS account required — use personal AWS account
- Set env vars: AWS_PROFILE, AWS_REGION
- All tutorials include cleanup() — always run it after testing

### Docker topics (Airflow, PySpark, dbt, PostgreSQL, SQLAlchemy, etc.)
- Use existing studybook_core stack (see DOCKER_INVENTORY.md)
- `docker compose up -d` from compose root before running

### Pure Python topics (Delta Lake, Parquet, Pandas, Polars, etc.)
- No infra needed
- pip install dependencies per file header
- Run directly: `python setup/01_filename.py`
