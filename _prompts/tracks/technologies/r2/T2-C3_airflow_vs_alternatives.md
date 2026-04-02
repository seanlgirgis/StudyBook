# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-C3_airflow_vs_alternatives.md

SAVE AS: airflow_vs_alternatives.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a comparison notebook.

TASK: Compare Airflow, Prefect, and Dagster architecturally. Use Airflow live (local stack). Show code examples for equivalent patterns in all three (Prefect/Dagster as code snippets in markdown cells, not executable — they are not installed).

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
1. Title + Mental Model — "Airflow vs Prefect vs Dagster — When Each Wins"
2. Airflow live demo — create a simple ETL DAG (Postgres query → transform → write back), trigger via REST API, monitor to completion
3. Decision Matrix table — rows: learning curve, UI quality, dynamic DAGs, data-aware scheduling, testing story, deployment model, cloud managed option, Citi fit
4. Prefect equivalent — markdown cell showing equivalent flow in Prefect syntax (Python-first, @flow decorator, automatic state tracking, Prefect Cloud)
5. Dagster equivalent — markdown cell showing equivalent job in Dagster syntax (assets-first, @asset decorator, software-defined assets, data lineage built-in)
6. When each wins — three markdown sections: "Use Airflow when...", "Use Prefect when...", "Use Dagster when..."
7. What Just Happened — "Airflow dominates enterprise financial services because of its maturity and MWAA managed offering on AWS. Dagster is winning greenfield data teams who want asset lineage natively. Citi uses Airflow with KubernetesExecutor — migration to Dagster is a 2026 consideration."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


