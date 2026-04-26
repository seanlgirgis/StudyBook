# ============================================================
# Topic   : PySpark for Data Engineers
# File    : 01_spark_session_and_rdds.py
# Covers  : SparkSession, RDD basics, lazy evaluation, DAG, RDD vs DataFrame
# Prereqs : pip install pyspark | Java 11+ installed, JAVA_HOME set
# Run     : python 01_spark_session_and_rdds.py
# ============================================================

from pyspark.sql import SparkSession
from pyspark import SparkContext
import os, time
from pathlib import Path


def get_output_dir() -> Path:
    """
    Resolve output directory in a cross-platform way.
    Uses OUTPUT_DIR env var if set, otherwise defaults per OS.
    """
    base = os.getenv("OUTPUT_DIR")
    if base:
        return Path(base)
    if os.name == "nt":
        return Path("C:/tmp/studybook/pyspark")
    return Path("/tmp/studybook/pyspark")


def create_spark_session(app_name: str = "01-spark-basics",
                         cores: str = "*") -> SparkSession:
    """
    Create SparkSession in local mode.

    .master(f"local[{cores}]") — [*] uses all cores, [2] caps at 2.
    .config("spark.sql.shuffle.partitions", "8") — reduce from default 200 for local mode.
    .config("spark.ui.enabled", "false") — disable web UI for tutorial scripts.

    WHY shuffle.partitions=8:
      Default 200 creates many tiny empty tasks locally → overhead dominates compute.
      In production: tune ~2–3× CPU cores.

    Print Spark version and master URL after creation.
    """
    spark = (
        SparkSession.builder
        .appName(app_name)
        .master(f"local[{cores}]")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )

    print(f"Spark Version: {spark.version}")
    print(f"Master: {spark.sparkContext.master}")

    return spark


def demonstrate_lazy_evaluation(spark: SparkSession) -> None:
    """
    Prove that transformations are lazy — nothing runs until an action.

    WHY lazy evaluation:
      Spark builds a DAG (Directed Acyclic Graph) of transformations.
      It delays execution so it can optimize:
        - predicate pushdown
        - stage pipelining
        - avoiding unnecessary computation

      This is fundamentally different from pandas (eager execution).
    """
    sc = spark.sparkContext

    rdd = sc.parallelize(range(1_000_000))

    # Transformations (lazy)
    transformed = rdd.map(lambda x: x * 2).filter(lambda x: x % 3 == 0)

    print("Transformations defined. Nothing computed yet.")

    # Action (triggers execution)
    t0 = time.perf_counter()
    count = transformed.count()
    t1 = time.perf_counter()

    print(f"Action triggered. Count = {count}")
    print(f"Computation time: {(t1 - t0) * 1000:.2f} ms")

    print("Action triggered. Computation complete.")


def rdd_word_count(spark: SparkSession, text: str) -> list[tuple[str, int]]:
    """
    Classic word count using RDD API.

    Steps:
      parallelize → flatMap → map → reduceByKey → sort

    WHY:
      This demonstrates the MapReduce paradigm:
        Map: transform records → key-value pairs
        Reduce: aggregate values per key

      This is one of the most common Spark interview questions.
    """
    sc = spark.sparkContext

    lines = text.strip().split("\n")
    rdd = sc.parallelize(lines)

    counts = (
        rdd.flatMap(lambda line: line.lower().split())
           .map(lambda word: (word, 1))
           .reduceByKey(lambda a, b: a + b)
           .sortBy(lambda x: -x[1])
    )

    top10 = counts.take(10)

    print("\nTop 10 Words:")
    print("-------------------------")
    for word, count in top10:
        print(f"{word:<15} {count}")

    return top10


def compare_rdd_vs_dataframe(spark: SparkSession) -> None:
    """
    Compare RDD vs DataFrame performance.

    WHY DataFrame is faster:
      - Uses Catalyst optimizer (query planning)
      - Generates optimized JVM bytecode
      - Avoids Python execution overhead

    WHY RDD still exists:
      - Fine-grained control
      - Custom logic not expressible in SQL
    """
    sc = spark.sparkContext

    text = "spark is fast and spark is scalable and spark is powerful " * 10000

    # RDD
    t0 = time.perf_counter()
    rdd = sc.parallelize(text.split())
    rdd_result = (
        rdd.map(lambda w: (w, 1))
           .reduceByKey(lambda a, b: a + b)
           .collect()
    )
    t1 = time.perf_counter()

    # DataFrame
    from pyspark.sql import functions as F

    t2 = time.perf_counter()
    df = spark.createDataFrame([(w,) for w in text.split()], ["word"])
    df_result = (
        df.groupBy("word")
          .count()
          .orderBy(F.desc("count"))
          .collect()
    )
    t3 = time.perf_counter()

    print(f"RDD:       {(t1 - t0) * 1000:.2f} ms")
    print(f"DataFrame: {(t3 - t2) * 1000:.2f} ms")


def show_dag_stages(spark: SparkSession) -> None:
    """
    Show Spark query plan and DAG stages.

    WHY this matters:
      Interviewers often ask:
        "Explain Spark execution plan"
        "What is Catalyst optimizer?"
    """
    from pyspark.sql import functions as F

    df = spark.range(1000000)

    df_transformed = (
        df.filter(F.col("id") % 2 == 0)
          .groupBy((F.col("id") % 10).alias("bucket"))
          .count()
          .orderBy(F.desc("count"))
    )

    print("\n=== EXPLAIN PLAN ===")
    df_transformed.explain(True)

    # Explanation:
    # Parsed Logical Plan: raw query
    # Analyzed Logical Plan: types resolved
    # Optimized Logical Plan: Catalyst optimizations applied
    # Physical Plan: actual execution strategy


def main():
    spark = None
    try:
        spark = create_spark_session()

        print("\n=== LAZY EVALUATION ===")
        demonstrate_lazy_evaluation(spark)

        print("\n=== RDD WORD COUNT ===")
        sample_text = """
        Toyota builds cars in plants across the world. Each plant has sensors
        monitoring temperature pressure and vibration. The sensors report data
        to a central system that processes the data and builds reports.
        """ * 100

        top10 = rdd_word_count(spark, sample_text)
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