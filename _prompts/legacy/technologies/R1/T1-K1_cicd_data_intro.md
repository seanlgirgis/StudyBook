SAVE AS: cicd_data_intro.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

ROLE: You are a senior Data Engineer writing a Jupyter notebook for an engineer learning
CI/CD for data pipelines for the first time. You write production-quality, fully working code.
No placeholders. No TODO comments. Every cell must execute.

TASK: Generate cicd_data_intro.ipynb — a Jupyter notebook covering the DataOps mental model,
GitHub Actions for dbt CI, and Great Expectations for data quality checks on the Citi telemetry data.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- dbt project: D:\Workspace\Technologies\citi_dbt\ (created in T1-D1)
- dbt models: stg_alerts, mart_alert_summary (in schema dbt_dev)
- endpoints: 10,000 rows | endpoint_id, name, region, status, category
- alerts: 25,000 rows | alert_id, endpoint_id, severity, message, created_at
- Citi narrative: data quality failures are production incidents — an alert with null severity breaks ops dashboards

TECH STACK CONTEXT — do not deviate:
- GitHub Actions: .github/workflows/ YAML files (shown in notebook, not executed locally)
- Great Expectations: installed via pip, runs locally against de_telemetry Postgres
- dbt: installed via pip (dbt-postgres), citi_dbt project

NOTEBOOK STRUCTURE — produce exactly these sections in order:

SECTION 1 — Title + Mental Model (markdown cell)
- H1: "CI/CD for Data — First Contact"
- 3-paragraph mental model: what DataOps is (DevOps applied to data pipelines), why data pipelines
  need CI/CD (silent data quality failures are worse than crashes), testing pyramid for data
  (unit tests → integration tests → data quality checks → pipeline tests)
- Citi framing: "A bad dbt model passes all SQL syntax checks but returns zero rows for HIGH severity alerts —
  ops team doesn't notice for 3 days. Great Expectations would have caught this in 2 minutes."
- ASCII diagram: [PR opened] → [GitHub Actions: dbt test] → [GE checkpoint] → [Pass: merge] / [Fail: block]

SECTION 2 — Install + Imports (code cell)
- pip install great-expectations dbt-postgres
- imports: great_expectations as gx, psycopg2, pandas, subprocess, json, pathlib

SECTION 3 — Great Expectations Setup (code cell + markdown)
- Markdown: H2 "Great Expectations — Data Quality as Code"
  - Explain: GE defines expectations (assertions about data), suites (collections of expectations),
    checkpoints (run a suite against a datasource), data docs (HTML report of results)
- Code:
  - context = gx.get_context(mode="file", project_root_dir="D:/Workspace/Technologies/citi_ge/")
  - Print: f"GE context created at: {context.root_directory}"

SECTION 4 — Add Postgres Datasource (code cell + markdown)
- Markdown: "Connect GE to the de_telemetry Postgres database"
- Code:
  - datasource = context.sources.add_postgres(
        name="de_telemetry",
        connection_string="postgresql+psycopg2://de_admin:DeAdmin2026!@localhost:5432/de_telemetry"
    )
  - asset_alerts = datasource.add_table_asset(name="alerts", table_name="alerts")
  - asset_endpoints = datasource.add_table_asset(name="endpoints", table_name="endpoints")
  - Print: "Datasource 'de_telemetry' with assets 'alerts' and 'endpoints' added"

