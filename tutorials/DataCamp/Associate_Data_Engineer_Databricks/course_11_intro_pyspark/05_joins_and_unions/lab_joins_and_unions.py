# Lab 05 teaching goal:
# Learn how join type affects row retention and why schema alignment matters
# before union operations.

from pyspark.sql import SparkSession

# SparkSession is the runtime entry point for DataFrame and Spark SQL work.
spark = SparkSession.builder.appName("lab_05_joins_and_unions").getOrCreate()
flights = spark.createDataFrame([("AA", "JFK", 100), ("UA", "SFO", 120), ("DL", "XYZ", 90)], ["carrier", "dest", "passengers"])
airports = spark.createDataFrame([("JFK", "New York"), ("SFO", "San Francisco")], ["dest", "city"])
inner_join = flights.join(airports, on="dest", how="inner")
left_join = flights.join(airports, on="dest", how="leftouter")
print("Flights:", flights.count(), "Inner:", inner_join.count(), "Left:", left_join.count())
left_join.show()
extra = spark.createDataFrame([("SW", "LAX", 80)], ["carrier", "dest", "passengers"])
print("Schema match for union:", flights.schema == extra.schema)
flights.union(extra).show()
# Always close the SparkSession to release local resources cleanly.
spark.stop()
