# Interview Questions — Orchestration

> Topics covered: DAG concepts · scheduling and triggers · retry and failure handling · backfill patterns · idempotent tasks
> Levels: Starter | Mid | Senior | Architect

---

## DAG Concepts

### Starter

**Q1: In c001_dag_concepts_demo.py, `transform_sales` lists `extract_orders` and `extract_payments` as dependencies. What does this mean for execution order?**
What a good answer covers:
- `transform_sales` cannot start until both upstream tasks have completed successfully
- The two extract tasks have no dependencies on each other and can run in parallel
- This dependency chain ensures the transformation always has both inputs available
Why this is asked: reading a dependency graph is the first skill needed to reason about any DAG-based pipeline.

**Q2: What does DAG stand for, and why must a pipeline DAG be acyclic?**
What a good answer covers:
- DAG stands for Directed Acyclic Graph
- Directed means dependencies flow in one direction; acyclic means there are no circular dependencies
- A cycle would mean a task depends on itself (directly or indirectly), making execution order impossible to resolve
Why this is asked: the acyclic constraint is foundational and its violation causes scheduling deadlocks.

**Q3: In c001_dag_concepts_demo.py, what would happen if `publish_report` failed? Which tasks would be affected?**
What a good answer covers:
- `notify_slack` depends on `publish_report` and would be blocked from running
- Tasks earlier in the chain (extract, transform, validate) would already be complete and unaffected
- The DAG would end in a partially completed state with downstream tasks marked as not run
Why this is asked: tracing failure propagation through a dependency graph is a core operational skill.

**Q4: What is the difference between a task and a DAG run in an orchestration framework like Airflow?**
What a good answer covers:
- A task is a single unit of work defined in the DAG (e.g., extract_orders)
- A DAG run is one execution instance of the entire DAG for a specific scheduled interval or trigger
- Multiple DAG runs can be in flight simultaneously (e.g., yesterday's run and today's run)
Why this is asked: distinguishing the definition from the execution instance prevents confusion when diagnosing failures.

### Mid

**Q5: Looking at c001_dag_concepts_demo.py, how would you add a task that sends a failure alert only if `validate_report` fails, without blocking the rest of the pipeline?**
What a good answer covers:
- Use a trigger rule (e.g., `trigger_rule=TriggerRule.ONE_FAILED` in Airflow) on an alert task
- The alert task depends on `validate_report` but uses the failure trigger rule so it only runs on failure
- The alert task does not block `publish_report` — it is a separate branch with no downstream dependents in the happy path
Why this is asked: conditional branching for alerting is a common real-world pattern.

**Q6: What is a critical path in a DAG, and why does it matter for pipeline SLA management?**
What a good answer covers:
- The critical path is the longest sequence of dependent tasks from start to finish
- Total pipeline duration cannot be shorter than the critical path's total runtime
- Optimizing tasks off the critical path does not reduce overall pipeline latency
Why this is asked: SLA management requires identifying which tasks actually determine end-to-end duration.

**Q7: How do you handle a DAG that has grown to over 200 tasks and is becoming difficult to maintain?**
What a good answer covers:
- Split the DAG into sub-DAGs or use task groups to organize related tasks visually and logically
- In Airflow 2+, TaskGroups replace SubDAGs for grouping without spawning separate DAG runs
- Consider whether some tasks belong in a separate DAG triggered by the parent (ExternalTaskSensor or DAG triggering)
- Document the purpose of each section with clear naming conventions
Why this is asked: DAG sprawl is a real maintenance problem in mature data platforms.

**Q8: What is a fan-out pattern in a DAG, and what are its risks at scale?**
What a good answer covers:
- Fan-out is when one task spawns many parallel downstream tasks (e.g., one task per customer or date partition)
- Dynamic task mapping (Airflow 2.3+) or generating tasks programmatically implements this pattern
- At scale, fan-out can overwhelm the scheduler, worker pool, or target system with concurrent requests
- Worker pool limits, rate limiting, and dynamic task count caps are used to control fan-out safely
Why this is asked: fan-out is a common pattern that becomes a stability risk if not designed with limits.

### Senior

**Q9: The finance report DAG in c001_dag_concepts_demo.py runs daily. A new requirement asks it to also run on-demand when triggered by an upstream system. How do you redesign the DAG to support both modes?**
What a good answer covers:
- Use a dataset-driven trigger or an external trigger (API call, message queue event) in addition to the cron schedule
- Parameterize the execution date so both scheduled and triggered runs process the correct date range
- Ensure the DAG is idempotent so a scheduled run and a triggered run for the same date do not conflict
- Monitoring must distinguish scheduled runs from triggered runs for SLA tracking
Why this is asked: hybrid scheduling is a real requirement as pipelines become event-driven.

