SAVE AS: github_actions_de.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a GitHub Actions for DE notebook.

TASK: CI/CD workflows for data pipelines — dbt CI, Great Expectations in pipeline, matrix testing — demonstrated conceptually with live local validation.

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
1. Title + Mental Model — "GitHub Actions for Data Engineering — dbt CI, GE, Matrix Testing"
2. Setup — subprocess for dbt (DBT_PATH = "C:/py_venv/proj_educate/Scripts/dbt.exe"), great_expectations imports; no pip install
3. dbt CI Workflow — write a complete .github/workflows/dbt-ci.yml as a Python string; include: trigger on PR, steps: checkout + pip install + dbt deps + dbt compile + dbt test --select state:modified+; save to D:/Workspace/Technologies/.github/workflows/dbt-ci.yml; print the YAML
4. GE Checkpoint in CI — run the existing GE checkpoint from cicd_data_intro locally; capture results as JSON; write a function that fails with non-zero exit code if any expectation fails; demonstrate the fail-fast behavior
5. Matrix Testing — write matrix.yml showing a matrix strategy across Python versions (3.10, 3.11, 3.12) and dbt adapters (postgres, snowflake); explain how matrix reduces redundant workflow code
6. Secrets Management — explain GitHub Secrets vs environment variables; show how to reference secrets in workflow YAML ({{ secrets.POSTGRES_PASSWORD }}); explain never hardcoding credentials in workflow files
7. Data Pipeline CI Flow — write a complete end-to-end CI workflow: lint SQL (sqlfluff) → dbt test → GE checkpoint → deploy (dbt run); explain the pipeline as a code contract
8. What Just Happened — "A CI pipeline for data is a quality gate. Every PR runs dbt tests + GE expectations before merge. Citi's data team catches schema drift, null violations, and referential integrity breaks in CI — before they hit production."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
