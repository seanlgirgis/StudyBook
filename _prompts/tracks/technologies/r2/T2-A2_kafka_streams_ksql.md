# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-A2_kafka_streams_ksql.md

SAVE AS: kafka_streams_ksql.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a stream processing notebook using Kafka and Python.

TASK: Demonstrate stateful stream processing concepts using confluent-kafka in Python (not Java Kafka Streams — use Python consumer with manual state). No KSQL server needed — implement windowed aggregation manually.

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
1. Title + Mental Model — "Stream Processing on Kafka — Windowed Aggregation, Stateful Consumers"
2. Imports + config (no pip install)
3. Produce telemetry stream — produce 200 alert events from alerts table, include timestamp in message payload, use severity as key; print "Produced 200 events to citi.stream.alerts"
4. Tumbling Window Aggregation — consumer that reads all messages, buckets by 60-second tumbling window using created_at timestamp from payload, counts per severity per window; print table of windows × severity × count
5. Stateful Count by Region — second consumer pass, join endpoint data (loaded from Postgres) to get region from endpoint_id, count alerts per region; print sorted table
6. Sliding Window Alert Rate — detect if any endpoint fires more than 3 alerts within a 5-minute window; print "HOT ENDPOINTS: {list of endpoint_ids}" or "No hot endpoints detected"
7. What Just Happened — explain micro-batch vs true streaming, watermarking concept, why Spark Structured Streaming or Flink is better for production stateful ops; Citi tie-in: "This pattern detects endpoint storm events before they cascade"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


