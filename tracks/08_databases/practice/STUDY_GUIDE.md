# Database Mastery — Study Guide

> Spiral method: three passes across all topics.
> Pass 1 — one concept per track, get the big picture.
> Pass 2 — fill in the track, go deeper.
> Pass 3 — expert patterns, edge cases, full system.

---

## PASS 1 — Jack of All Trades
*One entry point per track. Read the story, run the demo, get the mental model.*

---

### 1.1 Why data correctness matters — Transactions
The moment two things happen at the same time, data can corrupt.
Transactions are the contract that prevents it.

| | File |
|-|------|
| Story | [d01_domain_setup.md](transactions/d01_domain_setup.md) |
| Demo | [c011_transfer_happy_path.py](transactions/c011_transfer_happy_path.py) |
| Demo | [c012_transfer_rollback_demo.py](transactions/c012_transfer_rollback_demo.py) |

---

### 1.2 Why storage shape matters — Row vs Column
The same data stored differently runs 100x faster or slower.
Shape is a first-class decision in data engineering.

| | File |
|-|------|
| Story | [d01_row_vs_column_story.md](analytics/d01_row_vs_column_story.md) |
| Demo | [c060_row_vs_column_demo.py](analytics/c060_row_vs_column_demo.py) |

---

### 1.3 Why we add layers — Cache Aside
Your database cannot serve every read. Cache absorbs the load.
Cache-aside is the simplest and most common pattern.

| | File |
|-|------|
| Story | [d01_cache_aside_story.md](cache/d01_cache_aside_story.md) |
| Demo | [c070_cache_aside_demo.py](cache/c070_cache_aside_demo.py) |

---

### 1.4 Why one machine is not enough — Partitioning
Data grows past what one node can hold or serve.
Partitioning is how you split it without losing your mind.

| | File |
|-|------|
| Story | [d01_partitioning_story.md](distributed/d01_partitioning_story.md) |
| Demo | [c080_partitioning_demo.py](distributed/c080_partitioning_demo.py) |

---

### 1.5 Why SQL fails for search — Inverted Index
SQL scans rows. Search inverts the index — words point to documents.
This is the foundation of every search engine.

| | File |
|-|------|
| Story | [d01_search_story.md](retrieval/d01_search_story.md) |
| Demo | [c090_search_demo.py](retrieval/c090_search_demo.py) |

---

### 1.6 Why advanced SQL matters — Window Functions
GROUP BY collapses rows. Window functions let you aggregate without losing them.
The most used advanced SQL pattern in data engineering.

| | File |
|-|------|
| Story | [d01_window_functions_story.md](sql_de/d01_window_functions_story.md) |
| Demo | [c098_window_functions_demo.py](sql_de/c098_window_functions_demo.py) |

---

### 1.7 Why batch is not enough — Kafka Concepts
Batch runs every hour. Kafka streams every millisecond.
Producers write, consumers read, offsets track position.

| | File |
|-|------|
| Story | [d00_kafka_story.md](streaming/d00_kafka_story.md) |
| Demo | [c001_kafka_concepts_demo.py](streaming/c001_kafka_concepts_demo.py) |

---

### 1.8 Why raw tables break analytics — Star Schema
Raw tables are normalized for writes, not reads.
Star schema denormalizes into facts and dimensions for fast analytics.

| | File |
|-|------|
| Story | [d01_star_schema_story.md](modeling/d01_star_schema_story.md) |
| Demo | [c002_star_schema_demo.py](modeling/c002_star_schema_demo.py) |

---

## PASS 2 — Deepening
*Cover the full track. More concepts, more patterns, more pain.*

---

### 2.1 Relational — Isolation and Locking

