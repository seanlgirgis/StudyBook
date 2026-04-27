# ChatGPT Prompt — PySpark for Data Engineers
# READY TO PASTE — fully specified, no placeholders
# Paste everything between the === markers into ChatGPT

===

TOPIC: PySpark for Data Engineers
SLUG: pyspark
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: Pure Python — PySpark local mode (no cluster, no AWS, no Docker)
NO CLEANUP RULES NEEDED — no billable resources created.

===== CODING STANDARDS =====

FILE HEADER (every file):
# ============================================================
# Topic   : PySpark for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install pyspark | Java 11+ installed, JAVA_HOME set
# Run     : python NN_filename.py
# ============================================================

CRITICAL — CODE QUALITY:
- Every function COMPLETE and FULLY RUNNABLE — no placeholders, no TODO, no pass.
- Generate the ENTIRE file every time.
- Comments explain WHY — lazy evaluation, shuffle, DAG, GIL bypass are the concepts
  Toyota interviewers ask about. Make every Spark-specific behavior explicit.
- SparkSession: always master("local[*]") and appName with file number.
- Stop SparkSession in a finally block: spark.stop()
- Output dir: OUTPUT_DIR env var or C:/tmp/studybook/pyspark/ (Windows) / /tmp/studybook/pyspark/
- Detect platform with os.name. Use pathlib.Path.
- Seed all random data with fixed seed for reproducibility.

===== FILE 01: 01_spark_session_and_rdds.py =====

from pyspark.sql import SparkSession
from pyspark import SparkContext
import os, time
from pathlib import Path

def get_output_dir() -> Path: ...

def create_spark_session(app_name: str = "01-spark-basics",
                         cores: str = "*") -> SparkSession:
    """
    Create SparkSession in local mode.
    .master(f"local[{cores}]") — [*] uses all cores, [2] caps at 2.
    .config("spark.sql.shuffle.partitions", "8") — reduce from default 200 for local mode.
    .config("spark.ui.enabled", "false") — disable web UI for tutorial scripts.
    WHY shuffle.partitions=8: default 200 means 200 empty tasks for small datasets.
    Always tune this for local mode. In production: 2-3× CPU cores.
    Print Spark version and master URL after creation.
    Return SparkSession.
    """

def demonstrate_lazy_evaluation(spark: SparkSession) -> None:
    """
    Prove that transformations are lazy — nothing runs until an action.
    Steps:
      1. Create RDD from range(1_000_000)
      2. Apply .map(lambda x: x * 2).filter(lambda x: x % 3 == 0) — NO PRINT YET
      3. Print "Transformations defined. Nothing computed yet."
      4. Time spark.sparkContext.parallelize(range(1_000_000)).count() — this triggers execution
      5. Print "Action triggered. Computation complete."
    WHY lazy evaluation: Spark builds a DAG of transformations first, then optimizes
    the execution plan before running. This enables predicate pushdown, stage fusion,
    and other optimizations impossible in eager (pandas) frameworks.
    """

def rdd_word_count(spark: SparkSession, text: str) -> list[tuple[str, int]]:
    """
    Classic word count on RDD.
    Steps: parallelize lines → flatMap split → map to (word, 1) → reduceByKey sum
    Sort by count descending. Return top 10 as list of (word, count) tuples.
    Print formatted table.
    WHY RDD word count: it's the canonical Spark example that demonstrates
    the MapReduce programming model. Every Spark interview includes this.
    """

def compare_rdd_vs_dataframe(spark: SparkSession) -> None:
    """
    Same aggregation (word frequency) done two ways:
      RDD API:       sc.parallelize → map → reduceByKey → sortBy
      DataFrame API: spark.createDataFrame → groupBy → count → orderBy
    Time both. Print:
      RDD:       {time_ms} ms
      DataFrame: {time_ms} ms  (usually faster — Catalyst optimizer)
    WHY DataFrame wins: Catalyst optimizer generates optimized JVM bytecode.
    RDD is untyped Python — Spark can't optimize inside the lambda functions.
    WHY RDD still matters: custom accumulators, streaming, ML pipelines still use RDD.
    """

