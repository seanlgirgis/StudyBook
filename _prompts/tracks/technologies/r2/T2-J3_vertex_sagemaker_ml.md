# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-J3_vertex_sagemaker_ml.md

SAVE AS: vertex_sagemaker_ml.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a managed ML platform notebook.

TASK: SageMaker Pipelines and Vertex AI — the managed ML platforms on AWS and GCP. SageMaker via boto3 (study profile); Vertex AI via google-cloud-aiplatform (citi-de-learning project). Show the APIs and concepts; full pipeline execution is expensive so show job definitions + trigger, then describe/status.

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
1. Title + Mental Model — "SageMaker vs Vertex AI — Managed ML Pipelines"
2. Setup — boto3 sagemaker client; GOOGLE_APPLICATION_CREDENTIALS set; project="citi-de-learning"
3. SageMaker Training Job — define a SKLearn training job (IsolationForest on telemetry metrics) with S3 input/output; create the training job via boto3; wait for it to complete; print "SageMaker training job: {status}"
4. SageMaker Pipeline — show a pipeline definition (JSON) with steps: Processing → Training → Evaluation → Model Registration; explain step types; show how to create and trigger via boto3
5. Vertex AI Training Job — define a CustomJob using the Vertex AI SDK; run IsolationForest training; print "Vertex AI job: {status}"
6. Platform Comparison — table: SageMaker vs Vertex AI × rows: managed notebooks, pipeline orchestration, feature store, model registry, monitoring, cost model, Citi recommendation
7. What Just Happened — "SageMaker is AWS's end-to-end ML platform. Vertex AI is GCP's equivalent. Both provide managed training, pipelines, and serving. The Data Engineer's role is building the feature pipeline and deployment automation — the model itself is Data Science's responsibility."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


