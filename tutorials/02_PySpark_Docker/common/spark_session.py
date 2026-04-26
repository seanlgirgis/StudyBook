from __future__ import annotations

import os
from pyspark.sql import SparkSession

DEFAULT_SPARK_MASTER = "spark://localhost:7077"


def create_spark_session(app_name: str) -> SparkSession:
    """Create a SparkSession configured for the Docker standalone cluster."""
    spark_master = os.getenv("SPARK_MASTER_URL", DEFAULT_SPARK_MASTER)

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master(spark_master)
        .config("spark.executor.memory", "1g")
        .config("spark.driver.memory", "1g")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.sql.adaptive.enabled", "true")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    print("=" * 72)
    print("Spark Session Created")
    print(f"Spark Version: {spark.version}")
    print(f"Master: {spark.sparkContext.master}")
    print(f"App Name: {app_name}")
    print("=" * 72)

    return spark
