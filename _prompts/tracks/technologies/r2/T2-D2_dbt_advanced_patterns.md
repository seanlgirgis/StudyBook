# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-D2_dbt_advanced_patterns.md

SAVE AS: dbt_advanced_patterns.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing advanced dbt patterns.

TASK: Macros, packages, exposures, and CI/CD patterns for dbt — running live.

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
1. Title + Mental Model — "dbt Advanced — Macros, Packages, Exposures, CI/CD"
2. Imports + dbt setup
3. Macros — create macros/citi_helpers.sql with: cents_to_dollars(column) macro (divide by 100), current_timestamp_utc() macro, generate_surrogate_key(columns) macro; use each in a model; run dbt run; verify macro output
4. Packages — add dbt_utils to packages.yml; run dbt deps; use dbt_utils.surrogate_key() in a model; run; print "Package dbt_utils installed and used"
5. Exposures — add an exposure in schema.yml pointing to a "Citi Telemetry Dashboard" that depends on mart_alert_summary; run dbt ls --select +exposures; show exposure metadata
6. Custom Generic Test — write a custom test assert_severity_distribution that checks no single severity exceeds 40% of total; add to schema.yml; run dbt test; show result
7. CI/CD Pattern — write a bash-script-as-string showing the full dbt CI flow: dbt deps → dbt compile → dbt test --select state:modified+ → dbt run --select state:modified+; explain state:modified
8. What Just Happened — "Macros are dbt's DRY mechanism. Packages extend the standard library. Exposures create lineage from dbt to BI tools. CI/CD with state:modified+ runs only what changed — 10-second CI for a 500-model project."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


