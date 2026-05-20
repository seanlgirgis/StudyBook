# 1000-Foot View — What PySpark Is

## Mental Model

Spark is the big distributed engine.
PySpark is the Python steering wheel.

## Spark

Spark is a distributed processing engine designed to run large data workloads across multiple machines.

## PySpark

PySpark is the Python API for Spark. It lets you describe data work in Python while Spark executes it in a distributed way.

## Driver

The driver is the control process. It plans the work and coordinates execution.

## Executors

Executors are worker processes that run tasks and process partitions of data.

## SparkSession

SparkSession is the main entry point to Spark from PySpark. You use it to read data and configure runtime behavior.

## DataFrame

A DataFrame is a distributed table-like structure with named columns and a schema.

## Transformations

Transformations describe how data should change, for example `filter`, `select`, and `groupBy`.

## Actions

Actions ask Spark to produce a result, for example `show`, `count`, or `collect`.

## Lazy Evaluation

Spark does not execute transformations immediately. It builds an execution plan and runs it when an action is called.

## Partitions

Partitions are chunks of distributed data. Spark processes partitions in parallel.

## Shuffle

Shuffle is data movement between partitions, usually needed for operations like joins and groupBy. It is powerful but often expensive.

## Tiny Conceptual Example (Non-Runnable)

```python
df = spark.read.csv("input.csv", header=True)
result = df.filter(df.status == "ACTIVE").groupBy("region").count()
result.show()
```

`show()` is an action, so it triggers execution of the prior transformation plan.

## Common Mistake

Do not think PySpark is just Pandas with different syntax.
PySpark is built for distributed execution, execution planning, and cluster behavior.
