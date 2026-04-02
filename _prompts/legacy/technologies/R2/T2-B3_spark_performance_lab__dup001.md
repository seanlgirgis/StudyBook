SAVE AS: spark_performance_lab.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a Spark performance tuning lab.

TASK: Live performance experiments on the telemetry dataset — broadcast join, skew handling, partition tuning, coalesce vs repartition.

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
1. Title + Mental Model — "Spark Performance Lab — Broadcast, Skew, Partitions, AQE"
2. Imports + SparkSession + timing helper (time.perf_counter wrapper)
3. Experiment 1: Broadcast Join — join alerts (25K) to endpoints (10K) with and without broadcast hint; time both; print "Without broadcast: Xs, With broadcast: Xs, Speedup: Xx"
4. Experiment 2: Partition Tuning — count alerts grouped by severity with 2, 10, 50, 200 partitions (spark.sql.shuffle.partitions); time each; print results table; explain sweet spot
5. Experiment 3: Skew Simulation — create skewed dataset (99% of alerts for one endpoint_id), join to endpoints, show partition size distribution; apply salting technique to fix skew; compare times
6. Experiment 4: coalesce vs repartition — start with 200 partitions, coalesce to 4 vs repartition to 4; time write to Parquet for each; explain when to use each
7. Experiment 5: Predicate Pushdown via JDBC — compare loading full metrics table vs loading with pushdown_predicate WHERE metric_name='cpu_utilization'; show row counts and time
8. What Just Happened — consolidate all 5 experiments into a decision guide; "At Citi scale (500K metrics, 25K alerts), these tuning decisions are the difference between a 30-second job and a 5-minute job."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
