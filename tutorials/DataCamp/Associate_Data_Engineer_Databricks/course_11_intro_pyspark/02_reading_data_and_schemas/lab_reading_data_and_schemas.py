# Lab 02 teaching goal:
# Compare schema inference versus manual schema definition so we can control
# data types intentionally instead of guessing in production-style pipelines.

from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# SparkSession is the runtime entry point for DataFrame and Spark SQL work.
spark = SparkSession.builder.appName("lab_02_reading_data_and_schemas").getOrCreate()
lab_dir = Path(__file__).resolve().parent
data_dir = lab_dir / "data"
data_dir.mkdir(exist_ok=True)
csv_path = data_dir / "employees.csv"
csv_path.write_text("employee_id,name,department,salary,age\n1,Ava,Data Engineering,120000,34\n2,Ben,Analytics,98000,29\n3,Cory,Data Engineering,131000,41\n")

df_infer = spark.read.csv(str(csv_path), header=True, inferSchema=True)
print("Inferred schema:")
df_infer.printSchema()
schema = StructType([
    StructField("employee_id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("department", StringType(), True),
    StructField("salary", IntegerType(), True),
    StructField("age", IntegerType(), True),
])
df_manual = spark.read.csv(str(csv_path), header=True, schema=schema)
print("Manual schema:")
df_manual.printSchema()
# Always close the SparkSession to release local resources cleanly.
spark.stop()
