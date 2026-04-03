# Airflow Glossary

Plain-English definitions for every Airflow term you need for production work
and Data Engineering interviews.

---

## Core Concepts

### DAG (Directed Acyclic Graph)
A collection of tasks with defined execution order.  "Directed" means
dependencies flow in one direction; "Acyclic" means no circular dependencies.
In Airflow, a DAG is a Python file that defines the pipeline structure.
One DAG file = one pipeline.

### Task
A single unit of work inside a DAG.  Each task runs one operator.
Tasks have their own state, retries, and logs.  They're the
smallest schedulable unit.

### Operator
The type of work a task performs.  Think of an operator as the template;
a task is one instance of that template inside a DAG.
- `PythonOperator` — runs a Python function
- `BashOperator`   — runs a shell command
- `EmailOperator`  — sends an email
- `@task` decorator — TaskFlow API shortcut for PythonOperator

### Scheduler
The Airflow component that continuously parses DAG files and creates
task instances when their schedule is due.  The scheduler is NOT responsible
for running tasks — it only queues them.

### Executor
The component that actually runs task instances.  The executor type
determines how and where tasks execute:
- `LocalExecutor`       — runs tasks as subprocesses on the same machine
- `CeleryExecutor`      — distributes tasks to a Celery worker fleet
- `KubernetesExecutor`  — runs each task in its own Kubernetes pod
- `SequentialExecutor`  — runs one task at a time (development only)

### Worker
A process (or pod) that picks up queued task instances from the executor
and runs them.  In CeleryExecutor, workers are separate machines/containers.
In LocalExecutor, the scheduler itself is the worker.

### Webserver
The Flask-based UI component.  Serves the Airflow web interface at
`http://localhost:8082` (in this lab).  Also exposes the REST API at
`/api/v1/*`.

### Metadatabase
The relational database (usually PostgreSQL) that stores DAG definitions,
task instance states, XCom values, Variables, Connections, and all audit
history.  The scheduler and webserver both read from and write to this DB.

---

## Scheduling

### execution_date (data_interval_start)
The START of the data interval a DAG run processes.  For a daily DAG,
the run that fires on 2024-01-02 has `execution_date = 2024-01-01`.
It's always past-pointing.  Use `{{ ds }}` in templates.

### data_interval_end
The END of the data interval.  For a daily DAG, a run with
`execution_date=2024-01-01` has `data_interval_end=2024-01-02`.
The run actually fires at (or after) `data_interval_end`.

### schedule
The cron expression, timedelta, preset, or `None` that controls
when the scheduler creates new runs.
- `"@daily"` = `"0 0 * * *"` = midnight UTC every day
- `None`      = manual trigger only (no automatic runs)

### catchup
When `catchup=True`, deploying a DAG with a past `start_date` causes
the scheduler to create runs for all missed intervals back to `start_date`.
This can create hundreds of runs instantly.  Use `catchup=False` in
production; backfill explicitly via CLI when needed.

### backfill
CLI command to run a DAG for a specific date range.
```
airflow dags backfill my_dag --start-date 2024-01-01 --end-date 2024-01-31
```
Creates runs for every interval in the range.

### max_active_runs
Maximum number of concurrent DAG runs allowed.  Set to `1` to prevent
a slow run from being lapped by the next scheduled run.

---

## Task Lifecycle

### Task States

| State             | Meaning                                               |
|-------------------|-------------------------------------------------------|
| `queued`          | Waiting for a worker slot                             |
| `running`         | Actively executing                                    |
| `success`         | Completed without error                               |
| `failed`          | Exhausted all retries                                 |
| `skipped`         | Short-circuited or branched away from                 |
| `upstream_failed` | Upstream task failed; this task won't run             |
| `up_for_retry`    | Failed; waiting for retry delay                       |
| `up_for_reschedule` | Sensor between poke intervals                       |
| `removed`         | Task no longer exists in the DAG file                 |

### Clear (a task)
Resets a task instance back to `queued` so it re-runs.  Does not
delete logs.  The most common recovery action.
```
airflow tasks clear dag_id --task-id task_id --execution-date YYYY-MM-DD
```

### Mark success / Mark failed
Manually override a task's state without re-running it.  Use with
care — marking as success bypasses the actual execution.

---

## XCom (Cross-Communication)

### XCom
Airflow's mechanism for tasks to share small values.  Values are
stored in the metadatabase and retrieved by key.

### xcom_push / xcom_pull
The explicit API:
```python
ti.xcom_push(key="my_key", value="my_value")
val = ti.xcom_pull(task_ids="upstream_task", key="my_key")
```
With TaskFlow API, `return value` auto-pushes as `key="return_value"`,
and passing the return value as an argument auto-pulls it.

### XCom size limit
~48KB per value (varies by database VARCHAR limit).
**Never XCom a DataFrame, array, or binary file.**
Pattern: write large data to S3/GCS; XCom the path string.

---

## Sensors

### Sensor
A special operator that polls a condition and blocks (or reschedules)
until it is met or until timeout.  Examples:
- `FileSensor`          — wait for a file to appear
- `ExternalTaskSensor`  — wait for another DAG/task to complete
- `TimeDeltaSensor`     — wait a fixed duration
- `HttpSensor`          — wait for an HTTP endpoint to return 200

