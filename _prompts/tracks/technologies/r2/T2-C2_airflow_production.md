# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-C2_airflow_production.md

SAVE AS: airflow_production.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing an Airflow production patterns notebook.

TASK: Executor types, SLAs, alerting, monitoring, and production readiness concepts — demonstrated against local Airflow.

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
1. Title + Mental Model — "Airflow Production — Executors, SLAs, Alerting, Monitoring"
2. Imports + REST API setup
3. Executor Comparison — markdown explaining LocalExecutor vs CeleryExecutor vs KubernetesExecutor; show current executor via GET /api/v1/config; table: executor type × use case × when to upgrade
4. SLA Configuration — write a DAG with sla=timedelta(minutes=1) on a task; trigger it; poll; show SLA miss concept; explain sla_miss_callback
5. DAG Health Monitoring — GET /api/v1/dags, /api/v1/dag-runs, show counts of running/failed/success; write function check_dag_health() that returns red/yellow/green per DAG
6. Connection Management — GET /api/v1/connections; show how Airflow stores connection strings; explain why credentials should not be in DAG code; demonstrate using a Variable vs a Connection
7. Production Checklist — markdown cell with 10-item production readiness checklist: executor, parallelism settings, catchup=False, max_active_runs, retry policy, sla_miss_callback, alerting email/Slack, log storage, metadata DB cleanup, DAG versioning
8. What Just Happened — "LocalExecutor works for single-machine orchestration. KubernetesExecutor is the Citi production pattern — each task is a pod, no shared state, scales to thousands of parallel tasks."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