**Q10: How would you design a DAG that processes daily data but must respect an upstream system's maintenance window from 02:00 to 04:00 UTC?**
What a good answer covers:
- Schedule the DAG to start after 04:00 UTC to avoid the maintenance window entirely
- Alternatively, add a sensor task at the start of the DAG that waits for the upstream system to become available
- Include a timeout on the sensor so the DAG fails alertably if the upstream system does not recover
- Document the maintenance window dependency in the DAG description and on-call runbook
Why this is asked: real pipelines must account for external system constraints.

**Q11: What is a DAG's `max_active_runs` setting, and what problem does it prevent?**
What a good answer covers:
- `max_active_runs` limits how many DAG runs of the same DAG can execute concurrently
- Without a limit, a slow DAG can accumulate many overlapping runs that compete for resources and write to the same targets
- Setting it to 1 enforces sequential runs; higher values allow controlled parallelism for backfill scenarios
- The right value depends on whether the DAG's tasks are idempotent and whether target systems can handle concurrent writes
Why this is asked: concurrency limits are a critical operational setting that candidates must understand.

### Architect

**Q12: How do you design a DAG orchestration layer that supports reliable ELT pipelines where transformations run inside the warehouse (e.g., dbt) and ingestion is handled by a separate tool?**
What a good answer covers:
- The orchestrator (Airflow, Prefect, Dagster) acts as the control plane: it triggers ingestion jobs, monitors completion, then triggers dbt model runs
- Dependency between ingestion and transformation is expressed as task dependencies in the DAG
- Data freshness checks (sensors or source freshness assertions) replace time-based waits for more reliable triggering
- Failures in dbt models are surfaced back to the orchestrator and treated as task failures for consistent alerting and retry
Why this is asked: ELT orchestration across multiple tools is the dominant pattern in modern data stacks.

**Q13: A streaming pipeline feeds a real-time feature store, and a daily DAG pipeline feeds a batch feature store. How do you architect the orchestration layer to serve both while maintaining consistency between the two stores?**
What a good answer covers:
- The orchestrator manages the daily batch pipeline and coordinates reconciliation jobs between batch and streaming stores
- A scheduled reconciliation DAG compares batch and streaming feature values at the end of each day and flags divergence
- The streaming system publishes checkpoints or watermarks that the orchestrator can read before triggering batch runs that depend on streaming completeness
- Transactional semantics are enforced at the feature store level; the orchestrator ensures ordering but not atomicity across stores
Why this is asked: hybrid batch/streaming architectures require careful coordination between two fundamentally different execution models.

---

## Scheduling and Triggers

### Starter

**Q1: What is a cron expression, and what does `0 6 * * *` schedule?**
What a good answer covers:
- A cron expression defines a recurring schedule using five fields: minute, hour, day-of-month, month, day-of-week
- `0 6 * * *` runs at 06:00 every day
- Cron is the most common scheduling mechanism in orchestration frameworks
Why this is asked: reading and writing cron expressions is a baseline operational skill.

**Q2: What is the difference between a schedule-based trigger and an event-based trigger in a pipeline orchestrator?**
What a good answer covers:
- Schedule-based: the DAG runs at a fixed time regardless of whether new data has arrived
- Event-based: the DAG runs when a specific event occurs (file arrival, message on a queue, upstream DAG completion)
- Event-based triggers are more responsive and avoid running when there is nothing to process
Why this is asked: choosing the right trigger type affects pipeline reliability and resource efficiency.

**Q3: What is Airflow's `execution_date` (or `data_interval_start`), and why does it matter for a daily pipeline?**
What a good answer covers:
- `execution_date` represents the start of the data interval the DAG run is processing, not the time the run actually started
- A DAG scheduled at midnight processes the previous day's data, so execution_date is yesterday's date
- Code that uses `execution_date` to construct filenames or SQL date filters must understand this offset
Why this is asked: confusion about execution_date vs run time is one of the most common bugs in Airflow pipelines.

**Q4: What happens if an orchestrator is down for four hours during a time when three scheduled DAG runs were supposed to start?**
What a good answer covers:
- When the orchestrator recovers, it detects the missed runs and may schedule them as catch-up runs
- Whether catch-up runs execute depends on the `catchup` setting on the DAG
- If `catchup=False`, missed runs are skipped and only the most recent run executes
Why this is asked: catch-up behavior is critical to understand for operational reliability.

### Mid