### poke mode
The sensor holds a worker slot and polls on a timer.  Good for
short waits (< 5 minutes).  Dangerous for long waits — slot starvation.

### reschedule mode
The sensor releases its worker slot between checks and is
rescheduled at the next `poke_interval`.  **Always use for long waits.**

### soft_fail
When `soft_fail=True`, a sensor that times out marks itself as
`SKIPPED` instead of `FAILED`.  The pipeline continues.

---

## SLA and Timeouts

### SLA (Service Level Agreement)
A `timedelta` declared on a task that says "this task should complete
within X time of `execution_date`."  If it doesn't, `sla_miss_callback`
is called — once per SLA miss.  **Does NOT stop the task.**

### execution_timeout
A hard limit on how long a task can run.  If exceeded, the task is
killed and marked `FAILED`.  Measured from **task start time**.

### dagrun_timeout
A hard limit on how long an entire DAG run can be active.  If exceeded,
the run is marked `FAILED` and all running tasks are killed.

### SLA vs execution_timeout
| Feature         | SLA                       | execution_timeout       |
|-----------------|---------------------------|-------------------------|
| Effect          | Alert callback (soft)     | Task killed (hard)      |
| Measured from   | execution_date            | Task start time         |
| Stops task?     | No                        | Yes                     |

---

## Retries

### retries
Number of times to retry a failed task before marking it `FAILED`.
Set globally in `default_args` or per task.

### retry_delay
`timedelta` to wait between retry attempts.

### retry_exponential_backoff
When `True`, the delay doubles on each retry:
`retry_delay * 2^(attempt - 1)`, capped at `max_retry_delay`.

### on_failure_callback
A Python function called when a task exhausts all retries.
Receives the full `context` dict with task, dag, exception, log_url, etc.
Use this to send Slack/PagerDuty/email alerts.

### on_retry_callback
Called on each retry attempt.

---

## Pools

### Pool
A named bucket of worker slots.  Tasks assigned to a pool can only run
if a slot is available.  Used to throttle concurrency for specific
resources (DB connections, API rate limits, etc.).

### pool_slots
How many slots a single task instance consumes from its pool.
Default: `1`.  Set higher for resource-heavy tasks.

### Slot starvation
When too many sensors in `poke` mode fill all pool slots, blocking
processing tasks from running.  Fix: use `mode=reschedule` on sensors.

---

## Branching

### BranchPythonOperator / @task.branch
Returns the `task_id` (or list of `task_id`s) of the branch(es) to run.
All other downstream branches are marked `SKIPPED`.

### ShortCircuitOperator
Returns `bool`.  If `False`, all downstream tasks are `SKIPPED`.
If `True`, pipeline continues normally.

### trigger_rule
Controls when a task runs relative to its upstream tasks.

| Rule                           | Meaning                                      |
|--------------------------------|----------------------------------------------|
| `ALL_SUCCESS` (default)        | All upstreams succeeded                      |
| `ALL_DONE`                     | All upstreams finished (any state)           |
| `NONE_FAILED`                  | No upstream failed (success or skipped OK)   |
| `NONE_FAILED_MIN_ONE_SUCCESS`  | NONE_FAILED + at least one succeeded        |
| `ONE_SUCCESS`                  | At least one upstream succeeded              |
| `ONE_FAILED`                   | At least one upstream failed                 |

Always use `NONE_FAILED` (or `NONE_FAILED_MIN_ONE_SUCCESS`) on join
tasks after a branch — without it, the join fails because skipped
branches are treated as non-success.

---

## Connections and Variables

### Connection
A named set of credentials/endpoints stored in the Airflow metadatabase
(Admin > Connections).  Tasks reference connections by `conn_id`.
Credentials are stored encrypted (Fernet key).

### Variable
A key-value store in the Airflow metadatabase (Admin > Variables).
Used for runtime configuration (batch sizes, feature flags, etc.).
```python
from airflow.models import Variable
batch_size = Variable.get("lab_airflow_batch_size", default_var="100")
```

---

## TaskFlow API

### @dag
Decorator that turns a function into a DAG factory.  Parameters
match `DAG()` constructor arguments.

### @task
Decorator that turns a function into a PythonOperator task.  Return
values are automatically pushed to XCom; arguments from upstream
`@task` functions are automatically pulled.

### @task.branch
Decorator for a function that returns a `task_id` string —
equivalent to `BranchPythonOperator`.

### @task.sensor (Airflow 2.5+)
Decorator for writing custom sensors as simple Python functions.

---

## Interview Quick-Reference

| Term                | One-sentence answer                                      |
|---------------------|----------------------------------------------------------|
| execution_date      | Start of the data interval (past-pointing)               |
| catchup=True        | Creates runs for all missed intervals since start_date   |
| XCom                | Small value exchange via metadatabase (< 48KB)           |
| reschedule mode     | Sensor releases slot between pokes (required for long waits) |
| idempotent task     | Rerunning produces the same result                       |
| trigger_rule        | When to run a task relative to upstream states           |
| pool                | Slot bucket to limit resource concurrency               |
| SLA                 | Soft alert; execution_timeout is the hard kill           |
| backfill            | CLI to re-run historical date ranges                     |
| Clear task          | Reset to queued for rerun                               |
