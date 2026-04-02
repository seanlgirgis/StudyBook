# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R1\\T1-I3_multicloud_concepts.md

SAVE AS: multicloud_concepts.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

ROLE: You are a senior Data Engineer writing a reference guide for an engineer preparing
for Staff DE interviews at a financial institution. Precise, dense, no filler.

TASK: Generate multicloud_concepts.md — a concept reference covering the cross-cloud DE service
landscape, decision frameworks, and portability strategies for Staff DE interviews.

DATASET CONTEXT — do not deviate:
- Citi narrative: AWS primary in Americas, Azure primary in EMEA, GCP for ML/BigQuery workloads

STRUCTURE — produce exactly these sections in order:

# Multicloud Data Engineering — Concepts

## 1. Why Multicloud Exists
One paragraph. Cover: enterprise contracts (AWS vs Azure vs GCP pricing), regulatory requirements
(data residency in EMEA → Azure, Americas → AWS), M&A (acquired company on different cloud),
best-of-breed (BigQuery ML vs SageMaker), avoiding vendor lock-in, operational complexity as the
real cost of multicloud.
End with: "Citi operates AWS in Americas, Azure in EMEA — not by choice of elegance but by organizational and regulatory reality."

## 2. The Universal Data Lake Pattern
One paragraph. Cover: object storage + open table format = portable data layer, Parquet on S3/ADLS/GCS
reads identically from Spark, Athena, BigQuery, Synapse; Apache Iceberg adds ACID on any cloud;
the pattern: store data in open format, swap the query engine without migrating data.
End with: "Citi's telemetry in Parquet+Iceberg on S3 can be queried by Athena today and Snowflake tomorrow — no data movement required."

## 3. Streaming: Kafka vs Kinesis vs Pub/Sub vs Event Hubs
One paragraph. Cover: all four implement publish-subscribe with partitions/shards and consumer groups,
Kafka = portable (runs anywhere, self-managed or Confluent), Kinesis = AWS-native serverless,
Pub/Sub = GCP-native (no partition management), Event Hubs = Azure-native (Kafka-protocol compatible),
porting: Kafka protocol compatibility means confluent-kafka client works against Event Hubs directly.
End with: "Migrating from Kafka to Event Hubs: change the bootstrap.servers to Event Hubs endpoint — same client code, no application changes."

## 4. Batch Compute: EMR vs Dataproc vs Synapse Spark vs Databricks
One paragraph. Cover: all run Apache Spark, differences are in management overhead and ecosystem,
EMR = deepest AWS integration (S3, Glue, Lake Formation), Dataproc = fastest cluster start (90s),
Synapse Spark = integrated with Synapse workspace (SQL + Spark together), Databricks = cloud-agnostic
(runs on AWS/Azure/GCP), Delta Lake = Databricks default format on all three clouds.
End with: "Staff DE answer for 'cloud-agnostic Spark': Databricks — same notebooks, same Delta tables, same job configs across AWS/Azure/GCP."

## 5. Serverless SQL: Athena vs BigQuery vs Synapse Serverless
One paragraph. Cover: all three query files in object storage without provisioning clusters,
BigQuery = stores data internally (not S3/GCS — stored in Colossus), Athena = queries S3 directly
(you manage format), Synapse Serverless = queries ADLS Gen2 via OPENROWSET, pricing all $5/TB scanned,
BigQuery has 1TB/month free, Athena has no free tier.
End with: "Staff DE selection: AWS-first → Athena, GCP-first → BigQuery, Azure-first → Synapse Serverless. Avoid mixing — cross-cloud egress costs are the trap."

