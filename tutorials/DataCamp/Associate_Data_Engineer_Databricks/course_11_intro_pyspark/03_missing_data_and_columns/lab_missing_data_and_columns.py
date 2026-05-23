# Lab 03 teaching goal:
# Practice null handling and column transformations while watching row-count
# impact, because cleanup choices directly change downstream metrics.

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# SparkSession is the runtime entry point for DataFrame and Spark SQL work.
spark = SparkSession.builder.appName("lab_03_missing_data_and_columns").getOrCreate()
rows = [(1, "Ava", 120000, None), (2, "Ben", None, "US"), (3, "Cory", 131000, "US"), (4, None, 105000, "IN")]
# Create a tiny in-memory dataset so behavior is deterministic and easy to inspect.
df = spark.createDataFrame(rows, ["employee_id", "name", "salary", "country"])
print("Original count:", df.count())
print("na.drop count:", df.na.drop().count())
print("na.drop subset count:", df.na.drop(subset=["name", "salary"]).count())
fixed = df.na.fill({"name": "UNKNOWN", "salary": 0})
fixed = fixed.withColumn("salary_k", col("salary") / 1000)
fixed = fixed.withColumnRenamed("country", "country_code")
fixed = fixed.drop("country_code")
fixed.show()
# Production warning: broad null handling can silently remove meaningful data.
# Always close the SparkSession to release local resources cleanly.
spark.stop()
