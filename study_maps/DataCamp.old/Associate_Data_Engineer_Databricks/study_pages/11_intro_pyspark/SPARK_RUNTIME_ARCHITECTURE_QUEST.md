# Spark Runtime Architecture Quest

Purpose:
Explain the production architecture around a PySpark job. This answers Sean's question: "I wrote PySpark code. How does Spark know what cluster or machines to use, and what roles do Hadoop, YARN, Kubernetes, Databricks, EMR, Glue, and Airflow play?"

# 1. The Core Idea

A PySpark job is not just Python code. It sits inside a production runtime architecture.

PySpark code defines the data-processing work.

The submission layer starts the job.

Spark runtime creates the driver and executors.

The cluster/resource manager allocates machines, CPU, and memory.

Storage holds the data.

The catalog/metadata layer describes tables, schemas, and locations.

The orchestrator coordinates job order, dependencies, retries, and alerts.

Punch line:
Code says what to do. The platform decides where and with what resources it runs.

# 2. Architecture Layers

## Layer 1 - PySpark Application Code

Role:
Defines the ETL/data logic.

Examples:
- read CSV, JSON, Parquet, Delta, tables
- select/filter/withColumn
- joins/unions
- aggregations
- validations
- writes

Safe sentence:
My PySpark code defines the data work. It usually should not hard-code the physical machines.

## Layer 2 - Submission / Job Layer

Role:
Starts the Spark application and passes runtime configuration.

Examples:
- spark-submit
- Airflow Spark task
- Databricks Job
- EMR Step
- AWS Glue Job
- Kubernetes SparkApplication or job spec

What it controls:
- app name
- parameters
- deploy mode
- cluster target
- executor count
- executor memory
- executor cores
- packages/configs

Example:

```bash
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --num-executors 8 \
  --executor-memory 4G \
  --executor-cores 2 \
  daily_salary_etl.py
```

## Layer 3 - Spark Runtime

Role:
Runs the Spark application.

Main parts:
- SparkSession / SparkContext
- driver
- executors
- tasks
- partitions
- Spark SQL / Catalyst planning
- stages / shuffle

Driver:
Coordinates the application, builds the plan, schedules tasks, tracks progress.

Executors:
Run tasks on partitions and report status/failures back to the driver.

## Layer 4 - Cluster / Resource Manager

Role:
Allocates compute resources.

Examples:
- YARN
- Kubernetes
- Spark Standalone
- Databricks cluster manager
- EMR managed cluster/YARN
- AWS Glue managed Spark runtime

Important:
Spark does distributed data processing. The cluster/resource manager provides the resources Spark uses.

## Layer 5 - Storage Layer

Role:
Stores input and output data.

Examples:
- HDFS
- S3
- ADLS
- GCS
- Parquet
- Delta Lake
- databases via JDBC
- Kafka / streaming sources

Safe sentence:
Spark is compute; storage is where data lives.

## Layer 6 - Catalog / Metadata Layer

Role:
Tracks table names, schemas, locations, and permissions.

Examples:
- Hive Metastore
- AWS Glue Data Catalog
- Databricks Unity Catalog

Safe sentence:
The catalog tells Spark what a table means and where it lives.

## Layer 7 - Orchestration Layer

Role:
Coordinates workflows across jobs.

Examples:
- Airflow
- Databricks Workflows / Jobs
- Control-M
- Autosys
- AWS Step Functions
- Oozie, older Hadoop world

What it controls:
- schedules
- dependencies
- retries
- parameters
- alerts
- operational history

Safe sentence:
Airflow or another scheduler may start and monitor a PySpark job, but Spark does the distributed execution inside the job.

# 3. Platform Families

## Hadoop / YARN Spark

Classic enterprise big-data pattern.

Spark job submitted with spark-submit.
YARN allocates cluster resources.
Data often lives in HDFS, Hive tables, or object storage.
Common in older enterprise Hadoop environments.

## Spark on Kubernetes

Spark driver and executors run as Kubernetes pods.
Kubernetes schedules containers and resources.
Common in cloud-native/containerized environments.

## Spark Standalone

Spark's built-in cluster manager.
Useful for simpler Spark clusters, learning, or controlled deployments.

## Databricks

