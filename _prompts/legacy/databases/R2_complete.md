# Databases R2 Prompts — Complete

Generated: 2026-04-01
Total: 35 prompts (R2-A1 and R2-A2 already exist as files — no prompts needed)

## Execution order

Run notebooks (.ipynb) in ChatGPT (GPT-4o). Run .md files in either tool.
One prompt = one file. Paste the entire prompt. Do not add instructions.

| ID | Prompt file | Output file | Type | Tool | Notes |
|----|-------------|-------------|------|------|-------|
| R2-A1 | — | `sql_advanced_postgres.ipynb` | notebook | — | Already exists ✅ |
| R2-A2 | — | `sql_indexing_deep_dive.ipynb` | notebook | — | Already exists ✅ |
| R2-A3 | R2/R2-A3_sql_transactions_isolation.md | `sql_transactions_isolation.ipynb` | notebook | ChatGPT | |
| R2-A4 | R2/R2-A4_sql_query_optimization_live.md | `sql_query_optimization_live.ipynb` | notebook | ChatGPT | |
| R2-A5 | R2/R2-A5_relational_qa.md | `relational_qa.md` | QA | Either | |
| R2-A6 | R2/R2-A6_relational_nuggets.md | `relational_nuggets.md` | nuggets | Either | |
| R2-A7 | R2/R2-A7_rds_aurora_setup.md | `rds_aurora_setup.md` | guide | Either | Needs AWS creds |
| R2-B1 | R2/R2-B1_duckdb_guide.md | `duckdb_guide.ipynb` | notebook | ChatGPT | |
| R2-B2 | R2/R2-B2_snowflake_architecture.md | `snowflake_architecture.ipynb` | notebook | ChatGPT | Fill SNOWFLAKE_ACCOUNT after trial setup |
| R2-B3 | R2/R2-B3_bigquery_guide.md | `bigquery_guide.ipynb` | notebook | ChatGPT | Uses citi-de-learning GCP project |
| R2-B4 | R2/R2-B4_redshift_guide.md | `redshift_guide.ipynb` | notebook | ChatGPT | Fill REDSHIFT_HOST after cluster creation |
| R2-B5 | R2/R2-B5_olap_comparison.md | `olap_comparison.ipynb` | notebook | ChatGPT | Requires DuckDB + GCP ready |
| R2-B6 | R2/R2-B6_columnar_qa.md | `columnar_qa.md` | QA | Either | |
| R2-B7 | R2/R2-B7_columnar_nuggets.md | `columnar_nuggets.md` | nuggets | Either | |
| R2-C1 | R2/R2-C1_mongodb_guide.md | `mongodb_guide.ipynb` | notebook | ChatGPT | Fill MONGO_URI after Atlas setup |
| R2-C2 | R2/R2-C2_dynamodb_guide.md | `dynamodb_guide.ipynb` | notebook | ChatGPT | Uses AWS profile=study |
| R2-C3 | R2/R2-C3_document_qa.md | `document_qa.md` | QA | Either | |
| R2-C4 | R2/R2-C4_document_nuggets.md | `document_nuggets.md` | nuggets | Either | |
| R2-D1 | R2/R2-D1_redis_patterns.md | `redis_patterns.ipynb` | notebook | ChatGPT | Port 6380 |
| R2-D2 | R2/R2-D2_keyvalue_qa.md | `keyvalue_qa.md` | QA | Either | |
| R2-D3 | R2/R2-D3_keyvalue_nuggets.md | `keyvalue_nuggets.md` | nuggets | Either | |
| R2-E1 | R2/R2-E1_cassandra_guide.md | `cassandra_guide.ipynb` | notebook | ChatGPT | gevent reactor required |
| R2-E2 | R2/R2-E2_widecolumn_qa.md | `widecolumn_qa.md` | QA | Either | |
| R2-E3 | R2/R2-E3_widecolumn_nuggets.md | `widecolumn_nuggets.md` | nuggets | Either | |
| R2-F1 | R2/R2-F1_neo4j_cypher.md | `neo4j_cypher.ipynb` | notebook | ChatGPT | |
| R2-F2 | R2/R2-F2_graph_qa.md | `graph_qa.md` | QA | Either | |
| R2-F3 | R2/R2-F3_graph_nuggets.md | `graph_nuggets.md` | nuggets | Either | |
| R2-G1 | R2/R2-G1_influxdb_guide.md | `influxdb_guide.ipynb` | notebook | ChatGPT | |
| R2-G2 | R2/R2-G2_timescaledb_guide.md | `timescaledb_guide.ipynb` | notebook | ChatGPT | Extension may need install |
| R2-G3 | R2/R2-G3_timeseries_qa.md | `timeseries_qa.md` | QA | Either | |
| R2-G4 | R2/R2-G4_timeseries_nuggets.md | `timeseries_nuggets.md` | nuggets | Either | |
| R2-H1 | R2/R2-H1_vector_db_guide.md | `vector_db_guide.ipynb` | notebook | ChatGPT | Uses sentence-transformers (local) |
| R2-H2 | R2/R2-H2_vector_qa.md | `vector_qa.md` | QA | Either | |
| R2-H3 | R2/R2-H3_vector_nuggets.md | `vector_nuggets.md` | nuggets | Either | |
| R2-I1 | R2/R2-I1_elasticsearch_guide.md | `elasticsearch_guide.ipynb` | notebook | ChatGPT | |
| R2-I2 | R2/R2-I2_search_qa.md | `search_qa.md` | QA | Either | |
| R2-I3 | R2/R2-I3_search_nuggets.md | `search_nuggets.md` | nuggets | Either | |

## Cloud credential notes

Three prompts require credentials to be filled in before execution:

| Prompt | Variable to fill | How to get it |
|--------|-----------------|---------------|
| R2-B2 Snowflake | SNOWFLAKE_ACCOUNT | Snowflake free trial → account URL |
| R2-B4 Redshift | REDSHIFT_HOST | AWS CLI: `aws rds describe-db-clusters` after R2-A7 setup |
| R2-C1 MongoDB | MONGO_URI | Atlas free tier → Connect → Python driver string |

## Stack required

All local notebooks require the Databases Docker stack running:
```
cd D:\Workspace\Basics\Databases
docker compose --env-file _setup/env up -d
python _setup/verify_all.py
→ must print all green
```

