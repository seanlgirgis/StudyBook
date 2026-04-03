# Possible Micro-Nuggets To Create (Streaming)

Current lanes already present:
- `kafka`
- `spark_structured_streaming`

## Priority Candidates

1. `flink`
2. `kafka_connect`
3. `debezium_cdc`
4. `schema_registry`
5. `ksqldb`
6. `pulsar`
7. `redpanda`
8. `event_hubs_kafka_api`
9. `kinesis`
10. `pubsub_streaming`

## Per-Lane Nugget Menu (Reusable Template)

1. `00_setup/00_prereq_check.py`
2. `00_setup/01_seed_lab.py`
3. `01_core_streaming/01_topic_or_source_basics.py`
4. `01_core_streaming/02_producer_or_ingest.py`
5. `01_core_streaming/03_consumer_or_sink.py`
6. `02_time_semantics/01_event_time_vs_processing_time.py`
7. `02_time_semantics/02_watermarks.py`
8. `02_time_semantics/03_late_event_policies.py`
9. `03_stateful_processing/01_windowing.py`
10. `03_stateful_processing/02_dedup.py`
11. `03_stateful_processing/03_sessionization.py`
12. `04_reliability/01_delivery_semantics.py`
13. `04_reliability/02_retries_dlq.py`
14. `04_reliability/03_checkpoint_recovery.py`
15. `05_de_patterns/01_bronze_silver_gold.py`
16. `05_de_patterns/02_incremental_aggregates.py`
17. `06_operations/01_lag_and_backpressure.py`
18. `06_operations/02_partition_skew.py`
19. `07_interview_drills/01_interview_drills.py`
20. `08_mini_capstone/01_mini_capstone.py`

## Advanced Streaming Ideas

- `exactly_once_patterns`: transactional producers/consumers and idempotent sinks.
- `stream_table_joins`: stream-stream and stream-table joins.
- `operability`: SLA alerts, autoscaling signals, incident playbooks.
- `chaos_tests`: broker failures, partition loss, consumer crash recovery.
