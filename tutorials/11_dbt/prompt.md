# ChatGPT Prompt — dbt Tutorial
# Paste everything between the === markers into ChatGPT

===

TOPIC: dbt (data build tool) for Data Engineers
SLUG: dbt
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: Docker — PostgreSQL on localhost:5432 (db=studybook, user=studybook, pass=studybook)
  Existing container: postgres (studybook_core stack). Do NOT spin up a new container.

===== CODING STANDARDS =====

FILE HEADER:
# ============================================================
# Topic   : dbt for Data Engineers
# File    : NN_filename.py  (or .sql / .yml as appropriate)
# Covers  : one-line description
# Prereqs : pip install dbt-postgres | Docker postgres on localhost:5432
# Run     : python filename.py  OR  dbt run --select model_name
# ============================================================

COMMENTS: Explain WHY. dbt is SQL-first — Python files here are drivers/orchestrators.
Explain the dbt project structure, ref() vs source(), materialization strategies.
Note: tutorial files are Python scripts that use dbt-core programmatically
  OR show dbt CLI commands + SQL models inline as strings for inspection.
Env vars: DBT_PROFILES_DIR, POSTGRES_HOST=localhost, POSTGRES_PORT=5432,
  POSTGRES_DB=studybook, POSTGRES_USER=studybook, POSTGRES_PASSWORD=studybook

===== FILES TO GENERATE =====

01_dbt_project_setup.py
  Purpose: Set up a dbt project programmatically — profiles, project.yml, sources
  Key concepts: profiles.yml (connection config), dbt_project.yml (project config),
    materializations (table vs view vs incremental vs ephemeral), source vs ref
  Functions:
    - generate_profiles_yml(host, port, db, user, password, schema="analytics") → str
      — YAML string for ~/.dbt/profiles.yml targeting Postgres
    - generate_dbt_project_yml(project_name, model_paths, profile_name) → str
      — YAML string for dbt_project.yml
    - generate_source_yml(source_name, schema, tables: list[str]) → str
      — sources.yml for declaring upstream tables
    - create_dbt_project_structure(base_dir, project_name) → None
      — create folder tree: models/staging/, models/marts/, tests/, macros/, seeds/
    - write_profiles_and_project(base_dir, project_name, db_config: dict) → None
      — write both YAMLs to correct locations
    - verify_dbt_connection(project_dir) → bool
      — run `dbt debug` via subprocess, parse output
  Main block: create a dbt project at /tmp/studybook/dbt_tutorial/, write profiles,
    create folder structure, verify connection

02_dbt_models_and_refs.py
  Purpose: Write dbt models — SQL models, ref(), materialization, schema testing
  Key concepts: ref() for lineage, config() block, staging vs mart pattern,
    built-in tests (unique, not_null, accepted_values, relationships)
  Functions:
    - generate_staging_model(source_name, table_name, select_cols: list[str],
        renamed_cols: dict, filter_expr=None) → str
      — return staging SQL model string (stg_sourcename__tablename.sql pattern)
    - generate_mart_model(name, staging_refs: list[str], joins: list[dict],
        aggregations: list[dict], materialization="table") → str
      — return mart SQL model string with config() block
    - generate_schema_yml(models: list[dict]) → str
      — YAML with column descriptions and built-in test declarations
    - write_model_files(project_dir, staging_models: list, mart_models: list) → None
      — write .sql files to correct subdirectories
    - run_dbt_command(project_dir, command: list[str]) → dict
      — subprocess wrapper: dbt run/test/compile; return {success, stdout, stderr}
  Main block: generate 2 staging models + 1 mart model for studybook Postgres schema,
    write files, run `dbt run`, check output

03_dbt_incremental_models.py
  Purpose: Incremental models — process only new/changed records, strategies, merge keys
  Key concepts: is_incremental() macro, unique_key, incremental_strategy (append vs merge
    vs delete+insert), late-arriving data handling
  Functions:
    - generate_incremental_model(name, source_ref, ts_column, unique_key,
        strategy="merge") → str
      — SQL with {% if is_incremental() %} block, config() with incremental_strategy
    - generate_late_arriving_handler(model_name, lookback_days=3) → str
      — incremental model that looks back N days to catch late data
    - compare_full_refresh_vs_incremental(project_dir, model_name) → dict
      — time both: dbt run --full-refresh vs dbt run; show duration + row counts
    - demonstrate_merge_strategy(project_dir, model_name) → None
      — insert new rows, update changed, skip unchanged; verify counts
    - get_model_run_results(project_dir) → list[dict]
      — parse run_results.json: show rows affected, timing per model
  Main block: create incremental model on a simulated events table, run initial load,
    insert 100 new events, run incremental, show only new rows processed

