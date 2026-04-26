# PySpark With Docker - Educational Tutorial

This tutorial series teaches PySpark fundamentals using a Dockerized Spark cluster instead of a fragile local Windows Spark setup.

## Why This Tutorial Uses Docker

Local Windows Spark setups often fail because of Java conflicts, Hadoop/winutils friction, or Python worker instability. Here we connect a local Python driver to a Docker Spark master so we can focus on learning Spark itself.

## Learning Goals

By the end of this tutorial track, you will be able to:

- Connect a Python client to a Spark standalone cluster.
- Build DataFrame-first transformations.
- Read physical plans and reason about shuffles.
- Compare join strategies including broadcast joins.
- Use partitioning, cache/persist, and skew diagnostics.
- Implement a Bronze/Silver/Gold mini pipeline.
- Inspect jobs in Spark UI.

## Collaboration Model (You + Codex + ChatGPT)

- You: decide direction, run scripts, ask questions.
- Codex: implement files, keep repo structure clean, maintain continuity artifacts.
- ChatGPT: explain concepts, quiz/interview practice, clarify confusion.

Use this loop for each lesson:

1. Run script.
2. Capture output snippets and Spark UI observations.
3. Record what you learned and one open question.
4. Move to next file only after concepts are clear.

## Prerequisites

- Docker Desktop running.
- Spark cluster container(s) running with master URL reachable.
- Python virtual environment active (your `proj_educate` env is fine).
- Install dependencies:

```powershell
pip install -r .\requirements.txt
```

## Version Compatibility Rule (Critical)

`pyspark` version in your venv must exactly match the Spark Docker image version on both master and worker.

Current tutorial baseline:

- Docker images: `apache/spark:3.5.3`
- Python package: `pyspark==3.5.3`

If these differ (for example `pyspark 3.5.4` with cluster `3.5.3`), jobs can fail with serialization errors such as `InvalidClassException` / `serialVersionUID` mismatch.

## Verify Cluster Availability

```powershell
docker ps
```

Confirm Spark master is reachable at `spark://localhost:7077`.

Spark UI is usually one of:

- `http://localhost:8080`
- `http://localhost:8086`

## Current Implemented Lesson Files

- `common/spark_session.py`
- `01_cluster_connection.py`
- `02_dataframe_operations.py`
- `03_sql_and_views.py`
- `04_joins_and_broadcast.py`
- `05_shuffle_partitions_cache.py`
- `06_bronze_silver_gold_pipeline.py`
- `07_spark_ui_experiments.py`

## Docker Deep Dive Pack

For Docker-focused teaching notes, deployment paths, and runnable templates, see:

- [`docker/README.md`](./docker/README.md)

## Run Lesson 01

```powershell
python -u .\01_cluster_connection.py
```

Expected highlights:

- Spark version prints.
- Master URL prints.
- A grouped result appears for bucket counts.
- Physical plan appears from `explain(True)`.

## Lesson-By-Lesson Expected Output

Use this as a quick verification checklist after each run.

### Lesson 01 - `01_cluster_connection.py`

- Spark session banner shows:
  - `Spark Version: 3.5.3`
  - `Master: spark://localhost:7077`
- Bucket output includes `0` to `9` with equal `count` values.
- `explain(True)` prints logical + physical plan blocks.

### Lesson 02 - `02_dataframe_operations.py`

- Schema includes:
  - `sale_id`, `date`, `region`, `model`, `units`, `unit_price`, `revenue`, `salesperson`
- High-value filter prints a non-zero `High-value count`.
- Monthly aggregation and top-salesperson tables print successfully.
- `explain(True)` prints plan containing aggregation + exchange stages.

### Lesson 03 - `03_sql_and_views.py`

- `Temp view created: sales` appears.
- Monthly SQL aggregation table prints.
- `RANK()` output appears (`revenue_rank` column).
- MoM output appears with `prev_month_revenue` and `mom_growth_pct`.
- `explain(True)` prints SQL plan sections.

### Lesson 04 - `04_joins_and_broadcast.py`

- Inner join and left join sample rows both print.
- Regular join plan shows `SortMergeJoin` and `Exchange`.
- Broadcast join plan shows `BroadcastHashJoin` and `BroadcastExchange`.
- Equality check prints `Same results: True`.

### Lesson 05 - `05_shuffle_partitions_cache.py`

- Partition counts show expected transition (base -> repartition -> coalesce).
- `cache()` second action is faster than first in most runs.
- Skew metrics block prints all fields:
  - `total_rows`, `unique_keys`, `top_key`, `top_key_count`, `top_key_pct`, `median_count`, `skew_ratio`, `is_skewed`
- Example skew signal: `is_skewed: True`.

### Lesson 06 - `06_bronze_silver_gold_pipeline.py`

- Bronze/Silver/Gold row counts print.
- Audit report prints:
  - `Bronze rows`
  - `Duplicates`
  - `Nulls fixed`
  - `Silver rows`
  - `Gold rows`
  - `Total runtime`
- Silver quality checks show:
  - `Null revenue in Silver: 0`
  - `Invalid revenue (<=0) in Silver: 0`

### Lesson 07 - `07_spark_ui_experiments.py`

- Script prints UI guidance links and tabs to inspect.
- Workload steps print results for:
  - `groupBy`, `join`, `repartition`, `cache`, `count`
- Cache timing shows second action faster in most runs.
- Script pauses with `UI inspection window: sleeping 30 seconds...`.

## Troubleshooting

### Cannot connect to Spark master

- Check `docker ps` and ensure Spark services are up.
- Verify master URL and mapped ports.

### Spark UI not loading

- Try both `8080` and `8086`.
- Check container logs and port mappings.

### Slow or unstable scripts

- Keep row sizes moderate while learning.
- Avoid Python UDFs in early lessons.
- Prefer built-in functions in `pyspark.sql.functions`.

### `winutils.exe` warning on Windows

You may still see warnings like `Did not find winutils.exe` when launching from Windows.
For this Docker Spark tutorial (remote standalone master/worker), this warning is typically non-blocking if jobs run successfully.

## Learning Journal Template

After each lesson, add notes in your own journal:

- What I ran:
- What I observed in output:
- What I saw in Spark UI:
- One concept I can explain now:
- One question I still have:
