# Airflow Speedy Story and Interview Guide

A narrative from beginner to Data Engineering interview-ready, with 32
Q&A pairs linked to runnable nuggets.

---

## Part 1: The Story — From Cron Jobs to Production Orchestration

### Scene 1: The Cron Job Era

You join a data team.  The pipeline is five bash scripts triggered by
`crontab`.  It works — until one script fails silently at 2am, the next
one runs on stale data, and nobody notices until the CEO's dashboard
shows wrong numbers at 9am Monday.

You inherit the on-call rotation.  By Tuesday you've decided: there must
be a better way.

### Scene 2: Your First Airflow DAG

You write your first Airflow DAG.  It's just three tasks — extract,
transform, load — but something is different:

- The UI shows exactly which task failed and why
- The logs are right there, per task
- You can clear the failed task and rerun just that step
- Tomorrow's run will automatically happen at midnight

You show it to your manager.  She says: "Can we add a data quality check
before the transform?"  You add a fourth task in ten minutes.  This is
the moment Airflow clicks.

### Scene 3: The execution_date Trap

Your new daily DAG has `start_date = yesterday` but it's not running.
You wait.  Nothing.  You google for an hour before finding the answer:

**Airflow runs AFTER the interval ends.**

If `start_date=2024-01-01` and `schedule=@daily`, the first run fires
on 2024-01-02 — because the 2024-01-01 interval doesn't end until
midnight on 2024-01-02.  `execution_date` is the START of the interval
being processed, not when the run fires.

This is the single most confusing thing in Airflow.  You'll explain it
in every interview.

### Scene 4: The Catchup Disaster

You deploy a new DAG with `start_date = six months ago` and
`catchup=True`.  Within seconds the scheduler creates 180 DAG runs.
All your workers are swamped.  The production pipeline is delayed.

Lesson learned: **always use `catchup=False`**.  Backfill explicitly
with the CLI when you actually need historical data.

### Scene 5: The XCom Anti-Pattern

You inherit a DAG where a task XComs a 500MB DataFrame.  The scheduler
starts throwing memory errors.  The metadata database disk fills up.

You rewrite it: write the DataFrame to S3, XCom the S3 path (a 60-byte
string).  Immediately the issues disappear.

Rule: **XCom is for small values (< 48KB).  Write large data to storage.
Pass the path via XCom.**

### Scene 6: Sensor Slot Starvation

You deploy 20 DAGs each with a FileSensor in `poke` mode.  The sensors
run every 5 minutes and your worker pool has 16 slots.  All 16 slots
are occupied by waiting sensors.  No processing tasks can run.
Everything is stuck.

Fix: change all sensors to `mode="reschedule"`.  Slots are released
between checks.  Processing tasks can run again.

### Scene 7: Idempotency in Production

A pipeline fails halfway through the load step.  You clear the task and
rerun.  But the load step inserted 5000 rows before failing — now
you've loaded 10,000 rows, half of them duplicates.

Fix: implement the **DELETE + INSERT** pattern.
```sql
DELETE FROM target WHERE partition_date = '{{ ds }}';
INSERT INTO target SELECT * FROM staging WHERE partition_date = '{{ ds }}';
```
Now rerunning always produces exactly the right result.

### Scene 8: Interview Day

You walk into the Airflow interview at a senior DE level.  They ask:
*"What is execution_date and why is it called that?"*

You smile.  You have a story for this.

---

## Part 2: 32 Interview Q&A

---

### Scheduling and Basics

**Q01: What is execution_date in Airflow?**
`execution_date` (also called `data_interval_start` in Airflow 2.2+) is the
START of the data interval a DAG run processes.  For a daily DAG,
`execution_date=2024-01-01` means the run processes January 1 data.
The run actually fires on January 2 after the interval ends.
Use `{{ ds }}` in templates to get it as `YYYY-MM-DD`.
*See nugget: 02_dependencies_and_scheduling/02_scheduling_and_catchup.py*

---

**Q02: What is the difference between execution_date and the actual run time?**
`execution_date` is the start of the data interval (past-pointing).
The actual run time is when the scheduler creates the task instance —
which is at or after `data_interval_end`.
For `@daily` with `start_date=2024-01-01`:
- `execution_date = 2024-01-01`
- `data_interval_end = 2024-01-02`
- Actual run time: 2024-01-02 00:00 UTC
*See nugget: 02_dependencies_and_scheduling/02_scheduling_and_catchup.py*

---

**Q03: I deployed a DAG with start_date yesterday and catchup=False. Why hasn't it run?**
With `catchup=False`, Airflow only creates the most recent interval run.
For `@daily`, that run fires at midnight after the current day's interval
ends — so if you deploy mid-day, the first run happens the following midnight.
Check: is the DAG unpaused in the UI?  Is the scheduler running?
*See nugget: 02_dependencies_and_scheduling/02_scheduling_and_catchup.py*

---

**Q04: What does catchup=True do and when is it dangerous?**
`catchup=True` instructs the scheduler to create runs for all intervals
between `start_date` and now.  Deploying with a 6-month-old `start_date`
creates ~180 runs instantly, potentially overwhelming workers.
Use `catchup=False` in production and backfill explicitly:
```
airflow dags backfill my_dag --start-date 2024-01-01 --end-date 2024-03-31
```
*See nugget: 02_dependencies_and_scheduling/02_scheduling_and_catchup.py*

---

**Q05: What is a backfill and how do you run one?**
A backfill creates DAG runs for a specific historical date range.
```bash
airflow dags backfill my_dag \
  --start-date 2024-01-01 \
  --end-date   2024-01-31 \
  --dry-run    # preview without running
```
Use `--dry-run` first.  Backfill runs historical intervals in parallel
up to `max_active_runs`.
*See nugget: 05_operations_and_observability/01_dag_run_lifecycle.py*

---

### XCom

**Q06: What is XCom and what are its limitations?**
XCom (Cross-Communication) lets tasks share small values via the metadata
database.  The `@task` return value is automatically pushed; passing it
as an argument to another `@task` automatically pulls it.
**Limitation**: ~48KB per value.  Never XCom DataFrames, arrays, or
binary files — use object storage (S3/GCS) and XCom the path instead.
*See nugget: 01_dag_basics/04_xcom_fundamentals.py*

---

**Q07: How do you pass a large DataFrame between tasks?**
Write it to S3/GCS in the first task; XCom the path string.
```python
@task
def extract() -> str:
    df = fetch_data()
    path = "s3://my-bucket/tmp/run123/data.parquet"
    df.to_parquet(path)
    return path   # XComs the path string (~50 bytes)

@task
def transform(path: str) -> str:
    df = pd.read_parquet(path)
    ...
```
*See nugget: 01_dag_basics/04_xcom_fundamentals.py*

---

**Q08: What is the difference between TaskFlow XCom and classic XCom?**
TaskFlow: return value auto-pushed; passing the return as arg auto-pulls.
Classic: explicit `ti.xcom_push(key=..., value=...)` and
`ti.xcom_pull(task_ids=..., key=...)`.
Both store values in the same metadatabase table.
*See nuggets: 01_dag_basics/01_taskflow_api.py and 02_python_bash_operators.py*

---

### Sensors

**Q09: What is a sensor in Airflow?**
A sensor is a special operator that polls a condition and blocks until
it is met (or times out).  Used to wait for files, external DAGs,
APIs, or database rows to be ready before proceeding.
*See nugget: 02_dependencies_and_scheduling/03_sensors.py*

---

**Q10: What is the difference between poke mode and reschedule mode?**
`poke`: sensor holds a worker slot the entire time it waits.
`reschedule`: sensor releases the slot between checks; rescheduled
at next `poke_interval`.
**Rule**: always use `reschedule` for waits longer than ~5 minutes
to avoid slot starvation.
*See nugget: 02_dependencies_and_scheduling/03_sensors.py*

