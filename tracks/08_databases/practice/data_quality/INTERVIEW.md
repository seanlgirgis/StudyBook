# Interview Questions — Data Quality

> Topics covered: schema validation · null and type checks · referential integrity · data freshness · anomaly detection
> Levels: Starter | Mid | Senior | Architect

---

## Topic 1 — Schema Validation

*Reference file: `c001_schema_validation_demo.py`*

---

**Q1: What does schema validation check in a data pipeline?**
What a good answer covers:
- Schema validation verifies that incoming data conforms to the expected structure: correct field names, correct data types, no missing required fields, and no unexpected extra fields
- In `c001_schema_validation_demo.py`, the validator checks each row against `EXPECTED_SCHEMA`, reporting missing fields, wrong types, and extra fields as distinct issues
- It acts as a contract enforcement layer at the pipeline boundary, preventing corrupt data from reaching curated tables
Why this is asked: Establishes whether the candidate understands validation as a gating mechanism, not just a logging exercise.

**Q2: Why is it important to validate schema at the pipeline's ingestion boundary rather than at the consuming query layer?**
What a good answer covers:
- Catching schema violations early prevents bad data from propagating through multiple transformation stages, limiting the blast radius of corruption
- Validating at the query layer means the bad data has already been stored; fixing it requires reprocessing, which is more expensive than rejecting at ingest
- Early validation enables fast feedback to source teams so they can correct the upstream issue before the next batch
Why this is asked: Tests whether the candidate thinks about failure containment and shift-left data quality.

**Q3: In `c001_schema_validation_demo.py`, the BAD_BATCH contains a row with `customer_name` instead of `customer`. How does the validator detect and report this?**
What a good answer covers:
- The validator iterates `EXPECTED_SCHEMA` fields and checks each required field is present in the row; `customer` is absent, so it records "missing customer"
- The extra-fields check (`set(row.keys()) - set(schema.keys())`) detects `customer_name` as an unexpected column
- The result is a row-level issue list that the pipeline can use to route the row to a quarantine table with the issue description attached
Why this is asked: Makes the candidate read and reason about actual demo code, not just recite abstract concepts.