**Q5: How do you design a pipeline that should only run when new source data has actually arrived, rather than on a fixed schedule?**
What a good answer covers:
- Use a sensor task (S3KeySensor, FileSensor, or ExternalTaskSensor) as the first task in the DAG to poll for the arrival condition
- In Airflow 2.4+, use dataset-driven scheduling where the DAG is triggered when an upstream task marks a dataset as updated
- Set a timeout on the sensor and a failure callback to alert if data does not arrive within the SLA window
Why this is asked: event-driven designs reduce wasted runs and improve SLA alignment with source systems.

**Q6: What is a sensor task, and what are the trade-offs between poke mode and reschedule mode?**
What a good answer covers:
- A sensor repeatedly checks a condition and holds the task slot until the condition is met
- Poke mode: the sensor occupies a worker slot continuously, checking at intervals — wastes resources for long waits
- Reschedule mode: the sensor releases the worker slot between checks and wakes up on a schedule — more efficient for long polling windows
Why this is asked: choosing the wrong sensor mode can exhaust worker slots and starve other tasks.

**Q7: How do you handle a downstream DAG that must wait for multiple independent upstream DAGs to complete before running?**
What a good answer covers:
- Use ExternalTaskSensor tasks, one per upstream DAG, as dependencies at the start of the downstream DAG
- All sensors must succeed before the first processing task is allowed to run
- In Airflow 2.4+, dataset-based scheduling can trigger a DAG when all required datasets have been updated
Why this is asked: cross-DAG dependencies are common in real data platforms and must be handled explicitly.

**Q8: A DAG runs every hour, but the last task — loading to the data warehouse — must not run between 06:00 and 08:00 UTC due to a reporting batch window. How do you implement this constraint?**
What a good answer covers:
- Add a TimeDeltaSensor or a custom sensor before the load task that checks the current UTC hour
- Alternatively, split the DAG: run extraction and transformation hourly, but schedule the load task to a separate DAG that runs outside the restricted window
- Document the business reason for the constraint in the DAG and the load task description
Why this is asked: time-window constraints are a real operational requirement that tests creative use of scheduling primitives.

### Senior

**Q9: How do you implement a priority-based scheduling system in Airflow when some DAGs are business-critical and others are best-effort?**
What a good answer covers:
- Assign priority weights to tasks and DAGs — higher weight tasks get scheduled before lower weight tasks when workers are contiguous
- Use separate worker queues for critical versus best-effort workloads and route tasks to the appropriate queue
- Monitor queue depth and worker utilization to verify that critical tasks are not starved by best-effort work
Why this is asked: resource contention is real in shared orchestration environments and must be managed explicitly.

**Q10: How do you design scheduling for a pipeline that processes data from multiple time zones where "end of business day" differs by region?**
What a good answer covers:
- Define a canonical UTC schedule and parameterize the business day cutoff per region as a configuration variable
- Run one DAG per region with a schedule offset corresponding to that region's end-of-business hour in UTC
- Alternatively, use a single parameterized DAG triggered by events from each region's source system rather than a time-based schedule
Why this is asked: multi-timezone scheduling is a common international data engineering problem.

**Q11: What is dynamic DAG generation, and what are its maintainability risks?**
What a good answer covers:
- Dynamic DAG generation creates DAG structures programmatically at parse time (e.g., one DAG per client, per table, or per config entry)
- Risks: the scheduler must re-parse DAGs frequently; bugs in the generation logic affect all generated DAGs simultaneously; debugging requires understanding two layers of code
- Best practice is to limit dynamic generation to task-level (dynamic task mapping) rather than DAG-level where possible
Why this is asked: dynamic generation is widely used but often over-applied in ways that harm observability and stability.

### Architect

**Q12: Design a scheduling architecture for a global data platform where regional pipelines must complete before a global aggregation DAG runs, and failures in any region must not block the global run indefinitely.**
What a good answer covers:
- Each regional pipeline signals completion by updating a shared status table or marking a dataset
- The global aggregation DAG uses sensors with defined timeouts to wait for each region
- Regions that fail their timeout are marked as missing and excluded from the current global run with an alert, rather than blocking indefinitely
- A reconciliation job runs after the global aggregation to reprocess any missed regions once they recover
Why this is asked: global aggregation with partial failure tolerance is an architectural challenge that requires explicit design decisions.

**Q13: How do you design a scheduling and trigger system that bridges a batch orchestration layer (Airflow) and a streaming platform (Kafka) so that batch jobs can be triggered by stream processing milestones without tight coupling?**
What a good answer covers:
- The streaming system publishes completion events to a dedicated Kafka topic or a control table when a processing milestone is reached (e.g., all events for a partition are committed)
- A lightweight sensor DAG in Airflow polls the control table or consumes the topic and triggers downstream batch DAGs
- The contract between the streaming system and the orchestrator is the control record schema — neither system knows implementation details of the other
- This decoupling allows the streaming and batch layers to evolve independently while maintaining reliable handoff
Why this is asked: streaming-to-batch handoffs are increasingly common and require careful interface design to avoid brittle coupling.

