# Database Mastery — Project Plan
**Owner:** Sean Girgis  
**Started:** 2026-03-23  
**Last updated:** 2026-03-23  
**Location:** `Basics\Databases\`  
**Strategy:** Parallel spiral — all 9 categories advance together round by round  
**Mantra:** Simplicity and clarity is Gold.

---

## How to use this file

- Update `Status` as work completes: `⬜ Not Started` → `🔄 In Progress` → `✅ Done`
- Update `Notes` with anything useful — what worked, what to revisit, cloud costs
- **Always pull fresh from repo before handing to Claude** — stale plan = wrong decisions
- Hand this file to Claude when starting a session — full context in one file
- Claude updates this file after generating any deliverable

---

## Stack at a glance

| Layer | What | How | Status |
|-------|------|-----|--------|
| Local | Postgres, Redis, Cassandra, Neo4j, InfluxDB, Elasticsearch + Kibana | Docker Compose | ✅ Running |
| Free cloud forever | MongoDB Atlas, DynamoDB, Firestore, Pinecone, BigQuery, Neo4j AuraDB | Free tier accounts | ⬜ |
| AWS credits | RDS, Aurora, Redshift, Timestream, ElastiCache, Neptune, OpenSearch | Existing account | ⬜ |
| GCP credits | Bigtable, Spanner, AlloyDB | Create account | ⬜ |
| Azure | Cosmos DB, Synapse, Azure SQL | Student account | ⬜ |
| Data spine | Citi telemetry dataset — endpoints, metrics, alerts, events | Same data in every DB | ✅ Seeded (10K endpoints · 500K metrics · 25K alerts) |

### Live Docker containers

| Container | Service | Port | Status |
|-----------|---------|------|--------|
| de_postgres | PostgreSQL 16 | 5432 | ✅ healthy |
| de_redis | Redis 7 | 6379 | ✅ healthy |
| de_cassandra | Cassandra 4.1 | 9042 | ✅ healthy |
| de_neo4j | Neo4j 5 | 7474 / 7687 | ✅ healthy |
| de_influxdb | InfluxDB 2.7 | 8086 | ✅ healthy |
| de_elasticsearch | Elasticsearch 8.12 | 9200 | ✅ healthy |
| de_kibana | Kibana 8.12 | 5601 | ✅ healthy |

**Run command:** `docker compose --env-file env up -d`  
**Data location:** `D:\Workspace\Basics\Databases\_setup\volumes\`  
**Credentials:** `D:\Workspace\Basics\Databases\_setup\env`

---

## ROUND 0 — Foundation (do once, unlocks everything)

> Goal: one `docker compose up` starts everything. Same seed data in every DB. Every connection verified.

| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R0-1 | `_setup/docker-compose.yml` | infra | ✅ | 7 containers healthy on D drive |
| R0-2 | `_setup/master_seed_data.py` | script | ✅ | 10K endpoints · 500K metrics · 25K alerts seeded; Cassandra 1M rows |
| R0-3 | `_setup/db_connections.py` | script | ✅ | All 7 connections passing (gevent reactor for Cassandra on Python 3.12) |
| R0-4 | `_setup/verify_all.py` | script | ✅ | ALL GREEN — PG 10K endpoints · Redis 10K keys · Cassandra 1M metrics · Neo4j 10K nodes · InfluxDB 5K points · ES 25K alerts |
| R0-5 | `_setup/cloud_setup.md` | guide | ⬜ | Step-by-step: MongoDB Atlas · DynamoDB · BigQuery · Pinecone · GCP · Azure |
| R0-6 | `_setup/README.md` | guide | ✅ | Deployed with stack |
| R0-7 | `_setup/env` | config | ✅ | All credentials — rename to .env for standard usage |
| R0-8 | `_setup/requirements_databases.txt` | config | ✅ | 70+ packages installed in proj_educate venv |
| R0-9 | `_setup/create_volumes.ps1` | script | ✅ | 13 volume dirs created on D drive |

**Round 0 complete when:** `verify_all.py` prints all green. **Currently: 7/9 items done.** R0-5 (cloud setup) and R0-6 (README) remain.

---

## ROUND 1 — First contact (concept + connect + first real query)

> Goal: for every category, understand the mental model, spin up the DB, run a meaningful query against the telemetry data.
> **Blocked by:** R0-2 (seed data) and R0-3 (db_connections.py) must be done first.

### 1A. Relational
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R1-A1 | `sql_relational_intro.ipynb` | notebook | ✅ | 5 queries live on telemetry data · EXPLAIN shows seq scan on metrics — index opportunity noted |
| R1-A2 | `relational_concepts.md` | concepts | ⬜ | MVCC, WAL, B-tree index, query planner — one paragraph each |

### 1B. Columnar / OLAP
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R1-B1 | `columnar_intro.ipynb` | notebook | ✅ | DuckDB attached to Postgres · 4 queries timed · comparison table in cell 10 · Parquet benchmark reserved for R2 |
| R1-B2 | `columnar_concepts.md` | concepts | ⬜ | Columnar vs row storage · vectorized execution · compression |

### 1C. Document
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R1-C1 | `document_intro.ipynb` | notebook | 🔄 | Document model · MongoDB · telemetry as JSON documents |
| R1-C2 | `document_concepts.md` | concepts | ⬜ | Schema-less tradeoffs · embedding vs referencing · index types |

### 1D. Key-Value
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R1-D1 | `keyvalue_intro.ipynb` | notebook | 🔄 | Redis data structures · cache the telemetry endpoint lookup |
| R1-D2 | `keyvalue_concepts.md` | concepts | ⬜ | When KV wins · TTL · eviction · Redis vs Memcached |

### 1E. Wide-Column
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R1-E1 | `widecolumn_intro.ipynb` | notebook | 🔄 | Cassandra mental model · CQL · write telemetry metrics |
| R1-E2 | `widecolumn_concepts.md` | concepts | ⬜ | Partition key design · consistency levels · CAP position |

### 1F. Graph
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R1-F1 | `graph_intro.ipynb` | notebook | 🔄 | Neo4j · endpoint dependencies as graph · first Cypher |
| R1-F2 | `graph_concepts.md` | concepts | ⬜ | Nodes/edges/properties · when graph wins · Cypher vs SQL |

### 1G. Time-Series
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R1-G1 | `timeseries_intro.ipynb` | notebook | 🔄 | InfluxDB · write telemetry metrics with timestamps · first Flux query |
| R1-G2 | `timeseries_concepts.md` | concepts | ⬜ | Time-series data model · retention · downsampling · Citi narrative |

### 1H. Vector
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R1-H1 | `vector_intro.ipynb` | notebook | ✅ | pgvector · embed telemetry alert text · first similarity search |
| R1-H2 | `vector_concepts.md` | concepts | ⬜ | Embeddings · ANN · cosine similarity · RAG connection |

### 1I. Search
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R1-I1 | `search_intro.ipynb` | notebook | ✅ | ES match, bool, aggs, fuzzy, multi_match+date range · 25K alerts · Kibana at 5601 |
| R1-I2 | `search_concepts.md` | concepts | ⬜ | Inverted index · relevance scoring · when search wins vs SQL LIKE |

**Round 1 complete when:** All 9 categories have a working notebook with live queries. **ALL 9 notebooks complete ✅**

---

## ROUND 2 — Deep notebooks + QA + nuggets

> Goal: full master guide notebook per category, 30+ interview Q&A, gotcha nuggets.

### 2A. Relational
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R2-A1 | `sql_advanced_postgres.ipynb` | notebook | ✅ | MVCC · WAL · VACUUM · EXPLAIN before/after index · partitioning · interview Q&A |
| R2-A2 | `sql_indexing_deep_dive.ipynb` | notebook | ✅ | B-tree · Hash · GIN · Partial · index audit · 6 interview Q&A |
| R2-A3 | `sql_transactions_isolation.ipynb` | notebook | ⬜ | Isolation levels · deadlock simulation · MVCC internals |
| R2-A4 | `sql_query_optimization_live.ipynb` | notebook | ⬜ | Real EXPLAIN plans on telemetry · 10 optimization drills |
| R2-A5 | `relational_qa.md` | QA | ⬜ | 40 Q&A: indexes, isolation, EXPLAIN, replication, partitioning |
| R2-A6 | `relational_nuggets.md` | nuggets | ⬜ | NULL in indexes · LIKE vs ILIKE · seq scan surprises · VACUUM timing |
| R2-A7 | `rds_aurora_setup.md` | cloud | ⬜ | Connect notebooks to AWS RDS · Aurora Serverless setup |

### 2B. Columnar / OLAP
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R2-B1 | `duckdb_guide.ipynb` | notebook | ⬜ | Columnar internals · vectorized execution · Parquet queries |
| R2-B2 | `snowflake_architecture.ipynb` | notebook | ⬜ | Virtual warehouses · micro-partitions · Time Travel · zero-copy clone |
| R2-B3 | `bigquery_guide.ipynb` | notebook | ⬜ | Slots · partitioning · clustering · cost control · cost anti-patterns |
| R2-B4 | `redshift_guide.ipynb` | notebook | ⬜ | Distribution keys · sort keys · COPY · Spectrum · RA3 nodes |
| R2-B5 | `olap_comparison.ipynb` | notebook | ⬜ | Same query: DuckDB vs Snowflake vs BigQuery — time + cost |
| R2-B6 | `columnar_qa.md` | QA | ⬜ | 30 Q&A: columnar vs row, MPP, Snowflake pricing, BigQuery slots |
| R2-B7 | `columnar_nuggets.md` | nuggets | ⬜ | Snowflake credit burn · BigQuery partition pruning · DuckDB sweet spot |

### 2C. Document
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R2-C1 | `mongodb_guide.ipynb` | notebook | ⬜ | Aggregation pipeline · indexes · Atlas search · transactions |
| R2-C2 | `dynamodb_guide.ipynb` | notebook | ⬜ | Partition design · GSI · LSI · single-table · streams |
| R2-C3 | `document_qa.md` | QA | ⬜ | 30 Q&A: embedding vs referencing, hot partitions, GSI tradeoffs |
| R2-C4 | `document_nuggets.md` | nuggets | ⬜ | DynamoDB hot partition trap · Mongo index intersection · $lookup cost |

### 2D. Key-Value
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R2-D1 | `redis_patterns.ipynb` | notebook | ⬜ | Data structures · pub/sub · Lua scripts · cache-aside · write-through |
| R2-D2 | `keyvalue_qa.md` | QA | ⬜ | 25 Q&A: cache patterns, Redis vs Memcached, TTL strategy, eviction |
| R2-D3 | `keyvalue_nuggets.md` | nuggets | ⬜ | Cache stampede · thundering herd · Redis single-thread myth |

### 2E. Wide-Column
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R2-E1 | `cassandra_guide.ipynb` | notebook | ⬜ | Partition design · CQL · consistency levels · compaction · tombstones |
| R2-E2 | `widecolumn_qa.md` | QA | ⬜ | 25 Q&A: partition key design, consistency tradeoffs, compaction |
| R2-E3 | `widecolumn_nuggets.md` | nuggets | ⬜ | Tombstone accumulation · wide partition · quorum math |

### 2F. Graph
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R2-F1 | `neo4j_cypher.ipynb` | notebook | ⬜ | Cypher patterns · MATCH/MERGE/CREATE · fraud detection queries |
| R2-F2 | `graph_qa.md` | QA | ⬜ | 20 Q&A: when graph wins, Cypher vs SQL, Neptune vs Neo4j |
| R2-F3 | `graph_nuggets.md` | nuggets | ⬜ | Supernode problem · relationship direction · graph vs relational |

### 2G. Time-Series
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R2-G1 | `influxdb_guide.ipynb` | notebook | ⬜ | Measurements · tags · fields · continuous queries · Flux |
| R2-G2 | `timescaledb_guide.ipynb` | notebook | ⬜ | Hypertables · compression · continuous aggregates |
| R2-G3 | `timeseries_qa.md` | QA | ⬜ | 25 Q&A: time-series vs relational, retention, downsampling |
| R2-G4 | `timeseries_nuggets.md` | nuggets | ⬜ | Cardinality explosion · tag vs field · retention cost math |

### 2H. Vector
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R2-H1 | `vector_db_guide.ipynb` | notebook | ⬜ | Embeddings · ANN · HNSW · IVFFlat · pgvector vs Pinecone vs Chroma |
| R2-H2 | `vector_qa.md` | QA | ⬜ | 20 Q&A: ANN vs exact, HNSW tradeoffs, RAG pipeline design |
| R2-H3 | `vector_nuggets.md` | nuggets | ⬜ | Dimensionality curse · recall vs latency · index rebuild cost |

### 2I. Search
| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R2-I1 | `elasticsearch_guide.ipynb` | notebook | ⬜ | Inverted index · mappings · aggregations · relevance tuning |
| R2-I2 | `search_qa.md` | QA | ⬜ | 20 Q&A: ES vs SQL LIKE, shard sizing, mapping explosion |
| R2-I3 | `search_nuggets.md` | nuggets | ⬜ | Mapping explosion · shard rebalancing · near-real-time lag |

**Round 2 complete when:** Every category has deep notebook(s) + QA + nuggets.

---

## ROUND 3 — Cloud native + decision frameworks + capstone

> Goal: AWS/GCP/Azure depth, cross-category comparison, polyglot architecture, interview simulation.

| ID | Deliverable | Type | Status | Notes |
|----|-------------|------|--------|-------|
| R3-1 | `aws_data_stores_map.ipynb` | notebook | ⬜ | RDS/Aurora/DynamoDB/ElastiCache/Timestream/Neptune/OpenSearch |
| R3-2 | `aws_cost_patterns.ipynb` | notebook | ⬜ | Cost anti-patterns · right-sizing · reserved vs on-demand |
| R3-3 | `gcp_data_stores.ipynb` | notebook | ⬜ | BigQuery/Bigtable/Firestore/Spanner/AlloyDB |
| R3-4 | `azure_data_stores.ipynb` | notebook | ⬜ | Cosmos DB/Synapse/Azure SQL — student account |
| R3-5 | `cloud_decision_matrix.ipynb` | notebook | ⬜ | Given a workload — which cloud, which service, why |
| R3-6 | `nosql_decision_guide.ipynb` | notebook | ⬜ | Document vs KV vs Wide-col vs Graph — decision tree |
| R3-7 | `polyglot_pipeline.ipynb` | notebook | ⬜ | One pipeline: ingest→Postgres · cache→Redis · search→ES · embed→pgvector |
| R3-8 | `db_selection_framework.ipynb` | notebook | ⬜ | Complete decision tree for any workload type |
| R3-9 | `interview_simulation.ipynb` | notebook | ⬜ | 60 questions across all categories · timed · self-graded |
| R3-10 | `cloud_qa.md` | QA | ⬜ | 30 scenarios: "which service would you use for X?" |
| R3-11 | `master_nuggets_databases.md` | nuggets | ⬜ | All nuggets consolidated — the master reference |
| R3-12 | `citi_narrative_databases.md` | narrative | ⬜ | Map every DB category to Citi telemetry work |

**Round 3 complete when:** You can walk an interviewer through the polyglot pipeline and justify every DB choice.

---

## Progress Summary

| Category | R0 | R1 | R2 | R3 |
|----------|----|----|----|----|
| Foundation | ✅ | — | — | — |
| Relational | — | ✅ | ⬜ | ⬜ |
| Columnar | — | ✅ | ⬜ | ⬜ |
| Document | — | ✅ | ⬜ | ⬜ |
| Key-Value | — | ✅ | ⬜ | ⬜ |
| Wide-Column | — | ✅ | ⬜ | ⬜ |
| Graph | — | ✅ | ⬜ | ⬜ |
| Time-Series | — | ✅ | ⬜ | ⬜ |
| Vector | — | ✅ | ⬜ | ⬜ |
| Search | — | ✅ | ⬜ | ⬜ |

---

## Deliverable counts

| Round | Notebooks | Concept MDs | QA files | Nugget files | Setup/Cloud | Total |
|-------|-----------|-------------|----------|--------------|-------------|-------|
| R0 | 0 | 0 | 0 | 0 | 6 | 6 |
| R1 | 9 | 9 | 0 | 0 | 0 | 18 |
| R2 | 22 | 0 | 9 | 9 | 2 | 42 |
| R3 | 9 | 0 | 1 | 1 | 0 | 11 |
| **Total** | **40** | **9** | **10** | **10** | **8** | **77** |

---

## Active work log

| Date | What was done | By |
|------|--------------|-----|
| 2026-03-23 | Project plan created | Claude |
| 2026-03-23 | docker-compose.yml — 7 containers deployed and healthy on D drive | Claude + Claude Code |
| 2026-03-23 | README.md, env, requirements_databases.txt, create_volumes.ps1 deployed | Claude + Claude Code |
| 2026-03-23 | 13 volume directories created on D drive | Claude Code |
| 2026-03-23 | 70+ Python DB packages installed in proj_educate venv | Claude Code |
| 2026-03-23 | Kibana kibana_system password set to DeKibana2026! | Claude Code |
| 2026-03-23 | db_connections.py — all 7 DBs passing (gevent reactor fixed Cassandra on Python 3.12/Windows) | Claude Code |
| 2026-03-23 | master_seed_data.py — Citi telemetry seeded: 10K endpoints, 500K metrics, 25K alerts into 6 live DBs | Claude Code |
| 2026-03-23 | verify_all.py — ALL GREEN: PG 10K · Redis 10K · Cassandra 1M · Neo4j 10K · InfluxDB 5K · ES 25K | Claude Code |
| 2026-03-23 | sql_relational_intro.ipynb created — R1-A1 in progress (10 cells, 5 live telemetry queries + EXPLAIN ANALYZE) | Claude Code |
| 2026-03-23 | R1-A1: sql_relational_intro.ipynb complete, all queries live | Claude Code |
| 2026-03-23 | R1-B1: columnar_intro.ipynb generated | Claude Code |
| 2026-03-23 | R1-B1: columnar_intro.ipynb complete | Claude Code |
| 2026-03-23 | R1-C1: document_intro.ipynb generated, MongoDB Atlas connected | Claude Code |
| 2026-03-23 | R1-D1: keyvalue_intro.ipynb generated | Claude Code |
| 2026-03-23 | R1-E1: widecolumn_intro.ipynb generated | Claude Code |
| 2026-03-23 | R1-F1: graph_intro.ipynb generated | Claude Code |
| 2026-03-23 | R1-G1: timeseries_intro.ipynb generated | Claude Code |
| 2026-03-23 | R1-H1: vector_intro.ipynb generated | Claude Code |
| 2026-03-23 | R1-I1: search_intro.ipynb generated — 12 cells, 5 ES queries (match, bool, aggs, fuzzy, multi_match+range) | Claude Code |
| 2026-04-01 | R2 prompts completed — 35 files in Basics\Databases\prompts\R2\ | Claude |
| 2026-04-01 | R0_complete.md + R1_complete.md created — inventory of directly-built R0/R1 deliverables | Claude |
| 2026-03-23 | Round 1 COMPLETE — all 9 category notebooks generated | Claude |
| 2026-03-23 | R2-A1: sql_advanced_postgres.ipynb generated | Claude Code |
| 2026-03-24 | R2-A2: sql_indexing_deep_dive.ipynb generated | Antigravity |
| 2026-03-24 | R2-A2: GIN cells patched in, notebook complete | Antigravity |

---

## Decisions log

| Date | Decision | Reason |
|------|----------|--------|
| 2026-03-23 | Parallel spiral — all 9 categories advance together | Jack of all trades first, then deepen |
| 2026-03-23 | Citi telemetry as master dataset | Same data in every DB — enables real comparison |
| 2026-03-23 | Docker local + free cloud tiers | Zero cost until Round 3 |
| 2026-03-23 | Lives in `Basics\Databases\` | Databases are foundational, not specialty |
| 2026-03-23 | Elasticsearch + Kibana not OpenSearch | Better community, can add OpenSearch later for AWS depth |
| 2026-03-23 | All volumes on D drive | Larger drive, no space issues, persists across rebuilds |
| 2026-03-23 | Claude = architect, Claude Code = executor | Plan file is the shared source of truth between all three |

---

## Next — R0 remaining (give this to Claude Code)

```
Read prompts/agent_rules.md — then generate these 3 files
in D:\Workspace\Basics\Databases\_setup\

1. db_connections.py
   - Connection helpers for: Postgres, Redis, Cassandra, Neo4j,
     InfluxDB, Elasticsearch, DuckDB
   - Load credentials from env file using python-dotenv
   - Each DB: get_<name>_connection() function
   - Each DB: test_<name>_connection() → True/False
   - Single test_all_connections() that prints a table

2. master_seed_data.py
   - Generates Citi telemetry dataset using Faker + tqdm
   - Tables/collections: endpoints (10K), metrics (1M),
     alerts (50K), events (100K)
   - Loads into: Postgres, Redis, Cassandra, Neo4j,
     InfluxDB, Elasticsearch
   - Reads credentials from env file
   - Idempotent — safe to run multiple times

3. verify_all.py
   - Imports db_connections.py
   - Connects to all 7 DBs (including DuckDB local)
   - Prints pass/fail table with latency
   - Exit code 0 if all pass, 1 if any fail

After generating, run:
  python verify_all.py
Report the output. Then run gitq.
```

---

*Last updated: 2026-03-23*  
*Simplicity and clarity is Gold.*
