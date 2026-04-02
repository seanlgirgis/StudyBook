# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R3\\T3-11_citi_narrative_technologies.md

SAVE AS: citi_narrative_technologies.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing the master Citi interview narrative document.

TASK: Write a structured interview story connecting every technology category to the Citi 6,000-endpoint telemetry system. This is the document to read before any Staff DE interview at Citi — it maps every technology choice to a real business reason and provides ready-to-deliver interview stories per category.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics table: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

STRUCTURE:
1. Header + System Overview — "Citi Telemetry Platform — Technologies Interview Narrative"; the 3-sentence system description to open every interview answer with: scale (6,000 endpoints, 60,000 events/sec), purpose (real-time latency + error monitoring for regulated API services), stack (Kafka → Spark → dbt → Airflow → Splunk)

2. The Citi Architecture — full ASCII system diagram showing all 11 technology categories in their operational roles; include data volumes at each stage

3. Category A — Kafka / Streaming: the problem Kafka solves at Citi (60K events/sec, ordered per endpoint, replay for regulatory audit); the architecture decision (why self-managed Kafka, not Kinesis: on-prem compliance, cross-DC replication, 7-year retention); the interview story (STAR format: 3 sentences situation + 2 sentences task + 3 sentences action + 2 sentences result); 2 numbers to memorize

4. Category B — Spark / Compute: the problem Spark solves (500K metric rows/day + streaming alerts, same team writes both); the architecture decision (why Spark over Flink: batch+streaming unification, existing PySpark expertise); interview story (STAR); 2 numbers

5. Category C — Airflow / Orchestration: the problem Airflow solves (nightly batch pipeline with 8 dependent steps, SLA by 6 AM); the architecture decision (why Airflow over Prefect: enterprise support, compliance audit trail, existing Citi footprint); interview story (STAR); 2 numbers

6. Category D — dbt / Transformation: the problem dbt solves (15 analysts writing SQL transforms with no lineage, breaking each other); the architecture decision (why dbt: version-controlled SQL, auto-lineage, CI/CD for transformations); interview story (STAR); 2 numbers

7. Category E — Databricks / Lakehouse: the problem Databricks solves (Spark on-prem cluster management overhead, ad-hoc ML notebook environment); the architecture decision (why Databricks Serverless: zero cluster management, Unity Catalog for governance); interview story (STAR); 2 numbers

8. Category F — Infrastructure / IaC: the problem Terraform solves (12 engineers provisioning cloud resources manually, no drift detection); the architecture decision (why Terraform over CDK: multi-cloud (AWS+GCP+Azure), provider-agnostic state); interview story (STAR); 2 numbers

9. Category G — Splunk / Observability: the problem Splunk solves (6,000 endpoints, 7-year regulatory retention, real-time alert correlation); the architecture decision (why Splunk over ELK: regulatory auditability, enterprise support SLA, existing Citi license); interview story (STAR); 2 numbers

10. Category H — AWS DE: the problem AWS Glue/Athena solves (ad-hoc historical query over 500M archived metric rows without standing up a cluster); the architecture decision (why Athena over Redshift for cold data: serverless, pay-per-query, S3-native); interview story (STAR); 2 numbers

11. Category I — GCP + Azure DE: the problem GCP/Azure solves (cross-cloud analytics for business units on different cloud contracts); the architecture decision (why BigQuery for analytics: columnar, serverless, no DBA); interview story (STAR); 2 numbers

12. Category J — ML Platform: the problem MLflow solves (data scientists running IsolationForest experiments with no reproducibility, no model registry); the architecture decision (why MLflow over SageMaker for experiments: local + cloud-agnostic, open source, no vendor lock-in for experiment tracking); interview story (STAR); 2 numbers

13. Category K — CI/CD for Data: the problem GitHub Actions + Great Expectations solves (dbt model merged to prod without data quality check, breaking 3 downstream dashboards); the architecture decision (why GE in CI: contract testing before merge, not after); interview story (STAR); 2 numbers

14. The Master Interview Answer — a single 90-second answer to "Tell me about a data platform you've designed or operated at scale" — weaves all 11 categories into a coherent Citi story; structured as: opening (scale) → streaming layer → batch layer → transformation → orchestration → observability → result

CONSTRAINTS:
- Valid GitHub Flavored Markdown
- Every STAR story: Situation 3 sentences, Task 2 sentences, Action 3 sentences, Result 2 sentences + one number
- Numbers to memorize per category: exactly 2, specific and memorable (e.g., "60,000 events/sec", "7-year retention")

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.


