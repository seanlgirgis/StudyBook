# Lab 06 teaching goal:
# Reinforce the decision ladder: built-in Spark functions first, then regular
# UDFs, and pandas UDFs only when custom vectorized logic is justified.

from pyspark.sql import SparkSession
from pyspark.sql.functions import upper, udf
from pyspark.sql.types import StringType

# SparkSession is the runtime entry point for DataFrame and Spark SQL work.
spark = SparkSession.builder.appName("lab_06_udfs_and_pandas_udfs").getOrCreate()
# Create a tiny in-memory dataset so behavior is deterministic and easy to inspect.
df = spark.createDataFrame([("ava", 34), (None, 22)], ["name", "age"])
df.withColumn("name_upper", upper("name")).show()

def age_band(age):
    if age is None:
        return "UNKNOWN"
    return "SENIOR" if age >= 30 else "JUNIOR"

age_band_udf = udf(age_band, StringType())
df2 = df.withColumn("age_band", age_band_udf("age"))
df2.show()
try:
    from pyspark.sql.functions import pandas_udf
    from pyspark.sql.types import IntegerType

    @pandas_udf(IntegerType())
    def add_ten(col):
        return col + 10

    df2.withColumn("age_plus_ten", add_ten("age")).show()
except Exception as e:
    print("pandas UDF skipped (dependency/runtime unavailable):", e)
# Always close the SparkSession to release local resources cleanly.
spark.stop()
