# Study Progress Tracker

## Proficiency Scale

| Level | Meaning |
|-------|---------|
| 0 | Not started |
| 1 | Read the story |
| 2 | Ran the demo |
| 3 | Can explain it without looking |
| 4 | Can reproduce it from memory |

---

## How to Update

Edit the `Level` and `Reviews` columns as you study.
Update `Last Reviewed` with the date you last touched it.

---

## TRACK 1 — Transactions

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Domain setup | [c011_transfer_happy_path.py](transactions/c011_transfer_happy_path.py) | 0 | 0 | - |
| Rollback | [c012_transfer_rollback_demo.py](transactions/c012_transfer_rollback_demo.py) | 0 | 0 | - |
| Dirty read protection | [c021_dirty_read_protection_demo.py](transactions/c021_dirty_read_protection_demo.py) | 0 | 0 | - |
| Read committed | [c022_read_committed_non_repeatable_read_demo.py](transactions/c022_read_committed_non_repeatable_read_demo.py) | 0 | 0 | - |
| Repeatable read | [c023_repeatable_read_snapshot_demo.py](transactions/c023_repeatable_read_snapshot_demo.py) | 0 | 0 | - |
| Phantom read (read committed) | [c024a_phantom_read_read_committed.py](transactions/c024a_phantom_read_read_committed.py) | 0 | 0 | - |
| Phantom read (repeatable read) | [c024b_phantom_read_repeatable_read.py](transactions/c024b_phantom_read_repeatable_read.py) | 0 | 0 | - |
| Row locking | [c031_row_locking_select_for_update.py](transactions/c031_row_locking_select_for_update.py) | 0 | 0 | - |
| Job queue skip locked | [c032_job_queue_skip_locked.py](transactions/c032_job_queue_skip_locked.py) | 0 | 0 | - |
| Retry on failure | [c041_retry_failure_demo.py](transactions/c041_retry_failure_demo.py) | 0 | 0 | - |
| Idempotency | [c042_idempotency_demo.py](transactions/c042_idempotency_demo.py) | 0 | 0 | - |
| Dead letter queue | [c043_dead_letter_queue_demo.py](transactions/c043_dead_letter_queue_demo.py) | 0 | 0 | - |
| Reliable worker system | [c044_mini_reliable_worker_system.py](transactions/c044_mini_reliable_worker_system.py) | 0 | 0 | - |
| Serializable write skew | [c045_serializable_write_skew_repeatable_read.py](transactions/c045_serializable_write_skew_repeatable_read.py) | 0 | 0 | - |
| Serializable retry | [c046_serializable_retry_pattern.py](transactions/c046_serializable_retry_pattern.py) | 0 | 0 | - |
| Deadlock demo | [c047_deadlock_demo.py](transactions/c047_deadlock_demo.py) | 0 | 0 | - |
| Deadlock fix (ordering) | [c048_deadlock_fix_ordering.py](transactions/c048_deadlock_fix_ordering.py) | 0 | 0 | - |
| Deadlock retry | [c049_deadlock_retry_pattern.py](transactions/c049_deadlock_retry_pattern.py) | 0 | 0 | - |

---

## TRACK 2 — Joins

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Nested loop vs hash join | [c057_nested_loop_vs_hash_join.py](joins/c057_nested_loop_vs_hash_join.py) | 0 | 0 | - |
| Join with index vs without | [c058_join_with_index_vs_without.py](joins/c058_join_with_index_vs_without.py) | 0 | 0 | - |

---

## TRACK 3 — Query Optimization

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Bad vs good queries | [c050_query_optimization_bad_vs_good.py](query_optimization/c050_query_optimization_bad_vs_good.py) | 0 | 0 | - |
| EXPLAIN plan reading | [c051_explain_plan_reading.py](query_optimization/c051_explain_plan_reading.py) | 0 | 0 | - |
| Index not used cases | [c052_index_not_used_cases.py](query_optimization/c052_index_not_used_cases.py) | 0 | 0 | - |
| Composite index left-to-right | [c053_composite_index_left_to_right.py](query_optimization/c053_composite_index_left_to_right.py) | 0 | 0 | - |
| Composite index good vs bad | [c054_composite_index_good_vs_bad_queries.py](query_optimization/c054_composite_index_good_vs_bad_queries.py) | 0 | 0 | - |
| Covering index vs normal | [c055_covering_index_vs_normal_index.py](query_optimization/c055_covering_index_vs_normal_index.py) | 0 | 0 | - |
| Index only scan | [c056_index_only_scan_demo.py](query_optimization/c056_index_only_scan_demo.py) | 0 | 0 | - |

---

## TRACK 4 — Analytics

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Row vs column storage | [c060_row_vs_column_demo.py](analytics/c060_row_vs_column_demo.py) | 0 | 0 | - |
| Parquet | [c061_parquet_demo.py](analytics/c061_parquet_demo.py) | 0 | 0 | - |
| Partition pruning | [c062_partition_pruning_demo.py](analytics/c062_partition_pruning_demo.py) | 0 | 0 | - |
| Cost model | [c063_cost_model_demo.py](analytics/c063_cost_model_demo.py) | 0 | 0 | - |

