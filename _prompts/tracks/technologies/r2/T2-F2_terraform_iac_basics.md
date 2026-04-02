# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-F2_terraform_iac_basics.md

SAVE AS: terraform_iac_basics.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a Terraform deep dive notebook.

TASK: Modules, state backends, workspaces, and AWS provider patterns for DE — running live with terraform CLI (at C:\Windows\System32\terraform.exe or system PATH) and AWS profile=study.

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
1. Title + Mental Model — "Terraform IaC — Modules, State, Workspaces, DE Patterns"
2. Setup — subprocess wrapper for terraform with UTF-8 encoding; AWS_PROFILE=study and AWS_DEFAULT_REGION=us-east-1 set via os.environ; working directory D:/Workspace/Technologies/citi_terraform_advanced
3. Module Pattern — write a reusable module in modules/s3_lake/ with main.tf (aws_s3_bucket + aws_s3_bucket_versioning), variables.tf (bucket_name, tags), outputs.tf (bucket_arn, bucket_name); call the module from root main.tf for two environments (dev, prod); terraform init + plan; print plan summary
4. State Backend (S3) — write backend config using S3 backend (bucket=egirgis-lab or any existing bucket, key=citi-terraform/terraform.tfstate, region=us-east-1); explain why local state is dangerous for teams; NOTE: don't actually init with S3 backend (it needs the bucket to exist) — show the config and explain
5. Workspaces — terraform workspace new dev; terraform workspace new prod; terraform workspace list; explain how workspaces isolate state; show how to use ${terraform.workspace} in resource names
6. DE Infrastructure Pattern — write a full DE stack module: S3 bucket (data lake) + Glue database + Athena workgroup; apply; show outputs; terraform destroy
7. What Just Happened — "Modules make infrastructure reusable. State backends make it team-safe. Workspaces separate dev/prod without separate configs. A Citi DE team uses Terraform to provision S3 + Glue + Athena in under 5 minutes."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


