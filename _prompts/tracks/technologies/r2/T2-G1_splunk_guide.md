# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-G1_splunk_guide.md

SAVE AS: splunk_guide.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a comprehensive Splunk SPL guide.

TASK: SPL fundamentals — stats, eval, transaction, rex, timechart, alerts — running live against Splunk HEC (localhost:8088, token=f9d0f92a-fcad-4a02-a76e-0b9a325cffe8, index=citi_telemetry).

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
1. Title + Mental Model — "Splunk SPL — stats, eval, transaction, rex, timechart"
2. Setup — send 500 events to Splunk HEC using requests; events are alerts from Postgres (real data); no pip install
3. SPL Fundamentals — run 6 SPL queries via Splunk REST API (localhost:8089/services/search/jobs):
   - stats count by severity
   - eval severity_score = case(severity=="CRITICAL",4, severity=="HIGH",3, severity=="MEDIUM",2,1)
   - timechart span=1h count by severity
   - top 10 endpoint_id by alert count
   - transaction endpoint_id maxspan=10m (group related alerts)
   - rex field=message "(?<error_type>\w+\s\w+)" to extract error type
4. Search Commands Cheat Sheet — markdown table: command | purpose | example
5. Alert Configuration — explain saved searches, alert thresholds, action types (email, webhook, script); show alert creation via REST API
6. Dashboard Pattern — explain dashboard XML structure; show a sample panel XML for alert count by severity over time
7. What Just Happened — cover all 6 SPL commands with Citi framing; "SPL is the language of operational intelligence. A Citi SOC analyst uses these exact commands to triage 6,000+ endpoints."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


