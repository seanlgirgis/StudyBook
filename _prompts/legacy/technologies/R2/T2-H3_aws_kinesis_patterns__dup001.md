SAVE AS: aws_kinesis_patterns.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a Kinesis streaming notebook.

TASK: Kinesis Data Streams, Firehose, and analytics patterns — running live against AWS study account.

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
1. Title + Mental Model — "AWS Kinesis — Data Streams, Firehose, Analytics"
2. Setup — boto3 kinesis + firehose clients with study profile
3. Kinesis Data Streams — create stream "citi-telemetry-stream" (1 shard); put 50 records from alerts table; get records via shard iterator; print first 5; delete stream; explain shard capacity math (1MB/s write, 2MB/s read)
4. Kinesis Firehose — create a delivery stream to S3 (bucket=egirgis-lab or create temp); put 50 records; wait 60 seconds for delivery; list S3 objects to confirm delivery; explain buffering (1MB or 60s whichever first); delete stream
5. Shard Calculator — write a function kinesis_shard_count(events_per_sec, avg_bytes_per_event) that returns required shards; run for Citi scenario (6000 endpoints × 10 events = 60K events/sec × 500 bytes = 30MB/s → 30 shards)
6. Kinesis vs Kafka Decision Table — rows: ordering, replay, managed overhead, latency, multi-consumer, pricing, max throughput, when to use
7. What Just Happened — "Kinesis is the AWS-native Kafka. For pure AWS shops, Firehose → S3 → Athena is the zero-ops streaming pipeline. Citi uses Kinesis for CloudTrail event streaming into the security lake."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
