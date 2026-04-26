# ChatGPT Prompt — AWS EMR Tutorial (READY TO PASTE)
# Paste everything between the triple-backtick fences into ChatGPT

```
TOPIC: AWS EMR for Data Engineers
SLUG: 06_aws_emr
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: AWS (boto3) — prefer EMR Serverless to avoid cluster costs

===== CODING STANDARDS =====

FILE HEADER (every file must start with this exact block):
# ============================================================
# Topic   : AWS EMR for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install boto3 | AWS credentials configured | S3 bucket
# Run     : python NN_filename.py
# ============================================================

STYLE RULES:
- Comments explain WHY, not what. Always call out cost implications.
- Every main() uses try/finally — cleanup() always runs
- Read env vars at top of file with os.environ.get(); document them in a block comment
- Required env vars per file: AWS_REGION, AWS_PROFILE, EMR_S3_BUCKET, EMR_SUBNET_ID
- Optional: EMR_EC2_KEY_PAIR, STEP_FUNCTIONS_ROLE_ARN
- Use uuid4() suffix on all resource names for idempotency
- f-strings only; no % formatting; no .format()
- Type hints on all function signatures
- No placeholder comments, no TODO, no pass, no NotImplementedError

CLEANUP RULES — MANDATORY:
- Every main() wraps ALL demo code in try/finally — cleanup() lives in the finally block
- Every file that creates a resource has its own cleanup() in the same file
- Cleanup functions catch "resource not found" / "already deleted" errors and continue silently
- Print ⚠️  COST WARNING: <resource type> is now running and accruing charges. immediately after any billable resource starts
- Print ✅ Cleanup complete. No ongoing charges. as the final line of every cleanup()
- capstone/cleanup.py deletes EVERYTHING created by the capstone and ends with that confirmation line

===== FILE 01: 01_emr_cluster_basics.py =====

PURPOSE: Create, monitor, and terminate EMR clusters — instance types, configurations
COVERS: master/core/task nodes, instance types, EMR versions, bootstrap actions

EXACT FUNCTION SIGNATURES:

def create_emr_cluster(
    name: str,
    instance_type: str,
    core_count: int,
    emr_version: str,
    s3_bucket: str,
    subnet_id: str,
    ec2_key_pair: str | None = None,
) -> str:
    """
    Create an EMR cluster and return the cluster_id.
    - Uses TERMINATE_AT_TASK_COMPLETION to avoid dangling clusters.
    - Log URI: s3://{s3_bucket}/emr-logs/
    - One master node (ON_DEMAND) + core_count core nodes (SPOT preferred).
    - Print ⚠️  COST WARNING immediately after create_cluster call.
    - Returns cluster_id string.
    """

def wait_for_cluster(
    cluster_id: str,
    target_state: str = "WAITING",
    timeout: int = 600,
) -> dict:
    """
    Poll describe_cluster every 15 seconds until state == target_state or TERMINATED/FAILED.
    Raise TimeoutError if not reached within timeout seconds.
    Return final describe_cluster response.
    """

def describe_cluster(cluster_id: str) -> None:
    """
    Print formatted cluster summary:
    - Cluster ID, Name, State, StateChangeReason
    - Master/Core/Task node counts and instance types
    - Creation time and elapsed time
    """

def list_steps(cluster_id: str) -> list[dict]:
    """
    Return list of step dicts from list_steps() API.
    Print each step: Id, Name, Status.State, CreationDateTime.
    """

def terminate_cluster(cluster_id: str) -> None:
    """
    Terminate the cluster. Catch AlreadyTerminated errors silently.
    Print ✅ Cleanup complete. No ongoing charges. after confirmed.
    """

def recommend_instance_type(
    data_size_gb: float,
    compute_vs_memory: str = "balanced",
) -> dict:
    """
    Return a recommendation dict:
      {
        "master": "m5.xlarge",
        "core": "r5.2xlarge",
        "task": "r5.4xlarge",  # spot
        "core_count": 4,
        "rationale": "Memory-heavy workload (>500GB) needs r5 family...",
        "estimated_cost_per_hour": 1.23,
      }
    Decision table:
      - <50GB  → m5.xlarge master, m5.xlarge core x2
      - 50-500GB → m5.2xlarge master, m5.4xlarge core x4
      - >500GB, balanced → r5.4xlarge master, r5.4xlarge core x6
      - >500GB, compute → c5.4xlarge master, c5.9xlarge core x6
      - >500GB, memory → r5.8xlarge master, r5.8xlarge core x8
    """

MAIN BLOCK:
  - Show cluster creation code in a comment block with explanation
  - Demonstrate recommend_instance_type() for three scenarios:
      recommend_instance_type(30)          # small batch
      recommend_instance_type(300, "compute")   # medium, compute-heavy
      recommend_instance_type(1000, "memory")   # large, memory-heavy
  - Print a formatted table of all three recommendations
  - If EMR_S3_BUCKET and EMR_SUBNET_ID are set, run the live demo:
      cluster_id = create_emr_cluster(...)
      wait_for_cluster(cluster_id, "WAITING")
      describe_cluster(cluster_id)
  - Otherwise print: "Set EMR_S3_BUCKET and EMR_SUBNET_ID to run live demo"

===== FILE 02: 02_spark_jobs_on_emr.py =====

PURPOSE: Submit PySpark jobs to EMR — step submission, script upload, monitoring
COVERS: EMR steps, action-on-failure, S3 script storage, job arguments

EXACT FUNCTION SIGNATURES:

def upload_script_to_s3(
    script_path: str,
    bucket: str,
    prefix: str = "emr-scripts",
) -> str:
    """
    Upload local PySpark script to S3. Return full s3:// URI.
    Print: Uploaded {script_path} → s3://{bucket}/{prefix}/{filename}
    """

def submit_spark_step(
    cluster_id: str,
    script_s3_path: str,
    args: list[str],
    step_name: str = "PySpark Step",
    action_on_failure: str = "CONTINUE",
) -> str:
    """
    Submit a Spark step to an existing cluster. Return step_id.
    Jar: command-runner.jar, Args: ["spark-submit", script_s3_path, *args]
    """

def wait_for_step(
    cluster_id: str,
    step_id: str,
    poll_interval: int = 15,
    timeout: int = 600,
) -> str:
    """
    Poll step status every poll_interval seconds.
    Print progress dots: Step {step_id}: PENDING... RUNNING... COMPLETED
    Return final state string.
    Raise TimeoutError if not terminal within timeout.
    """

def get_step_logs(
    cluster_id: str,
    step_id: str,
    bucket: str,
) -> str:
    """
    Construct S3 log path: s3://{bucket}/emr-logs/{cluster_id}/steps/{step_id}/
    Attempt to read stderr and stdout from S3.
    Return concatenated log content or "Logs not yet available" if key missing.
    """

def build_spark_submit_args(
    conf_overrides: dict[str, str] | None = None,
    py_files: list[str] | None = None,
    jars: list[str] | None = None,
) -> list[str]:
    """
    Build list of spark-submit CLI arguments.
    conf_overrides: {"spark.executor.memory": "4g"} → ["--conf", "spark.executor.memory=4g", ...]
    py_files: ["s3://bucket/lib.py"] → ["--py-files", "s3://bucket/lib.py"]
    jars: ["s3://bucket/dep.jar"] → ["--jars", "s3://bucket/dep.jar"]
    """

ALSO GENERATE: A sample PySpark script string (as a Python string constant) that:
  - Reads a CSV from S3 (path from sys.argv[1])
  - Groups by a "category" column, counts rows
  - Writes result as Parquet to S3 (path from sys.argv[2])
  - This string is what generate_script_content() returns and gets written to a temp file for upload

MAIN BLOCK:
  - Show build_spark_submit_args() examples with three scenarios
  - If EMR_CLUSTER_ID is set in env:
      Write sample script to /tmp/sample_spark_job.py
      upload_script_to_s3("/tmp/sample_spark_job.py", bucket)
      step_id = submit_spark_step(cluster_id, s3_path, args)
      wait_for_step(cluster_id, step_id)
      get_step_logs(cluster_id, step_id, bucket)
  - Otherwise: print script content and explain each step

===== FILE 03: 03_emr_serverless.py =====

PURPOSE: EMR Serverless — no cluster management, pay per use, ideal for batch jobs
COVERS: Application lifecycle, Job Runs, pre-initialized capacity, cost calculation

EXACT FUNCTION SIGNATURES:

def create_serverless_application(
    name: str,
    emr_version: str = "emr-6.15.0",
    pre_init_capacity: dict | None = None,
) -> str:
    """
    Create EMR Serverless application with Spark type. Return application_id.
    pre_init_capacity example: {"workerCount": 2, "workerConfiguration": {"cpu": "4vCPU", "memory": "16GB"}}
    If pre_init_capacity is None, no pre-initialized workers (cold start ~30s).
    Print ⚠️  COST WARNING if pre_init_capacity is set (workers charge when idle).
    """

def start_serverless_application(application_id: str) -> None:
    """
    Call start_application() and poll until state == STARTED.
    Poll every 10 seconds, timeout 300 seconds.
    """

def submit_serverless_job(
    application_id: str,
    role_arn: str,
    script_s3: str,
    args: list[str],
    spark_conf: dict[str, str] | None = None,
    job_name: str = "emr-serverless-job",
) -> str:
    """
    Submit a job run. Return job_run_id.
    spark_conf keys become --conf entries in sparkSubmitParameters.
    Print: Submitted job {job_name} → {job_run_id}
    """

def wait_for_job(
    application_id: str,
    job_run_id: str,
    timeout: int = 600,
) -> dict:
    """
    Poll get_job_run() every 15 seconds.
    Print progress: Job {job_run_id}: PENDING → RUNNING → SUCCESS/FAILED
    Return final job_run dict.
    Raise RuntimeError on FAILED with error message from response.
    """

def get_job_details(application_id: str, job_run_id: str) -> dict:
    """
    Return dict with:
      {
        "job_run_id": str,
        "state": str,
        "duration_seconds": float,
        "total_vcpu_hours": float,
        "total_memory_gb_hours": float,
        "estimated_cost_usd": float,  # vcpu_hours * 0.052 + mem_gb_hours * 0.0057
        "cost_breakdown": str,        # human readable
      }
    """

def stop_and_delete_application(application_id: str) -> None:
    """
    Stop application (wait for STOPPED state), then delete it.
    Catch ResourceNotFoundException silently.
    Print ✅ Cleanup complete. No ongoing charges.
    """

MAIN BLOCK (always runs — uses mocked values when env vars not set):
  - Print EMR Serverless vs Cluster comparison table:
      | Dimension        | EMR Serverless | EMR Cluster  |
      | Setup time       | ~30 seconds    | 5-10 minutes |
      | Min cost         | Per second     | Per hour     |
      | Management       | Zero           | Full control |
      | Max scale        | Automatic      | Manual       |
      | Best for         | Batch jobs     | Long-running |
  - Run live demo if EMR_SERVERLESS_ROLE_ARN and EMR_S3_BUCKET are set
  - Otherwise simulate with printed output

===== FILE 04: 04_cost_optimization.py =====

PURPOSE: Control EMR spend — Spot instances, auto-scaling, rightsizing
COVERS: Spot vs On-Demand, instance fleets, auto-scaling policies, cost comparison

EXACT FUNCTION SIGNATURES:

def calculate_cluster_cost(
    instance_type: str,
    core_count: int,
    hours: float,
    use_spot: bool = True,
) -> dict:
    """
    Return cost breakdown dict:
      {
        "instance_type": str,
        "core_count": int,
        "hours": float,
        "on_demand_price_per_hour": float,
        "spot_discount_pct": float,    # typically 70-80% discount
        "spot_price_per_hour": float,
        "total_on_demand_usd": float,
        "total_spot_usd": float,
        "recommended_usd": float,      # spot if use_spot else on_demand
        "savings_vs_on_demand_usd": float,
      }
    Use these representative us-east-1 prices (hardcode):
      m5.xlarge: $0.192/hr, m5.2xlarge: $0.384/hr, m5.4xlarge: $0.768/hr,
      r5.2xlarge: $0.504/hr, r5.4xlarge: $1.008/hr, r5.8xlarge: $2.016/hr,
      c5.4xlarge: $0.680/hr, c5.9xlarge: $1.530/hr
    Spot discount: 70% for r5, 75% for m5, 60% for c5.
    Master node always ON_DEMAND. Core nodes use spot if use_spot=True.
    """

def calculate_serverless_cost(
    vcpu_hours: float,
    memory_gb_hours: float,
) -> dict:
    """
    Return:
      {
        "vcpu_hours": float,
        "memory_gb_hours": float,
        "vcpu_cost_usd": float,         # vcpu_hours * 0.052
        "memory_cost_usd": float,       # memory_gb_hours * 0.0057
        "total_usd": float,
        "cost_per_hour_equivalent": float,
      }
    """

def compare_options(job_hours: float, data_size_gb: float) -> None:
    """
    Print a formatted cost comparison table for three job sizes.
    For each of: small (2 m5.xlarge cores), medium (4 m5.4xlarge cores), large (8 r5.4xlarge cores):
      - EMR Cluster (On-Demand)
      - EMR Cluster (Spot)
      - EMR Serverless (estimated vcpu/memory from data_size_gb)
    Show winner with ★ symbol.
    """

def build_instance_fleet_config(
    on_demand_capacity: int,
    spot_capacity: int,
    instance_types: list[str],
) -> dict:
    """
    Return boto3-ready InstanceFleets config dict.
    Each instance type weighted equally.
    SpotSpecification: AllocationStrategy = "CAPACITY_OPTIMIZED"
    OnDemandSpecification: AllocationStrategy = "LOWEST_PRICE"
    """

def build_autoscaling_policy(
    min_instances: int,
    max_instances: int,
    scale_out_metric: str = "YARNMemoryAvailablePercentage",
) -> dict:
    """
    Return boto3-ready AutoScalingPolicy dict with:
    - ScaleOut: when scale_out_metric < 15% for 5 minutes → add 2 instances
    - ScaleIn: when YARNMemoryAvailablePercentage > 75% for 5 minutes → remove 2 instances
    """

MAIN BLOCK:
  - Run compare_options() for three profiles:
      compare_options(2.0, 50)    # Small job: 2 hours, 50GB
      compare_options(8.0, 500)   # Medium job: 8 hours, 500GB
      compare_options(24.0, 5000) # Large job: 24 hours, 5TB
  - Print instance fleet config example
  - Print autoscaling policy example
  - Print "Cost optimization tips" section with 5 concrete recommendations

===== FILE 05: 05_monitoring_and_bootstrap.py =====

PURPOSE: EMR monitoring, bootstrap actions, and debugging failed steps
COVERS: CloudWatch integration, YARN UI, bootstrap actions, log parsing

EXACT FUNCTION SIGNATURES:

def create_bootstrap_action(
    name: str,
    script_s3_path: str,
    args: list[str] | None = None,
) -> dict:
    """
    Return bootstrap action dict ready for BootstrapActions parameter in create_cluster.
    Example name: "Install Python packages"
    Example script: s3://bucket/scripts/bootstrap.sh
    Example args: ["pandas==2.0.0", "pyarrow==13.0.0"]
    Also generate the shell script content as a string constant BOOTSTRAP_SCRIPT that
    pip-installs the packages from args.
    """

def get_cluster_metrics(
    cluster_id: str,
    minutes: int = 60,
) -> dict:
    """
    Pull CloudWatch metrics for the cluster (namespace: AWS/ElasticMapReduce):
      - YARNMemoryAvailablePercentage (avg)
      - ContainerPendingRatio (max)
      - HDFSUtilization (max)
      - CoreNodesRunning (max)
    Return dict: {metric_name: {"avg": float, "max": float, "min": float}}
    Use period=300 (5-min granularity).
    """

def find_failed_step_logs(
    cluster_id: str,
    step_id: str,
    log_bucket: str,
) -> dict:
    """
    Construct expected S3 paths for step logs:
      stderr: s3://{log_bucket}/emr-logs/{cluster_id}/steps/{step_id}/stderr.gz
      stdout: s3://{log_bucket}/emr-logs/{cluster_id}/steps/{step_id}/stdout.gz
      controller: s3://{log_bucket}/emr-logs/{cluster_id}/steps/{step_id}/controller.gz
    Attempt to download and decompress each.
    Return: {"stderr": str, "stdout": str, "controller": str}
    If a file doesn't exist: set value to "Not available yet"
    """

def parse_spark_log_for_errors(log_content: str) -> list[dict]:
    """
    Scan log_content for known error patterns. Return list of findings:
      [
        {"type": "OOM", "line": 142, "message": "java.lang.OutOfMemoryError: GC overhead limit exceeded", "suggestion": "Increase executor memory with --conf spark.executor.memory=8g"},
        {"type": "SHUFFLE", "line": 891, "message": "org.apache.spark.shuffle.FetchFailedException", "suggestion": "Increase spark.reducer.maxReqsInFlight and spark.shuffle.io.retryWait"},
        {"type": "PARTITION", "line": 203, "message": "Job aborted due to stage failure: Total size of serialized results...", "suggestion": "Reduce spark.driver.maxResultSize or increase partition count"},
      ]
    Patterns to detect (use re.search):
      - "OutOfMemoryError" → type OOM
      - "FetchFailedException" → type SHUFFLE
      - "Total size of serialized results" → type PARTITION
      - "FileNotFoundException" → type FILE_NOT_FOUND
      - "AccessDeniedException" → type PERMISSIONS
    """

def setup_cloudwatch_alarms(
    cluster_id: str,
    sns_topic_arn: str,
) -> list[str]:
    """
    Create two CloudWatch alarms. Return list of alarm names created.
    Alarm 1: YARNMemoryAvailablePercentage < 10% for 10 minutes → notify SNS
      AlarmName: f"emr-{cluster_id}-low-memory"
    Alarm 2: ContainerPendingRatio > 0.75 for 5 minutes → notify SNS
      AlarmName: f"emr-{cluster_id}-high-pending"
    """

MAIN BLOCK:
  - Print BOOTSTRAP_SCRIPT content with explanation
  - Demonstrate parse_spark_log_for_errors() with a realistic sample log string containing:
      * An OOM error line
      * A FetchFailedException line
      * Normal INFO lines (to show filtering works)
  - Print findings table with type, line number, message snippet, suggestion
  - If AWS_REGION is set: demonstrate get_cluster_metrics() structure
  - Print "EMR Debugging Checklist" — 6-point guide (OOM → memory, shuffle → network, etc.)

===== CAPSTONE =====

Generate these files (all COMPLETE and FULLY RUNNABLE):

--- capstone/brief.md ---
Title: Large-Scale Log Processing with EMR Serverless
Scenario: Process one week of simulated web server access logs (1M records) using
  EMR Serverless PySpark. Filter 4xx/5xx errors, aggregate by endpoint + status code
  + hour, write results as Parquet partitioned by date/status_code to S3.

--- capstone/generate_logs.py ---
PURPOSE: Generate 1M synthetic Apache Combined Log Format records, write to local CSV,
  upload to s3://{EMR_S3_BUCKET}/raw/weblogs/

CONSTANTS:
  N_RECORDS = 1_000_000
  ENDPOINTS = ["/api/users", "/api/orders", "/api/products", "/health", "/api/payments",
               "/api/reports", "/api/auth/login", "/api/auth/logout"]
  STATUS_CODES = [200]*70 + [201]*10 + [400]*8 + [404]*5 + [500]*5 + [503]*2

EXACT FUNCTION SIGNATURES:

def generate_log_record(ts: datetime) -> dict:
    """
    Return dict with keys:
      timestamp (ISO 8601), endpoint, method (GET/POST/PUT/DELETE weighted),
      status_code, response_time_ms (50-2000, higher for 5xx),
      bytes_sent (100-50000), user_agent, ip_address
    """

def generate_log_batch(n: int = N_RECORDS) -> list[dict]:
    """Generate n records spread across 7 days ending today."""

def save_to_csv(records: list[dict], path: str) -> None:
    """Write records to CSV using csv.DictWriter."""

def upload_to_s3(local_path: str, bucket: str, key: str) -> str:
    """Upload file to S3. Return s3:// URI. Print progress."""

def main() -> None:
    """Generate logs, save, upload. Print record count and S3 location."""

--- capstone/process_logs.py ---
PURPOSE: PySpark script designed to run on EMR Serverless (reads from S3, writes to S3).
  Must work with spark-submit — no local mode setup, uses SparkContext from environment.

EXACT LOGIC:
  1. Read CSV from sys.argv[1] (s3:// URI)
  2. Parse timestamp column to timestamp type
  3. Filter: keep only status_code >= 400 (errors only)
  4. Enrich: add hour column (extract hour from timestamp), date column
  5. Aggregate: groupBy(date, endpoint, status_code, hour).agg(
       count("*").alias("request_count"),
       avg("response_time_ms").alias("avg_response_ms"),
       sum("bytes_sent").alias("total_bytes")
     )
  6. Write as Parquet to sys.argv[2] partitioned by ["date", "status_code"]
  7. Print row count of input and output

--- capstone/orchestrate.py ---
PURPOSE: Upload process_logs.py, create EMR Serverless app, submit job, monitor, report cost.

CONSTANTS:
  EMR_VERSION = "emr-6.15.0"
  APP_NAME = f"studybook-log-processor-{uuid4().hex[:8]}"

EXACT FUNCTION SIGNATURES:

def setup(bucket: str) -> tuple[str, str]:
    """
    Upload capstone/process_logs.py to s3://{bucket}/emr-scripts/process_logs.py.
    Return (script_s3_uri, input_s3_uri).
    """

def run_pipeline(
    role_arn: str,
    bucket: str,
) -> dict:
    """
    Full pipeline:
      1. create_serverless_application(APP_NAME, EMR_VERSION)
      2. start_serverless_application(application_id)
      3. setup(bucket) → script_uri, input_uri
      4. output_uri = f"s3://{bucket}/processed/weblogs/"
      5. submit_serverless_job(application_id, role_arn, script_uri, [input_uri, output_uri])
      6. wait_for_job(application_id, job_run_id, timeout=900)
      7. details = get_job_details(application_id, job_run_id)
      8. Print cost report
      9. Return details
    """

def print_cost_report(details: dict) -> None:
    """
    Print formatted cost report:
      ╔══════════════════════════════════════╗
      ║     EMR Serverless Cost Report       ║
      ╠══════════════════════════════════════╣
      ║ Duration:        XX.X seconds        ║
      ║ vCPU-hours:      X.XXXX              ║
      ║ Memory GB-hours: XX.XXXX             ║
      ║ Total cost:      $X.XXXX             ║
      ╚══════════════════════════════════════╝
    """

def main() -> None:
    """
    Gate on EMR_SERVERLESS_ROLE_ARN and EMR_S3_BUCKET.
    If not set: print setup instructions and exit.
    Otherwise run run_pipeline() in try/finally, call stop_and_delete_application() in finally.
    """

--- capstone/cleanup.py ---
PURPOSE: Remove ALL resources created by this capstone.
  - Delete S3 objects under s3://{EMR_S3_BUCKET}/raw/weblogs/
  - Delete S3 objects under s3://{EMR_S3_BUCKET}/processed/weblogs/
  - Delete S3 objects under s3://{EMR_S3_BUCKET}/emr-scripts/
  - Stop and delete any EMR Serverless applications matching name prefix "studybook-log-processor-"
  - Print count of deleted objects per prefix
  - End with: print("✅ Cleanup complete. No ongoing charges.")

--- capstone/test_capstone.py ---
PURPOSE: Test log generation and aggregation logic locally — no AWS calls, no EMR.

EXACT TEST FUNCTIONS:

def test_generate_log_record_has_required_fields():
    """
    from generate_logs import generate_log_record
    record = generate_log_record(datetime(2024, 1, 15, 12, 0, 0))
    required = ["timestamp", "endpoint", "method", "status_code",
                "response_time_ms", "bytes_sent", "user_agent", "ip_address"]
    assert all(k in record for k in required)
    assert record["status_code"] in [200, 201, 400, 404, 500, 503]
    """

def test_generate_log_batch_count():
    """
    from generate_logs import generate_log_batch
    records = generate_log_batch(1000)
    assert len(records) == 1000
    """

def test_log_batch_spans_multiple_days():
    """
    from generate_logs import generate_log_batch
    from datetime import datetime
    records = generate_log_batch(500)
    dates = {r["timestamp"][:10] for r in records}
    assert len(dates) >= 5  # should span at least 5 different days
    """

def test_error_status_codes_present():
    """
    from generate_logs import generate_log_batch
    records = generate_log_batch(2000)
    status_codes = {r["status_code"] for r in records}
    assert 500 in status_codes
    assert 404 in status_codes
    """

def test_log_aggregation_logic():
    """
    Test the aggregation logic from process_logs.py using pandas (no Spark).
    import pandas as pd
    records = [
        {"endpoint": "/api/orders", "status_code": 500, "hour": 14, "date": "2024-01-15",
         "response_time_ms": 1500, "bytes_sent": 200},
        {"endpoint": "/api/orders", "status_code": 500, "hour": 14, "date": "2024-01-15",
         "response_time_ms": 2000, "bytes_sent": 300},
        {"endpoint": "/api/users", "status_code": 404, "hour": 10, "date": "2024-01-15",
         "response_time_ms": 80, "bytes_sent": 100},
    ]
    df = pd.DataFrame(records)
    agg = df.groupby(["date", "endpoint", "status_code", "hour"]).agg(
        request_count=("status_code", "count"),
        avg_response_ms=("response_time_ms", "mean"),
        total_bytes=("bytes_sent", "sum"),
    ).reset_index()
    orders_row = agg[(agg["endpoint"] == "/api/orders") & (agg["status_code"] == 500)]
    assert len(orders_row) == 1
    assert orders_row.iloc[0]["request_count"] == 2
    assert orders_row.iloc[0]["total_bytes"] == 500
    assert orders_row.iloc[0]["avg_response_ms"] == 1750.0
    """

def test_cost_calculator():
    """
    from orchestrate import get_job_details  # or inline the formula
    # Validate cost formula: vcpu_hours * 0.052 + mem_gb_hours * 0.0057
    vcpu_hours = 2.0
    mem_gb_hours = 16.0
    expected = round(vcpu_hours * 0.052 + mem_gb_hours * 0.0057, 4)
    assert expected == round(2.0 * 0.052 + 16.0 * 0.0057, 4)
    assert expected > 0
    """

===== GENERATION INSTRUCTIONS =====

Generate files ONE AT A TIME in this order:
  01_emr_cluster_basics.py
  02_spark_jobs_on_emr.py
  03_emr_serverless.py
  04_cost_optimization.py
  05_monitoring_and_bootstrap.py
  capstone/brief.md
  capstone/generate_logs.py
  capstone/process_logs.py
  capstone/orchestrate.py
  capstone/cleanup.py
  capstone/test_capstone.py

Each file must be COMPLETE and FULLY RUNNABLE — no placeholders, no TODO comments, no pass statements.
Use exact function signatures shown above.
After each file, wait for me to say "next".

Acknowledge these instructions, then wait for me to say "generate file 01".
```
