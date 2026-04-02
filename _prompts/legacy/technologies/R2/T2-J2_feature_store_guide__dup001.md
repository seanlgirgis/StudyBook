SAVE AS: feature_store_guide.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a feature store concepts notebook.

TASK: Feature store architecture, online vs offline store, point-in-time join, and serving — using Feast (open source) against local Postgres as offline store. Install is done externally so no pip install cell.

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
1. Title + Mental Model — "Feature Stores — Offline, Online, Point-in-Time Join, Serving"
2. Setup — feast imports; define feature repo pointing to local Postgres; PROJECT_ID="citi_features"; no pip install
3. Feature Definition — define FeatureView for endpoint_alert_features (alert count per endpoint per day, last severity, alert rate); define Entity (endpoint_id); write feature_store.yaml for local Postgres
4. Offline Store — feast apply; materialize features from Postgres into offline store; retrieve historical features with point-in-time join for a training dataset; print "Training dataset: {N} rows × {M} features"
5. Online Store — feast materialize-incremental to push latest features to SQLite online store; retrieve online features for 10 endpoint_ids in <10ms; print "Online feature retrieval: Xms"
6. Point-in-Time Join Deep Dive — explain why naive joins leak future data; show the timestamp alignment logic; demonstrate with an example where wrong join gives 15% higher accuracy (data leakage)
7. Feature Store Architecture — comparison table: Feast vs Tecton vs Hopsworks vs SageMaker Feature Store; rows: open source, online latency, offline batch, streaming features, cost
8. What Just Happened — "A feature store prevents the #1 ML production bug: training-serving skew. Features computed the same way at training time and serving time. Point-in-time join prevents data leakage. Citi's risk models use features computed 24h before the event being predicted."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
