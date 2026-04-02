# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R3\\T3-1_lambda_kappa_architecture.md

SAVE AS: lambda_kappa_architecture.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a capstone integration notebook.

TASK: Build both Lambda and Kappa architectures against the Citi telemetry stack. Implement each pattern with real running code, compare the tradeoffs, and explain when each applies in a Staff DE interview.

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
1. Title + Architecture Overview — "Lambda vs Kappa — Two Ways to Build the Citi Telemetry Pipeline"; ASCII diagram of each architecture
2. Imports + config (confluent-kafka, pyspark, psycopg2, real credentials, no pip install)
3. Lambda — Batch Layer: use psycopg2 to load all 500K metrics into a Spark DataFrame, compute hourly P95 latency per region, write result table "batch_views" to Postgres; print row count + sample
4. Lambda — Speed Layer: produce 50 fresh metrics to Kafka topic "citi.lambda.speed", consume and aggregate in Spark Structured Streaming (memory sink "speed_view"); after 8 seconds show results
5. Lambda — Serving Layer: merge batch_views + speed_view with a UNION query in psycopg2; print "Lambda serving layer: batch + speed merged — X rows"
6. Kappa — Single Stream: produce the same 50 metrics to "citi.kappa.stream", run one Spark Structured Streaming job that computes the same P95 — no separate batch layer; print "Kappa result: X rows from single stream"
7. Tradeoff Comparison — markdown cell: table comparing Lambda vs Kappa on complexity, latency, reprocessing, operational cost, when each wins; Citi framing: "Citi moved from Lambda toward Kappa as Spark Structured Streaming matured — reprocessing is replay, not rebuild"
8. What Just Happened — 3 ready-to-deliver interview answers: "What is Lambda architecture?", "When would you choose Kappa?", "How does Citi's telemetry fit each model?"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