04_dbt_tests_and_documentation.py
  Purpose: dbt testing — schema tests, singular tests, custom macros, dbt docs
  Key concepts: built-in vs singular (custom SQL) tests, generic test macros,
    dbt docs generate/serve, lineage DAG
  Functions:
    - generate_singular_test(name, model, sql_assertion) → str
      — custom SQL test file: passes if returns 0 rows
    - generate_generic_test_macro(name, column_expression, config_args: dict) → str
      — reusable generic test: e.g., is_positive, is_valid_email
    - generate_documentation_block(model_name, model_description, columns: list[dict]) → str
      — docs block YAML with column-level descriptions
    - run_dbt_test(project_dir, model=None) → dict
      — run `dbt test`, parse results: {passed, failed, errors, test_details}
    - generate_dbt_docs(project_dir) → str
      — run `dbt docs generate`, return path to index.html
    - explain_test_strategies() → None
      — print: when to use schema tests vs singular tests vs Python tests (pytest)
  Main block: add 5 tests to existing mart model, run tests, show pass/fail,
    generate docs, print path

05_dbt_advanced_patterns.py
  Purpose: Advanced dbt — seeds, snapshots (SCD Type 2), macros, packages, hooks
  Key concepts: seeds for reference data, snapshots for CDC/SCD2,
    dbt packages (dbt-utils), pre/post hooks for audit
  Functions:
    - generate_seed_csv(name, data: list[dict]) → str — CSV content for dbt seed
    - generate_snapshot_model(name, source_ref, unique_key, strategy,
        updated_at_col=None, check_cols=None) → str
      — snapshot .sql file: track history using dbt snapshot (SCD Type 2)
    - generate_macro(name, args: list[str], sql_body: str) → str
      — Jinja macro file for reusable SQL logic
    - generate_packages_yml(packages: list[dict]) → str — packages.yml for dbt-utils etc.
    - generate_audit_hook(hook_type: str) → str
      — pre-hook: log run start to audit table; post-hook: log completion + row count
    - demonstrate_snapshot_run(project_dir, snapshot_name) → None
      — run initial snapshot, modify source data, run again, show history table
  Main block: create seed + snapshot + macro, run `dbt snapshot` twice with data changes,
    query snapshot table to show SCD2 history

===== CAPSTONE PROJECT =====

capstone/brief.md
  Title: Analytics Engineering Pipeline with dbt
  Scenario: The studybook Postgres database has raw tables (simulated IoT sensor readings
    and device registry). Build a dbt project that transforms raw → staging → marts,
    with full testing and documentation.
  What to build:
    - setup.py: create raw tables in Postgres (raw_sensor_readings: device_id, ts, value;
      raw_devices: device_id, name, location, type), insert 10k synthetic rows
    - dbt project (dbt_tutorial/): 
        staging/stg_sensors.sql — clean + rename raw columns
        staging/stg_devices.sql — deduplicate devices
        marts/hourly_sensor_agg.sql — incremental: hourly avg/min/max per device
        marts/device_summary.sql — join devices + latest sensor reading
    - schema.yml: unique/not_null tests on all key columns, documentation for all columns
    - snapshots/device_snapshot.sql — track device location changes over time
    - seeds/sensor_thresholds.csv — reference data for alert thresholds by device type
    - run_pipeline.py: orchestrate full dbt run with subprocess: seed → snapshot → run → test → docs
    - test_dbt_models.py: pytest — validate staging row counts, mart join correctness (query Postgres directly)

  Acceptance criteria:
    - dbt run succeeds with 0 errors
    - dbt test passes all schema tests
    - Incremental model processes only new rows on second run
    - Snapshot shows SCD2 history after a device location change
    - dbt docs generate completes and index.html exists

capstone/capstone.py — run_pipeline.py (as above)
capstone/test_capstone.py — test_dbt_models.py (as above)

===== INFRASTRUCTURE NOTES =====

Requires existing studybook_core Docker stack: postgres on localhost:5432
  db=studybook, user=studybook, password=studybook
Install: pip install dbt-postgres psycopg2-binary
dbt project written to /tmp/studybook/dbt_tutorial/ or DBT_PROJECT_DIR env var
profiles.yml written to /tmp/studybook/dbt_profiles/ or DBT_PROFILES_DIR env var
All Python files drive dbt via subprocess — they are orchestrators, not replacements for dbt.

===== START =====

Acknowledge these instructions, then wait for me to say "generate file 01".

===
