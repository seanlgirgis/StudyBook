# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R3\\T3-9_technologies_qa_master.md

SAVE AS: technologies_qa_master.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing the master Q&A reference document for Staff DE interviews.

TASK: Consolidate the highest-signal Q&A pairs across all 11 technology categories into one master document. This is the single document to read the night before a Staff DE interview. Prioritize questions that appear in real interviews and distinguish Staff-level answers from senior-level answers.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics table: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

STRUCTURE:
1. Header — "Technologies Master Q&A — Staff DE Interview Reference"; note: "5 best questions per category = 55 total; every answer ends with a Citi framing sentence"
2. Section A — Kafka / Streaming (5 Q&A): ISR + acks tradeoff at scale, exactly-once semantics implementation, consumer group rebalancing prevention, partition sizing for 60K events/sec, Kafka vs Kinesis decision
3. Section B — Spark / Compute (5 Q&A): catalyst optimizer + physical plan, shuffle vs broadcast join at 500K rows, AQE adaptive partitioning, Structured Streaming watermark design, Spark OOM diagnosis steps
4. Section C — Airflow / Orchestration (5 Q&A): idempotency design for nightly pipeline, CeleryExecutor vs KubernetesExecutor, SLA miss detection + response, dynamic DAG generation pattern, backfill safety
5. Section D — dbt / Transformation (5 Q&A): incremental model late-arriving data handling, snapshot vs incremental for SCD2, dbt test coverage strategy, CI/CD for dbt in production, semantic layer vs BI tool logic
6. Section E — Databricks / Lakehouse (5 Q&A): Delta Lake ACID mechanics, time travel cost and vacuum conflict, Z-order vs partitioning for query pruning, Delta vs Iceberg decision, Unity Catalog governance model
7. Section F — Infrastructure (5 Q&A): Terraform state locking in a team, Spark on Kubernetes persistent volume design, K8s resource quota for DE workloads, IaC testing strategy, multi-environment Terraform workspace pattern
8. Section G — Splunk / Observability (5 Q&A): HEC vs forwarder tradeoff at 60K events/sec, SPL performance optimization, index vs sourcetype design, license throttling prevention, Splunk vs ELK decision
9. Section H — AWS DE (5 Q&A): Glue DPU cost vs EMR for 500K rows, Athena partition projection pattern, Lake Formation row-level security, Kinesis shard sizing, S3 data lake governance
10. Section I — GCP + Azure DE (5 Q&A): Dataflow autoscaling vs Spark for streaming, BigQuery partitioning + clustering strategy, Pub/Sub ordering guarantee, Azure Synapse vs Databricks, multi-cloud data contract design
11. Section J — ML Platform (5 Q&A): model registry vs artifact store distinction, training-serving skew detection, feature store online vs offline latency, MLflow experiment reproducibility, SageMaker vs Vertex AI decision
12. Section K — CI/CD for Data (5 Q&A): data contract testing in CI pipeline, Great Expectations checkpoint design, dbt CI run cost reduction, blue-green pipeline deployment, flaky data test management

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 4-6 sentences, precise, no filler, Staff-level depth (not entry-level definitions)
- Every answer must end with a Citi framing sentence
- Valid GitHub Flavored Markdown
- Each section must have exactly 5 Q&A pairs

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.


