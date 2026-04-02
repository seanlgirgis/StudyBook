# Interview Questions — dbt Patterns

> Topics covered: models (staging/intermediate/marts) · incremental models · dbt tests · snapshots · sources and freshness
> Levels: Starter | Mid | Senior | Architect

---

## Topic 1: Models — Staging, Intermediate, and Marts

**Q1 (Starter): In c001_models_demo.py, raw orders have inconsistent date formats, mixed-case status values, and dollar-sign amounts. Which dbt layer is responsible for fixing these issues, and why?**
What a good answer covers:
- The staging layer is the normalization boundary — it cleans, casts, and renames raw source columns without adding business logic
- Fixing formats at staging (as `_normalize_date` and `_parse_amount` do in the demo) means every downstream model inherits clean, typed data
- Staging models are named `stg_<source>__<entity>` by convention to signal their role
Why this is asked: Tests whether the candidate understands that cleaning belongs at the layer closest to the source, not scattered across marts.

**Q2 (Starter): What is the purpose of the intermediate layer in the dbt model hierarchy shown in c001_models_demo.py?**
What a good answer covers:
- Intermediate models join and reshape data from one or more staging models into business-meaningful entities
- They isolate complex transformation logic so mart models stay simple and readable
- Intermediate models are typically ephemeral or materialized as views; they are not intended for direct consumption by analysts
Why this is asked: Many candidates skip the intermediate layer and put join logic directly in marts — this question checks awareness of the three-layer pattern.

**Q3 (Starter): Why would a mart model reference a staging model's cleaned `customer_id` field rather than the raw `CustID` field from the source?**
What a good answer covers:
- The raw `CustID` in c001_models_demo.py has inconsistent casing and trailing spaces (e.g., `" c01 "`, `"C02"`)
- Referencing the cleaned field ensures the mart always works with a consistent, trusted key
- Bypassing staging would silently propagate data quality issues into production dashboards
Why this is asked: Confirms the candidate understands why the staging contract exists — data consumers should never touch raw fields.

**Q4 (Starter): In c001_models_demo.py, `_parse_amount` returns `0.0` when the raw amount is `None`. Is this the right behavior for a staging model? What alternative would you consider?**
What a good answer covers:
- Replacing `None` with `0.0` in staging changes the meaning of missing data — a null amount and a zero amount are different business facts
- A better staging approach is to preserve `NULL` and let a mart or metric layer apply business rules (e.g., exclude nulls, default to zero, flag for review)
- If coalescing to zero is the correct business rule, that decision should be documented and belong in the intermediate or mart model, not silently applied in staging
Why this is asked: Tests whether the candidate thinks about semantic correctness versus mechanical cleaning.

---

**Q5 (Mid): c001_models_demo.py shows raw orders with multiple date formats being normalized by `_normalize_date`. How would you implement this in a dbt staging model, and how would you test that normalization is correct?**
What a good answer covers:
- In dbt SQL, use `TRY_TO_DATE` (Snowflake) or `SAFE.PARSE_DATE` (BigQuery) with multiple format masks, or cast after a regex normalization using a macro
- Write a dbt test using `dbt-utils.expression_is_true` to assert that `order_date IS NOT NULL` and matches the `YYYY-MM-DD` pattern after staging
- Add a singular test that checks for any remaining non-standard dates in the staging output
Why this is asked: Bridges the demo's Python normalization logic to the SQL and testing practices used in real dbt projects.

**Q6 (Mid): When should a model be materialized as a `view`, a `table`, or an `incremental` model in the dbt layer hierarchy?**
What a good answer covers:
- Staging models: views — they are cheap queries over the source, and freshness is handled by the source layer
- Intermediate models: views or ephemeral — they add no materialization cost and are consumed only by other models
- Mart models: tables — analysts and BI tools query them directly; materializing avoids repeated expensive joins at query time
- Incremental models: for large fact tables where full rebuilds are too slow; only new or changed rows are appended or merged
Why this is asked: Materialization strategy is a fundamental dbt configuration decision with performance and cost implications.

**Q7 (Mid): How does dbt's `ref()` function enforce layer boundaries and enable lineage tracking?**
What a good answer covers:
- `ref('model_name')` resolves to the compiled schema and table name of another dbt model, creating an explicit dependency in the DAG
- dbt uses these dependencies to determine build order and to generate the lineage graph visible in dbt docs
- Using `ref()` instead of hardcoded table names means the correct environment (dev, staging, prod) is always targeted without manual changes
- It prevents mart models from accidentally querying raw source tables by making the dependency explicit and auditable
Why this is asked: `ref()` is the core mechanism of dbt's dependency and lineage system.

**Q8 (Mid): In a project following the c001_models_demo.py pattern, an analyst team wants to add a custom revenue calculation to a mart. They propose modifying the staging model directly. Why is this wrong, and what should they do instead?**
What a good answer covers:
- Staging models are shared contracts used by multiple downstream models — modifying them changes outputs for all consumers, not just the requesting team
- Business logic belongs in intermediate or mart models where it is scoped to the consuming use case
- The analyst team should create a new mart model (or extend an existing one) that references the staging model and adds the custom calculation there
- This keeps staging stable and auditable; changes to mart logic do not break other consumers
Why this is asked: Layer discipline is frequently violated in practice — this tests whether the candidate can articulate and defend the boundary.

---

**Q9 (Senior): A staging model in the c001_models_demo.py pattern is becoming a bottleneck — every mart model queries it, and it re-reads the raw source table each time. How do you address this without violating the layer pattern?**
What a good answer covers:
- Materialize the staging model as a `table` or `incremental` instead of a `view`; this caches the cleaned output and all downstream marts read from the materialized result
- If the source table is large, convert the staging model to incremental using a `unique_key` and `is_incremental()` guard so only new rows are processed each run
- Add a `post-hook` to run `ANALYZE` or update statistics after the staging table is refreshed, so the query planner has accurate cardinality estimates for downstream joins
- Avoid duplicating staging logic into an intermediate model just to work around the performance issue — fix the materialization instead
Why this is asked: Production performance tuning within the dbt layer model is a senior concern.

