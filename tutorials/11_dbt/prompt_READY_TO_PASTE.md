# READY TO PASTE INTO CHATGPT
# Open a FRESH ChatGPT chat. Copy everything between the === markers.
# Postgres must be running: docker ps | grep postgres
# After acknowledgment follow this sequence:
#   "generate file 01"
#   "generate file 02"
#   "generate file 03"
#   "generate file 04"
#   "generate file 05"
#   "generate readme"
#   "generate capstone file setup.py"
#   "generate capstone file stg_sensors.sql"
#   "generate capstone file stg_devices.sql"
#   "generate capstone file hourly_sensor_agg.sql"
#   "generate capstone file device_summary.sql"
#   "generate capstone file schema.yml"
#   "generate capstone file sources.yml"
#   "generate capstone file device_snapshot.sql"
#   "generate capstone file sensor_thresholds.csv"
#   "generate capstone file run_pipeline.py"
#   "generate capstone file test_capstone.py"
#   "generate capstone brief.md"
# Save each file to the correct path immediately.
# ============================================================

===

You are generating educational Python tutorial files for a Senior Data Engineer
personal study system. Every file you generate must be:
- COMPLETE and FULLY RUNNABLE — no placeholders, no TODO comments, no `pass` statements,
  no skeleton functions, no "implement this" notes
- Production-quality with heavy WHY comments
- Runnable against a real local Postgres database

If a file would be too long for one response, continue immediately without waiting.
Never truncate a file mid-function.

TOPIC: dbt (data build tool) for Data Engineers
SLUG: dbt
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: Docker — PostgreSQL on localhost:5432
  db=studybook, user=studybook, password=studybook
  This container is ALREADY RUNNING in the studybook_core stack.
  Do NOT generate docker-compose files or instructions to start Postgres.
  Connect directly to localhost:5432.

===== CODING STANDARDS =====

FILE HEADER — every Python file starts with:
# ============================================================
# Topic   : dbt for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install dbt-postgres psycopg2-binary | Postgres on localhost:5432
# Run     : python filename.py
# ============================================================

SQL and YAML files use a comment header:
-- ============================================================
-- Topic   : dbt for Data Engineers
-- File    : filename.sql
-- Covers  : one-line description
-- ============================================================

ENVIRONMENT VARIABLES — declare at top of every Python file:
  POSTGRES_HOST      default "localhost"
  POSTGRES_PORT      default "5432"
  POSTGRES_DB        default "studybook"
  POSTGRES_USER      default "studybook"
  POSTGRES_PASSWORD  default "studybook"
  DBT_PROJECT_DIR    default "/tmp/studybook/dbt_tutorial"
  DBT_PROFILES_DIR   default "/tmp/studybook/dbt_profiles"

DOCSTRINGS — every Python function must have:
  - One-line summary
  - WHY field: the senior insight
  - Args with types
  - Returns with type
  - Raises if applicable

CODE RULES:
  - Python 3.11+, type hints on all signatures
  - os.environ for ALL config — never hardcode
  - subprocess.run() for all dbt CLI calls — capture stdout/stderr
  - Specific exception handling — never bare except:
  - Every Python file ends with if __name__ == "__main__": that runs a full demo
  - All dbt project files written to DBT_PROJECT_DIR; profiles.yml to DBT_PROFILES_DIR

CLEANUP — include a cleanup() function in every Python file that creates DB objects.
  Cleanup drops tables/schemas created by that file.
  Wrap main() demo in try/finally with cleanup in finally.
  Print "✅ Cleanup complete." at end of cleanup().

===== FILES TO GENERATE =====

