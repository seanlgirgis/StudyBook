# 05 - How To Run This Tutorial Using The Containers

Back to [Docker Pack Index](./README.md)

## Current tutorial connection

Tutorial scripts use:

- `spark://localhost:7077`

That maps your local driver to Docker Spark master.

## Recommended run flow

1. Start `citi_spark` and `citi_spark_worker`.
2. Confirm from `docker ps`.
3. Run lessons in order:

```powershell
python -u .\01_cluster_connection.py
python -u .\02_dataframe_operations.py
python -u .\03_sql_and_views.py
python -u .\04_joins_and_broadcast.py
python -u .\05_shuffle_partitions_cache.py
python -u .\06_bronze_silver_gold_pipeline.py
python -u .\07_spark_ui_experiments.py
```

## Helpful runner sample

See [run_tutorial_local.ps1](./samples/run_tutorial_local.ps1).

## If Spark URL changes

Set env var before running:

```powershell
$env:SPARK_MASTER_URL="spark://localhost:7077"
```

Next: [Docker vs Local Spark](./06_docker_vs_local.md)