def show_dag_stages(spark: SparkSession) -> None:
    """
    Show the query plan using df.explain(mode="formatted").
    Create a DataFrame with a filter + groupBy + sort.
    Call df.explain(True) and print the output.
    Explain in comments what each section means:
      == Parsed Logical Plan ==   — what you wrote
      == Analyzed Logical Plan == — after type resolution
      == Optimized Logical Plan == — after Catalyst optimization (predicate pushdown, etc.)
      == Physical Plan ==          — actual execution plan (sort merge join vs broadcast join)
    """

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

===== FILE 02: 02_dataframe_operations.py =====

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window
import random
from pathlib import Path

def get_output_dir() -> Path: ...

def create_spark_session() -> SparkSession: ...  # same as file 01

def create_sales_df(spark: SparkSession, n_rows: int = 100_000) -> DataFrame:
    """
    Generate synthetic sales dataset with pandas then convert to Spark DataFrame.
    Columns:
      sale_id:    string  "SALE-{i:07d}"
      date:       date    random within last 3 years
      region:     string  one of ["North","South","East","West","Central"]
      model:      string  one of 10 Toyota models (Camry, Corolla, RAV4, etc.)
      units:      int     1–5
      unit_price: float   15000–55000 (realistic car prices)
      revenue:    float   units × unit_price
      salesperson:string  "SP-{i%50:03d}"
    Introduce 2% null revenue rows and 1% duplicate sale_ids for cleaning demo.
    Seed = 42. Print schema and row count.
    """

def basic_transformations(df: DataFrame) -> DataFrame:
    """
    Demonstrate:
      select   : pick subset of columns
      filter   : revenue > 50000
      withColumn: add margin_pct = (revenue - units*30000) / revenue
      drop     : remove sale_id
      withColumnRenamed: rename region → sales_region
    Print count at each step to show row count changes.
    Return final transformed DataFrame.
    WHY withColumn not UDF: built-in F.col expressions run in JVM.
    Python UDFs serialize data through the Python interpreter — 10-100× slower.
    """

def aggregations_and_groupby(df: DataFrame) -> DataFrame:
    """
    Three aggregation patterns:
      1. Simple groupBy:
           df.groupBy("region").agg(
               F.sum("revenue").alias("total_revenue"),
               F.avg("units").alias("avg_units"),
               F.count("*").alias("sale_count"))
      2. Pivot table: region × model → total_revenue
           df.groupBy("region").pivot("model").sum("revenue")
      3. Multi-level aggregation:
           df.groupBy("region", "model").agg(F.sum("revenue"))
             .groupBy("region").agg(F.sum("sum(revenue)").alias("regional_total"))
    Print each result with .show(5).
    WHY pivot: generates a column per unique model — equivalent to CASE WHEN in SQL.
    Expensive (requires two passes) but essential for report generation.
    Return the simple groupBy result DataFrame.
    """

def join_patterns(spark: SparkSession, df: DataFrame) -> None:
    """
    Create a targets DataFrame: region → revenue_target.
    Demonstrate:
      inner join: only regions with targets
      left join:  all sales, null target if region not in targets
      broadcast join: F.broadcast(targets) — avoids shuffle when one table is small
    For each join: print row count and first 5 rows.
    Explain in comments:
      WHY broadcast join: if one table fits in executor memory (< spark.sql.autoBroadcastJoinThreshold,
      default 10MB), Spark sends it to all workers instead of shuffling both tables.
      A shuffle join on 100M rows can take minutes; a broadcast join takes seconds.
    """

def window_functions(df: DataFrame) -> DataFrame:
    """
    Three window function patterns:
      1. Rank per region by revenue:
           Window.partitionBy("region").orderBy(F.desc("revenue"))
           F.rank().over(window_spec)
      2. Running total of revenue by date (global, ordered by date):
           Window.orderBy("date").rowsBetween(Window.unboundedPreceding, Window.currentRow)
           F.sum("revenue").over(running_total_spec)
      3. Lag/Lead: previous and next day's revenue per region:
           Window.partitionBy("region").orderBy("date")
           F.lag("revenue", 1).over(lag_spec)
           F.lead("revenue", 1).over(lead_spec)
    Print each with .show(10).
    WHY window functions: they compute values relative to a group without collapsing rows.
    Essential for YoY growth, running totals, ranking, and moving averages.
    Return DataFrame with rank column added.
    """