01_dbt_project_setup.py
  Purpose: Create a dbt project from Python, write all config files, verify connection
  Key concepts: profiles.yml (connection config), dbt_project.yml (project config),
    materializations (table vs view vs incremental vs ephemeral), why dbt over raw SQL scripts
  Functions:
    - get_db_conn() -> psycopg2.connection
        WHY: verify Postgres is reachable before doing any dbt work — fail fast
    - generate_profiles_yml(host: str, port: str, db: str, user: str,
        password: str, schema: str = "analytics") -> str
        — return complete profiles.yml YAML string for the "studybook" profile
        WHY: profiles.yml lives outside the project repo (in DBT_PROFILES_DIR) so
        credentials are never committed to git
    - generate_dbt_project_yml(project_name: str, profile_name: str) -> str
        — return complete dbt_project.yml YAML string:
          name, version, profile, model-paths, seed-paths, snapshot-paths, macro-paths
          models config: staging → +materialized: view; marts → +materialized: table
        WHY: default materializations per folder means individual models don't need
        config() blocks unless overriding — less boilerplate
    - create_dbt_project_structure(base_dir: Path) -> None
        — create all required directories:
          models/staging/, models/marts/, snapshots/, seeds/, macros/, tests/, analyses/
    - write_project_files(base_dir: Path, profiles_dir: Path) -> None
        — write dbt_project.yml to base_dir
        — write profiles.yml to profiles_dir
        — write a .gitignore to base_dir (ignore: target/, dbt_packages/, logs/)
    - run_dbt_debug(project_dir: Path, profiles_dir: Path) -> dict
        — subprocess: dbt debug --project-dir ... --profiles-dir ...
        — parse stdout: return {success: bool, connection_ok: bool, output: str}
        WHY: dbt debug is the first thing to run after creating a project —
        it validates profiles, adapter, and database connectivity in one command
  Main block (try/finally with cleanup):
    - create project structure at DBT_PROJECT_DIR
    - write project + profile files
    - run dbt debug, print result
    - cleanup: remove DBT_PROJECT_DIR and DBT_PROFILES_DIR directories

02_dbt_models_and_refs.py
  Purpose: Write and run dbt SQL models — staging pattern, ref(), schema tests
  Key concepts: staging → marts layers, ref() for DAG lineage, config() block,
    built-in schema tests: unique, not_null, accepted_values, relationships
  Functions:
    - setup_raw_tables(conn: psycopg2.connection) -> None
        — create schema "raw" if not exists
        — create and populate raw.orders (order_id, customer_id, amount, status, created_at)
          with 200 rows of synthetic data
        — create and populate raw.customers (customer_id, name, region, tier)
          with 50 rows
        WHY: dbt needs upstream "raw" tables — in real pipelines these come from
        your ingestion layer (Firehose, Airbyte, Kafka Connect)
    - generate_staging_model(source_name: str, table_name: str,
        renamed_cols: dict[str, str], filter_expr: str | None = None) -> str
        — return SQL string for a staging model:
          {{ config(materialized='view') }}
          with source as (
            select * from {{ source(source_name, table_name) }}
          )
          select <renamed columns> from source
          [where filter_expr]
        WHY: staging models are the "translation layer" — they rename, cast, and
        filter raw source data into a clean contract for downstream models
    - generate_mart_model(name: str, staging_refs: list[str],
        join_conditions: list[str], select_cols: list[str],
        materialization: str = "table") -> str
        — return SQL string for a mart model using {{ ref() }} for all upstream refs
    - generate_sources_yml(source_name: str, schema: str,
        tables: list[str]) -> str
        — return sources.yml YAML string declaring the raw tables
    - generate_schema_yml(models: list[dict]) -> str
        — return schema.yml YAML; each model dict has:
          {name, description, columns: [{name, description, tests: [list]}]}
        — include unique + not_null tests on all ID columns
        — include accepted_values test on status column
    - write_and_run_models(project_dir: Path, profiles_dir: Path) -> dict
        — write all SQL + YAML files to project_dir
        — run: dbt deps, dbt run, dbt test
        — return {run_success, test_success, stdout}
  Main block (try/finally with cleanup):
    - setup_raw_tables
    - write 2 staging models (stg_orders, stg_customers) + 1 mart (orders_summary)
    - write sources.yml + schema.yml
    - run dbt run + dbt test
    - print results
    - cleanup: drop raw schema, drop analytics schema, remove project files

