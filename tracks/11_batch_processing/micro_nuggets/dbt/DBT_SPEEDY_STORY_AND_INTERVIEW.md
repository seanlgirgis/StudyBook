# dbt Speedy Story and Interview Guide

A narrative journey from raw SQL chaos to production-grade dbt pipelines.
Read linearly for maximum retention, or jump to any chapter.

---

## Chapter 1: Why dbt? The Raw SQL Problem

Imagine you join a data team. Your predecessor left behind 47 SQL scripts.
Some are in Confluence, some in a shared drive, some in a Slack message from 2021.
Nobody knows what order to run them. One script overwrites another's table.
Tests? Nonexistent. Documentation? "Look at the SQL."

This is the raw SQL problem: analytics SQL has no engineering discipline.

dbt solves this by bringing software practices to SQL:
- Version control (git every SQL file)
- Dependency management (ref() builds the execution graph)
- Testing (schema.yml + tests/ enforce data contracts)
- Documentation (manifest.json + dbt docs generate + dbt docs serve)
- Environments (dev vs prod via profiles.yml)

dbt is NOT an orchestrator (like Airflow). It does not schedule jobs.
dbt is a TRANSFORMATION TOOL: you give it SELECT statements; it handles
the CREATE TABLE/VIEW, dependency ordering, and testing.

---

## Chapter 2: Your First dbt Project

A dbt project has one key file: `dbt_project.yml`. It declares:
- Project name and version
- Which directories contain models, seeds, tests, macros, snapshots
- Per-directory materialization defaults

A `profiles.yml` holds credentials (and lives OUTSIDE the project by convention,
at `~/.dbt/profiles.yml` — never committed to git).

Run `dbt debug` to validate both files and test DB connectivity.

Key separation: `dbt_project.yml` = WHAT (config, committed), `profiles.yml` = WHERE (credentials, secret).

In this lane, `_dbt_lane_connect.py` auto-generates `profiles.yml` by detecting
the best available backend (PostgreSQL → Snowflake → Databricks → DuckDB).

See: `01_dbt_basics/01_project_init_and_profiles.py`

---

## Chapter 3: Sources and Staging — The Foundation

Every dbt project has a staging layer. It is the ONLY place that calls `source()`.

`source('schema', 'table')` tells dbt:
- "This table was not built by dbt — it belongs to an external system."
- Enables freshness checks (`warn_after`, `error_after` in schema.yml).
- Generates a documented lineage edge from raw to first dbt layer.

`ref('model_name')` tells dbt:
- "This table WAS built by dbt — I depend on it."
- Creates a DAG edge → enforces execution order.
- Resolves the correct schema automatically (dev schema vs prod schema).

The staging layer rule: rename columns, cast types, lowercase emails. Nothing else.
No filtering. No business logic. No aggregations.
Downstream models rely on staging as a stable, clean foundation.

See: `01_dbt_basics/02_sources_and_staging.py`

---

## Chapter 4: ref() and the DAG — dbt's Superpower

Every `ref()` call creates a directed edge in the DAG (Directed Acyclic Graph).

```
stg_orders ──────────────────────────────► fct_orders
stg_customers ──► int_orders_with_customers (ephemeral) ──► fct_orders
dim_customers ───────────────────────────────────────────► fct_orders
```

dbt performs a topological sort on this graph. Models with no dependencies
run first. Models with dependencies wait for their parents.

You never think about "what order do I run these scripts?" dbt knows.

Graph operators for exploration:
- `+model` = model + all ancestors (upstream)
- `model+` = model + all descendants (downstream)
- `dbt ls --select +fct_orders` = show everything fct_orders depends on
- `dbt ls --select tag:daily` = show all models tagged 'daily'

See: `02_modeling_and_materializations/02_ephemeral_and_ref_graph.py`

---

## Chapter 5: Materializations — view, table, incremental, ephemeral

Materialization = HOW dbt writes results to the database.

**view**: SQL stored as a DB view. No data stored. Cheapest to build, slowest
to query (the SELECT runs every time downstream queries it). Use for staging.

**table**: DROP + CREATE TABLE AS SELECT. Full rebuild every run. Fast to query,
predictable. Use for dim tables and small-to-medium fact tables.

**incremental**: Only processes new/changed rows. Controlled by
`{% if is_incremental() %} WHERE event_ts > max(event_ts) {% endif %}`.
First run: full load. Subsequent runs: delta only.
Use for high-volume append-only tables (events, logs, clickstream).

**ephemeral**: Not materialized at all — inlined as a CTE inside the calling model.
Use for single-consumer intermediate logic you want to name for readability.

`on_schema_change` for incremental:
- `"ignore"`: new columns silently dropped (dangerous default)
- `"fail"`: errors if schema changes (safe)
- `"append_new_columns"`: adds new columns, NULLs old rows (production standard)
- `"sync_all_columns"`: adds and removes columns (risky)

See: `02_modeling_and_materializations/01_views_tables_incremental.py`

---