**Q10 (Senior): How would you handle a source table in c001_models_demo.py that changes its schema without notice — for example, a new column appears or an existing column is renamed?**
What a good answer covers:
- Define the source schema explicitly in `sources.yml` with column-level descriptions; dbt's `source` freshness and schema contracts flag unexpected changes
- Use `dbt-contracts` or dbt's built-in `contract` enforcement (dbt 1.5+) to assert that column names and types match the declared schema on each run
- Add a CI step that diffs the compiled staging model SQL against the prior version to detect column reference changes before deployment
- In the staging model, alias raw column names to stable output names (`CustID as customer_id`) so downstream models are insulated from upstream renames
Why this is asked: Source schema instability is one of the most common causes of silent data pipeline failures.

**Q11 (Senior): Describe how you would implement a slowly changing dimension (SCD Type 2) for customer data in the dbt staging/intermediate/mart pattern from c001_models_demo.py.**
What a good answer covers:
- Use a dbt snapshot (c004_snapshots_demo.py) on the raw customer source to track historical changes with `dbt_valid_from` and `dbt_valid_to` columns
- Create a staging model that selects from the snapshot table, normalizing column names and types
- In the intermediate layer, join the snapshot-backed customer staging model to orders on both `customer_id` and the date range so each order gets the customer attributes that were current at the time of the order
- The mart model surfaces the current customer record by filtering `dbt_valid_to IS NULL`, or exposes the full history for audit queries
Why this is asked: SCD Type 2 implementation spans multiple dbt features and tests whether the candidate can connect the layer pattern to snapshot mechanics.

---

**Q12 (Architect): Your organization has 50 teams each building their own dbt marts. Source models like those in c001_models_demo.py are being duplicated across projects. Design a shared data platform model governance strategy.**
What a good answer covers:
- Establish a central "foundation" dbt project that owns all staging and shared intermediate models; publish it as a dbt package or mesh node that downstream projects consume via `ref()` cross-project references
- Use dbt Mesh's `access` and `group` controls to declare which models are public contracts vs. internal implementation details
- Require that all staging models pass a standard test suite (not-null, unique, accepted values) before being promoted to the public contract catalog
- Connect to data quality track: instrument each staging model with dbt Artifacts (manifest.json, run_results.json) forwarded to a data observability tool so lineage and test results are centrally visible
- Govern schema changes through a pull-request process with required reviews from the data platform team before public models are altered
Why this is asked: Multi-team dbt governance is an architect-level organizational and technical design problem.

**Q13 (Architect): How would you design the dbt model layer (staging/intermediate/marts) to support both a real-time BI dashboard and a daily batch analytics use case, sharing as much transformation logic as possible?**
What a good answer covers:
- Staging and intermediate models remain shared — both use cases consume the same normalized, joined entities
- For the real-time dashboard: materialize key intermediate models as Delta/Iceberg tables with streaming appends (via Spark or Flink) and expose them through a mart view with minimal additional transformation
- For batch analytics: the daily mart runs a full incremental refresh on top of the same intermediate models, adding heavier aggregations not needed in real time
- Use dbt's `config(enabled=...)` or environment variables to conditionally enable real-time vs batch materialization strategies per environment
- Connect to orchestration track: schedule the batch marts in a separate DAG downstream of the streaming intermediate refresh so the batch always reads the latest streamed data, not stale snapshots
Why this is asked: Bridging real-time and batch on a shared dbt model graph is an architect-level design challenge.

---

## Topic 2: Incremental Models

**Q1 (Starter): What problem does an incremental dbt model solve compared to a standard table model?**
What a good answer covers:
- A full table model rebuilds all rows from scratch on every run — expensive and slow for large fact tables
- An incremental model processes only new or changed rows since the last run, appending or merging them into the existing table
- This dramatically reduces run time and compute cost for tables that grow continuously (e.g., orders, events, logs)
Why this is asked: Incremental models are the most important performance optimization in dbt for large datasets.

**Q2 (Starter): In c002_incremental_models_demo.py, how does the `is_incremental()` macro determine which rows to process on each run?**
What a good answer covers:
- `is_incremental()` returns `True` only when the target table already exists and the run is not a `--full-refresh`
- Inside the `WHERE` clause, the model uses `is_incremental()` to filter source rows to only those newer than the maximum value of a timestamp column in the existing target table
- On the first run, `is_incremental()` is `False` and all rows are loaded; on subsequent runs, only the delta is processed
Why this is asked: The `is_incremental()` pattern is the core mechanic every dbt user must understand.

**Q3 (Starter): What does `unique_key` do in an incremental dbt model configuration?**
What a good answer covers:
- `unique_key` tells dbt which column (or set of columns) uniquely identifies a row in the target table
- When new rows arrive with a `unique_key` that already exists in the target, dbt performs an upsert (MERGE) rather than a plain INSERT
- Without `unique_key`, re-processed rows would create duplicates; with it, the latest version of each row replaces the old one
Why this is asked: `unique_key` is the mechanism that makes incremental models safe for updates, not just appends.

**Q4 (Starter): When would you run `dbt run --full-refresh` on an incremental model, and what does it do?**
What a good answer covers:
- `--full-refresh` drops and rebuilds the target table from scratch, ignoring the `is_incremental()` guard
- Use it when the model logic changes in a way that requires reprocessing historical data (e.g., a new column was added, a filter condition changed)
- Also use it when the incremental state is suspected to be corrupted or when the lookback window has drifted too far from the source
Why this is asked: `--full-refresh` is a critical operational concept — candidates must know when it is necessary and what its cost is.

---

**Q5 (Mid): c002_incremental_models_demo.py uses the max timestamp of the target table as the incremental filter boundary. What are the failure modes of this approach, and how would you make it more robust?**
What a good answer covers:
- Late-arriving data: rows with timestamps older than the current max are silently excluded; fix by using a lookback window (e.g., `WHERE event_ts >= max_ts - INTERVAL 3 DAY`)
- Clock skew: source systems with unsynchronized clocks may generate rows with timestamps slightly behind the max, causing missed rows; the lookback window also mitigates this
- Null timestamps: rows with `NULL` event_ts fail the comparison and are excluded forever; add an explicit null check or coalesce to a sentinel date
- Reprocessed source data: if the source retroactively updates old rows, the incremental filter misses them; a `unique_key` merge handles updates but only for re-ingested rows
Why this is asked: Incremental model correctness at the edge cases is a key mid-level concern.

