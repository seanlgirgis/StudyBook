SAVE AS: system_design_streaming.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a system design interview simulation notebook for real-time streaming pipelines.

TASK: Simulate a full Staff DE system design interview — "Design a real-time telemetry pipeline for 6,000 API endpoints." Walk through clarifying questions, constraints, architecture decisions, deep dives, and tradeoffs. Code cells prove the key decisions with live stack validation.

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
1. Title + Interview Framing — "System Design — Real-Time Telemetry Pipeline"; explain the 45-minute interview structure: clarify (5 min) → high-level design (10 min) → deep dive (20 min) → tradeoffs (10 min)
2. Step 1 — Clarifying Questions: markdown cell listing 8 clarifying questions with model answers; volume math: 6,000 endpoints × 10 events/sec = 60,000 events/sec = 216M events/hour; latency SLA: <30 seconds end-to-end for alerting
3. Step 2 — High-Level Design: ASCII diagram: API endpoints → Kafka (ingest) → Spark Streaming (process) → Delta/Postgres (store) → dbt (serve) → Splunk (alert); code: verify all 4 local services are healthy (Kafka AdminClient + SparkSession + Airflow health + MLflow health); print "All services healthy — design is runnable"
4. Step 3 — Kafka Deep Dive: partition count math (60K events/sec ÷ 10K events/sec/partition = 6 partitions minimum, add 3× buffer = 18); produce 60 alert events to "citi.sysdesign.stream" (10 per partition × 6 partitions); print partition distribution
5. Step 4 — Spark Processing Deep Dive: Spark Structured Streaming on "citi.sysdesign.stream"; trigger every 10 seconds; group by severity + 30-second window; write to memory sink "realtime_alerts"; show results; explain watermark choice
6. Step 5 — Storage Deep Dive: explain Delta Lake ACID guarantees for exactly-once; explain retention tiers (hot: 7 days Postgres, warm: 90 days S3/GCS, cold: 7 years archive); write streaming results to Postgres "rt_alert_summary"; verify row count
7. Step 6 — Tradeoffs and Failure Modes: markdown table — what happens when: Kafka broker goes down, Spark executor OOM, dbt run fails, Postgres disk full; mitigation for each; Citi framing: "At 60K events/sec, even 1 minute of downtime = 3.6M lost events — replay is mandatory"
8. Step 7 — Interview Wrap-Up: 3 ready-to-deliver closing statements; what to say when asked "what would you scale next?"; common Staff DE follow-up questions with model answers

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

