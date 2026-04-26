# ============================================================
# Topic   : PySpark for Data Engineers
# File    : 04_performance_tuning.py
# Covers  : broadcast joins, partitions, cache, skew, shuffle tuning
# Prereqs : pip install pyspark | Java 11+ installed, JAVA_HOME set
# Run     : python -u .\04_performance_tuning.py
# ============================================================

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.storagelevel import StorageLevel
import os
import sys
import time


def create_spark_session(app_name: str = "04-performance") -> SparkSession:
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


def create_sales_df(spark: SparkSession, n_rows: int = 200_000) -> DataFrame:
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
        .withColumn("sale_id", F.format_string("SALE-%07d", F.col("id")))
        .withColumn("region", F.element_at(regions, ((F.col("id") % 5) + 1).cast("int")))
        .withColumn("model", F.element_at(models, ((F.col("id") % 10) + 1).cast("int")))
        .withColumn("units", ((F.col("id") % 5) + 1).cast("long"))
        .withColumn("unit_price", (F.lit(15000) + (F.col("id") % 40000)).cast("double"))
        .withColumn("revenue", (F.col("units") * F.col("unit_price")).cast("double"))
        .drop("id")
    )

    print(f"Generated sales rows: {df.count():,}")
    return df


def create_targets_df(spark: SparkSession) -> DataFrame:
    return (
        spark.range(1, 6)
        .withColumn(
            "region",
            F.when(F.col("id") == 1, F.lit("North"))
             .when(F.col("id") == 2, F.lit("South"))
             .when(F.col("id") == 3, F.lit("East"))
             .when(F.col("id") == 4, F.lit("West"))
             .otherwise(F.lit("Central"))
        )
        .withColumn("revenue_target", F.lit(5_000_000.0) + (F.col("id") * 250_000.0))
        .drop("id")
    )


def demonstrate_shuffle_cost(spark: SparkSession) -> dict:
    large_df = create_sales_df(spark, 200_000)
    small_df = create_targets_df(spark)

    print("\nWITHOUT broadcast:")
    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")
    joined_no_broadcast = large_df.join(small_df, "region")

    t0 = time.perf_counter()
    no_broadcast_count = joined_no_broadcast.count()
    no_broadcast_ms = (time.perf_counter() - t0) * 1000

    joined_no_broadcast.explain(True)

    print("\nWITH broadcast:")
    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10485760")
    joined_broadcast = large_df.join(F.broadcast(small_df), "region")

    t1 = time.perf_counter()
    broadcast_count = joined_broadcast.count()
    broadcast_ms = (time.perf_counter() - t1) * 1000

    joined_broadcast.explain(True)

    speedup = no_broadcast_ms / broadcast_ms if broadcast_ms > 0 else 0

    print(f"No broadcast count: {no_broadcast_count:,}")
    print(f"Broadcast count:    {broadcast_count:,}")
    print(f"No broadcast:       {no_broadcast_ms:.2f} ms")
    print(f"Broadcast:          {broadcast_ms:.2f} ms")
    print(f"Speedup:            {speedup:.2f}x")

    return {
        "no_broadcast_ms": no_broadcast_ms,
        "broadcast_ms": broadcast_ms,
        "speedup_x": speedup,
    }


def optimize_partitions(spark: SparkSession, df: DataFrame) -> None:
    print("\nPartition counts:")
    print(f"Original partitions: {df.rdd.getNumPartitions()}")

    df_repartitioned = df.repartition(8, "region")
    df_coalesced = df.coalesce(1)

    print(f"After repartition(8): {df_repartitioned.rdd.getNumPartitions()}")
    print(f"After coalesce(1):    {df_coalesced.rdd.getNumPartitions()}")

    print("\nWHY:")
    print("  repartition = full shuffle, better distribution before joins/aggregations.")
    print("  coalesce    = reduces partitions, usually before writing fewer output files.")

    for label, candidate in [
        ("original", df),
        ("repartitioned", df_repartitioned),
        ("coalesced", df_coalesced),
    ]:
        t0 = time.perf_counter()
        candidate.groupBy("region").agg(F.sum("revenue").alias("total_revenue")).count()
        elapsed = (time.perf_counter() - t0) * 1000
        print(f"{label:<15} groupBy time: {elapsed:.2f} ms")


