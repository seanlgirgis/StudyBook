SAVE AS: great_expectations_guide.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a comprehensive Great Expectations guide.

TASK: Expectations, suites, checkpoints, data docs — running live against the Citi Postgres database using GE 1.x API.

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
1. Title + Mental Model — "Great Expectations — Suites, Checkpoints, Data Docs"
2. Setup — import great_expectations as gx; context = gx.get_context(); no pip install; use GE 1.x API (context.data_sources not context.sources)
3. Data Source — add Postgres data source (postgresql+psycopg2://de_admin:DeAdmin2026!@localhost:5432/de_telemetry); add table assets for endpoints, alerts, metrics
4. Expectation Suite — create suite "citi_telemetry_suite"; add 10 expectations covering: column existence, not_null (endpoint_id, severity), unique (alert_id), accepted_values (severity in [HIGH,CRITICAL,MEDIUM,LOW]), row count range (20000-30000 for alerts), column min/max (alert_id > 0), regex match on message field
5. Checkpoint — create and run checkpoint; parse results; print "Expectations: X passed, Y failed"
6. Data Docs — generate data docs via context.build_data_docs(); explain the HTML output structure; explain how to host Data Docs on S3 for team visibility
7. Custom Expectations — write a custom ColumnExpectation that checks no endpoint has more than 10 alerts (business rule); register and run it; print result
8. What Just Happened — "Great Expectations is the data contract framework. Suites define what 'good data' looks like. Checkpoints run those contracts on a schedule or in CI. Data Docs make results visible to stakeholders. Citi uses this to validate every dbt model output before promotion to production."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
