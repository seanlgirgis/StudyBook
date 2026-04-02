SAVE AS: spark_internals_tuning.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a Spark internals notebook.

TASK: DAG inspection, stage/shuffle mechanics, memory management, and Catalyst optimizer — all running live on the telemetry dataset.

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
1. Title + Mental Model — "Spark Internals — DAG, Shuffle, Memory, Catalyst"
2. Imports + SparkSession (master=local[*], JAVA_HOME and HADOOP_HOME set via os.environ, no pip install)
3. DAG Inspection — load endpoints + alerts via JDBC, do a join + groupBy, call .explain(True) to show physical plan; explain each stage in markdown
4. Shuffle Deep Dive — force a wide transformation (repartition to 10 partitions, then count per partition); show partition distribution with rdd.glom().map(len).collect(); explain shuffle write/read cost
5. Memory Management — demonstrate spill by processing metrics (500K rows), show spark.executor.memory config; explain on-heap vs off-heap, storage vs execution memory fractions
6. Catalyst Optimizer — show predicate pushdown: filter before join vs after join (use .explain() to confirm); show broadcast hint forcing: spark.sql.autoBroadcastJoinThreshold vs manual broadcast()
7. AQE (Adaptive Query Execution) — enable spark.sql.adaptive.enabled=true, run skewed join, show how AQE splits skewed partitions; compare plan with/without AQE
8. What Just Happened — "Every Spark job is a DAG of stages separated by shuffles. Tuning = minimize shuffles, maximize pushdown, right-size partitions. Citi Spark jobs on 500K metrics + 25K alerts should run in under 10 seconds on local[*]."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