## Chapter 6: Testing — Trust Your Data

dbt tests are SELECT queries. A test FAILS if the SELECT returns ANY rows.

**Generic tests** (in schema.yml):
- `not_null`: column must have no NULLs
- `unique`: column values must all be distinct
- `relationships`: FK check — column values must exist in another table
- `accepted_values`: column values must be in a defined list

**Singular tests** (SQL files in tests/):
- You write the SQL; return violation rows
- Use for complex business rules generic tests can't express
- Example: `WHERE amount_cents <= 0` — catches zero-amount refunds

CI/CD pattern: `dbt build` (not `dbt run`) — build runs tests for each node
BEFORE its downstream dependents run. If staging tests fail, marts don't build.

See: `03_tests_and_quality/01_generic_tests.py` and `02_custom_tests...`

---

## Chapter 7: Snapshots — Tracking History

The SCD Type 2 problem: "What was Alice's tier in February?" requires history.

dbt snapshot automatically implements SCD Type 2:
- `dbt_valid_from`: when this version became active
- `dbt_valid_to`: when it ended (NULL = current version)
- `dbt_scd_id`: unique hash per historical row

Two strategies:
- `strategy='check'`: compare listed `check_cols`; any change creates a new row
- `strategy='timestamp'`: use an `updated_at` column; faster at large scale

Query for current state: `WHERE dbt_valid_to IS NULL`
Query for a point in time: `WHERE dbt_valid_from <= '2023-06-01' AND (dbt_valid_to > '2023-06-01' OR dbt_valid_to IS NULL)`

vs raw SQL MERGE SCD2: with dbt you define WHAT to track; dbt writes the MERGE.
With raw SQL you maintain the MERGE logic yourself — complex and error-prone.

See: `04_snapshots_and_scd/01_snapshots_scd2.py`

---

## Chapter 8: Operations — build, docs, CI/CD

**dbt run vs dbt build:**
`dbt run` executes model SQL only. `dbt build` = seed + run + test + snapshot
in DAG order, testing each node BEFORE its downstream runs. Use `dbt build` in CI.

**dbt docs generate** produces:
- `manifest.json`: full project graph (every node, SQL, config, dependencies)
- `catalog.json`: DB introspection (column names, types, row counts)
- `index.html`: interactive lineage UI (run `dbt docs serve`)

**manifest.json** is the artifact every dbt tool reads:
- dbt Cloud (scheduling, IDE, Explorer)
- elementary (data quality monitoring)
- Lightdash, Looker, Metabase (BI with lineage)
- CI/CD for `state:modified` comparison

**run_results.json**: per-node execution status + timing. Parse this for alerts:
"Any model took > 5 minutes → page on-call."

See: `05_operations_and_deploy/01_run_build_seed_docs.py`

---

## Chapter 9: Selectors and State — Production Efficiency

Without selectors: `dbt build` runs ALL 200 models every CI push. Expensive.

With `state:modified+`:
```bash
dbt build --select state:modified+ --state ./prod_manifest/
```
Only changed models + their downstream dependents rebuild. 2-hour CI → 10 minutes.

**State workflow:**
1. Every successful prod run uploads `manifest.json` as a CI artifact
2. Next CI run downloads that artifact as `./prod_manifest/manifest.json`
3. `state:modified+` compares current manifest vs prod manifest
4. Only changed nodes rebuild

**defer**: `dbt run --select my_model --defer --state ./prod_manifest/`
For unchanged upstream deps, uses PROD tables instead of rebuilding in dev.
If you changed only `fct_orders.sql`, dbt uses prod's `stg_customers` etc.

**Common selector patterns:**
- `tag:daily` — daily rebuild models only
- `+dim_customers` — dim_customers and all ancestors
- `source:dbt_lab_raw+` — everything downstream of raw sources
- `state:new` — models that didn't exist in previous manifest

See: `05_operations_and_deploy/02_selectors_state_artifacts.py`

---

## Chapter 10: The Medallion Architecture Mini-Capstone

The medallion architecture divides data into quality zones:

**Bronze (brz_)**: Raw data preserved exactly. Minimal filtering. View or table.
"Never lose the original; always able to reprocess."

**Silver (slv_)**: Cleaned, standardized, deduplicated. Business rules applied.
Enriched with dimension attributes. Table (frequently read by gold).
"Trusted source; not yet aggregated."

**Gold (gld_)**: Pre-aggregated, denormalized, BI-ready. Table always.
"Final answer for the dashboard."

dbt lineage in this lane:
```
stg_orders → brz_raw_orders → slv_orders_cleaned → gld_order_summary
                                     ↑
                               stg_customers
```

Why medallion beats one big query:
- Debug each layer independently
- Multiple gold tables can share one silver model
- Silver can be materialized (fast for gold to read)
- Clear separation of concerns in dbt docs

See: `07_mini_capstone/01_mini_capstone.py`

---

## Interview Fast Track: Top 15 Q&A

