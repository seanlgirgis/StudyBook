# Sharkforce PySpark Lab

## What This Project Is
`sharkforce-pyspark-lab` is a local Docker-based PySpark + JupyterLab environment for hands-on Spark practice in a reproducible setup.

Primary folder:
`D:\Workarea\StudyBook\docker\sharkforce-pyspark-lab`

Docker identity:
- Image: `sharkforce-pyspark-lab:0.1`
- Container: `sharkforce-pyspark-lab`
- Jupyter URL: `http://localhost:8888/lab`

## What This Project Is Not
This project is not Databricks and does not provide Databricks-managed platform features such as:
- Databricks Workspaces/Jobs/Workflows
- Unity Catalog
- Delta Live Tables (DLT)
- Databricks SQL Warehouse
- Auto Loader
- managed Databricks clusters
- default AWS S3/IAM integration

## Why This Exists
This lab exists to support repeatable, interview-safe practice for:
- Spark DataFrame transformations
- entity resolution and deduplication logic
- data quality checks
- PySpark unit testing
- Parquet (and optional local Delta) experiments
- Sharkforce Sr. Data Engineer interview preparation
- future migration of high-value labs into StudyBook tutorials

## Build
```powershell
cd D:\Workarea\StudyBook\docker\sharkforce-pyspark-lab
docker compose build --no-cache
```

## Start (Foreground)
```powershell
docker compose up
```

## Start (Detached)
```powershell
docker compose up -d
```

## Stop
```powershell
docker compose down
```

## View Logs
```powershell
docker compose logs -f
```

## Open Jupyter
Open:
`http://localhost:8888/lab`

Jupyter root directory is configured as:
`/workspace/project`

## Persistence and Volume Mapping
The full project is mounted to:
- Windows `./` -> container `/workspace/project`

Legacy explicit mounts are also retained for compatibility:
- Windows `./notebooks` -> `/workspace/notebooks`
- Windows `./data` -> `/workspace/data`
- Windows `./src` -> `/workspace/src`
- Windows `./tests` -> `/workspace/tests`
- Windows `./outputs` -> `/workspace/outputs`

In daily use, prefer the project-root path:
- notebooks: `/workspace/project/notebooks`
- data: `/workspace/project/data`
- source code: `/workspace/project/src`
- tests: `/workspace/project/tests`
- outputs: `/workspace/project/outputs`

## First PySpark Smoke Test
Create a notebook cell in Jupyter and run:

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("sharkforce-smoke-test")
    .master("local[*]")
    .getOrCreate()
)

df = spark.createDataFrame(
    [("  Sean GIRGIS ", " austin "), ("Mariam  Ali", "DALLAS")],
    ["full_name", "city"],
)

normalized = (
    df
    .withColumn("full_name", F.regexp_replace(F.trim(F.col("full_name")), r"\\s+", " "))
    .withColumn("full_name", F.initcap(F.col("full_name")))
    .withColumn("city", F.upper(F.trim(F.col("city"))))
)

normalized.show(truncate=False)
```

Expected behavior:
- SparkSession starts on local mode.
- DataFrame operations run successfully.
- normalized output appears in notebook output.

## Interview-Safe Wording
Use this wording in interviews:
- "I built a local Docker-based PySpark lab with JupyterLab to practice Spark transformations, data quality checks, and dedup/entity-resolution patterns in a reproducible environment."
- "This setup simulates Spark coding workflows locally; it is intentionally separate from Databricks platform services such as Unity Catalog or Databricks Workflows."

## Troubleshooting
- Port conflict on `8888`:
  - Stop the process using port 8888 or change compose port mapping.
- Jupyter does not load:
  - Run `docker compose ps` and `docker compose logs -f`.
- PySpark import issues:
  - Rebuild image with `docker compose build --no-cache`.
- Kernel dies or Spark startup fails:
  - Confirm Java and PySpark versions inside container:
    - `java -version`
    - `python --version`
    - `python -c "import pyspark; print(pyspark.__version__)"`
- Files not visible in Jupyter:
  - Confirm mount exists in `docker-compose.yml` and browse under `/workspace/project`.