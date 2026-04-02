# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-E2_lakehouse_formats.md

SAVE AS: lakehouse_formats.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a format comparison notebook.

TASK: Delta Lake vs Apache Iceberg vs Apache Hudi — architecture, tradeoffs, and when each wins. Implemented as a conceptual notebook with live Delta examples on Databricks + markdown comparisons for Iceberg and Hudi.

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
1. Title + Mental Model — "Delta vs Iceberg vs Hudi — The Format Wars"
2. Delta Lake live demo — create citi_delta.format_comparison table, write 1000 rows, run VACUUM, show _delta_log structure via DESCRIBE HISTORY
3. Architecture Comparison table — rows: transaction log location, catalog dependency, time travel, schema evolution, row-level deletes (MERGE), streaming support, cloud optimization, primary adopters
4. Iceberg deep dive (markdown) — explain manifest files, snapshot model, hidden partitioning, catalog requirement (Hive, Glue, Nessie); when Iceberg wins (multi-engine shops, Flink + Spark on same table)
5. Hudi deep dive (markdown) — explain Copy-on-Write vs Merge-on-Read, record-level indexing, Bloom filter index, timeline; when Hudi wins (high-frequency upserts, CDC ingestion)
6. Decision Matrix — Citi scenario: "You have a Databricks workspace, 10TB of telemetry data, daily OPTIMIZE runs, and a Spark + SQL team" — which format wins and why
7. What Just Happened — "Delta wins on Databricks. Iceberg wins on multi-engine open architectures. Hudi wins on upsert-heavy CDC pipelines. In 2026, Iceberg is gaining ground on Delta outside Databricks."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


