# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-E1_databricks_delta_lake.md

SAVE AS: databricks_delta_lake.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a Delta Lake internals notebook.

TASK: Delta Lake ACID transactions, time travel, Z-ordering, and OPTIMIZE — running against the Databricks workspace via requests (not databricks-sdk).

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
1. Title + Mental Model — "Delta Lake — ACID, Time Travel, Z-ordering, OPTIMIZE"
2. Setup — HOST, TOKEN, WAREHOUSE_ID hardcoded; requests-based SQL executor (poll loop until SUCCEEDED); no pip install
3. Create Delta table — execute SQL to create a Delta table citi_delta.alerts from a VALUES clause with 20 sample alerts; print "Delta table created"
4. ACID: Concurrent Writes — run two INSERT statements sequentially; show that Delta's transaction log prevents conflicts; explain optimistic concurrency
5. Time Travel — INSERT 5 more rows; then SELECT with VERSION AS OF 0 to see original state; and TIMESTAMP AS OF to show time-based travel; print both result sets
6. Schema Evolution — ALTER TABLE to add a new column response_time_ms; INSERT rows with the new column; show how Delta handles schema changes safely
7. Z-ordering — run OPTIMIZE citi_delta.alerts ZORDER BY (severity, endpoint_id); explain what Z-ordering does for query pruning; run a filtered query before and after and compare
8. What Just Happened — "Delta Lake = Parquet + transaction log. The _delta_log/ directory is the entire ACID story. Time travel is free — it is just reading an older version of the log. Citi uses Delta on Databricks as the production lakehouse format."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


