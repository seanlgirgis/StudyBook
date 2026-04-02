SAVE AS: airflow_intro.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

ROLE: You are a senior Data Engineer writing a Jupyter notebook for an engineer learning
Apache Airflow for the first time. You write production-quality, fully working code.
No placeholders. No TODO comments. Every cell must execute against the real running stack.

TASK: Generate airflow_intro.ipynb — a Jupyter notebook covering the Airflow mental model,
DAG authoring, and a first real DAG that reads telemetry data and writes a summary.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints, daily alert summary report needed by ops team at 06:00

TECH STACK CONTEXT — do not deviate:
- Airflow: localhost:8082, apache/airflow:2.8.0, standalone mode, LocalExecutor
- Airflow UI credentials: admin/admin (standalone default)
- DAG files must be placed in the airflow-dags Docker volume — from host, use the Airflow API to trigger
- Airflow REST API base: http://localhost:8082/api/v1

NOTEBOOK STRUCTURE — produce exactly these sections in order:

SECTION 1 — Title + Mental Model (markdown cell)
- H1: "Apache Airflow — First Contact"
- 3-paragraph mental model: what Airflow is, workflow orchestration vs execution,
  DAG = Directed Acyclic Graph of tasks with dependencies
- Citi framing: "Every morning at 06:00, Citi ops need an alert summary: how many HIGH/CRITICAL
  alerts per region overnight. This is a scheduled pipeline — exactly what Airflow orchestrates."
- ASCII diagram: [Scheduler] → [DAG: extract_alerts → transform_summary → load_report] → [Postgres]

SECTION 2 — Install + Imports (code cell)
- pip install apache-airflow requests psycopg2-binary
- imports: requests, json, psycopg2, datetime, time

SECTION 3 — Airflow API Health Check (code cell + markdown)
- Markdown: "Verify Airflow is up before we interact with it"
- Code: GET http://localhost:8082/health, auth=('admin','admin')
  Print response JSON and "Airflow is healthy" or raise error with full response text

SECTION 4 — The DAG File (markdown + code cell)
- Markdown: H2 "Writing the DAG"
  - Explain: a DAG file is a Python script placed in the dags/ folder
  - Airflow scheduler scans dags/ every 30s and picks up new DAGs automatically
  - This notebook writes the DAG file content and shows you what to place in the dags folder
- Code: define DAG_CONTENT as a Python string containing a complete, valid Airflow DAG:
  ```
  DAG ID: citi_alert_summary
  Schedule: 0 6 * * * (daily at 06:00)
  Start date: datetime(2026, 1, 1)
  catchup: False
  tags: ['citi', 'telemetry', 'daily']

  Tasks (using @task decorator / TaskFlow API):

  Task 1: extract_alerts()
    - Connect to Postgres (hardcoded: host.docker.internal:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!)
    - SELECT alert_id, endpoint_id, severity, created_at FROM alerts
      WHERE created_at >= CURRENT_DATE - INTERVAL '1 day'
    - Return list of dicts (json-serializable)
    - Print: f"Extracted {len(rows)} alerts"

  Task 2: transform_summary(alerts: list)
    - Group by severity, count per severity
    - Return dict: {"HIGH": N, "CRITICAL": N, "MEDIUM": N, ...}
    - Print summary dict

  Task 3: load_report(summary: dict)
    - Connect to Postgres
    - CREATE TABLE IF NOT EXISTS alert_daily_summary
        (report_date DATE, severity VARCHAR, alert_count INT, created_at TIMESTAMPTZ DEFAULT NOW())
    - INSERT one row per severity from summary dict, report_date = CURRENT_DATE
    - Print: f"Loaded {len(summary)} severity rows to alert_daily_summary"

  Task dependency: extract >> transform >> load (using TaskFlow return values)
  ```
- Print DAG_CONTENT to notebook so user can review it

SECTION 5 — DAG Placement Instructions (markdown cell)
- H2: "Where to Put the DAG File"
- Explain: the airflow-dags Docker volume is at /opt/airflow/dags inside the container
- Command to copy into container:
  ```
  docker cp citi_alert_summary.py citi_airflow:/opt/airflow/dags/
  ```
- Or use the Airflow API to write the file (Section 7 does this via REST API)
- Note: Airflow rescans every 30 seconds — wait before triggering

SECTION 6 — Write DAG File to Container (code cell + markdown)
- Markdown: "We write the DAG file directly into the Airflow container via docker exec"
- Code:
  - Write DAG_CONTENT to a local temp file: /tmp/citi_alert_summary.py
  - Use subprocess to: docker cp /tmp/citi_alert_summary.py citi_airflow:/opt/airflow/dags/
  - Print: "DAG file copied to citi_airflow container"
  - time.sleep(35) with print "Waiting 35s for Airflow scheduler to pick up the DAG..."

SECTION 7 — Verify DAG Registered (code cell + markdown)
- Markdown: "Check the Airflow API to confirm the DAG is registered"
- Code: GET http://localhost:8082/api/v1/dags/citi_alert_summary, auth=('admin','admin')
  Print: dag_id, schedule_interval, is_paused
  If 404, print "DAG not found — wait another 30s and re-run this cell"

SECTION 8 — Unpause + Trigger the DAG (code cell + markdown)
- Markdown: "New DAGs start paused. Unpause then trigger a manual run."
- Code:
  - PATCH /api/v1/dags/citi_alert_summary with {"is_paused": false}
  - POST /api/v1/dags/citi_alert_summary/dagRuns with {"logical_date": today's date ISO format}
  - Print: f"DAG run triggered: {response.json()['dag_run_id']}"

SECTION 9 — Poll Run Status (code cell + markdown)
- Markdown: "Poll until the run succeeds or fails (max 60s)"
- Code:
  - Loop up to 12 times with 5s sleep
  - GET /api/v1/dags/citi_alert_summary/dagRuns/{dag_run_id}
  - Print state each iteration
  - Break when state in ("success", "failed")
  - Print final outcome

SECTION 10 — Verify Output in Postgres (code cell + markdown)
- Markdown: "The DAG wrote to alert_daily_summary — let's verify"
- Code: psycopg2 connect, SELECT * FROM alert_daily_summary ORDER BY report_date DESC LIMIT 10
  Print rows

SECTION 11 — Summary (markdown cell)
- H2: "What Just Happened"
- Bullets: authored a DAG in TaskFlow API, deployed via docker cp, triggered via REST API,
  data in Postgres confirmed
- Citi tie-in: "This DAG runs every morning at 06:00. Ops teams get fresh alert counts without
  any manual intervention. Add a Slack notification task to make it production-ready."
- Next: "Run airflow_concepts.md for vocabulary, then Round 2 for production patterns."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4
- The DAG file content (DAG_CONTENT) must be valid Python that imports from airflow correctly
- All API calls use requests with auth=('admin','admin') — no hardcoded session objects
- subprocess import added in Section 6 cell
- Poll loop must terminate — max 12 iterations
- No placeholder values anywhere

ACCEPTANCE: Every code cell executes top-to-bottom. Section 10 shows rows in alert_daily_summary.

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

