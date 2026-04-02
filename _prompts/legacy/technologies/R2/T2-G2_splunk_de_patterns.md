SAVE AS: splunk_de_patterns.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing Splunk data engineering patterns.

TASK: HEC ingestion, index design, retention policy, and forwarder concepts — running live against the local Splunk instance.

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
1. Title + Mental Model — "Splunk for Data Engineers — HEC, Index Design, Retention, Forwarders"
2. HEC Bulk Ingestion — send 1000 events in batches of 100 (batch HEC API); measure throughput; print "Ingested 1000 events at X events/sec"
3. Index Design — explain index separation strategy (operational vs security vs compliance vs metrics); show why citi_telemetry is the right index name; explain sourcetype design
4. Retention Policy — explain hot/warm/cold/frozen bucket lifecycle; show retention config concepts; calculate storage cost for 6000 endpoints × 10 events/sec × 90 days
5. Forwarder Architecture — explain Universal Forwarder vs Heavy Forwarder vs HTTP Event Collector; when to use each; draw ASCII architecture for Citi: [Endpoints] → [UF] → [Indexer Cluster] → [Search Head]
6. Lookup Tables — create a CSV lookup (endpoint_id → region, category); upload to Splunk via REST API; run SPL query with | lookup to enrich events
7. What Just Happened — "HEC is the fastest ingest path — it bypasses the forwarder stack. For DE purposes, HEC + Python = the streaming ingest pattern. Citi uses HEC for real-time telemetry and Universal Forwarders for log file tailing."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

