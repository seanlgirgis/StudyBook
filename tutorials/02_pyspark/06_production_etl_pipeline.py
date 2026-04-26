# ============================================================
# Topic   : PySpark for Data Engineers
# File    : 06_production_etl_pipeline.py
# Covers  : Bronze/Silver/Gold ETL, validation, incremental logic, audit metrics
# Prereqs : pip install pyspark | Java 11+ installed, JAVA_HOME set
# Run     : python -u .\06_production_etl_pipeline.py
# ============================================================

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
import os
import sys
import time


def create_spark_session(app_name: str = "06-production-etl") -> SparkSession:
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
    os.environ["PYTHONHASHSEED"] = "0"

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[2]")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.default.parallelism", "2")
        .config("spark.sql.adaptive.enabled", "true")
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


def create_bronze_sales(spark: SparkSession, n_rows: int = 100_000) -> DataFrame:
    """
    Bronze layer = raw-ish ingested data.

    In production, bronze is usually:
      - minimally transformed
      - append-only
      - includes ingestion metadata
      - keeps bad/null/duplicate data for traceability
    """
    models = F.array(
        F.lit("Camry"), F.lit("Corolla"), F.lit("RAV4"), F.lit("Highlander"),
        F.lit("Tacoma"), F.lit("Tundra"), F.lit("Prius"), F.lit("Sienna"),
        F.lit("4Runner"), F.lit("Venza")
    )

    regions = F.array(
        F.lit("North"), F.lit("South"), F.lit("East"),
        F.lit("West"), F.lit("Central")
    )

    df = (
        spark.range(1, n_rows + 1)
        .withColumn(
            "sale_id",
            F.when(F.col("id") % 100 == 0, F.format_string("SALE-%07d", F.col("id") - 1))
             .otherwise(F.format_string("SALE-%07d", F.col("id")))
        )
        .withColumn("event_date", F.date_sub(F.current_date(), (F.col("id") % 730).cast("int")))
        .withColumn("region", F.element_at(regions, ((F.col("id") % 5) + 1).cast("int")))
        .withColumn("model", F.element_at(models, ((F.col("id") % 10) + 1).cast("int")))
        .withColumn("units", ((F.col("id") % 5) + 1).cast("long"))
        .withColumn("unit_price", (F.lit(15000) + (F.col("id") % 40000)).cast("double"))
        .withColumn(
            "revenue",
            F.when(F.col("id") % 50 == 0, F.lit(None).cast("double"))
             .otherwise((F.col("units") * F.col("unit_price")).cast("double"))
        )
        .withColumn("source_system", F.lit("dealer_feed"))
        .withColumn("ingest_ts", F.current_timestamp())
        .drop("id")
    )

    print("\n=== BRONZE CREATED ===")
    print(f"Bronze rows: {df.count():,}")
    df.show(5, truncate=False)
    return df


def validate_bronze(df: DataFrame) -> dict:
    """
    Data quality checks.

    In production, these often become:
      - Great Expectations checks
      - Deequ checks
      - custom validation tables
      - pipeline stop/fail rules
    """
    metrics = df.agg(
        F.count("*").alias("total_rows"),
        F.countDistinct("sale_id").alias("distinct_sale_ids"),
        F.sum(F.when(F.col("revenue").isNull(), 1).otherwise(0)).alias("null_revenue_rows"),
        F.sum(F.when(F.col("units") <= 0, 1).otherwise(0)).alias("bad_units_rows"),
        F.min("event_date").alias("min_event_date"),
        F.max("event_date").alias("max_event_date"),
    ).first()

    total_rows = int(metrics["total_rows"])
    distinct_sale_ids = int(metrics["distinct_sale_ids"])
    duplicate_rows = total_rows - distinct_sale_ids
    null_revenue_rows = int(metrics["null_revenue_rows"])
    bad_units_rows = int(metrics["bad_units_rows"])

    result = {
        "total_rows": total_rows,
        "distinct_sale_ids": distinct_sale_ids,
        "duplicate_rows": duplicate_rows,
        "null_revenue_rows": null_revenue_rows,
        "bad_units_rows": bad_units_rows,
        "min_event_date": str(metrics["min_event_date"]),
        "max_event_date": str(metrics["max_event_date"]),
    }

    print("\n=== DATA QUALITY METRICS ===")
    for k, v in result.items():
        print(f"{k:<22}: {v}")

    return result


