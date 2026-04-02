SAVE AS: spark_structured_streaming.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a Spark Structured Streaming notebook.

TASK: Micro-batch streaming from Kafka topic, watermarking, stateful aggregations, checkpointing — live against local Kafka stack.

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
1. Title + Mental Model — "Spark Structured Streaming — Micro-batch, Watermarking, State"
2. Imports + SparkSession + Kafka jar config (spark.jars.packages = org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4)
3. Produce stream — first cell produces 100 alerts to "citi.stream.spark" Kafka topic using confluent-kafka
4. Read from Kafka — create streaming DataFrame from Kafka source, parse JSON payload, show schema
5. Stateful Count with Watermark — groupBy severity + 1-minute window, watermark 30 seconds late, writeStream to memory sink "alert_counts"; after 10 seconds, spark.sql("SELECT * FROM alert_counts").show()
6. Exactly-once with Checkpointing — explain checkpointLocation, how Spark recovers from failure; show config
7. Output Modes — explain append vs complete vs update with code examples for each
8. What Just Happened — compare with Kafka Streams and Flink; Citi tie-in: "Spark Structured Streaming on Kafka is Citi's go-to for batch-to-streaming migration — same DataFrame API, same team, different trigger"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