---

## Retry and Failure Handling

### Starter

**Q1: In c003_retry_failure_demo.py, the function `_run_with_retry` distinguishes between `non_retryable` and retryable failures. Why is this distinction important?**
What a good answer covers:
- Retrying a non-retryable failure (e.g., authentication error, invalid data) wastes time and delays alerting
- Retrying a transient failure (network timeout, temporary resource unavailability) may succeed on the next attempt
- Correct classification reduces mean time to resolution and avoids masking permanent errors
Why this is asked: directly tests reading comprehension of the demo and understanding of retry design rationale.

**Q2: What are common examples of retryable versus non-retryable failures in a data pipeline?**
What a good answer covers:
- Retryable: network timeouts, API rate limits (429), temporary database connection failures, brief cloud service outages
- Non-retryable: authentication failures (401/403), data validation errors, missing required columns, disk full errors
- The classification depends on whether the root cause can resolve itself without human intervention
Why this is asked: every data engineer must be able to classify failures correctly to design appropriate retry behavior.

**Q3: What is exponential backoff, and why is it preferred over a fixed retry interval?**
What a good answer covers:
- Exponential backoff increases the wait time between retries geometrically (e.g., 1s, 2s, 4s, 8s)
- Fixed intervals can swamp a recovering system with retry storms if many tasks retry simultaneously
- Exponential backoff with jitter (randomized delay) spreads retries across time, reducing thundering herd effects
Why this is asked: retry storm mitigation is a production reliability concern that tests operational experience.

**Q4: In c003_retry_failure_demo.py, `_block_if_failed` prevents a task from running if its dependencies did not succeed. Why is this blocking behavior correct?**
What a good answer covers:
- Running a task whose inputs are incomplete or corrupt produces meaningless or wrong outputs
- Blocking downstream tasks makes the failure visible at the correct point in the pipeline
- It prevents a bad result from propagating to reports, dashboards, or downstream systems
Why this is asked: dependency-aware failure propagation is core to DAG-based orchestration safety.

### Mid

**Q5: How do you configure different retry behavior for different tasks in the same DAG — for example, an API call task that should retry three times with exponential backoff, versus a SQL task that should never retry?**
What a good answer covers:
- In Airflow, retry settings (`retries`, `retry_delay`, `retry_exponential_backoff`) are set per task, not at DAG level
- The API task gets `retries=3, retry_exponential_backoff=True`; the SQL task gets `retries=0`
- Custom retry logic can also be implemented inside the task's Python function for more fine-grained control
Why this is asked: per-task retry configuration is a real implementation requirement.

**Q6: A pipeline's extract task fails at 02:00 AM. What information should a good alert contain, and how do you ensure on-call engineers have what they need to diagnose the issue quickly?**
What a good answer covers:
- Alert should include: DAG name, task name, execution date, error message, link to logs, number of retries attempted
- On-call runbook link and escalation contact should be included in the alert body
- Structured log output with context variables (table name, row count, source system) makes diagnosis faster
Why this is asked: alert quality directly affects mean time to resolution for production incidents.

**Q7: How does c003_retry_failure_demo.py's `_block_if_failed` function relate to Airflow's `TriggerRule` concept?**
What a good answer covers:
- `_block_if_failed` manually checks upstream state; Airflow's TriggerRule encodes the same logic declaratively in the DAG definition
- Default trigger rule is ALL_SUCCESS — a task only runs if all upstream tasks succeeded
- Other trigger rules (ALL_DONE, ONE_FAILED, NONE_FAILED_MIN_ONE_SUCCESS) handle branching and notification patterns
Why this is asked: connects the demo's manual implementation to the framework's built-in abstraction.

**Q8: What is the difference between a task failure and a task timeout, and how should each be handled differently?**
What a good answer covers:
- Task failure: the task raised an exception or returned a failure code — may be retryable or non-retryable
- Task timeout: the task exceeded its allowed execution time — often caused by a hung query or lock contention
- Timeouts should trigger a hard kill and an alert; long-running tasks may need different timeout thresholds than short ones
- Both should be tracked separately in monitoring to identify systemic problems (too many timeouts = query performance issue)
Why this is asked: distinguishing failure modes leads to more targeted operational responses.

### Senior

