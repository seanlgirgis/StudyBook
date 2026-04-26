from __future__ import annotations

import time

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from common.spark_session import create_spark_session


def build_bronze_df(spark) -> DataFrame:
    base = (
        spark.range(1, 200_001)
        .withColumnRenamed("id", "sale_id")
        .withColumn("date", F.expr("date_add(to_date('2026-01-01'), int(sale_id % 120))"))
        .withColumn(
            "region",
            F.when((F.col("sale_id") % 5) == 0, F.lit("North"))
            .when((F.col("sale_id") % 5) == 1, F.lit("South"))
            .when((F.col("sale_id") % 5) == 2, F.lit("East"))
            .when((F.col("sale_id") % 5) == 3, F.lit("West"))
            .otherwise(F.lit("Central")),
        )
        .withColumn(
            "model",
            F.when((F.col("sale_id") % 4) == 0, F.lit("Camry"))
            .when((F.col("sale_id") % 4) == 1, F.lit("Corolla"))
            .when((F.col("sale_id") % 4) == 2, F.lit("RAV4"))
            .otherwise(F.lit("Prius")),
        )
        .withColumn("units", (F.col("sale_id") % 6 + F.lit(1)).cast("int"))
        .withColumn(
            "unit_price",
            F.when(F.col("model") == "Camry", F.lit(32000.0))
            .when(F.col("model") == "Corolla", F.lit(24000.0))
            .when(F.col("model") == "RAV4", F.lit(35000.0))
            .otherwise(F.lit(29000.0)),
        )
        .withColumn("revenue", (F.col("units") * F.col("unit_price")).cast("double"))
        .withColumn("ingest_ts", F.current_timestamp())
    )

    # Inject null revenue rows for data-quality handling in Silver.
    with_nulls = base.withColumn(
        "revenue",
        F.when((F.col("sale_id") % 23) == 0, F.lit(None).cast("double")).otherwise(F.col("revenue")),
    )

    # Inject duplicates by unioning a deterministic slice.
    duplicates_slice = with_nulls.filter((F.col("sale_id") % 47) == 0)
    bronze_df = with_nulls.unionByName(duplicates_slice)

    return bronze_df


def build_silver_df(bronze_df: DataFrame) -> DataFrame:
    silver = (
        bronze_df.dropDuplicates(["sale_id"])  # dedupe by business key
        .withColumn("revenue", F.coalesce(F.col("revenue"), F.col("units") * F.col("unit_price")))
        .filter(F.col("revenue") > 0)
        .withColumn("year", F.year("date"))
        .withColumn("month", F.date_format("date", "yyyy-MM"))
        .withColumn("quarter", F.concat(F.lit("Q"), F.quarter("date")))
    )
    return silver


def build_gold_df(silver_df: DataFrame) -> DataFrame:
    gold = (
        silver_df.groupBy("month", "region", "model")
        .agg(
            F.count("*").alias("num_sales"),
            F.sum("units").alias("total_units"),
            F.round(F.sum("revenue"), 2).alias("total_revenue"),
            F.round(F.avg("revenue"), 2).alias("avg_revenue"),
            F.round((F.sum("revenue") / F.sum("units")), 2).alias("avg_revenue_per_unit"),
        )
        .orderBy(F.col("total_revenue").desc(), F.col("month"), F.col("region"), F.col("model"))
    )
    return gold


def main() -> None:
    spark = create_spark_session("06_bronze_silver_gold_pipeline")

    t0 = time.perf_counter()

    try:
        print("\n[Step 1] Bronze layer: raw synthetic sales with duplicates + null revenue")
        bronze_df = build_bronze_df(spark)
        bronze_df.printSchema()

        bronze_rows = bronze_df.count()
        duplicate_count = bronze_rows - bronze_df.select("sale_id").dropDuplicates().count()
        null_revenue_bronze = bronze_df.filter(F.col("revenue").isNull()).count()

        print(f"Bronze rows: {bronze_rows}")
        print(f"Injected duplicates: {duplicate_count}")
        print(f"Null revenue in Bronze: {null_revenue_bronze}")

        print("\nBronze sample:")
        bronze_df.select("sale_id", "date", "region", "model", "units", "unit_price", "revenue").show(8, truncate=False)

        print("\n[Step 2] Silver layer: dedupe + null fix + quality checks + date enrich")
        silver_df = build_silver_df(bronze_df)

        silver_rows = silver_df.count()
        null_revenue_silver = silver_df.filter(F.col("revenue").isNull()).count()
        invalid_revenue_silver = silver_df.filter(F.col("revenue") <= 0).count()
        nulls_fixed = max(null_revenue_bronze - null_revenue_silver, 0)

        print(f"Silver rows: {silver_rows}")
        print(f"Null revenue in Silver: {null_revenue_silver}")
        print(f"Invalid revenue (<=0) in Silver: {invalid_revenue_silver}")

        print("\nSilver sample:")
        silver_df.select(
            "sale_id", "date", "year", "month", "quarter", "region", "model", "units", "revenue"
        ).show(8, truncate=False)

        print("\n[Step 3] Gold layer: monthly region/model business aggregates")
        gold_df = build_gold_df(silver_df)
        gold_rows = gold_df.count()

        print(f"Gold rows: {gold_rows}")

        print("\nGold sample:")
        gold_df.show(15, truncate=False)

        print("\n[Step 4] Explain physical plan for Gold aggregation")
        gold_df.explain(True)

        total_runtime = round(time.perf_counter() - t0, 3)

        print("\nAudit report:")
        print(f"Bronze rows: {bronze_rows}")
        print(f"Duplicates: {duplicate_count}")
        print(f"Nulls fixed: {nulls_fixed}")
        print(f"Silver rows: {silver_rows}")
        print(f"Gold rows: {gold_rows}")
        print(f"Total runtime: {total_runtime}s")

        print("\nConcept recap:")
        print("- Bronze keeps raw data, including imperfect records.")
        print("- Silver enforces quality and standardized columns.")
        print("- Gold serves business-ready aggregated datasets.")

    finally:
        print("\nStopping Spark session...")
        spark.stop()


if __name__ == "__main__":
    main()