Managed Spark/lakehouse platform.
Common pieces:
- notebooks
- jobs/workflows
- job clusters
- all-purpose clusters
- Delta Lake
- Unity Catalog
- DBFS/cloud storage integrations

Safe sentence:
In Databricks, the platform hides much of spark-submit and cluster-management detail behind jobs, clusters, workflows, and notebooks.

## Amazon EMR

Managed Hadoop/Spark cluster service on AWS.
More infrastructure control than Glue.
Common for teams that want Spark/Hadoop clusters integrated with S3 and AWS.

## AWS Glue

Managed/serverless-style Spark ETL service.
Good for ETL jobs integrated with S3 and Glue Data Catalog.
Less cluster-management work for the developer.

# 4. Common Architecture Flows

## Flow A - Hadoop/YARN

Airflow or scheduler
-> spark-submit
-> YARN
-> Spark driver/executors
-> HDFS/S3/Hive
-> output table/file

## Flow B - Databricks

Databricks Workflow/Job
-> job cluster or existing cluster
-> Spark driver/executors
-> Delta/S3/ADLS
-> Unity Catalog/metastore
-> output table

## Flow C - AWS Glue

Glue Job
-> managed Spark runtime
-> Spark driver/executors abstracted by Glue
-> S3
-> Glue Data Catalog
-> output dataset/table

## Flow D - Kubernetes Spark

Job spec / operator / spark-submit
-> Kubernetes API
-> driver pod
-> executor pods
-> object storage or database
-> output dataset

# 5. Practical Classification

Spark:
Distributed compute engine.

PySpark:
Python API for Spark.

spark-submit:
Launches a Spark application.

Airflow:
Workflow orchestrator.

YARN / Kubernetes / Standalone:
Cluster/resource managers.

Hadoop:
Older big-data ecosystem, often HDFS + YARN + Hive.

Databricks:
Managed Spark/lakehouse platform.

EMR:
Managed Hadoop/Spark cluster platform on AWS.

Glue:
Managed ETL service that can run Spark jobs.

Delta Lake:
Reliable lakehouse table/storage layer.

Catalog:
Metadata layer for tables, schemas, locations, and permissions.

# 6. Interview-Safe Answer

A PySpark job is not just Python code. In production, the code defines the data-processing logic, but the job usually runs inside a larger architecture.

The job may be submitted through spark-submit, Airflow, Databricks Jobs, EMR Steps, Glue Jobs, or Kubernetes. Spark then runs the application using a driver and executors. A cluster manager or managed platform allocates resources like machines, CPU, and memory. The data usually lives in storage such as HDFS, S3, ADLS, Parquet, or Delta tables. A catalog or metastore tracks table metadata. An orchestrator coordinates job order, dependencies, retries, and alerts.

Punch line:
PySpark defines the data work. The submission layer starts it. Spark runs it. The cluster manager resources it. Storage holds the data. The catalog describes the data. The orchestrator coordinates the pipeline.

# 7. Common Confusions

Confusion:
"Does my code tell Spark which machines to use?"

Answer:
Usually no. The submission layer/platform/cluster manager handles that.

Confusion:
"Is Airflow running Spark?"

Answer:
Airflow can start and monitor Spark jobs, but Spark runs the distributed data work.

Confusion:
"Is Hadoop the same as Spark?"

Answer:
No. Hadoop is an ecosystem. Spark can run in Hadoop/YARN environments and read from HDFS/Hive, but Spark is the compute engine.

Confusion:
"Is Databricks the same as Spark?"

Answer:
No. Databricks is a managed lakehouse platform built around Spark and related tools.

Confusion:
"Is Glue the same as EMR?"

Answer:
No. EMR gives managed Spark/Hadoop clusters with more infrastructure control. Glue is a more managed ETL service.

# 8. Source Notes

- Apache Spark cluster overview: SparkContext connects to cluster managers such as Standalone, YARN, or Kubernetes, which allocate resources. Executors run computations and store data for the application.
- Apache Spark submitting applications: spark-submit is the standard way to launch Spark applications and pass configuration.
- Databricks Jobs / Workflows: Databricks Jobs/Workflows orchestrate and schedule data processing tasks.
- Amazon EMR: EMR is a managed platform for Hadoop/Spark-style clusters.
- AWS Glue: Glue is a managed/serverless-style ETL service that can run Spark jobs.