def null_handling(df: DataFrame) -> DataFrame:
    """
    Demonstrate:
      df.filter(F.col("revenue").isNull()).count()  — count nulls
      df.fillna({"revenue": 0, "units": 1})         — fill by column
      df.dropna(subset=["revenue"])                  — drop rows with null revenue
      F.coalesce(F.col("revenue"), F.lit(0))         — inline null replacement
      F.when(F.col("revenue") > 100000, "HIGH")
       .when(F.col("revenue") > 50000, "MED")
       .otherwise("LOW").alias("tier")               — conditional column
    Print null counts before and after.
    Return cleaned DataFrame.
    """

def main():
    spark = None
    try:
        spark = create_spark_session("02-dataframe-ops")
        df = create_sales_df(spark, n_rows=100_000)

        print("\n=== BASIC TRANSFORMATIONS ===")
        df_clean = basic_transformations(df)

        print("\n=== AGGREGATIONS ===")
        df_agg = aggregations_and_groupby(df)

        print("\n=== JOIN PATTERNS ===")
        join_patterns(spark, df)

        print("\n=== WINDOW FUNCTIONS ===")
        df_ranked = window_functions(df)

        print("\n=== NULL HANDLING ===")
        df_nulls = null_handling(df)
        print(f"Rows after null drop: {df_nulls.count()}")
    finally:
        if spark: spark.stop()

if __name__ == "__main__":
    main()

===== FILE 03: 03_reading_and_writing.py =====

Functions:

def read_csv_with_schema(spark, path: str) -> DataFrame:
    """
    Read CSV two ways:
      A. schema inference: spark.read.option("inferSchema", True).option("header", True).csv(path)
      B. explicit schema: define StructType, read with schema=
    Print time for each. Print schema for each.
    WHY explicit schema: inferSchema reads the entire file twice (one pass to infer,
    one to load). For 10GB files this doubles read time. Always define schema in production.
    WHY header=True: without it, Spark treats row 1 as data.
    """

def read_json_nested(spark, path: str) -> DataFrame:
    """
    Read JSON with nested structure: { sale_id, customer: { name, region }, items: [...] }
    Generate 1000 such records, write as JSON, read back.
    Demonstrate:
      df.select("customer.name", "customer.region")  — dot notation for nested fields
      F.explode("items")                              — expand array to rows
      df.select(F.col("items")[0].alias("first_item")) — array indexing
    Print schema before and after explode.
    """

def write_parquet_partitioned(df: DataFrame, path: str,
                               partition_cols: list[str]) -> None:
    """
    Write DataFrame as Parquet with hive partitioning.
    df.write.mode("overwrite").partitionBy(*partition_cols)
      .option("compression", "snappy").parquet(path)
    Print: file count per partition, total size.
    WHY partitionBy: queries with WHERE region='North' skip all other region folders.
    Partition pruning can reduce I/O by 80%+ on large datasets.
    WHY snappy: default Parquet compression. Good balance of speed and ratio.
    """

def read_with_predicate_pushdown(spark, path: str,
                                  filter_col: str, filter_val: str) -> DataFrame:
    """
    Read partitioned Parquet with and without filter. Time both.
    df_full     = spark.read.parquet(path)
    df_filtered = spark.read.parquet(path).filter(F.col(filter_col) == filter_val)
    Call df.explain() on filtered version — show "PartitionFilters" in physical plan.
    WHY pushdown: Spark passes the filter to the file scanner. Only matching partition
    folders are opened. The JVM never reads data it will discard.
    Print files scanned count (from ScanMetrics if available).
    """

def compare_format_performance(spark, output_dir: Path) -> dict:
    """
    Write same 100k-row DataFrame as CSV, JSON, Parquet (snappy), Parquet (zstd).
    Read each back 3 times, take median.
    Return: { csv: {size_mb, write_ms, read_ms}, json: {...}, parquet_snappy: {...}, parquet_zstd: {...} }
    Print comparison table sorted by read_ms.
    """