def bronze_to_silver(df: DataFrame) -> DataFrame:
    """
    Silver layer = cleaned, typed, deduplicated, business-valid data.

    Typical silver rules:
      - remove duplicates
      - fix nulls where safe
      - enforce schema/typing
      - add derived columns
      - filter invalid business records
    """
    silver = (
        df.dropDuplicates(["sale_id"])
        .withColumn(
            "revenue",
            F.coalesce(F.col("revenue"), F.col("units") * F.col("unit_price"))
        )
        .filter(F.col("revenue") > 0)
        .filter(F.col("units") > 0)
        .withColumn("year", F.year("event_date"))
        .withColumn("month", F.month("event_date"))
        .withColumn("quarter", F.quarter("event_date"))
        .withColumn("processed_ts", F.current_timestamp())
    )

    print("\n=== SILVER CREATED ===")
    print(f"Silver rows: {silver.count():,}")
    silver.show(5, truncate=False)

    return silver


def build_gold_monthly_sales(silver: DataFrame) -> DataFrame:
    """
    Gold layer = business-ready aggregate.

    Gold tables are usually consumed by:
      - dashboards
      - reporting
      - analysts
      - ML feature pipelines
    """
    gold = (
        silver.groupBy("year", "month", "region", "model")
        .agg(
            F.count("*").alias("sale_count"),
            F.sum("units").alias("total_units"),
            F.round(F.sum("revenue"), 2).alias("total_revenue"),
            F.round(F.avg("revenue"), 2).alias("avg_sale_revenue"),
        )
        .orderBy("year", "month", "region", "model")
    )

    print("\n=== GOLD MONTHLY SALES ===")
    gold.show(20, truncate=False)

    return gold


def calculate_incremental_cutoff(silver: DataFrame) -> None:
    """
    Incremental processing concept.

    In real pipelines, you usually process:
      - new records since max processed timestamp
      - new partitions since last successful run
      - CDC changes from source
    """
    max_event_date = silver.agg(F.max("event_date").alias("max_event_date")).first()["max_event_date"]

    print("\n=== INCREMENTAL PROCESSING CONCEPT ===")
    print(f"Current max event_date: {max_event_date}")
    print("Production pattern:")
    print("  1. Store last successful watermark in an audit/control table.")
    print("  2. Next run filters source where event_date > watermark.")
    print("  3. Process only new/changed data.")
    print("  4. Update watermark only after successful completion.")


def create_audit_report(
    bronze_metrics: dict,
    silver: DataFrame,
    gold: DataFrame,
    total_ms: float
) -> None:
    silver_rows = silver.count()
    gold_rows = gold.count()

    print("\n╔════════════════════════════════════════════╗")
    print("║        PySpark ETL Pipeline Report         ║")
    print("╠════════════════════════════════════════════╣")
    print(f"║ Bronze rows          : {bronze_metrics['total_rows']:>18,} ║")
    print(f"║ Duplicate rows       : {bronze_metrics['duplicate_rows']:>18,} ║")
    print(f"║ Null revenue rows    : {bronze_metrics['null_revenue_rows']:>18,} ║")
    print(f"║ Silver rows          : {silver_rows:>18,} ║")
    print(f"║ Gold rows            : {gold_rows:>18,} ║")
    print(f"║ Total time seconds   : {total_ms / 1000:>18.2f} ║")
    print("╚════════════════════════════════════════════╝")


def explain_pipeline_plan(gold: DataFrame) -> None:
    print("\n=== GOLD EXPLAIN PLAN ===")
    gold.explain(True)

    print("\nLook for:")
    print("  Project        -> derived columns")
    print("  HashAggregate  -> groupBy aggregations")
    print("  Exchange       -> shuffle")
    print("  Sort           -> orderBy")


def main() -> None:
    spark = None
    start = time.perf_counter()

    try:
        spark = create_spark_session()

        bronze = create_bronze_sales(spark, n_rows=100_000)
        bronze_metrics = validate_bronze(bronze)

        silver = bronze_to_silver(bronze)
        gold = build_gold_monthly_sales(silver)

        calculate_incremental_cutoff(silver)
        explain_pipeline_plan(gold)

        total_ms = (time.perf_counter() - start) * 1000
        create_audit_report(bronze_metrics, silver, gold, total_ms)

    finally:
        if spark:
            spark.stop()


if __name__ == "__main__":
    main()