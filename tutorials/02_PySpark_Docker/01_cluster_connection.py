from __future__ import annotations

from common.spark_session import create_spark_session


def main() -> None:
    spark = create_spark_session("01_cluster_connection")

    try:
        print("\n[Step 1] Build a synthetic DataFrame with spark.range")
        df = spark.range(1, 100001)

        print("\n[Step 2] Basic inspection")
        print(f"Row count (expected 100000): {df.count()}")
        print(f"Number of partitions: {df.rdd.getNumPartitions()}")

        print("\n[Step 3] Trigger a transformation + action")
        bucketed = df.groupBy((df.id % 10).alias("bucket")).count().orderBy("bucket")
        bucketed.show(truncate=False)

        print("\n[Step 4] Explain physical plan")
        bucketed.explain(True)

        print("\n[Step 5] Driver vs Executor (concept check)")
        print("Driver: coordinates the job and plans execution.")
        print("Executors: run tasks in parallel on partitions.")
        print("Each action (count/show) triggers Spark execution.")

    finally:
        print("\nStopping Spark session...")
        spark.stop()


if __name__ == "__main__":
    main()