def main():
    spark = None
    try:
        spark = create_spark_session("03-io")
        out   = get_output_dir()

        # Generate and write sample data
        df = create_sales_df(spark, n_rows=100_000)

        csv_path = str(out / "sales.csv")
        df.toPandas().to_csv(csv_path, index=False)

        print("\n=== CSV SCHEMA INFERENCE vs EXPLICIT ===")
        read_csv_with_schema(spark, csv_path)

        json_path = str(out / "sales_nested.json")
        print("\n=== NESTED JSON ===")
        read_json_nested(spark, json_path)

        parquet_path = str(out / "sales_partitioned")
        print("\n=== WRITE PARTITIONED PARQUET ===")
        write_parquet_partitioned(df, parquet_path, ["region"])

        print("\n=== PREDICATE PUSHDOWN ===")
        read_with_predicate_pushdown(spark, parquet_path, "region", "North")

        print("\n=== FORMAT PERFORMANCE ===")
        stats = compare_format_performance(spark, out)
        for fmt, s in sorted(stats.items(), key=lambda x: x[1]["read_ms"]):
            print(f"  {fmt:<20} {s['size_mb']:6.1f} MB  read {s['read_ms']:.0f}ms")
    finally:
        if spark: spark.stop()

if __name__ == "__main__":
    main()

===== FILE 04: 04_performance_tuning.py =====

Functions (all fully implemented):

def demonstrate_shuffle_cost(spark) -> dict:
    """
    Create large_df (1M rows) and small_df (200 rows — region targets).
    Join WITHOUT broadcast:
      spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")  # disable auto-broadcast
      large_df.join(small_df, "region").count()  — forces SortMergeJoin (expensive shuffle)
    Join WITH broadcast:
      spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10485760")  # re-enable
      large_df.join(F.broadcast(small_df), "region").count()
    Time both. Print speedup. Show physical plan difference (SortMergeJoin vs BroadcastHashJoin).
    Return { no_broadcast_ms, broadcast_ms, speedup_x }
    """

def optimize_partitions(spark, df) -> None:
    """
    Show effect of partition count on performance:
      df.rdd.getNumPartitions()   — current partition count
      df.repartition(200)         — increase (for joins/aggregations)
      df.coalesce(4)              — decrease (for writing fewer files)
    WHY repartition vs coalesce:
      repartition: full shuffle, even distribution — use before wide operations
      coalesce: avoids shuffle, can be uneven — use only for reducing partitions before write
    Benchmark groupBy on both. Print partition count and time.
    """

def cache_vs_persist(spark, df) -> dict:
    """
    Run the same groupBy aggregation on df three times:
      1. No cache: time all 3 runs
      2. df.cache() (MEMORY_AND_DISK): time all 3 runs
      3. df.persist(StorageLevel.MEMORY_ONLY): time all 3 runs
    Compare first run vs subsequent runs.
    Return { no_cache_avg_ms, cached_avg_ms, speedup_x }
    WHY cache: if a DataFrame is used multiple times (ML iterations, multiple aggregations),
    caching avoids re-reading and re-computing from the source.
    WHY not always cache: caching evicts other data from executor memory. Use only for
    DataFrames that are reused 2+ times and are expensive to recompute.
    """

def detect_data_skew(df, key_col: str) -> dict:
    """
    Count records per unique key_col value.
    Return:
      { total_rows, unique_keys, top_key, top_key_count, top_key_pct,
        median_count, skew_ratio (top/median), is_skewed: bool }
    is_skewed = True if skew_ratio > 10.
    Print warning if skewed with fix suggestions:
      - Salting: add random suffix to hot key, join on salted key, aggregate back
      - AQE (Adaptive Query Execution): spark.sql.adaptive.enabled=true (Spark 3.0+)
    """

def tune_shuffle_partitions(spark, df) -> None:
    """
    Run groupBy with shuffle.partitions = 8, 50, 200, 400.
    Time each. Print table: partitions → time_ms → recommendation.
    Explain:
      Too few: large partitions, OOM risk
      Too many: task scheduling overhead, tiny partitions
      Rule of thumb: target 128MB per partition after shuffle
    Show: spark.conf.set("spark.sql.adaptive.enabled", "true") enables AQE
    to auto-tune partitions in Spark 3.0+.
    """

def main():
    spark = None
    try:
        spark = create_spark_session("04-performance")
        df = create_sales_df(spark, n_rows=1_000_000)

        print("\n=== BROADCAST JOIN SPEEDUP ===")
        stats = demonstrate_shuffle_cost(spark)
        print(f"Speedup: {stats['speedup_x']:.1f}×")

        print("\n=== PARTITION OPTIMIZATION ===")
        optimize_partitions(spark, df)

        print("\n=== CACHE vs PERSIST ===")
        cache_stats = cache_vs_persist(spark, df)
        print(f"Cache speedup: {cache_stats['speedup_x']:.1f}×")

        print("\n=== SKEW DETECTION ===")
        skew_stats = detect_data_skew(df, "region")
        print(skew_stats)

        print("\n=== SHUFFLE PARTITION TUNING ===")
        tune_shuffle_partitions(spark, df)
    finally:
        if spark: spark.stop()

