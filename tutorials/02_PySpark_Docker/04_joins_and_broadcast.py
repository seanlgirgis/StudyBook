from __future__ import annotations

from pyspark.sql import functions as F

from common.spark_session import create_spark_session


def main() -> None:
    spark = create_spark_session("04_joins_and_broadcast")

    try:
        print("\n[Step 1] Build large sales DataFrame (fact-like)")
        large_df = (
            spark.range(1, 300_001)
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
        print(f"Large DF rows: {large_df.count()}")

        print("\n[Step 2] Build small region target DataFrame (dimension-like)")
        small_df = spark.sql(
            """
            SELECT * FROM VALUES
                ('North',   1.08D, 'A'),
                ('South',   1.03D, 'B'),
                ('East',    1.05D, 'A'),
                ('West',    1.02D, 'C'),
                ('Central', 1.06D, 'B'),
                ('Midwest', 1.04D, 'B')
            AS region_targets(region, target_multiplier, priority_tier)
            """
        )
        small_df.show(truncate=False)

        print("\n[Step 3] Inner join example")
        inner_joined = large_df.join(small_df, on="region", how="inner")
        inner_joined.select("sale_id", "region", "model", "revenue", "target_multiplier").show(8, truncate=False)

        print("\n[Step 4] Left join example")
        left_joined = large_df.join(small_df, on="region", how="left")
        left_joined.select("sale_id", "region", "model", "priority_tier").show(8, truncate=False)

        print("\n[Step 5] Compare regular join vs broadcast join plans")
        original_threshold = spark.conf.get("spark.sql.autoBroadcastJoinThreshold")
        spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)

        regular_join = large_df.join(small_df, on="region", how="inner")
        regular_summary = (
            regular_join.groupBy("region")
            .agg(F.round(F.sum("revenue"), 2).alias("total_revenue"))
            .orderBy("region")
        )

        print("\nRegular join physical plan (expect SortMergeJoin + Exchange):")
        regular_summary.explain(True)

        broadcast_join = large_df.join(F.broadcast(small_df), on="region", how="inner")
        broadcast_summary = (
            broadcast_join.groupBy("region")
            .agg(F.round(F.sum("revenue"), 2).alias("total_revenue"))
            .orderBy("region")
        )

        print("\nBroadcast join physical plan (expect BroadcastHashJoin + BroadcastExchange):")
        broadcast_summary.explain(True)

        print("\n[Step 6] Execute both summaries (results should match)")
        regular_rows = regular_summary.collect()
        broadcast_rows = broadcast_summary.collect()

        print("Regular join result:")
        for row in regular_rows:
            print(row)

        print("\nBroadcast join result:")
        for row in broadcast_rows:
            print(row)

        print("\n[Step 7] Equality check")
        print(f"Same results: {regular_rows == broadcast_rows}")

        print("\nConcept recap:")
        print("- Inner join keeps matching keys only.")
        print("- Left join keeps all left rows even when right-side key is missing.")
        print("- SortMergeJoin usually requires shuffle/exchange on both sides.")
        print("- BroadcastHashJoin ships the small table to executors to avoid large shuffle.")

        spark.conf.set("spark.sql.autoBroadcastJoinThreshold", original_threshold)

    finally:
        print("\nStopping Spark session...")
        spark.stop()


if __name__ == "__main__":
    main()
