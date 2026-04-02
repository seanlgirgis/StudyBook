# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-A1_kafka_patterns_internals.md

SAVE AS: kafka_patterns_internals.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a deep Kafka internals notebook.

TASK: Cover ISR mechanics, exactly-once semantics, consumer group rebalancing, and log compaction — all running live against the Citi Kafka stack.

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
1. Title + Mental Model — "Kafka Internals — Replication, Exactly-Once, Consumer Groups, Compaction"
2. Imports + config (confluent-kafka, psycopg2, real credentials, no pip install)
3. ISR Deep Dive — use AdminClient to describe "citi.alerts" topic, show ISR set, explain what happens when a broker goes down; print partition leaders and ISR lists
4. Exactly-Once Semantics — create a transactional producer (transactional.id="citi-txn-1"), produce 10 alerts in a transaction, commit; explain idempotent vs transactional vs at-least-once; print "Transaction committed — 10 alerts written exactly once"
5. Consumer Group Mechanics — create 2 consumers in group "citi-deep-group", show partition assignment per consumer, consume 20 messages splitting across consumers, show how many each consumed; simulate a consumer leaving and show rebalance
6. Log Compaction — explain compaction policy; create topic "citi.endpoint-status" with cleanup.policy=compact, produce 20 status events for 5 endpoints (multiple updates per endpoint), produce a tombstone for one endpoint (null value); print "Compacted topic created — latest value per key preserved"
7. What Just Happened — summary + Citi interview angle: "ISR shrink + acks=all = the tradeoff Citi makes between latency and durability"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


