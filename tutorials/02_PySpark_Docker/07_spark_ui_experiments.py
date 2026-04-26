from __future__ import annotations

import time

from pyspark.sql import functions as F

from common.spark_session import create_spark_session


def main() -> None:
    spark = create_spark_session("07_spark_ui_experiments")

    try:
        app_ui = spark.sparkContext.uiWebUrl

        print("\nOpen Spark UI at: http://localhost:8086")
        print("Also check (common in this setup):")
        print("- Cluster UI: http://localhost:8081")
        print(f"- Application UI (driver): {app_ui}")
        print("Check:")
        print("- Jobs")
        print("- Stages")
        print("- Tasks")
        print("- SQL tab")
        print("- Executors")

        print("\n[Step 1] Build synthetic workload DataFrame")
        fact_df = (
            spark.range(1, 500_001)
            .withColumnRenamed("id", "sale_id")
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
        )

        print("\n[Step 2] groupBy workload (watch SQL + Stages)")
        grouped = (
            fact_df.groupBy("region", "model")
            .agg(
                F.count("*").alias("num_sales"),
                F.round(F.sum("revenue"), 2).alias("total_revenue"),
            )
            .orderBy(F.col("total_revenue").desc())
        )
        grouped.show(20, truncate=False)

        print("\n[Step 3] join workload (watch join strategy + shuffles)")
        target_df = spark.sql(
            """
            SELECT * FROM VALUES
                ('North',   1.08D, 'A'),
                ('South',   1.03D, 'B'),
                ('East',    1.05D, 'A'),
                ('West',    1.02D, 'C'),
                ('Central', 1.06D, 'B')
            AS region_targets(region, target_multiplier, priority_tier)
            """
        )

        joined = fact_df.join(target_df, on="region", how="inner")
        joined_agg = (
            joined.groupBy("priority_tier")
            .agg(F.round(F.sum("revenue"), 2).alias("tier_revenue"))
            .orderBy("priority_tier")
        )
        joined_agg.show(truncate=False)

        print("\n[Step 4] repartition workload (watch task parallelism)")
        repart_df = fact_df.repartition(12, "region")
        repart_result = repart_df.groupBy("region").agg(F.count("*").alias("cnt")).orderBy("region")
        repart_result.show(truncate=False)

        print("\n[Step 5] cache workload (watch repeated job behavior)")
        cached = repart_df.cache()

        t0 = time.perf_counter()
        cached.groupBy("model").agg(F.sum("revenue").alias("rev")).count()
        t1 = time.perf_counter()

        cached.groupBy("model").agg(F.sum("revenue").alias("rev")).count()
        t2 = time.perf_counter()

        print(f"Cache first action:  {t1 - t0:.3f}s")
        print(f"Cache second action: {t2 - t1:.3f}s")

        print("\n[Step 6] count workload (simple action)")
        total_rows = cached.count()
        print(f"Total rows in cached DataFrame: {total_rows}")

        cached.unpersist()

        print("\nUI inspection window: sleeping 30 seconds...")
        time.sleep(30)

    finally:
        print("\nStopping Spark session...")
        spark.stop()


if __name__ == "__main__":
    main()