**Q9: Design a retry strategy for a pipeline that writes to both a database and an external API, where a partial success (database written, API failed) leaves data in an inconsistent state.**
What a good answer covers:
- Separate the database write and API call into distinct tasks with their own retry policies
- If the API fails after a successful database write, the retry must be idempotent — the database write should not be duplicated
- Use a status column in the database to track whether the API call completed; the retry logic checks this before re-writing
- Consider a compensating transaction (rollback or soft-delete) if the API consistently fails and consistency must be restored
Why this is asked: partial success in multi-system writes is one of the hardest reliability problems in data engineering.

**Q10: How do you implement a dead-letter queue pattern in a data pipeline to preserve failed records for later inspection and reprocessing?**
What a good answer covers:
- Failed records are written to a separate dead-letter table or storage path rather than being silently dropped or blocking the pipeline
- Each dead-letter record captures the original payload, the error message, and the timestamp
- A separate remediation pipeline processes dead-letter records after the root cause is fixed
- Alerting fires when the dead-letter queue exceeds a threshold, and SLAs define the maximum acceptable lag
Why this is asked: dead-letter patterns are essential for pipelines that cannot afford to block on individual record failures.

**Q11: A critical pipeline fails on the third of five tasks. The first two tasks have already written data to intermediate staging tables. How do you design the recovery so that the next run does not re-execute the first two tasks unnecessarily?**
What a good answer covers:
- Use a completion marker (e.g., a status record in a control table or a sentinel file) that each task writes on success
- On re-run, tasks check for their completion marker before executing — if it exists, they skip and mark themselves successful
- This is the checkpoint pattern; it requires each task to be idempotent within its own scope
- Airflow's task state persistence handles this automatically for successful task runs within the same DAG run
Why this is asked: avoiding redundant re-execution is important for long pipelines with expensive tasks.

### Architect

**Q12: Design a failure handling architecture for a high-value financial pipeline where any undetected data error reaching the reporting layer could result in regulatory fines. How do you layer validation, retry, and alerting to provide defense in depth?**
What a good answer covers:
- Layer 1: Source validation — schema checks, null checks, and row count assertions before any transformation begins
- Layer 2: Transformation validation — dbt tests or custom assertions after each transformation step; failures halt the pipeline
- Layer 3: Pre-publish validation — reconcile aggregated totals against known control figures before writing to the reporting layer
- Retry policy is aggressive for transient infrastructure errors but zero-retry for data validation failures (non-retryable)
- Alerting is tiered: validation warnings go to the data team; validation failures that halt the pipeline page on-call
- An audit log records every run's validation results and the data lineage of every published report
Why this is asked: defense-in-depth for financial pipelines is an architectural design problem that tests judgment about where to place controls.

**Q13: How do you design a failure handling strategy for a streaming pipeline that feeds a real-time dashboard, where a failure in the enrichment step (joining stream events to a slow-changing dimension table) must not cause dashboard outages but also must not serve stale enrichment data indefinitely?**
What a good answer covers:
- Maintain a last-known-good cache of the enrichment dimension; on enrichment failure, serve from cache with a staleness indicator
- Define a maximum staleness SLA (e.g., 15 minutes) after which the dashboard shows a data freshness warning rather than cached data
- The enrichment pipeline retries independently with exponential backoff; recovery is automatic when the dimension table becomes available
- A transactional commit to the dashboard's backing store ensures consumers never see a partially enriched batch
- Staleness events are logged and feed into a separate SLA monitoring dashboard for the data engineering team
Why this is asked: real-time pipelines require failure modes that degrade gracefully rather than failing hard, which is an architectural trade-off between availability and data correctness.

---

## Backfill Patterns

### Starter

**Q1: What is a backfill in the context of data pipeline orchestration?**
What a good answer covers:
- A backfill is the process of running a pipeline for historical date ranges that were not processed during normal scheduled operation
- Common reasons: pipeline was not deployed yet, historical data was made available retroactively, or a bug was fixed and old data needs reprocessing
- Backfills use the same pipeline code as normal runs, parameterized by a different execution date
Why this is asked: backfill is a standard operational concept every data engineer encounters.

**Q2: In Airflow, what does the `catchup` parameter on a DAG control?**
What a good answer covers:
- When `catchup=True`, Airflow creates DAG runs for all missed scheduled intervals since the DAG's start_date
- When `catchup=False`, only the most recent scheduled run is created when the DAG is first activated or resumed after a pause
- Leaving `catchup=True` on a DAG with an old start_date can trigger hundreds of unexpected runs on first deployment
Why this is asked: catchup misconfiguration is one of the most common Airflow deployment mistakes.