---

**Q11: What is sensor slot starvation?**
When many sensors in `poke` mode occupy all worker slots simultaneously,
no processing tasks can get a slot — the pipeline freezes.
Fix: use `mode="reschedule"` on all long-running sensors.
*See nugget: 06_interview_drills/01_interview_drills.py (Q10)*

---

**Q12: What does soft_fail=True do on a sensor?**
Instead of raising `AirflowSensorTimeout` (task `FAILED`), the sensor
marks itself as `SKIPPED`.  Downstream tasks with `trigger_rule=NONE_FAILED`
will still proceed.  Use when the sensor condition is optional.
*See nugget: 02_dependencies_and_scheduling/03_sensors.py*

---

### Retries and Error Handling

**Q13: How do you configure retries in Airflow?**
Set in `default_args` for all tasks, or override per task:
```python
default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=30),
}
```
Per-task override: `@task(retries=5, retry_delay=timedelta(seconds=30))`
*See nugget: 03_retries_slas_and_alerting/01_retries_and_backoff.py*

---

**Q14: What is exponential backoff and why is it better than fixed retry?**
Exponential backoff doubles the delay on each retry:
`delay = base_delay * 2^(attempt - 1)`.
Better than fixed retry because: (1) it gives transient issues time to
resolve, (2) it reduces load on failing downstream systems, (3) it
spreads retries further apart as failure count grows.
*See nugget: 03_retries_slas_and_alerting/01_retries_and_backoff.py*

---

**Q15: How do you send a Slack alert when a task fails?**
Use `on_failure_callback` in `default_args`:
```python
def notify_slack(context):
    send_slack_message(
        channel="#data-alerts",
        text=f"Task failed: {context['dag'].dag_id}.{context['task'].task_id}"
    )

default_args = {"on_failure_callback": notify_slack}
```
`context` contains: `dag`, `task`, `task_instance`, `run_id`,
`execution_date`, `exception`, `log_url`.
*See nugget: 03_retries_slas_and_alerting/01_retries_and_backoff.py*

---

**Q16: What is execution_timeout vs SLA?**
`execution_timeout`: hard kill — task is stopped if it exceeds the
duration.  Measured from task start time.
`SLA`: soft alert — `sla_miss_callback` fires but task keeps running.
Measured from `execution_date`.
*See nugget: 03_retries_slas_and_alerting/02_sla_and_timeouts.py*

---

### Idempotency and Data Patterns

**Q17: What does idempotent mean in the context of Airflow?**
An idempotent task produces the same result every time it runs for the
same input.  Critical for safe reruns.
Pattern: filter by `{{ ds }}`, use DELETE+INSERT (not append), write
to date-partitioned paths.
*See nugget: 04_data_pipeline_patterns/01_etl_pattern.py*

---

**Q18: How do you implement an idempotent load?**
```sql
-- DELETE existing partition, then INSERT fresh
DELETE FROM target WHERE partition_date = '{{ ds }}';
INSERT INTO target
SELECT * FROM staging WHERE partition_date = '{{ ds }}';
```
Also works for S3: overwrite the partition path on each run.
*See nugget: 04_data_pipeline_patterns/01_etl_pattern.py*

---

**Q19: How do you design an incremental pipeline with a watermark?**
Store a high-water mark (last processed timestamp) in an Airflow Variable
or a metadata table.  On each run:
1. Read watermark
2. Extract records where `updated_at > watermark`
3. Process and load
4. Update watermark to `data_interval_end`
*See nugget: 04_data_pipeline_patterns/01_etl_pattern.py*

---

### Branching and Dependencies

**Q20: How do you run tasks in parallel in Airflow?**
Simply give multiple tasks the same upstream:
```python
b = process_bronze(raw)
s = process_silver(raw)
g = process_gold(raw)
result = aggregate(b, s, g)  # waits for all three
```
In TaskFlow, multiple args from the same level run in parallel.
*See nugget: 02_dependencies_and_scheduling/01_dependency_graphs.py*

