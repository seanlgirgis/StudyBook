SAVE AS: batch_pipeline_end2end.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a capstone end-to-end batch pipeline notebook.

TASK: Build a complete batch pipeline: Airflow DAG → Spark batch job → dbt transform → Postgres serving table → query verification. Every stage runs live against the local stack.

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
1. Title + Pipeline Diagram — "Batch Pipeline — Airflow → Spark → dbt → Postgres"; ASCII diagram showing all stages; explain nightly batch pattern vs streaming
2. Imports + config (pyspark, psycopg2, subprocess for dbt, requests for Airflow REST API, real credentials, no pip install)
3. Stage 1 — Spark Batch Extract: load all 500K metrics from Postgres via JDBC into Spark DataFrame; compute daily alert counts + P50/P95 latency per endpoint; write to Postgres table "batch_daily_summary" (overwrite); print "Stage 1 complete — X endpoints summarized"
4. Stage 2 — dbt Transform: first write the dbt model file to disk using Python open() — path C:/py_venv/proj_educate/dbt/citi_dbt/models/marts/mart_batch_daily_summary.sql — content: SELECT b.endpoint_id, e.name, e.region, e.category, b.alert_count, b.p95_latency FROM batch_daily_summary b JOIN endpoints e ON e.endpoint_id = b.endpoint_id; then run subprocess([r"C:/py_venv/proj_educate/Scripts/dbt.exe", "run", "--select", "mart_batch_daily_summary", "--project-dir", r"C:/py_venv/proj_educate/dbt/citi_dbt", "--profiles-dir", r"C:/Users/{USER}/.dbt"]); capture stdout; print "Stage 2 complete — mart_batch_daily_summary built"
5. Stage 3 — dbt Test: subprocess([r"C:/py_venv/proj_educate/Scripts/dbt.exe", "test", "--select", "mart_batch_daily_summary", "--project-dir", r"C:/py_venv/proj_educate/dbt/citi_dbt", "--profiles-dir", r"C:/Users/{USER}/.dbt"]); capture return code; print "Stage 3 complete — dbt tests passed" if rc==0 else print warning and continue (do not raise)
6. Stage 4 — Airflow Trigger: use the Airflow REST API (requests, NOT subprocess — Airflow runs in Docker and the CLI is not available locally); POST http://localhost:8082/api/v1/dags/batch_pipeline_nightly/dagRuns with auth admin/admin; if 404 (DAG not yet deployed), print "Stage 4 skipped — DAG not yet deployed (expected on first run)" and continue; otherwise poll GET /dagRuns/{run_id} until state in {success, failed}; print final state and run_id
7. Stage 5 — Serving Verification: psycopg2 query: top 10 endpoints by alert count with region; print results; assert row count > 0; print "Pipeline verified — serving layer ready"
8. What Just Happened — explain idempotency, backfill, SLA design; Citi framing: "This nightly batch job produces the endpoint health scorecard that risk teams use the next morning — idempotency is non-negotiable at Citi"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