**Q6 (Mid): What is the difference between the `append`, `merge`, `delete+insert`, and `insert_overwrite` incremental strategies in dbt?**
What a good answer covers:
- `append`: new rows are inserted without any deduplication — fastest but creates duplicates if rows are reprocessed
- `merge`: uses `MERGE INTO` SQL to upsert rows matching `unique_key` and insert new ones — correct for updates, requires warehouse MERGE support
- `delete+insert`: deletes existing rows that match the new batch's keys, then inserts the new batch — equivalent to merge but works on warehouses without native MERGE
- `insert_overwrite`: replaces entire partitions at once — efficient for partition-aligned incremental loads (e.g., overwrite yesterday's partition) but requires partitioning by the incremental key
Why this is asked: Strategy selection depends on warehouse, data volume, and update patterns — a mid-level engineer must know all four options.

**Q7 (Mid): How do you test that an incremental dbt model is not creating duplicate rows over time?**
What a good answer covers:
- Add a `unique` test on the `unique_key` column in `schema.yml`; dbt runs this after every model build and fails if duplicates are found
- For append-only models without a `unique_key`, use `dbt-utils.expression_is_true` to assert row counts match expectations, or use a custom singular test that counts duplicates
- Run `dbt test --select <model>` after every incremental run in CI to catch regressions immediately
- Monitor row count deltas between runs using dbt's `store_failures` option so unexpected spikes (which often indicate duplicate inserts) are visible in the results table
Why this is asked: Incremental model correctness is hard to verify visually — testing discipline is essential.

**Q8 (Mid): An incremental model in c002_incremental_models_demo.py has been running for a year. The source table has changed its primary key structure. How do you safely migrate the incremental model?**
What a good answer covers:
- A primary key change means existing rows in the target table may not match new rows on the new key — a plain incremental run will create duplicates or miss updates
- Safe migration path: update the model SQL and `unique_key` config, then run `dbt run --full-refresh` to rebuild from scratch using the new key structure
- Schedule the `--full-refresh` during a maintenance window and communicate downstream impact (the table is unavailable during rebuild)
- After rebuild, verify with a `unique` test on the new key and a row count check against the source
Why this is asked: Schema evolution in incremental models is a common operational challenge.

---

**Q9 (Senior): A high-volume incremental model processes 100 M rows per day. The merge step is taking 45 minutes. Walk through your optimization approach.**
What a good answer covers:
- Check whether the `unique_key` column is indexed or clustered in the target warehouse — without it, the MERGE must scan the entire target table for each matching key
- Cluster or partition the target table on the `unique_key` so the MERGE only scans relevant micro-partitions (Snowflake) or partitions (BigQuery, Delta)
- Reduce the merge scope by narrowing the incremental filter to the minimum necessary window (e.g., yesterday only rather than last 7 days)
- Switch strategy from `merge` to `insert_overwrite` if data is naturally partition-aligned — overwriting whole partitions is faster than row-level merging
- Consider pre-aggregating or deduplicating the incoming batch before the merge to reduce the number of rows that must be matched
Why this is asked: Incremental merge performance tuning is a senior operational skill.

**Q10 (Senior): How would you implement a reliable late-arriving data strategy for an incremental model that ingests order events from c002_incremental_models_demo.py, where orders can be updated up to 30 days after creation?**
What a good answer covers:
- Use a 30-day lookback window in the incremental filter: `WHERE updated_at >= (SELECT MAX(updated_at) FROM {{ this }}) - INTERVAL 30 DAY`
- Use `unique_key = 'order_id'` with `merge` strategy so updated rows replace old ones rather than appending duplicates
- Partition the target table by `order_date` and use `insert_overwrite` with a 30-day partition range as an alternative — replace 30 days of partitions each run instead of merging row by row
- Document the 30-day SLA in the model's `description` and add a dbt test that flags orders last updated more than 30 days ago as a data quality warning
Why this is asked: Late-arriving data handling is a real-world requirement that distinguishes senior engineers.

**Q11 (Senior): Describe how you would use dbt's incremental model pattern alongside Spark (c002_incremental_models_demo.py style) in a medallion architecture (bronze/silver/gold).**
What a good answer covers:
- Bronze: raw ingestion via Spark Structured Streaming or batch, writing to a Delta table with append-only — no dbt involvement at this layer
- Silver: dbt incremental model reads from the Bronze Delta table using an `is_incremental()` filter on the ingestion timestamp, applies cleaning and normalization (mirroring c001_models_demo.py staging), and merges into a Silver Delta table
- Gold: dbt mart models read from Silver, apply business-logic aggregations, and write to Gold tables materialized as full tables or incremental with partition overwrite
- The Spark job handles heavy IO and format conversion; dbt handles SQL transformation logic and test governance — each does what it is best at
Why this is asked: Combining Spark ingestion with dbt transformation in a medallion architecture is a common modern ELT pattern.

---

**Q12 (Architect): Design an incremental model strategy for a platform that processes 500 GB of new data daily across 200 dbt models, some of which depend on each other incrementally.**
What a good answer covers:
- Classify models into tiers: high-frequency staging (incremental, append), mid-frequency intermediate (incremental with merge), low-frequency mart (full table or partition overwrite)
- Use dbt's `--select` and `--exclude` flags with orchestration (Airflow, Prefect) to run model tiers in dependency order, respecting DAG topology
- For incremental chains (model A feeds model B feeds model C), ensure each model's incremental filter references the upstream model's `updated_at` watermark, not the original source — otherwise staleness propagates incorrectly
- Implement a run metadata table that logs each model's last successful run timestamp; use this for audit and to detect incremental drift
- Connect to orchestration track: use Airflow sensors to gate downstream incremental runs until upstream runs complete, preventing a downstream model from reading a partially-refreshed upstream
Why this is asked: Multi-model incremental dependency management is an architect-level orchestration and design problem.

**Q13 (Architect): Your data platform needs to support both daily batch incremental dbt runs and ad hoc analyst queries that must always see the latest data. How do you design the incremental model refresh strategy to satisfy both requirements?**
What a good answer covers:
- Materialize core intermediate models as Delta or Iceberg tables with micro-batch streaming appends (Spark or Flink) so they are continuously fresh
- Batch incremental dbt mart models run on a schedule, reading from the always-fresh intermediate tables — they are slightly behind real time but consistent
- For analysts who need truly current data, expose the intermediate Delta tables directly through a query engine (e.g., Trino, Athena, Spark SQL) with a disclaimer that these are not governed mart tables
- Implement a two-table pattern per mart: a `_current` view that queries the live intermediate table and a `_daily` table that is the governed incremental mart — analysts choose based on freshness vs governance needs
- Connect to sources and freshness track: configure dbt source freshness checks on the intermediate tables so the orchestrator knows when to trigger the batch mart refresh
Why this is asked: Balancing real-time freshness with governed batch processing is an architect-level data platform design decision.

---

## Topic 3: dbt Tests

**Q1 (Starter): In c003_dbt_tests_demo.py, the orders data contains a duplicate `order_id` and a null `completed_at` timestamp. What built-in dbt tests would catch each of these issues?**
What a good answer covers:
- `unique` test on `order_id` catches the duplicate row (`order_id: "1002"` appears twice in the demo data)
- `not_null` test on `completed_at` catches the row where `completed_at` is `None`
- These are two of dbt's four generic tests (also `accepted_values` and `relationships`), defined in `schema.yml`
Why this is asked: The four generic tests are the first thing every dbt user learns; applying them to specific demo data confirms practical understanding.

**Q2 (Starter): What is the difference between a generic dbt test and a singular dbt test?**
What a good answer covers:
- Generic tests are reusable test macros applied to any column via `schema.yml` (e.g., `unique`, `not_null`, `accepted_values`, `relationships`)
- Singular tests are one-off SQL queries written as `.sql` files in the `tests/` directory that return rows when the test fails
- Singular tests are used for custom business rules that cannot be expressed as a generic macro (e.g., "the sum of refund amounts must not exceed total revenue")
Why this is asked: Distinguishing the two test types is fundamental dbt knowledge.

**Q3 (Starter): How does dbt run tests, and what does a test failure mean in practice?**
What a good answer covers:
- `dbt test` compiles each test into a SQL query; if the query returns any rows, the test fails (for generic tests, rows = violations)
- A failure exits with a non-zero code, which causes a CI job to fail or an orchestrator to alert
- By default, failed tests do not stop downstream model runs unless `--fail-fast` is set or the orchestrator gates on test results
Why this is asked: Understanding the test execution model — SQL queries that return violating rows — is essential for writing and debugging tests.

**Q4 (Starter): In c003_dbt_tests_demo.py, one order references `customer_id: "C99"` which does not exist in the customers table. Which dbt test catches this, and how is it configured?**
What a good answer covers:
- The `relationships` test checks referential integrity: every value in the foreign key column must exist in the referenced table's primary key column
- Configuration in `schema.yml`: `- relationships: {to: ref('stg_customers'), field: customer_id}`
- This test compiles to a `LEFT JOIN` with a `WHERE ... IS NULL` clause that returns orphaned foreign key values
Why this is asked: The `relationships` test is the most commonly misunderstood of the four generic tests.

---

**Q5 (Mid): c003_dbt_tests_demo.py shows that a null `completed_at` value slips through into the orders model. How would you configure a dbt test to warn on nulls rather than fail hard, and when would you prefer a warning over a failure?**
What a good answer covers:
- Set `config: {severity: warn}` on the `not_null` test in `schema.yml` — dbt logs the failure but exits with code 0
- Warnings are appropriate when nulls are expected for certain record states (e.g., an in-progress order legitimately has no `completed_at`) and hard failures would cause false alarms
- Use `where: "status = 'completed'"` as a test filter so the `not_null` test only applies to completed orders, making it a true failure rather than a warning
Why this is asked: Test severity configuration is a mid-level dbt skill; knowing when to warn vs fail requires business context judgment.

**Q6 (Mid): How would you test that the revenue totals in a mart model built on c003_dbt_tests_demo.py data are consistent with the source — i.e., no amounts are silently dropped or doubled during transformation?**
What a good answer covers:
- Write a singular test that compares `SUM(amount_usd)` in the mart model against `SUM(amount_usd)` in the staging model, asserting the difference is within a tolerance (e.g., zero for exact match)
- Use `dbt-utils.equality` or `dbt-utils.expression_is_true` to assert aggregate values match between layers
- Also add a row count assertion: the mart should not have fewer rows than the source (unless intentional deduplication occurred)
Why this is asked: Reconciliation tests between layers are essential for catching silent data loss, a frequent production bug.

**Q7 (Mid): What is `store_failures` in dbt, and why is it useful in a production environment?**
What a good answer covers:
- When `store_failures: true` is set on a test (or globally), dbt writes the failing rows from each test into a table in the database (`<schema>_dbt_test__audit.<test_name>`)
- This allows data engineers and analysts to query the exact rows that failed a test without re-running the pipeline
- In production, this is invaluable for triaging data quality issues quickly — you can immediately see which customers or orders triggered a `not_null` or `relationships` failure
Why this is asked: `store_failures` is a production observability feature that separates teams with mature data quality practices.

**Q8 (Mid): How does `dbt-utils` extend the built-in generic tests, and what are three commonly used `dbt-utils` tests?**
What a good answer covers:
- `dbt-utils` is an open-source package providing additional generic tests, macros, and cross-database SQL functions
- Commonly used tests: `expression_is_true` (assert a SQL expression is true for all rows), `unique_combination_of_columns` (composite uniqueness check), `not_constant` (assert a column has more than one distinct value)
- Also useful: `recency` (assert the most recent record is within a time window — directly relevant to c005_sources_freshness_demo.py) and `accepted_range` (assert numeric values fall within bounds)
Why this is asked: Knowing `dbt-utils` tests shows the candidate operates beyond the default four and has practical experience with real project test suites.

---

**Q9 (Senior): The c003_dbt_tests_demo.py dataset has a duplicate order (order_id "1002" appears twice). Describe how you would build a dbt test suite that detects this at the source, prevents it from entering the staging model, and alerts if it reaches the mart.**
What a good answer covers:
- At the source: add a `unique` test on the raw source in `sources.yml` so dbt flags duplicates before any transformation runs — use `severity: warn` if the source is known to occasionally produce duplicates
- In the staging model: deduplicate using `ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY updated_at DESC) = 1` and add a `unique` test on the staging output with `severity: error` to guarantee the contract
- In the mart: add a `unique` test on `order_id` and a row count singular test comparing the mart to a deduplicated staging CTE — if they diverge, a duplicate slipped through
- Instrument `store_failures: true` at the mart level so violating rows are persisted for triage
Why this is asked: Multi-layer deduplication testing strategy is a senior data quality design skill.

**Q10 (Senior): How would you integrate dbt tests into a CI/CD pipeline to prevent bad data models from reaching production?**
What a good answer covers:
- In the CI job: run `dbt build --select state:modified+` to build only changed models and their downstream dependents, then run `dbt test --select state:modified+` to test them
- Use dbt's `--defer` flag with a production manifest to resolve unmodified upstream models from production rather than rebuilding the full graph in CI
- Gate the pull request merge on CI test success: any `error`-severity test failure blocks deployment
- For slow-running tests, split the CI suite: generic tests run on every PR; expensive singular reconciliation tests run nightly
- Connect to data quality track: publish `run_results.json` from CI to a data observability tool so test trend analysis is available across all runs, not just the latest
Why this is asked: CI/CD integration for dbt tests is a senior DevOps-meets-data-engineering skill.

**Q11 (Senior): You are onboarding a legacy analytics codebase with no dbt tests. Describe your prioritization strategy for adding tests to 150 existing models.**
What a good answer covers:
- Start with the highest-impact layer: add `unique` and `not_null` tests to all primary keys in staging models — these catch the most fundamental data quality issues across all downstream consumers
- Second priority: add `relationships` tests on all foreign keys between staging models — orphaned keys are a common silent failure
- Third: add `accepted_values` tests on status/type columns that drive business logic (e.g., `status` in c003_dbt_tests_demo.py) to catch unexpected enumeration values from source systems
- Fourth: add singular reconciliation tests on the top five mart models used by the most dashboards — these catch aggregate-level errors that matter most to stakeholders
- Track test coverage as a metric (models with at least one test / total models) and set a team goal to improve it each sprint
Why this is asked: Prioritizing a test backlog is a senior operational and stakeholder management challenge.

---

**Q12 (Architect): Design a data quality framework built on dbt tests for a regulated industry (e.g., financial services) where data quality failures must be audited, escalated, and remediated with full traceability.**
What a good answer covers:
- Use `store_failures: true` globally so all test failures persist to audit tables with timestamps, model names, and violating row keys
- Classify tests by severity and business impact: critical tests (PII completeness, regulatory reference integrity) fail the pipeline and page on-call; warning tests log to a quality dashboard for review
- Publish `run_results.json` and `manifest.json` after every dbt run to a data observability platform (e.g., Monte Carlo, Bigeye) or a custom dashboard built on the audit tables — connect to data quality track
- Implement a remediation workflow: when a critical test fails, a ticket is auto-created in the issue tracker with the failing rows, the model lineage, and the owning team; SLA timers start automatically
- For auditors: provide a queryable history of all test results per model per run with links to the `store_failures` tables — this satisfies audit requirements for data provenance and quality attestation
Why this is asked: Regulated data quality governance is an architect-level design problem that spans tooling, process, and compliance.

**Q13 (Architect): How would you design a cross-project dbt test strategy in a dbt Mesh environment where dozens of teams own different domains, each with their own dbt project, but data flows between domains?**
What a good answer covers:
- Define public model contracts in each domain project using dbt's `contract: {enforced: true}` — the schema (column names and types) is guaranteed and tested on every build
- For cross-domain `relationships` tests: use cross-project `ref()` to reference the upstream domain's public model; the test validates referential integrity across the domain boundary
- Establish a platform-owned "contract registry" project that imports all public models and runs a nightly integration test suite asserting cross-domain consistency (row counts, key overlap, aggregate reconciliation)
- Gate public model promotions (contract changes) on a review process requiring the downstream domain teams' approval — breaking contract changes trigger a deprecation workflow, not immediate deletion
- Connect to orchestration track: use a platform-level Airflow DAG that runs the integration test suite after all domain dbt jobs complete, surfacing cross-domain quality issues before they reach the BI layer
Why this is asked: Cross-domain test governance in a federated dbt Mesh is an emerging architect-level challenge as organizations scale their data mesh adoption.

---

## Topic 4: Snapshots

**Q1 (Starter): What is a dbt snapshot, and what problem does it solve that a standard model cannot?**
What a good answer covers:
- A snapshot captures the state of a source table at a point in time and tracks how rows change over time by adding `dbt_valid_from` and `dbt_valid_to` columns
- Standard models always reflect the current state of source data — they overwrite previous values on each run
- Snapshots enable slowly changing dimension (SCD Type 2) history: you can query what a customer's address or status was on any past date
Why this is asked: Snapshots solve a specific historical tracking problem — candidates must state the problem before explaining the solution.

**Q2 (Starter): In c004_snapshots_demo.py, what does the `updated_at` strategy tell dbt to watch for?**
What a good answer covers:
- The `updated_at` strategy compares the source row's `updated_at` timestamp against the timestamp stored in the snapshot table
- If `updated_at` has changed since the last snapshot run, dbt closes the old snapshot row (sets `dbt_valid_to` to now) and inserts a new current row
- This is more efficient than the `check` strategy because it does not compare all column values — only the timestamp
Why this is asked: Understanding the two snapshot strategies (timestamp vs check) is a core snapshot concept.

**Q3 (Starter): What is the `check` snapshot strategy in dbt, and when would you use it over `updated_at`?**
What a good answer covers:
- The `check` strategy compares a specified list of columns (or all columns) between the source and the existing snapshot; if any differ, dbt creates a new snapshot record
- Use `check` when the source table does not have a reliable `updated_at` timestamp (e.g., the source system does not maintain an audit field)
- `check` is slower because it compares column values for every row on every run; `updated_at` only checks the timestamp
Why this is asked: The trade-off between the two strategies is a practical decision candidates encounter in real projects.

**Q4 (Starter): How do you query a dbt snapshot to find the value of a column as it was on a specific historical date?**
What a good answer covers:
- Filter the snapshot table where `dbt_valid_from <= target_date AND (dbt_valid_to > target_date OR dbt_valid_to IS NULL)`
- `dbt_valid_to IS NULL` identifies the current (open) record; historical records have a non-null `dbt_valid_to`
- This pattern is the standard SCD Type 2 point-in-time query and is used in the intermediate layer to join orders to the customer state at the time of the order
Why this is asked: Querying snapshot history correctly is the most common operational use of snapshots.

---

**Q5 (Mid): A dbt snapshot in c004_snapshots_demo.py runs hourly, but the source system only updates customer records once a day. What are the implications, and how would you adjust the snapshot cadence?**
What a good answer covers:
- Running snapshots more frequently than the source update cadence adds unnecessary compute cost and creates more snapshot rows than needed (though duplicate consecutive rows are not created by dbt — it only inserts on change detection)
- However, running less frequently than the update cadence risks missing intermediate states if a row changes multiple times between runs
- Align the snapshot cadence with the source system's update frequency; monitor source freshness (c005_sources_freshness_demo.py) to validate the assumption
- If the source occasionally updates more than once per day, keep the hourly cadence but accept the cost as insurance
Why this is asked: Snapshot cadence is a practical operational decision that connects to source freshness awareness.

**Q6 (Mid): How does dbt handle snapshot invalidation when a source row is deleted — for example, a customer account is permanently closed in c004_snapshots_demo.py?**
What a good answer covers:
- By default, dbt snapshots do not detect hard deletes — if a row disappears from the source, the snapshot retains the last known row with `dbt_valid_to IS NULL` indefinitely
- To detect deletes, use the `invalidate_hard_deletes` configuration option: dbt compares source row keys against the snapshot and closes records for keys that no longer appear in the source
- Alternatively, the source system should soft-delete by setting a `deleted_at` timestamp, which the `updated_at` strategy naturally captures as a change
Why this is asked: Hard delete handling is a non-obvious snapshot edge case that separates candidates with real snapshot production experience.

**Q7 (Mid): What is the performance impact of running a dbt snapshot on a very large source table (e.g., 500 M rows), and how do you mitigate it?**
What a good answer covers:
- On each run, dbt compares the full source table against the existing snapshot to detect changes — for 500 M rows this is a full table scan on both sides
- For the `updated_at` strategy, add a filter to the snapshot source using a `where` clause that only selects rows updated since the last snapshot run — dramatically reducing the scan size
- Partition the source table and snapshot table on the `updated_at` column so the comparison only scans recent partitions
- Consider splitting a monolithic snapshot into multiple targeted snapshots (e.g., one per customer segment) to parallelize the work
Why this is asked: Snapshot scalability is a senior concern; the default configuration is not designed for very large tables without optimization.

**Q8 (Mid): How do downstream mart models consume a dbt snapshot correctly to avoid including historical (closed) records in a current-state report?**
What a good answer covers:
- Filter on `dbt_valid_to IS NULL` to select only the current (open) snapshot record for each entity
- Alternatively, use `dbt_valid_to = '9999-12-31'` if the snapshot uses a sentinel date instead of NULL for open records — check the snapshot configuration
- In the intermediate layer, create a `current_customers` CTE that applies this filter once, so all mart models reference the CTE rather than re-implementing the filter
- Add a `unique` test on the primary key in the intermediate model to guarantee that the filter produced exactly one current record per entity
Why this is asked: Correctly filtering snapshots for current-state queries is a common mistake that causes duplicates in reports.

---

**Q9 (Senior): A business analyst discovers that a dbt snapshot for customer status is missing a transition — a customer changed from "active" to "suspended" and back to "active" between two snapshot runs, and only the final "active" state is recorded. How do you address this?**
What a good answer covers:
- This is expected snapshot behavior — snapshots capture state at run time, not every intermediate state; if two changes happen between runs, only the final state is recorded
- To capture all intermediate states, increase the snapshot run frequency to be less than the minimum time between state changes
- If the source system records a change log (event stream), build the snapshot from the change log rather than the current-state table — every state transition will be captured
- Communicate clearly to stakeholders: snapshots are point-in-time records, not full change data capture; for full CDC, use Debezium or a streaming CDC tool
Why this is asked: The fundamental limitation of snapshot cadence vs CDC is a senior architectural distinction.

**Q10 (Senior): How would you use a dbt snapshot alongside an incremental model to build a slowly changing dimension that feeds a mart model for historical revenue attribution?**
What a good answer covers:
- Snapshot the customer dimension table to track changes in segment, region, or tier over time (using `updated_at` strategy)
- Build an incremental staging model on the orders fact that appends new orders daily
- In the intermediate model, join orders to the snapshot using a point-in-time join: `orders.order_date BETWEEN customers_snapshot.dbt_valid_from AND COALESCE(customers_snapshot.dbt_valid_to, CURRENT_DATE)`
- The mart aggregates revenue by the customer segment that was in effect at order time — not the current segment
- Run the snapshot before the incremental model in the orchestration DAG to ensure new customer state changes are captured before orders are joined
Why this is asked: The combination of snapshots and incremental models for historical attribution is an advanced design pattern.

**Q11 (Senior): Describe how you would test a dbt snapshot to verify its correctness, including the handling of SCD Type 2 history.**
What a good answer covers:
- `unique` test on `snapshot_id` (the surrogate key dbt generates) to ensure no duplicate snapshot records exist
- `not_null` tests on `dbt_valid_from`, `dbt_scd_id`, and the natural key (`customer_id`)
- Singular test: assert that for each `customer_id`, there is exactly one row where `dbt_valid_to IS NULL` (exactly one current record)
- Singular test: assert that `dbt_valid_from < dbt_valid_to` for all closed records (no inverted date ranges)
- Row count test: assert the snapshot has at least as many rows as the source (it should have more if any history has been captured)
Why this is asked: Snapshot testing requires custom singular tests because the four generic tests do not cover SCD-specific invariants.

---

**Q12 (Architect): Design a snapshot strategy for a GDPR-regulated environment where customer personal data must be erasable on request, but historical analytical records must be preserved.**
What a good answer covers:
- Separate personally identifiable information (PII) from analytical attributes at the snapshot level: snapshot customer segment, tier, and status; do not snapshot name, email, or address directly
- Store PII in a separate pseudonymization table keyed by `customer_id`; the snapshot references only `customer_id` as the join key
- On GDPR erasure request: delete or null out the PII pseudonymization table row; the snapshot retains the historical analytical record (segment, tier changes) without PII
- This satisfies both GDPR (PII is erasable) and analytics (historical segment attribution is preserved)
- Connect to data quality track: add a dbt test that asserts no PII columns exist in any snapshot model — enforced at CI time to prevent accidental PII inclusion
Why this is asked: GDPR-compliant snapshot design is an architect-level privacy engineering challenge.

**Q13 (Architect): Your organization wants to use dbt snapshots as the foundation of a data vault implementation. How would snapshots map to data vault hubs, satellites, and links?**
What a good answer covers:
- Hubs: contain only the business key and load timestamp — implement as a standard incremental dbt model that appends new business keys as they appear
- Satellites: track attribute changes over time — this is exactly what dbt snapshots do; each satellite is a snapshot of the source entity's descriptive attributes
- Links: record relationships between business keys — implement as incremental models that append new relationship records; use snapshots if relationship attributes (e.g., a contract between customer and product) also change over time
- Use dbt's `ref()` to wire hubs, satellites, and links together in the DAG so the build order is enforced
- Connect to orchestration track: the data vault load order (hubs before links before satellites) must be reflected in the orchestration DAG; use dbt's dependency graph to generate the correct Airflow task order automatically
Why this is asked: Mapping dbt primitives to data vault constructs is an architect-level modeling decision that tests deep familiarity with both paradigms.

---

## Topic 5: Sources and Freshness

**Q1 (Starter): What is a dbt source, and why declare sources in `sources.yml` instead of using hardcoded table names in models?**
What a good answer covers:
- A dbt source is a declaration of an external table or view that dbt did not create — it lives in `sources.yml` under the `sources:` key
- Using `{{ source('schema', 'table') }}` in model SQL resolves to the correct database and schema per environment, without hardcoding
- `sources.yml` is also where freshness checks, column descriptions, and tests are defined for source tables — centralizing governance of the ingestion boundary
Why this is asked: Source declarations are the entry point of the dbt DAG — every dbt user must understand their purpose.

**Q2 (Starter): What is source freshness in dbt, and what does `dbt source freshness` check?**
What a good answer covers:
- Source freshness checks verify that a source table has been updated within a configured time threshold (e.g., warn if the latest row is more than 1 hour old; error if more than 3 hours old)
- `dbt source freshness` queries the `loaded_at_field` column (a timestamp on the source table) and compares the maximum value against the current time
- If the freshness check fails, it signals that the upstream ingestion pipeline has stalled before any dbt models run
Why this is asked: Source freshness is the first line of defense against running transformations on stale data.

**Q3 (Starter): In c005_sources_freshness_demo.py, a freshness check is run before the dbt pipeline executes. What happens to downstream models if the freshness check fails?**
What a good answer covers:
- By default, a freshness failure (error) does not automatically block downstream model runs — it exits with a non-zero code, but `dbt run` must be explicitly gated on `dbt source freshness` success by the orchestrator
- In orchestration (e.g., Airflow), the pattern is: run `dbt source freshness` as a task, set it as an upstream dependency of `dbt run`, and configure the DAG to fail if the freshness task fails
- With `dbt build`, freshness checks are included in the build graph and failures propagate through the DAG automatically
Why this is asked: Freshness checks are only useful if the pipeline respects them — candidates must know how to wire them into the execution flow.

**Q4 (Starter): How do you configure a warn threshold and an error threshold for a source freshness check in `sources.yml`?**
What a good answer covers:
- Under the source table definition, add `freshness: {warn_after: {count: 1, period: hour}, error_after: {count: 3, period: hour}}`
- `warn_after` causes a warning (exit code 0) if the source is between 1 and 3 hours old; `error_after` causes a failure (exit code 1) if it is older than 3 hours
- You must also specify `loaded_at_field: <timestamp_column>` so dbt knows which column to use as the freshness indicator
Why this is asked: Configuration syntax for freshness is a basic practical skill.

---

**Q5 (Mid): c005_sources_freshness_demo.py runs freshness checks on multiple source tables. How would you configure different freshness SLAs for different tables — for example, a real-time events table vs a daily customer export?**
What a good answer covers:
- Each table under a source can have its own `freshness` block with independent `warn_after` and `error_after` settings
- Real-time events table: `warn_after: {count: 15, period: minute}, error_after: {count: 1, period: hour}`
- Daily customer export: `warn_after: {count: 25, period: hour}, error_after: {count: 49, period: hour}` (slightly more than one day to tolerate weekend/holiday delays)
- Tables with no freshness requirement can set `freshness: null` to skip the check entirely
Why this is asked: Per-table freshness SLAs are a real configuration task that requires understanding the business context of each source.

**Q6 (Mid): What are the limitations of dbt's built-in source freshness check, and how would you extend it for more sophisticated freshness monitoring?**
What a good answer covers:
- The built-in check only looks at the maximum value of the `loaded_at_field` — it does not check row counts, data completeness, or distribution shifts
- It cannot detect a source that is "fresh but wrong" (the timestamp is recent but the ingestion job loaded 0 rows or duplicate rows)
- Extensions: pair freshness checks with a `dbt-utils.recency` test that also asserts a minimum row count in the recent window; use a data observability tool (e.g., Monte Carlo, Great Expectations) for distribution-level freshness monitoring
- For sources without a `loaded_at_field`, use a custom macro that queries audit log tables or counts rows in a date range as a proxy freshness signal
Why this is asked: Understanding the limitations of built-in features and knowing how to extend them is a mid-level engineering maturity marker.

**Q7 (Mid): How do you handle a source table that does not have a timestamp column, making standard dbt freshness checks impossible?**
What a good answer covers:
- Option 1: add a row count check as a surrogate freshness signal — if today's partition has fewer than N rows, the source is likely stale
- Option 2: use a metadata query against the warehouse's table information schema to get the last modified time of the physical table (e.g., `INFORMATION_SCHEMA.TABLES.LAST_ALTERED` in Snowflake)
- Option 3: work with the upstream data engineering team to add an ingestion timestamp column to the source at the pipeline level
- In `sources.yml`, use `freshness: null` to disable the built-in check and implement the alternative check as a singular dbt test instead
Why this is asked: Real-world sources often lack ideal freshness columns — candidates must have pragmatic alternatives.

**Q8 (Mid): How does dbt source freshness interact with `dbt build` vs running `dbt source freshness` and `dbt run` separately?**
What a good answer covers:
- `dbt build` runs sources, snapshots, models, and tests in DAG order in a single command; freshness checks for sources are included and a freshness failure propagates to block dependent model builds
- Running `dbt source freshness` separately gives more control: you can inspect the freshness results before deciding whether to proceed with `dbt run`
- In CI, running separately allows the freshness check to fail fast before spending time compiling and running models against stale data
- In production orchestration, `dbt build` is simpler but couples freshness failures to model failures; separate execution decouples alerting (freshness alert) from pipeline failure (model error)
Why this is asked: Operational workflow design around `dbt build` vs separate commands is a mid-level DevOps concern.

---

**Q9 (Senior): In a production pipeline based on c005_sources_freshness_demo.py, a source freshness check is triggering false positives during known batch windows (e.g., the nightly ETL runs between 2–4 AM and the source is legitimately stale during this window). How do you handle this?**
What a good answer covers:
- Widen the `error_after` threshold to accommodate the full batch window plus a buffer: if the batch runs for 2 hours, set `error_after` to 3 hours to avoid false positives during the window
- Use the orchestrator to suppress or skip the freshness check during the known batch window: in Airflow, use `ShortCircuitOperator` or `BranchPythonOperator` to skip freshness tasks between 2–4 AM
- Add a "batch in progress" flag to a control table that the freshness check reads before emitting an alert — if the flag is set, downgrade the failure to a warning
- Communicate the maintenance window SLA in `sources.yml` via the `description` field so the check threshold is self-documenting
Why this is asked: False positive management in production freshness monitoring is a senior operational skill.

**Q10 (Senior): How would you build an end-to-end data freshness SLA dashboard using dbt source freshness results and dbt artifacts?**
What a good answer covers:
- After every `dbt source freshness` run, dbt writes results to `sources.json` (dbt artifact); parse this file in a post-run hook or a pipeline step and load it to a metadata table in the warehouse
- The metadata table schema: `source_name`, `table_name`, `max_loaded_at`, `freshness_status` (pass/warn/error), `run_at`, `warn_threshold`, `error_threshold`
- Build a dbt model on top of the metadata table to calculate rolling freshness SLA compliance (e.g., "what percentage of runs in the last 30 days passed freshness checks per source?")
- Expose the model as a mart table consumed by a BI dashboard; set up alerts when freshness SLA compliance drops below threshold
- Connect to orchestration track: trigger the metadata load as a downstream task in the Airflow DAG so the dashboard is always current after each pipeline run
Why this is asked: Building observability infrastructure from dbt artifacts is a senior data platform engineering skill.

**Q11 (Senior): A source table's freshness degrades gradually over weeks — check times drift from 30 minutes to 4 hours without ever breaching the error threshold. How do you detect and address this trend before it becomes an incident?**
What a good answer covers:
- Trend monitoring: load `sources.json` artifacts to the warehouse after every run and query the `max_loaded_at` distribution over time; build a rolling average freshness age metric
- Alert on trend: set a secondary alert when the 7-day rolling average freshness age exceeds 2x the historical baseline — this fires before the error threshold is breached
- Root cause analysis: correlate freshness degradation with upstream pipeline metrics (ingestion job duration, row counts, error rates) to identify whether the source ETL is slowing down
- Connect to data quality track: integrate freshness trend data into the data observability platform alongside test failure rates and model run durations for a unified pipeline health view
Why this is asked: Trend-based alerting before threshold breach is a senior observability engineering practice.

---

**Q12 (Architect): Design a multi-source freshness monitoring architecture for a data platform with 500 source tables from 20 upstream systems, each with different update frequencies and business criticality.**
What a good answer covers:
- Classify sources into tiers by criticality: Tier 1 (revenue-critical, real-time); Tier 2 (operational, hourly); Tier 3 (reference data, daily)
- Configure freshness thresholds per tier in `sources.yml` templates enforced by a linting tool that validates all source declarations match their tier's standard
- Run `dbt source freshness` on a schedule matching the tightest tier (every 5 minutes for Tier 1); use `--select source:<specific_sources>` to run subset checks for faster iteration
- Route freshness alerts by tier: Tier 1 failures page the on-call engineer immediately; Tier 2 creates a ticket; Tier 3 logs to a weekly review digest
- Connect to ELT pipeline patterns track: gate ELT pipeline runs in Airflow on freshness checks for their specific source dependencies — a Tier 1 pipeline does not start if its Tier 1 sources are stale
- Centralize freshness metadata in a data catalog so business stakeholders can see source reliability scores alongside data lineage
Why this is asked: Multi-source freshness governance at platform scale is an architect-level design problem.

**Q13 (Architect): How would you architect a self-healing data pipeline where dbt source freshness failures automatically trigger upstream remediation rather than just alerting?**
What a good answer covers:
- Instrument `dbt source freshness` as an Airflow task with failure callbacks that publish a remediation event to a message queue (e.g., SNS, PubSub)
- Each upstream ingestion pipeline subscribes to its relevant source's remediation topic; on receipt, it triggers a re-run of the failed ingestion job
- Implement a circuit breaker: if a source fails freshness more than N times in a rolling window, stop auto-remediation and escalate to on-call — prevent infinite retry loops that mask systemic failures
- After upstream remediation, re-run `dbt source freshness` as a verification step; if it passes, resume the blocked dbt pipeline automatically
- Connect to orchestration track: use Airflow's `TriggerDagRunOperator` to chain the remediation DAG to the blocked analytics DAG; once freshness passes, the analytics DAG resumes from the failed task using Airflow's partial retry
- Log all auto-remediation events to an audit table so the platform team can track which sources are chronically unreliable and prioritize upstream improvements
Why this is asked: Self-healing pipeline design requires architect-level knowledge of orchestration, event-driven systems, and operational risk management.
