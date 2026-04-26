# ChatGPT Prompt — Apache Airflow Tutorial
# Paste everything between the === markers into ChatGPT

===

You are generating educational Python tutorial files for a Senior Data Engineer
personal study system. Each file must be production-quality, heavily commented,
and fully runnable.

TOPIC: Apache Airflow for Data Engineers
SLUG: apache-airflow
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: Pure Python (Airflow standalone — pip install apache-airflow)

===== CODING STANDARDS =====

FILE HEADER — every file starts with:
# ============================================================
# Topic   : Apache Airflow for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install apache-airflow | airflow db init | airflow standalone
# Run     : place in ~/airflow/dags/ and trigger via UI or airflow dags trigger
# ============================================================

COMMENTS: Explain WHY, not WHAT. Explain Airflow-specific concepts
(DAG serialization, task isolation, XCom, scheduler behavior) where they appear.

DOCSTRINGS — every function/DAG must have thorough explanation of design choices.

===== FILES TO GENERATE =====

01_dag_basics.py
  Purpose: First DAG — structure, scheduling, task dependencies, backfill
  Key concepts: DAG definition, schedule_interval, start_date, catchup, task dependency operators
  Contents:
    - Simple linear DAG: extract → transform → load → notify
    - Explain why start_date must be in the past, catchup=False for production
    - Show >> and << dependency operators
    - Show set_upstream / set_downstream equivalents
    - Add task-level retries and retry_delay
    - Explain the scheduler's role vs executor's role

02_operators_and_sensors.py
  Purpose: Core operators — PythonOperator, BashOperator, sensors, branching
  Key concepts: operator types, sensor poke vs reschedule, BranchPythonOperator, TriggerRule
  Contents:
    - PythonOperator: run a Python function as a task
    - BashOperator: shell command with environment injection
    - FileSensor: wait for a file to appear (reschedule mode to not block a worker slot)
    - BranchPythonOperator: route to different tasks based on logic
    - TriggerRule.ALL_DONE: run a cleanup task regardless of upstream success/failure
    - Explain poke_interval and timeout on sensors

03_xcom_variables_connections.py
  Purpose: Task communication and configuration — XCom, Variables, Connections
  Key concepts: XCom push/pull, Variable store, Connection store, when XCom is wrong choice
  Contents:
    - XCom: push a record count from extract, pull in load to validate
    - Explain XCom size limits — XCom is for metadata not data (max ~48KB in DB)
    - Airflow Variables: store config that changes without code deploy
    - Airflow Connections: store DB/API credentials, retrieve in tasks via BaseHook
    - Show how to set Variables and Connections via CLI and UI

04_dynamic_dags_and_taskflow.py
  Purpose: Modern DAG patterns — TaskFlow API, dynamic task mapping, parameterized DAGs
  Key concepts: @dag decorator, @task decorator, dynamic task mapping with .expand()
  Contents:
    - Rewrite a classic DAG using @dag and @task decorators (TaskFlow API)
    - Show how @task handles XCom automatically vs manual push/pull
    - Dynamic task mapping: process a list of files with .expand() — one task per file
    - Parameterized DAG: run same DAG logic for multiple pipelines using DAG params
    - Explain when TaskFlow simplifies code vs when classic operators are better

05_error_handling_and_monitoring.py
  Purpose: Production DAG patterns — callbacks, SLAs, retries, alerting, logging
  Key concepts: on_failure_callback, on_success_callback, SLA miss, email alerts, task logs
  Contents:
    - on_failure_callback: send Slack/email notification with task context
    - on_success_callback: log pipeline metrics on completion
    - SLA: define expected completion time, trigger SLA miss callback
    - Email operator: send summary report on DAG completion
    - Custom log statements in tasks: use logging.getLogger("airflow.task")
    - Explain how to find task logs in the UI and in the file system

===== CAPSTONE PROJECT =====

capstone/brief.md
  Title: Daily ETL Orchestration DAG
  Scenario: An Airflow DAG orchestrates a daily data pipeline that:
    extracts records from a PostgreSQL source table (simulated),
    validates row counts and null rates,
    transforms using pandas (clean, enrich, aggregate),
    loads to a target table,
    sends a success/failure report.
  What to build:
    - DAG with schedule="@daily", catchup=False
    - ExtractTask: query source, push record count via XCom
    - ValidateTask: pull count, fail if < 100 or null rate > 5%
    - TransformTask: pandas transform, write to /tmp/
    - LoadTask: load from /tmp/ to target (simulated)
    - NotifyTask: always runs (TriggerRule.ALL_DONE), reports status
    - on_failure_callback logs full context with traceback
  Acceptance criteria:
    - DAG loads without import errors
    - Validation task fails the DAG correctly when counts are bad
    - NotifyTask runs regardless of upstream failure
    - All XCom values visible in the Airflow UI

capstone/capstone.py — complete DAG file, place in ~/airflow/dags/
capstone/test_capstone.py — pytest using airflow.models.dagbag.DagBag to validate DAG loads

===== INFRASTRUCTURE NOTES =====

Pure Python — Airflow standalone mode.
Install: pip install apache-airflow
Init: airflow db init && airflow standalone
DAG files go in ~/airflow/dags/
PostgreSQL simulation: use sqlite or generate data synthetically — no Docker needed for DAG logic.
All file paths use /tmp/studybook/airflow/ or configurable env var.

===== START =====

Acknowledge these instructions, then wait for me to say "generate file 01".

===
