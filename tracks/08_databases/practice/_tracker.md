## RELATIONAL
- [x] transactions
- [x] serializable
- [x] deadlocks
- [x] query optimization
- [x] composite indexes
- [x] covering indexes
- [x] joins

## ANALYTICS
- [x] row vs column
- [x] parquet
- [x] partition pruning
- [x] cost model

## CACHE
- [x] cache aside
- [x] ttl
- [x] stampede
- [x] locks

## DISTRIBUTED
- [x] partitioning
- [x] consistency
- [x] cassandra
- [x] dynamodb

## RETRIEVAL
- [x] search
- [x] ranking
- [x] vector
- [x] hybrid
- [x] metadata filtering
- [x] bm25
- [x] reranking
- [x] top-k / recall@k

## SQL FOR DATA ENGINEERING
- [x] window functions
- [x] qualify
- [x] merge / upsert
- [x] recursive ctes
- [x] pivot / unpivot
- [x] json / array functions
- [x] dynamic sql

## SYSTEM DESIGN
- [x] final pipeline

## STREAMING
- [x] kafka concepts (producers, consumers, offsets)
- [x] consumer groups
- [x] CDC (change data capture)
- [x] event-driven ingestion pattern
- [x] at-least-once vs exactly-once delivery

## DATA MODELING
- [x] star schema
- [x] snowflake schema
- [x] SCD type 1 (overwrite)
- [x] SCD type 2 (history rows)
- [x] fact vs dimension tables
- [x] data vault basics

## ORCHESTRATION
- [x] DAG concepts and task dependencies
- [x] scheduling and triggers
- [x] retry and failure handling
- [x] backfill patterns
- [x] idempotent tasks

## DBT PATTERNS
- [x] models (staging / intermediate / marts)
- [x] incremental models
- [x] dbt tests (schema + custom)
- [x] snapshots (SCD Type 2 in dbt)
- [x] sources and freshness

## SPARK BASICS
- [x] DataFrames vs RDDs
- [x] lazy evaluation (transformations vs actions)
- [x] partitioning and shuffling
- [x] joins at scale
- [x] broadcast joins

## ELT PIPELINE PATTERNS
- [ ] staging to raw to curated layer design
- [ ] full load vs incremental load
- [ ] watermarks and high-water marks
- [ ] schema evolution
- [ ] data contracts

## DATA QUALITY
- [ ] schema validation
- [ ] null and type checks
- [ ] referential integrity checks
- [ ] data freshness
- [ ] anomaly detection basics

## DATA LAKEHOUSE
- [ ] object storage concepts
- [ ] ACID on object storage (Delta Lake concepts)
- [ ] table formats (Iceberg concepts)
- [ ] time travel queries
- [ ] compaction and optimization

## SPLUNK
- [x] log ingestion and indexing concepts
- [x] SPL (Search Processing Language) basics
- [x] dashboards and alerting patterns
- [x] log-based anomaly detection
- [x] Splunk vs Elasticsearch comparison

---

## INTERVIEW QUESTIONS
*(one INTERVIEW.md per track folder — topics listed below are covered in that file)*

### transactions/
- [x] serializable isolation + write skew + deadlock patterns
- [x] transfer happy path + rollback
- [x] dirty read + read committed + repeatable read + phantom reads
- [x] retry + idempotency + dead letter queue + reliable worker

### joins/
- [x] nested loop vs hash join + index impact
- [x] join with index vs without

### query_optimization/
- [x] bad vs good queries + EXPLAIN plan reading
- [x] index not used cases
- [x] composite indexes (left-to-right rule)
- [x] covering indexes + index-only scan

### analytics/
- [x] row vs column + parquet + partition pruning + cost model

### cache/
- [x] cache-aside + TTL + stampede + distributed locks

### distributed/
- [x] partitioning + consistency + cassandra + dynamodb patterns

### retrieval/
- [x] search / inverted index
- [x] ranking
- [x] vector similarity
- [x] hybrid search
- [x] metadata filtering
- [x] BM25
- [x] reranking + top-k

### sql_de/
- [x] window functions + qualify + merge + recursive CTEs + pivot + JSON + dynamic SQL

### streaming/
- [x] kafka + consumer groups + CDC + event-driven + delivery semantics

### modeling/
- [x] star schema + snowflake + SCD1 + SCD2 + fact vs dimension + data vault

### orchestration/
- [x] DAGs + scheduling + retry + backfill + idempotency

### dbt_patterns/
- [x] models + incremental + tests + snapshots + sources

### spark/
- [x] DataFrames vs RDDs + lazy eval + partitioning + joins + broadcast

### elt_pipeline_patterns/
- [x] staging/raw/curated + full vs incremental + watermarks + schema evolution + data contracts

### data_quality/
- [x] schema validation + null checks + referential integrity + freshness + anomaly detection

### data_lakehouse/
- [x] object storage + Delta Lake ACID + Iceberg table formats + time travel + compaction

### splunk/
- [x] log ingestion and indexing concepts
- [x] SPL basics
- [x] dashboards and alerting patterns
- [x] log-based anomaly detection
- [x] Splunk vs Elasticsearch comparison