**Q1. What is dbt and what problem does it solve?**
dbt (data build tool) is a transformation framework that turns raw SQL SELECT statements into a fully-orchestrated, tested, documented data pipeline. It solves the "raw SQL chaos" problem: analysts run ad-hoc scripts with no dependency management, no tests, no documentation, and no version control. dbt brings software engineering practices to analytics engineering.

**Q2. What is the dbt DAG and why does it matter?**
The DAG (Directed Acyclic Graph) is the execution dependency graph dbt builds from ref() calls. Each ref() creates a directed edge. dbt topologically sorts the DAG so models run in the correct order automatically — no manual script orchestration. The DAG also enables impact analysis and state-based CI/CD.

**Q3. What is the difference between ref() and source()?**
ref('model_name') references another dbt model — generates the correct schema-qualified name at runtime and creates a DAG dependency. source('schema', 'table') references an external/raw table not owned by dbt. Rule: use source() ONLY in the staging layer; use ref() everywhere else.

**Q4. When would you choose incremental over table materialization?**
Use incremental when: (1) the table is large (millions+ rows), (2) data is append-only with a clear watermark column, and (3) rebuilding from scratch is too expensive. Use table when data is small enough to rebuild cheaply, or when historical corrections happen frequently. Incremental saves cost; table guarantees correctness.

**Q5. What are the four on_schema_change options for incremental models?**
"ignore": new columns silently dropped. "fail": dbt errors on schema change. "append_new_columns": new columns added, old rows get NULL. "sync_all_columns": adds new and removes old columns (risky). In production, "append_new_columns" is the safest for additive changes.

**Q6. What is a dbt snapshot and how does it differ from a SCD2 MERGE?**
A dbt snapshot automatically implements SCD Type 2 — it adds dbt_valid_from, dbt_valid_to, dbt_scd_id. strategy='check' detects changes by comparing column values; strategy='timestamp' uses updated_at. vs MERGE SCD2: with dbt you define WHAT to track; dbt writes the MERGE logic, integrates with DAG and docs, and is idempotent.

**Q7. What is the difference between dbt run, dbt test, and dbt build?**
dbt run executes model SQL only. dbt test runs all tests. dbt build = seed + run + test + snapshot in DAG order, testing each node BEFORE its downstream dependents run. Use dbt build in CI/CD for maximum safety.

**Q8. What are the four built-in generic tests in dbt?**
not_null (no NULLs), unique (no duplicates), relationships (FK check — values exist in parent table), accepted_values (enum check — values within allowed set). Defined in schema.yml; dbt auto-generates the SQL.

**Q9. What is a singular test and when do you use it?**
A singular test is a SQL file in tests/ that selects violation rows — any rows returned = fail. Use for business-logic assertions generic tests can't express: "no payment exceeds order total", "no two active subscriptions per user". Use ref() so tests work across dev/prod schemas.

**Q10. How does dbt handle dev vs prod environments?**
Profiles.yml defines multiple targets (dev, prod). In dev, dbt appends username to schema (dbt_lab_your_name) preventing overwriting prod. ref() resolves to current target's schema automatically. Use --target prod in CI/CD. Use env_var() for dynamic credentials.

**Q11. What is manifest.json and why is it critical for CI/CD?**
manifest.json is a JSON artifact generated by every dbt compile/run/build. It contains every node with compiled SQL, configuration, tags, and DAG dependencies. CI/CD tools use it for state:modified comparison. All observability tools (elementary, Lightdash, re_data) read it for lineage. Always store as a CI artifact.

**Q12. Explain state:modified and when to use it in CI/CD.**
state:modified compares current manifest to a previous one (last prod run). Only models whose SQL/config changed are selected. `dbt build --select state:modified+ --state ./prod_manifest/` runs changed + downstream. On large projects: 2-hour CI → 10 minutes. Requires storing manifest.json as artifact after each successful prod run.

**Q13. What is a dbt macro and when would you create one?**
A macro is a Jinja2 function in macros/ callable from any model. Use for: repeated SQL patterns (cents_to_dollars, generate_surrogate_key), cross-database compatibility, dynamic SQL. Built-in macros: ref(), source(), this, is_incremental(). Third-party: dbt-utils. Macros compile at parse time.

**Q14. What are the pros and cons of dbt Cloud vs dbt Core?**
dbt Core (open source): free, runs anywhere, full features. Cons: you manage orchestration, no IDE, no job scheduler. dbt Cloud: built-in IDE, scheduler, CI integration, state management, SSO, Explorer. Cons: paid for most features, vendor lock-in. Most small teams: Core + GitHub Actions. Enterprise: Cloud for governance.

**Q15. How would you optimize a dbt project that takes 4 hours to run?**
(1) state:modified+ in CI to only rebuild changed models. (2) Find slowest models via run_results.json; optimize SQL. (3) Convert large table materializations to incremental where append-safe. (4) Increase threads (threads: 8+) for parallelism. (5) Use defer in dev. (6) Partition large incrementals by date. (7) Remove unused wide columns to reduce bytes scanned.
