SAVE AS: aws_lake_formation.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a Lake Formation governance notebook.

TASK: Lake Formation registration, permissions, column-level security, and row filters — conceptual + live API calls where possible.

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
1. Title + Mental Model — "AWS Lake Formation — Fine-grained Access Control for Data Lakes"
2. Setup — boto3 lakeformation client with study profile
3. Lake Registration — register an S3 bucket as a Lake Formation location; explain what registration means (LF controls access instead of S3 bucket policies)
4. Database and Table Permissions — grant SELECT on citi_deep_glue.alerts to an IAM principal; show the permission model; compare to IAM-only approach
5. Column-level Security — show how to grant access to specific columns only (endpoint_id, severity) while denying message column (PII simulation); explain DESCRIBE vs SELECT permission
6. Row-level Filters — explain Data Filter concept; show how to create a filter WHERE severity='CRITICAL' for a security analyst role; walk through the API call
7. LF vs IAM — decision table: when IAM alone is sufficient vs when Lake Formation is required; explain the "hybrid mode" pitfall
8. What Just Happened — "Lake Formation is Citi's governance layer for S3-based data lakes. It enables column masking (PII), row-level filtering (regional data isolation), and centralized audit logging — all requirements for a regulated financial institution."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
