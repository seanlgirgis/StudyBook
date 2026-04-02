# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R3\\T3-4_platform_decision_matrix.md

SAVE AS: platform_decision_matrix.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a platform decision framework notebook.

TASK: Build a structured decision matrix for choosing between competing DE technologies. For each decision axis, implement a working code example on the winning technology to prove the point — not just slides.

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
1. Title + Framing — "Platform Decision Matrix — How a Staff DE Chooses Technology"; explain the workload-first decision philosophy
2. Decision 1 — Kafka vs Kinesis: markdown decision table (throughput, ordering, replay, cost, ops burden, on-prem); code: produce 50 alerts to Kafka "citi.decision.kafka" and consume — prove sub-10ms round trip; Citi framing: when Citi chooses self-managed Kafka vs AWS Kinesis
3. Decision 2 — Spark vs Flink: markdown decision table (batch/streaming unification, state management, latency, ecosystem, hiring pool); code: Spark Structured Streaming micro-batch on "citi.decision.spark" — 50 messages — show batch interval; Citi framing: Spark for batch-first teams, Flink for sub-second latency requirements
4. Decision 3 — Airflow vs Prefect vs Dagster: markdown decision table (code-first vs UI-first, dynamic DAGs, observability, cloud managed options); code: trigger Airflow DAG via CLI, show health check response; Citi framing: Airflow for regulated environments with established tooling
5. Decision 4 — dbt vs SQLMesh: markdown decision table (lineage, semantic layer, stateful runs, incremental strategies); code: run `dbt ls` to list models; Citi framing: dbt for broad ecosystem + dbt Cloud managed SLA
6. Decision 5 — Delta Lake vs Iceberg vs Hudi: markdown decision table (ACID support, time travel, streaming write, engine compatibility, Databricks lock-in); Citi framing: Delta for Databricks shops, Iceberg for multi-engine environments
7. Decision 6 — AWS vs GCP vs Azure for DE: markdown decision table (managed Kafka, managed Spark, data warehouse, pricing model, existing enterprise contracts); Citi framing: multi-cloud by business unit, not by workload
8. The Decision Framework — flowchart as markdown pseudocode: start with "What is the latency requirement?" → branch to streaming vs batch → branch to managed vs self-managed → end at a technology recommendation; Citi framing tying all decisions together

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