**Serializable isolation** — the strongest guarantee; reads and writes behave as if alone.
| Story | [d03_serializable_story.md](transactions/d03_serializable_story.md) |
|-|------|
| Demos | [c021](transactions/c021_dirty_read_protection_demo.py) · [c022](transactions/c022_read_committed_non_repeatable_read_demo.py) · [c023](transactions/c023_repeatable_read_snapshot_demo.py) · [c045](transactions/c045_serializable_write_skew_repeatable_read.py) |

**Deadlocks** — two transactions each waiting for the other. Fix: order your locks.
| Story | [d04_deadlock_story.md](transactions/d04_deadlock_story.md) |
|-|------|
| Demos | [c047](transactions/c047_deadlock_demo.py) · [c048](transactions/c048_deadlock_fix_ordering.py) · [c049](transactions/c049_deadlock_retry_pattern.py) |

**Joins and index behaviour** — how the engine chooses nested loop vs hash join.
| Story | [d01_joins_story.md](joins/d01_joins_story.md) |
|-|------|
| Demos | [c057](joins/c057_nested_loop_vs_hash_join.py) · [c058](joins/c058_join_with_index_vs_without.py) |

---

### 2.2 Analytics — File Formats and Cost

**Parquet** — columnar file format; compression + predicate pushdown built in.
| Story | [d02_parquet_story.md](analytics/d02_parquet_story.md) |
|-|------|
| Demo | [c061_parquet_demo.py](analytics/c061_parquet_demo.py) |

**Partition pruning** — skip entire file partitions; the difference between scanning 1 file vs 1000.
| Story | [d03_partition_pruning_story.md](analytics/d03_partition_pruning_story.md) |
|-|------|
| Demo | [c062_partition_pruning_demo.py](analytics/c062_partition_pruning_demo.py) |

**Cost model** — how query engines estimate and choose execution plans.
| Story | [d04_cost_model_story.md](analytics/d04_cost_model_story.md) |
|-|------|
| Demo | [c063_cost_model_demo.py](analytics/c063_cost_model_demo.py) |

---

### 2.3 Cache — Expiry and Race Conditions

**TTL** — cached data has a shelf life. Stale data is a feature, not a bug — until it isn't.
| Story | [d02_ttl_story.md](cache/d02_ttl_story.md) |
|-|------|
| Demo | [c071_ttl_demo.py](cache/c071_ttl_demo.py) |

**Cache stampede** — TTL expires, 10,000 requests hit the DB at once. Use locking or jitter.
| Story | [d03_stampede_story.md](cache/d03_stampede_story.md) |
|-|------|
| Demo | [c072_stampede_demo.py](cache/c072_stampede_demo.py) |

---

### 2.4 Distributed — Consistency and NoSQL Engines

**Consistency models** — eventual vs strong; CAP theorem in practice.
| Story | [d02_consistency_story.md](distributed/d02_consistency_story.md) |
|-|------|
| Demo | [c081_consistency_demo.py](distributed/c081_consistency_demo.py) |

**Cassandra** — wide-column store; partition key is everything; model for your queries.
| Story | [d03_cassandra_story.md](distributed/d03_cassandra_story.md) |
|-|------|
| Demo | [c082_cassandra_demo.py](distributed/c082_cassandra_demo.py) |

---

### 2.5 Retrieval — Ranking and Vectors

**Ranking** — not all results are equal; TF-IDF and scoring models.
| Story | [d02_ranking_story.md](retrieval/d02_ranking_story.md) |
|-|------|
| Demo | [c091_ranking_demo.py](retrieval/c091_ranking_demo.py) |

**Vector similarity** — meaning over keywords; embeddings + cosine distance.
| Story | [d03_vector_story.md](retrieval/d03_vector_story.md) |
|-|------|
| Demo | [c092_vector_demo.py](retrieval/c092_vector_demo.py) |

**Hybrid search** — combine keyword and vector; the real-world default.
| Story | [d04_hybrid_story.md](retrieval/d04_hybrid_story.md) |
|-|------|
| Demo | [c093_hybrid_demo.py](retrieval/c093_hybrid_demo.py) |