03_dbt_incremental_models.py
  Purpose: Incremental models — process only new/changed data on each run
  Key concepts: is_incremental() Jinja macro, unique_key, merge vs append strategy,
    late-arriving data lookback window, run_results.json for timing
  Functions:
    - setup_events_table(conn: psycopg2.connection) -> None
        — create raw.pipeline_events (event_id serial, pipeline_name, stage,
          records_in, records_out, run_at timestamptz, status)
        — insert 500 rows with run_at spread across last 7 days
    - generate_incremental_model(model_name: str, source_ref: str,
        ts_column: str, unique_key: str,
        strategy: str = "merge") -> str
        — return complete SQL for an incremental model:
          {{ config(materialized='incremental',
                    unique_key=unique_key,
                    incremental_strategy=strategy) }}
          select * from {{ source(...) }}
          {% if is_incremental() %}
            where {{ ts_column }} > (select max({{ ts_column }}) from {{ this }})
          {% endif %}
        WHY: is_incremental() is the core dbt incremental pattern — on first run it
        processes all data; on subsequent runs it processes only the delta.
        The `this` keyword refers to the existing table, enabling self-referencing.
    - generate_late_arriving_model(model_name: str, ts_column: str,
        lookback_days: int = 3) -> str
        — incremental model that looks back N days to catch records that arrived late
        WHY: event data from IoT devices or mobile apps can arrive hours or days late.
        A pure max(ts) filter would miss these — the lookback window catches them.
    - insert_new_events(conn: psycopg2.connection, count: int = 100) -> None
        — insert `count` new rows with run_at = now()
    - parse_run_results(project_dir: Path) -> list[dict]
        — read target/run_results.json, extract per-model:
          {model_name, status, rows_affected, execution_time_s}
        WHY: run_results.json is how you instrument dbt in a CI/CD pipeline — check
        row counts and timing programmatically without parsing stdout
    - compare_full_vs_incremental(project_dir: Path,
        profiles_dir: Path, model_name: str) -> dict
        — run dbt run --full-refresh, record timing + rows
        — insert 100 new events
        — run dbt run (incremental), record timing + rows
        — return {full_refresh_rows, full_refresh_ms, incremental_rows, incremental_ms}
  Main block (try/finally with cleanup):
    - setup_events_table
    - write incremental model + late_arriving model to project
    - call compare_full_vs_incremental, print comparison table
    - cleanup: drop raw.pipeline_events, drop analytics schema, remove project files

04_dbt_tests_and_documentation.py
  Purpose: dbt testing — schema tests, singular tests, generic test macros, dbt docs
  Key concepts: built-in tests vs singular tests (custom SQL), generic test macros,
    dbt docs generate, test result parsing
  Functions:
    - generate_singular_test(test_name: str, model_ref: str,
        sql_assertion: str) -> str
        — return SQL for a singular test file (returns 0 rows = pass):
          -- Test: test_name
          -- Passes if 0 rows returned (all rows satisfy the condition)
          select * from {{ ref(model_ref) }}
          where not (sql_assertion)
        WHY: singular tests are for business rules that can't be expressed as
        generic schema tests — e.g., "amount must be positive for completed orders"
    - generate_generic_test_macro(macro_name: str,
        description: str, sql_template: str) -> str
        — return Jinja macro defining a reusable test:
          {% test macro_name(model, column_name) %}
            sql_template using model + column_name
          {% endtest %}
        — provide 2 examples: is_positive(model, column_name) and
          is_non_empty_string(model, column_name)
        WHY: generic test macros extend dbt's built-in tests — define once, apply
        to any model column in schema.yml with just the test name
    - generate_docs_block(model_name: str, model_description: str,
        columns: list[dict]) -> str
        — return YAML docs block for schema.yml:
          each column dict: {name, description, tests: [list]}
    - run_dbt_test(project_dir: Path, profiles_dir: Path,
        select: str | None = None) -> dict
        — subprocess: dbt test [--select select]
        — parse output: return {passed: int, failed: int, errors: int,
            failed_tests: [list of test names]}
    - generate_dbt_docs(project_dir: Path, profiles_dir: Path) -> Path
        — subprocess: dbt docs generate
        — return path to target/index.html
        WHY: dbt docs generates a full data catalog with lineage DAG — the best
        free documentation tool available to analytics engineers
    - explain_test_strategies() -> None
        — print a formatted comparison table:
          | Test type      | When to use                          | Example              |
          | schema test    | column constraints (null, unique)    | not_null, unique     |
          | singular test  | business rules, cross-column rules   | amount > 0 for paid  |
          | generic macro  | reusable custom constraints          | is_positive          |
          | pytest         | pipeline orchestration, row counts   | after dbt run        |
  Main block (try/finally with cleanup):
    - assume raw tables from file 02 (re-create if needed)
    - write 3 schema tests, 2 singular tests, 1 generic macro to project
    - run dbt run + dbt test, print pass/fail per test
    - generate docs, print path to index.html
    - cleanup: drop schemas, remove project