**Q3: Why is it important for a pipeline task to use the execution date (rather than the current date) when filtering source data during a backfill?**
What a good answer covers:
- A task running as a backfill for 30 days ago must process data from 30 days ago, not today's data
- Using `{{ ds }}` (Airflow's execution date template variable) ensures the correct date range is queried
- Hardcoding `TODAY()` or `CURRENT_DATE` causes backfill runs to produce incorrect or duplicate results
Why this is asked: execution-date-parameterized queries are the prerequisite for any pipeline to be backfillable.

**Q4: What are the risks of running a backfill on a pipeline that was not designed with backfill in mind?**
What a good answer covers:
- Duplicate data if INSERT operations are not idempotent (not checking for existing rows before inserting)
- Incorrect date ranges if the pipeline uses wall-clock time instead of execution date
- Target system overload if many backfill runs execute concurrently against the same database
Why this is asked: understanding backfill risks motivates designing pipelines correctly from the start.

### Mid

**Q5: How do you safely run a backfill for 90 days of historical data without overwhelming the target database or downstream systems?**
What a good answer covers:
- Set `max_active_runs` to a low number (e.g., 3–5) to limit concurrent backfill DAG runs
- Run the backfill during off-peak hours to avoid competing with production queries
- Monitor target system resource utilization (CPU, I/O, connection count) during the backfill and pause if thresholds are breached
Why this is asked: backfill execution is an operational exercise that requires resource-aware planning.

**Q6: A backfill for a pipeline that writes to a partitioned table by date needs to re-run 60 days. How do you ensure each run only writes to its own partition without affecting other partitions?**
What a good answer covers:
- Use partition overwrite mode: the write operation replaces only the partition matching the execution date
- Most warehouse engines (BigQuery, Spark, Delta Lake) support dynamic partition overwrite
- Verify that the pipeline's write mode is `overwrite partition` not `overwrite table` before running the backfill
Why this is asked: partition-safe writes are the foundational mechanism for backfill correctness in partitioned tables.

**Q7: How do you validate that a backfill completed correctly and that the resulting data is consistent with what a normal pipeline run would have produced?**
What a good answer covers:
- Compare row counts and aggregate totals for backfilled partitions against source system control figures
- Run the same data quality checks that run on normal pipeline outputs (dbt tests, Great Expectations, custom assertions)
- For critical pipelines, run a parallel normal-schedule run and diff the outputs before promoting the backfill results
Why this is asked: backfill validation is often skipped and leads to silent data quality regressions.

**Q8: A code change to a transformation logic was deployed two weeks ago. The business now realizes the old logic was correct and wants the last two weeks of data reverted to the pre-change output. How do you approach this?**
What a good answer covers:
- Roll back or branch the code to the pre-change version
- Identify all partitions or date ranges affected by the bad logic
- Run a backfill using the rolled-back code to overwrite the affected partitions
- Validate the reverted data matches the expected output and notify stakeholders of the resolution timeline
Why this is asked: code-driven data regressions requiring backfill are a real operational scenario.

### Senior

**Q9: Design a backfill management system for a data platform with 50+ DAGs where backfills are run regularly due to frequent source data corrections.**
What a good answer covers:
- Build a backfill request interface (CLI or UI) that records the DAG name, date range, requester, and reason in a control table
- Automatically set `max_active_runs` and pool limits for backfill-tagged runs to prevent resource contention with production
- Generate a completion report when the backfill finishes, summarizing rows written, validation results, and duration
- Implement a backfill history log for auditing and to identify which DAGs require frequent backfills (a signal of upstream data quality issues)
Why this is asked: at scale, ad hoc backfills become a platform management problem requiring systematic tooling.

**Q10: How do you handle a backfill for a pipeline that includes an API call to an external system that rate-limits requests and does not support historical queries?**
What a good answer covers:
- If the external API cannot provide historical data, a true backfill is not possible — acknowledge this limitation explicitly
- If the API has some historical access, implement request pacing (sleep between calls) and exponential backoff to respect rate limits
- Consider whether the API call is necessary for historical data or whether a cached/snapshot source can substitute
- For future protection, log API responses to a raw storage layer so historical data is available for future backfills
Why this is asked: external system constraints often break the assumption that backfills are straightforward replays.

**Q11: How does the backfill pattern interact with a SCD Type 2 dimension — specifically, how do you backfill a fact table that must join to the correct historical version of the dimension?**
What a good answer covers:
- The SCD Type 2 dimension must already contain the correct historical rows covering the backfill date range before the backfill runs
- If the dimension history was also incorrect, backfill the dimension first, then backfill the fact table
- Fact rows loaded during backfill must resolve surrogate keys against the dimension version current at the execution date, not the current version
- Validate post-backfill that fact-to-dimension joins resolve correctly across all affected dates
Why this is asked: SCD Type 2 and backfill interact in ways that cause subtle correctness bugs if not explicitly managed.

### Architect

**Q12: A regulatory audit requires re-running three months of a financial transaction pipeline using an updated calculation methodology, while ensuring the original output is preserved for comparison. Design the architecture for this re-processing.**
What a good answer covers:
- Write the backfill output to a separate schema or table suffix (e.g., `fact_transactions_v2`) while preserving the original
- Run both versions in parallel for a validation period, comparing outputs row by row for material differences
- Once validated and approved by finance and compliance, swap the reporting layer to point to the new version
- Archive the original output to cold storage for the audit trail retention period required by the regulation
- Document the methodology change, the validation results, and the cutover date in a data change log
Why this is asked: regulated re-processing requires both technical correctness and governance discipline, testing whether the candidate thinks beyond just "run the backfill."

**Q13: How do you design a backfill system for a pipeline that writes to both a transactional database (PostgreSQL) and a streaming output (Kafka topic), where downstream consumers of the Kafka topic must also reprocess historical data?**
What a good answer covers:
- The backfill pipeline writes corrected records to PostgreSQL using partition-safe upserts
- For Kafka, produce corrected records with a `backfill=true` header and the original event timestamp so consumers can distinguish backfill from live traffic
- Downstream consumers that maintain materialized state (aggregations, feature stores) must replay their own logic over the backfill events
- Coordinate the backfill start time with all downstream consumer teams so they can prepare their replay logic before messages arrive
- A compacted Kafka topic or a replay-capable event store (e.g., Kafka with long retention) makes this pattern feasible without re-publishing to live topics
Why this is asked: backfilling into a streaming architecture requires designing for downstream consumer impact, which tests end-to-end system thinking.

---

## Idempotent Tasks

### Starter

**Q1: What does it mean for a pipeline task to be idempotent?**
What a good answer covers:
- An idempotent task produces the same result whether it is run once or multiple times with the same inputs
- Re-running an idempotent task after a failure does not cause duplicate data, incorrect totals, or side effects
- Idempotency is the property that makes retries and backfills safe
Why this is asked: idempotency is one of the most important design properties in data engineering.

**Q2: Why is a task that uses `INSERT INTO table SELECT ...` without deduplication not idempotent?**
What a good answer covers:
- If the task runs twice, two copies of every row are inserted, doubling row counts and aggregated totals
- A subsequent deduplication step could recover the data, but the task itself caused a correctness problem
- Idempotent alternatives: `INSERT OVERWRITE`, `MERGE`, or `DELETE WHERE date = X` followed by `INSERT`
Why this is asked: INSERT without deduplication is the most common source of non-idempotent pipeline bugs.

**Q3: What is the difference between `INSERT OVERWRITE` (or partition overwrite) and `INSERT INTO` in terms of idempotency?**
What a good answer covers:
- `INSERT OVERWRITE` replaces all data for the target partition — running it twice produces the same final state
- `INSERT INTO` appends rows — running it twice doubles the row count for that partition
- `INSERT OVERWRITE` is the standard approach for idempotent daily partition writes in most warehouse systems
Why this is asked: insert strategy is the most direct implementation decision affecting idempotency.

**Q4: Name two real-world scenarios where a non-idempotent task in a pipeline caused or could cause a data quality incident.**
What a good answer covers:
- Scenario 1: A retry after a transient network error causes the same invoice rows to be inserted twice, inflating revenue figures
- Scenario 2: A backfill using `INSERT INTO` appends duplicate historical data, corrupting cumulative metrics
- In both cases, the bug is not immediately visible and may only surface during reconciliation or audit
Why this is asked: grounding the concept in consequences motivates engineers to take idempotency seriously.

### Mid

**Q5: How do you make a task that calls an external API idempotent when the API does not natively support idempotent requests?**
What a good answer covers:
- Record each API call and its result in a local state table (e.g., `api_call_log`) keyed by the request parameters
- On re-run, check the log before making the call — if a successful result exists, return the cached result and skip the API call
- Ensure the state table write and the API call are sequenced correctly: log the intent before calling, update the log with the result after
Why this is asked: external API idempotency is harder than database idempotency and tests practical design skill.

**Q6: How would you redesign a pipeline task that sends an email notification to make it idempotent?**
What a good answer covers:
- Record the notification in a sent_notifications table with a unique key (DAG run ID, notification type, recipient)
- Before sending, check whether a record for this run already exists — if so, skip the send
- This prevents duplicate emails on retry while still ensuring the email is sent on the first successful attempt
Why this is asked: notification tasks are often non-idempotent and a common source of user-facing pipeline bugs.

**Q7: What is the role of a surrogate key or idempotency key in making a pipeline task safe to retry?**
What a good answer covers:
- An idempotency key is a unique identifier for a specific logical operation (e.g., DAG run ID + task ID + target partition)
- The target system uses the key to detect and reject duplicate requests or writes
- Generating the key deterministically from the inputs (not from a timestamp or UUID at runtime) ensures consistency across retries
Why this is asked: idempotency keys are the mechanism that enables safe retry across systems.

**Q8: How does the MERGE (UPSERT) pattern make a task idempotent for dimension or reference data loads?**
What a good answer covers:
- MERGE matches incoming rows to existing rows on a natural key
- Matching rows are updated with new attribute values; non-matching rows are inserted as new records
- Running MERGE twice with the same input produces the same final state — the second run's updates are no-ops
Why this is asked: MERGE is the standard idempotent pattern for dimension loads and candidates must understand why.

### Senior

**Q9: Design an idempotent task that writes daily sales aggregates to a summary table, ensuring that a re-run on any day never produces duplicate or inconsistent summary rows.**
What a good answer covers:
- Before writing, delete all summary rows for the execution date: `DELETE FROM summary WHERE summary_date = '{{ ds }}'`
- Then insert the freshly computed aggregates for that date
- This DELETE + INSERT pattern is atomic within a transaction and produces the same result on every run
- Alternative: use partition overwrite if the target system supports it, eliminating the need for an explicit DELETE
Why this is asked: DELETE + INSERT or partition overwrite is the most reliable pattern for aggregate idempotency.

**Q10: How do you test whether a pipeline task is truly idempotent before deploying it to production?**
What a good answer covers:
- Run the task once against a test environment; capture row counts and checksums of the output
- Run the task a second time with identical inputs; compare row counts and checksums — they must match exactly
- Test with both a clean target (first run) and a populated target (re-run scenario) to catch both insert and update bugs
- Include this idempotency test in the CI pipeline so regressions are caught before deployment
Why this is asked: idempotency is easy to claim and easy to break; verifying it through testing is a senior-level discipline.

**Q11: A pipeline team argues that adding idempotency checks (DELETE before INSERT, MERGE instead of INSERT) adds overhead and slows their pipelines. How do you make the case for idempotency, and where might you accept trade-offs?**
What a good answer covers:
- The overhead of a DELETE or MERGE is small compared to the cost of a production data incident, a backfill, and the downstream trust damage
- For very large tables, partition-scoped deletes are cheap because they only touch the relevant partition
- Acceptable trade-off: for append-only event tables where duplicates are handled by the consumer (e.g., deduplicated at query time), strict idempotency at write time may not be necessary
- Document the decision explicitly so future engineers understand the chosen approach and its constraints
Why this is asked: senior engineers must balance pragmatism with correctness and defend their design decisions.

### Architect

**Q12: How do you design an idempotency framework for a data platform where dozens of pipelines share common write targets (shared dimension tables, shared fact tables), and multiple pipelines may write to the same partition concurrently?**
What a good answer covers:
- Define a write ownership model: each partition of a shared table is owned by exactly one pipeline at a time
- Use a distributed lock (e.g., a row in a control table with a pipeline ID and expiry) to prevent concurrent writes to the same partition
- Pipelines must acquire the lock before writing and release it after committing; a lock expiry handles crashed pipelines
- Standardize the idempotency pattern (partition overwrite with lock) as a platform library so individual pipeline authors do not implement it ad hoc
Why this is asked: shared write targets require coordination mechanisms that go beyond single-pipeline idempotency.

**Q13: In an ELT architecture where transformations run as SQL inside the warehouse (e.g., dbt), how do you design the idempotency and transactional guarantees for a pipeline that must atomically update three related tables — a fact table, a summary table, and an audit log — as part of a single logical operation?**
What a good answer covers:
- Wrap all three writes in an explicit warehouse transaction if the engine supports multi-statement transactions (Snowflake, PostgreSQL, BigQuery with BEGIN/COMMIT)
- If the warehouse does not support cross-table transactions, use a two-phase commit pattern: write to staging tables for all three, then atomically swap staging to production using table rename or pointer update
- The audit log write must be the last operation before commit so it reflects the final committed state
- dbt's `on-run-end` hooks or post-hooks can trigger the audit log write after the model materialization commits
- Test the transactional boundary explicitly: simulate a failure mid-way and verify that none, not two of three, tables are updated
Why this is asked: transactional consistency across multiple tables in a warehouse is an architect-level concern that connects orchestration, ELT, and data integrity.