---

### 2.6 SQL DE — Core Patterns

**QUALIFY** — filter window function results in one pass; replaces a subquery.
| Story | [d02_qualify_story.md](sql_de/d02_qualify_story.md) |
|-|------|
| Demo | [c099_qualify_demo.py](sql_de/c099_qualify_demo.py) |

**Merge / Upsert** — insert if new, update if exists; the backbone of incremental loads.
| Story | [d03_recursive_ctes_story.md](sql_de/d03_recursive_ctes_story.md) |
|-|------|
| Demo | [c100_merge_upsert_demo.py](sql_de/c100_merge_upsert_demo.py) |

**Recursive CTEs** — SQL loops for hierarchies; org charts, bill of materials, graphs.
| Story | [d03_recursive_ctes_story.md](sql_de/d03_recursive_ctes_story.md) |
|-|------|
| Demo | [c101_recursive_ctes_demo.py](sql_de/c101_recursive_ctes_demo.py) |

**Pivot / Unpivot** — rotate rows to columns and back; shape data for reporting vs analytics.
| Story | [d04_pivot_unpivot_story.md](sql_de/d04_pivot_unpivot_story.md) |
|-|------|
| Demo | [c102_pivot_unpivot_demo.py](sql_de/c102_pivot_unpivot_demo.py) |

---

### 2.7 Streaming — Consumer Groups and CDC

**Consumer groups** — scale consumers horizontally; each partition consumed by one worker.
| Story | [d01_consumer_groups_story.md](streaming/d01_consumer_groups_story.md) |
|-|------|
| Demo | [c002_consumer_groups_demo.py](streaming/c002_consumer_groups_demo.py) |

**CDC — Change Data Capture** — detect row-level changes in a source DB and stream them downstream.
| Story | [d02_cdc_story.md](streaming/d02_cdc_story.md) |
|-|------|
| Demo | [c003_cdc_demo.py](streaming/c003_cdc_demo.py) |

---

### 2.8 Modeling — Dimensions and History

**Fact vs dimension** — facts are measurements, dimensions are context. Get this wrong and nothing queries well.
| Story | [d00_fact_vs_dimension_story.md](modeling/d00_fact_vs_dimension_story.md) |
|-|------|
| Demo | [c001_fact_vs_dimension_demo.py](modeling/c001_fact_vs_dimension_demo.py) |

**Snowflake schema** — normalize dimensions further; saves space, costs joins.
| Story | [d02_snowflake_schema_story.md](modeling/d02_snowflake_schema_story.md) |
|-|------|
| Demo | [c003_snowflake_schema_demo.py](modeling/c003_snowflake_schema_demo.py) |

**SCD Type 1** — overwrite old values; no history kept; simple but lossy.
| Story | [d03_scd_type1_story.md](modeling/d03_scd_type1_story.md) |
|-|------|
| Demo | [c004_scd_type1_demo.py](modeling/c004_scd_type1_demo.py) |

---

## PASS 3 — Expert
*Edge cases, advanced patterns, and the full system.*

---

### 3.1 Relational — Query Optimization and Index Mastery

**Query optimization** — bad queries vs good queries; EXPLAIN plan reading.
| Story | [d01_query_optimization_story.md](query_optimization/d01_query_optimization_story.md) |
|-|------|
| Demos | [c050](query_optimization/c050_query_optimization_bad_vs_good.py) · [c051](query_optimization/c051_explain_plan_reading.py) · [c052](query_optimization/c052_index_not_used_cases.py) |

**Composite indexes** — column order is everything; left-to-right rule.
| Story | [d02_composite_indexes_story.md](query_optimization/d02_composite_indexes_story.md) |
|-|------|
| Demos | [c053](query_optimization/c053_composite_index_left_to_right.py) · [c054](query_optimization/c054_composite_index_good_vs_bad_queries.py) |

