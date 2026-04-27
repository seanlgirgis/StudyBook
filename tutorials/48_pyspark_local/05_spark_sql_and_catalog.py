# ============================================================
# Topic   : PySpark for Data Engineers
# File    : 05_spark_sql_and_catalog.py
# Covers  : Temp views, Spark SQL, window functions, UDF concepts, SQL execution plans
# Prereqs : pip install pyspark | Java 11+ installed, JAVA_HOME set
# Run     : python -u .\05_spark_sql_and_catalog.py
# ============================================================

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
import os
import sys
import time
from pathlib import Path


def has_winutils() -> bool:
    hadoop_home = os.getenv("HADOOP_HOME") or os.getenv("hadoop.home.dir")
    if not hadoop_home:
        return False
    return (Path(hadoop_home) / "bin" / "winutils.exe").exists()


def create_spark_session(app_name: str = "05-sql") -> SparkSession:
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

    if os.name == "nt" and not has_winutils():
        print("\nWINDOWS NOTE:")
        print("  winutils.exe is not configured.")
        print("  Spark catalog APIs may fail because they touch Hadoop local filesystem.")
        print("  This file uses temp views directly and skips unsafe catalog operations.")

    return spark


def create_sales_df(spark: SparkSession, n_rows: int = 100_000) -> DataFrame:
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
        .withColumn("date", F.date_sub(F.current_date(), (F.col("id") % 1095).cast("int")))
        .withColumn("region", F.element_at(regions, ((F.col("id") % 5) + 1).cast("int")))
        .withColumn("model", F.element_at(models, ((F.col("id") % 10) + 1).cast("int")))
        .withColumn("units", ((F.col("id") % 5) + 1).cast("long"))
        .withColumn("unit_price", (F.lit(15000) + (F.col("id") % 40000)).cast("double"))
        .withColumn("revenue", (F.col("units") * F.col("unit_price")).cast("double"))
        .withColumn("salesperson", F.format_string("SP-%03d", F.col("id") % 50))
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


def register_temp_views(dfs: dict[str, DataFrame]) -> None:
    print("\n=== REGISTER TEMP VIEWS ===")

    for name, df in dfs.items():
        df.createOrReplaceTempView(name)
        print(f"Registered temp view: {name}")

    print("\nCatalog listTables skipped on this Windows runtime.")
    print("WHY:")
    print("  spark.catalog.listTables() can initialize Hadoop local filesystem.")
    print("  Without winutils.exe, that fails on Windows.")
    print("\nTemp views still work:")
    print("  - sales")
    print("  - targets")


def run_analytical_sql(spark: SparkSession) -> DataFrame:
    print("\n=== ANALYTICAL SQL ===")

    query = """
    WITH monthly AS (
        SELECT
            region,
            model,
            YEAR(date) AS year,
            MONTH(date) AS month,
            DATE_TRUNC('month', date) AS month_start,
            SUM(revenue) AS monthly_revenue,
            COUNT(*) AS sale_count
        FROM sales
        GROUP BY region, model, YEAR(date), MONTH(date), DATE_TRUNC('month', date)
    ),
    ranked AS (
        SELECT
            *,
            RANK() OVER (
                PARTITION BY region, year, month
                ORDER BY monthly_revenue DESC
            ) AS model_rank
        FROM monthly
    ),
    with_lag AS (
        SELECT
            region,
            model,
            year,
            month,
            month_start,
            monthly_revenue,
            sale_count,
            model_rank,
            LAG(monthly_revenue, 1) OVER (
                PARTITION BY region, model
                ORDER BY year, month
            ) AS prev_month_revenue
        FROM ranked
    )
    SELECT
        region,
        model,
        year,
        month,
        monthly_revenue,
        prev_month_revenue,
        ROUND(
            (monthly_revenue - prev_month_revenue)
            / NULLIF(prev_month_revenue, 0) * 100,
            2
        ) AS mom_growth_pct,
        model_rank
    FROM with_lag
    WHERE model_rank <= 3
    ORDER BY region, year, month, model_rank
    """

    df = spark.sql(query)
    df.show(20, truncate=False)

    print("\nWHY this matters:")
    print("  Spark SQL supports CTEs, aggregation, rank, lag, and growth calculations.")
    print("  These are common analytics-engineering interview patterns.")

    return df


