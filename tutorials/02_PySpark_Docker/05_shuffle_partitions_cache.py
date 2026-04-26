from __future__ import annotations

import time

from pyspark import StorageLevel
from pyspark.sql import functions as F

from common.spark_session import create_spark_session


def main() -> None:
    spark = create_spark_session("05_shuffle_partitions_cache")

    try:
        print("\n[Step 1] Build base synthetic sales DataFrame")
        base_df = (
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
            .withColumn("units", (F.col("sale_id") % 6 + F.lit(1)).cast("int"))
            .withColumn("revenue", (F.col("units") * F.lit(25000.0)).cast("double"))
        )
        print(f"Base partitions: {base_df.rdd.getNumPartitions()}")

        print("\n[Step 2] repartition(8, 'region')")
        repart_df = base_df.repartition(8, "region")
        print(f"Partitions after repartition: {repart_df.rdd.getNumPartitions()}")

        print("\n[Step 3] coalesce(1) from repartitioned DataFrame")
        coalesced_df = repart_df.coalesce(1)
        print(f"Partitions after coalesce: {coalesced_df.rdd.getNumPartitions()}")
        print("Note: coalesce(1) can become a bottleneck; use carefully.")

        print("\n[Step 4] explain(True) to inspect shuffle in repartition path")
        repart_agg = repart_df.groupBy("region").agg(F.sum("revenue").alias("region_revenue"))
        repart_agg.explain(True)

        print("\n[Step 5] cache() demo (same action twice)")
        cached_df = repart_df.cache()

        t0 = time.perf_counter()
        cached_df.groupBy("region").agg(F.sum("revenue").alias("total_revenue")).count()
        t1 = time.perf_counter()

        cached_df.groupBy("region").agg(F.sum("revenue").alias("total_revenue")).count()
        t2 = time.perf_counter()

        print(f"First action (populate cache): {t1 - t0:.3f}s")
        print(f"Second action (reuse cache):  {t2 - t1:.3f}s")
        print(f"Storage level (cache): {cached_df.storageLevel}")

        print("\n[Step 6] persist(StorageLevel.MEMORY_AND_DISK) demo")
        persisted_df = base_df.persist(StorageLevel.MEMORY_AND_DISK)
        p0 = time.perf_counter()
        persisted_df.groupBy("region").agg(F.avg("units").alias("avg_units")).count()
        p1 = time.perf_counter()

        print(f"Persisted action runtime: {p1 - p0:.3f}s")
        print(f"Storage level (persist): {persisted_df.storageLevel}")

        print("\n[Step 7] Data skew detection")
        skew_df = (
            spark.range(1, 500_001)
            .select(
                F.when((F.col("id") % 10) < 7, F.lit("HOT"))
                .otherwise(F.concat(F.lit("K_"), F.format_string("%02d", F.col("id") % 30)))
                .alias("key")
            )
        )

        key_counts = skew_df.groupBy("key").count()

        total_rows = skew_df.count()
        unique_keys = key_counts.count()

        top_row = key_counts.orderBy(F.col("count").desc(), F.col("key").asc()).first()
        top_key = top_row["key"]
        top_key_count = int(top_row["count"])

        top_key_pct = round((top_key_count * 100.0) / total_rows, 2)

        median_count = int(
            key_counts.agg(F.expr("percentile_approx(count, 0.5) as median_count")).first()["median_count"]
        )

        skew_ratio = round(top_key_count / median_count, 2) if median_count else None
        is_skewed = bool(skew_ratio is not None and skew_ratio >= 3.0)

        print("Skew metrics:")
        print(f"total_rows: {total_rows}")
        print(f"unique_keys: {unique_keys}")
        print(f"top_key: {top_key}")
        print(f"top_key_count: {top_key_count}")
        print(f"top_key_pct: {top_key_pct}")
        print(f"median_count: {median_count}")
        print(f"skew_ratio: {skew_ratio}")
        print(f"is_skewed: {is_skewed}")

        print("\nTop key distribution (descending):")
        key_counts.orderBy(F.col("count").desc(), F.col("key").asc()).show(10, truncate=False)

        print("\nConcept recap:")
        print("- repartition increases/decreases partitions with full shuffle.")
        print("- coalesce reduces partitions with minimal shuffle (best for downsizing).")
        print("- cache/persist can reduce repeated-computation cost.")
        print("- Skewed keys can create straggler tasks and slow pipelines.")

        cached_df.unpersist()
        persisted_df.unpersist()

    finally:
        print("\nStopping Spark session...")
        spark.stop()


if __name__ == "__main__":
    main()
