# Lab 08 teaching goal:
# Bridge SQL skills into PySpark by proving that spark.sql() returns a
# DataFrame that can continue through DataFrame APIs.

from pyspark.sql import SparkSession

# SparkSession is the runtime entry point for DataFrame and Spark SQL work.
spark = SparkSession.builder.appName("lab_08_spark_sql_temp_views").getOrCreate()
# Create a tiny in-memory dataset so behavior is deterministic and easy to inspect.
df = spark.createDataFrame([("Ava", "Data Engineering", 120000), ("Ben", "Analytics", 98000), ("Cory", "Data Engineering", 131000)], ["name", "department", "salary"])
df.createOrReplaceTempView("employees")
sql_df = spark.sql("""
SELECT department, AVG(salary) AS avg_salary, COUNT(*) AS cnt
FROM employees
WHERE salary > 90000
GROUP BY department
ORDER BY avg_salary DESC
""")
sql_df.show()
sql_df.filter(sql_df.cnt >= 1).show()
# Temp view is session-scoped.
# Always close the SparkSession to release local resources cleanly.
spark.stop()
