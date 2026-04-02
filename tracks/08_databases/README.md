# Databases — Master Study Guide
**Owner:** Sean Girgis | Dallas, TX | Senior Data Engineer / AI Architect  
**Mantra:** Simplicity and clarity is Gold.

---

## What this folder is

Your complete database mastery curriculum. Nine categories covering every database
type a Staff/Principal DE needs to know — from Postgres internals to graph traversal
to vector similarity search. Every notebook connects to the same Citi telemetry
dataset (10K endpoints, 500K metrics, 25K alerts) so you can compare apples to apples
across every database type.

---

## How to use this

1. **Start here every session** — read this file first
2. **Check "What to study next"** below — one clear instruction
3. **Open the notebook** — run every cell, read every comment
4. **Fill in the Key Observations cell** — write your own words, not the pre-filled text
5. **Update the plan** — hand `db_mastery_plan.md` to Claude Code after each notebook
6. **Add nuggets** — anything surprising or hard-won goes in `database_nuggets.md`

---

## ▶ WHAT TO STUDY NEXT

> **Round 2 — Relational Deep Dive**  
> Open: `sql_indexing_deep_dive.ipynb` (R2-A2, just completed) then start `R2-A3`  
> Topic: Transaction isolation levels — read committed, repeatable read, serializable · deadlock simulation  
> Notebook to generate: `sql_transactions_isolation.ipynb`  
> Command to give Antigravity:  
> *"Read prompts/agent_rules.md — generate Basics/Databases/sql_transactions_isolation.ipynb — R2-A3 per db_mastery_plan.md"*

---

## Round Status

| Round | Description | Status |
|-------|-------------|--------|
| R0 | Infrastructure — Docker stack, seed data, connections | ✅ Complete |
| R1 | First contact — all 9 categories, live queries | ✅ Complete |
| R2 | Deep dive — internals, QA, nuggets per category | 🔄 In Progress (2 of 12 done) |
| R3 | Cloud native, polyglot pipeline, interview simulation | ⬜ Not started |

---

## The 9 Categories — What They Are and When to Use Them

| # | Category | Best DB | Use When |
|---|----------|---------|----------|
| A | **Relational** | PostgreSQL | Structured data, joins, ACID transactions, reporting |
| B | **Columnar / OLAP** | DuckDB / Snowflake | Analytics, aggregations, wide tables, read-heavy |
| C | **Document** | MongoDB | Flexible schema, nested/hierarchical data, evolving structure |
| D | **Key-Value** | Redis | Caching, session storage, counters, sub-millisecond lookups |
| E | **Wide-Column** | Cassandra | Time-series, write-heavy, data partitioned by ID + time |
| F | **Graph** | Neo4j | Dependencies, fraud detection, network topology, recommendations |
| G | **Time-Series** | InfluxDB | Metrics, sensor data, anything with timestamp as primary axis |
| H | **Vector** | pgvector | Semantic search, RAG pipelines, similarity, deduplication |
| I | **Search** | Elasticsearch | Full-text search, log analytics, relevance ranking, fuzzy match |

---

## Notebook Inventory

### Round 1 — First Contact (all complete ✅)

| File | Category | Status | Key Thing Learned |
|------|----------|--------|-------------------|
| `sql_relational_intro.ipynb` | Relational | ✅ | EXPLAIN shows seq scan on metrics — index opportunity |
| `columnar_intro.ipynb` | Columnar | ✅ | DuckDB over attached Postgres ≠ columnar I/O — Parquet is the real test |
| `document_intro.ipynb` | Document | ✅ | Aggregation pipeline chains like Unix pipes — no schema needed |
| `keyvalue_intro.ipynb` | Key-Value | ✅ | LPUSH+LTRIM = bounded queue — cache-aside is the DE pattern |
| `widecolumn_intro.ipynb` | Wide-Column | ✅ | Partition key is everything — ALLOW FILTERING cost depends on it |
| `graph_intro.ipynb` | Graph | ✅ | *1..2 = 2-hop traversal in one token — found 2 real cycles in seed data |
| `timeseries_intro.ipynb` | Time-Series | ✅ | sort()+limit() is per-series — group() first for global top-N |
| `vector_intro.ipynb` | Vector | ✅ | HNSW index + <=> operator — real embeddings come in Round 2 |
| `search_intro.ipynb` | Search | ✅ | bool query = must+filter+should — BM25 relevance ranking built in |