SECTION 5 — Create Expectation Suite for Alerts (code cell + markdown)
- Markdown: H2 "Expectation Suite — Defining Data Quality Rules"
- Code:
  - suite = context.add_expectation_suite("citi_alerts_suite")
  - validator = context.get_validator(
        batch_request=asset_alerts.build_batch_request(),
        expectation_suite_name="citi_alerts_suite"
    )
  - Add expectations:
    validator.expect_column_values_to_not_be_null("alert_id")
    validator.expect_column_values_to_be_unique("alert_id")
    validator.expect_column_values_to_not_be_null("severity")
    validator.expect_column_values_to_be_in_set("severity", ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
    validator.expect_column_values_to_not_be_null("endpoint_id")
    validator.expect_table_row_count_to_be_between(min_value=1000, max_value=100000)
    validator.expect_column_values_to_not_be_null("created_at")
  - validator.save_expectation_suite()
  - Print: f"Saved suite 'citi_alerts_suite' with {len(suite.expectations)} expectations"

SECTION 6 — Run Checkpoint (code cell + markdown)
- Markdown: H2 "Checkpoint — Running the Suite"
- Code:
  - checkpoint = context.add_or_update_checkpoint(
        name="citi_alerts_checkpoint",
        validations=[{
            "batch_request": asset_alerts.build_batch_request(),
            "expectation_suite_name": "citi_alerts_suite"
        }]
    )
  - result = checkpoint.run()
  - Print: f"Overall success: {result.success}"
  - For each validation result, print: column, expectation_type, success, observed_value
  - Print: "View full HTML report: context.open_data_docs()"

SECTION 7 — dbt Tests Reminder (code cell + markdown)
- Markdown: H2 "dbt Tests — the First Line of Defense"
- Code: run dbt test on citi_dbt and print output:
  subprocess.run(["dbt", "test", "--project-dir", "D:/Workspace/Technologies/citi_dbt"], ...)
  Print pass/fail count

SECTION 8 — GitHub Actions Workflow (markdown cell with embedded YAML)
- Markdown: H2 "GitHub Actions — CI for Your dbt + GE Pipeline"
  - Explain: .github/workflows/dbt_ci.yml runs on every PR, runs dbt test + GE checkpoint,
    fails the PR if either fails — no broken models merged to main
  - Label: "📋 Create this file at: .github/workflows/dbt_ci.yml"
- Embedded YAML code fence:
  ```yaml
  name: dbt + Data Quality CI

  on:
    pull_request:
      branches: [main]
    push:
      branches: [main]

  jobs:
    dbt-test:
      name: dbt build + test
      runs-on: ubuntu-latest

      env:
        DBT_PROFILES_DIR: ${{ github.workspace }}/.dbt
        POSTGRES_HOST: localhost
        POSTGRES_PORT: 5432
        POSTGRES_DB: de_telemetry
        POSTGRES_USER: de_admin
        POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}

      services:
        postgres:
          image: postgres:16
          env:
            POSTGRES_USER: de_admin
            POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
            POSTGRES_DB: de_telemetry
          ports:
            - 5432:5432
          options: >-
            --health-cmd pg_isready
            --health-interval 10s
            --health-timeout 5s
            --health-retries 5

      steps:
        - uses: actions/checkout@v4

        - name: Set up Python
          uses: actions/setup-python@v5
          with:
            python-version: '3.11'

        - name: Install dependencies
          run: |
            pip install dbt-postgres great-expectations psycopg2-binary

        - name: Write dbt profiles.yml
          run: |
            mkdir -p .dbt
            cat > .dbt/profiles.yml << EOF
            citi_dbt:
              target: ci
              outputs:
                ci:
                  type: postgres
                  host: localhost
                  port: 5432
                  dbname: de_telemetry
                  user: de_admin
                  password: ${{ secrets.POSTGRES_PASSWORD }}
                  schema: dbt_ci
                  threads: 4
            EOF

        - name: Seed test data
          run: python Technologies/scripts/seed_ci_data.py

        - name: dbt build (run + test)
          run: dbt build --project-dir Technologies/citi_dbt

        - name: Great Expectations checkpoint
          run: python Technologies/scripts/run_ge_checkpoint.py

        - name: Upload GE data docs
          if: always()
          uses: actions/upload-artifact@v4
          with:
            name: ge-data-docs
            path: Technologies/citi_ge/uncommitted/data_docs/
  ```

SECTION 9 — DataOps Testing Pyramid (markdown cell)
- H2: "The Data Testing Pyramid"
- Table:

| Level | What you test | Tool | When it runs |
|-------|--------------|------|-------------|
| Unit | SQL logic in isolation (mock data) | dbt tests | On every dbt build |
| Integration | Model against real DB | dbt build in CI | On every PR |
| Data Quality | Source data assertions | Great Expectations | On every PR + schedule |
| Pipeline | End-to-end DAG run | Airflow test mode | On deploy |
| Contract | Schema agreed with producers | dbt sources freshness | On schedule |

SECTION 10 — Summary (markdown cell)
- H2: "What Just Happened"
- Bullets: GE context + Postgres datasource, 7 expectations on alerts table, checkpoint run,
  dbt tests run, GitHub Actions workflow shown
- Citi tie-in: "Every PR to the Citi telemetry dbt repo triggers: dbt build → dbt test → GE checkpoint.
  A model that breaks the severity constraint fails CI in 90 seconds — not in production 3 days later."
- Next: "Run cicd_data_concepts.md for vocabulary, then Round 2 for advanced GE patterns and data contracts."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4
- GE context uses mode="file" with explicit project_root_dir (not interactive mode)
- All subprocess calls: capture_output=True, text=True
- Section 8 GitHub Actions YAML is in a markdown cell as an embedded code fence — NOT a code cell
- GE API uses fluent datasource API (not legacy v2 context.add_datasource)
- citi_ge directory: D:/Workspace/Technologies/citi_ge/

ACCEPTANCE: Every code cell executes. Section 6 prints GE checkpoint results with overall success.

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

