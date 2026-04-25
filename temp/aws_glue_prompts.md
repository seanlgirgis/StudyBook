# AWS Glue — ChatGPT Project Prompts

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: AWS Glue
Slug: aws-glue
Extra coverage required: Glue Data Catalog — databases, tables, partitions, and why it is the shared metastore for Athena, Redshift Spectrum, and EMR,
crawlers — how they infer schema, when to use them vs manual table definitions, crawl scheduling,
Glue ETL jobs — Spark-based jobs, Python shell jobs, and the newer Ray runtime,
DynamicFrames vs Spark DataFrames — when DynamicFrame resolveChoice matters and when to just use DataFrames,
job bookmarks — how Glue tracks processed files for incremental loads and the traps around them,
pushdown predicates — filtering at the source before data hits the Spark executor,
Glue workflows and triggers — chaining crawlers and jobs into a pipeline,
Glue Studio visual editor vs writing scripts — what each is good for,
worker types and DPUs — G.1X vs G.2X vs G.025X for Python shell, sizing for cost vs speed,
Glue + S3 — raw to processed to curated pattern using Glue jobs,
Glue + Redshift — writing from Glue into Redshift using the JDBC connector and the Redshift connector,
Glue Schema Registry — enforcing Avro and JSON schemas across Kafka and streaming pipelines,
Glue vs EMR vs Lambda — which to reach for at different scales and use cases,
common failure patterns — bookmark corruption, driver OOM, small file explosion, partition explosion.
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug aws-glue -ChunkSize 750
```

Upload final_aws-glue.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_aws-glue.mp3` is live on R2.

```
Topic: AWS Glue
Slug: aws-glue
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-glue.mp3
Today's date: 2026-04-25
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-glue.html
