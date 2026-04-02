# Database Mastery Roadmap (Story-Based System)

## Philosophy

We do NOT learn databases by reading.

We learn by:

story -> scenario -> code -> failure -> fix -> pattern -> system

Every concept must:
- be felt (pain)
- be solved (code)
- become reusable (pattern)

---

## Folder Structure

practice/
    relational/
    analytics/
    cache/
    distributed/
    retrieval/
    sql_de/
    streaming/
    modeling/
    orchestration/
    dbt_patterns/
    spark/
    elt_pipeline_patterns/
    data_quality/
    data_lakehouse/
    splunk/
    system_design/
    _tracker.md
    ROADMAP.md

Each track follows:

    dNN_topic_story.md
    cNNN_topic_demo.py

---

## TRACK 1 — RELATIONAL (FOUNDATION) [COMPLETE]

Goal:
Understand correctness, isolation, and behavior under concurrency

Story:
"Your data is wrong. You don't know why."

Topics:
- transactions
- serializable isolation
- deadlocks
- query optimization
- composite indexes
- covering indexes
- joins

Outcome:
"Why your data is correct — or corrupted"

Folder: practice/relational/

---

## TRACK 2 — ANALYTICS (COLUMNAR / OLAP) [COMPLETE]

Goal:
Understand performance + cost at scale

Story:
"You run analytics. Queries are slow. Costs are exploding."

Topics:
- row vs column storage
- parquet
- partition pruning
- cost model / aggregation cost

Outcome:
"Why queries are fast or bankrupt you"

Folder: practice/analytics/

---

## TRACK 3 — CACHE (REDIS THINKING) [COMPLETE]

Goal:
Understand speed vs correctness tradeoffs

Story:
"System is slow. DB is dying. You add cache."

Topics:
- cache-aside
- TTL expiration
- cache stampede
- distributed locks

Outcome:
"Why cache helps — and how it breaks things"

Folder: practice/cache/

---

## TRACK 4 — DISTRIBUTED DATA (NOSQL) [COMPLETE]

Goal:
Understand scale + tradeoffs

Story:
"You go global. One DB is not enough."

Topics:
- partitioning
- consistency
- Cassandra modeling
- DynamoDB patterns

Outcome:
"Why NoSQL exists"

Folder: practice/distributed/

---

## TRACK 5 — SEARCH + VECTOR [COMPLETE]

Goal:
Understand retrieval systems

Story:
"Users search logs, alerts, meaning"

Topics:
- search / inverted index
- ranking
- vector similarity
- hybrid search
- metadata filtering
- BM25
- reranking
- top-k / recall@k

Outcome:
"Search vs SQL vs Vector"

Folder: practice/retrieval/

---

## TRACK 6 — SQL FOR DATA ENGINEERING [COMPLETE]

Goal:
Master advanced SQL patterns used daily in data engineering

Story:
"You can write SELECT. But real DE SQL looks nothing like that."

Topics:
- window functions         -> c098_window_functions_demo.py
- qualify                  -> c099_qualify_demo.py
- merge / upsert           -> c100_merge_upsert_demo.py
- recursive CTEs           -> c101_recursive_ctes_demo.py
- pivot / unpivot          -> c102_pivot_unpivot_demo.py
- json / array functions   -> c103_json_array_functions_demo.py
- dynamic sql              -> c104_dynamic_sql_demo.py

Outcome:
"Write SQL that data engineers actually write"

Folder: practice/sql_de/

---

## TRACK 7 — STREAMING [COMPLETE]

Goal:
Understand event-driven data movement

Story:
"Your batch pipeline is too slow. Data must flow in real time."

Topics:
- Kafka concepts: producers, consumers, offsets  -> c001_kafka_concepts_demo.py
- consumer groups                                -> c002_consumer_groups_demo.py
- CDC — change data capture                      -> c003_cdc_demo.py
- event-driven ingestion pattern                 -> c004_event_driven_ingestion_demo.py
- at-least-once vs exactly-once delivery         -> c005_delivery_semantics_demo.py

Outcome:
"Why streaming exists and when to use it over batch"

Folder: practice/streaming/

---

## TRACK 8 — DATA MODELING [COMPLETE]

Goal:
Understand how to structure data for warehouses and analytics

Story:
"Your data is in the warehouse but nobody can query it efficiently."

Topics:
- fact vs dimension tables    -> c001_fact_vs_dimension_demo.py
- star schema                 -> c002_star_schema_demo.py
- snowflake schema            -> c003_snowflake_schema_demo.py
- SCD Type 1 (overwrite)      -> c004_scd_type1_demo.py
- SCD Type 2 (history rows)   -> c005_scd_type2_demo.py
- data vault basics           -> c006_data_vault_demo.py

Outcome:
"Design a warehouse schema from scratch"

Folder: practice/modeling/

---

## TRACK 9 — ORCHESTRATION [ ]

Goal:
Understand how production pipelines are scheduled, monitored, and recovered

Story:
"Your pipeline ran. Then it didn't. Nobody noticed for three days."

Topics:
- DAG concepts and task dependencies        -> c001_dag_concepts_demo.py
- scheduling and triggers                   -> c002_scheduling_demo.py
- retry and failure handling                -> c003_retry_failure_demo.py
- backfill patterns                         -> c004_backfill_demo.py
- idempotent tasks                          -> c005_idempotent_tasks_demo.py

