#!/usr/bin/env bash
set -euo pipefail

# Run inside a Python client container attached to the same Docker network.
# Adjust path and network names for your environment.

export SPARK_MASTER_URL=${SPARK_MASTER_URL:-spark://spark-master:7077}

python -u 01_cluster_connection.py
python -u 02_dataframe_operations.py
python -u 03_sql_and_views.py
python -u 04_joins_and_broadcast.py
python -u 05_shuffle_partitions_cache.py
python -u 06_bronze_silver_gold_pipeline.py
python -u 07_spark_ui_experiments.py