---

**Q21: What is BranchPythonOperator and when do you use it?**
It's an operator (or `@task.branch` decorator) that returns the
`task_id` (or list) of the branch to execute.  All other branches
are marked `SKIPPED`.
Use when you need to take different paths based on runtime data:
e.g., small vs large dataset processing, staging vs prod routing.
*See nugget: 04_data_pipeline_patterns/02_branching_and_shortcircuit.py*

---

**Q22: Why do you need trigger_rule=NONE_FAILED after a branch?**
Skipped branches look like non-success to the default `ALL_SUCCESS`
rule.  Without `NONE_FAILED`, the join task after the branch never runs.
`NONE_FAILED`: run if no upstream is in `FAILED` state (success or skipped is OK).
*See nugget: 04_data_pipeline_patterns/02_branching_and_shortcircuit.py*

---

**Q23: What is ShortCircuitOperator?**
Returns `bool`.  If `False`, all downstream tasks are skipped.
If `True`, pipeline proceeds normally.
Use when you want to skip the entire rest of the pipeline based on
a single condition (e.g., no new data today).
*See nugget: 04_data_pipeline_patterns/02_branching_and_shortcircuit.py*

---

**Q24: What trigger_rule would you use for a cleanup task that must always run?**
`trigger_rule=ALL_DONE` — runs after all upstreams finish regardless
of state (success, failed, or skipped).  Perfect for cleanup, notification,
and "dead-letter" tasks.
*See nuggets: 02_dependencies_and_scheduling/01_dependency_graphs.py,
07_mini_capstone/01_mini_capstone.py*

---

### Operations and Observability

**Q25: How do you rerun a failed task without rerunning the whole DAG?**
In the Airflow UI: click on the task in the Tree/Graph view, click
"Clear" (optionally with "Downstream" to clear dependent tasks too).
CLI: `airflow tasks clear dag_id --task-id task_id --execution-date DATE`
The task instance is reset to `queued` and the scheduler picks it up.
*See nugget: 05_operations_and_observability/01_dag_run_lifecycle.py*

---

**Q26: What is the difference between "Clear" and "Mark Success"?**
Clear: resets task to queued — the actual code runs again.
Mark Success: skips execution and directly sets state to `success`.
Use Clear for genuine reruns; use Mark Success only when you're certain
the task's effect has already occurred (e.g., manual SQL fix applied).
*See nugget: 05_operations_and_observability/01_dag_run_lifecycle.py*

---

**Q27: What is a Pool in Airflow?**
A named bucket of worker slots.  Tasks assigned to a pool can only run
if a slot is available.  Configured in UI: Admin > Pools or via CLI.
Use pools to:
- Limit DB connection concurrency (e.g., max 5 Postgres connections)
- Rate-limit external API calls
- Separate high/low priority workloads
*See nugget: 05_operations_and_observability/01_dag_run_lifecycle.py*

---

**Q28: How do you debug a failing task in Airflow?**
1. Click the failed task in the UI Tree/Graph view
2. Click "Log" to see the full task log
3. Check the traceback at the bottom
4. Use `airflow tasks test dag_id task_id YYYY-MM-DD` to run locally
5. Check `airflow scheduler` logs if task never starts (scheduler issue)
6. Check worker logs if task starts but crashes (executor issue)
*See nugget: 05_operations_and_observability/01_dag_run_lifecycle.py*

---

### Architecture and Design

**Q29: What is the difference between TaskFlow API and classic operators?**
TaskFlow (`@dag`, `@task`): modern, decorator-based, automatic XCom,
minimal boilerplate, Pythonic.  Introduced Airflow 2.0.
Classic (`DAG()`, `PythonOperator()`): explicit, verbose, required for
Airflow 1.x compatibility, easier to mock/test in isolation.
Both compile to the same task graph.  Use TaskFlow for new DAGs.
*See nuggets: 01_dag_basics/01_taskflow_api.py,
01_dag_basics/02_python_bash_operators.py*

