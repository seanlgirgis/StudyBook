# Lab 01 teaching goal:
# Build confidence with the SparkSession entry point and the core DataFrame
# inspection actions used in almost every PySpark workflow.

from pyspark.sql import SparkSession

# SparkSession is the runtime entry point for DataFrame and Spark SQL work.
spark = SparkSession.builder.appName("lab_01_sparksession_dataframe_basics").getOrCreate()
employees = [(1,"Ava","Data Engineering",120000,34),(2,"Ben","Analytics",98000,29),(3,"Cory","Data Engineering",131000,41),(4,"Diya","Finance",105000,36)]
# Create a tiny in-memory dataset so behavior is deterministic and easy to inspect.
df = spark.createDataFrame(employees,["employee_id","name","department","salary","age"])
# printSchema() confirms inferred/declared data types before transformations.
df.printSchema()
# show() is an action: it triggers Spark execution and displays sample rows.
df.show(truncate=False)
df.select("employee_id","name","salary").show(truncate=False)
# count() is an action often used as a quick validation checkpoint.
print("Row count:", df.count())
# Always close the SparkSession to release local resources cleanly.
spark.stop()