def run_join_sql(spark: SparkSession) -> None:
    print("\n=== SQL JOIN ===")

    df = spark.sql("""
        SELECT
            s.region,
            COUNT(*) AS sale_count,
            ROUND(SUM(s.revenue), 2) AS total_revenue,
            MAX(t.revenue_target) AS revenue_target,
            ROUND(SUM(s.revenue) - MAX(t.revenue_target), 2) AS variance_to_target
        FROM sales s
        INNER JOIN targets t
            ON s.region = t.region
        GROUP BY s.region
        ORDER BY total_revenue DESC
    """)

    df.show(truncate=False)

    print("\nWHY this matters:")
    print("  Fact table + dimension/target table joins are core data engineering work.")


def create_builtin_classification(spark: SparkSession) -> None:
    print("\n=== BUILT-IN CLASSIFICATION INSTEAD OF PYTHON UDF ===")

    t0 = time.perf_counter()

    df = spark.sql("""
        SELECT
            sale_id,
            region,
            model,
            revenue,
            CASE
                WHEN revenue >= 200000 THEN 'PREMIUM'
                WHEN revenue >= 100000 THEN 'HIGH'
                WHEN revenue >= 50000  THEN 'MEDIUM'
                ELSE 'LOW'
            END AS revenue_class
        FROM sales
        LIMIT 10
    """)

    df.show(truncate=False)

    elapsed = (time.perf_counter() - t0) * 1000

    print(f"Built-in CASE expression time: {elapsed:.2f} ms")
    print("\nWHY not Python UDF here:")
    print("  Python UDFs serialize data JVM -> Python -> JVM.")
    print("  They are slower and less optimizable than built-in Spark expressions.")
    print("  Prefer CASE WHEN / F.when whenever possible.")


def create_pandas_udf_concept() -> None:
    print("\n=== PANDAS UDF CONCEPT ===")

    print("Pandas UDF example pattern:")
    print("""
    @F.pandas_udf(StringType())
    def classify_revenue_pandas(series: pd.Series) -> pd.Series:
        return series.apply(lambda x: "HIGH" if x > 100000 else "LOW")
    """)

    print("WHY Pandas UDF:")
    print("  Processes column batches using Apache Arrow.")
    print("  Usually faster than row-by-row Python UDFs.")
    print("  Still usually slower than built-in Spark expressions.")

    print("\nSkipped execution:")
    print("  Your Windows runtime has Python worker instability.")
    print("  Built-ins are preferred anyway for performance and optimizer support.")


def catalog_operations_concept(spark: SparkSession, dfs: dict[str, DataFrame]) -> None:
    print("\n=== CATALOG CONCEPTS ===")

    print("Current database concept: default")
    print("\nKnown temp views from this script:")
    for name, df in dfs.items():
        print(f"\nView: {name}")
        print("Columns:")
        for col_name, dtype in df.dtypes:
            print(f"  {col_name:<18} {dtype}")

    print("\nCatalog APIs you would normally use:")
    print("  spark.catalog.currentDatabase()")
    print("  spark.catalog.listDatabases()")
    print("  spark.catalog.listTables()")
    print("  spark.catalog.listColumns('sales')")
    print("  spark.catalog.cacheTable('sales')")
    print("  spark.catalog.uncacheTable('sales')")

    print("\nSkipped live catalog calls:")
    print("  On this Windows machine, those APIs can hit Hadoop local filesystem.")
    print("  Without winutils.exe / HADOOP_HOME, they can fail even for temp views.")


def explain_sql_plan(spark: SparkSession) -> None:
    print("\n=== SQL EXPLAIN PLAN ===")

    df = spark.sql("""
        SELECT
            region,
            SUM(revenue) AS total_revenue
        FROM sales
        WHERE revenue > 100000
        GROUP BY region
        ORDER BY total_revenue DESC
    """)

    df.explain(True)

    print("\nLook for:")
    print("  Filter         -> WHERE clause")
    print("  HashAggregate  -> GROUP BY")
    print("  Exchange       -> shuffle")
    print("  Sort           -> ORDER BY")


def main() -> None:
    spark = None

    try:
        spark = create_spark_session("05-sql")

        df_sales = create_sales_df(spark, n_rows=100_000)
        df_targets = create_targets_df(spark)

        dfs = {
            "sales": df_sales,
            "targets": df_targets,
        }

        register_temp_views(dfs)
        run_analytical_sql(spark)
        run_join_sql(spark)
        create_builtin_classification(spark)
        create_pandas_udf_concept()
        catalog_operations_concept(spark, dfs)
        explain_sql_plan(spark)

    finally:
        if spark:
            spark.stop()


if __name__ == "__main__":
    main()