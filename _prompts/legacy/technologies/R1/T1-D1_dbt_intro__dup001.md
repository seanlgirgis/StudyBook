SAVE AS: dbt_intro.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

ROLE: You are a senior Data Engineer writing a Jupyter notebook for an engineer learning
dbt (data build tool) for the first time. You write production-quality, fully working code.
No placeholders. No TODO comments. Every cell must execute against the real running stack.

TASK: Generate dbt_intro.ipynb — a Jupyter notebook covering the dbt mental model,
project structure, first model, and first test against the Citi telemetry dataset.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints; ops team needs clean, tested, documented views of alert data

TECH STACK CONTEXT — do not deviate:
- dbt: installed via pip (dbt-postgres), runs as CLI from the host machine
- dbt project lives at: D:\Workspace\Technologies\citi_dbt\
- dbt connects to the same Postgres instance as everything else

NOTEBOOK STRUCTURE — produce exactly these sections in order:

SECTION 1 — Title + Mental Model (markdown cell)
- H1: "dbt — First Contact"
- 3-paragraph mental model: what dbt is, transform-in-place philosophy (ELT not ETL),
  models = SELECT statements, dbt compiles and runs them, everything testable and documented
- Citi framing: "The raw alerts table is engineer-friendly but not analyst-friendly. dbt transforms
  raw tables into clean, named, tested views that ops teams can query in Kibana or Tableau."
- ASCII diagram: [raw: alerts] → [dbt model: stg_alerts] → [dbt model: mart_alert_summary] → [Analyst]

SECTION 2 — Install + Verify (code cell)
- pip install dbt-postgres
- Code: import subprocess; result = subprocess.run(["dbt", "--version"], capture_output=True, text=True)
  Print result.stdout

SECTION 3 — Initialize dbt Project (code cell + markdown)
- Markdown: "dbt init creates the project scaffold"
- Code: use subprocess to run:
  dbt init citi_dbt --adapter postgres --skip-profile-setup
  from working directory D:\Workspace\Technologies\
  Print stdout + stderr
  Then print the directory tree of citi_dbt/ using os.walk

SECTION 4 — profiles.yml (code cell + markdown)
- Markdown: explain profiles.yml — holds DB connection, lives in ~/.dbt/ NOT in project
- Code: write profiles.yml to Path.home() / ".dbt" / "profiles.yml" with content:
  ```yaml
  citi_dbt:
    target: dev
    outputs:
      dev:
        type: postgres
        host: localhost
        port: 5432
        dbname: de_telemetry
        user: de_admin
        password: DeAdmin2026!
        schema: dbt_dev
        threads: 4
  ```
- Print: "profiles.yml written to ~/.dbt/profiles.yml"

SECTION 5 — dbt debug (code cell + markdown)
- Markdown: "Verify dbt can reach Postgres before writing models"
- Code: subprocess.run(["dbt", "debug", "--project-dir", "citi_dbt"], capture_output=True, text=True)
  Print stdout. If "All checks passed!" in output: print "dbt debug OK"
  else: print full stderr and raise RuntimeError("dbt debug failed")

SECTION 6 — First Model: stg_alerts (code cell + markdown)
- Markdown: H2 "Staging Model"
  - Explain: staging models = 1-to-1 with source tables, rename/cast/clean only, no joins
  - Convention: models/staging/stg_alerts.sql
- Code: write the file D:\Workspace\Technologies\citi_dbt\models\staging\stg_alerts.sql with content:
  ```sql
  -- stg_alerts: clean and rename raw alerts
  SELECT
      alert_id,
      endpoint_id,
      UPPER(severity) AS severity,
      message,
      created_at::DATE AS alert_date,
      created_at AS alert_timestamp
  FROM {{ source('de_telemetry', 'alerts') }}
  ```
  Then write models/staging/sources.yml:
  ```yaml
  version: 2
  sources:
    - name: de_telemetry
      database: de_telemetry
      schema: public
      tables:
        - name: alerts
        - name: endpoints
  ```
- Print file paths written

SECTION 7 — Second Model: mart_alert_summary (code cell + markdown)
- Markdown: H2 "Mart Model"
  - Explain: mart models = business logic, joins, aggregations; materialized as tables
- Code: write D:\Workspace\Technologies\citi_dbt\models\marts\mart_alert_summary.sql:
  ```sql
  -- mart_alert_summary: daily alert counts per region and severity
  {{ config(materialized='table') }}

  WITH alerts AS (
      SELECT * FROM {{ ref('stg_alerts') }}
  ),
  endpoints AS (
      SELECT endpoint_id, name, region, category
      FROM {{ source('de_telemetry', 'endpoints') }}
  )
  SELECT
      a.alert_date,
      e.region,
      a.severity,
      COUNT(*) AS alert_count
  FROM alerts a
  LEFT JOIN endpoints e USING (endpoint_id)
  GROUP BY 1, 2, 3
  ORDER BY 1 DESC, 4 DESC
  ```
- Print: "mart_alert_summary.sql written"

SECTION 8 — Run the Models (code cell + markdown)
- Markdown: "dbt run compiles SQL and executes against Postgres"
- Code: subprocess.run(["dbt", "run", "--project-dir", "citi_dbt"], capture_output=True, text=True)
  Print stdout. Confirm "Completed successfully" or print error

SECTION 9 — Add Tests (code cell + markdown)
- Markdown: H2 "Testing"
  - Explain: dbt generic tests (not_null, unique, accepted_values, relationships)
- Code: write models/staging/stg_alerts.yml:
  ```yaml
  version: 2
  models:
    - name: stg_alerts
      columns:
        - name: alert_id
          tests:
            - unique
            - not_null
        - name: severity
          tests:
            - not_null
            - accepted_values:
                values: ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        - name: endpoint_id
          tests:
            - not_null
            - relationships:
                to: source('de_telemetry', 'endpoints')
                field: endpoint_id
  ```
  Then run: dbt test --project-dir citi_dbt
  Print test results

SECTION 10 — Query the Mart (code cell + markdown)
- Markdown: "Verify the mart in Postgres"
- Code: psycopg2 connect, SELECT * FROM dbt_dev.mart_alert_summary LIMIT 20, print rows

SECTION 11 — Summary (markdown cell)
- H2: "What Just Happened"
- Bullets: init project, write staging + mart models, sources.yml, tests, dbt run + dbt test, mart in Postgres
- Citi tie-in: "These two models give ops a clean, tested, documented view of alerts by region —
  updated by an Airflow DAG calling dbt run nightly."
- Next: "Run dbt_concepts.md for vocabulary, then Round 2 for incremental models and advanced patterns."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4
- All subprocess calls: capture_output=True, text=True, cwd set where needed
- File writes use pathlib.Path — create parent directories with mkdir(parents=True, exist_ok=True)
- No placeholder values
- dbt project name in dbt_project.yml must match profiles.yml key: citi_dbt

ACCEPTANCE: Every code cell executes. Section 10 shows rows from dbt_dev.mart_alert_summary.

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
