# Lab 07 teaching goal:
# Show foundational RDD mechanics while contrasting them with DataFrame-style
# structured processing that is usually preferred in production ETL.

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg

# SparkSession is the runtime entry point for DataFrame and Spark SQL work.
spark = SparkSession.builder.appName("lab_07_rdds_vs_dataframes").getOrCreate()
# Create a tiny in-memory dataset so behavior is deterministic and easy to inspect.
df = spark.createDataFrame([("Data Engineering", 120000), ("Data Engineering", 130000), ("Analytics", 98000)], ["department", "salary"])
rdd = df.rdd
print("RDD tiny collect:", rdd.map(lambda r: (r["department"], r["salary"])).filter(lambda x: x[1] > 100000).collect())
# DataFrames are preferred for structured ETL and optimizer support.
df.groupBy("department").agg(avg("salary").alias("avg_salary")).show()
# Always close the SparkSession to release local resources cleanly.
spark.stop()
