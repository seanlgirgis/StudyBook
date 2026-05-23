# Course 11 PySpark Lab Sequence

Docker is the canonical runner for Course 11 labs.
Reference: `HOW_TO_RUN_DOCKER_LABS.md`

Status:
- Lab 01: PASS (Docker)
- Lab 02: PASS (Docker)
- Lab 03: PASS (Docker)
- Lab 04: PASS (Docker)
- Lab 05: PASS (Docker)
- Lab 06: PASS (Docker)
- Lab 07: PASS (Docker)
- Lab 08: PASS (Docker)
- Lab 09: PASS (Docker)
- Lab 10: PASS (Docker)

Docker shell workflow:

```powershell
cd D:\Workarea\StudyBook
.\env_setter.ps1
docker exec -it sharkforce-pyspark-lab bash
cd /workspace/studybook/tutorials/DataCamp/Associate_Data_Engineer_Databricks/course_11_intro_pyspark
```

Run order and concepts:
1. `01_sparksession_dataframe_basics` - SparkSession, createDataFrame, schema/show/select/count
2. `02_reading_data_and_schemas` - local CSV generation, inferSchema vs manual StructType
3. `03_missing_data_and_columns` - null handling and column operations
4. `04_filtering_and_aggregations` - filtering + groupBy/agg
5. `05_joins_and_unions` - inner/left joins, union, schema checks
6. `06_udfs_and_pandas_udfs` - built-ins first, regular UDF, optional pandas UDF
7. `07_rdds_vs_dataframes` - RDD basics and DataFrame comparison
8. `08_spark_sql_temp_views` - temp views and spark.sql DataFrame flow
9. `09_scale_explain_cache_broadcast` - explain/cache/unpersist/broadcast concepts
10. `10_production_support_checks` - production-oriented checks and guardrails
