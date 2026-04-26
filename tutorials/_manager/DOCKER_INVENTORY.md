# Docker Inventory — StudyBook
# Last updated: 2026-04-25
# Source: studybook_core compose stack + setup containers
# Purpose: Know which containers to use in tutorials. DO NOT spin up duplicates.

---

## Running Stack: studybook_core

Start command: `docker compose up -d` (from compose root)
Stop command: `docker compose down`

### Core Services

| Container | Image | Port (host) | Internal Port | Purpose |
|---|---|---|---|---|
| postgres | postgres:16-alpine | 5432 | 5432 | Primary SQL database |
| kafka | confluentinc/cp-kafka:7.6.0 | 29092 | 9092 | Kafka broker |
| zookeeper | confluentinc/cp-zookeeper:7.6.0 | 2181 | 2181 | Kafka coordination |
| kafka-ui | provectuslabs/kafka-ui | 8080 | 8080 | Kafka browser UI |
| airflow | apache/airflow:2.8.1 | 8082 | 8080 | Workflow orchestration |
| spark-master | bitnami/spark:3.5 | 7077, 8081 | 7077, 8080 | Spark master node |
| spark-worker | bitnami/spark:3.5 | — | — | Spark worker |
| elasticsearch | elasticsearch:8.12.0 | 9200 | 9200 | Full-text search / analytics |
| kibana | kibana:8.12.0 | 5601 | 5601 | Elasticsearch UI |
| redis | redis:7-alpine | 6380 | 6379 | Cache / queue |
| cassandra | cassandra:4.1 | 9042 | 9042 | Wide-column NoSQL |
| neo4j | neo4j:5.17 | 7474, 7687 | 7474, 7687 | Graph database |
| influxdb | influxdb:2.7 | 8086 | 8086 | Time-series database |
| mlflow | ghcr.io/mlflow/mlflow | 5000 | 5000 | ML experiment tracking |
| splunk | splunk/splunk | 8000 | 8000 | Log aggregation / SIEM |

### Setup / Utility Containers (may be stop-and-remove after use)

| Container | Purpose |
|---|---|
| kafka-init | Creates topics at startup (runs once, exits) |
| airflow-init | DB migration + admin user setup (runs once, exits) |
| postgres-init | Schema + seed data (runs once, exits) |

---

## Connection Strings

```python
# PostgreSQL
POSTGRES_URI = "postgresql://studybook:studybook@localhost:5432/studybook"
# psycopg2: psycopg2.connect(host="localhost", port=5432, dbname="studybook", user="studybook", password="studybook")

# Kafka
KAFKA_BOOTSTRAP = "localhost:29092"
# kafka-python: KafkaProducer(bootstrap_servers=["localhost:29092"])
# confluent-kafka: Producer({"bootstrap.servers": "localhost:29092"})

# Redis
REDIS_URI = "redis://localhost:6380/0"
# redis-py: redis.Redis(host="localhost", port=6380, db=0)

# Elasticsearch
ES_HOST = "http://localhost:9200"
# elasticsearch-py: Elasticsearch("http://localhost:9200")

# Cassandra
CASSANDRA_HOST = "localhost"  # port 9042
# cassandra-driver: Cluster(["localhost"]).connect()

# Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "studybook")

# InfluxDB
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "studybook-token"  # check docker-compose env

# Spark (submit via master)
SPARK_MASTER = "spark://localhost:7077"
# SparkSession.builder.master("spark://localhost:7077").getOrCreate()
# OR local mode: .master("local[*]")

# Airflow (web UI)
AIRFLOW_URL = "http://localhost:8082"
AIRFLOW_USER = "admin"  # set during airflow-init

# MLflow
MLFLOW_URI = "http://localhost:5000"

# Splunk web
SPLUNK_URL = "http://localhost:8000"
```

---

## Which Tutorial Uses Which Container

| Tutorial | Container(s) Used |
|---|---|
| 01_aws_kinesis | AWS (real) — no local substitute |
| 02_pyspark | spark-master (local[*] acceptable too) |
| 03_apache_airflow | airflow (localhost:8082), postgres |
| 04_aws_step_functions | AWS (real) |
| 05_delta_lake | Pure Python / local filesystem |
| 06_aws_emr | AWS (real) — EMR Serverless |
| 07_aws_glue | AWS (real) |
| 08_aws_s3 | AWS (real) |
| 09_aws_cloudwatch | AWS (real) |
| 10_python_logging | No container — pure Python |
| 11_dbt | postgres (localhost:5432) |
| 12_parquet | Pure Python / local filesystem |
| 13_python_concurrency | No container — pure Python |
| 14_encryption | No container — pure Python |
| 15_data_anonymization_pii | postgres (localhost:5432) |
| 16_aws_iam | AWS (real) |
| 17_postgresql | postgres (localhost:5432) |
| 18_sql_patterns | postgres (localhost:5432) |
| 19_python_testing | No container — pure Python |
| 20_pydantic | No container — pure Python |
| 21_aws_redshift | AWS (real) |
| 22_aws_athena | AWS (real) |
| 23_sqlalchemy | postgres (localhost:5432) |
| 24_pandas | No container — pure Python |
| 25_numpy | No container — pure Python |
| 26_polars | No container — pure Python |
| 27_duckdb | No container — pure Python |
| 28_data_stubbing | No container — pure Python |
| 29_streamlit | No container — pure Python |
| 30_fastapi | No container — pure Python |
| 31_aws_lambda | AWS (real) |
| 32_aws_dynamodb | AWS (real) |
| 33_aws_msk_kafka | kafka (localhost:29092) for local dev |
| 34_aws_bedrock | AWS (real) |
| 35_terraform | AWS (real) |
| 36_docker | Docker daemon (local) |
| 37_cicd | No container — GitHub Actions concepts |
| 38_aws_ecs | AWS (real) |
| 39_aws_cloudformation | AWS (real) |
| 40_opensearch | elasticsearch (localhost:9200) as substitute |
| 41_snowflake_pyiceberg | Snowflake account required |

---

## Docker Quick Commands

```powershell
# Start everything
docker compose up -d

# Check what's running
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Stop without removing volumes
docker compose stop

# Full teardown (keeps volumes)
docker compose down

# Full teardown + wipe volumes (destructive!)
docker compose down -v

# View logs for one container
docker logs kafka --tail 50 -f

# Connect to postgres
docker exec -it postgres psql -U studybook -d studybook
```

---

## Notes for Tutorial Prompt Authors

- **Never tell ChatGPT to spin up new Docker containers** for topics already covered above.
- For Airflow tutorials: use `localhost:8082`, not the default 8080 (our host port is remapped).
- For Kafka tutorials: bootstrap server is `localhost:29092` (external listener), NOT 9092.
- For Spark tutorials: prefer `local[*]` master for simplicity unless testing cluster submission.
- Postgres password: `studybook` (matches POSTGRES_PASSWORD in compose).
- All tutorials should check env vars first, fall back to these defaults.
