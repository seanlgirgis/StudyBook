SAVE AS: aws_glue_emr_athena.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a deep AWS DE notebook.

TASK: Glue Data Catalog, Glue ETL jobs, EMR Serverless, and Athena — running live against AWS (profile=study, us-east-1).

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
1. Title + Mental Model — "AWS DE Deep — Glue Catalog, Glue ETL, EMR Serverless, Athena"
2. Setup — boto3 with os.environ["AWS_PROFILE"]="study"; no pip install
3. Glue Catalog — create a Glue database "citi_deep_glue"; create a table definition for endpoints (CSV schema, S3 location); use Glue client to list databases and tables; print catalog hierarchy
4. Glue ETL Job (Script) — write a Glue ETL script (as Python string) that reads from S3, transforms (filter HIGH/CRITICAL alerts), writes Parquet; create the job definition via Glue client; explain DPU pricing; do NOT run the job (cost) — show the job definition
5. Athena Advanced — upload endpoints + alerts CSV to S3; create Athena table with PARTITION BY (severity); run MSCK REPAIR TABLE; run 3 partitioned queries; compare costs with/without partitioning (show data scanned)
6. Athena Workgroup — create a workgroup "citi-analytics" with result location and 1GB query limit; run a query in that workgroup; show how workgroups enable cost control per team
7. Cleanup — delete all S3 objects, Glue database, Athena workgroup
8. What Just Happened — "Glue Catalog is the metadata layer for all AWS analytics. Athena pays per scan — partitioning is how you cut costs 10-100x. EMR Serverless is Spark without cluster management. Citi uses this stack for batch analytics on CloudTrail + telemetry logs."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