if __name__ == "__main__":
    main()

===== FILE 05: 05_spark_sql_and_catalog.py =====

Functions:

def register_temp_views(spark, dfs: dict[str, DataFrame]) -> None:
    """
    Register each DataFrame in dfs as a temp view.
    dfs = {"sales": df_sales, "targets": df_targets, "regions": df_regions}
    Call df.createOrReplaceTempView(name) for each.
    List registered views via spark.catalog.listTables().
    WHY temp views: let you mix DataFrame API and SQL in the same session.
    Temp views are session-scoped — gone when SparkSession closes.
    """

def run_analytical_sql(spark) -> DataFrame:
    """
    Run a complex SQL query using Spark SQL:
    WITH monthly AS (
        SELECT region, model,
               DATE_TRUNC('month', date) AS month,
               SUM(revenue) AS monthly_revenue
        FROM sales GROUP BY 1,2,3
    ),
    ranked AS (
        SELECT *, RANK() OVER (PARTITION BY region, month ORDER BY monthly_revenue DESC) AS rank
        FROM monthly
    )
    SELECT region, model, month, monthly_revenue,
           LAG(monthly_revenue) OVER (PARTITION BY region, model ORDER BY month) AS prev_month,
           ROUND((monthly_revenue - LAG(monthly_revenue) OVER (
               PARTITION BY region, model ORDER BY month)) /
               NULLIF(LAG(monthly_revenue) OVER (
               PARTITION BY region, model ORDER BY month), 0) * 100, 2) AS mom_growth_pct
    FROM ranked WHERE rank <= 3
    ORDER BY region, month, rank
    Print .show(20). Return DataFrame.
    """

def create_python_udf(spark) -> None:
    """
    Register a Python UDF: classify_revenue(revenue: float) → str
    Returns "LOW" / "MEDIUM" / "HIGH" / "PREMIUM" based on thresholds.
    Register with spark.udf.register("classify_revenue", fn, StringType()).
    Run via SQL: SELECT classify_revenue(revenue) FROM sales LIMIT 5.
    Time 100k rows.
    Explain in comments:
      WHY Python UDFs are slow: every row crosses the JVM→Python boundary via pickle.
      Data is serialized, deserialized, processed in Python, serialized back.
      For 1M rows this can be 10-100× slower than a built-in F.when() expression.
      Use UDFs only when no built-in alternative exists.
    """

def create_pandas_udf(spark) -> None:
    """
    Implement same classify_revenue as a Pandas UDF (vectorized):
    @F.pandas_udf(StringType())
    def classify_revenue_pandas(series: pd.Series) -> pd.Series:
        return series.apply(lambda x: "HIGH" if x > 100000 else "LOW")
    Time on 100k rows vs Python UDF.
    WHY Pandas UDF: processes data in columnar batches using Apache Arrow.
    No per-row pickle overhead. Typically 5-20× faster than Python UDF.
    Still slower than built-in expressions but much more flexible.
    """

def catalog_operations(spark) -> None:
    """
    Demonstrate the Spark catalog API:
      spark.catalog.currentDatabase()
      spark.catalog.listDatabases()
      spark.catalog.listTables()
      spark.catalog.listColumns("sales")
      spark.catalog.isCached("sales")
    Print formatted output for each.
    WHY catalog: in production (with a Hive metastore or Unity Catalog),
    this API discovers tables, schemas, and partitions programmatically.
    """

def main():
    spark = None
    try:
        spark = create_spark_session("05-sql")
        df_sales   = create_sales_df(spark, n_rows=50_000)
        df_targets = spark.createDataFrame(
            [("North", 5e6), ("South", 4e6), ("East", 4.5e6),
             ("West", 6e6), ("Central", 3.5e6)],
            ["region", "revenue_target"])

        print("\n=== REGISTER TEMP VIEWS ===")
        register_temp_views(spark, {"sales": df_sales, "targets": df_targets})

        print("\n=== ANALYTICAL SQL ===")
        run_analytical_sql(spark)

        print("\n=== PYTHON UDF ===")
        create_python_udf(spark)

        print("\n=== PANDAS UDF ===")
        create_pandas_udf(spark)

        print("\n=== CATALOG ===")
        catalog_operations(spark)
    finally:
        if spark: spark.stop()