**Q4: What is the difference between schema validation and schema enforcement?**
What a good answer covers:
- Schema validation detects and reports violations but may allow the pipeline to continue with quarantined bad rows
- Schema enforcement rejects writes outright when the incoming data does not match the registered schema (Delta Lake's default behavior with `enforceSchema = true`)
- Validation is appropriate when partial loads are acceptable; enforcement is appropriate when any deviation must block the load entirely
Why this is asked: Distinguishes two related but operationally different behaviors.

---

**Q5: A batch arrives with 10,000 rows, 200 of which fail schema validation. Should the pipeline load the 9,800 good rows and quarantine the 200, or fail the entire batch? What factors drive this decision?**
What a good answer covers:
- Depends on the business impact of partial loads: for financial tables where completeness is mandatory, fail the entire batch to avoid partial state
- For operational tables where best-effort loading is acceptable, load valid rows and quarantine failures with an alert to the source team
- The data contract (`c005_data_contracts_demo.py`) should specify the policy: a "zero-tolerance" contract fails the batch; a "best-effort" contract permits partial loads
- Either way, the quarantine table must be monitored and resolved before the next batch run to prevent growing backlogs
Why this is asked: Tests practical judgment about pipeline behavior under partial failure, which candidates often have strong opinions about.

**Q6: How would you extend the schema validator in `c001_schema_validation_demo.py` to support nullable vs non-nullable constraints on individual fields?**
What a good answer covers:
- Add a `nullable` flag to each field definition in `EXPECTED_SCHEMA` (e.g., `{"type": float, "nullable": False}`)
- In `_validate_row`, after type-checking, add a check: if `not nullable` and value is `None` or empty string, append a "null not allowed" issue
- Document which fields are nullable in the schema registry so source teams know which fields are strictly required
- Test with rows where nullable fields are omitted (should pass) and non-nullable fields are None (should fail)
Why this is asked: Extends the candidate's understanding from the demo code to a realistic production enhancement.

**Q7: Schema validation passes, but downstream analytics produce wrong results because a `status` field accepts any string and a source team accidentally sends "PIAD" instead of "PAID". How do you catch this class of error?**
What a good answer covers:
- Add an accepted-values constraint to the schema definition for enumerated fields (analogous to dbt's `accepted_values` test)
- Treat any value outside the defined set as a schema violation, routing the row to quarantine with an "invalid status value" reason
- Maintain the accepted-values list in a config file or data contract so it can be updated without code changes when new statuses are introduced
- Alert when new unseen values appear, even if the pipeline does not quarantine them, so operations teams are informed of source-side changes
Why this is asked: Bridges type validation to value-domain validation, which is equally important in practice.

**Q8: You inherit a pipeline where schema validation is disabled because "it causes too many failures." How do you re-enable it incrementally without disrupting production loads?**
What a good answer covers:
- Start in audit mode: run validation and log all violations without blocking the pipeline; build a baseline of what violations exist today
- Triage violations: distinguish systemic issues (source always sends extra fields) from intermittent issues (occasional type errors)
- Fix systemic issues at the source or in the transformation layer before enabling enforcement
- Re-enable enforcement one field at a time, starting with the most critical (primary keys, required financial fields) and last with optional or frequently varying fields
Why this is asked: Incremental remediation in a messy production system is a senior engineering skill.

---

**Q9: Design a schema validation framework that supports 50 different source schemas, each updated independently by different teams, without requiring a central schema team to approve every change.**
What a good answer covers:
- Each source team owns their schema definition file in a central git repository; changes go through a PR review gated by CI that runs backward-compatibility checks
- The CI pipeline runs `c001_schema_validation_demo.py`-style validation against the last 7 days of historical data using the proposed new schema to detect regressions
- A self-service schema registry UI allows source teams to view their current contract and propose changes; breaking changes require a consumer impact report before merge
- The platform team maintains the validation framework infrastructure; source teams own the schema definitions — aligning with data mesh ownership principles
Why this is asked: Scales the single-schema validator to an organizational governance system.

**Q10: A source delivers data via a REST API that returns JSON with dynamically nested structures that vary per record type. How do you apply schema validation to heterogeneous records?**
What a good answer covers:
- Use a discriminator field (e.g., `record_type`) to select the appropriate schema for each record before validation
- Define a schema registry keyed by `record_type`; the validator dispatches to the correct schema dynamically
- Records with unknown `record_type` values are routed to a quarantine table with a "no schema registered" reason and alerted on
- For deeply nested JSON, use a recursive schema validator or a JSON Schema library (e.g., Python `jsonschema`) rather than the flat-field approach in `c001_schema_validation_demo.py`
Why this is asked: Extends validation to real-world heterogeneous API payloads.

**Q11: Your schema validation runs in a Spark job that processes 500GB batches. The validation logic written in pure Python (as in `c001_schema_validation_demo.py`) is a bottleneck. How do you scale it?**
What a good answer covers:
- Rewrite validation as Spark native operations using DataFrame `schema` enforcement, `withColumn` type casting with error handling, or `pyspark.sql.functions` for value checks
- Delta Lake's `enforceSchema` handles structural validation natively without custom Python code
- For complex business-rule validation, use Spark UDFs only as a last resort; prefer SQL expressions that Spark can optimize
- Profile the validation job to identify whether the bottleneck is Python serialization, the validation logic itself, or I/O; address the actual bottleneck
Why this is asked: Tests the candidate's ability to translate a correct but non-scalable prototype into production-scale implementation.

---

**Q12: A regulated financial pipeline must prove to auditors that schema validation ran on every batch and that no violations were silently suppressed. Design an immutable audit trail for schema validation results.**
What a good answer covers:
- Write validation results (batch ID, timestamp, row count, violation count, sampled violation details) to an append-only audit table in the data lakehouse after every run
- Use Delta Lake's transaction log to ensure the audit record is committed atomically with the data load; if the load fails, the audit record shows the failure
- Sign or hash the audit records to prevent tampering; store the hash in a separate system the pipeline cannot modify
- Connect to the data contracts track: the audit trail is the evidence that the contract's quality clauses are enforced; auditors can query it directly without requiring access to raw data
Why this is asked: Compliance-driven audit trail design is an architect-level requirement in financial pipelines.

**Q13: Explain how schema validation must adapt when a data lakehouse transitions from a single-writer architecture to a multi-writer architecture where streaming and batch pipelines write concurrently to the same table.**
What a good answer covers:
- Single-writer validation is straightforward: validate the batch before writing. Multi-writer requires validation before each write and conflict detection after the write
- Delta Lake's optimistic concurrency control serializes concurrent writes via the transaction log; a write that conflicts is retried or rejected, but the schema of each write is validated independently
- Schema validation must be idempotent: re-validating a batch that was already partially written (due to a retry) must not flag the already-committed portion as a violation
- Connect to the ACID properties in the lakehouse track (`c002_delta_lake_acid_demo.py`): schema enforcement and ACID transactions work together to ensure each commit is both structurally valid and atomically applied
Why this is asked: Multi-writer schema consistency is an architect-level concern that spans the data quality and lakehouse tracks.

---

## Topic 2 — Null and Type Checks

*Reference file: `c002_null_type_checks_demo.py`*

---

**Q1: Why are null checks important in a data quality pipeline?**
What a good answer covers:
- Null values in required fields cause silent errors in downstream calculations (e.g., a null `amount` is excluded from a revenue sum without warning)
- They indicate upstream data capture failures that should be investigated at the source, not silently absorbed by the pipeline
- `c002_null_type_checks_demo.py` demonstrates flagging rows where required fields are null so they can be quarantined before reaching curated tables
Why this is asked: Null handling is the most common class of data quality bug; this question tests baseline awareness.

**Q2: What is the difference between a null value and an empty string, and why does the distinction matter in a pipeline?**
What a good answer covers:
- Null means the value is absent or unknown; an empty string is a valid (if semantically empty) string value
- Many source systems serialize missing values as empty strings rather than nulls, which passes a `NOT NULL` check but fails a business-rule check
- Pipelines must normalize both to null (or flag both) for required fields; the normalization rule should be defined in the data contract
Why this is asked: This distinction is frequently overlooked and causes real production bugs.

**Q3: How would you check that an `amount` column contains only valid numeric values when it arrives as a string field (as in `c001_staging_raw_curated_demo.py`, where "N/A" appears)?**
What a good answer covers:
- Attempt to cast the string to float; catch the cast failure and flag the row as a type violation
- In `c001_staging_raw_curated_demo.py`, "N/A" would fail the numeric cast; the row should be quarantined with reason "amount not castable to float"
- Do not silently coerce to null or zero; both destroy information about why the value is missing
Why this is asked: Type coercion with silent data loss is a common but dangerous anti-pattern.

**Q4: What is a null rate threshold and how is it used in data quality monitoring?**
What a good answer covers:
- A null rate threshold defines the maximum acceptable percentage of nulls in a given column (e.g., `customer` may be null in at most 1% of rows)
- If the null rate exceeds the threshold, it indicates a systematic upstream data capture failure rather than isolated missing values
- Thresholds are defined in the data contract and checked after every load; a breach triggers an alert and potentially blocks the curated table update
Why this is asked: Introduces statistical quality monitoring as a complement to row-level checks.

---

**Q5: A column has a 0% null rate in test data but suddenly shows a 15% null rate in production. Walk through how you would diagnose the root cause.**
What a good answer covers:
- Check whether the 15% null rate correlates with a specific source partition (date, region, system) to isolate the scope of the problem
- Compare the production batch's schema to the expected schema: a renamed column would appear as 100% null for the new name and 0% for the old name
- Review source system release notes or change logs for the date the null rate appeared; correlate with deployments
- In `c002_null_type_checks_demo.py`, the null check should include a comparison to a baseline null rate so anomalies are surfaced automatically rather than requiring manual investigation
Why this is asked: Diagnostic reasoning under a real production scenario tests senior-level incident response skills.

**Q6: Your pipeline receives an `order_id` column that is sometimes an integer and sometimes a string depending on the source environment. How do you handle this without breaking downstream consumers?**
What a good answer covers:
- Normalize to string at ingestion: cast all integer order IDs to string in the staging-to-raw transformation; never pass the type ambiguity downstream
- Document the normalization rule in the data contract so consumers know the canonical type is always string
- Alert if the incoming type changes unexpectedly (an integer `order_id` arriving in a batch that historically sent strings) because it may indicate a source-side issue beyond just type
- Add a uniqueness check on the normalized key to catch cases where integer 101 and string "101" coexist and would create duplicate keys after normalization
Why this is asked: Mixed-type primary keys are a production reality; candidates must have a concrete normalization strategy.

**Q7: How do you apply type checks efficiently across a DataFrame with 200 columns and 50 million rows without writing a check for every column manually?**
What a good answer covers:
- Drive checks from a schema definition file: iterate the schema dict and apply the appropriate check for each column's declared type (similar to `c001_schema_validation_demo.py`)
- In Spark, use `df.schema` to compare inferred types to the expected types programmatically; flag mismatches without row-level iteration
- For null rate checks, use `df.select([F.mean(F.col(c).isNull().cast("int")).alias(c) for c in df.columns])` to compute null rates for all columns in a single pass
- Generate a summary report per run rather than per-row output so monitoring is O(columns) not O(rows)
Why this is asked: Scalable quality checking architecture separates those who have built production systems from those who have only read about quality checks.

**Q8: A dbt model has tests for `not_null` and `accepted_values` on the `status` column, but the tests run after the model materializes. What risk does this create and how do you mitigate it?**
What a good answer covers:
- If the test runs after materialization, bad data is already written to the target table; consumers who query between the write and the test see invalid data
- Mitigation: run dbt tests against a staging schema before promoting to the production schema (using dbt's `--defer` or a blue/green promotion pattern)
- Alternatively, add pre-hook validation that runs the quality checks inside the model transaction before committing
- Connect to schema validation: move the most critical checks to the source layer (upstream of dbt) so the model only receives pre-validated data
Why this is asked: Tests awareness of the timing gap between data writing and quality assertion in dbt workflows.

---

**Q9: Design a null and type check system that can learn "normal" null rates from historical data and alert on deviations without requiring manually set thresholds for each column.**
What a good answer covers:
- Compute a rolling baseline null rate for each column using the last 30 days of runs; store per-column statistics in a quality metadata table
- Use statistical control limits (mean ± 3 standard deviations) to flag anomalies automatically — similar to the baseline approach in `c005_anomaly_detection_demo.py`
- Bootstrap new columns: the first 14 days of data are in "learning mode" with no alerts; after that, the learned baseline activates
- Alert on both sudden spikes (15% null rate after 0% baseline) and gradual drift (null rate increases 0.5% per week over two months)
Why this is asked: Adaptive quality thresholds are a senior-level data observability design pattern.

**Q10: A `timestamp` column arrives in three different formats across source batches: ISO 8601, Unix epoch seconds, and `MM/DD/YYYY HH:MM`. How do you handle this in the pipeline without data loss?**
What a good answer covers:
- Detect the format at ingestion: apply a format-detection heuristic or try each parser in order; the first successful parse wins
- Log the detected format per batch to the quality metadata table so format drift is visible over time
- Normalize all timestamps to UTC ISO 8601 at the staging-to-raw boundary; store the original string in a `raw_timestamp` column for audit
- Alert if a new format is detected that does not match any known pattern; quarantine the row rather than silently dropping the timestamp
Why this is asked: Multi-format timestamps are one of the most common real-world null/type problems.

**Q11: You discover that a critical revenue column has been silently coercing type-cast failures to 0.0 for the past six months. Design the remediation strategy and the controls to prevent recurrence.**
What a good answer covers:
- Identify the date range and affected rows by replaying the raw layer with a correct (non-coercing) type check to isolate rows where the original value was non-numeric
- Quantify the revenue impact: compare the coerced totals against source system totals for the affected period
- Restore correct values from the raw layer; if the original source value was genuinely corrupt, quarantine those rows with a "source data corrupt" flag
- Prevention: replace the coercion with a hard failure; add a regression test with a row containing a non-numeric amount; add a null/zero rate monitor that would have flagged the anomaly
Why this is asked: Incident reconstruction from the raw layer and root-cause prevention are senior engineering skills.

---

**Q12: A machine learning feature pipeline relies on null imputation (filling nulls with column means) before training. Downstream monitoring shows model drift. Design a data quality system that distinguishes between "genuine nulls" and "imputed values" to support root-cause analysis.**
What a good answer covers:
- Add a companion boolean column for each imputed field: `amount_is_imputed` = True when the original value was null and the displayed value is the imputed mean
- Store the imputation statistics (mean used, imputation date, null rate at imputation time) in a feature metadata table for audit
- Track the imputation rate over time; a rising imputation rate is an early warning of upstream data degradation before model drift becomes visible
- Connect to anomaly detection (`c005_anomaly_detection_demo.py`): flag batches where the imputation rate exceeds the baseline as a data quality anomaly before they enter the training pipeline
Why this is asked: Connects null handling to ML feature quality — a cross-track scenario that tests architecture-level thinking.

**Q13: An organization is migrating from a relational warehouse (where NOT NULL is enforced at the database level) to a lakehouse (where enforcement is optional). Design a governance model that maintains the same null constraint guarantees without relying on database-level enforcement.**
What a good answer covers:
- Export the NOT NULL constraints from the warehouse's information schema and convert them to data contract quality rules automatically during migration
- Implement pre-write validation in the pipeline (as in `c001_schema_validation_demo.py`) to enforce NOT NULL before any write reaches the lakehouse
- Add Delta Lake table constraints (`ALTER TABLE ... ADD CONSTRAINT`) where supported to provide a second enforcement layer
- Run daily reconciliation checks that compare the lakehouse null rates against the warehouse's historical null rates; alert on divergence during the transition period
- Post-migration: the quality rules in the contract replace the database constraint; CI tests validate the rules match the original constraint definitions
Why this is asked: Migration governance that preserves data integrity guarantees is an architect-level design scenario.

---

## Topic 3 — Referential Integrity

*Reference file: `c003_referential_integrity_demo.py`*

---

**Q1: What is referential integrity in a data pipeline context?**
What a good answer covers:
- Referential integrity means that a foreign key value in one table always has a corresponding primary key row in the referenced table (e.g., every `order.customer_id` exists in the `customers` table)
- In a pipeline, a referential integrity check validates this relationship after each load before the data is promoted to the curated layer
- `c003_referential_integrity_demo.py` demonstrates detecting orphan rows — records whose foreign key has no match in the parent table
Why this is asked: Tests whether the candidate understands relational data quality beyond column-level checks.

**Q2: Why do data warehouses and lakehouses often not enforce foreign key constraints at the storage level, and what replaces them?**
What a good answer covers:
- Enforcing FK constraints at write time is expensive at data warehouse scale; most analytical databases (Snowflake, BigQuery, Delta Lake) accept FK definitions as metadata only, not as enforced constraints
- Enforcement is replaced by pipeline-level referential integrity checks run as a quality gate after each load
- dbt's `relationships` test is the most common implementation: it checks that all values in a FK column exist in the referenced PK column
Why this is asked: Candidates must understand why traditional RDBMS guarantees do not automatically transfer to the analytics stack.

**Q3: What is an orphan record and what are its typical downstream consequences?**
What a good answer covers:
- An orphan record has a foreign key value that does not exist in the parent table (e.g., an order with a `customer_id` that has no row in `customers`)
- Downstream JOINs silently drop orphan rows (INNER JOIN) or produce NULLs for all parent columns (LEFT JOIN), both of which corrupt aggregations
- Revenue by customer reports would undercount if orphan orders are dropped, and per-customer metrics would show NULL for orphan orders' customer names
Why this is asked: Connects the abstract concept to concrete downstream damage.

**Q4: A pipeline loads `orders` and `customers` from two different source systems. In what order should they be loaded to minimize referential integrity violations?**
What a good answer covers:
- Load the parent table (`customers`) before the child table (`orders`) so that by the time orders are loaded, their FK references already exist
- This is not always possible in streaming or concurrent batch scenarios; the pipeline must be designed to handle the case where a customer record arrives after the order that references it
- A delayed retry or a "pending" quarantine queue holds orders whose customer FK is unresolved until the parent record arrives
Why this is asked: Load ordering is a practical constraint candidates who have built multi-source pipelines will have dealt with.

---

**Q5: An order references a `product_id` that exists at load time but is later deleted from the `products` table by a soft-delete or hard-delete operation. How does your pipeline preserve referential integrity retrospectively?**
What a good answer covers:
- Use soft deletes in the parent table (add `is_deleted = true`) so FK references remain valid even after the logical deletion
- For hard deletes, add a tombstone record in `products` that preserves the `product_id` with a `deleted_at` timestamp
- Historical orders referencing a deleted product should resolve to the tombstone rather than producing a NULL join
- This design satisfies both GDPR erasure (set `is_deleted` and anonymize PII) and referential integrity (the key still resolves)
Why this is asked: The delete propagation problem is a common production challenge that mid/senior candidates should have solved.

**Q6: How do you implement a referential integrity check in dbt for a `fact_orders` table that references `dim_customers`, and what do you do with the failures?**
What a good answer covers:
- Use dbt's `relationships` test in `schema.yml`: `- relationships: to: ref('dim_customers'), field: customer_id`
- Failures are reported in the dbt test output; configure `store_failures = true` to persist failing rows to a test failure table for inspection
- Depending on severity: block the run (set `severity: error`) or warn and continue (set `severity: warn`) based on the data contract policy
- Investigate whether failures are orphans from load ordering gaps or genuine data quality issues at the source
Why this is asked: Connects the concept to the most common real-world implementation tool.

**Q7: A streaming pipeline ingests orders and customer events from separate Kafka topics with no guaranteed ordering. How do you handle referential integrity when a customer update has not yet arrived when the order event is processed?**
What a good answer covers:
- Use an event-time join with a bounded wait window: hold the order event in state for up to N seconds waiting for the matching customer event
- If the customer event does not arrive within the window, route the order to a "pending resolution" queue for later reconciliation
- A periodic batch reconciliation job joins the pending queue against the customer table and resolves any orders whose customer has since arrived
- Connect to the watermark pattern (`c003_watermarks_demo.py`): the wait window is effectively a per-key watermark on the customer stream
Why this is asked: Streaming referential integrity requires different solutions than batch; senior candidates must have both.

**Q8: You discover that 0.3% of orders in a 3-year-old production table have orphaned `customer_id` values because historical integrity checks were never run. How do you remediate this without reprocessing all 3 years of data?**
What a good answer covers:
- First, quantify: 0.3% may be acceptable for analytical use cases but unacceptable for financial reporting; get business sign-off on the remediation scope
- Identify orphans by running a LEFT JOIN between orders and customers on `customer_id` WHERE customer is NULL; partition the result by year to understand temporal distribution
- For each orphan, attempt to resolve via a lookup in archived customer data, the raw layer, or the source system
- Unresolvable orphans are tagged with `customer_resolution_status = 'unresolvable'` and excluded from affected reports with documentation
- Going forward, add a post-load RI check that blocks the curated promotion until orphan rate is below the contracted threshold
Why this is asked: Historical remediation under production constraints is a senior operational skill.

---

**Q9: Design a referential integrity monitoring system for a star schema with 8 dimension tables and 4 fact tables, where any of the 32 FK relationships could break at any time due to independent source system deployments.**
What a good answer covers:
- Build a configuration-driven RI check framework: define all 32 FK relationships in a YAML file; the check engine executes each relationship check after every load
- Prioritize checks by impact: fact-to-dimension relationships used in financial reports are severity=error; lookup tables used only in non-critical reports are severity=warn
- Publish a live RI health dashboard showing pass/fail status per relationship; alert when any error-severity check fails
- Track the orphan rate per relationship over time; a rising trend signals a degrading source system before it becomes a critical failure
Why this is asked: Scales from a single check to a monitoring system — an architect-level design exercise.

**Q10: A new data source introduces a composite foreign key (two columns together form the FK). How does this affect your referential integrity check implementation?**
What a good answer covers:
- Single-column FK checks (checking each column independently) are insufficient; both columns must match simultaneously in the parent table
- Implement a concatenated key check or a multi-column JOIN: `SELECT order_id FROM orders o LEFT JOIN parent p ON o.col1 = p.col1 AND o.col2 = p.col2 WHERE p.col1 IS NULL`
- Document the composite key in the data contract explicitly; single-key RI tools (like basic dbt `relationships` tests) require a workaround (concatenate keys, or use a custom test)
Why this is asked: Composite keys are common in real data models; candidates should know that single-column tools need adaptation.

**Q11: How do referential integrity checks interact with incremental pipeline loads, and why might a full-table RI check be necessary even when only a small incremental batch was loaded?**
What a good answer covers:
- An incremental RI check validates only the newly added rows against the parent table; this misses orphans introduced by parent-table deletes applied since the last incremental run
- If a customer is deleted from `dim_customers` after the last RI check, existing `fact_orders` rows now have orphaned FKs — but an incremental check on today's new orders would not detect this
- A periodic full-table RI check (daily or weekly) is required to catch FK violations created by parent-table mutations
- The frequency of full checks is proportional to the rate of parent-table churn; a slowly changing dimension may only need weekly full checks
Why this is asked: The interaction between incremental loads and full RI validation is a nuanced production design consideration.

---

**Q12: You are designing a data vault architecture where referential integrity is structurally enforced through hub/link/satellite relationships. How does your RI monitoring strategy differ from a traditional star schema approach?**
What a good answer covers:
- In data vault, hubs contain business keys; links reference hubs using surrogate keys (hash keys); RI between links and hubs is structurally enforced by the architecture
- RI monitoring focuses on whether link records have corresponding hub records (every link's hash key must exist in the referenced hub)
- Because hash keys are deterministically computed from business keys, orphan links are impossible if the load order is correct (hub before link); RI checks become load-order validation
- Connect to the ELT pipeline patterns track: the staging-to-raw-to-curated pattern maps to staging → raw vault (hubs/links/sats) → business vault (curated)
Why this is asked: Data vault RI is structurally different from star schema RI; architects working in enterprise DWH environments must understand both.

**Q13: Regulatory data lineage requirements demand that every foreign key relationship in a financial data model be traceable to its source system's equivalent relationship. Design a metadata system that captures cross-system referential lineage.**
What a good answer covers:
- Build a lineage metadata table that maps each warehouse FK relationship to its source system equivalent: `(warehouse_table, warehouse_fk_column) → (source_system, source_table, source_pk_column)`
- Populate lineage metadata during pipeline onboarding; require source teams to declare their equivalent keys in the data contract
- Run cross-system RI checks: validate that every FK value in the warehouse FK column exists in the source system's PK, not just in the warehouse parent table
- This catches cases where the warehouse parent table itself has data quality issues and not all source PKs were successfully loaded
- Connect to the schema evolution track: when source systems rename or restructure key columns, the lineage metadata must be updated as part of the schema change process
Why this is asked: Cross-system referential lineage is an architect-level regulatory requirement in financial services data governance.

---

## Topic 4 — Data Freshness

*Reference file: `c004_data_freshness_demo.py`*

---

**Q1: What is data freshness and why is it a data quality concern?**
What a good answer covers:
- Data freshness measures the age of the most recent data available in a table relative to the current time or a promised SLA
- Stale data causes downstream decisions to be made on outdated information; for operational dashboards this can lead to incorrect business actions
- `c004_data_freshness_demo.py` demonstrates checking whether the latest record's timestamp falls within an acceptable freshness window
Why this is asked: Freshness is the most user-visible data quality dimension; operations teams notice it immediately when a dashboard is stale.

**Q2: How do you define a freshness SLA for a table?**
What a good answer covers:
- A freshness SLA specifies the maximum acceptable age of the most recent record in a table at any given time (e.g., "orders must be refreshed within 30 minutes of source capture")
- It is defined in the data contract and is separate from the pipeline's scheduled run frequency; an SLA of 30 minutes with a 1-hour scheduled run is a misconfiguration
- The SLA must account for end-to-end latency: source capture time + pipeline processing time + any queue lag
Why this is asked: Tests whether the candidate can translate a business availability requirement into a measurable technical SLA.

**Q3: What is the difference between pipeline run freshness and data freshness?**
What a good answer covers:
- Pipeline run freshness measures whether the pipeline executed on schedule (the pipeline ran at 08:00 as expected)
- Data freshness measures whether the data in the table is up to date relative to the source (the latest record's event_time is from 07:55)
- A pipeline can run on time but produce stale data if the source system itself is delayed; monitoring only the pipeline schedule misses this scenario
Why this is asked: Many teams monitor pipeline schedules but not data currency; this distinction catches that gap.

**Q4: How does dbt's `freshness` configuration work and what does it check?**
What a good answer covers:
- dbt's source freshness uses `loaded_at_field` and `freshness` thresholds (`warn_after`, `error_after`) defined in `sources.yml`
- It queries `MAX(loaded_at_field)` and compares it to the current time; if the age exceeds `warn_after`, dbt emits a warning; if it exceeds `error_after`, it emits an error
- This check is run with `dbt source freshness` and can be integrated into CI/CD or monitoring pipelines
- It only checks the latest timestamp, not whether all expected partitions are present; a missing partition with an old latest timestamp would be flagged, but a missing partition in the middle of the range would not
Why this is asked: Tests knowledge of the most commonly used freshness tooling in the modern data stack.

---

**Q5: A business dashboard shows data from yesterday morning even though the pipeline appears to have run successfully last night. How do you diagnose whether this is a pipeline issue or a data issue?**
What a good answer covers:
- Check the pipeline run log: did the last night's run complete successfully, and what was the max event_time in the output?
- If the run completed but max event_time is still yesterday morning, the source system delivered stale data — the pipeline ran correctly but processed old records
- Check the watermark: if the high-water mark was not advanced correctly, the pipeline may have re-processed yesterday's already-loaded data
- Check whether the curated table and the BI tool are pointing at the same partition; a misconfigured view or cache can make a current table appear stale
Why this is asked: Distinguishes pipeline failures from source-side freshness failures, which require different responses.

**Q6: How would you implement a freshness check that validates not just the latest record but also that every expected daily partition is present?**
What a good answer covers:
- Generate a "expected partitions" calendar for the check period (e.g., every calendar day for the past 30 days) and LEFT JOIN against the table's actual partition list
- Any expected partition with no data is a freshness gap, even if the latest partition is current
- Alert on gaps with the specific missing dates so the pipeline team can investigate the cause (source delivery failure, pipeline skipped run, etc.)
- This is distinct from a simple `MAX(load_ts)` check and catches scenarios like a weekend job that did not run on a holiday
Why this is asked: Partition completeness is a more thorough freshness check that candidates with production experience will have implemented.

**Q7: A streaming pipeline delivers data continuously and the consumer expects sub-minute freshness. How do you monitor freshness for a continuously updated table without running a query every second?**
What a good answer covers:
- Use a metadata-based freshness signal: the streaming pipeline publishes a "last committed event_time" metric to a monitoring system (Prometheus, Datadog) on every micro-batch commit
- The monitoring system evaluates the freshness SLA against this metric without querying the data table directly
- Alert when the freshness metric exceeds the SLA threshold; the alert should include the last-committed event_time and the current lag
- Connect to the watermark pattern (`c003_watermarks_demo.py`): the streaming watermark is effectively the freshness indicator for stream-processed tables
Why this is asked: High-frequency freshness monitoring requires a different architecture than batch freshness checks.

**Q8: Multiple downstream consumers have different freshness requirements for the same table: the operations team needs data within 5 minutes, and the finance team needs data within 24 hours but with guaranteed completeness. How do you serve both?**
What a good answer covers:
- Publish two views or tables: a "live" view backed by the streaming layer for operations, and a "final" view backed by the complete batch window for finance
- The live view accepts the incompleteness trade-off of the current streaming window; the final view enforces completeness through watermark-gating
- Each view has its own freshness SLA defined in the data contract; monitors track each independently
- Connect to the watermarks topic: the final view's cutover is driven by the batch pipeline's watermark advancing past the close of the business day
Why this is asked: Multi-consumer freshness design is a practical architecture question that senior engineers encounter frequently.

---

**Q9: Your organization's data freshness SLAs are breached on average twice per week due to upstream source system delays that are outside your control. Design a resilience pattern that maintains consumer experience during these delays.**
What a good answer covers:
- Implement a "last known good" pattern: when a new batch fails the freshness SLA, keep the last successfully validated batch visible to consumers rather than showing partial or stale data
- Publish a freshness metadata endpoint that consumers can query to display a "data as of [timestamp]" indicator on dashboards
- Negotiate a tiered SLA with upstream: a "soft" target (breach triggers internal alert) and a "hard" limit (breach triggers escalation to source team)
- For consumers that cannot tolerate any delay, provision a real-time streaming path that bypasses the batch pipeline entirely
Why this is asked: Resilience under external SLA dependencies is an architect-level design challenge.

**Q10: How do you detect and alert on a gradual freshness degradation (latency increasing 2 minutes per day) before it breaches the SLA, rather than only alerting after the breach?**
What a good answer covers:
- Track the daily pipeline latency (source capture time to table availability time) in a quality metrics table over a rolling 30-day window
- Apply a linear trend analysis or simple exponential smoothing to detect a consistent upward trend in latency
- Alert when the trend projection predicts an SLA breach within the next 72 hours, not just when the breach occurs
- Connect to anomaly detection (`c005_anomaly_detection_demo.py`): gradual drift is a different pattern from a sudden spike; the anomaly detector must be tuned to catch both
Why this is asked: Proactive trend-based alerting separates reactive operations from predictive data reliability engineering.

**Q11: Design a freshness SLA enforcement system for a data platform with 200 tables, each with different SLAs defined in data contracts, and a requirement to produce a daily data reliability report for senior management.**
What a good answer covers:
- Store all SLA definitions in a contract registry keyed by table name; the freshness monitoring job loads SLAs at runtime rather than hardcoding them
- Run the freshness check for all 200 tables as a single scheduled job; aggregate results into a quality summary table with columns: table_name, sla_minutes, actual_freshness_minutes, status, last_breach_time
- Generate the daily report by querying the summary table: tables at risk (within 20% of SLA), tables in breach, and tables with improving/degrading trends
- Escalation routing is driven by the contract's owner field; breaches automatically create tickets in the owning team's issue tracker
Why this is asked: Scaling quality monitoring to an organizational system is an architect-level operations design problem.

---

**Q12: A machine learning model is retrained nightly using the previous day's curated data. If the data freshness SLA is breached, the model trains on stale data and serves degraded predictions. Design an automated freshness gate that prevents stale model training.**
What a good answer covers:
- Add a freshness validation step to the ML training pipeline that reads the curated table's `max(event_time)` and compares it to `current_date - 1`; abort training if freshness is outside tolerance
- Store the freshness validation result in the model metadata (MLflow experiment run tags) so every trained model version has a recorded data freshness certificate
- Alert the ML engineering team when training is aborted; provide a manual override workflow with a documented justification requirement
- Connect to data contracts: define a freshness SLA for the training dataset as a contract clause; the ML pipeline is a registered consumer of that contract
Why this is asked: Connects data freshness to ML reliability — a cross-track architecture scenario.

**Q13: Your company operates in multiple time zones and source systems deliver data according to local business hours. Design a freshness monitoring system that correctly evaluates SLAs relative to each source's local business day rather than UTC.**
What a good answer covers:
- Store each source system's timezone and business hours in the contract registry; compute the expected delivery deadline as `local_business_day_end + pipeline_processing_time`, converted to UTC for comparison
- A source in Tokyo that closes at 18:00 JST has a different UTC deadline than a source in New York that closes at 18:00 EST; the monitoring system must handle this correctly
- During daylight saving transitions, the UTC offset changes; use IANA timezone identifiers (not fixed offsets) to handle DST automatically
- Publish a timezone-normalized freshness dashboard that shows all sources relative to their own business day deadlines, not a single UTC threshold
- Connect to the data contracts track: the business-day freshness expectation is a contract clause that source teams must agree to, not a unilateral assumption by the pipeline team
Why this is asked: Multi-timezone freshness is a real architectural challenge in global organizations; this tests whether the candidate thinks beyond UTC-centric monitoring.

---

## Topic 5 — Anomaly Detection

*Reference file: `c005_anomaly_detection_demo.py`*

---

**Q1: What is anomaly detection in the context of data quality?**
What a good answer covers:
- Anomaly detection identifies records or batches where values fall outside the expected normal range, signaling a potential data quality problem or a genuine business event
- In `c005_anomaly_detection_demo.py`, the daily revenue total is compared to a baseline range (`BASELINE_AVG ± BASELINE_TOLERANCE`); values outside this range are flagged as FAIL
- Anomaly detection complements rule-based checks (null checks, schema validation) by catching unexpected but structurally valid data
Why this is asked: Tests whether the candidate understands that rule-based quality checks alone miss statistical anomalies.

**Q2: What is the difference between a threshold-based anomaly check and a statistical anomaly check?**
What a good answer covers:
- Threshold-based: a fixed upper and lower bound (e.g., revenue must be between 800 and 1200); simple, interpretable, but requires manual calibration
- Statistical: bounds are computed from historical data (mean ± N standard deviations, IQR); adapts automatically as the data distribution shifts
- `c005_anomaly_detection_demo.py` uses a fixed baseline, which is threshold-based; a statistical approach would compute the 30-day rolling mean and standard deviation dynamically
Why this is asked: Distinguishes the simplest approach from more robust statistical methods.

**Q3: In `c005_anomaly_detection_demo.py`, `OUTLIER_DAY` has revenue of 2400 against a baseline of 800–1200. Is this always a data quality problem? What else might it indicate?**
What a good answer covers:
- The spike might be a genuine business event: a large one-time order, a promotional campaign, or a new enterprise customer
- Anomaly detection flags for human review, not for automatic rejection; a genuine business spike should be acknowledged and the baseline updated
- Automatically rejecting anomalous values would suppress real business data; the correct response is to route the flagged record for investigation before deciding to include or exclude it
Why this is asked: Tests critical thinking about the difference between data quality failures and legitimate outliers.

**Q4: What is a Z-score and how is it used in anomaly detection?**
What a good answer covers:
- A Z-score measures how many standard deviations a value is from the mean of the distribution: `Z = (value - mean) / std_dev`
- Values with |Z| > 3 are conventionally considered outliers (approximately 0.3% of normally distributed data)
- Applied to a revenue time series, a Z-score flags days that are statistically unusual relative to the historical distribution, automatically adapting as the baseline shifts
- Unlike the fixed range in `c005_anomaly_detection_demo.py`, Z-score thresholds do not require manual recalibration as the business grows
Why this is asked: Introduces the most common statistical anomaly detection primitive.

---

**Q5: Your anomaly detector flags 30% of days as anomalous because the business has seasonal patterns (December revenue is always 3x higher than July). How do you fix this?**
What a good answer covers:
- Compare each day's revenue against the same period in prior years rather than against a flat rolling average (seasonal decomposition)
- Use a year-over-year comparison: flag days where revenue deviates more than X% from the same calendar week in the prior year
- Alternatively, apply time series decomposition (STL decomposition) to separate trend, seasonality, and residual components; detect anomalies in the residual only
- Connect to the baseline approach in `c005_anomaly_detection_demo.py`: the fixed `BASELINE_AVG` would need to be replaced with a seasonally adjusted expected value
Why this is asked: Seasonal data is a ubiquitous real-world challenge that naive anomaly detectors fail on.

**Q6: A sudden zero in a daily revenue total triggers the anomaly detector. How do you distinguish between "source system was down" and "there was genuinely no revenue today"?**
What a good answer covers:
- Cross-reference the data freshness check: if the pipeline loaded no rows (or zero rows), the zero revenue is likely a pipeline or source failure, not genuine
- Check source system health logs or status APIs at the time of the failure; a zero row count with a source system outage confirms the cause
- For genuine zero-revenue days (e.g., a holiday closure), maintain a business calendar and suppress anomaly alerts for known non-business days
- Alert on both zero-row loads and zero-revenue loads as distinct signals; zero rows always warrants investigation regardless of the business calendar
Why this is asked: Distinguishes data collection failures from real business zeros — a critical operational skill.

**Q7: How would you apply anomaly detection to column-level statistics (null rates, value distributions) rather than just aggregate metrics like revenue totals?**
What a good answer covers:
- Compute per-column statistics on each batch: null rate, distinct value count, min, max, mean, and standard deviation
- Store these statistics in a quality metrics table and build a rolling baseline per column (last 30 batches)
- Flag columns where any statistic deviates beyond N standard deviations from its baseline; alert with the specific column and metric that changed
- A sudden null rate spike in `customer_id` is as important as a revenue spike; column-level anomaly detection catches upstream schema or data capture issues early
Why this is asked: Extends aggregate anomaly detection to a more granular, scalable quality monitoring approach.

**Q8: An e-commerce platform processes orders from 50 countries. Daily revenue anomalies in one country should not trigger alerts for all countries. How do you design a multi-dimensional anomaly detector?**
What a good answer covers:
- Compute separate baselines per dimension slice (country, product category, channel); detect anomalies within each slice independently
- This requires O(dimensions × slices) baseline records; the quality metrics table must be partitioned efficiently to support this scale
- Aggregate-level anomalies (total revenue) may mask or be caused by a single slice anomaly; display both the aggregate and the contributing slice in alerts
- Connect to the data freshness topic: if a country's data is missing entirely, it appears as a revenue drop anomaly — freshness checks and anomaly detection work together to distinguish the two causes
Why this is asked: Multi-dimensional detection is a practical scaling requirement for any global data platform.

---

**Q9: Design an anomaly detection system that handles both sudden spikes (revenue doubles in one day) and slow drift (revenue grows 0.5% per day above trend for 60 days), with different alert severities for each.**
What a good answer covers:
- For spikes: Z-score against a short rolling window (7–14 days); a Z > 3 on a 7-day window detects sudden deviations quickly; alert severity = high
- For drift: apply a linear regression trend line over 90 days; alert when the actual value diverges from the predicted trend by more than X% for 5 consecutive days; alert severity = medium (requires sustained deviation to fire)
- Run both detectors in parallel; a single day can trigger both if a spike occurs on top of an existing drift
- Alert payload includes the detection method, the baseline value, the observed value, and the consecutive-days-in-drift count so responders have context immediately
Why this is asked: Spike and drift are fundamentally different anomaly patterns requiring different statistical approaches; senior candidates must handle both.

**Q10: You need to detect anomalies in real-time on a Kafka stream of order events, not on daily batch aggregates. How does the anomaly detection architecture change?**
What a good answer covers:
- Compute rolling statistics (count, sum, running mean, running std dev) on micro-batch windows in Flink or Spark Structured Streaming
- Anomaly detection runs on each micro-batch result (e.g., every 1-minute window) rather than on a daily aggregate
- The baseline must be a sliding window of recent micro-batch statistics, not a daily history; exponential moving averages adapt quickly to legitimate trend shifts
- Alert latency must be designed for: a spike in a 1-minute window should trigger an alert within seconds, not after the daily report runs
- Connect to the watermarks topic (`c003_watermarks_demo.py`): the anomaly detection window is bounded by the stream's watermark; late-arriving events may retroactively affect a closed window's statistics
Why this is asked: Real-time anomaly detection connects the data quality track to the streaming architecture track.

**Q11: An anomaly detector generates 500 alerts per day, 95% of which are false positives from expected business events. The on-call team has stopped responding to alerts. Design a remediation plan.**
What a good answer covers:
- Audit all 500 alerts over the past 30 days; categorize each as true positive, known-business-event false positive, or unexplained false positive
- For known business events: build a business calendar and suppress alerts for expected events (promotions, holidays, new product launches)
- For systematic false positives: recalibrate thresholds using the classification audit; tighten the anomaly definition to reduce noise
- Introduce alert tiering: only page on-call for high-confidence anomalies (Z > 4, no business calendar explanation); route medium-confidence anomalies to a daily digest
- Track the alert-to-true-positive ratio as a quality metric for the anomaly detection system itself; target >50% precision before the team re-engages with the alert channel
Why this is asked: Alert fatigue from poorly calibrated anomaly detectors is a real production problem; this tests whether the candidate can fix it systematically.

---

**Q12: An ML model is producing predictions that suddenly degrade in accuracy. The root cause turns out to be a data quality anomaly in the training feature pipeline that was never detected. Design a retroactive anomaly detection system that could have caught this.**
What a good answer covers:
- Instrument the feature pipeline to log per-feature statistics (mean, std dev, null rate, distribution percentiles) for every training batch to a feature quality table
- Build an anomaly detector that compares each batch's feature statistics to the historical baseline; flag batches where any feature's distribution shifts significantly
- Correlate feature quality anomalies with model performance metrics: if a feature distribution shift precedes a model accuracy drop by N days, that feature is a leading indicator
- Connect to the ML model versioning system: annotate each model version with the quality status of the training data used; a model trained on anomalous data is tagged for review before deployment
- Connect to `c005_anomaly_detection_demo.py`: the same baseline-vs-actual check applied to revenue totals can be applied to feature distributions
Why this is asked: ML data quality monitoring is a cross-track architect-level scenario connecting data quality to model reliability.

**Q13: Your anomaly detection system must comply with model explainability requirements: every anomaly alert must include a human-readable explanation of why the value was flagged, traceable to the source data. Design the explainability layer.**
What a good answer covers:
- Each alert payload includes: the detected value, the baseline range or distribution, the statistical method used (Z-score, IQR, trend), and the contributing raw rows (sample of records that drove the anomalous aggregate)
- Store contributing row IDs in the alert record with a reference to the raw layer so analysts can drill down from alert to source data without additional investigation
- For multi-dimensional anomalies, include a breakdown showing which dimension slice contributes most to the deviation (e.g., "France accounts for 80% of the spike")
- For regulatory use cases, generate a signed audit document per alert that records the baseline computation inputs, detection algorithm version, and alert decision — immutable for the retention period
- Connect to data contracts: the explainability requirement is a clause in the data quality SLA that the anomaly detection system must contractually satisfy
Why this is asked: Explainable anomaly detection is an architect-level requirement in regulated industries where "the algorithm flagged it" is not an acceptable audit response.
