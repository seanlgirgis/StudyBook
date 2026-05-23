# Lab 10 teaching goal:
# Convert syntax knowledge into production support checks: row counts, schema,
# nulls, duplicates, joins, and aggregation sanity validation.

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count as fcount

# SparkSession is the runtime entry point for DataFrame and Spark SQL work.
spark = SparkSession.builder.appName("lab_10_production_support_checks").getOrCreate()
input_# Create a tiny in-memory dataset so behavior is deterministic and easy to inspect.
df = spark.createDataFrame([(1, "A", 100), (2, "B", 200), (2, "B", 200), (3, None, 150)], ["id", "category", "amount"])
print("Input row count:", input_df.count())
input_# printSchema() confirms inferred/declared data types before transformations.
df.printSchema()
print("Null category rows:", input_df.filter(col("category").isNull()).count())
print("Duplicate key groups:", input_df.groupBy("id").agg(fcount("*").alias("c")).filter(col("c") > 1).count())
lookup_# Create a tiny in-memory dataset so behavior is deterministic and easy to inspect.
df = spark.createDataFrame([(1, "x"), (2, "y")], ["id", "tag"])
joined = input_df.join(lookup_df, on="id", how="left")
print("Join output row count:", joined.count())
out = joined.groupBy("category").sum("amount")
out.show()
print("Output row count:", out.count())
# Safe rerun discussion: validate idempotency and append vs overwrite risk before production writes.
# Always close the SparkSession to release local resources cleanly.
spark.stop()
