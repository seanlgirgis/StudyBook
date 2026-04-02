# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-J1_mlflow_tracking.md

SAVE AS: mlflow_tracking.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing an MLflow deep dive notebook.

TASK: MLflow tracking server, experiment management, artifact logging, model registry, and serving — running live against local MLflow (localhost:5000).

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
1. Title + Mental Model — "MLflow — Experiments, Runs, Registry, Serving"
2. Setup — mlflow.set_tracking_uri("http://localhost:5000"); imports: mlflow, sklearn, pandas, psycopg2; no pip install
3. Experiment Management — create experiment "citi-anomaly-detection"; log 3 runs with different hyperparameters (contamination: 0.01, 0.05, 0.1); log params, metrics, tags; print experiment URL
4. Artifact Logging — in best run, log: trained IsolationForest model, feature importance plot (matplotlib), confusion matrix, a JSON artifact with model metadata; show artifact URI
5. Model Registry — register best model to "citi-anomaly-detector"; transition through Staging → Production; add description and tags; list all registered model versions; print "Model citi-anomaly-detector v1 in Production"
6. Model Loading + Inference — load model from registry using mlflow.sklearn.load_model("models:/citi-anomaly-detector/Production"); run inference on 100 new metrics rows from Postgres; print anomaly count and sample anomalies
7. Comparing Runs — use mlflow.search_runs() to load all runs as a DataFrame; sort by metric; show the comparison table; explain how this supports hyperparameter search
8. What Just Happened — "MLflow is the experiment tracker that makes ML reproducible. The model registry is the handoff between Data Science (training) and Data Engineering (serving). At Citi, every model that touches production data must be registered with its training data version."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


