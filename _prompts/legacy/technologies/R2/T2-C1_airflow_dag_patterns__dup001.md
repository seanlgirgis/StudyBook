SAVE AS: airflow_dag_patterns.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing an Airflow advanced patterns notebook.

TASK: Idempotency, backfill, sensors, dynamic DAGs, and TaskFlow API — all running against local Airflow (localhost:8082).

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
1. Title + Mental Model — "Airflow — Idempotency, Backfill, Sensors, Dynamic DAGs, TaskFlow"
2. Imports + Airflow REST API client (requests, localhost:8082, auth admin/admin, no pip install)
3. Idempotency Pattern — create a DAG via file write that uses PostgresOperator with INSERT ... ON CONFLICT DO NOTHING; trigger it twice via REST API; verify table has same row count; print "Idempotency verified: {count} rows, no duplicates"
4. Backfill Simulation — trigger DAG with logical_date set 7 days ago via REST API; poll until complete; print execution summary
5. Sensor Pattern — write a FileSensor DAG that waits for a file to appear; create the file via Python after 3 seconds; poll DAG run until success; print "FileSensor triggered and completed"
6. Dynamic DAG — write a DAG that generates tasks dynamically from a list (one task per Citi region: NYC1, SNG1, LDN1, TKY1, SYD1); each task queries alert count for that region from Postgres; print results
7. TaskFlow API — rewrite the dynamic DAG using @task decorator and @dag decorator; show how XCom is implicit with TaskFlow; compare with traditional PythonOperator approach
8. What Just Happened — "Idempotency is the most important Airflow property for data engineering. A DAG that can be re-run safely is a DAG that can be monitored, recovered, and backfilled. Citi's SLA-driven pipelines depend on this."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
