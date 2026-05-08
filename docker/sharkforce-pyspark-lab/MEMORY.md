# MEMORY.md

## Project Name
sharkforce-pyspark-lab

## Purpose
Persistent local Docker lab for PySpark + Jupyter practice focused on Spark transformations, entity resolution/deduplication, data quality checks, and interview-ready demos.

## Path
`D:\Workarea\StudyBook\docker\sharkforce-pyspark-lab`

## Current Status
- Local Docker Compose environment is working.
- JupyterLab runs at `http://localhost:8888/lab`.
- PySpark works in notebooks.
- SparkSession starts in local mode (`master("local[*]")`).
- DataFrame transformation examples are validated.

## Core Commands
```powershell
cd D:\Workarea\StudyBook\docker\sharkforce-pyspark-lab
docker compose build --no-cache
docker compose up
docker compose up -d
docker compose ps
docker compose logs -f
docker compose down
docker exec -it sharkforce-pyspark-lab bash
```

## Capabilities
- Jupyter notebooks
- local PySpark with Spark DataFrames
- transformation logic (select/filter/withColumn/groupBy/join/window)
- entity resolution and dedup practice
- data quality checks
- PySpark unit-test practice under `tests`
- read/write local CSV/JSON/Parquet
- persisted artifacts via bind mounts

## Limitations
- Not Databricks.
- No Unity Catalog, Workflows, DLT, SQL Warehouse, Auto Loader.
- No production multi-node cluster behavior.
- No AWS S3/IAM integration by default.

## Persistence Rules
- Persisted data comes from Docker bind mounts.
- Full project is mounted to `/workspace/project`.
- Existing specific mounts remain for compatibility.
- Keep notebooks/data/src/tests/outputs under project folder for durable local state.

## Known Warnings (Usually Non-Fatal)
- Jupyter token/password disabled warning when running local trusted environment.
- Spark UI port message variations depending on session lifecycle.
- Minor hostname/local IP warnings can appear in local containers and still allow Spark execution.

## Databricks Relationship
This lab is a local Spark coding environment only. It supports transferable Spark coding skills but does not emulate Databricks platform services.

## Sharkforce Interview Prep Relationship
Use this lab to practice and demo:
- clean Spark transformation logic
- dedup/entity-resolution heuristics
- data quality assertions
- testable PySpark patterns
- reproducible local execution story

## StudyBook Migration Path
High-quality notebooks/scripts from this lab can later be curated into reusable StudyBook tutorials by:
- extracting reusable patterns into `src`
- adding tests in `tests`
- converting selected notebooks into tutorial-ready markdown/notebook lessons

## Exact Future Prompt for Sean
Tell me what this PySpark Docker lab is and how to use it.