if __name__ == "__main__":
    main()

===== CAPSTONE PROJECT =====

Title: Manufacturing Sales Analytics Pipeline
Scenario: 1M Toyota regional sales records → clean → aggregate → YoY growth → top-5 ranking
→ partitioned Parquet output → performance report.

Directory layout:
  capstone/
    capstone.py         ← full pipeline
    test_capstone.py    ← pytest with SparkSession fixture

===== CAPSTONE FILE: capstone.py =====

"""
Toyota Manufacturing Sales Analytics Pipeline — PySpark capstone.

Pipeline:
  1. Generate 1M synthetic sales records
  2. Clean: drop duplicates, fill nulls, validate revenue > 0
  3. Aggregate: monthly revenue by region × model
  4. YoY growth: window function comparing same month prior year
  5. Top-5 ranking: rank models per region per quarter
  6. Write: partitioned Parquet by year/region (snappy)
  7. Report: total time, records, partition count, file sizes
"""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import *
import os, time
from pathlib import Path

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR",
    "C:/tmp/studybook/pyspark" if os.name == "nt" else "/tmp/studybook/pyspark"))
MODELS = ["Camry","Corolla","RAV4","Highlander","Tacoma",
          "Tundra","Prius","Sienna","4Runner","Venza"]
REGIONS = ["North","South","East","West","Central"]

def create_spark_session() -> SparkSession:
    """Local[*], shuffle.partitions=20, UI disabled."""

def generate_sales_data(spark: SparkSession, n_rows: int = 1_000_000) -> DataFrame:
    """
    Generate n_rows sales records. Columns:
      sale_id, date (last 3 years random), region, model, units (1-5),
      unit_price (15000-55000), revenue (units × unit_price), salesperson
    Introduce 2% null revenue, 1% duplicate sale_ids.
    Use spark.range(n_rows) + withColumn expressions + F.rand(seed=42).
    Print: "Generated {n:,} rows in {ms}ms"
    """

def clean_data(df: DataFrame) -> DataFrame:
    """
    1. Drop duplicate sale_ids (keep first occurrence)
    2. Fill null revenue with units × unit_price (recalculate)
    3. Filter revenue > 0
    4. Add year, month, quarter columns from date
    Print: rows before → rows after, nulls fixed, dupes dropped.
    Return cleaned DataFrame. Cache it (used in multiple downstream steps).
    """

def monthly_revenue_by_region_model(df: DataFrame) -> DataFrame:
    """
    GROUP BY year, month, region, model → SUM(revenue), COUNT(*), AVG(units).
    Sort by year, month, region, model.
    Print: .show(10).
    Return DataFrame.
    """

def calculate_yoy_growth(df: DataFrame) -> DataFrame:
    """
    For each region × model × month combination, calculate:
      yoy_growth_pct = (current_month_revenue - same_month_prior_year) / same_month_prior_year × 100
    Use Window.partitionBy("region", "model", "month").orderBy("year")
    and F.lag("total_revenue", 1) for prior year revenue.
    Filter out rows where prior year is null (first year).
    Print .show(15). Return DataFrame.
    """

def rank_top5_per_region_quarter(df: DataFrame) -> DataFrame:
    """
    Aggregate to quarterly revenue: year, quarter, region, model → quarterly_revenue.
    Rank models within (region, quarter) by quarterly_revenue DESC.
    Filter rank <= 5. Return DataFrame.
    Print: .show(20).
    """

def write_output(df: DataFrame, path: Path) -> dict:
    """
    Write as partitioned Parquet: partitionBy("year", "region"), snappy compression.
    Return:
      { output_path, partition_count, total_files, total_size_mb, write_ms }
    Compute file count and size by walking output_path with pathlib.
    """

