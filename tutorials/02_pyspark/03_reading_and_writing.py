# ============================================================
# Topic   : PySpark for Data Engineers
# File    : 03_reading_and_writing.py
# Covers  : CSV schema, JSON, Parquet concepts, partitioning, predicate pushdown
# Prereqs : pip install pyspark | Java 11+ installed, JAVA_HOME set
# Run     : python -u .\03_reading_and_writing.py
# ============================================================

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, LongType, DoubleType, DateType
)
from pathlib import Path
import csv
import json
import os
import shutil
import sys
import time


def get_output_dir() -> Path:
    base = os.getenv("OUTPUT_DIR")
    if base:
        return Path(base)

    if os.name == "nt":
        return Path("C:/tmp/studybook/pyspark")

    return Path("/tmp/studybook/pyspark")


def has_winutils() -> bool:
    hadoop_home = os.getenv("HADOOP_HOME") or os.getenv("hadoop.home.dir")
    if not hadoop_home:
        return False

    return (Path(hadoop_home) / "bin" / "winutils.exe").exists()


def create_spark_session(app_name: str = "03-io") -> SparkSession:
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
    os.environ["PYTHONHASHSEED"] = "0"

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[2]")
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

    if os.name == "nt" and not has_winutils():
        print("\nWINDOWS NOTE:")
        print("  winutils.exe is not configured.")
        print("  Spark reads can still work, but Spark writes may fail on Windows.")
        print("  This file will use Python stdlib writes where needed.")

    return spark


def create_sales_df(spark: SparkSession, n_rows: int = 20_000) -> DataFrame:
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

    print("\nGenerated sales DataFrame")
    df.printSchema()
    print(f"Rows: {df.count():,}")

    return df


def write_sample_csv_with_python(path: Path, n_rows: int = 20_000) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    models = ["Camry", "Corolla", "RAV4", "Highlander", "Tacoma",
              "Tundra", "Prius", "Sienna", "4Runner", "Venza"]
    regions = ["North", "South", "East", "West", "Central"]

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "sale_id", "date", "region", "model",
            "units", "unit_price", "revenue", "salesperson"
        ])

        for i in range(1, n_rows + 1):
            sale_id = f"SALE-{i:07d}"
            date = f"2024-{((i % 12) + 1):02d}-{((i % 28) + 1):02d}"
            region = regions[i % len(regions)]
            model = models[i % len(models)]
            units = (i % 5) + 1
            unit_price = float(15000 + (i % 40000))
            revenue = units * unit_price
            salesperson = f"SP-{i % 50:03d}"
            writer.writerow([
                sale_id, date, region, model,
                units, unit_price, revenue, salesperson
            ])


def read_csv_with_schema(spark: SparkSession, path: str) -> DataFrame:
    print("\nA) CSV with inferSchema=True")

    t0 = time.perf_counter()
    df_infer = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(path)
    )
    print(f"Infer schema count: {df_infer.count():,}")
    print(f"Infer schema time: {(time.perf_counter() - t0) * 1000:.2f} ms")
    df_infer.printSchema()

    print("\nB) CSV with explicit schema")

    schema = StructType([
        StructField("sale_id", StringType(), True),
        StructField("date", DateType(), True),
        StructField("region", StringType(), True),
        StructField("model", StringType(), True),
        StructField("units", LongType(), True),
        StructField("unit_price", DoubleType(), True),
        StructField("revenue", DoubleType(), True),
        StructField("salesperson", StringType(), True),
    ])

    t1 = time.perf_counter()
    df_schema = (
        spark.read
        .option("header", True)
        .schema(schema)
        .csv(path)
    )
    print(f"Explicit schema count: {df_schema.count():,}")
    print(f"Explicit schema time: {(time.perf_counter() - t1) * 1000:.2f} ms")
    df_schema.printSchema()

    print("\nWHY explicit schema:")
    print("  inferSchema guesses types from data; explicit schema is faster and safer in production.")

    return df_schema


def write_sample_json_with_python(path: Path, n_rows: int = 1_000) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        for i in range(1, n_rows + 1):
            record = {
                "sale_id": f"SALE-{i:07d}",
                "customer": {
                    "name": f"Customer-{i:04d}",
                    "region": "North" if i % 2 == 0 else "South",
                },
                "items": [
                    {"item_name": "engine", "qty": 1},
                    {"item_name": "wheel", "qty": 4},
                ],
            }
            f.write(json.dumps(record) + "\n")


