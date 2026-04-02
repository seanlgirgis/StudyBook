# Databases R3 Prompts — Complete

Generated: 2026-04-01
Total: 18 prompts across 6 sections

## What R3 Is

R3 is the integration and synthesis round. R1 introduced each DB type. R2 deep-dived each DB type individually.
R3 combines them: cross-database patterns, pipelines, performance tuning, consistency models, system design, and master review.

## Execution order

Run notebooks (.ipynb) in ChatGPT (GPT-4o). Run .md files in either tool.
One prompt = one file. Paste the entire prompt. Do not add instructions.

| ID | Prompt file | Output file | Type | Tool | Notes |
|----|-------------|-------------|------|------|-------|
| R3-A1 | R3/R3-A1_polyglot_persistence.md | `polyglot_persistence.ipynb` | notebook | ChatGPT | Requires full Docker stack + all 8 DBs |
| R3-A2 | R3/R3-A2_database_selection.md | `database_selection.ipynb` | notebook | ChatGPT | Requires Postgres + DuckDB + ES |
| R3-A3 | R3/R3-A3_architecture_qa.md | `architecture_qa.md` | QA | Either | |
| R3-A4 | R3/R3-A4_architecture_nuggets.md | `architecture_nuggets.md` | nuggets | Either | |
| R3-B1 | R3/R3-B1_cdc_pipeline.md | `cdc_pipeline.ipynb` | notebook | ChatGPT | Requires Postgres + Redis + ES |
| R3-B2 | R3/R3-B2_etl_s3_pipeline.md | `etl_s3_pipeline.ipynb` | notebook | ChatGPT | Requires Postgres + S3 + Redshift; AWS profile=study |
| R3-B3 | R3/R3-B3_pipeline_qa.md | `pipeline_qa.md` | QA | Either | |
| R3-B4 | R3/R3-B4_pipeline_nuggets.md | `pipeline_nuggets.md` | nuggets | Either | |
| R3-C1 | R3/R3-C1_indexing_master.md | `indexing_master.ipynb` | notebook | ChatGPT | Requires Postgres + Cassandra + ES + Redshift |
| R3-C2 | R3/R3-C2_query_execution.md | `query_execution.ipynb` | notebook | ChatGPT | Requires Postgres + DuckDB |
| R3-C3 | R3/R3-C3_performance_qa.md | `performance_qa.md` | QA | Either | |
| R3-C4 | R3/R3-C4_performance_nuggets.md | `performance_nuggets.md` | nuggets | Either | |
| R3-D1 | R3/R3-D1_consistency_models.md | `consistency_models.ipynb` | notebook | ChatGPT | Requires Postgres + Cassandra + Redis |
| R3-D2 | R3/R3-D2_replication_patterns.md | `replication_patterns.ipynb` | notebook | ChatGPT | Requires Postgres + Cassandra + Redis |
| R3-D3 | R3/R3-D3_ha_qa.md | `ha_qa.md` | QA | Either | |
| R3-D4 | R3/R3-D4_ha_nuggets.md | `ha_nuggets.md` | nuggets | Either | |
| R3-E1 | R3/R3-E1_system_design_citi.md | `system_design_citi.ipynb` | notebook | ChatGPT | Requires Postgres + Redis + Cassandra + ES + InfluxDB + DuckDB |
| R3-E2 | R3/R3-E2_system_design_qa.md | `system_design_qa.md` | QA | Either | |
| R3-F1 | R3/R3-F1_master_qa.md | `master_qa.md` | QA | Either | 80 questions — full curriculum review |
| R3-F2 | R3/R3-F2_master_nuggets.md | `master_nuggets.md` | nuggets | Either | 60 nuggets — full curriculum review |

## Section summary

| Section | Theme | Notebooks | QA/Nuggets |
|---------|-------|-----------|------------|
| R3-A | Polyglot Persistence & Architecture | 2 | 2 |
| R3-B | Data Pipelines & CDC | 2 | 2 |
| R3-C | Indexing & Performance | 2 | 2 |
| R3-D | Consistency & Replication | 2 | 2 |
| R3-E | System Design | 1 notebook + 1 QA | — |
| R3-F | Master Review | — | 2 (80 Q + 60 nuggets) |

## Cloud credential notes

Two prompts require cloud access:

| Prompt | Credentials needed |
|--------|-------------------|
| R3-B2 ETL Pipeline | AWS profile=study, S3=citi-telemetry-data-lake-dev, Redshift=default-workgroup.357811130281.us-east-1.redshift-serverless.amazonaws.com |
| R3-C1 Indexing Master | Redshift=default-workgroup.357811130281.us-east-1.redshift-serverless.amazonaws.com (de_admin/DeAdmin2026!) |

All other notebooks use only the local Docker stack.

## Stack required for local notebooks

```
cd D:\Workspace\Basics\Databases
docker compose --env-file _setup/env up -d
python _setup/verify_all.py
→ must print all green before running any R3 notebook
```