### Round 2 — Deep Dive (not started)

| ID | File | Category | Status |
|----|------|----------|--------|
| R2-A1 | `sql_advanced_postgres.ipynb` | Relational | 🔄 |
| R2-A2 | `sql_indexing_deep_dive.ipynb` | Relational | ✅ |
| R2-A3 | `sql_transactions_isolation.ipynb` | Relational | ⬜ |
| R2-A4 | `sql_query_optimization_live.ipynb` | Relational | ⬜ |
| R2-B1 | `duckdb_parquet_guide.ipynb` | Columnar | ⬜ |
| R2-C1 | `mongodb_aggregation_deep.ipynb` | Document | ⬜ |
| R2-D1 | `redis_patterns_deep.ipynb` | Key-Value | ⬜ |
| R2-E1 | `cassandra_partition_design.ipynb` | Wide-Column | ⬜ |
| R2-F1 | `neo4j_cypher_deep.ipynb` | Graph | ⬜ |
| R2-G1 | `influxdb_flux_deep.ipynb` | Time-Series | ⬜ |
| R2-H1 | `vector_real_embeddings.ipynb` | Vector | ⬜ |
| R2-I1 | `elasticsearch_deep.ipynb` | Search | ⬜ |

---

## Key Resources

| File | What it is |
|------|-----------|
| `db_mastery_plan.md` | Full project plan — all rounds, all deliverables, status |
| `database_nuggets.md` | Field manual — hard-won gotchas, one tight insight per entry |
| `_setup/db_connections.py` | Connection helpers for all 8 databases — import and go |
| `_setup/verify_all.py` | Health check — run after any infrastructure change |
| `_setup/env` | All credentials — never commit, already gitignored |

---

## Live Stack

| Service | Port | Status |
|---------|------|--------|
| PostgreSQL 16 | 5432 | ✅ |
| Redis 7 | 6379 | ✅ |
| Cassandra 4.1 | 9042 | ✅ |
| Neo4j 5 | 7474 / 7687 | ✅ |
| InfluxDB 2.7 | 8086 | ✅ |
| Elasticsearch 8.12 | 9200 | ✅ |
| Kibana 8.12 | 5601 | ✅ |
| MongoDB Atlas | cloud | ✅ |

Start stack: `docker compose --env-file env up -d`  
From: `D:\Workspace\Basics\Databases\_setup\`

---

## Nuggets Filed So Far

| # | Topic | One-line summary |
|---|-------|-----------------|
| 1 | Cassandra / Python 3.12 / Windows | Use `import asyncore` (pyasyncore) — gevent breaks Jupyter |
| 2 | Cassandra / ALLOW FILTERING | With partition key = cheap. Without = full cluster scan. Same error. |
| 3 | DuckDB / Attached Postgres | Wire protocol — not columnar I/O. Real benchmark is Parquet. |
| 4 | Redis / LPUSH+LTRIM | Bounded queue in 2 atomic commands. No cleanup job needed. |
| 5 | Neo4j / Variable-length paths | `*1..2` = 2 hops. SQL needs recursive CTE + anti-cycle guard. |
| 6 | InfluxDB / sort()+limit() | Per-series, not global. Need group() first for true top-N. |
| 7 | InfluxDB / Tag cardinality | Tags = indexed. UUIDs as tags = OOM. Keep tag cardinality low. |

Full details: `database_nuggets.md`

---

*Last updated: 2026-03-23*  
*Simplicity and clarity is Gold.*
