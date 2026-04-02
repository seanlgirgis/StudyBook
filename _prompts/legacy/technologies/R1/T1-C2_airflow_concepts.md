SAVE AS: airflow_concepts.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

ROLE: You are a senior Data Engineer writing a reference guide for an engineer preparing
for Staff DE interviews at a financial institution. Precise, dense, no filler.

TASK: Generate airflow_concepts.md — a concept reference covering 8 core Airflow abstractions,
each in one tight paragraph, followed by a Citi narrative tie-in.

DATASET CONTEXT — do not deviate:
- Citi narrative: daily alert summary DAG (citi_alert_summary), runs at 06:00, 3 tasks

STRUCTURE — produce exactly these sections in order:

# Apache Airflow — Core Concepts

## 1. DAG
One paragraph. Cover: Python file defining a workflow as a Directed Acyclic Graph,
no cycles allowed (no task can depend on itself directly or transitively), scheduler reads dags/ folder,
catchup=False vs backfill behavior, tags for organization.
End with: "citi_alert_summary is a DAG with 3 tasks, scheduled daily at 06:00, catchup=False."

## 2. Task
One paragraph. Cover: atomic unit of work in a DAG, each task is an operator instance with
a unique task_id, tasks have states (queued, running, success, failed, skipped, upstream_failed),
task retries, task_id must be unique within a DAG.
End with: "extract_alerts, transform_summary, load_report — three tasks, each with its own log, state, and retry config."

## 3. Operator
One paragraph. Cover: template for a task, PythonOperator executes a callable, BashOperator runs shell,
PostgresOperator runs SQL, HttpSensor waits for HTTP endpoint, TaskFlow API (@task decorator) wraps
functions as PythonOperator automatically with XCom return.
End with: "The citi_alert_summary DAG uses @task (TaskFlow) — cleaner than PythonOperator for Python-native pipelines."

## 4. Scheduler
One paragraph. Cover: process that reads DAG files, evaluates schedule intervals, creates DagRuns
at the right time, assigns TaskInstances to the executor, heartbeat interval (default 5s),
scheduler is NOT the executor — it queues work.
End with: "After docker cp, you wait 30s for the scheduler's next scan cycle to pick up the new DAG file."

## 5. Executor
One paragraph. Cover: component that runs tasks, LocalExecutor runs tasks as subprocesses on
the same machine (good for dev, single machine), CeleryExecutor distributes across a worker pool,
KubernetesExecutor spins a pod per task, executor is configured in airflow.cfg.
End with: "The learning stack uses LocalExecutor — sufficient for single-machine development; Citi production uses CeleryExecutor or KubernetsExecutor."

## 6. XCom
One paragraph. Cover: cross-communication between tasks, tasks push values to XCom store (Postgres),
downstream tasks pull by key + task_id, TaskFlow passes XCom implicitly via return values,
XCom is not for large data (limited by DB row size) — use shared storage for DataFrames.
End with: "transform_summary receives the alert list via XCom — passed automatically because TaskFlow uses return values."

## 7. DagRun
One paragraph. Cover: instance of a DAG at a specific logical date (execution_date),
manual trigger vs scheduled, run states (queued, running, success, failed),
each DagRun contains one TaskInstance per task, logical_date vs data_interval_start.
End with: "Triggering POST /dags/citi_alert_summary/dagRuns creates a DagRun — its dag_run_id tracks the full pipeline execution."

## 8. SLA + Alerting
One paragraph. Cover: Service Level Agreement on task duration, SLA miss triggers a callback,
on_failure_callback and on_retry_callback on tasks, email_on_failure, Slack webhook via HttpOperator,
Airflow does not retry by default — set retries=3 explicitly.
End with: "In production, load_report would have retries=3 and an on_failure_callback posting to the Citi ops Slack channel."

---

## Quick Reference Table

| Concept | One-line definition | Learning stack value |
|---------|---------------------|----------------------|
| DAG | Python workflow definition | citi_alert_summary |
| Task | Atomic unit of work | extract, transform, load |
| Operator | Task template | @task (TaskFlow) |
| Scheduler | Reads DAGs, creates runs, queues tasks | heartbeat: 5s |
| Executor | Runs tasks | LocalExecutor |
| XCom | Cross-task data passing | return values via TaskFlow |
| DagRun | DAG instance at a logical date | triggered via REST API |
| SLA | Max allowed task duration | retries=3, on_failure_callback |

---

## Interview Flashcards

**Q: What is the difference between the Scheduler and the Executor?**
A: The Scheduler decides when to run tasks — it reads DAG files, evaluates schedules, and creates
DagRuns. The Executor actually runs tasks. They are separate components. LocalExecutor runs tasks
as subprocesses; CeleryExecutor sends them to a distributed worker pool.

**Q: When should you NOT use XCom?**
A: When the data is large (DataFrames, files, large result sets). XCom is stored in Airflow's
metadata DB — typically Postgres — which has row size limits and is not designed for bulk data.
Pass large data through S3, GCS, or a shared Postgres table, and pass only the path/identifier via XCom.

**Q: What does catchup=False do?**
A: Prevents Airflow from backfilling missed runs between start_date and today. With catchup=True
(default), if you deploy a daily DAG with start_date 30 days ago, Airflow queues 30 DagRuns immediately.
catchup=False runs only from the current schedule interval forward.

**Q: What happens when an upstream task fails?**
A: Downstream tasks move to upstream_failed state and are skipped — they do not run. The DagRun
ends in failed state. If the upstream task has retries configured, Airflow retries before propagating
the failure.

**Q: What is logical_date (execution_date) and why is it confusing?**
A: The logical_date represents the start of the data interval the DAG run is processing — it is
one schedule interval behind the actual run time. A daily DAG scheduled at midnight on 2026-04-01
has logical_date 2026-03-31 — it processes March 31st data. This trips up everyone the first time.

CONSTRAINTS:
- Each concept: exactly one paragraph, 4-6 sentences, no bullets inside
- Citi tie-in is the last sentence of each paragraph
- Table: valid GFM pipe table
- No filler phrases

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

