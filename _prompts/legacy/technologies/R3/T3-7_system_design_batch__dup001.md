SAVE AS: system_design_batch.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a system design interview simulation notebook for batch pipelines.

TASK: Simulate a full Staff DE system design interview — "Design a nightly data warehouse load for 6,000 API endpoints." Walk through clarifying questions, constraints, architecture decisions, deep dives, and tradeoffs. Code cells prove the key decisions with live stack validation.

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
1. Title + Interview Framing — "System Design — Nightly Data Warehouse Load"; explain the SLA: 500K metrics + 25K alerts + 10K endpoints loaded, transformed, and served before 6 AM; 45-minute interview structure
2. Step 1 — Clarifying Questions: markdown cell listing 8 clarifying questions with model answers; volume math: 500K metrics/day = ~5.8 events/sec average, peak 50K/minute at midnight; idempotency requirement: re-running the pipeline must not duplicate data
3. Step 2 — High-Level Design: ASCII diagram: Source Postgres (OLTP) → Airflow (orchestrate) → Spark (extract+transform) → Postgres (warehouse tables) → dbt (mart layer) → dbt tests (quality gate); code: Airflow health check + SparkSession init; print "Design is runnable"
4. Step 3 — Airflow Orchestration Deep Dive: explain DAG structure (extract → transform → test → load → notify); trigger "batch_pipeline_nightly" via CLI; show DAG run state; explain retry policy (3 retries, 5-minute delay), SLA miss alert, backfill strategy
5. Step 4 — Spark Extraction Deep Dive: load 500K metrics via JDBC with partitioning (numPartitions=4, partitionColumn=endpoint_id, lowerBound=1, upperBound=10000); show partition distribution; time the load; explain JDBC partition math
6. Step 5 — dbt Transform Deep Dive: subprocess `dbt run --select mart_endpoint_daily_health`; show SQL inline (markdown): JOIN metrics + endpoints + alerts on endpoint_id, compute daily P95, alert_count, status; explain incremental vs full refresh choice; subprocess `dbt test`; print test results
7. Step 6 — Idempotency and Failure Modes: code demo — run the Spark extract + write twice; show that row count does not double (use INSERT ... ON CONFLICT DO UPDATE or TRUNCATE + INSERT pattern); explain idempotency contract; markdown: failure mode table (Spark OOM, dbt test fail, Airflow scheduler down) + mitigation
8. Step 7 — Interview Wrap-Up: cost estimation (Spark EMR cost for 500K metrics/day), scaling to 10× data volume, what changes; 3 ready-to-deliver closing statements; Citi framing: "This nightly job is the data contract between Citi's operational telemetry and its risk reporting layer"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
