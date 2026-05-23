# Lab 09 teaching goal:
# Introduce scale-thinking tools (explain/cache/unpersist/broadcast) and show
# when they help reduce repeated work and shuffle costs.

from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast

# SparkSession is the runtime entry point for DataFrame and Spark SQL work.
spark = SparkSession.builder.appName("lab_09_scale_explain_cache_broadcast").getOrCreate()
large_# Create a tiny in-memory dataset so behavior is deterministic and easy to inspect.
df = spark.createDataFrame([(1, "A", 120), (2, "B", 90), (3, "C", 150)], ["id", "key", "value"])
small_lookup_# Create a tiny in-memory dataset so behavior is deterministic and easy to inspect.
df = spark.createDataFrame([("A", "Alpha"), ("B", "Beta")], ["key", "label"])
large_df.explain()
filtered = large_df.filter(large_df.value > 80)
filtered.cache()
print("Materialize cache:", filtered.count())
filtered.groupBy("key").count().show()
filtered.unpersist()
large_df.join(broadcast(small_lookup_df), on="key", how="left").show()
# Repeated actions can trigger repeated jobs; joins/groupBy can trigger shuffle.
# Always close the SparkSession to release local resources cleanly.
spark.stop()