## 6. Orchestration Across Clouds
One paragraph. Cover: Airflow runs anywhere and can submit jobs to any cloud (via operators for AWS,
GCP, Azure), Airflow = cloud-agnostic orchestrator of choice for multicloud pipelines, managed
options: MWAA (AWS), Cloud Composer (GCP), Azure Managed Airflow (preview), Prefect/Dagster also
cloud-agnostic, avoid cloud-native orchestrators (Step Functions, Cloud Workflows) for multicloud work.
End with: "Citi's orchestration: one Airflow deployment on AWS orchestrates jobs that run on AWS EMR, GCP Dataproc, and Azure Synapse — operators handle the cloud-specific API calls."

## 7. Governance Across Clouds
One paragraph. Cover: no cloud-native governance solution spans multiple clouds, options: Apache Atlas
(open-source, self-hosted), Alation/Collibra (vendor, cloud-agnostic), Unity Catalog (Databricks,
cross-cloud when Databricks is the platform), Microsoft Purview (Azure-first but has connectors),
the real answer: standardize on one data catalog and build connectors.
End with: "Citi's governance reality: Microsoft Purview for Azure assets, Lake Formation for AWS — two systems, one GRC team reconciling them."

## 8. Egress Costs — The Hidden Multicloud Tax
One paragraph. Cover: ingress to any cloud is free, egress (data leaving a cloud) is $0.08-0.09/GB,
cross-region within a cloud is $0.01-0.02/GB, egress kills naive multicloud architectures where
data flows between clouds continuously, the correct pattern: process data where it lives,
move only aggregated/summarized results.
End with: "Moving 1TB of raw telemetry from AWS to Azure for Azure ML costs ~$90 in egress. Solution: run ML on AWS SageMaker where the data lives, move only model artifacts to Azure."

---

## Master Service Comparison

| Function | AWS | Azure | GCP | Cloud-Agnostic |
|----------|-----|-------|-----|----------------|
| Object storage | S3 | ADLS Gen2 / Blob | Cloud Storage | MinIO (self-hosted) |
| Data lake format | Delta/Iceberg/Parquet | Delta/Iceberg/Parquet | Delta/Iceberg/Parquet | Apache Iceberg |
| Serverless SQL | Athena | Synapse Serverless | BigQuery | Trino / DuckDB |
| Managed Spark | EMR | Synapse Spark | Dataproc | Databricks |
| Streaming | Kinesis | Event Hubs | Pub/Sub | Apache Kafka |
| ETL/pipeline | Glue ETL | Data Factory | Dataflow | Apache Beam |
| Orchestration | MWAA | Managed Airflow | Cloud Composer | Airflow (self-hosted) |
| Governance | Lake Formation | Purview | Dataplex | Unity Catalog / Collibra |
| Data warehouse | Redshift | Synapse Dedicated | BigQuery | Snowflake |

---

## Interview Flashcards

**Q: How would you design a pipeline that works across AWS and Azure?**
A: Store data in Apache Iceberg on S3 (or replicated to ADLS Gen2). Use Airflow as the
cloud-agnostic orchestrator. Use Spark (EMR or Synapse) for processing — same Spark code runs on both.
Use cloud-native SQL only for ad-hoc (Athena on AWS, Synapse Serverless on Azure). Avoid cloud-specific
operators in core business logic.

**Q: When does multicloud make sense and when doesn't it?**
A: Makes sense: regulatory data residency requirements, M&A integration, best-of-breed (BigQuery ML
+ AWS EMR). Doesn't make sense: if it's a pure cost play — egress costs eliminate savings.
The operational complexity of multicloud (two IAM systems, two observability stacks, two on-call runbooks)
is real and underestimated.

**Q: What is the cheapest way to query data across clouds?**
A: Don't. Process data where it lives and move only the results. If unavoidable: use Snowflake
(cross-cloud warehouse with data stored in each cloud's object storage via external tables) or
Databricks (runs on any cloud, reads from that cloud's storage natively).

CONSTRAINTS:
- Each concept: exactly one paragraph, 4-6 sentences, no bullets inside
- Citi tie-in is the last sentence of each paragraph
- Tables: valid GFM pipe tables
- No filler phrases

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.


