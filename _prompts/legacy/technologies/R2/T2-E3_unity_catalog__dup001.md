SAVE AS: unity_catalog.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a Unity Catalog notebook.

TASK: Data governance on Databricks — catalog/schema/table hierarchy, lineage, and access control — via requests against the Databricks workspace.

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
1. Title + Mental Model — "Unity Catalog — Governance, Lineage, Access Control on Databricks"
2. Setup — requests-based UC API client using /api/2.1/unity-catalog/ endpoints
3. Catalog/Schema Discovery — list catalogs via GET /api/2.1/unity-catalog/catalogs; list schemas in main catalog; list tables; print hierarchy tree
4. Table Metadata — GET table details for one table; show columns, owner, created_at, data_source_format; print as formatted table
5. Lineage (conceptual) — explain column-level lineage: how Unity Catalog tracks which query read which columns and produced which output table; show the API endpoint structure (GET /api/2.1/lineage-tracking/table-lineage)
6. Access Control — explain the 3-level privilege model: catalog → schema → table; show GRANT/REVOKE SQL pattern; explain how Unity Catalog differs from workspace-level ACLs
7. Tags and Classification — show how to add tags to a table via PATCH /api/2.1/unity-catalog/tables/{table_id}; explain PII classification use case for Citi telemetry data
8. What Just Happened — "Unity Catalog is Databricks' answer to data governance. One catalog across all workspaces, column-level lineage, row-level security. At Citi, this maps to regulatory data classification requirements — PII fields need column-level masking."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