def cache_vs_persist(spark: SparkSession, df: DataFrame) -> dict:
    def run_three_times(label: str, candidate: DataFrame) -> list[float]:
        times = []
        for i in range(3):
            t0 = time.perf_counter()
            candidate.groupBy("region", "model").agg(F.sum("revenue")).count()
            elapsed = (time.perf_counter() - t0) * 1000
            times.append(elapsed)
            print(f"{label} run {i + 1}: {elapsed:.2f} ms")
        return times

    print("\nNo cache:")
    no_cache_times = run_three_times("no_cache", df)

    print("\ncache():")
    cached = df.cache()
    cached.count()
    cached_times = run_three_times("cache", cached)
    cached.unpersist()

    print("\npersist(MEMORY_AND_DISK):")
    persisted = df.persist(StorageLevel.MEMORY_AND_DISK)
    persisted.count()
    persisted_times = run_three_times("persist", persisted)
    persisted.unpersist()

    no_cache_avg = sum(no_cache_times) / len(no_cache_times)
    cache_avg = sum(cached_times) / len(cached_times)
    speedup = no_cache_avg / cache_avg if cache_avg > 0 else 0

    print("\nWHY cache:")
    print("  Cache helps when the same expensive DataFrame is reused multiple times.")
    print("  Do not cache everything; cached data competes for executor memory.")

    return {
        "no_cache_avg_ms": no_cache_avg,
        "cached_avg_ms": cache_avg,
        "speedup_x": speedup,
    }


def detect_data_skew(df: DataFrame, key_col: str) -> dict:
    counts_df = df.groupBy(key_col).count()
    counts_df.show(truncate=False)

    stats = counts_df.agg(
        F.sum("count").alias("total_rows"),
        F.count("*").alias("unique_keys"),
        F.max("count").alias("top_key_count"),
        F.percentile_approx("count", 0.5).alias("median_count"),
    ).first()

    top_row = counts_df.orderBy(F.desc("count")).first()

    total_rows = int(stats["total_rows"])
    unique_keys = int(stats["unique_keys"])
    top_key = top_row[key_col]
    top_key_count = int(stats["top_key_count"])
    median_count = int(stats["median_count"])
    skew_ratio = top_key_count / median_count if median_count else 0
    top_key_pct = top_key_count / total_rows * 100 if total_rows else 0
    is_skewed = skew_ratio > 10

    result = {
        "total_rows": total_rows,
        "unique_keys": unique_keys,
        "top_key": top_key,
        "top_key_count": top_key_count,
        "top_key_pct": top_key_pct,
        "median_count": median_count,
        "skew_ratio": skew_ratio,
        "is_skewed": is_skewed,
    }

    print(result)

    if is_skewed:
        print("WARNING: Data skew detected.")
        print("Fixes: salting hot keys, broadcast joins, AQE skew join handling.")
    else:
        print("No major skew detected.")

    return result


def create_skewed_df(spark: SparkSession, n_rows: int = 100_000) -> DataFrame:
    return (
        spark.range(1, n_rows + 1)
        .withColumn(
            "region",
            F.when(F.col("id") <= int(n_rows * 0.85), F.lit("North"))
             .when(F.col("id") % 4 == 0, F.lit("South"))
             .when(F.col("id") % 4 == 1, F.lit("East"))
             .when(F.col("id") % 4 == 2, F.lit("West"))
             .otherwise(F.lit("Central"))
        )
        .withColumn("revenue", (F.lit(10000) + F.col("id")).cast("double"))
        .drop("id")
    )


def tune_shuffle_partitions(spark: SparkSession, df: DataFrame) -> None:
    print("\nShuffle partition tuning:")

    results = []

    for partitions in [1, 2, 4, 8]:
        spark.conf.set("spark.sql.shuffle.partitions", str(partitions))

        t0 = time.perf_counter()
        df.groupBy("region", "model").agg(F.sum("revenue").alias("total_revenue")).count()
        elapsed = (time.perf_counter() - t0) * 1000

        results.append((partitions, elapsed))

    print(f"{'partitions':<12} {'time_ms':>12}")
    for partitions, elapsed in results:
        print(f"{partitions:<12} {elapsed:>12.2f}")

    print("\nRule of thumb:")
    print("  Too few partitions: large tasks, memory pressure.")
    print("  Too many partitions: scheduler overhead and tiny tasks.")
    print("  In production, target roughly 128 MB per shuffle partition.")
    print("  AQE can coalesce shuffle partitions automatically.")


def main() -> None:
    spark = None

    try:
        spark = create_spark_session("04-performance")

        df = create_sales_df(spark, n_rows=200_000)

        print("\n=== BROADCAST JOIN SPEEDUP ===")
        stats = demonstrate_shuffle_cost(spark)
        print(f"Speedup: {stats['speedup_x']:.2f}x")

        print("\n=== PARTITION OPTIMIZATION ===")
        optimize_partitions(spark, df)

        print("\n=== CACHE vs PERSIST ===")
        cache_stats = cache_vs_persist(spark, df)
        print(f"Cache speedup: {cache_stats['speedup_x']:.2f}x")

        print("\n=== SKEW DETECTION: NORMAL DATA ===")
        detect_data_skew(df, "region")

        print("\n=== SKEW DETECTION: SKEWED DATA ===")
        skewed_df = create_skewed_df(spark, n_rows=100_000)
        detect_data_skew(skewed_df, "region")

        print("\n=== SHUFFLE PARTITION TUNING ===")
        tune_shuffle_partitions(spark, df)

    finally:
        if spark:
            spark.stop()


if __name__ == "__main__":
    main()