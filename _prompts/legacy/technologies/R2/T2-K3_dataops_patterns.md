SAVE AS: dataops_patterns.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a DataOps patterns notebook.

TASK: DataOps loop, testing pyramid, blue-green pipeline deploys, and contract testing — demonstrated conceptually with live local validation against the Citi Postgres database and dbt project.

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
1. Title + Mental Model — "DataOps Patterns — Testing Pyramid, Blue-Green Deploys, Data Contracts"
2. Setup — psycopg2 + subprocess for dbt; PYTHONIOENCODING=utf-8; no pip install; DBT_PATH = "C:/py_venv/proj_educate/Scripts/dbt.exe"
3. DataOps Loop — explain the four phases (plan → develop → test → release) as a code cell with commentary; map each phase to a concrete Citi example (e.g., plan=schema contract for alerts, test=GE checkpoint, release=dbt run to mart); print the loop as a diagram string
4. Data Testing Pyramid — write a Python class DataTestingPyramid with three layers: unit (dbt singular tests on mart_alert_summary), integration (GE expectations on raw alerts table via psycopg2 row count + null check), end-to-end (dbt run → assert mart row count > 0); run all three layers; print pass/fail for each; explain why the pyramid shape matters (cheap unit tests at base, expensive e2e at top)
5. Blue-Green Pipeline Deploy — simulate a blue-green deploy: create two schema variants (citi_blue, citi_green) in Postgres via psycopg2; write alerts_summary to blue; run a validation (row count check); if validation passes, swap the alias by creating a view citi_active pointing to citi_green; explain how this pattern eliminates downtime in production pipeline promotions
6. Data Contract Testing — define a Python dataclass DataContract with fields: table_name, required_columns, max_null_pct, min_row_count; instantiate contracts for alerts and endpoints; write a validate_contract() function that queries Postgres and checks each constraint; run validation on both contracts; print a compliance report
7. Schema Evolution Safety — demonstrate a safe schema migration pattern: add a nullable column via ALTER TABLE (if not exists guard); run dbt test to confirm no breakage; explain the difference between additive (safe) and breaking (column rename, type change) schema changes; show how data contracts catch breaking changes before deployment
8. What Just Happened — "DataOps closes the gap between data engineering and software engineering. The testing pyramid gives you fast feedback at low cost. Blue-green deploys make pipeline promotions reversible. Data contracts make schema expectations explicit and machine-checkable. Citi's alerting pipeline uses all three to ship safely across 6,000 endpoints."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