**Covering indexes** — the query never touches the table; index-only scan.
| Story | [d03_covering_indexes_story.md](query_optimization/d03_covering_indexes_story.md) |
|-|------|
| Demos | [c055](query_optimization/c055_covering_index_vs_normal_index.py) · [c056](query_optimization/c056_index_only_scan_demo.py) |

**Reliable worker patterns** — retry, idempotency, dead-letter queue.
| Demos | [c041](transactions/c041_retry_failure_demo.py) · [c042](transactions/c042_idempotency_demo.py) · [c043](transactions/c043_dead_letter_queue_demo.py) · [c044](transactions/c044_mini_reliable_worker_system.py) |
|-|------|

---

### 3.2 Distributed — DynamoDB Patterns

**DynamoDB** — single-table design; access patterns drive the schema; GSIs.
| Story | [d04_dynamodb_story.md](distributed/d04_dynamodb_story.md) |
|-|------|
| Demo | [c083_dynamodb_demo.py](distributed/c083_dynamodb_demo.py) |

---

### 3.3 Cache — Distributed Locks

**Distributed locks** — prevent concurrent writes across services using Redis SETNX.
| Story | [d04_locks_story.md](cache/d04_locks_story.md) |
|-|------|
| Demo | [c073_locks_demo.py](cache/c073_locks_demo.py) |

---

### 3.4 Retrieval — Precision and Recall

**Metadata filtering** — narrow the vector search space before scoring; speed + relevance.
| Story | [d05_metadata_filtering_story.md](retrieval/d05_metadata_filtering_story.md) |
|-|------|
| Demo | [c094_metadata_filtering_demo.py](retrieval/c094_metadata_filtering_demo.py) |

**BM25** — probabilistic keyword ranking; better than TF-IDF for most text retrieval.
| Story | [d06_bm25_story.md](retrieval/d06_bm25_story.md) |
|-|------|
| Demo | [c095_bm25_demo.py](retrieval/c095_bm25_demo.py) |

**Reranking** — two-stage retrieval: fast recall then slow precision scoring.
| Story | [d07_reranking_story.md](retrieval/d07_reranking_story.md) |
|-|------|
| Demo | [c096_reranking_demo.py](retrieval/c096_reranking_demo.py) |

**Top-k / Recall@k** — how to measure whether your retrieval system is actually working.
| Story | [d08_topk_recall_story.md](retrieval/d08_topk_recall_story.md) |
|-|------|
| Demo | [c097_topk_recall_demo.py](retrieval/c097_topk_recall_demo.py) |

---

### 3.5 SQL DE — Advanced Patterns

**JSON / Array functions** — query semi-structured data without exploding it into rows.
| Story | [d05_json_array_functions_story.md](sql_de/d05_json_array_functions_story.md) |
|-|------|
| Demo | [c103_json_array_functions_demo.py](sql_de/c103_json_array_functions_demo.py) |

**Dynamic SQL** — build queries at runtime; parameterized table names, conditional filters.
| Story | [d06_dynamic_sql_story.md](sql_de/d06_dynamic_sql_story.md) |
|-|------|
| Demo | [c104_dynamic_sql_demo.py](sql_de/c104_dynamic_sql_demo.py) |

---

### 3.6 Streaming — Delivery Guarantees and Ingestion

**Event-driven ingestion** — events trigger pipeline stages; decouple producers from consumers.
| Story | [d03_event_driven_ingestion_story.md](streaming/d03_event_driven_ingestion_story.md) |
|-|------|
| Demo | [c004_event_driven_ingestion_demo.py](streaming/c004_event_driven_ingestion_demo.py) |

**At-least-once vs exactly-once** — idempotency is the price of reliability.
| Story | [d04_delivery_semantics_story.md](streaming/d04_delivery_semantics_story.md) |
|-|------|
| Demo | [c005_delivery_semantics_demo.py](streaming/c005_delivery_semantics_demo.py) |

