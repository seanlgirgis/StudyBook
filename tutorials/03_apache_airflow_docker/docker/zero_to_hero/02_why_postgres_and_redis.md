# 02 - Why PostgreSQL and Redis?

Back: [00_START_HERE.md](./00_START_HERE.md)

Airflow in Docker can run in different executor modes. We use `CeleryExecutor`.

For `CeleryExecutor`, Airflow needs two supporting services:

## PostgreSQL (metadata + results)

PostgreSQL stores Airflow metadata:
- DAG run history
- task states
- users and roles
- variables and connections

Without PostgreSQL, Airflow has no durable memory of runs.

## Redis (message broker)

Redis works like a fast message queue.

- Scheduler says: "run task X"
- That task message is sent to Redis
- Workers read from Redis and execute tasks

Without Redis in Celery mode, workers do not receive queued tasks.

## Mental model

- PostgreSQL = notebook (long-term memory)
- Redis = walkie-talkie (fast instructions)
- Airflow scheduler/worker/webserver = team doing the work