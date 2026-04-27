# My Spark Project

This is a standard Scala SBT project structure.

## Structure
- `build.sbt`: Project configuration.
- `src/main/scala`: Application code.
- `src/test/scala`: Unit tests.
- `data`: Sample input data.

## Prerequisites
You need **SBT** installed.
If `sbt` command is not found, verify your installation or PATH.

## Commands

### 1. Compile
```bash
sbt compile
```

### 2. Run Tests
```bash
sbt test
```

### 3. Run Pipeline
To run locally (simulating `spark-submit`):
```bash
sbt "run data/sample_transactions.csv output/risk_summary"
```
*Note: Since dependencies are marked "provided" in build.sbt, running locally with `sbt run` might require changing them to "compile" scope or using a specific runner config.*

### 4. Package for Cluster
```bash
sbt assembly
```
Then use `spark-submit` to deploy the JAR to a cluster.
