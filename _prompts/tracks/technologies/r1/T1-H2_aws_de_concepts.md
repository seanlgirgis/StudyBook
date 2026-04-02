# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R1\\T1-H2_aws_de_concepts.md

SAVE AS: aws_de_concepts.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

ROLE: You are a senior Data Engineer writing a reference guide for an engineer preparing
for Staff DE interviews at a financial institution. Precise, dense, no filler.

TASK: Generate aws_de_concepts.md — a concept reference covering the 8 core AWS DE services,
each in one tight paragraph, with Citi narrative tie-ins.

DATASET CONTEXT — do not deviate:
- Citi narrative: telemetry pipeline on AWS — S3 data lake, Glue catalog, Athena, EMR, Kinesis

STRUCTURE — produce exactly these sections in order:

# AWS Data Engineering — Core Concepts

## 1. S3 (Simple Storage Service) as Data Lake
One paragraph. Cover: object storage (not a filesystem), unlimited scale, 11 nines durability,
storage classes (Standard, Intelligent-Tiering, Glacier), S3 as the hub of the AWS DE ecosystem
(everything reads from and writes to S3), Parquet/ORC/Avro as the preferred formats,
partitioning by year/month/day for query efficiency.
End with: "Citi's telemetry lands in s3://citi-telemetry-lake/telemetry/alerts/year=2026/month=03/ — partitioned by date for Athena partition pruning."

## 2. AWS Glue Data Catalog
One paragraph. Cover: managed Hive metastore, stores database/table/column definitions,
shared by Athena, EMR, Redshift Spectrum, Glue ETL jobs, Glue Crawler auto-discovers schema
from S3 (Parquet, JSON, CSV), partitions tracked in catalog, updating catalog when new partitions arrive.
End with: "The citi_telemetry_db Glue database holds table definitions — Athena reads the schema from here without any setup."

## 3. Amazon Athena
One paragraph. Cover: serverless Presto-based SQL engine, queries S3 directly, pay $5/TB scanned,
Parquet + compression reduces cost 10x vs CSV, partition pruning eliminates scanning irrelevant data,
CTAS (CREATE TABLE AS SELECT) to write results back to S3, Athena Federated Query for non-S3 sources.
End with: "Athena query on 500K alert rows in Parquet: scans ~5MB, costs $0.00003 — same query on CSV: 50MB, $0.0003."

## 4. AWS Glue ETL
One paragraph. Cover: serverless Spark ETL service, DPU-based pricing (Data Processing Units),
job bookmarks for incremental processing, Glue DynamicFrame vs Spark DataFrame, Glue Studio visual ETL,
connection to JDBC sources (RDS, Redshift), difference from EMR (Glue = serverless, EMR = managed cluster).
End with: "A Glue ETL job reads alerts from Postgres via JDBC, converts to Parquet, writes to S3, and updates the Glue catalog — no cluster to manage."

## 5. Amazon EMR (Elastic MapReduce)
One paragraph. Cover: managed Hadoop/Spark cluster, instance groups (master, core, task), spot instances
for task nodes (up to 90% cost savings), EMR Serverless (no cluster management), EMR Steps for job submission,
bootstrap actions for software installation, EMR vs Glue (EMR = full control, Glue = serverless).
End with: "Citi's nightly 10TB telemetry aggregation runs on EMR Serverless — no cluster provisioning, auto-scaling, pay only for vCPU-hours used."

## 6. Amazon Kinesis
One paragraph. Cover: three services — Kinesis Data Streams (KDS, like Kafka), Kinesis Data Firehose
(managed delivery to S3/Redshift, no consumer code needed), Kinesis Data Analytics (SQL/Flink on streams),
KDS shard = partition (1MB/s write, 2MB/s read per shard), Firehose buffers and batches automatically.
End with: "Citi's real-time alerting: endpoint metrics → KDS → Lambda anomaly detector → Firehose → S3 → Athena — fully serverless."

## 7. AWS Lake Formation
One paragraph. Cover: governance layer on top of Glue catalog, fine-grained access control
(column-level, row-level filters), tag-based access control, centralized permissions replacing
bucket policies and IAM, cross-account data sharing, data lineage (preview).
End with: "Lake Formation ensures only the Citi risk team can query CRITICAL alerts — ops team sees the same table but severity=CRITICAL rows are filtered."

## 8. AWS vs On-Prem DE — the Staff Interview Answer
One paragraph. Cover: the key trade-offs — serverless (Athena, Glue, Kinesis Firehose) eliminates
ops burden but requires AWS expertise, cost model shifts from CapEx to OpEx, vendor lock-in is real
(Parquet/Delta Lake are portable; Glue DynamicFrame is not), egress costs are the hidden trap,
the right answer: use serverless for elasticity, keep data in open formats (Parquet/Iceberg) for portability.
End with: "Staff DE answer: 'We use Athena for ad-hoc, Glue for catalog, EMR Serverless for heavy batch — everything in Parquet so we can switch engines without migrating data.'"

---

## AWS DE Service Map

| Need | AWS Service | Alternative |
|------|-------------|-------------|
| Object storage | S3 | Azure Blob, GCS |
| Schema catalog | Glue Data Catalog | Hive metastore, Unity Catalog |
| Serverless SQL | Athena | BigQuery, Synapse Serverless |
| Serverless ETL | Glue ETL | Dataflow, Azure Data Factory |
| Managed Spark | EMR / EMR Serverless | Dataproc, Databricks |
| Event streaming | Kinesis Data Streams | Kafka, Pub/Sub, Event Hubs |
| Managed delivery | Kinesis Firehose | Kafka Connect |
| Governance | Lake Formation | Unity Catalog, Purview |

---

## Interview Flashcards

**Q: When would you choose Glue ETL over EMR?**
A: Glue when you want zero cluster management and the job is straightforward ETL — read JDBC,
transform, write Parquet. EMR when you need full Spark control (custom JARs, specific configs,
HDFS), long-running jobs, or when Glue DPU costs exceed EMR instance costs at scale.

**Q: What is the cost trap with Athena?**
A: Athena charges $5/TB scanned — on CSV files without partitioning, a query scans the entire
dataset. Fix: store data as Parquet (10x compression), partition by date/region, use partition
pruning in WHERE clauses. An unoptimized Athena query on 1TB CSV costs $5; optimized on Parquet: $0.05.

**Q: How does Kinesis Data Streams differ from SQS?**
A: KDS is a replay-capable ordered log (like Kafka) — multiple consumers read independently,
messages retained up to 7 days, ordered within a shard. SQS is a queue — one consumer per message,
no ordering guarantee across messages, no replay. Use KDS for streaming analytics; SQS for task queues.

**Q: What is Lake Formation and why is it needed on top of IAM?**
A: IAM and bucket policies can only grant/deny access to entire S3 buckets or prefixes. Lake
Formation adds column-level and row-level filtering on Glue catalog tables — essential for
regulatory compliance where different teams see different subsets of the same dataset.

CONSTRAINTS:
- Each concept: exactly one paragraph, 4-6 sentences, no bullets inside
- Citi tie-in is the last sentence of each paragraph
- Tables: valid GFM pipe tables
- No filler phrases

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.


