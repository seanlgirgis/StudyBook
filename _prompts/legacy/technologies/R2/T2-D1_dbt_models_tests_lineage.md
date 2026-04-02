SAVE AS: dbt_models_tests_lineage.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a deep dbt notebook.

TASK: Materialization strategies, incremental models, snapshots, and data tests — running live against the Citi dbt project (citi_dbt).

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
1. Title + Mental Model — "dbt Deep — Materializations, Incremental, Snapshots, Tests"
2. Imports + dbt path setup (DBT_PATH = "C:/py_venv/proj_educate/Scripts/dbt.exe", subprocess with UTF-8 encoding)
3. Materialization Comparison — create 4 model files in citi_dbt/models/: table_model.sql, view_model.sql, ephemeral_model.sql, incremental_model.sql; each selects from public.alerts with different materialized config; run dbt run; show execution times from run results JSON
4. Incremental Model Deep Dive — incremental_model.sql uses is_incremental() macro to only process new alerts by created_at; run twice (first full, second incremental); print "First run: X rows, Second run: Y rows (incremental)"
5. Snapshot — create a snapshot on public.endpoints to track status changes (strategy=check, check_cols=[status]); run dbt snapshot; update one endpoint status in Postgres; run snapshot again; show dbt_scd_* columns
6. Tests — add schema.yml with not_null, unique, accepted_values (severity in HIGH/CRITICAL/MEDIUM/LOW), relationships tests; run dbt test; parse test results JSON; print pass/fail per test
7. Lineage — run dbt ls --select alerts+; show DAG structure; explain how dbt lineage works
8. What Just Happened — "Incremental models are the most important dbt concept for production. They turn a full-refresh job into a delta-only job. Citi's dbt models on 25K alerts incrementally process only new rows since last run."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