Outcome:
"Build pipelines that survive failure and recover cleanly"

Folder: practice/orchestration/

---

## TRACK 10 — DBT PATTERNS [ ]

Goal:
Understand the standard transformation layer in modern data warehouses

Story:
"SQL is everywhere. dbt makes it testable, versioned, and documented."

Topics:
- models: staging / intermediate / marts    -> c001_models_demo.py
- incremental models                        -> c002_incremental_models_demo.py
- dbt tests (schema + custom)               -> c003_dbt_tests_demo.py
- snapshots (SCD Type 2 in dbt)             -> c004_snapshots_demo.py
- sources and freshness                     -> c005_sources_freshness_demo.py

Outcome:
"Structure and test warehouse transformations like an engineer"

Folder: practice/dbt_patterns/

---

## TRACK 11 — SPARK BASICS [COMPLETE]

Goal:
Understand distributed compute for large-scale data transformation

Story:
"Your pandas job runs fine on 1GB. It dies on 100GB."

Topics:
- DataFrames vs RDDs                        -> c001_dataframes_vs_rdds_demo.py
- lazy evaluation (transformations/actions) -> c002_lazy_evaluation_demo.py
- partitioning and shuffling                -> c003_partitioning_shuffling_demo.py
- joins at scale                            -> c004_joins_at_scale_demo.py
- broadcast joins                           -> c005_broadcast_joins_demo.py

Outcome:
"Reason about distributed compute without needing a cluster"

Folder: practice/spark/

---

## TRACK 12 — ELT PIPELINE PATTERNS [COMPLETE]

Goal:
Understand how data moves through a modern warehouse architecture

Story:
"Data lands. Nobody knows where it came from or whether it changed."

Topics:
- staging / raw / curated layer design      -> c001_staging_raw_curated_demo.py
- full load vs incremental load             -> c002_full_vs_incremental_demo.py
- watermarks and high-water marks           -> c003_watermarks_demo.py
- schema evolution                          -> c004_schema_evolution_demo.py
- data contracts                            -> c005_data_contracts_demo.py

Outcome:
"Design a warehouse ingestion layer that handles change"

Folder: practice/elt_pipeline_patterns/

---

## TRACK 13 — DATA QUALITY [COMPLETE]

Goal:
Understand how to validate, monitor, and trust data in production

Story:
"The dashboard showed wrong numbers for a week. Nobody caught it."

Topics:
- schema validation                         -> c001_schema_validation_demo.py
- null and type checks                      -> c002_null_type_checks_demo.py
- referential integrity checks              -> c003_referential_integrity_demo.py
- data freshness                            -> c004_data_freshness_demo.py
- anomaly detection basics                  -> c005_anomaly_detection_demo.py

Outcome:
"Catch data problems before users do"

Folder: practice/data_quality/

---

## TRACK 14 — DATA LAKEHOUSE [COMPLETE]

Goal:
Understand the architecture replacing traditional data warehouses

Story:
"You store data in S3. Now you want ACID, time travel, and schema enforcement."

Topics:
- object storage concepts                   -> c001_object_storage_demo.py
- ACID on object storage (Delta Lake)       -> c002_delta_lake_acid_demo.py
- table formats (Iceberg concepts)          -> c003_iceberg_table_format_demo.py
- time travel queries                       -> c004_time_travel_demo.py
- compaction and optimization               -> c005_compaction_demo.py

Outcome:
"Understand why Delta Lake and Iceberg exist and when to use them"

Folder: practice/data_lakehouse/

---

## TRACK 15 — SPLUNK [DEFERRED — requires large download]

Goal:
Understand log analytics and observability at scale

Story:
"Production is down. You have 10 million log lines and 5 minutes to find the cause."

Topics:
- log ingestion and indexing concepts       -> c001_log_ingestion_demo.py
- SPL basics (Search Processing Language)   -> c002_spl_basics_demo.py
- dashboards and alerting patterns          -> c003_alerting_demo.py
- log-based anomaly detection               -> c004_log_anomaly_demo.py
- Splunk vs Elasticsearch comparison        -> c005_splunk_vs_elastic_demo.py

Outcome:
"Search and alert on operational data the way Splunk does"

Folder: practice/splunk/

Note: Splunk requires a local install or Docker image (~1GB). Complete this track when on a stable connection.

---

## FINAL TRACK — SYSTEM DESIGN [COMPLETE]

Goal:
Combine everything into one real system

Story:
"You build a real data platform"

System:
- ingestion -> relational
- cache -> Redis
- analytics -> columnar
- search -> index
- vector -> embeddings
- queue -> worker system

Final file:
c999_full_polyglot_pipeline.py

Outcome:
"You design real systems"

Folder: practice/system_design/

---

## GOLDEN RULES

1. Every file starts with a STORY
2. Every scenario must FAIL first
3. Every fix must be explained
4. Every track ends with a SYSTEM
5. Comments = layman + correct technical terms

---

## What Success Looks Like

You can:

- explain isolation without memorizing
- design cache without breaking consistency
- choose SQL vs NoSQL correctly
- reason about cost in analytics
- build streaming pipelines from scratch
- model a warehouse schema from requirements
- design real polyglot data platforms

---

## Final Mental Model

You are not learning tools.

You are building:

"A data systems brain"
