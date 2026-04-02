# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-I1_gcp_dataflow_pubsub.md

SAVE AS: gcp_dataflow_pubsub.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a GCP streaming and batch notebook.

TASK: Pub/Sub messaging, Dataflow templates, and Dataproc — running live against GCP project citi-de-learning.

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
1. Title + Mental Model — "GCP Streaming and Batch — Pub/Sub, Dataflow, Dataproc"
2. Setup — GOOGLE_APPLICATION_CREDENTIALS set; google-cloud-pubsub, google-cloud-dataflow imports; PROJECT_ID="citi-de-learning"; no pip install
3. Pub/Sub Advanced — create topic "citi-telemetry-stream"; create 2 subscriptions (alerting-sub, analytics-sub) showing fan-out pattern; publish 50 alerts with attributes (severity, region); pull from both subscriptions; show each received all 50; delete topic + subs
4. Dataflow Template (conceptual + API call) — explain Dataflow's Apache Beam model (PCollections, PTransforms, runners); show how to launch a Dataflow template job via REST API (use the GCS-to-BigQuery text template); explain when to use Dataflow vs Spark
5. Dataproc — explain Dataproc as managed Spark/Hadoop; create a cluster via gcloud API call (show the REST payload); explain preemptible nodes, autoscaling, component gateway; do NOT actually create (cost) — show the API call and explain
6. GCP vs AWS Streaming Comparison — Pub/Sub vs Kinesis; Dataflow vs EMR/Glue; BigQuery vs Athena; table format
7. What Just Happened — "Pub/Sub fan-out is GCP's answer to multiple consumer groups in Kafka. Dataflow is the operational Apache Beam runner. For Citi's GCP workloads, Pub/Sub → Dataflow → BigQuery is the canonical streaming pipeline."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