def read_json_nested(spark: SparkSession, path: str) -> DataFrame:
    df = spark.read.json(path)

    print("\nNested JSON schema:")
    df.printSchema()

    print("\nDot notation for nested fields:")
    df.select("sale_id", "customer.name", "customer.region").show(5, truncate=False)

    exploded = df.select("sale_id", F.explode("items").alias("item"))

    print("\nAfter explode:")
    exploded.printSchema()
    exploded.show(5, truncate=False)

    print("\nArray indexing:")
    df.select("sale_id", F.col("items")[0].alias("first_item")).show(5, truncate=False)

    return df


def demonstrate_partitioning_concept(df: DataFrame) -> None:
    print("\n=== PARTITIONING CONCEPT ===")

    print("In production, you would write:")
    print('  df.write.mode("overwrite").partitionBy("region").parquet(path)')

    print("\nWHY partitionBy:")
    print("  A query like WHERE region = 'North' can skip other folders.")
    print("  That is called partition pruning.")

    print("\nSimulated partition counts:")
    (
        df.groupBy("region")
        .count()
        .orderBy("region")
        .show(truncate=False)
    )


def demonstrate_predicate_pushdown_concept(df: DataFrame) -> None:
    print("\n=== PREDICATE PUSHDOWN CONCEPT ===")

    filtered = df.filter(F.col("region") == "North")

    print("Filtered count:")
    print(filtered.count())

    print("\nPhysical plan:")
    filtered.explain(True)

    print("\nWHY predicate pushdown:")
    print("  Spark tries to push filters into the file scan.")
    print("  With Parquet + partitions, Spark can avoid reading irrelevant data.")


def compare_format_performance_concept(csv_path: Path, json_path: Path) -> None:
    print("\n=== FORMAT PERFORMANCE CONCEPT ===")

    csv_mb = csv_path.stat().st_size / (1024 * 1024)
    json_mb = json_path.stat().st_size / (1024 * 1024)

    print(f"{'format':<15} {'size_mb':>10} {'notes'}")
    print(f"{'csv':<15} {csv_mb:>10.2f} row-based, human-readable, slower schema handling")
    print(f"{'json':<15} {json_mb:>10.2f} flexible nested data, larger files")
    print(f"{'parquet':<15} {'n/a':>10} columnar, compressed, best for analytics")

    print("\nWHY Parquet usually wins:")
    print("  - column pruning")
    print("  - predicate pushdown")
    print("  - compression")
    print("  - efficient typed storage")


def main() -> None:
    spark = None

    try:
        spark = create_spark_session("03-io")
        out = get_output_dir()
        out.mkdir(parents=True, exist_ok=True)

        df = create_sales_df(spark, n_rows=20_000)

        csv_file = out / "sales.csv"
        json_file = out / "sales_nested.json"

        print("\n=== WRITE SAMPLE CSV WITH PYTHON ===")
        write_sample_csv_with_python(csv_file, n_rows=20_000)
        print(f"Wrote CSV: {csv_file}")

        print("\n=== CSV SCHEMA INFERENCE vs EXPLICIT ===")
        df_csv = read_csv_with_schema(spark, str(csv_file))

        print("\n=== WRITE SAMPLE NESTED JSON WITH PYTHON ===")
        write_sample_json_with_python(json_file, n_rows=1_000)
        print(f"Wrote JSON: {json_file}")

        print("\n=== NESTED JSON ===")
        read_json_nested(spark, str(json_file))

        demonstrate_partitioning_concept(df_csv)
        demonstrate_predicate_pushdown_concept(df_csv)
        compare_format_performance_concept(csv_file, json_file)

        if os.name == "nt" and not has_winutils():
            print("\nNOTE:")
            print("  Spark write demos were skipped because winutils.exe is not configured.")
            print("  To enable Spark CSV/JSON/Parquet writes on Windows, install winutils and set HADOOP_HOME.")

    finally:
        if spark:
            spark.stop()


if __name__ == "__main__":
    main()