def print_report(generate_ms: float, clean_stats: dict,
                 write_stats: dict, total_ms: float) -> None:
    """
    ╔═══════════════════════════════════════════╗
    ║  PySpark Sales Analytics — Report          ║
    ╠═══════════════════════════════════════════╣
    ║  Records generated   :  1,000,000          ║
    ║  Records after clean :    982,341          ║
    ║  Dupes dropped       :      9,872          ║
    ║  Nulls fixed         :     19,654          ║
    ║  Partitions written  :         15          ║
    ║  Output size         :      42.3 MB        ║
    ║  Total time          :      38.4 s         ║
    ╚═══════════════════════════════════════════╝
    """

def main():
    spark = None
    try:
        spark = create_spark_session()
        out   = OUTPUT_DIR / "capstone_output"

        t0 = time.perf_counter()

        t1 = time.perf_counter()
        df_raw = generate_sales_data(spark, 1_000_000)
        generate_ms = (time.perf_counter() - t1) * 1000

        df_clean = clean_data(df_raw)
        df_monthly = monthly_revenue_by_region_model(df_clean)
        df_yoy = calculate_yoy_growth(df_monthly)
        df_top5 = rank_top5_per_region_quarter(df_monthly)
        write_stats = write_output(df_yoy, out)

        total_ms = (time.perf_counter() - t0) * 1000
        print_report(generate_ms, {}, write_stats, total_ms)

        # Verify output with SQL
        df_verify = spark.read.parquet(str(out))
        print(f"\nVerification: {df_verify.count():,} rows in output Parquet")
    finally:
        if spark: spark.stop()

if __name__ == "__main__":
    main()

===== CAPSTONE FILE: test_capstone.py =====

"""pytest — 6 tests for the PySpark capstone."""
import pytest
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from capstone import (generate_sales_data, clean_data,
                       monthly_revenue_by_region_model,
                       calculate_yoy_growth, rank_top5_per_region_quarter)

@pytest.fixture(scope="session")
def spark():
    session = (SparkSession.builder
               .master("local[2]")
               .appName("test-capstone")
               .config("spark.sql.shuffle.partitions", "4")
               .config("spark.ui.enabled", "false")
               .getOrCreate())
    yield session
    session.stop()

@pytest.fixture(scope="session")
def df_clean(spark):
    df_raw = generate_sales_data(spark, n_rows=10_000)
    return clean_data(df_raw)

def test_generate_returns_correct_row_count(spark):
    df = generate_sales_data(spark, n_rows=5_000)
    # After dedup, slightly less than 5000 expected
    assert df.count() <= 5_000

def test_clean_removes_null_revenue(df_clean):
    null_count = df_clean.filter(F.col("revenue").isNull()).count()
    assert null_count == 0

def test_clean_removes_zero_revenue(df_clean):
    zero_count = df_clean.filter(F.col("revenue") <= 0).count()
    assert zero_count == 0

def test_monthly_agg_has_required_columns(df_clean):
    df_monthly = monthly_revenue_by_region_model(df_clean)
    required = {"year", "month", "region", "model", "total_revenue"}
    assert required.issubset(set(df_monthly.columns))

def test_top5_ranking_never_exceeds_5(df_clean):
    df_monthly = monthly_revenue_by_region_model(df_clean)
    df_top5 = rank_top5_per_region_quarter(df_monthly)
    max_rank = df_top5.agg(F.max("rank")).collect()[0][0]
    assert max_rank <= 5

def test_yoy_growth_has_no_nulls_after_filter(df_clean):
    df_monthly = monthly_revenue_by_region_model(df_clean)
    df_yoy = calculate_yoy_growth(df_monthly)
    # After filtering out first year, no prior_year_revenue should be null
    null_prior = df_yoy.filter(F.col("prior_year_revenue").isNull()).count()
    assert null_prior == 0

===== GENERATION SEQUENCE =====

Acknowledge these instructions, then wait for me to say "generate file 01".

  "generate file 01"  → 01_spark_session_and_rdds.py
  "generate file 02"  → 02_dataframe_operations.py
  "generate file 03"  → 03_reading_and_writing.py
  "generate file 04"  → 04_performance_tuning.py
  "generate file 05"  → 05_spark_sql_and_catalog.py
  "generate readme"   → README.md
  "generate capstone" → capstone/capstone.py
  "generate tests"    → capstone/test_capstone.py

Each file COMPLETE and FULLY RUNNABLE. No placeholders. No pass statements.

===
