# Docker Inventory - Tutorials
Last updated: 2026-04-26

## Intent

Use existing containers; do not create duplicate stacks unless explicitly needed.

## Core Endpoints Used By Tutorials

- Kafka bootstrap: `localhost:29092`
- Airflow web: `http://localhost:8082`
- Spark master: `spark://localhost:7077`
- Postgres: `postgresql://studybook:studybook@localhost:5432/studybook`
- Elasticsearch: `http://localhost:9200`

## Tutorial-to-Infra Mapping (Current)

| Tutorial folder | Infra mode | Notes |
|---|---|---|
| `01_aws_kinesis` | AWS account | real AWS resources |
| `02_pyspark` | local PySpark (`local[*]`) | canonical topic-02 track |
| `02_PySpark_Docker` | Docker Spark cluster | intentional variant (master/worker) |
| `03_apache_airflow` | Airflow + Postgres (Docker) | READY_TO_PASTE only currently |
| `04_aws_step_functions` | AWS account | READY_TO_PASTE only currently |
| `05_delta_lake` | local filesystem | READY_TO_PASTE only currently |
| `06_aws_emr` | AWS account | READY_TO_PASTE only currently |
| `07_aws_glue` | AWS account | READY_TO_PASTE only currently |
| `08_aws_s3` | AWS account | user-reported working |
| `09_aws_cloudwatch` | AWS account | user-reported working |
| `10_python_logging` | local Python | user-reported working |
| `11_dbt` | Postgres (Docker) | READY_TO_PASTE only currently |
| `12_parquet` | local Python | user-reported working |
| `13_python_concurrency` | local Python | user-reported working |
| `14_encryption` | local Python | user-reported working |
| `24_pandas` | local Python | READY_TO_PASTE only currently |
| `26_polars` | local Python | READY_TO_PASTE only currently |
| `27_duckdb` | local Python | READY_TO_PASTE only currently |
| `33_aws_msk_kafka` | Kafka Docker (local dev) or AWS MSK | READY_TO_PASTE only currently |
| `36_docker` | Docker daemon | READY_TO_PASTE only currently |

## Quick Docker Commands

```powershell
docker compose up -d
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
docker compose stop
docker compose down
```

## Guardrails

- Keep `02_pyspark` and `02_PySpark_Docker` as separate tracks.
- Prefer existing mapped ports (`29092`, `8082`, `7077`) in prompts and generated code.
