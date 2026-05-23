# Lab 04 teaching goal:
# Combine filtering and aggregations to create trustworthy summary metrics.
# Validate assumptions before reading group-level results.

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, sum as fsum, count, min as fmin, max as fmax

# SparkSession is the runtime entry point for DataFrame and Spark SQL work.
spark = SparkSession.builder.appName("lab_04_filtering_and_aggregations").getOrCreate()
rows = [("Data Engineering", "US", 120000), ("Data Engineering", "US", 131000), ("Analytics", "US", 98000), ("Finance", "IN", 105000)]
# Create a tiny in-memory dataset so behavior is deterministic and easy to inspect.
df = spark.createDataFrame(rows, ["department", "country", "salary"])
# printSchema() confirms inferred/declared data types before transformations.
df.printSchema()
print("Before filter:", df.count())
filtered = df.filter((df.country == "US") & (df.salary > 100000))
print("After filter:", filtered.count())
filtered.where(df.department != "Finance").show()
df.groupBy("department").agg(avg("salary").alias("avg_salary"), fsum("salary").alias("sum_salary"), count("*").alias("row_count"), fmin("salary").alias("min_salary"), fmax("salary").alias("max_salary")).show()
# Always close the SparkSession to release local resources cleanly.
spark.stop()
