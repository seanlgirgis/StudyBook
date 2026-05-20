# Code Snippets - PySpark Course 11

## SparkSession
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("my_spark").getOrCreate()
```

## Read files
```python
df_csv = spark.read.csv("file.csv", header=True, inferSchema=True)
df_json = spark.read.json("file.json")
df_parquet = spark.read.parquet("file.parquet")
```

## Inspect DataFrames
```python
df.printSchema()
df.show(5)
df.count()
```

## Schema
```python
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
schema = StructType([
    StructField("age", IntegerType(), True),
    StructField("income", StringType(), True)
])
df = spark.read.csv("adult_reduced_100.csv", header=False, schema=schema)
```

## Select/filter/where
```python
df.select("age", "income")
df.filter(df.age > 30)
df.where(df.income == ">50K")
```

## Sort/orderBy
```python
df.sort("age")
df.orderBy(df.age.desc())
```

## Missing data
```python
df.na.drop()
df.na.fill({"age": 0})
```

## Column operations
```python
df = df.withColumn("weekly_salary", df.income / 52)
df = df.withColumnRenamed("age", "years")
df = df.drop("department")
```

## Group/aggregate
```python
from pyspark.sql.functions import avg, sum, count
df.groupBy("education").agg(avg("age"), sum("hours_per_week"), count("*") )
```

## Joins
```python
airports = airports.withColumnRenamed("faa", "dest")
flights_with_airports = flights.join(airports, on="dest", how="leftouter")
```

## Union
```python
combined = df1.union(df2)
```

## UDFs
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

age_category_udf = udf(age_category, StringType())
result = df.withColumn("category", age_category_udf(df["age"]))
```

### UDF Decision Ladder (Built-ins First)
1. Use built-in Spark functions first.
2. Use DataFrame expressions for simple logic.
3. Use regular UDF only for genuinely custom logic.
4. Use pandas UDF for vectorized custom logic when appropriate.
5. External/JVM/platform-specific UDFs are environment-specific choices.

Built-in expression example:
```python
df = df.withColumn("10_plus", df["value"] + 10)
```

pandas UDF syntax example:
```python
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import DoubleType

@pandas_udf(DoubleType())
def add_ten_pandas(column):
    return column + 10

df = df.withColumn(
    "10_plus",
    add_ten_pandas(df["value"])
)

df.show()
```

## RDDs vs DataFrames
```python
# DataFrame -> RDD
rdd = df.rdd

# RDD map
mapped_rdd = rdd.map(lambda row: row)

# RDD filter
filtered_rdd = rdd.filter(lambda row: row["age"] > 40)

# collect tiny results only
small_result = filtered_rdd.collect()
```

## Spark SQL and Temporary Views
```python
employees_df = spark.read.csv("employees.csv", header=True, inferSchema=True)
employees_df.createOrReplaceTempView("employees")

high_earners = spark.sql("""
    SELECT name, salary
    FROM employees
    WHERE salary > 100000
""")

high_earners.show()
```

### Spark SQL output as DataFrame (describe pattern)
```python
salaries_df.createOrReplaceTempView("salaries_table")

query = """
    SELECT job_title, salary_in_usd
    FROM salaries_table
    WHERE company_location = 'CA'
"""

canada_titles = spark.sql(query)
canada_titles.describe().show()
```

## Aggregations and Summary Metrics
```python
# Spark SQL aggregation
df.createOrReplaceTempView("employees")
result_sql = spark.sql("""
    SELECT department,
           SUM(salary) AS total_salary,
           AVG(salary) AS avg_salary,
           COUNT(*) AS employee_count
    FROM employees
    GROUP BY department
""")

# DataFrame API aggregation
from pyspark.sql.functions import sum, avg, count, max, min
result_df = (
    df.groupBy("department").agg(
        sum("salary").alias("total_salary"),
        avg("salary").alias("avg_salary"),
        count("*").alias("employee_count"),
        max("salary").alias("max_salary"),
        min("salary").alias("min_salary")
    )
)

# Cast before aggregation
from pyspark.sql.functions import col
df_clean = df.withColumn("salary", col("salary").cast("double"))
```

## At Scale / Optimization
```python
# Inspect execution plan
df.explain()

# Cache reused intermediate
filtered_df = df.filter(df["company_location"] == "US")
filtered_df.cache()
filtered_df.count()
filtered_df.groupBy("job_title").avg("salary_in_usd").show()
filtered_df.unpersist()

# Persist with storage level
from pyspark import StorageLevel
df.persist(StorageLevel.MEMORY_AND_DISK)
df.unpersist()

# Broadcast join
from pyspark.sql.functions import broadcast
joined_df = large_df.join(broadcast(small_lookup_df), on="key", how="left")
```
