# Apache Airflow / MWAA — ChatGPT Project Prompts

Priority: 🔴 Critical — Toyota gap #2

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Apache Airflow and MWAA
Slug: apache-airflow
Extra coverage required: Airflow architecture — scheduler, webserver, executor, metadata database, worker,
DAGs — what they are, how they're authored, scheduling with cron and timetables,
operators — PythonOperator, BashOperator, S3ToRedshiftOperator, GlueJobOperator, the operator ecosystem,
sensors — waiting for S3 files, external DAG completion, custom sensors,
XComs — passing small values between tasks, when XCom is the wrong tool,
task dependencies — set_upstream, set_downstream, bitshift operators, branching,
dynamic DAGs — generating tasks programmatically for scalable pipeline patterns,
backfill — how Airflow handles historical runs, catchup=True vs False,
retries and SLAs — per-task retry config, DAG-level SLA miss callbacks,
connections and variables — storing credentials and config outside DAG code,
executors — LocalExecutor, CeleryExecutor, KubernetesExecutor — tradeoffs,
MWAA — AWS managed Airflow — setup, S3 DAG sync, environment sizing, cost model,
Airflow for data engineering — orchestrating Glue jobs, EMR steps, ECS tasks, dbt runs,
common mistakes — heavy logic in DAGs, misusing XCom for large data, scheduler overload,
Airflow vs Step Functions vs Prefect — when to choose each.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
```
run_mission_audio.ps1 -Slug apache-airflow -ChunkSize 750
```

Upload final_apache-airflow.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_apache-airflow.mp3` is live on R2.

```
Topic: Apache Airflow and MWAA
Slug: apache-airflow
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_apache-airflow.mp3
Today's date: 2026-04-25

Content sections — create exactly these, in this order:
Architecture Overview | DAGs & Scheduling | Operators & Sensors | XComs & Task Dependencies | Dynamic DAGs & Backfill | Executors | MWAA on AWS | Airflow for Data Engineering | Common Mistakes & Comparisons
Then add: Interview Q&A (6 pairs) | Quick Reference (12-15 rows)
Size per section: 2-3 tight paragraphs, one code block max (20 lines). No tutorials.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\apache-airflow.html
