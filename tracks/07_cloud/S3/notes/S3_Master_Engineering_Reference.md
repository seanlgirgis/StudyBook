# Amazon S3 — Master Engineering Reference
> **Purpose:** refresh
> **Audience:** Senior Data Engineer preparing for Lead DE interview  
> **Time to read:** 30–40 minutes  
> **Last updated:** 2026-04-13

---

## Table of Contents
1. [What S3 Actually Is](#1-what-s3-actually-is)
2. [Core Concepts](#2-core-concepts)
3. [Storage Classes](#3-storage-classes)
4. [Data Lake Patterns](#4-data-lake-patterns)
5. [Partitioning Strategy](#5-partitioning-strategy)
6. [Security Model](#6-security-model)
7. [Performance at Scale](#7-performance-at-scale)
8. [S3 + Glue Integration](#8-s3--glue-integration)
9. [S3 + Redshift Integration](#9-s3--redshift-integration)
10. [S3 + ECS/EC2 Pipelines](#10-s3--ecsec2-pipelines)
11. [Event Notifications and Pipeline Triggers](#11-event-notifications-and-pipeline-triggers)
12. [Consistency Model](#12-consistency-model)
13. [10 Interview Questions and Answers](#13-10-interview-questions-and-answers)
14. [Your Story Angles](#14-your-story-angles)

---

## 1. What S3 Actually Is

S3 is **object storage** — not a file system, not a database. Think of it as an infinitely large key-value store where:
- The **key** is the full path: `s3://my-bucket/raw/2026/04/13/telemetry.json`
- The **value** is the file content (any format, any size)
- There are no real "folders" — the `/` in the key is just a naming convention

**Why this matters in interviews:**  
When someone asks "how does S3 work under the hood," the answer is: flat namespace, keys that look like paths, metadata attached to each object. The folder illusion is just the console making it friendly.

**S3 vs other storage:**

| Storage Type | Example | Best For |
|---|---|---|
| Object | S3 | Data lakes, backups, pipeline staging |
| Block | EBS | Databases, OS volumes |
| File | EFS | Shared file systems across EC2 |
| Warehouse | Redshift | Structured analytics queries |

**Helpful Addition for Learners:**  
S3 is built on a massively distributed system with automatic replication across multiple Availability Zones (by default) for 99.999999999% (11 9’s) durability. This design allows virtually unlimited scale without you managing any underlying infrastructure.

---

## 2. Core Concepts

### Buckets
- Global namespace — bucket names must be **globally unique** across all AWS accounts
- Tied to a **region** — data stays in that region unless you replicate
- Flat container — no true hierarchy, just key prefixes

### Objects
- Max object size: **5 TB**
- Each object = data + metadata (system metadata like `Content-Type` + custom metadata)
- Identified uniquely by: **bucket + key + version ID** (if versioning enabled)

### Keys
- The full "path" of an object
- Example: `telemetry/raw/year=2026/month=04/day=13/host=srv001/data.parquet`
- Key design directly impacts **Glue performance**, **Athena query cost**, and **request throughput**

### Versioning
- Once enabled on a bucket, every PUT creates a new version — old versions preserved
- DELETE creates a **delete marker**, doesn't actually remove the object
- Useful for: audit trails, accidental deletion protection, pipeline replay

### Lifecycle Policies
- Rules that automatically transition objects between storage classes or expire them
- Example rule: 
  - After 30 days → move raw telemetry to S3-IA
  - After 90 days → move to Glacier
  - After 365 days → delete
- Critical for cost management on large data lakes

**Helpful Addition for Learners:**  
Lifecycle policies can also include rules for transitioning to S3 Intelligent-Tiering automatically or expiring incomplete multipart uploads after a set number of days to avoid storage waste.

---

## 3. Storage Classes

Understanding when to use each class is a common interview question.

| Class | Access Pattern | Retrieval | Cost | Use Case |
|---|---|---|---|---|
| **S3 Standard** | Frequent | Milliseconds | Higher | Active pipeline data, hot landing zone |
| **S3 Intelligent-Tiering** | Unknown/changing | Milliseconds | Auto-optimized | Data with unpredictable access |
| **S3 Standard-IA** | Infrequent | Milliseconds | Lower storage, retrieval fee | Processed data accessed occasionally |
| **S3 One Zone-IA** | Infrequent, non-critical | Milliseconds | Cheapest IA | Reproducible data, dev/test |
| **S3 Glacier Instant** | Rare, needs fast access | Milliseconds | Very low | Compliance archives |
| **S3 Glacier Flexible** | Rare | Minutes–hours | Very low | Long-term backups |
| **S3 Glacier Deep Archive** | Almost never | 12 hours | Lowest | 7-year regulatory retention |

**Helpful Addition for Learners:**  
As of 2026, S3 Express One Zone is also available for workloads needing single-digit millisecond latency and high throughput (ideal for ML training or real-time analytics). It is not covered in the original table but is worth evaluating for performance-critical hot paths.

### The Rule of Thumb for Pipelines
```
Landing zone (hot, actively written)     → S3 Standard
Processed/curated (read occasionally)    → S3 Standard-IA or Intelligent-Tiering
Archive (compliance, rarely touched)     → Glacier
```

---

## 4. Data Lake Patterns

This is the most important section for your interview.  will care about how you design an S3-based data platform.

### The Three-Zone Pattern

```
s3://company-datalake/
    ├── raw/           ← Landing zone: exactly as received, never modified
    ├── processed/     ← Cleaned, validated, transformed
    └── curated/       ← Business-ready, optimized for analytics
```

**Why three zones matter:**
- **Raw** = source of truth. If processing goes wrong, you replay from raw. Never delete raw.
- **Processed** = cleansed, deduplicated, type-cast. Glue jobs write here.
- **Curated** = aggregated, partitioned optimally for query patterns. Redshift or Athena reads from here.

### Your Parallel
At your previous role your pipeline flow was:
```
BMC TrueSight telemetry → S3 raw/ → Glue ETL → S3 processed/ → Redshift → Forecasting models
```
This is exactly the three-zone pattern. You lived it — just name it properly in the interview.

### Naming Conventions That Matter
```
s3://capacity/raw/source=bmc-truesight/year=2026/month=04/day=13/
s3://capacity/processed/entity=server/year=2026/month=04/
s3://capacity/curated/domain=capacity/report=monthly-utilization/
```

**Helpful Addition for Learners:**  
A common extension is a fourth “analytics” or “consumption” zone for materialized views or aggregated tables optimized specifically for BI tools or ML feature stores. This keeps the curated zone focused on reusable business entities.

---

## 5. Partitioning Strategy

**Partitioning = how you organize key prefixes to make queries faster and cheaper.**

### Hive-Style Partitioning
The standard pattern — used by Glue, Athena, Spark, and most analytics tools:
```
s3://bucket/table/year=2026/month=04/day=13/hour=10/filename.parquet
```
- Glue crawlers automatically detect this pattern and build the catalog
- Athena uses partition pruning — only scans folders matching your WHERE clause
- Result: **lower cost, faster queries**

### Choosing Partition Keys
Ask: "What columns appear most in my WHERE clauses?"

```sql
-- If queries filter by date:
WHERE year='2026' AND month='04'        → partition by year/month

-- If queries filter by server:
WHERE host='srv001'                     → partition by host

-- If queries filter by both:
WHERE year='2026' AND region='us-east'  → partition by year/region
```

### Over-Partitioning Anti-Pattern
Don't partition by high-cardinality columns like `host_id` if you have 10,000 hosts:
- Creates 10,000 folders with tiny files
- Glue metadata overhead kills performance
- **Small files problem**: many 1KB files vs. few 128MB files — always prefer fewer larger files

### The Small Files Problem
Parquet files under ~128MB are inefficient. Fix with:
- **Compaction jobs**: Glue job that reads many small files → writes fewer large files
- **Coalesce in Spark**: `df.coalesce(10).write.parquet(path)`

**Helpful Addition for Learners:**  
Aim for Parquet files between 128MB and 1GB for optimal performance with most query engines. Tools like AWS Glue’s “compact” transformation or Apache Iceberg / Delta Lake can help manage partitioning and small-file issues more elegantly in modern data lakes.

---

## 6. Security Model

### The "Private By Default" Rule
Every bucket and object in S3 is **private by default**. Access must be explicitly granted. This is the first thing to say in any security discussion.

### Four Layers of Access Control

```
1. IAM Policies          → Who (user/role) can do what across AWS
2. Bucket Policies       → What actions are allowed on this specific bucket
3. S3 Access Points      → Named endpoints with their own policies (for shared datasets)
4. Block Public Access   → Nuclear override — blocks ALL public access regardless of other policies
```

### IAM Role vs Bucket Policy — When to Use Which

| Scenario | Use |
|---|---|
| EC2/ECS container needs to read S3 | IAM Role attached to EC2/ECS task |
| Glue job needs to read/write S3 | IAM Role attached to Glue job |
| Cross-account access | Bucket Policy |
| Restrict a specific prefix | Bucket Policy with Condition on `s3:prefix` |

### Encryption
- **SSE-S3**: AWS manages keys, transparent, no cost — default since 2023
- **SSE-KMS**: You manage keys via AWS KMS — auditable, required for compliance (PCI, SOX)
- **Client-side**: You encrypt before upload — maximum control, maximum complexity

### For Financial Services Specifically
Financial services = SSE-KMS + bucket policies + no public access. They will ask about this. Answer:
> "All S3 buckets had Block Public Access enabled at the account level. Data at rest used SSE-KMS so every access was auditable through CloudTrail. IAM roles were scoped to least-privilege — Glue jobs had read on raw/, write on processed/ only."

**Helpful Addition for Learners:**  
Always enable S3 Object Lock (WORM) for regulatory data requiring immutability. Combine with AWS Macie for automated sensitive data discovery and S3 Inventory for auditing large-scale bucket contents.

---

## 7. Performance at Scale

### Request Rate Limits
S3 supports:
- **3,500 PUT/COPY/POST/DELETE** requests per second per prefix
- **5,500 GET/HEAD** requests per second per prefix

If you exceed this, you get throttling (503 errors). Fix: **spread requests across multiple prefixes**.

### Prefix Randomization (Old Pattern — Pre-2018)
Before 2018, S3 partitioned internally by prefix. You had to randomize:
```
# Old: bad — all traffic hits one prefix
s3://bucket/2026/04/13/file.parquet

# Old: good — spread across prefixes  
s3://bucket/a3f2/2026/04/13/file.parquet
s3://bucket/b7d1/2026/04/13/file.parquet
```
**Post-2018: S3 auto-scales per prefix. You no longer need to randomize for performance.** But knowing the history shows depth.

### Multipart Upload
For objects > 100MB, use multipart upload:
- Uploads parts in parallel → faster
- If one part fails, retry just that part
- Required for objects > 5GB

### Transfer Acceleration
Routes uploads through AWS CloudFront edge locations → faster for geographically distributed sources.

**Helpful Addition for Learners:**  
Monitor with CloudWatch metrics (BucketSizeBytes, NumberOfObjects, 4xx/5xx errors) and set alarms on high request rates. For extreme throughput, consider S3 Express One Zone buckets which support hundreds of thousands of requests per second.

---

## 8. S3 + Glue Integration

This is your core stack. Know this cold.

### How Glue Uses S3

```
S3 (data store)
    ↓
Glue Crawler (scans S3, infers schema, writes to Data Catalog)
    ↓
Glue Data Catalog (metadata: table name, schema, partition info, S3 location)
    ↓
Glue ETL Job (reads from catalog, transforms, writes back to S3 or Redshift)
    ↓
Athena / Redshift Spectrum (queries using catalog metadata)
```

### Glue Crawler
- Scans S3 paths, detects Hive-style partitions, infers schema from Parquet/JSON/CSV
- Creates/updates tables in the Glue Data Catalog
- Run on schedule or triggered by S3 event notification
- **Key setting**: `TableThreshold` — how many tables created per crawler run

### Glue ETL Job
- Runs PySpark or Python shell
- Reads from S3 via catalog or direct path
- Transforms data (cleanse, join, aggregate)
- Writes back to S3 (processed/ or curated/) in Parquet format
- **DynamicFrame** vs **DataFrame**: DynamicFrame handles schema inconsistencies, DataFrame is standard Spark

### Connection to Your Work
At your previous role your Glue jobs:
- Read raw telemetry from `s3://raw/` (BMC TrueSight dumps)
- Transformed and typed the data (timestamps, numeric conversions)
- Wrote Parquet to `s3://processed/`
- Redshift then loaded from `s3://processed/` via COPY command

**Helpful Addition for Learners:**  
Use Glue Job bookmarks to avoid reprocessing the same data on reruns. Enable Spark UI logging for troubleshooting long-running jobs, and consider AWS Glue Data Quality rules to validate data before writing to the processed zone.

---

## 9. S3 + Redshift Integration

### COPY Command — The Primary Load Mechanism
```sql
COPY capacity_metrics
FROM 's3://capacity/processed/entity=server/year=2026/month=04/'
IAM_ROLE 'arn:aws:iam::123456789:role/RedshiftS3Role'
FORMAT AS PARQUET;
```
- Massively parallel — Redshift nodes read S3 files in parallel
- Parquet is preferred format (columnar, compressed, schema embedded)
- IAM Role must have `s3:GetObject` and `s3:ListBucket` permissions

### UNLOAD Command — Export From Redshift to S3
```sql
UNLOAD ('SELECT * FROM monthly_utilization WHERE year=2026')
TO 's3://capacity/curated/exports/'
IAM_ROLE 'arn:aws:iam::123456789:role/RedshiftS3Role'
FORMAT AS PARQUET
PARALLEL ON;
```

### Redshift Spectrum
- Query S3 data directly without loading into Redshift
- Uses Glue Data Catalog for schema
- Great for: querying historical data in S3 without paying for Redshift storage

### Distribution Styles (Redshift Performance)
When loading from S3 into Redshift, table design matters:
- `EVEN` — round-robin distribution, good for large tables with no clear join key
- `KEY` — distribute on a column, good for join-heavy queries
- `ALL` — copy to every node, good for small dimension tables

**Helpful Addition for Learners:**  
For very large datasets, use the COPY command with the MANIFEST option to explicitly list files and improve reliability. Also consider Redshift’s AUTO distribution and sort key optimization features introduced in recent years for hands-off tuning.

---

## 10. S3 + ECS/EC2 Pipelines

### How Your Containers Worked

```
ECS Task (Python ETL container)
    ├── Reads config from S3 or environment
    ├── Pulls raw data from S3 raw/
    ├── Processes (pandas, scikit-learn, Prophet)
    └── Writes output to S3 processed/ or pushes to Redshift
```

### IAM Role for ECS Tasks
ECS tasks use **Task Roles** — an IAM role attached to the task definition:
```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject", "s3:ListBucket"],
  "Resource": [
    "arn:aws:s3:::capacity",
    "arn:aws:s3:::capacity/*"
  ]
}
```
Never hardcode AWS credentials in containers. Always use task roles.

### boto3 — Python SDK for S3
```python
import boto3

s3 = boto3.client('s3')

# Read file
obj = s3.get_object(Bucket='capacity', Key='raw/2026/04/13/data.json')
data = obj['Body'].read().decode('utf-8')

# Write file
s3.put_object(
    Bucket='capacity',
    Key='processed/2026/04/13/data.parquet',
    Body=parquet_bytes
)

# List files with prefix
response = s3.list_objects_v2(Bucket='capacity', Prefix='raw/2026/04/13/')
files = [obj['Key'] for obj in response.get('Contents', [])]
```

**Helpful Addition for Learners:**  
Use boto3’s `upload_fileobj()` and `download_fileobj()` for memory-efficient handling of large files. Enable server-side encryption explicitly in put_object calls when needed, and consider using S3 Transfer Manager for resumable multipart uploads in production code.

---

## 11. Event Notifications and Pipeline Triggers

S3 can trigger downstream systems when objects are created, deleted, or restored.

### Supported Targets
- **AWS Lambda** — run a function when a file lands
- **Amazon SQS** — queue the event for a worker to process
- **Amazon SNS** — fan out notifications to multiple subscribers
- **Amazon EventBridge** — route events to any AWS service

### Pipeline Trigger Pattern
```
New telemetry file lands in s3://raw/
    → S3 Event Notification
    → SQS Queue
    → ECS Task polls queue
    → Task processes file → writes to s3://processed/
    → Glue Crawler triggered → updates Data Catalog
    → Redshift COPY job runs
```

### EventBridge (Modern Approach)
More flexible than direct S3 notifications:
```json
{
  "source": ["aws.s3"],
  "detail-type": ["Object Created"],
  "detail": {
    "bucket": {"name": ["capacity"]},
    "object": {"key": [{"prefix": "raw/"}]}
  }
}
```
Route to Step Functions, ECS, Glue — anything.

**Helpful Addition for Learners:**  
Filter events using S3 EventBridge rules on specific suffixes (e.g., only .parquet files) to reduce noise. For high-volume buckets, prefer SQS over direct Lambda to avoid throttling and enable dead-letter queues for failed processing.

---

## 12. Consistency Model

S3 provides **strong read-after-write consistency** for all operations (since December 2020).

What this means practically:
- You PUT a file → immediately GET it → you see the new file ✅
- You DELETE a file → immediately LIST the bucket → file is gone ✅
- Two writers PUT to the same key simultaneously → **last writer wins** (timestamp-based)

**Before December 2020:** S3 had eventual consistency for overwrites and deletes. You may see this mentioned in older articles — it no longer applies.

**Why this matters for pipelines:**
- You can safely read a file immediately after writing it
- No need for sleep/retry loops waiting for consistency
- But: for concurrent writes to the same key, design your pipeline to avoid races

**Helpful Addition for Learners:**  
List operations are now also strongly consistent. For multi-object atomicity needs, consider using S3 Batch Operations or higher-level frameworks like Apache Iceberg that provide ACID transactions on top of S3.

---

## 13. Ten Interview Questions and Answers

### Q1: "How would you design an S3-based data lake for a high-volume telemetry pipeline?"

> "I'd use a three-zone pattern — raw, processed, curated. Raw is the immutable landing zone, exactly as received. Processed is cleansed and transformed by Glue ETL jobs. Curated is optimized for the query patterns — Hive-partitioned Parquet files that Redshift or Athena can read efficiently. S3 lifecycle policies move data to Standard-IA after 30 days and Glacier after a year. Glue crawlers maintain the Data Catalog so everything is discoverable."

---

### Q2: "What's your approach to partitioning data in S3?"

> "I partition by the columns that appear most in query WHERE clauses — typically date (year/month/day) and sometimes an entity like region or service. I use Hive-style prefixes so Glue and Athena can prune partitions automatically. I also watch for the small files problem — if a job generates thousands of tiny files I add a compaction step to merge them into ~128MB Parquet files. Over-partitioning on high-cardinality columns like host ID is an anti-pattern I actively avoid."

---

### Q3: "How do you secure S3 buckets in a financial services environment?"

> "Private by default, Block Public Access enabled at the account level. Data at rest encrypted with SSE-KMS so every key usage is auditable through CloudTrail. IAM roles scoped to least-privilege — Glue jobs get read on raw, write on processed only. Bucket policies for cross-account access. S3 Access Points for shared datasets where multiple teams need different scoped access. And S3 Object Lock for compliance data that can't be modified or deleted."

---

### Q4: "What's the difference between IAM policies and bucket policies?"

> "IAM policies are attached to principals — users, roles, groups. They define what that principal can do across all of AWS. Bucket policies are attached to the bucket itself and define who can access that specific bucket. For most pipeline use cases I use IAM roles on EC2 and ECS tasks. Bucket policies come in when I need cross-account access or want to restrict access to specific prefixes regardless of what IAM allows."

---

### Q5: "How does Glue interact with S3?"

> "Glue crawlers scan S3 paths, detect Hive-style partitions, infer schema from Parquet or JSON files, and write table definitions to the Glue Data Catalog. ETL jobs then read from the catalog — they don't need to know the S3 path directly. Jobs transform the data and write back to S3 in Parquet format. The catalog makes everything discoverable to Athena, Redshift Spectrum, and other consumers without duplicating metadata."

---

### Q6: "How do you load data from S3 into Redshift efficiently?"

> "The COPY command — it's massively parallel. Redshift's compute nodes read S3 files in parallel, so the more files you have the faster it loads. I use Parquet format because it's columnar and compressed — much faster than CSV. I make sure the IAM role attached to the Redshift cluster has GetObject and ListBucket on the source S3 path. For very large loads I also tune the distribution style and sort keys on the target table to match the query patterns."

---

### Q7: "What is S3 Intelligent-Tiering and when would you use it?"

> "Intelligent-Tiering automatically moves objects between Frequent Access and Infrequent Access tiers based on access patterns — no retrieval fee, just a small monitoring fee per object. I'd use it for data where access patterns are unpredictable or change over time — like historical reports that are accessed heavily after generation then rarely touched. For data with known patterns I'd use explicit lifecycle policies instead — it's more predictable on cost."

---

### Q8: "How do you trigger a pipeline when a new file lands in S3?"

> "S3 Event Notifications sent to SQS is the reliable pattern for pipeline triggers — the queue decouples the producer from the consumer and handles bursts gracefully. The downstream ECS task or Lambda polls the queue and processes files as they arrive. For more complex routing I use EventBridge — it lets me pattern-match on bucket name and key prefix and route to Step Functions or Glue jobs. The key is idempotency — the consumer should handle duplicate events gracefully."

---

### Q9: "What is the S3 consistency model?"

> "Since December 2020 S3 provides strong read-after-write consistency for all operations. A file you just wrote is immediately readable — no eventual consistency delays for normal operations. The one nuance is concurrent writes to the same key — last writer wins based on timestamp. In pipeline design I avoid concurrent writes to the same key by including unique identifiers like timestamps or UUIDs in the file names."

---

### Q10: "Tell me about a time you used S3 in a production data pipeline."

> Use **Story 4 from your interview prep file.**  
> Previous role → hybrid platform → S3 landing zone → Glue ETL → Redshift forecasting workloads → ECS containerized Python jobs. 6,000+ endpoints, 8 years production, Oracle alongside for existing reporting.

---

## 14. Your Story Angles

Map your real experience to the concepts in this doc:

| Concept | Your Experience |
|---|---|
| Three-zone data lake | Raw telemetry → processed → Redshift curated |
| Glue ETL | Transformed BMC TrueSight telemetry, type-cast, deduped |
| Redshift COPY | Loaded processed Parquet files into forecasting tables |
| ECS containers | Containerized Python ETL and forecasting jobs |
| S3 as landing zone | 6,000+ endpoints dumping telemetry to S3 raw/ |
| Lifecycle policies | Archived historical telemetry after retention period |
| IAM roles | ECS task roles scoped to specific S3 prefixes |
| SSE-KMS | Financial data encrypted, auditable via CloudTrail |
| Event notifications | File landing triggered downstream Glue crawler |
| Partitioning | year/month/day + source system prefix for query efficiency |

**Helpful Addition for Learners:**  
When telling stories, quantify impact where possible (e.g., “reduced query costs by 40% through better partitioning” or “handled 5x data volume growth without increasing infrastructure spend”). This makes answers more memorable and demonstrates business value.

---

## Quick Reference Cheat Sheet

```
Bucket         = globally unique container, tied to a region
Key            = full object path (the "filename")
Prefix         = simulated folder (just part of the key)
Partition      = Hive-style key prefix for query pruning
COPY           = load from S3 to Redshift (parallel, fast)
UNLOAD         = export from Redshift to S3
Task Role      = IAM role for ECS containers (never hardcode credentials)
Block Public   = account-level switch, overrides everything
SSE-KMS        = encryption with auditable key usage
Crawler        = Glue tool that infers schema and builds Data Catalog
DynamicFrame   = Glue's schema-flexible version of Spark DataFrame
Compaction     = merging small files into larger ones for performance
```

**Helpful Addition for Learners (Quick Reference):**  
Additional modern tip: Consider adopting table formats like Apache Iceberg or Delta Lake on S3 for features such as schema evolution, time travel, and ACID transactions while keeping all data in open Parquet files.

---

*Feed this file to NotebookLM and ask the hosts to focus on sections 4, 5, 8, 9, and 13 for the audio overview.*