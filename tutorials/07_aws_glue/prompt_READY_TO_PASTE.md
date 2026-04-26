# ChatGPT Prompt — AWS Glue Tutorial (READY TO PASTE)
# Paste everything between the triple-backtick fences into ChatGPT

```
TOPIC: AWS Glue for Data Engineers
SLUG: 07_aws_glue
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: AWS (boto3 for control plane; Glue scripts run in AWS managed Spark)

===== CODING STANDARDS =====

FILE HEADER (every file must start with this exact block):
# ============================================================
# Topic   : AWS Glue
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install boto3 | AWS credentials configured | S3 bucket | IAM role
# Run     : python NN_filename.py
# ============================================================

STYLE RULES:
- Comments explain WHY, not what. Always call out Glue gotchas.
- Every main() uses try/finally — cleanup() always runs
- Read env vars at top of file with os.environ.get(); document them in a block comment
- Required env vars: AWS_REGION, AWS_PROFILE, GLUE_S3_BUCKET, GLUE_IAM_ROLE_ARN
- Use uuid4() suffix on all resource names for idempotency
- f-strings only; no % formatting; no .format()
- Type hints on all function signatures
- No placeholder comments, no TODO, no pass, no NotImplementedError

CLEANUP RULES — MANDATORY:
- Every main() wraps ALL demo code in try/finally — cleanup() lives in the finally block
- Every file that creates a resource has its own cleanup() in the same file
- Cleanup functions catch EntityNotFoundException / ResourceNotFoundException silently
- Print ⚠️  COST WARNING: Glue 4.0 = $0.44/DPU-hour, 2 DPU minimum ($0.88/hr). immediately after creating any Glue job or running any job
- Print ✅ Cleanup complete. No ongoing charges. as the final line of every cleanup()
- capstone/cleanup.py deletes EVERYTHING created by the capstone and ends with that confirmation line

===== FILE 01: 01_glue_catalog.py =====

PURPOSE: Glue Data Catalog — databases, tables, crawlers, schema discovery
COVERS: Catalog as Hive metastore, crawlers, classifiers, partition projection

EXACT FUNCTION SIGNATURES:

def create_catalog_database(
    name: str,
    description: str = "",
) -> None:
    """
    Create a Glue catalog database.
    Catch AlreadyExistsException and continue silently (idempotent).
    Print: Created database: {name}
    """

def create_catalog_table(
    database: str,
    name: str,
    s3_location: str,
    schema_cols: list[dict],
    partition_keys: list[dict] | None = None,
) -> None:
    """
    Create a Glue catalog table pointing at an S3 location.
    schema_cols format: [{"Name": "user_id", "Type": "string"}, {"Name": "amount", "Type": "double"}]
    partition_keys format: [{"Name": "date", "Type": "string"}]
    StorageDescriptor: use SerdeInfo with "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    InputFormat: "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    OutputFormat: "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"
    Catch AlreadyExistsException silently.
    Print: Created table: {database}.{name}
    """

def create_crawler(
    name: str,
    role_arn: str,
    s3_targets: list[str],
    database: str,
    schedule: str | None = None,
) -> None:
    """
    Create a Glue crawler targeting S3 paths.
    s3_targets: ["s3://bucket/prefix/"] → Targets.S3Targets = [{"Path": p} for p in s3_targets]
    schedule: cron expression string or None (no schedule = on-demand only).
    TablePrefix: "" (no prefix added to discovered table names).
    Catch AlreadyExistsException silently.
    Print: Created crawler: {name}
    """

def run_crawler_and_wait(
    name: str,
    timeout: int = 300,
) -> str:
    """
    Start crawler. Poll get_crawler() every 10 seconds until State == "READY".
    Raise TimeoutError if not READY within timeout.
    Return final crawler state string.
    Print progress: Crawler {name}: STARTING → RUNNING → READY
    """

def get_table_details(database: str, table: str) -> None:
    """
    Print formatted table summary:
    - Database, table name, S3 location
    - Column list with types (formatted as: col_name (type))
    - Partition keys (if any)
    - Classification (csv/parquet/json)
    - Last updated timestamp
    """

def list_partitions(database: str, table: str) -> list[dict]:
    """
    Return list of partition dicts from get_partitions().
    Print each partition: values=[2024-01, us-east-1] → s3://bucket/prefix/year=2024/month=01/
    Return empty list if no partitions.
    """

def cleanup(resources: dict) -> None:
    """
    Delete in order: crawlers, tables, databases.
    resources: {"crawlers": [str], "tables": [(db, table)], "databases": [str]}
    Catch EntityNotFoundException silently.
    Print ✅ Cleanup complete. No ongoing charges.
    """

MAIN BLOCK:
  - Define sample schema:
      schema_cols = [
          {"Name": "order_id", "Type": "string"},
          {"Name": "customer_id", "Type": "string"},
          {"Name": "amount", "Type": "double"},
          {"Name": "status", "Type": "string"},
          {"Name": "created_at", "Type": "timestamp"},
      ]
      partition_keys = [{"Name": "date", "Type": "string"}]
  - If GLUE_S3_BUCKET and GLUE_IAM_ROLE_ARN are set: run full live demo in try/finally
  - Otherwise: print schema and explain catalog architecture with ASCII diagram:
      Raw S3 ──► Crawler ──► Glue Catalog ──► Athena/Spark/Redshift
                              (Hive-compatible metastore)

===== FILE 02: 02_glue_etl_jobs.py =====

PURPOSE: Create and run Glue ETL jobs — job parameters, bookmarks, monitoring
COVERS: DynamicFrame vs DataFrame, job bookmarks, resolveChoice, ApplyMapping

EXACT FUNCTION SIGNATURES:

def generate_sample_etl_script(source_bucket: str, target_bucket: str) -> str:
    """
    Return a complete Glue PySpark+GlueContext ETL script as a string.
    The script must:
      1. Initialize GlueContext from SparkContext (standard Glue boilerplate)
      2. Read source CSV from s3://{source_bucket}/glue-input/ using glueContext.create_dynamic_frame.from_options()
      3. Apply mapping: rename "order_id" → "id", cast "amount" to double
         using ApplyMapping.apply(frame, mappings=[...])
      4. Resolve choice conflicts with resolveChoice(choice="make_cols")
      5. Filter records where amount > 0 using Filter.apply()
      6. Write to s3://{target_bucket}/glue-output/ as Parquet using glueContext.write_dynamic_frame.from_options()
      7. job.commit() at the end
    Include all necessary imports: awsglue.transforms, awsglue.utils, awsglue.job
    """

def upload_script_to_s3(script_content: str, bucket: str, key: str) -> str:
    """
    Write script_content to a temp file, upload to S3.
    Return s3://{bucket}/{key}
    Print: Uploaded ETL script → s3://{bucket}/{key}
    """

def create_glue_job(
    name: str,
    role_arn: str,
    script_s3_path: str,
    glue_version: str = "4.0",
    worker_type: str = "G.1X",
    number_of_workers: int = 2,
) -> str:
    """
    Create Glue job. Return job name.
    GlueVersion: glue_version
    WorkerType: worker_type (G.1X = 4vCPU/16GB, G.2X = 8vCPU/32GB)
    NumberOfWorkers: number_of_workers (minimum 2)
    DefaultArguments: {"--job-bookmark-option": "job-bookmark-disable", "--enable-metrics": ""}
    Print ⚠️  COST WARNING: Glue 4.0 = $0.44/DPU-hour, 2 DPU minimum ($0.88/hr).
    """

def start_job_run(
    job_name: str,
    arguments: dict[str, str] | None = None,
) -> str:
    """
    Start a job run. Return run_id.
    Print: Started job {job_name} → run {run_id}
    """

def wait_for_job_run(
    job_name: str,
    run_id: str,
    poll_interval: int = 15,
    timeout: int = 600,
) -> str:
    """
    Poll get_job_run() every poll_interval seconds.
    Print progress: Job {run_id}: STARTING → RUNNING → SUCCEEDED/FAILED
    Return final JobRunState string.
    On FAILED: raise RuntimeError with ErrorMessage from response.
    """

def get_job_run_metrics(job_name: str, run_id: str) -> dict:
    """
    Return metrics dict:
      {
        "job_name": str,
        "run_id": str,
        "state": str,
        "started_on": datetime,
        "completed_on": datetime,
        "duration_seconds": float,
        "dpu_seconds": float,
        "estimated_cost_usd": float,   # dpu_seconds / 3600 * 0.44
        "error_message": str | None,
      }
    """

def enable_job_bookmark(job_name: str) -> None:
    """
    Update job to enable bookmark: DefaultArguments["--job-bookmark-option"] = "job-bookmark-enable"
    Print: Bookmark enabled for {job_name}
    Print explanation: "Job bookmark tracks the last successfully processed S3 object.
      Subsequent runs only process NEW files, enabling incremental ETL without state management."
    """

def cleanup(resources: dict) -> None:
    """
    Delete job runs (optional, they auto-expire), then delete job.
    resources: {"jobs": [str]}
    Print ✅ Cleanup complete. No ongoing charges.
    """

MAIN BLOCK:
  - Print DynamicFrame vs DataFrame comparison table:
      | Feature        | DynamicFrame       | DataFrame         |
      | Schema         | Flexible (choice)  | Strict            |
      | Null handling  | Graceful           | Strict            |
      | Performance    | Slightly slower    | Faster            |
      | Best for       | Messy JSON/CSV     | Clean data        |
      | Conversion     | toDF() / fromDF()  | toDF() / fromDF() |
  - Generate script with generate_sample_etl_script("demo-src", "demo-tgt")
  - Print script content with syntax highlighting
  - If GLUE_S3_BUCKET and GLUE_IAM_ROLE_ARN are set: run full live demo in try/finally
  - Otherwise: walk through what each step would do

===== FILE 03: 03_glue_triggers_and_workflows.py =====

PURPOSE: Automate Glue — scheduled triggers, event triggers, Glue Workflows
COVERS: trigger types (SCHEDULED, CONDITIONAL, ON_DEMAND), Workflow, crawl-then-transform

EXACT FUNCTION SIGNATURES:

def create_scheduled_trigger(
    name: str,
    job_name: str,
    cron_expression: str,
) -> str:
    """
    Create a SCHEDULED trigger. Return trigger name.
    Example cron: "cron(0 6 * * ? *)" = 6 AM UTC daily.
    StartOnCreation: True so it activates immediately.
    Print: Created scheduled trigger: {name} → runs {cron_expression}
    """

def create_conditional_trigger(
    name: str,
    watch_job: str,
    then_run_job: str,
    watch_state: str = "SUCCEEDED",
) -> str:
    """
    Create a CONDITIONAL trigger. Return trigger name.
    Predicate: {"Conditions": [{"JobName": watch_job, "State": watch_state, "LogicalOperator": "EQUALS"}]}
    StartOnCreation: True.
    Print: Created conditional trigger: {name} → runs {then_run_job} when {watch_job} {watch_state}
    """

def create_workflow(
    name: str,
    description: str = "",
) -> str:
    """
    Create a Glue Workflow. Return workflow name.
    A workflow is a container for triggers — the triggers must reference it via WorkflowName.
    Print: Created workflow: {name}
    """

def add_trigger_to_workflow(
    workflow_name: str,
    trigger_name: str,
) -> None:
    """
    Update trigger to associate it with the workflow.
    Use update_trigger() to set WorkflowName on the trigger.
    Print: Associated trigger {trigger_name} → workflow {workflow_name}
    """

def start_workflow_run(workflow_name: str) -> str:
    """
    Start a workflow run. Return run_id.
    Print: Started workflow {workflow_name} → run {run_id}
    """

def get_workflow_run_status(workflow_name: str, run_id: str) -> dict:
    """
    Call get_workflow_run() with IncludeGraph=True.
    Return dict:
      {
        "run_id": str,
        "status": str,
        "started_on": datetime,
        "nodes": [
          {"name": str, "type": "JOB|CRAWLER|TRIGGER", "status": str}
        ]
      }
    Print node-by-node status as an ASCII flow:
      [CRAWLER] daily-crawler ✅ SUCCEEDED
          ↓
      [JOB] transform-job ⏳ RUNNING
          ↓
      [JOB] load-job ⏸ WAITING
    """

def cleanup(resources: dict) -> None:
    """
    Delete: triggers (stop first if ACTIVATED), workflows.
    resources: {"triggers": [str], "workflows": [str]}
    Catch EntityNotFoundException silently.
    Print ✅ Cleanup complete. No ongoing charges.
    """

MAIN BLOCK:
  - Print workflow architecture diagram:
      ON_DEMAND trigger (start)
          → CRAWLER: raw-data-crawler
      CONDITIONAL trigger (crawler SUCCEEDED)
          → JOB: validate-and-transform
      CONDITIONAL trigger (job SUCCEEDED)
          → JOB: update-catalog-partitions
  - Explain each trigger type with when to use it
  - If GLUE_IAM_ROLE_ARN is set: create and print the workflow structure in try/finally
  - Otherwise: print the create_workflow() call with all arguments explained

===== FILE 04: 04_glue_data_quality.py =====

PURPOSE: Glue Data Quality — define DQDL rules, evaluate, act on failures
COVERS: DQDL rules, Evaluate Data Quality transform, rulesets, outcomes

IMPORTANT CONTEXT: DQDL = Data Quality Definition Language, Glue-specific SQL-like syntax.
Rules are strings like: "Completeness 'customer_id' >= 0.99"

EXACT FUNCTION SIGNATURES:

def build_ruleset(rules: list[str]) -> str:
    """
    Join rules into a DQDL ruleset string.
    Format:
      Rules = [
          Completeness "customer_id" >= 0.99,
          Uniqueness "order_id" >= 1.0,
          ColumnValues "amount" > 0,
          IsComplete "status",
          RowCount >= 100
      ]
    Separate rules with commas. Wrap in Rules = [ ... ] block.
    """

def create_data_quality_ruleset(
    name: str,
    database: str,
    table: str,
    ruleset_string: str,
) -> str:
    """
    Create a Glue Data Quality ruleset linked to a catalog table. Return ruleset name.
    Catch AlreadyExistsException and update instead.
    Print: Created DQ ruleset: {name} with {len(rules)} rules
    """

def start_data_quality_run(
    ruleset_name: str,
    database: str,
    table: str,
    role_arn: str,
) -> str:
    """
    Start data quality evaluation. Return run_id.
    DataSource: {"GlueTable": {"DatabaseName": database, "TableName": table}}
    Role: role_arn
    RulesetNames: [ruleset_name]
    Print: Started DQ evaluation → run {run_id}
    """

def wait_for_dq_run(run_id: str, timeout: int = 300) -> str:
    """
    Poll get_data_quality_rule_recommendation_run() every 10 seconds.
    Return final status: SUCCEEDED, FAILED, TIMEOUT.
    """

def get_data_quality_results(result_id: str) -> dict:
    """
    Call get_data_quality_result() and return structured results:
      {
        "result_id": str,
        "overall_score": float,   # 0.0 to 1.0
        "passed": bool,
        "rule_results": [
          {
            "rule": str,           # DQDL rule string
            "passed": bool,
            "actual_value": float,
            "description": str,
          }
        ]
      }
    Print a formatted results table:
      Rule                              | Result | Actual | Threshold
      Completeness "customer_id" >= 0.99| PASS   | 1.000  | 0.990
      Uniqueness "order_id" >= 1.0      | FAIL   | 0.987  | 1.000
    """

def common_rules_for_etl_output() -> list[str]:
    """
    Return list of 7 standard DQDL rules for typical ETL output validation:
      1. Completeness "primary_key_col" >= 1.0   (no nulls in PK)
      2. Uniqueness "primary_key_col" >= 1.0     (no duplicates in PK)
      3. RowCount >= 1                            (table not empty)
      4. ColumnValues "amount" > 0               (positive amounts)
      5. Completeness "status" >= 0.95           (status mostly populated)
      6. ColumnValues "created_at" <= now()      (no future dates)
      7. IsComplete "customer_id"                (customer always present)
    Use "primary_key_col" as a placeholder — add a comment explaining to substitute real name.
    """

def cleanup(resources: dict) -> None:
    """
    Delete rulesets by name.
    resources: {"rulesets": [str]}
    Print ✅ Cleanup complete. No ongoing charges.
    """

MAIN BLOCK:
  - Demonstrate build_ruleset() with 5 realistic rules
  - Print the generated DQDL string — explain each line
  - Call common_rules_for_etl_output() and print with explanations
  - If GLUE_S3_BUCKET and GLUE_IAM_ROLE_ARN are set: run full evaluation in try/finally
  - Otherwise: explain what each API call does and what the results would look like
  - Print "What to do on DQ failure" guide:
      PASS (>=0.95): proceed to next stage
      WARN (0.80-0.95): proceed but alert data team
      FAIL (<0.80): halt pipeline, quarantine data, page on-call

===== FILE 05: 05_glue_vs_emr_vs_lambda.py =====

PURPOSE: Decision guide — Glue vs EMR vs Lambda for ETL use cases
COVERS: managed vs configurable, DPU pricing, cold start, use-case matrix

EXACT FUNCTION SIGNATURES:

def calculate_glue_cost(
    dpu_count: float,
    hours: float,
    glue_version: str = "4.0",
) -> dict:
    """
    Return:
      {
        "service": "Glue",
        "dpu_count": float,
        "hours": float,
        "price_per_dpu_hour": float,   # 4.0 = $0.44, 3.0 = $0.44, 2.0 = $0.44 (same)
        "total_usd": float,            # dpu_count * hours * price_per_dpu_hour
        "minimum_dpu": 2,
        "minimum_billing_minutes": 1,
        "notes": str,
      }
    Note in docstring: Glue 4.0 G.1X = 4 vCPU + 16GB per DPU. Minimum 2 DPU per job.
    """

def calculate_emr_cost(
    instance_type: str,
    core_count: int,
    hours: float,
    spot: bool = True,
) -> dict:
    """
    Return:
      {
        "service": "EMR",
        "instance_type": str,
        "core_count": int,
        "hours": float,
        "use_spot": bool,
        "on_demand_total_usd": float,
        "spot_total_usd": float,
        "recommended_usd": float,
        "notes": str,
      }
    Prices (us-east-1, master always on-demand):
      m5.xlarge=$0.192, m5.2xlarge=$0.384, m5.4xlarge=$0.768,
      r5.2xlarge=$0.504, r5.4xlarge=$1.008
    Spot discount: 70%.
    """

def calculate_lambda_cost(
    invocations: int,
    avg_duration_ms: float,
    memory_mb: int,
) -> dict:
    """
    Return:
      {
        "service": "Lambda",
        "invocations": int,
        "avg_duration_ms": float,
        "memory_mb": int,
        "compute_seconds": float,      # invocations * avg_duration_ms / 1000
        "gb_seconds": float,           # compute_seconds * memory_mb / 1024
        "compute_cost_usd": float,     # gb_seconds * 0.0000166667
        "request_cost_usd": float,     # invocations * 0.0000002
        "total_usd": float,
        "notes": str,
      }
    Free tier: 400,000 GB-seconds/month, 1M requests/month (do NOT subtract in calculation).
    Max Lambda timeout: 15 minutes. Max memory: 10GB.
    """

def recommend_service(
    data_size_gb: float,
    frequency_per_day: float,
    latency_req_seconds: float,
    team_spark_expertise: bool,
) -> dict:
    """
    Return recommendation dict:
      {
        "recommended": "Glue" | "EMR" | "Lambda",
        "rationale": str,        # 2-3 sentence explanation
        "alternatives": [str],   # other viable options
        "avoid": str,            # worst choice and why
        "estimated_monthly_cost": float,
      }
    Decision rules (apply in order):
      1. latency_req_seconds < 60 → Lambda (event-driven, low latency)
      2. data_size_gb < 1 and frequency_per_day > 10 → Lambda
      3. data_size_gb > 500 and team_spark_expertise → EMR (full control, cheaper at scale)
      4. data_size_gb > 500 and not team_spark_expertise → Glue (managed Spark, no ops)
      5. frequency_per_day <= 1 → Glue (intermittent, pay-per-use)
      6. Default → Glue (safe managed choice)
    """

def print_decision_matrix() -> None:
    """
    Print a formatted comparison matrix:

    ╔══════════════════════╦════════════════╦═══════════════╦════════════════╗
    ║ Dimension            ║ Glue           ║ EMR           ║ Lambda         ║
    ╠══════════════════════╬════════════════╬═══════════════╬════════════════╣
    ║ Setup time           ║ 1-2 min        ║ 5-10 min      ║ <1 sec         ║
    ║ Max job duration     ║ 48 hours       ║ No limit      ║ 15 minutes     ║
    ║ Min cost             ║ 2 DPU = $0.88  ║ 1 master node ║ $0.0000002/req ║
    ║ Spark native         ║ Yes (managed)  ║ Yes (control) ║ No             ║
    ║ Cold start           ║ ~30 sec        ║ 5-10 min      ║ <1 sec         ║
    ║ Schema flexibility   ║ High (DynFrame)║ Medium        ║ High (code)    ║
    ║ Ops burden           ║ Zero           ║ High          ║ Low            ║
    ║ Best data size       ║ 1GB - 1TB      ║ 100GB - 100TB ║ <1GB           ║
    ║ Catalog integration  ║ Native         ║ Via metastore ║ Manual         ║
    ║ Job bookmarks        ║ Built-in       ║ Manual        ║ Manual (DDB)   ║
    ╚══════════════════════╩════════════════╩═══════════════╩════════════════╝
    """

MAIN BLOCK:
  - Call print_decision_matrix()
  - Run 4 real-world scenario recommendations:
      Scenario 1: E-commerce order events, 0.1GB/day, 100/day, latency<30s, no Spark → Lambda
      Scenario 2: Daily sales report, 50GB/day, 1/day, latency<4hr, some Spark → Glue
      Scenario 3: 1TB/day clickstream with transforms, 2/day, latency<2hr, Spark experts → EMR
      Scenario 4: Ad-hoc data science pipeline, 200GB, weekly, 24hr ok, no Spark → Glue
  - For each scenario: print recommendation, rationale, estimated monthly cost
  - Print total cost comparison table across all 4 scenarios

===== CAPSTONE =====

Generate these files (all COMPLETE and FULLY RUNNABLE):

--- capstone/brief.md ---
Title: Automated Data Lake ETL Pipeline with Glue
Scenario: Raw JSON files (orders data) land daily in s3://{GLUE_S3_BUCKET}/raw/orders/.
Build a Glue pipeline that:
  1. Crawls new files → creates/updates Glue catalog table
  2. Validates with Data Quality rules (5 rules, including one that a bad file fails)
  3. Transforms JSON to Parquet (rename fields, cast types, filter nulls)
  4. Writes to s3://{GLUE_S3_BUCKET}/silver/orders/ partitioned by date
  5. Reports metrics: DPU-hours consumed, DQ pass/fail, rows processed

--- capstone/setup.py ---
PURPOSE: Create catalog DB, generate sample JSON files, upload to S3.

CONSTANTS:
  DB_NAME = "studybook_glue_demo"
  TABLE_NAME = "raw_orders"
  N_GOOD_RECORDS = 500   # valid orders
  N_BAD_RECORDS = 50     # records with null order_id (to trigger DQ failure)

EXACT FUNCTION SIGNATURES:

def generate_good_records(n: int) -> list[dict]:
    """
    Return n dicts with keys:
      order_id (uuid4 string), customer_id (uuid4 string), amount (float 1.0-999.99),
      status (PENDING/CONFIRMED/SHIPPED/DELIVERED), product_sku (SKU-XXXXX),
      created_at (ISO 8601, within last 30 days)
    """

def generate_bad_records(n: int) -> list[dict]:
    """
    Return n dicts identical to good records BUT order_id = None.
    These should fail the Completeness "order_id" >= 1.0 DQ rule.
    """

def write_json_files(records: list[dict], label: str, bucket: str) -> list[str]:
    """
    Write records as newline-delimited JSON to two S3 files:
      s3://{bucket}/raw/orders/{label}_batch_A.json  (first half)
      s3://{bucket}/raw/orders/{label}_batch_B.json  (second half)
    Return list of S3 URIs.
    """

def setup_catalog(bucket: str, role_arn: str) -> None:
    """
    1. create_catalog_database(DB_NAME)
    2. Create crawler "studybook-orders-crawler" targeting s3://{bucket}/raw/orders/
    3. Print setup complete with paths
    """

def main() -> None:
    """
    Gate on GLUE_S3_BUCKET and GLUE_IAM_ROLE_ARN. Print instructions if not set.
    Otherwise:
      good = generate_good_records(N_GOOD_RECORDS)
      bad = generate_bad_records(N_BAD_RECORDS)
      write_json_files(good + bad, "orders", bucket)
      setup_catalog(bucket, role_arn)
    """

--- capstone/pipeline.py ---
PURPOSE: Create crawler, DQ ruleset, ETL job; wire with a workflow.

CONSTANTS:
  WORKFLOW_NAME = f"studybook-orders-pipeline-{uuid4().hex[:8]}"
  CRAWLER_NAME = "studybook-orders-crawler"
  DQ_RULESET_NAME = "studybook-orders-dq-rules"
  ETL_JOB_NAME = f"studybook-orders-etl-{uuid4().hex[:8]}"

EXACT FUNCTION SIGNATURES:

def create_dq_ruleset(database: str, table: str) -> str:
    """
    Create ruleset with these 5 rules:
      Completeness "order_id" >= 1.0
      Uniqueness "order_id" >= 0.99
      ColumnValues "amount" > 0
      Completeness "customer_id" >= 0.99
      IsComplete "status"
    Return ruleset name.
    """

def generate_etl_script(source_bucket: str, target_bucket: str) -> str:
    """
    Return complete Glue ETL script string that:
      1. Reads from s3://{source_bucket}/raw/orders/ (JSON)
      2. Drops records where order_id is null (filter bad records)
      3. ApplyMapping: order_id→id, customer_id→cust_id, amount→amount (double), status→status, created_at→created_at
      4. Derives date column from created_at for partitioning
      5. Writes to s3://{target_bucket}/silver/orders/ partitioned by date as Parquet
      6. job.commit()
    """

def build_pipeline(bucket: str, role_arn: str) -> dict:
    """
    Build complete pipeline:
      1. Upload ETL script to S3 → script_uri
      2. create_glue_job(ETL_JOB_NAME, role_arn, script_uri)
      3. Create workflow WORKFLOW_NAME
      4. Create ON_DEMAND trigger "start-crawler" → runs CRAWLER_NAME
      5. Create CONDITIONAL trigger "crawler-done" → runs ETL_JOB_NAME when CRAWLER_NAME SUCCEEDED
      6. Associate both triggers with workflow
    Return: {"workflow": str, "job": str, "triggers": [str]}
    Print ⚠️  COST WARNING after job creation.
    """

def main() -> None:
    """Gate on env vars. Run build_pipeline() in try/finally."""

--- capstone/monitor.py ---
PURPOSE: Check workflow run status, pull DQ results, print cost report.

EXACT FUNCTION SIGNATURES:

def check_pipeline_status(workflow_name: str, run_id: str) -> None:
    """
    Print node-by-node status (reuse get_workflow_run_status() from file 03).
    """

def pull_and_print_dq_results(ruleset_name: str) -> bool:
    """
    Get the most recent DQ run result for the ruleset.
    Print formatted results table.
    Return True if all rules passed.
    """

def print_pipeline_report(workflow_name: str, job_name: str) -> None:
    """
    Print summary:
      ╔══════════════════════════════════════╗
      ║   Glue Pipeline Execution Report     ║
      ╠══════════════════════════════════════╣
      ║ Workflow: {name}                     ║
      ║ Status: COMPLETED                    ║
      ║ DQ Rules: 4/5 passed                 ║
      ║ ETL Job DPU-hours: 0.034             ║
      ║ Estimated cost: $0.015               ║
      ║ Rows in: 550  Rows out: 500          ║
      ╚══════════════════════════════════════╝
    """

--- capstone/cleanup.py ---
PURPOSE: Remove ALL resources created by this capstone.
  - Delete Glue jobs matching prefix "studybook-orders-etl-"
  - Delete triggers matching prefix "studybook-" 
  - Delete workflows matching prefix "studybook-orders-pipeline-"
  - Delete DQ ruleset DQ_RULESET_NAME
  - Delete crawler CRAWLER_NAME
  - Delete catalog table raw_orders in studybook_glue_demo
  - Delete catalog database studybook_glue_demo
  - Delete S3 objects under s3://{GLUE_S3_BUCKET}/raw/orders/
  - Delete S3 objects under s3://{GLUE_S3_BUCKET}/silver/orders/
  - Delete S3 objects under s3://{GLUE_S3_BUCKET}/glue-scripts/
  - Print count of deleted resources per type
  - End with: print("✅ Cleanup complete. No ongoing charges.")

--- capstone/test_capstone.py ---
PURPOSE: Test data generation, DQ rule builder, cost calculator — no AWS calls.

EXACT TEST FUNCTIONS:

def test_generate_good_records_schema():
    """
    from setup import generate_good_records
    records = generate_good_records(10)
    assert len(records) == 10
    for r in records:
        assert r["order_id"] is not None
        assert isinstance(r["amount"], float)
        assert r["amount"] > 0
        assert r["status"] in ["PENDING", "CONFIRMED", "SHIPPED", "DELIVERED"]
    """

def test_generate_bad_records_have_null_order_id():
    """
    from setup import generate_bad_records
    records = generate_bad_records(5)
    assert len(records) == 5
    assert all(r["order_id"] is None for r in records)
    """

def test_build_ruleset_format():
    """
    from glue_data_quality import build_ruleset  # reuse from file 04 or inline
    rules = ['Completeness "order_id" >= 1.0', 'RowCount >= 100']
    result = build_ruleset(rules)
    assert result.startswith("Rules = [")
    assert 'Completeness "order_id" >= 1.0' in result
    assert "RowCount >= 100" in result
    """

def test_glue_cost_calculation():
    """
    from glue_vs_emr_vs_lambda import calculate_glue_cost
    result = calculate_glue_cost(dpu_count=2, hours=1.0)
    assert result["total_usd"] == pytest.approx(0.88, rel=0.01)
    assert result["dpu_count"] == 2
    assert result["minimum_dpu"] == 2
    """

def test_lambda_cost_calculation():
    """
    from glue_vs_emr_vs_lambda import calculate_lambda_cost
    result = calculate_lambda_cost(invocations=1_000_000, avg_duration_ms=500, memory_mb=512)
    assert result["gb_seconds"] == pytest.approx(250000.0, rel=0.01)
    assert result["total_usd"] > 0
    assert result["total_usd"] < 10  # 1M invocations at 500ms/512MB should cost <$10
    """

def test_service_recommendation_lambda_for_low_latency():
    """
    from glue_vs_emr_vs_lambda import recommend_service
    rec = recommend_service(data_size_gb=0.5, frequency_per_day=100, latency_req_seconds=30, team_spark_expertise=False)
    assert rec["recommended"] == "Lambda"
    """

def test_service_recommendation_emr_for_large_data():
    """
    from glue_vs_emr_vs_lambda import recommend_service
    rec = recommend_service(data_size_gb=1000, frequency_per_day=2, latency_req_seconds=3600, team_spark_expertise=True)
    assert rec["recommended"] == "EMR"
    """

def test_common_dq_rules_count():
    """
    from glue_data_quality import common_rules_for_etl_output
    rules = common_rules_for_etl_output()
    assert len(rules) == 7
    assert any("Completeness" in r for r in rules)
    assert any("Uniqueness" in r for r in rules)
    assert any("RowCount" in r for r in rules)
    """

===== GENERATION INSTRUCTIONS =====

Generate files ONE AT A TIME in this order:
  01_glue_catalog.py
  02_glue_etl_jobs.py
  03_glue_triggers_and_workflows.py
  04_glue_data_quality.py
  05_glue_vs_emr_vs_lambda.py
  capstone/brief.md
  capstone/setup.py
  capstone/pipeline.py
  capstone/monitor.py
  capstone/cleanup.py
  capstone/test_capstone.py

Each file must be COMPLETE and FULLY RUNNABLE — no placeholders, no TODO comments, no pass statements.
Use exact function signatures shown above.
After each file, wait for me to say "next".

Acknowledge these instructions, then wait for me to say "generate file 01".
```
