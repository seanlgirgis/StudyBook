SAVE AS: streaming_pipeline_end2end.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a capstone end-to-end streaming pipeline notebook.

TASK: Build a complete streaming pipeline: Kafka → Spark Structured Streaming → Postgres (Delta-like staging table) → dbt transform → verify via Airflow trigger. Every stage runs live against the local stack.

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
1. Title + Pipeline Diagram — "Streaming Pipeline — Kafka → Spark → Postgres → dbt → Airflow"; ASCII diagram showing all 5 stages with data volumes at each stage
2. Imports + config (confluent-kafka, pyspark, psycopg2, subprocess for dbt, requests for Airflow REST API, real credentials, no pip install)
3. Stage 1 — Kafka Ingest: create topic "citi.stream.e2e", produce 200 alerts (JSON: alert_id, endpoint_id, severity, message, created_at) from the alerts table; print "Stage 1 complete — 200 events published to citi.stream.e2e"
4. Stage 2 — Spark Streaming: read from "citi.stream.e2e" micro-batch, parse JSON, write to Postgres table "stream_staging" (append mode, foreachBatch sink); run for 15 seconds then stop; print "Stage 2 complete — X rows written to stream_staging"
5. Stage 3 — dbt Transform: first write the dbt model file to disk using Python open() — path C:/py_venv/proj_educate/dbt/citi_dbt/models/staging/stg_stream_alerts.sql — content: SELECT alert_id, endpoint_id, severity, message, created_at FROM stream_staging WHERE severity IS NOT NULL; then run subprocess([r"C:/py_venv/proj_educate/Scripts/dbt.exe", "run", "--select", "stg_stream_alerts", "--project-dir", r"C:/py_venv/proj_educate/dbt/citi_dbt", "--profiles-dir", r"C:/Users/{USER}/.dbt"]); capture stdout; print "Stage 3 complete — stg_stream_alerts materialized"
6. Stage 4 — Airflow Verify: use the Airflow REST API (requests, NOT subprocess — Airflow runs in Docker and the CLI is not available locally); POST http://localhost:8082/api/v1/dags/stream_pipeline_verify/dagRuns with auth admin/admin; if 404 (DAG doesn't exist yet), print "Stage 4 skipped — DAG not yet deployed (expected on first run)" and continue; otherwise poll GET /dagRuns/{run_id} until state in {success, failed}; print final state
7. Stage 5 — End-to-End Verify: psycopg2 query counting rows in stg_stream_alerts; assert count > 0; print "Pipeline verified end-to-end — X alerts flowed from Kafka to serving layer"
8. What Just Happened — latency breakdown per stage, SLA implications, Citi framing: "This is the 60,000 events/sec pattern at scale — every alert that fires at Citi flows a path like this before an engineer sees it"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