05_dbt_advanced_patterns.py
  Purpose: Seeds, snapshots (SCD Type 2), macros, packages, pre/post hooks
  Key concepts: seeds for reference data, snapshots for tracking changes over time,
    Jinja macros for reusable SQL, dbt-utils package, audit hooks
  Functions:
    - generate_seed_csv(name: str, rows: list[dict]) -> str
        — return CSV string (header + rows) for a dbt seed file
        WHY: seeds are for small, static reference data that belongs in version control
        (e.g., country codes, alert thresholds, product categories)
    - generate_snapshot_sql(snapshot_name: str, source_schema: str,
        source_table: str, unique_key: str, strategy: str,
        updated_at_col: str | None = None,
        check_cols: list[str] | None = None) -> str
        — return complete snapshot SQL:
          {% snapshot snapshot_name %}
          {{ config(target_schema='snapshots',
                    unique_key=unique_key,
                    strategy=strategy,
                    updated_at=updated_at_col,  # if strategy='timestamp'
                    check_cols=check_cols) }}    # if strategy='check'
          select * from {{ source(source_schema, source_table) }}
          {% endsnapshot %}
        WHY: dbt snapshots implement SCD Type 2 automatically — they add
        dbt_valid_from, dbt_valid_to, dbt_scd_id columns and maintain history
        without you writing any merge logic
    - generate_audit_macro(macro_name: str = "log_model_run") -> str
        — return Jinja macro for a pre/post hook that writes to an audit table:
          insert into analytics.dbt_audit (model, run_at, rows_affected)
          values ('{{ this }}', now(), (select count(*) from {{ this }}))
    - generate_packages_yml() -> str
        — return packages.yml declaring dbt-utils ^1.0.0
        WHY: dbt-utils adds 50+ useful macros including generate_surrogate_key,
        date_spine, pivot, and many more — it's the de-facto standard dbt library
    - run_snapshot_twice(project_dir: Path, profiles_dir: Path,
        conn: psycopg2.connection,
        source_table: str) -> dict
        — run dbt snapshot (initial)
        — UPDATE 5 rows in source_table to simulate real changes
        — run dbt snapshot again
        — query snapshots schema: return {total_versions, rows_with_history,
            sample_scd_record: dict with dbt_valid_from, dbt_valid_to}
        WHY: running the snapshot twice with a change in between is the only way
        to actually see SCD2 behaviour — this demo makes it concrete
  Main block (try/finally with cleanup):
    - create raw.devices table (device_id, name, location, type, updated_at)
      with 20 rows
    - generate seed CSV (sensor_thresholds: device_type, warning_threshold, critical_threshold)
    - write snapshot SQL, macro, packages.yml to project
    - dbt deps (install dbt-utils), dbt seed, dbt snapshot (×2 with a data change)
    - query the snapshots table, print SCD2 history for one changed device
    - cleanup: drop raw.devices, drop snapshots schema, remove project files

===== README =====

Generate README.md for the 11_dbt directory with these exact sections:

1. Prerequisites
   - Docker postgres must be running: docker ps | grep postgres
   - pip install dbt-postgres psycopg2-binary
   - Environment variables (with defaults shown)

