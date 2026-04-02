# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-A3_kafka_vs_kinesis.md

SAVE AS: kafka_vs_kinesis.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a comparison notebook.

TASK: Produce a side-by-side architectural comparison of Kafka and Kinesis, with live code examples where possible (Kafka against local stack, Kinesis via boto3 against AWS study account).

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics table: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

TECH STACK CONTEXT — do not deviate:
- Kafka: localhost:9092, confluentinc/cp-kafka:7.6.0, container citi_kafka
- Spark: pyspark==3.5.4, master=local[*], JAVA_HOME=C:/Program Files/Java/jre1.8.0_481, HADOOP_HOME=C:/hadoop
- Airflow: localhost:8082, apache/airflow:2.8.0, LocalExecutor, credentials admin/admin
- MLflow: localhost:5000, SQLite backend
- dbt: C:/py_venv/proj_educate/Scripts/dbt.exe, profiles.yml at ~/.dbt/profiles.yml, project citi_dbt, target postgres
- Databricks: host=https://dbc-9f35a83d-b4e7.cloud.databricks.com, Serverless SQL Warehouse b6657f31d1e7a179
- GCP: project=citi-de-learning, key=D:/Workspace/Technologies/_setup/gcp_key.json
- Azure: subscription=b3811436-61fc-4a3a-a6a9-deb05955076d, az CLI at C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin\az.cmd
- AWS: profile=study, region=us-east-1, account=357811130281

SECTIONS:
1. Title + Mental Model — "Kafka vs Kinesis — When Each Wins"
2. Imports + config (boto3 with AWS_PROFILE=study, confluent-kafka, no pip install)
3. Kafka: produce 50 alerts to "citi.comparison" topic, measure latency (time.perf_counter before/after flush); print "Kafka P99 produce latency: Xms"
4. Kinesis: create stream "citi-comparison" (shard_count=1), put 50 records using boto3, measure latency; print "Kinesis P99 put latency: Xms"; delete stream after
5. Decision Matrix table — rows: managed overhead, ordering guarantee, replay window, consumer model, pricing model, max throughput, multi-cloud, Citi recommendation; Kafka vs Kinesis filled in for each
6. Migration Pattern — code showing how to write a dual-write shim (write to both Kafka and Kinesis with same payload) for migration scenarios; explain strangler fig pattern
7. What Just Happened — "Use Kafka when you control infrastructure and need sub-ms latency or cross-cloud portability. Use Kinesis when you are AWS-native and want zero-ops streaming. Citi uses Kafka on-prem; AWS workloads use Kinesis for event ingestion into Firehose → S3."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


