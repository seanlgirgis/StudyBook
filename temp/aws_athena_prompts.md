# Amazon Athena — ChatGPT Project Prompts

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Amazon Athena
Slug: aws-athena
Extra coverage required: serverless SQL on S3 — no infrastructure to manage,
cost model — per-query $5 per TB scanned and how to reduce it dramatically,
Parquet vs CSV impact on cost and speed — the single biggest lever,
partition pruning — how Hive-style partitions cut scan size,
Partition Projection — eliminate Glue catalog lookups for high-cardinality partitions,
CTAS — create table as select for materializing expensive query results,
views and named queries — reusable logic without cost,
workgroups — cost control and query isolation per team,
federated queries — Athena Data Source Connectors for RDS, DynamoDB, and custom,
Athena vs Redshift — when serverless SQL wins vs a dedicated warehouse,
Iceberg table support in Athena — time travel and MERGE on S3,
query result caching and reuse,
data engineering use cases — ad-hoc exploration, pipeline validation, cost-efficient reporting.
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug aws-athena -ChunkSize 750
```

Upload final_aws-athena.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_aws-athena.mp3` is live on R2.

```
Topic: Amazon Athena
Slug: aws-athena
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-athena.mp3
Today's date: 2026-04-25
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-athena.html