---

## TRACK 5 — Cache

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Cache aside | [c070_cache_aside_demo.py](cache/c070_cache_aside_demo.py) | 0 | 0 | - |
| TTL | [c071_ttl_demo.py](cache/c071_ttl_demo.py) | 0 | 0 | - |
| Cache stampede | [c072_stampede_demo.py](cache/c072_stampede_demo.py) | 0 | 0 | - |
| Distributed locks | [c073_locks_demo.py](cache/c073_locks_demo.py) | 0 | 0 | - |

---

## TRACK 6 — Distributed

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Partitioning | [c080_partitioning_demo.py](distributed/c080_partitioning_demo.py) | 0 | 0 | - |
| Consistency | [c081_consistency_demo.py](distributed/c081_consistency_demo.py) | 0 | 0 | - |
| Cassandra | [c082_cassandra_demo.py](distributed/c082_cassandra_demo.py) | 0 | 0 | - |
| DynamoDB | [c083_dynamodb_demo.py](distributed/c083_dynamodb_demo.py) | 0 | 0 | - |

---

## TRACK 7 — Retrieval

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Search / inverted index | [c090_search_demo.py](retrieval/c090_search_demo.py) | 0 | 0 | - |
| Ranking | [c091_ranking_demo.py](retrieval/c091_ranking_demo.py) | 0 | 0 | - |
| Vector similarity | [c092_vector_demo.py](retrieval/c092_vector_demo.py) | 0 | 0 | - |
| Hybrid search | [c093_hybrid_demo.py](retrieval/c093_hybrid_demo.py) | 0 | 0 | - |
| Metadata filtering | [c094_metadata_filtering_demo.py](retrieval/c094_metadata_filtering_demo.py) | 0 | 0 | - |
| BM25 | [c095_bm25_demo.py](retrieval/c095_bm25_demo.py) | 0 | 0 | - |
| Reranking | [c096_reranking_demo.py](retrieval/c096_reranking_demo.py) | 0 | 0 | - |
| Top-k / Recall@k | [c097_topk_recall_demo.py](retrieval/c097_topk_recall_demo.py) | 0 | 0 | - |

---

## TRACK 8 — SQL for Data Engineering

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Window functions | [c098_window_functions_demo.py](sql_de/c098_window_functions_demo.py) | 0 | 0 | - |
| QUALIFY | [c099_qualify_demo.py](sql_de/c099_qualify_demo.py) | 0 | 0 | - |
| Merge / Upsert | [c100_merge_upsert_demo.py](sql_de/c100_merge_upsert_demo.py) | 0 | 0 | - |
| Recursive CTEs | [c101_recursive_ctes_demo.py](sql_de/c101_recursive_ctes_demo.py) | 0 | 0 | - |
| Pivot / Unpivot | [c102_pivot_unpivot_demo.py](sql_de/c102_pivot_unpivot_demo.py) | 0 | 0 | - |
| JSON / Array functions | [c103_json_array_functions_demo.py](sql_de/c103_json_array_functions_demo.py) | 0 | 0 | - |
| Dynamic SQL | [c104_dynamic_sql_demo.py](sql_de/c104_dynamic_sql_demo.py) | 0 | 0 | - |

---

## TRACK 9 — Streaming

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Kafka concepts | [c001_kafka_concepts_demo.py](streaming/c001_kafka_concepts_demo.py) | 0 | 0 | - |
| Consumer groups | [c002_consumer_groups_demo.py](streaming/c002_consumer_groups_demo.py) | 0 | 0 | - |
| CDC | [c003_cdc_demo.py](streaming/c003_cdc_demo.py) | 0 | 0 | - |
| Event-driven ingestion | [c004_event_driven_ingestion_demo.py](streaming/c004_event_driven_ingestion_demo.py) | 0 | 0 | - |
| Delivery semantics | [c005_delivery_semantics_demo.py](streaming/c005_delivery_semantics_demo.py) | 0 | 0 | - |

---

## TRACK 10 — Data Modeling

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Fact vs dimension | [c001_fact_vs_dimension_demo.py](modeling/c001_fact_vs_dimension_demo.py) | 0 | 0 | - |
| Star schema | [c002_star_schema_demo.py](modeling/c002_star_schema_demo.py) | 0 | 0 | - |
| Snowflake schema | [c003_snowflake_schema_demo.py](modeling/c003_snowflake_schema_demo.py) | 0 | 0 | - |
| SCD Type 1 | [c004_scd_type1_demo.py](modeling/c004_scd_type1_demo.py) | 0 | 0 | - |
| SCD Type 2 | [c005_scd_type2_demo.py](modeling/c005_scd_type2_demo.py) | 0 | 0 | - |
| Data vault | [c006_data_vault_demo.py](modeling/c006_data_vault_demo.py) | 0 | 0 | - |

---

