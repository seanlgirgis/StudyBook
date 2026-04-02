# Database Spiral Execution Guide

## Authority
This file is the single source of truth for database spiral planning. If any other file conflicts, follow this guide.

## Normalized Canonical Filenames
Use these canonical names in all planning and future notebook work.
- README aliases:
  - `duckdb_parquet_guide.ipynb` → `duckdb_guide.ipynb`
  - `mongodb_aggregation_deep.ipynb` → `mongodb_guide.ipynb`
  - `redis_patterns_deep.ipynb` → `redis_patterns.ipynb`
  - `cassandra_partition_design.ipynb` → `cassandra_guide.ipynb`
  - `neo4j_cypher_deep.ipynb` → `neo4j_cypher.ipynb`
  - `influxdb_flux_deep.ipynb` → `influxdb_guide.ipynb`
  - `vector_real_embeddings.ipynb` → `vector_db_guide.ipynb`
  - `elasticsearch_deep.ipynb` → `elasticsearch_guide.ipynb`
- Plan alias:
  - `db_selection_framework.ipynb` → `db_decision_framework.ipynb`

## Current Standing (Filesystem Truth)
- R0: Incomplete. Missing `_setup/cloud_setup.md`.
- R1: All 9 intro notebooks exist. All 9 concept MDs are missing.
- R2: Relational A1, A2, A3 notebooks exist (`sql_advanced_postgres.ipynb`, `sql_indexing_deep_dive.ipynb`, `sql_transactions_isolation.ipynb`). All other R2 files are missing.
- R3: `db_decision_framework.ipynb` exists; all other R3 files are missing.

## Strict Study Order (No Ambiguity)
Follow in this exact order. Do not skip ahead.

### R0 — Foundation
1. `_setup/cloud_setup.md`
2. Verify stack with `_setup/verify_all.py`

### R1 — First Contact (A through I)
1. A Relational: `sql_relational_intro.ipynb` → `relational_concepts.md`
2. B Columnar: `columnar_intro.ipynb` → `columnar_concepts.md`
3. C Document: `document_intro.ipynb` → `document_concepts.md`
4. D Key-Value: `keyvalue_intro.ipynb` → `keyvalue_concepts.md`
5. E Wide-Column: `widecolumn_intro.ipynb` → `widecolumn_concepts.md`
6. F Graph: `graph_intro.ipynb` → `graph_concepts.md`
7. G Time-Series: `timeseries_intro.ipynb` → `timeseries_concepts.md`
8. H Vector: `vector_intro.ipynb` → `vector_concepts.md`
9. I Search: `search_intro.ipynb` → `search_concepts.md`

### R2 — Deep Dive (A through I)
1. A Relational: `sql_advanced_postgres.ipynb` → `sql_indexing_deep_dive.ipynb` → `sql_transactions_isolation.ipynb` → `sql_query_optimization_live.ipynb` → `relational_qa.md` → `relational_nuggets.md` → `rds_aurora_setup.md`
2. B Columnar: `duckdb_guide.ipynb` → `snowflake_architecture.ipynb` → `bigquery_guide.ipynb` → `redshift_guide.ipynb` → `olap_comparison.ipynb` → `columnar_qa.md` → `columnar_nuggets.md`
3. C Document: `mongodb_guide.ipynb` → `dynamodb_guide.ipynb` → `document_qa.md` → `document_nuggets.md`
4. D Key-Value: `redis_patterns.ipynb` → `keyvalue_qa.md` → `keyvalue_nuggets.md`
5. E Wide-Column: `cassandra_guide.ipynb` → `widecolumn_qa.md` → `widecolumn_nuggets.md`
6. F Graph: `neo4j_cypher.ipynb` → `graph_qa.md` → `graph_nuggets.md`
7. G Time-Series: `influxdb_guide.ipynb` → `timescaledb_guide.ipynb` → `timeseries_qa.md` → `timeseries_nuggets.md`
8. H Vector: `vector_db_guide.ipynb` → `vector_qa.md` → `vector_nuggets.md`
9. I Search: `elasticsearch_guide.ipynb` → `search_qa.md` → `search_nuggets.md`

### R3 — Cloud + Decision (Fixed Order)
1. `aws_data_stores_map.ipynb`
2. `aws_cost_patterns.ipynb`
3. `gcp_data_stores.ipynb`
4. `azure_data_stores.ipynb`
5. `cloud_decision_matrix.ipynb`
6. `nosql_decision_guide.ipynb`
7. `polyglot_pipeline.ipynb`
8. `db_decision_framework.ipynb`
9. `interview_simulation.ipynb`
10. `cloud_qa.md`
11. `master_nuggets_databases.md`
12. `citi_narrative_databases.md`

## Per-Database Flow (A through I)
Each family follows the same spiral:
- R1: Intro notebook → Concepts MD
- R2: Deep notebook(s) → QA → Nuggets
- R3: Decision framework coverage (via R3-5 through R3-8)

## Exit Criteria
- R0 exit: `_setup/cloud_setup.md` exists and `_setup/verify_all.py` passes.
- R1 exit: All 9 intro notebooks complete and all 9 concepts MDs created.
- R2 exit: Every family has deep notebook(s), QA, and nuggets; relational also has `rds_aurora_setup.md`.
- R3 exit: All cloud/decision notebooks complete plus `cloud_qa.md`, `master_nuggets_databases.md`, `citi_narrative_databases.md`.

## Ready to Study Immediately
- Hands-on: `sql_transactions_isolation.ipynb` (exists, next in R2-A sequence).
- Theory-only: any missing R1 concepts MDs, plus `relational_qa.md` and `relational_nuggets.md` outlines.

## Hospital Mode Study Plan (30–60 min, Theory-Only)
- 30 min: Draft `relational_concepts.md` (MVCC, WAL, B-tree, planner; 1 paragraph each).
- 30 min: Draft `columnar_concepts.md` (columnar vs row, vectorized exec, compression).
- 45 min: Draft `document_concepts.md` (schema-less tradeoffs, embedding vs referencing, index types).
- 45 min: Draft `keyvalue_concepts.md` (TTL, eviction, cache patterns, KV vs document).
- 45 min: Draft `widecolumn_concepts.md` (partition keys, consistency, CAP tradeoffs).
- 45 min: Draft `graph_concepts.md` (nodes/edges/properties, traversal, Cypher vs SQL).
- 45 min: Draft `timeseries_concepts.md` (retention, downsampling, tag vs field).
- 45 min: Draft `vector_concepts.md` (embeddings, ANN, cosine similarity).
- 45 min: Draft `search_concepts.md` (inverted index, scoring, when search wins).
- 60 min: Outline `relational_qa.md` (first 15 Q&A bullets).
- 60 min: Outline `columnar_qa.md` (first 15 Q&A bullets).

## Gap Tracking
See `db_spiral_gap_list.md` for the authoritative missing-items list.
