# Spark Review Lanes

Purpose:
Explain how to study the Course 11 and expanded Spark material without getting
lost in one giant QA file.

## Lane 1 - Course 11 PySpark Foundation

Source:
QA_01_1000ft_pyspark_opening.md

Use for:
- DataCamp Course 11 review
- Wipro sprint foundation
- Spark/PySpark basics
- DataFrames
- transformations/actions
- Spark SQL
- UDFs
- RDD basics
- aggregations
- explain/cache/broadcast
- safe interview claims

## Lane 2 - Production Runtime Architecture

Source:
Spark.Study.md

Use for:
- spark-submit
- Airflow
- Databricks Jobs
- EMR Steps
- Glue Jobs
- YARN
- Kubernetes
- driver/executors in production
- storage/catalog/orchestration architecture

## Lane 3 - Delta Lakehouse

Source:
Spark.Study.md

Use for:
- Parquet vs Delta
- _delta_log
- ACID
- schema enforcement/evolution
- time travel
- MERGE/upsert
- CDC
- idempotency
- medallion architecture
- Bronze/Silver/Gold
- quarantine/error tables

## Lane 4 - Performance and Maintenance

Source:
Spark.Study.md

Use for:
- partitions
- small-file problem
- OPTIMIZE
- VACUUM
- Z-ordering
- data skipping
- partition pruning
- logical vs physical delete

## Lane 5 - Streaming

Source:
Spark.Study.md

Use for:
- batch vs streaming vs micro-batch
- checkpoints
- watermarks
- event time vs processing time
- stateful vs stateless streaming
- Structured Streaming
- source/sink/checkpoint

## Study Order

1. Start with QA_01_1000ft_pyspark_opening.md.
2. Then move to Spark.Study.md only by lane.
3. Do not try to memorize Spark.Study.md as one giant file.
4. Study one lane, answer questions, then run labs later under tutorials.

Punch line:
Course 11 teaches the PySpark foundation. Spark.Study.md expands that into the
production Spark / Databricks / Delta / streaming story.

Duplicate policy:
The foundation QA owns Course 11 basics. Spark.Study.md owns expanded
production topics. When topics overlap, use the review lane to choose the
right source instead of reading both full answers.
