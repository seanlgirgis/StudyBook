# 01 - What Is Airflow?

Back: [00_START_HERE.md](./00_START_HERE.md)

Think of Apache Airflow as a workflow planner and traffic controller.

- You define work as a DAG (Directed Acyclic Graph).
- A DAG is a graph of tasks with order rules.
- Airflow decides when each task should run.
- Airflow tracks success/failure and retries.

Simple example in words:
1. Extract data
2. Transform data
3. Load data

Airflow stores that pipeline as a DAG and runs it on schedule or on demand.

## Core parts you will hear about

- Webserver: Airflow UI and API.
- Scheduler: decides what should run now.
- Worker: executes tasks.
- Triggerer: handles deferred/waiting tasks efficiently.
- Metadata DB: stores DAG runs, task states, users, variables.

In this tutorial we run all of that in Docker containers.