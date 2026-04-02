SAVE AS: azure_synapse_adf.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing an Azure analytics notebook.

TASK: Synapse Serverless SQL, Azure Data Factory concepts, and Event Hubs patterns — using Azure CLI (az.cmd) and Python SDK.

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
1. Title + Mental Model — "Azure Analytics — Synapse Serverless SQL, ADF, Event Hubs"
2. Setup — AZ path hardcoded; SUBSCRIPTION_ID="b3811436-61fc-4a3a-a6a9-deb05955076d"; run_az helper with UTF-8 encoding; Azure Python SDK imports (azure-storage-file-datalake, azure-eventhub); no pip install
3. ADLS Gen2 Setup — create resource group + storage account (ADLS Gen2 with HNS) via az CLI; upload Parquet file (endpoints + alerts from Postgres); print "Data uploaded to ADLS Gen2"
4. Synapse Serverless SQL Pattern — explain OPENROWSET for querying Parquet directly; write the SQL that would be run in Synapse Studio (in a markdown cell — Synapse workspace takes 10 minutes to provision so show the pattern, not live execution); show CREATE EXTERNAL TABLE pattern
5. Azure Data Factory — explain ADF pipelines (source → sink), Integration Runtimes (cloud vs self-hosted), triggers (schedule, tumbling window, event); show the JSON pipeline definition for a simple copy activity from ADLS → SQL Database
6. Event Hubs Patterns — create Event Hubs namespace + hub (Standard SKU); send 20 telemetry events; read them back; show consumer group isolation (two consumer groups, each receiving all events); delete namespace
7. Cleanup — delete resource group
8. What Just Happened — "Synapse Serverless SQL is Athena for Azure — pay per scan, no infrastructure. ADF is Glue for Azure — managed ETL with 90+ connectors. Event Hubs is Kafka for Azure — Kafka protocol compatible. Citi EMEA uses this stack."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