2. Quick Orientation — What dbt Is
   - 5-line plain-English explanation of what dbt does and why data engineers use it
   - The 3-layer pattern: raw → staging → marts

3. Phase 1 — Setup Scripts: one entry per file (01–05) with:
   - exact run command: python setup\01_dbt_project_setup.py
   - 2-sentence what it does
   - 1-sentence key takeaway

4. Phase 2 — Capstone: exact run order:
   python capstone\setup.py
   cd /tmp/studybook/dbt_capstone && dbt deps && dbt seed && dbt snapshot
   dbt run && dbt test && dbt docs generate
   python capstone\run_pipeline.py
   pytest capstone\test_capstone.py -v
   python capstone\cleanup.py

5. Emergency Cleanup — psycopg2 one-liner to drop all tutorial schemas:
   python -c "
   import psycopg2
   conn = psycopg2.connect(host='localhost', dbname='studybook', user='studybook', password='studybook')
   cur = conn.cursor()
   for schema in ['raw', 'analytics', 'snapshots', 'dbt_tutorial']:
       cur.execute(f'DROP SCHEMA IF EXISTS {schema} CASCADE')
   conn.commit(); conn.close()
   print('All tutorial schemas dropped.')
   "

6. Interview Angle — 3 bullet points on what Toyota/Capital One interviewers
   want to hear about dbt:
   - incremental models and why they matter for IoT/streaming data
   - SCD Type 2 with snapshots
   - testing as a first-class citizen (not an afterthought)

===== CAPSTONE PROJECT =====

The capstone is a COMPLETE, FULLY RUNNABLE Analytics Engineering Pipeline.
Every file must be complete — no placeholders, no TODO, no pass statements.

Title: IoT Device Analytics Pipeline with dbt
Scenario: The studybook Postgres database has raw IoT sensor data and a device registry.
  Build a production-grade dbt project that transforms raw → staging → marts,
  with incremental processing, SCD Type 2 device history, schema tests, and docs.

Database schema to work with:
  raw.sensor_readings  (reading_id serial, device_id varchar, sensor_type varchar,
                        value numeric, unit varchar, recorded_at timestamptz, quality_flag int)
  raw.devices          (device_id varchar, name varchar, plant varchar, device_type varchar,
                        location varchar, installed_at date, updated_at timestamptz)

dbt project location: /tmp/studybook/dbt_capstone  (or DBT_PROJECT_DIR)
dbt profiles location: /tmp/studybook/dbt_profiles  (or DBT_PROFILES_DIR)
Profile name: studybook
Target schema for models: analytics
Target schema for snapshots: snapshots

---

capstone/setup.py — COMPLETE FILE
  Purpose: Create raw tables, insert synthetic data, create dbt project structure
  Functions:
    - get_conn() -> psycopg2.connection
    - create_raw_schema(conn) -> None — CREATE SCHEMA IF NOT EXISTS raw
    - create_sensor_readings_table(conn) -> None — CREATE TABLE raw.sensor_readings (...)
    - create_devices_table(conn) -> None — CREATE TABLE raw.devices (...)
    - insert_sensor_readings(conn, count: int = 5000) -> None
        — insert count rows with:
          device_id: random from ["dev-001" through "dev-020"]
          sensor_type: random from ["temperature", "pressure", "vibration", "humidity"]
          value: realistic random floats per sensor_type
          unit: matching unit per sensor_type
          recorded_at: random timestamps across last 30 days
          quality_flag: 1 (good) with 5% chance of 0 (bad)
    - insert_devices(conn) -> None
        — insert exactly 20 devices across 3 plants: toyota-tx, toyota-ky, toyota-ca
          device_types: ["temperature_sensor", "pressure_sensor", "vibration_sensor"]
          updated_at: now()
    - create_dbt_project(project_dir: Path, profiles_dir: Path) -> None
        — write dbt_project.yml, profiles.yml, .gitignore
        — create all subdirectories
        — write packages.yml (dbt-utils ^1.0.0)
    - run_dbt_deps(project_dir: Path, profiles_dir: Path) -> None
        — subprocess: dbt deps
  Main block (try/finally — do NOT cleanup in setup, cleanup.py handles it):
    - call all setup functions in order
    - print row counts for both tables
    - print "Setup complete. Run run_pipeline.py to execute the dbt project."

