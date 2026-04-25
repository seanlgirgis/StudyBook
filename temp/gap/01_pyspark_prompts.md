# PySpark — ChatGPT Project Prompts

Priority: 🔴 Critical — Toyota gap #1

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: PySpark for Data Engineers
Slug: pyspark
Extra coverage required: Spark architecture — driver, executors, cluster manager, DAG scheduler,
RDDs vs DataFrames vs Datasets — why DataFrames win for data engineering,
lazy evaluation — nothing runs until an action, and why that matters for performance,
transformations vs actions — the distinction and common mistakes,
partitioning — how Spark splits data, default parallelism, repartition vs coalesce,
shuffles — what triggers a shuffle, why they're expensive, how to minimize them,
joins — broadcast join vs sort-merge join — when each applies and the broadcast threshold,
data skew — what it is, how to detect it in the Spark UI, salting as a remedy,
Adaptive Query Execution (AQE) — how Spark 3 auto-optimizes at runtime,
UDFs — why they're slow, when to use them vs built-in functions,
reading and writing Parquet from S3 — partition pruning, predicate pushdown, schema evolution,
PySpark on EMR vs Glue vs Databricks — which to reach for and when,
performance tuning — memory configuration, executor sizing, spark.sql.shuffle.partitions,
common OOM errors — driver OOM vs executor OOM — causes and fixes,
PySpark for manufacturing data — processing high-volume sensor telemetry at scale.
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug pyspark -ChunkSize 750
```

Upload final_pyspark.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_pyspark.mp3` is live on R2.

```
Topic: PySpark for Data Engineers
Slug: pyspark
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_pyspark.mp3
Today's date: 2026-04-25
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\pyspark.html
