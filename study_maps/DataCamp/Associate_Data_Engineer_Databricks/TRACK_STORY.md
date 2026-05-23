# Associate Data Engineer in Databricks - Track Story

Purpose:
Explain that this track is being built as a StudyBook learning system, not just
a transcript dump. It should help Sean understand the full journey from SQL
foundations into PySpark, Spark SQL, Databricks, Lakehouse, Delta, and data
engineering readiness.

# Current Priority

Course 11 - Introduction to PySpark

Status:
Stable StudyBook learning package.

Why it matters now:
- Wipro PySpark interview readiness
- Spark/PySpark foundation
- future Databricks and data engineering readiness
- reusable PySpark field guide for future roles

Course 11 endpoints:
- study_pages/11_intro_pyspark/index.html
- study_pages/11_intro_pyspark/MOTHERLOAD_PYSPARK_FIELD_GUIDE.html
- study_pages/11_intro_pyspark/QA_01_1000ft_pyspark_opening.html
- outputs/course_11_intro_pyspark_1000ft.html
- outputs/course_11_intro_pyspark_architecture_runtime.html
- docs/COURSE_11_FINAL_STABILIZATION_AUDIT.md

# Track Learning Story

1. SQL Foundations
   Tables, rows, columns, SELECT, WHERE, GROUP BY, basic aggregation.

2. Intermediate SQL
   Filtering, aggregation, arithmetic, NULLs, query order, reusable SQL thinking.

3. PySpark Foundations
   SparkSession, DataFrames, schemas, transformations, actions, lazy execution.

4. Spark SQL Bridge
   Temporary views, spark.sql(), SQL results as DataFrames.

5. PySpark Production Thinking
   row counts, schema checks, failed stages, logs, reruns, shuffles, caching,
   broadcast joins, explain(), production support.

6. Databricks / Lakehouse Later
   Not fully built yet. Future courses should attach here.

# Current Course State

Course 01:
- Has older standalone folder:
  Course_01_Introduction_to_SQL
- Also has study_pages/01_intro_sql
- This is legacy/inconsistent and should not be repaired during Course 11 work.

Course 02:
- Has study_pages/02_intermediate_sql
- Has source_material/course_02_intermediate_sql
- Does not yet have the same beautiful endpoint treatment as Course 11.

Course 11:
- Has strong finalized package.
- Has Course 11 home, Motherload, QA Q01-Q69, snippets, mistakes, production
  checklist, two maps, summary, final review, and stabilization audit.

# Navigation Principle

Course-level homes should be the human-friendly endpoints.
Track-level pages should link to course-level homes, not scatter users directly
into random raw notes unless necessary.

# Future Track Map

Recommend a future StudyBubble map with 9 to 12 bubbles:
- Track Front Door
- SQL Foundations
- Intermediate SQL
- PySpark Foundation
- DataFrames and Schemas
- Spark SQL Bridge
- Production PySpark
- Databricks/Lakehouse Later
- Interview Readiness
- Labs Deferred

Do not create the topic JSON yet.

Course 3 - Joining Data in SQL
Status: not started / shell created
Purpose: next SQL step after Intermediate SQL, focused on joining tables


Course 4 - Data Manipulation in SQL
Status: not started / shell created
Purpose: next SQL step after joining data, focused on manipulating and shaping query results