---

capstone SQL model files — generate each as a COMPLETE file:

models/staging/sources.yml
  — declare source "raw" with schema "raw", tables: sensor_readings, devices
  — add source freshness check on sensor_readings (warn_after 1 day, error_after 3 days)

models/staging/stg_sensors.sql
  {{ config(materialized='view') }}
  — select from {{ source('raw', 'sensor_readings') }}
  — rename: reading_id → sensor_reading_id, recorded_at → event_ts
  — cast value to float
  — add derived column: is_quality_good = (quality_flag = 1)
  — filter: quality_flag IS NOT NULL

models/staging/stg_devices.sql
  {{ config(materialized='view') }}
  — select from {{ source('raw', 'devices') }}
  — deduplicate by device_id keeping latest updated_at using ROW_NUMBER()
  — rename: installed_at → installation_date
  — add derived column: days_since_install = current_date - installation_date

models/marts/hourly_sensor_agg.sql
  {{ config(materialized='incremental',
            unique_key='agg_id',
            incremental_strategy='merge') }}
  — join {{ ref('stg_sensors') }} with {{ ref('stg_devices') }} on device_id
  — truncate event_ts to hour as hour_bucket
  — aggregate per (device_id, plant, sensor_type, hour_bucket):
      avg_value, min_value, max_value, reading_count, good_reading_count
  — add agg_id = md5(device_id || sensor_type || hour_bucket::text)
  — incremental filter: {% if is_incremental() %}
      where event_ts > (select max(hour_bucket) from {{ this }})
    {% endif %}

models/marts/device_summary.sql
  {{ config(materialized='table') }}
  — join {{ ref('stg_devices') }} with latest reading from {{ ref('stg_sensors') }}
    (use ROW_NUMBER() to get most recent reading per device)
  — join with {{ ref('hourly_sensor_agg') }} to get last 24h avg per device
  — output: device_id, name, plant, device_type, days_since_install,
      latest_value, latest_event_ts, last_24h_avg, last_24h_reading_count

models/marts/schema.yml
  — document and test both mart models:
    hourly_sensor_agg:
      columns: agg_id (unique, not_null), device_id (not_null), hour_bucket (not_null),
               avg_value (not_null), reading_count (not_null)
    device_summary:
      columns: device_id (unique, not_null), plant (not_null, accepted_values: toyota-tx/toyota-ky/toyota-ca),
               latest_value (not_null)

snapshots/device_snapshot.sql
  {% snapshot device_snapshot %}
  {{ config(target_schema='snapshots',
            unique_key='device_id',
            strategy='timestamp',
            updated_at='updated_at') }}
  select device_id, name, plant, device_type, location, updated_at
  from {{ source('raw', 'devices') }}
  {% endsnapshot %}

seeds/sensor_thresholds.csv
  — CSV with columns: device_type, sensor_type, warning_threshold, critical_threshold, unit
  — 6 rows covering all combinations of device_type × sensor_type in the dataset

---

capstone/run_pipeline.py — COMPLETE FILE
  Purpose: Orchestrate the full dbt pipeline programmatically via subprocess
  Functions:
    - run_step(step_name: str, cmd: list[str], project_dir: Path,
        profiles_dir: Path, fail_on_error: bool = True) -> dict
        — run subprocess with --project-dir and --profiles-dir args
        — return {step: str, success: bool, duration_ms: float, stdout: str, stderr: str}
        — print ✅ or ❌ with duration after each step
    - parse_test_results(project_dir: Path) -> dict
        — read target/run_results.json
        — return {passed: int, failed: int, failed_tests: list[str]}
    - print_pipeline_summary(results: list[dict], test_summary: dict) -> None
        — print a formatted table:
          STEP              STATUS    DURATION
          dbt deps          ✅        1.2s
          dbt seed          ✅        0.8s
          dbt snapshot      ✅        1.5s
          dbt run           ✅        3.2s
          dbt test          ✅        2.1s
          dbt docs generate ✅        4.0s
          Tests: 8 passed, 0 failed
  Main block (try/finally — does NOT call cleanup, cleanup.py handles it):
    - run steps in order: dbt seed, dbt snapshot, dbt run, dbt test, dbt docs generate
    - parse test results
    - print_pipeline_summary
    - update one device's location in raw.devices (to demonstrate snapshot SCD2)
    - run dbt snapshot again
    - query snapshots.device_snapshot and print the 1 row that now has dbt_valid_to set
    - print path to docs index.html

