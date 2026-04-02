# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-F1_docker_k8s_for_de.md

SAVE AS: docker_k8s_for_de.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a K8s for data engineering notebook.

TASK: Deploying data workloads on Kubernetes — Spark on K8s, persistent volumes, ConfigMaps, Secrets — demonstrated with Docker Desktop's local K8s cluster (enable Kubernetes in Docker Desktop Settings → Kubernetes → Enable).

NOTE: Include a graceful guard at the start: try kubectl cluster-info; if it fails, print "Enable Kubernetes in Docker Desktop → Settings → Kubernetes → Enable Kubernetes → Apply" and set k8s_available=False; wrap all K8s sections in if k8s_available checks.

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
1. Title + Mental Model — "Kubernetes for Data Engineering — Pods, PVCs, Secrets, Spark on K8s"
2. Setup — subprocess-based kubectl wrapper with UTF-8 encoding; k8s_available detection
3. Core Objects Demo (if k8s_available) — create a ConfigMap with Postgres connection params; create a Secret with credentials (base64 encoded); apply both; kubectl describe each; print "ConfigMap and Secret created"
4. PersistentVolumeClaim (if k8s_available) — create a PVC for 1Gi; create a Pod that mounts it and writes a test file; wait for completion; read the file back; delete pod and PVC
5. DE Deployment (if k8s_available) — deploy a simple "citi-checker" Deployment (2 replicas) that runs the same postgres check from R1; create a Service; kubectl get endpoints; print "Deployment running, 2 replicas healthy"
6. Spark on K8s Architecture (markdown) — explain how Spark KubernetesExecutor works: driver pod + dynamic executor pods; show spark-submit command for K8s; explain PVC for checkpoint storage
7. What Just Happened — "Every Spark executor in production Citi is a K8s pod. The KubernetesExecutor in Airflow spins a pod per task and deletes it when done. PVCs provide the durable checkpoint storage that survives pod termination."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