---

### 3.7 Modeling — SCD Type 2 and Data Vault

**SCD Type 2** — keep full history with effective dates; the standard for audit-safe warehouses.
| Story | [d04_scd_type2_story.md](modeling/d04_scd_type2_story.md) |
|-|------|
| Demo | [c005_scd_type2_demo.py](modeling/c005_scd_type2_demo.py) |

**Data Vault** — hubs, links, satellites; built for change, audit-friendly, scale-first.
| Story | [d05_data_vault_story.md](modeling/d05_data_vault_story.md) |
|-|------|
| Demo | [c006_data_vault_demo.py](modeling/c006_data_vault_demo.py) |

---

### 3.8 Final System — Everything Together

Build a real polyglot data platform end to end.
Ingestion -> relational -> cache -> analytics -> search -> vector -> streaming.

| Story | [d01_final_pipeline_story.md](system_design/d01_final_pipeline_story.md) |
|-|------|
| Demo | [c999_full_polyglot_pipeline.py](system_design/c999_full_polyglot_pipeline.py) |

---

---

## PASS 4 — Modern Stack (In Progress)
*These tracks cover the tools that appear in every modern DE job posting.*

---

### 4.1 Orchestration — DAGs, Retries, Backfill
*(Files coming — practice/orchestration/)*

How production pipelines are scheduled, monitored, and recovered.
DAG = directed acyclic graph. Every task has dependencies, retry rules, and a failure path.

---

### 4.2 dbt Patterns — Transformation Layer
*(Files coming — practice/dbt_patterns/)*

The standard tool for warehouse transformations.
Models flow staging → intermediate → marts. Tests run on every build. Snapshots handle SCD.

---

### 4.3 Spark Basics — Distributed Compute

When data outgrows pandas. DataFrames, lazy evaluation, shuffles, and broadcast joins.
Reason about distributed compute without needing a real cluster.

| | File |
|-|------|
| Demo | [c001_dataframes_vs_rdds_demo.py](spark/c001_dataframes_vs_rdds_demo.py) |
| Demo | [c002_lazy_evaluation_demo.py](spark/c002_lazy_evaluation_demo.py) |
| Demo | [c003_partitioning_shuffling_demo.py](spark/c003_partitioning_shuffling_demo.py) |
| Demo | [c004_joins_at_scale_demo.py](spark/c004_joins_at_scale_demo.py) |
| Demo | [c005_broadcast_joins_demo.py](spark/c005_broadcast_joins_demo.py) |

---

### 4.4 ELT Pipeline Patterns — Layer Design

How data flows through a warehouse: raw → staged → curated.
Full vs incremental loads, watermarks, schema evolution, data contracts.

| | File |
|-|------|
| Story | [d00_staging_raw_curated_story.md](elt_pipeline_patterns/d00_staging_raw_curated_story.md) |
| Demo | [c001_staging_raw_curated_demo.py](elt_pipeline_patterns/c001_staging_raw_curated_demo.py) |
| Story | [d01_full_vs_incremental_story.md](elt_pipeline_patterns/d01_full_vs_incremental_story.md) |
| Demo | [c002_full_vs_incremental_demo.py](elt_pipeline_patterns/c002_full_vs_incremental_demo.py) |
| Story | [d02_watermarks_story.md](elt_pipeline_patterns/d02_watermarks_story.md) |
| Demo | [c003_watermarks_demo.py](elt_pipeline_patterns/c003_watermarks_demo.py) |
| Story | [d03_schema_evolution_story.md](elt_pipeline_patterns/d03_schema_evolution_story.md) |
| Demo | [c004_schema_evolution_demo.py](elt_pipeline_patterns/c004_schema_evolution_demo.py) |
| Story | [d04_data_contracts_story.md](elt_pipeline_patterns/d04_data_contracts_story.md) |
| Demo | [c005_data_contracts_demo.py](elt_pipeline_patterns/c005_data_contracts_demo.py) |