---

**Q30: What executor would you use for a production DE team of 5 engineers?**
`CeleryExecutor` or `KubernetesExecutor`.
- Celery: simpler ops, predictable worker count, good for stable loads
- Kubernetes: dynamic scaling, resource isolation, good for variable loads
- LocalExecutor is fine for 1-2 engineers with low task concurrency
- SequentialExecutor: development only (runs one task at a time)
*See nugget: AIRFLOW_GLOSSARY.md (Executor)*

---

**Q31: How does Airflow handle a DAG that takes longer than its schedule interval?**
By default, the scheduler creates the next run even if the previous one
is still running (unless `max_active_runs=1`).  Set `max_active_runs=1`
to prevent this.  Also consider setting `dagrun_timeout` to fail stuck runs.
*See nugget: 02_dependencies_and_scheduling/02_scheduling_and_catchup.py*

---

**Q32: Walk me through how you would design a production ETL pipeline in Airflow.**
A model answer:

1. **Ingest** — TaskFlow `@task`, filter by `{{ ds }}`, no side-effects
2. **Quality gate** — fail fast before compute; check nulls, row counts, schema
3. **Transform** — apply business logic; return summary/aggregate rows
4. **Load** — DELETE+INSERT for idempotency; one partition per `{{ ds }}`
5. **Audit** — write run_id, rows_loaded, loaded_at to an audit table
6. **Failure handling** — `on_failure_callback` for Slack/PD alert;
   `retries=2` with exponential backoff for transient errors
7. **Scheduling** — `schedule="@daily"`, `catchup=False`, `max_active_runs=1`
8. **SLA** — set on critical path tasks; `sla_miss_callback` for early warning
9. **Testing** — `airflow tasks test` for local execution; pytest for callables

*See nugget: 04_data_pipeline_patterns/01_etl_pattern.py and
07_mini_capstone/01_mini_capstone.py*

---

## Part 3: Study Checklist

Before your interview, make sure you can:

- [ ] Explain execution_date and why it's past-pointing
- [ ] Explain why catchup=False is the safe default
- [ ] Explain the XCom size limit and the "pass the path" pattern
- [ ] Explain poke vs reschedule mode with slot starvation example
- [ ] Write an idempotent load (DELETE+INSERT pattern)
- [ ] Configure retries with exponential backoff
- [ ] Write an on_failure_callback that sends an alert
- [ ] Explain SLA vs execution_timeout
- [ ] Use BranchPythonOperator and know trigger_rule=NONE_FAILED
- [ ] Describe the executor types and when to use each
- [ ] Walk through a full ETL pipeline design end-to-end

---

## Part 4: Quick Reference Card

| Concept              | Key fact                                      | Nugget           |
|----------------------|-----------------------------------------------|------------------|
| execution_date       | Start of data interval, NOT run time         | 02-02            |
| catchup              | False = no backfill on deploy                | 02-02            |
| XCom limit           | ~48KB; pass file paths for large data        | 01-04            |
| Sensor reschedule    | Releases slot between pokes                  | 02-03            |
| Idempotency          | DELETE+INSERT by partition date              | 04-01            |
| Branching            | @task.branch returns task_id to run          | 04-02            |
| NONE_FAILED          | Required trigger_rule after branch joins     | 04-02            |
| ALL_DONE             | Cleanup tasks that must always run           | 02-01            |
| on_failure_callback  | Receives full context dict                   | 03-01            |
| execution_timeout    | Hard kill, from task start                   | 03-02            |
| SLA                  | Soft alert, from execution_date              | 03-02            |
| Pool                 | Slot bucket for concurrency control          | 05-01            |
| Clear task           | Reset to queued for rerun                    | 05-01            |
| max_active_runs=1    | Prevents overlapping runs                    | 02-02            |
