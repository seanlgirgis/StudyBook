# Databricks Crash Guide

## Databricks In Plain English
Databricks is a managed Spark platform for data engineering and analytics workflows using Python and SQL.

## Core Building Blocks
- Workspace: Shared area for notebooks, jobs, data assets, and permissions.
- Notebook: Interactive document for code, SQL, and notes.
- Compute: Execution resources for notebooks and jobs.
- Clusters: Configurable Spark compute.
- Serverless: Managed compute with less operational setup.

## Spark DataFrames
DataFrames are distributed table-like objects for transformations, joins, aggregations, and quality checks.

## SQL In Databricks
Use SQL for transformations, validation queries, and analyst-friendly consumption layers.

## Delta Lake And Delta Tables
- Delta Lake adds ACID transactions, schema enforcement, and table versioning on lake storage.
- Delta tables support reliable append, overwrite, and merge patterns.

## Jobs And Workflows
Workflows schedule and orchestrate notebook or task pipelines with retry and dependency control.

## Structured Streaming Basics
Structured Streaming treats incoming events as an unbounded table and processes updates in micro-batches with checkpointing.

## Unity Catalog Basics
Unity Catalog is a governance layer for data access control, catalog/schema/table organization, and lineage visibility.

## DLT Basics
Delta Live Tables is a managed framework to define declarative pipeline steps with built-in quality expectations and monitoring.

## Medallion Architecture
- Bronze: raw landing data.
- Silver: cleaned and conformed data.
- Gold: business-ready aggregates and serving tables.

## AWS S3 Integration Pattern
Common pattern:
1. Land raw files in S3.
2. Process with Databricks PySpark.
3. Write curated Delta tables.
4. Query with SQL.
5. Orchestrate with Workflows.

## Data Quality And Deduplication
Use schema checks, required-field checks, null thresholds, uniqueness tests, and reconciliation counts. For dedup, normalize keys, apply match logic, and keep survivorship rules explicit.

## Entity Resolution Example
1. Normalize name, email, and phone fields.
2. Build blocking keys to reduce candidate pairs.
3. Score candidate similarity across attributes.
4. Apply threshold bands: auto-match, review, non-match.
5. Store scores and decisions for auditability.

## Safe Interview Wording
"My strongest production depth is Python, SQL, AWS, and Spark-style data engineering. In Databricks, I have practical exposure and focused study, including notebooks, Delta tables, SQL workflows, and job patterns. I can contribute quickly while continuing to deepen Databricks platform depth in your environment."