---

capstone/test_capstone.py — COMPLETE PYTEST FILE
  Purpose: Validate pipeline outputs by querying Postgres directly
  Use psycopg2 to query the analytics schema after run_pipeline.py has run.

  Fixture:
    @pytest.fixture(scope="module")
    def conn():
        c = psycopg2.connect(host=..., dbname="studybook", ...)
        yield c
        c.close()

  Tests:
    - test_staging_sensors_row_count(conn):
        — query analytics.stg_sensors (or the view)
        — assert count(*) >= 4000  (allowing for quality filter dropping some rows)

    - test_staging_devices_no_duplicates(conn):
        — query analytics.stg_devices
        — assert count(*) == count(distinct device_id)  (deduplication worked)

    - test_hourly_agg_has_data(conn):
        — query analytics.hourly_sensor_agg
        — assert count(*) > 0
        — assert all avg_value IS NOT NULL

    - test_hourly_agg_unique_key(conn):
        — assert count(*) == count(distinct agg_id)

    - test_device_summary_all_devices_present(conn):
        — assert count(*) == 20  (all 20 devices represented)

    - test_snapshot_captures_history(conn):
        — query snapshots.device_snapshot
        — assert count(*) >= 20  (at least 20 current versions)
        — assert count(*) where dbt_valid_to IS NULL == 20  (20 current rows)
        — assert count(*) where dbt_valid_to IS NOT NULL >= 1  (at least 1 historical)

    - test_seeds_loaded(conn):
        — query analytics.sensor_thresholds
        — assert count(*) == 6

---

capstone/cleanup.py — COMPLETE FILE
  Purpose: Drop all schemas and files created by the capstone — safe to run twice
  Functions:
    - drop_db_schemas(schemas: list[str] = ["raw", "analytics", "snapshots"]) -> None
        — psycopg2 DROP SCHEMA IF EXISTS ... CASCADE for each
        — print each drop or "already gone"
    - remove_project_files(project_dir: Path, profiles_dir: Path) -> None
        — shutil.rmtree project_dir if exists
        — shutil.rmtree profiles_dir if exists
        — print each removal
    - cleanup_all() -> None
        — call both functions
        — print "✅ Cleanup complete. Postgres schemas dropped, project files removed."
  Main block:
    - cleanup_all()

===== INFRASTRUCTURE NOTES =====

Requires existing studybook_core Docker stack: postgres on localhost:5432
  db=studybook, user=studybook, password=studybook
  Container is ALREADY RUNNING — do not generate docker commands to start it.
Install: pip install dbt-postgres psycopg2-binary
dbt project written to DBT_PROJECT_DIR (default: /tmp/studybook/dbt_capstone)
profiles.yml written to DBT_PROFILES_DIR (default: /tmp/studybook/dbt_profiles)
All Python files drive dbt via subprocess — they are orchestrators, not replacements for dbt.
Cleanup: each setup file drops what it created; capstone/cleanup.py drops everything.
Print ✅ Cleanup complete. after every cleanup function.

===== START =====

Acknowledge these instructions. Confirm you understand:
1. Every file is COMPLETE and FULLY RUNNABLE — no placeholders, no TODO, no pass
2. SQL model files contain real, complete SQL — not descriptions of SQL
3. The capstone test file queries Postgres directly to verify actual pipeline output
4. After acknowledgment, wait for me to say "generate file 01"

===