## TRACK 11 — Orchestration

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| DAG concepts | [c001_dag_concepts_demo.py](orchestration/c001_dag_concepts_demo.py) | 0 | 0 | - |
| Scheduling and triggers | [c002_scheduling_demo.py](orchestration/c002_scheduling_demo.py) | 0 | 0 | - |
| Retry and failure handling | [c003_retry_failure_demo.py](orchestration/c003_retry_failure_demo.py) | 0 | 0 | - |
| Backfill patterns | [c004_backfill_demo.py](orchestration/c004_backfill_demo.py) | 0 | 0 | - |
| Idempotent tasks | [c005_idempotent_tasks_demo.py](orchestration/c005_idempotent_tasks_demo.py) | 0 | 0 | - |

---

## TRACK 12 — dbt Patterns *(coming)*

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Models (staging/intermediate/marts) | c001_models_demo.py | 0 | 0 | - |
| Incremental models | c002_incremental_models_demo.py | 0 | 0 | - |
| dbt tests | c003_dbt_tests_demo.py | 0 | 0 | - |
| Snapshots | c004_snapshots_demo.py | 0 | 0 | - |
| Sources and freshness | c005_sources_freshness_demo.py | 0 | 0 | - |

---

## TRACK 13 — Spark Basics

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| DataFrames vs RDDs | [c001_dataframes_vs_rdds_demo.py](spark/c001_dataframes_vs_rdds_demo.py) | 0 | 0 | - |
| Lazy evaluation | [c002_lazy_evaluation_demo.py](spark/c002_lazy_evaluation_demo.py) | 0 | 0 | - |
| Partitioning and shuffling | [c003_partitioning_shuffling_demo.py](spark/c003_partitioning_shuffling_demo.py) | 0 | 0 | - |
| Joins at scale | [c004_joins_at_scale_demo.py](spark/c004_joins_at_scale_demo.py) | 0 | 0 | - |
| Broadcast joins | [c005_broadcast_joins_demo.py](spark/c005_broadcast_joins_demo.py) | 0 | 0 | - |

---

## TRACK 14 — ELT Pipeline Patterns

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Layer design (staging/raw/curated) | [c001_staging_raw_curated_demo.py](elt_pipeline_patterns/c001_staging_raw_curated_demo.py) | 0 | 0 | - |
| Full load vs incremental | [c002_full_vs_incremental_demo.py](elt_pipeline_patterns/c002_full_vs_incremental_demo.py) | 0 | 0 | - |
| Watermarks | [c003_watermarks_demo.py](elt_pipeline_patterns/c003_watermarks_demo.py) | 0 | 0 | - |
| Schema evolution | [c004_schema_evolution_demo.py](elt_pipeline_patterns/c004_schema_evolution_demo.py) | 0 | 0 | - |
| Data contracts | [c005_data_contracts_demo.py](elt_pipeline_patterns/c005_data_contracts_demo.py) | 0 | 0 | - |

---

## TRACK 15 — Data Quality

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Schema validation | [c001_schema_validation_demo.py](data_quality/c001_schema_validation_demo.py) | 0 | 0 | - |
| Null and type checks | [c002_null_type_checks_demo.py](data_quality/c002_null_type_checks_demo.py) | 0 | 0 | - |
| Referential integrity | [c003_referential_integrity_demo.py](data_quality/c003_referential_integrity_demo.py) | 0 | 0 | - |
| Data freshness | [c004_data_freshness_demo.py](data_quality/c004_data_freshness_demo.py) | 0 | 0 | - |
| Anomaly detection | [c005_anomaly_detection_demo.py](data_quality/c005_anomaly_detection_demo.py) | 0 | 0 | - |

---

## TRACK 16 — Data Lakehouse

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Object storage concepts | [c001_object_storage_demo.py](data_lakehouse/c001_object_storage_demo.py) | 0 | 0 | - |
| ACID on object storage (Delta Lake) | [c002_delta_lake_acid_demo.py](data_lakehouse/c002_delta_lake_acid_demo.py) | 0 | 0 | - |
| Table formats (Iceberg) | [c003_iceberg_table_format_demo.py](data_lakehouse/c003_iceberg_table_format_demo.py) | 0 | 0 | - |
| Time travel | [c004_time_travel_demo.py](data_lakehouse/c004_time_travel_demo.py) | 0 | 0 | - |
| Compaction and optimization | [c005_compaction_demo.py](data_lakehouse/c005_compaction_demo.py) | 0 | 0 | - |

---

## TRACK 17 — Splunk *(deferred — large download)*

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Log ingestion and indexing | c001_log_ingestion_demo.py | 0 | 0 | - |
| SPL basics | c002_spl_basics_demo.py | 0 | 0 | - |
| Dashboards and alerting | c003_alerting_demo.py | 0 | 0 | - |
| Log-based anomaly detection | c004_log_anomaly_demo.py | 0 | 0 | - |
| Splunk vs Elasticsearch | c005_splunk_vs_elastic_demo.py | 0 | 0 | - |

---

## FINAL — System Design

| Topic | Demo | Level | Reviews | Last Reviewed |
|-------|------|-------|---------|---------------|
| Full polyglot pipeline | [c999_full_polyglot_pipeline.py](system_design/c999_full_polyglot_pipeline.py) | 0 | 0 | - |
