# ============================================================
# Topic   : PySpark for Data Engineers
# File    : 01_spark_session_and_rdds.py
# Covers  : SparkSession, lazy evaluation, DAG, RDD concepts, DataFrame-safe execution
# Prereqs : pip install pyspark | Java 11+ installed, JAVA_HOME set
# Run     : python -u .\01_spark_session_and_rdds.py
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import os
import sys
import time
from pathlib import Path


def get_output_dir() -> Path:
    base = os.getenv("OUTPUT_DIR")
    if base:
        return Path(base)
    if os.name == "nt":
        return Path("C:/tmp/studybook/pyspark")
    return Path("/tmp/studybook/pyspark")


def create_spark_session(
    app_name: str = "01-spark-basics",
    cores: str = "2"
) -> SparkSession:
    """
    Create a Windows-stable local SparkSession.

    WHY local[2]:
      Windows local mode can be fragile with many Python worker processes.
      local[2] keeps the tutorial stable.

    WHY sys.executable:
      Forces PySpark workers to use the same virtualenv Python.
    """
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
    os.environ["PYTHONHASHSEED"] = "0"

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master(f"local[{cores}]")
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
    print(f"Default Parallelism: {spark.sparkContext.defaultParallelism}")

    return spark


def demonstrate_lazy_evaluation(spark: SparkSession) -> None:
    """
    Prove lazy evaluation using Spark JVM/DataFrame operations.

    Transformations build a DAG. Nothing runs until an action like count().
    """
    df = spark.range(100_000)

    transformed = (
        df.withColumn("doubled", F.col("id") * 2)
          .filter(F.col("doubled") % 3 == 0)
    )

    print("Transformations defined. Nothing computed yet.")

    t0 = time.perf_counter()
    count = transformed.count()
    t1 = time.perf_counter()

    print(f"Action triggered. Count = {count}")
    print(f"Computation time: {(t1 - t0) * 1000:.2f} ms")
    print("Action triggered. Computation complete.")


def rdd_word_count(spark: SparkSession, text: str) -> list[tuple[str, int]]:
    """
    Demonstrate word-count logic without Python-worker RDD execution.

    Interview RDD pattern:
      lines -> flatMap(split) -> map((word, 1)) -> reduceByKey(sum)

    This local Windows-safe version computes the same result in plain Python
    because this machine's Spark Python workers crash during Python-backed
    RDD/DataFrame actions.
    """
    del spark  # Spark is not needed for this Windows-safe fallback.

    words: list[str] = []
    for line in text.strip().splitlines():
        for raw_word in line.lower().split():
            word = raw_word.strip(".,;:!?()[]{}\"'")
            if word:
                words.append(word)

    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1

    top10 = sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:10]

    print("\nTop 10 Words:")
    print("-------------------------")
    for word, count in top10:
        print(f"{word:<15} {count}")

    print("\nRDD equivalent:")
    print("  sc.parallelize(lines)")
    print("    .flatMap(lambda line: line.split())")
    print("    .map(lambda word: (word, 1))")
    print("    .reduceByKey(lambda a, b: a + b)")

    return top10


def compare_rdd_vs_dataframe(spark: SparkSession) -> None:
    """
    Compare RDD concept vs DataFrame execution.

    This avoids Python-backed input data and uses spark.range(), which is
    generated inside the JVM. That prevents Python worker crashes on Windows.
    """
    print("\nRDD timing skipped on this Windows runtime.")
    print("Reason: Python-backed RDD actions are crashing the local Python worker.")
    print("Conceptually, RDDs use Python lambdas; DataFrames use Catalyst/JVM plans.")

    t0 = time.perf_counter()

    df = (
        spark.range(100_000)
        .withColumn(
            "word",
            F.when((F.col("id") % 5) == 0, F.lit("spark"))
             .when((F.col("id") % 5) == 1, F.lit("fast"))
             .when((F.col("id") % 5) == 2, F.lit("scalable"))
             .when((F.col("id") % 5) == 3, F.lit("powerful"))
             .otherwise(F.lit("data"))
        )
    )

    result_df = (
        df.groupBy("word")
          .count()
          .orderBy(F.desc("count"), F.asc("word"))
    )

    result_df.show(truncate=False)

    t1 = time.perf_counter()

    print(f"DataFrame JVM execution time: {(t1 - t0) * 1000:.2f} ms")
    print("WHY DataFrame wins: Catalyst optimizer can inspect and optimize columns.")
    print("WHY RDD matters: it teaches Spark's low-level MapReduce execution model.")


def show_dag_stages(spark: SparkSession) -> None:
    """
    Show Spark query plan and DAG stages.

    Sections:
      Parsed Logical Plan    — what you wrote
      Analyzed Logical Plan  — resolved names and types
      Optimized Logical Plan — Catalyst optimizations
      Physical Plan          — actual execution plan and shuffles
    """
    df = spark.range(100_000)

    df_transformed = (
        df.filter(F.col("id") % 2 == 0)
          .groupBy((F.col("id") % 10).alias("bucket"))
          .count()
          .orderBy(F.desc("count"))
    )

    print("\n=== EXPLAIN PLAN ===")
    df_transformed.explain(True)


def main() -> None:
    spark = None

    try:
        spark = create_spark_session()

        print("\n=== LAZY EVALUATION ===")
        demonstrate_lazy_evaluation(spark)

        print("\n=== WORD COUNT / RDD CONCEPT ===")
        sample_text = """
        Toyota builds cars in plants across the world. Each plant has sensors
        monitoring temperature pressure and vibration. The sensors report data
        to a central system that processes the data and builds reports.
        """ * 100

        top10 = rdd_word_count(spark, sample_text)

        print("\nReturned top 10 list:")
        for word, count in top10:
            print(f"  {word:<15} {count}")

        print("\n=== RDD vs DATAFRAME ===")
        compare_rdd_vs_dataframe(spark)

        print("\n=== DAG / QUERY PLAN ===")
        show_dag_stages(spark)

    finally:
        if spark:
            spark.stop()


if __name__ == "__main__":
    main()