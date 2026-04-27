# ============================================================
# Topic   : PySpark for Data Engineers
# File    : 02_dataframe_operations.py
# Covers  : DataFrame select, filter, withColumn, groupBy, aggregations, sorting
# Prereqs : pip install pyspark | Java 11+ installed, JAVA_HOME set
# Run     : python -u .\02_dataframe_operations.py
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import os
import sys
from pathlib import Path


def get_output_dir() -> Path:
    base = os.getenv("OUTPUT_DIR")
    if base:
        return Path(base)
    if os.name == "nt":
        return Path("C:/tmp/studybook/pyspark")
    return Path("/tmp/studybook/pyspark")


def create_spark_session(app_name: str = "02-dataframe-ops") -> SparkSession:
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
    os.environ["PYTHONHASHSEED"] = "0"

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[2]")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.default.parallelism", "2")
        .config("spark.ui.enabled", "false")
        .config("spark.python.worker.reuse", "true")
        .config("spark.pyspark.python", sys.executable)
        .config("spark.pyspark.driver.python", sys.executable)
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    print(f"Spark Version: {spark.version}")
    print(f"Master: {spark.sparkContext.master}")
    print(f"Python Exec: {sys.executable}")

    return spark


def create_sample_df(spark: SparkSession):
    """
    Create sample data using spark.range(), not Python lists.

    WHY:
      On this Windows machine, Python-created Spark data triggers Python worker crashes.
      spark.range() is generated inside the JVM and is stable.
    """
    df = (
        spark.range(1, 101)
        .withColumn(
            "brand",
            F.when(F.col("id") % 3 == 0, F.lit("Toyota"))
             .when(F.col("id") % 3 == 1, F.lit("Ford"))
             .otherwise(F.lit("Tesla"))
        )
        .withColumn(
            "model",
            F.when((F.col("brand") == "Toyota") & (F.col("id") % 2 == 0), F.lit("Camry"))
             .when((F.col("brand") == "Toyota") & (F.col("id") % 2 == 1), F.lit("Corolla"))
             .when((F.col("brand") == "Ford") & (F.col("id") % 2 == 0), F.lit("F-150"))
             .when((F.col("brand") == "Ford") & (F.col("id") % 2 == 1), F.lit("Mustang"))
             .when((F.col("brand") == "Tesla") & (F.col("id") % 2 == 0), F.lit("Model Y"))
             .otherwise(F.lit("Model 3"))
        )
        .withColumn("year", F.lit(2020) + (F.col("id") % 5))
        .withColumn("price", F.lit(20000) + (F.col("id") * 750))
        .withColumn("units", (F.col("id") % 5) + 1)
        .withColumn("revenue", F.col("price") * F.col("units"))
    )

    print("\n=== ORIGINAL DATA ===")
    df.show(10, truncate=False)

    return df


def basic_select_filter(df):
    print("\n=== SELECT + FILTER ===")

    result = (
        df.select("brand", "model", "price", "revenue")
        .filter(F.col("revenue") > 100000)
    )

    result.show(10, truncate=False)


def with_column_example(df):
    print("\n=== WITH COLUMN ===")

    result = (
        df.withColumn("price_with_tax", F.round(F.col("price") * 1.10, 2))
        .withColumn(
            "revenue_tier",
            F.when(F.col("revenue") >= 250000, F.lit("HIGH"))
             .when(F.col("revenue") >= 100000, F.lit("MEDIUM"))
             .otherwise(F.lit("LOW"))
        )
    )

    result.select("brand", "model", "price", "price_with_tax", "revenue_tier").show(10, truncate=False)


def groupby_aggregation(df):
    print("\n=== GROUP BY AGGREGATION ===")

    result = (
        df.groupBy("brand")
        .agg(
            F.count("*").alias("sale_count"),
            F.sum("revenue").alias("total_revenue"),
            F.avg("price").alias("avg_price"),
            F.max("revenue").alias("max_revenue"),
        )
        .orderBy(F.desc("total_revenue"))
    )

    result.show(truncate=False)
    return result


def multi_column_aggregation(df):
    print("\n=== GROUP BY BRAND + MODEL ===")

    result = (
        df.groupBy("brand", "model")
        .agg(
            F.count("*").alias("sale_count"),
            F.sum("units").alias("total_units"),
            F.sum("revenue").alias("total_revenue"),
        )
        .orderBy(F.desc("total_revenue"))
    )

    result.show(truncate=False)


def sorting_example(df):
    print("\n=== SORTING ===")

    (
        df.select("brand", "model", "year", "price", "revenue")
        .orderBy(F.desc("revenue"))
        .show(10, truncate=False)
    )


def explain_plan(df):
    print("\n=== EXPLAIN PLAN ===")

    query = (
        df.filter(F.col("revenue") > 100000)
        .groupBy("brand")
        .agg(F.sum("revenue").alias("total_revenue"))
        .orderBy(F.desc("total_revenue"))
    )

    query.explain(True)


def main():
    spark = None

    try:
        spark = create_spark_session()

        df = create_sample_df(spark)

        basic_select_filter(df)
        with_column_example(df)
        groupby_aggregation(df)
        multi_column_aggregation(df)
        sorting_example(df)
        explain_plan(df)

    finally:
        if spark:
            spark.stop()


if __name__ == "__main__":
    main()