---

### 4.5 Data Quality — Trust Your Data

Schema validation, null checks, referential integrity, freshness checks, anomaly detection.
Data without quality checks is not production-ready.

| | File |
|-|------|
| Story | [d00_schema_validation_story.md](data_quality/d00_schema_validation_story.md) |
| Demo | [c001_schema_validation_demo.py](data_quality/c001_schema_validation_demo.py) |
| Story | [d01_null_type_checks_story.md](data_quality/d01_null_type_checks_story.md) |
| Demo | [c002_null_type_checks_demo.py](data_quality/c002_null_type_checks_demo.py) |
| Story | [d02_referential_integrity_story.md](data_quality/d02_referential_integrity_story.md) |
| Demo | [c003_referential_integrity_demo.py](data_quality/c003_referential_integrity_demo.py) |
| Story | [d03_data_freshness_story.md](data_quality/d03_data_freshness_story.md) |
| Demo | [c004_data_freshness_demo.py](data_quality/c004_data_freshness_demo.py) |
| Story | [d04_anomaly_detection_story.md](data_quality/d04_anomaly_detection_story.md) |
| Demo | [c005_anomaly_detection_demo.py](data_quality/c005_anomaly_detection_demo.py) |

---

### 4.6 Data Lakehouse — ACID on Object Storage

Why Delta Lake and Iceberg exist. ACID guarantees on S3.
Time travel, schema enforcement, compaction — the architecture replacing traditional warehouses.

| | File |
|-|------|
| Story | [d00_object_storage_story.md](data_lakehouse/d00_object_storage_story.md) |
| Demo | [c001_object_storage_demo.py](data_lakehouse/c001_object_storage_demo.py) |
| Story | [d01_delta_lake_acid_story.md](data_lakehouse/d01_delta_lake_acid_story.md) |
| Demo | [c002_delta_lake_acid_demo.py](data_lakehouse/c002_delta_lake_acid_demo.py) |
| Story | [d02_iceberg_table_format_story.md](data_lakehouse/d02_iceberg_table_format_story.md) |
| Demo | [c003_iceberg_table_format_demo.py](data_lakehouse/c003_iceberg_table_format_demo.py) |
| Story | [d03_time_travel_story.md](data_lakehouse/d03_time_travel_story.md) |
| Demo | [c004_time_travel_demo.py](data_lakehouse/c004_time_travel_demo.py) |
| Story | [d04_compaction_story.md](data_lakehouse/d04_compaction_story.md) |
| Demo | [c005_compaction_demo.py](data_lakehouse/c005_compaction_demo.py) |

---

## Quick Reference — All Files by Track

| Track | Stories | Demos |
|-------|---------|-------|
| Transactions | d00-d04 in transactions/ | c001-c049 |
| Joins | d01 in joins/ | c057-c058 |
| Query Optimization | d01-d03 in query_optimization/ | c050-c056 |
| Analytics | d01-d04 in analytics/ | c060-c063 |
| Cache | d01-d04 in cache/ | c070-c073 |
| Distributed | d01-d04 in distributed/ | c080-c083 |
| Retrieval | d01-d08 in retrieval/ | c090-c097 |
| SQL DE | d01-d06 in sql_de/ | c098-c104 |
| Streaming | d00-d04 in streaming/ | c001-c005 |
| Modeling | d00-d05 in modeling/ | c001-c006 |
| Spark | — | c001-c005 in spark/ |
| ELT Pipeline Patterns | d00-d04 in elt_pipeline_patterns/ | c001-c005 in elt_pipeline_patterns/ |
| Data Quality | d00-d04 in data_quality/ | c001-c005 in data_quality/ |
| Data Lakehouse | d00-d04 in data_lakehouse/ | c001-c005 in data_lakehouse/ |
| System Design | d01 in system_design/ | c999 |
