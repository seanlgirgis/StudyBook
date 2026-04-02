SAVE AS: modern_de_stack_2026.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a Staff-level opinion notebook on modern DE stack choices.

TASK: Opinionated, evidence-backed notebook — what a Staff DE recommends for a greenfield data platform in 2026 and why. Every recommendation runs a live sanity check against the local stack to prove it works.

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
1. Title + Philosophy — "The Modern DE Stack 2026 — What I'd Actually Recommend"; opening: "Complexity is the enemy of reliability — every technology you add must justify its operational cost"
2. The Recommended Stack (markdown): Kafka for streaming ingest → Spark for compute → Delta Lake for storage format → dbt for transformation → Airflow for orchestration → MLflow for model tracking → Great Expectations for data quality → Splunk/ELK for observability → Terraform for IaC; ASCII architecture diagram
3. Streaming Layer — Why Kafka: Kafka AdminClient health check against localhost:9092; list topics; print broker version; explain why Kafka beats alternatives for regulated, on-prem requirements
4. Compute Layer — Why Spark: SparkSession health check; load 10K endpoints from Postgres; show schema; explain why Spark's batch+streaming unification wins over Flink for most teams
5. Transformation Layer — Why dbt: subprocess `dbt debug`; explain why SQL-first transformation scales better than PySpark transforms for analytics engineers
6. Orchestration Layer — Why Airflow: requests GET http://localhost:8082/health; explain why Airflow's DAG-as-code wins for complex dependency management
7. Observability Layer — Why MLflow for ML experiments: requests GET http://localhost:5000/api/2.0/mlflow/experiments/list; explain experiment tracking as a first-class concern
8. What I'd Do Differently — honest reflection: where Kafka is overkill (use Postgres logical replication for <1K events/sec), where Spark is overkill (use DuckDB for <100GB), where Airflow is overkill (use cron for simple pipelines); Citi framing: "Citi's scale justifies every layer — but most teams should start simpler"
9. The Staff DE Interview Answer — ready-to-deliver 90-second answer to "Design me a modern data platform"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
