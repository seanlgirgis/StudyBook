# ChatGPT Prompt — AWS Step Functions for Data Engineers
# READY TO PASTE — fully specified, no placeholders
# Paste everything between the === markers into ChatGPT

===

TOPIC: AWS Step Functions for Data Engineers
SLUG: aws_step_functions
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: AWS — boto3, real AWS account required
AWS_PROFILE = "study"

===== CODING STANDARDS =====

FILE HEADER (every file):
# ============================================================
# Topic   : AWS Step Functions
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install boto3 | AWS credentials | IAM role for Step Functions
# Run     : python NN_filename.py
# ============================================================

ENVIRONMENT VARIABLES (document at top of every file):
  AWS_REGION                 — default "us-east-1"
  AWS_PROFILE                — default "study"
  STEP_FUNCTIONS_ROLE_ARN    — REQUIRED: IAM role ARN for Step Functions
  SNS_TOPIC_ARN              — optional, for notification demos

CRITICAL — If STEP_FUNCTIONS_ROLE_ARN is not set:
  Print a clear message: "STEP_FUNCTIONS_ROLE_ARN not set — showing ASL definitions only"
  Show the generated ASL JSON without creating real AWS resources.
  Run cost calculations and local logic. Never crash on missing env vars.

CLEANUP RULES (mandatory for all AWS files):
  C1: Every main() wraps ALL demo code in try/finally. cleanup() in finally.
  C2: Each file cleans up its own resources (its own state machines).
  C3: Idempotent cleanup — catch StateMachineDoesNotExist silently.
  C4: Print ⚠️ COST WARNING after creating state machine.
      "⚠️  COST: Standard workflow charges $0.025/1000 state transitions."
  C5: Print "✅ Cleanup complete. No ongoing charges." at end of cleanup().

NOTE: Step Functions Standard workflows have no idle cost — charge per state transition.
Express workflows: $1/million executions + duration. Both are cheap for testing.

CODING:
  - Python 3.11+, type hints, json for ASL generation
  - All resource names: f"studybook-sf-{uuid.uuid4().hex[:8]}" suffix
  - boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
  - ASL defined as Python dicts, json.dumps(asl_dict, indent=2) for display

===== FILE 01: 01_state_machine_basics.py =====

import boto3, json, os, time, uuid
from botocore.exceptions import ClientError

STATE_MACHINE_NAME = f"studybook-sf-basics-{uuid.uuid4().hex[:8]}"
AWS_REGION   = os.getenv("AWS_REGION",  "us-east-1")
AWS_PROFILE  = os.getenv("AWS_PROFILE", "study")
ROLE_ARN     = os.getenv("STEP_FUNCTIONS_ROLE_ARN")

def get_client():
    return boto3.Session(profile_name=AWS_PROFILE,
                         region_name=AWS_REGION).client("stepfunctions")

def build_simple_asl() -> dict:
    """
    Build a simple ASL (Amazon States Language) definition as a Python dict.
    States: Start → ProcessData (Pass state) → Validate (Pass state) → Done (Succeed state)
    WHY Pass state: a no-op state that passes input to output unchanged.
    Perfect for scaffolding a pipeline before replacing with real Task states.
    WHY Succeed state: explicitly marks successful terminal. Without it,
    the last state would implicitly end, but Succeed makes intent clear.
    Return ASL dict. Print json.dumps(asl, indent=2).
    """
    return {
        "Comment": "StudyBook: basic state machine",
        "StartAt": "ProcessData",
        "States": {
            "ProcessData": {
                "Type": "Pass",
                "Comment": "Pass state: input flows through unchanged",
                "Next": "Validate"
            },
            "Validate": {
                "Type": "Pass",
                "Result": {"validated": True},
                "ResultPath": "$.validation",
                "Next": "Done"
            },
            "Done": {
                "Type": "Succeed",
                "Comment": "Terminal success state"
            }
        }
    }

def create_state_machine(client, name: str, asl: dict, role_arn: str) -> str:
    """
    Create Standard workflow state machine.
    definition = json.dumps(asl)
    Return state machine ARN.
    Print ⚠️ COST WARNING.
    """

def start_execution(client, state_machine_arn: str,
                    input_dict: dict, execution_name: str = None) -> str:
    """
    Start execution. execution_name defaults to f"exec-{uuid.uuid4().hex[:8]}".
    input must be JSON string: json.dumps(input_dict)
    Return execution ARN.
    Print execution ARN.
    """

def wait_for_completion(client, execution_arn: str,
                        poll_interval: int = 2, timeout: int = 60) -> dict:
    """
    Poll describe_execution every poll_interval seconds.
    Terminal statuses: SUCCEEDED, FAILED, TIMED_OUT, ABORTED.
    Raise TimeoutError if not terminal within timeout seconds.
    Return execution description dict.
    Print status on each poll: "Status: RUNNING... (elapsed: 4s)"
    """

def get_execution_history(client, execution_arn: str) -> list[dict]:
    """
    Call get_execution_history (paginated). Return list of events.
    Print each event: timestamp, type, and relevant data.
    WHY history: Step Functions logs every state transition. This is the audit trail
    Toyota would use to trace exactly what happened in a failed pipeline run.
    """

def delete_state_machine(client, arn: str) -> None:
    """Delete state machine. Catch StateMachineDoesNotExist silently."""

def cleanup(client, state_machine_arn: str) -> None:
    """Delete state machine. Print ✅ Cleanup complete."""

def main():
    client = get_client()
    asl = build_simple_asl()

    if not ROLE_ARN:
        print("STEP_FUNCTIONS_ROLE_ARN not set — showing ASL only:")
        print(json.dumps(asl, indent=2))
        return

    sm_arn = None
    try:
        print("\n=== CREATE STATE MACHINE ===")
        sm_arn = create_state_machine(client, STATE_MACHINE_NAME, asl, ROLE_ARN)

        print("\n=== START EXECUTION ===")
        exec_arn = start_execution(client, sm_arn,
                                   {"sensor_id": "s001", "value": 72.5})

        print("\n=== WAIT FOR COMPLETION ===")
        result = wait_for_completion(client, exec_arn)
        print(f"Final status: {result['status']}")
        print(f"Output: {result.get('output', 'N/A')}")

        print("\n=== EXECUTION HISTORY ===")
        history = get_execution_history(client, exec_arn)
        print(f"Total events: {len(history)}")
    finally:
        if sm_arn:
            cleanup(client, sm_arn)

if __name__ == "__main__":
    main()

===== FILE 02: 02_task_states_and_lambda.py =====

PURPOSE: Task states and Lambda integration — the most common Step Functions pattern.
NOTE: This file creates ONLY the ASL definitions and state machine structure.
No real Lambda functions are created — use mock ARNs for ASL demonstration.
The state machine itself IS created (if ROLE_ARN is set) with Pass states
simulating Lambda results.

def build_lambda_task_state(lambda_arn: str, timeout_s: int = 300,
                             heartbeat_s: int = 60) -> dict:
    """
    Build an ASL Task state dict for Lambda integration.
    Use Resource: "arn:aws:states:::lambda:invoke.waitForTaskToken" for sync:2 pattern
    OR Resource: f"arn:aws:states:::lambda:invoke" for sync pattern.
    Include TimeoutSeconds and HeartbeatSeconds.
    WHY .sync vs .sync:2:
      .sync:  Step Functions polls Lambda for completion (Lambda must be synchronous)
      .sync:2 (waitForTaskToken): Lambda receives a task token, does async work,
              calls send_task_success when done. Used for long-running jobs.
    Return ASL state dict.
    """

def build_pipeline_asl(lambda_arns: list[str]) -> dict:
    """
    Build 3-step data pipeline ASL:
      ExtractData (Task → lambda_arns[0])
        → TransformData (Task → lambda_arns[1])
          → LoadData (Task → lambda_arns[2])
            → PipelineSucceeded (Succeed)
    Each Task state: TimeoutSeconds=300, HeartbeatSeconds=60.
    Add error handling to each: Retry on Lambda.ServiceException with 3 attempts.
    Return complete ASL dict. Print json.dumps.
    WHY retry on Lambda.ServiceException: Lambda occasionally has cold start failures
    or throttles. Automatic retry with exponential backoff handles transient failures.
    """

def demonstrate_sync_patterns() -> None:
    """
    Print comparison of Lambda integration patterns:

    Pattern                    | Resource suffix           | When to use
    ---------------------------|---------------------------|----------------------------
    Synchronous (request/resp) | :invoke                   | Fast Lambda (< 15 min)
    Sync with polling          | :invoke.waitForTaskToken  | Long-running async work
    Fire and forget            | :invoke (async)           | Background tasks, no result needed

    Also show: ResultSelector and ResultPath for extracting Lambda response fields:
      "ResultSelector": {"processed_rows.$": "$.Payload.processed_rows"}
      "ResultPath": "$.extract_result"
    """

def main():
    client = get_client()
    MOCK_ARNS = [
        f"arn:aws:lambda:{AWS_REGION}:123456789:function:mock-extract",
        f"arn:aws:lambda:{AWS_REGION}:123456789:function:mock-transform",
        f"arn:aws:lambda:{AWS_REGION}:123456789:function:mock-load",
    ]

    asl = build_pipeline_asl(MOCK_ARNS)
    print("=== 3-STEP LAMBDA PIPELINE ASL ===")
    print(json.dumps(asl, indent=2))

    print("\n=== SYNC PATTERNS ===")
    demonstrate_sync_patterns()

    if not ROLE_ARN:
        print("\nROLE_ARN not set — skipping state machine creation")
        return

    sm_arn = None
    try:
        # Create with Pass states (not real Lambda) for safe execution
        safe_asl = {
            "StartAt": "ExtractData",
            "States": {
                "ExtractData":   {"Type": "Pass", "Next": "TransformData",
                                  "Result": {"rows": 1000}},
                "TransformData": {"Type": "Pass", "Next": "LoadData",
                                  "Result": {"transformed": True}},
                "LoadData":      {"Type": "Pass", "Next": "Done",
                                  "Result": {"loaded": True}},
                "Done":          {"Type": "Succeed"}
            }
        }
        sm_arn = create_state_machine(
            client, f"studybook-sf-pipeline-{uuid.uuid4().hex[:8]}", safe_asl, ROLE_ARN)
        exec_arn = start_execution(client, sm_arn, {"batch_id": "B001"})
        result = wait_for_completion(client, exec_arn)
        print(f"\nPipeline execution: {result['status']}")
    finally:
        if sm_arn:
            cleanup(client, sm_arn)

if __name__ == "__main__":
    main()

===== FILE 03: 03_parallel_and_map_states.py =====

def build_parallel_asl() -> dict:
    """
    Build an ASL with a Parallel state running 3 branches simultaneously:
      Branch 1: ExtractFromDB    (Pass, returns {"source": "db", "rows": 1000})
      Branch 2: ExtractFromAPI   (Pass, returns {"source": "api", "rows": 500})
      Branch 3: ExtractFromFiles (Pass, returns {"source": "files", "rows": 200})
    After Parallel: MergeResults (Pass state combining all branch outputs)
    WHY Parallel: Step Functions runs all branches simultaneously and waits for ALL
    to complete before proceeding. Perfect for parallel ETL from multiple sources.
    Output: array of each branch's final output.
    Print ASL. Return dict.
    """

def build_map_asl() -> dict:
    """
    Build an ASL with a Map state processing each item in an array:
    Input: {"files": ["file1.csv", "file2.csv", "file3.csv"]}
    Map state: ItemsPath: "$.files", MaxConcurrency: 5
    Iterator: ProcessFile (Pass state, adds {"processed": true} to each item)
    After Map: WriteResults (Pass state)
    WHY Map: processes each element of an array with the same logic.
    MaxConcurrency limits simultaneous iterations — prevents Lambda throttling.
    MaxConcurrency: 0 = unlimited (process all in parallel).
    Print ASL. Return dict.
    """

def compare_parallel_vs_map() -> None:
    """
    Print formatted comparison:

    Feature           | Parallel State              | Map State
    ------------------|----------------------------|---------------------------
    Input             | Same input to all branches | Array — one item per iter
    Branches          | Fixed at design time        | Dynamic — scales with array
    Output            | Array of branch outputs     | Array of iter outputs
    MaxConcurrency    | N/A (all branches run)      | Configurable (0=unlimited)
    Use case          | Fan-out to different sources| Process collection of items
    Example           | Extract from 3 DBs at once  | Process 1000 S3 files

    Also explain: Parallel + Map can be nested. A common pattern:
    Map over a list of data sources, each iteration runs a Parallel of extract+validate.
    """

def main():
    print("=== PARALLEL STATE ASL ===")
    parallel_asl = build_parallel_asl()
    print(json.dumps(parallel_asl, indent=2))

    print("\n=== MAP STATE ASL ===")
    map_asl = build_map_asl()
    print(json.dumps(map_asl, indent=2))

    print("\n=== PARALLEL vs MAP COMPARISON ===")
    compare_parallel_vs_map()

    if not ROLE_ARN:
        return

    client = get_client()
    sm_arn = None
    try:
        sm_arn = create_state_machine(
            client, f"studybook-sf-map-{uuid.uuid4().hex[:8]}", map_asl, ROLE_ARN)
        exec_arn = start_execution(
            client, sm_arn,
            {"files": ["file1.csv", "file2.csv", "file3.csv"]})
        result = wait_for_completion(client, exec_arn)
        print(f"\nMap execution: {result['status']}")
        print(f"Output: {result.get('output', 'N/A')[:200]}")
    finally:
        if sm_arn:
            cleanup(client, sm_arn)

if __name__ == "__main__":
    main()

===== FILE 04: 04_error_handling_and_retry.py =====

def build_retry_config(max_attempts: int = 3, interval_s: int = 2,
                        backoff_rate: float = 2.0,
                        error_types: list[str] = None) -> dict:
    """
    Build an ASL Retry clause dict.
    Default error_types: ["Lambda.ServiceException", "Lambda.AWSLambdaException",
                          "Lambda.SdkClientException", "States.TaskFailed"]
    WHY exponential backoff: retrying immediately after a transient failure often
    hits the same overloaded resource. Backoff gives the system time to recover.
    WHY these error types: Lambda errors are transient and retryable.
    States.TaskFailed covers business logic failures that should NOT be retried
    (add only if idempotent).
    Return dict: { "ErrorEquals": [...], "IntervalSeconds": n,
                   "MaxAttempts": n, "BackoffRate": n }
    """

def build_catch_clause(error_types: list[str], next_state: str,
                        result_path: str = "$.error") -> dict:
    """
    Build an ASL Catch clause dict.
    result_path: where to put the error info in the state input (default "$.error").
    WHY Catch: after all retries are exhausted, Catch routes to a compensating state
    instead of failing the entire execution. Critical for pipelines that must
    clean up on failure.
    Return dict: { "ErrorEquals": [...], "Next": next_state, "ResultPath": result_path }
    """

def build_resilient_pipeline_asl() -> dict:
    """
    Build a pipeline ASL with full retry + catch:
    States:
      ValidateInput (Pass — validates input has required fields)
      ProcessData   (Pass — simulates data processing, can "fail")
        Retry: 3 attempts, 2s interval, backoff 2.0 on States.TaskFailed
        Catch: States.ALL → HandleError
      HandleError   (Pass — logs error info, Result: {"compensated": true})
        Next: → SendFailureNotification
      SendFailureNotification (Pass — simulates SNS notification)
        Next: → PipelineFailed
      PipelineFailed  (Fail state, Error: "PipelineError", Cause: "See $.error")
      LoadResults   (Pass — runs on ProcessData success)
        Next: → PipelineSucceeded
      PipelineSucceeded (Succeed)

    Print ASL. Return dict.
    WHY Fail state after handling: even after compensation, mark the execution
    as FAILED so monitoring systems know this run did not complete normally.
    """

def main():
    asl = build_resilient_pipeline_asl()
    print("=== RESILIENT PIPELINE ASL ===")
    print(json.dumps(asl, indent=2))

    if not ROLE_ARN:
        print("\nROLE_ARN not set — ASL display only")
        return

    client = get_client()
    sm_arn = None
    try:
        sm_arn = create_state_machine(
            client, f"studybook-sf-resilient-{uuid.uuid4().hex[:8]}", asl, ROLE_ARN)

        print("\n=== SUCCESSFUL EXECUTION ===")
        exec_ok = start_execution(client, sm_arn, {"valid": True, "data": [1, 2, 3]})
        r_ok = wait_for_completion(client, exec_ok)
        print(f"Status: {r_ok['status']}")

        print("\n=== EXECUTION SHOWING CATCH (invalid input triggers error path) ===")
        exec_fail = start_execution(client, sm_arn, {"valid": False})
        r_fail = wait_for_completion(client, exec_fail)
        print(f"Status: {r_fail['status']}")
    finally:
        if sm_arn:
            cleanup(client, sm_arn)

if __name__ == "__main__":
    main()

===== FILE 05: 05_express_workflows_and_cost.py =====

def calculate_standard_cost(n_state_transitions: int) -> float:
    """
    Standard workflow pricing: $0.025 per 1,000 state transitions.
    First 4,000 per month are free.
    Return monthly cost in USD. Print breakdown.
    """

def calculate_express_cost(n_executions: int,
                            avg_duration_ms: int,
                            avg_memory_gb: float = 0.064) -> float:
    """
    Express workflow pricing (us-east-1):
      Requests: $1.00 per 1,000,000 executions (first 1M free/month)
      Duration: $0.00001 per GB-second
    duration_gb_seconds = (avg_duration_ms / 1000) * avg_memory_gb * n_executions
    Return total monthly cost. Print breakdown.
    """

def recommend_workflow_type(executions_per_day: int,
                             requires_exactly_once: bool,
                             max_duration_s: int) -> str:
    """
    Decision rules:
      max_duration_s > 300   → Standard (Express max = 5 minutes)
      requires_exactly_once  → Standard (Express is at-least-once)
      executions_per_day > 100_000 → Express (much cheaper at scale)
      else → Standard (simpler, has execution history)
    Print recommendation and reasoning.
    Return "Standard" or "Express".
    """

def compare_all_scenarios() -> None:
    """
    Print cost comparison for 3 real-world scenarios:

    Scenario 1: Daily ETL pipeline
      - 1 execution/day, 50 transitions, 10 minutes long, exactly-once required
      → Standard. Cost: ~$0.00/month (within free tier)

    Scenario 2: IoT event processing
      - 1,000,000 executions/day, 5 transitions each, 2 seconds, at-least-once ok
      → Express. Cost: ~$4.60/month

    Scenario 3: Microservice orchestration
      - 500,000 executions/day, 3 transitions, 0.5 seconds, at-least-once ok
      → Express. Cost: ~$1.55/month

    For each scenario: show both Standard and Express cost, then recommended choice.
    """

def demonstrate_execution_difference() -> None:
    """
    Print key behavioral differences:

    Feature                | Standard Workflow    | Express Workflow
    -----------------------|---------------------|-------------------
    Max duration           | 1 year              | 5 minutes
    Execution semantics    | Exactly-once        | At-least-once
    Execution history      | Yes (90 days)       | No (CloudWatch only)
    Max state transitions  | Unlimited           | Unlimited
    Pricing model          | Per state transition | Per execution + duration
    Break-even point       | < ~30k exec/day     | > ~30k exec/day
    Use case               | ETL, long pipelines | IoT, high-volume events

    WHY exactly-once matters for ETL: ensures a Glue job isn't triggered twice
    for the same input — would cause duplicate data in the data lake.
    WHY Express for IoT: millions of sensor events/day. At-least-once is acceptable
    for telemetry — losing or duplicating a single sensor reading is tolerable.
    """

def main():
    print("=== COST CALCULATOR ===")
    standard_cost = calculate_standard_cost(n_state_transitions=10_000)
    express_cost  = calculate_express_cost(n_executions=100_000,
                                            avg_duration_ms=500)
    print(f"Standard (10k transitions/month): ${standard_cost:.4f}")
    print(f"Express  (100k executions/month): ${express_cost:.4f}")

    print("\n=== WORKFLOW RECOMMENDATION ===")
    recommend_workflow_type(executions_per_day=1,      requires_exactly_once=True,  max_duration_s=600)
    recommend_workflow_type(executions_per_day=500_000, requires_exactly_once=False, max_duration_s=5)

    print("\n=== SCENARIO COMPARISON ===")
    compare_all_scenarios()

    print("\n=== BEHAVIORAL DIFFERENCES ===")
    demonstrate_execution_difference()

    if not ROLE_ARN:
        return

    client = get_client()
    sm_arn = None
    try:
        express_asl = {
            "StartAt": "Process",
            "States": {"Process": {"Type": "Pass", "End": True}}
        }
        sm_arn = create_state_machine(
            client, f"studybook-sf-express-{uuid.uuid4().hex[:8]}",
            express_asl, ROLE_ARN)  # type="EXPRESS" — add to create call
        exec_arn = start_execution(client, sm_arn, {"event": "iot_reading"})
        result   = wait_for_completion(client, exec_arn, timeout=30)
        print(f"\nExpress execution: {result['status']}")
    finally:
        if sm_arn:
            cleanup(client, sm_arn)

if __name__ == "__main__":
    main()

===== CAPSTONE PROJECT =====

Title: Data Pipeline Orchestrator
Scenario: Step Functions state machine orchestrates: validate input → trigger Glue job
(simulated) → poll for completion → validate output → notify success or failure.

Directory layout:
  capstone/
    capstone.py       ← full orchestration
    test_capstone.py  ← pytest mocking boto3

===== CAPSTONE FILE: capstone.py =====

"""
Data Pipeline Orchestrator — Step Functions Capstone.

State machine:
  ValidateInput → StartGlueJob (Pass, simulated) → WaitForGlue (polling loop via Wait+Choice)
    → ValidateOutput → NotifySuccess
                     → NotifyFailure (on any error via Catch)

If STEP_FUNCTIONS_ROLE_ARN not set: prints ASL only (no AWS resources created).
"""

STATE_MACHINE_NAME = f"studybook-sf-pipeline-{uuid.uuid4().hex[:8]}"

def build_pipeline_asl() -> dict:
    """
    Build the full pipeline ASL:

    ValidateInput (Choice state):
      - If $.input_file exists and $.row_count > 0 → StartGlueJob
      - Else → NotifyFailure

    StartGlueJob (Pass state — simulates Glue job start):
      Result: {"job_run_id": "jr-12345", "status": "RUNNING"}
      Next: WaitForGlue

    WaitForGlue (Wait state, 10 seconds):
      Next: CheckJobStatus

    CheckJobStatus (Pass state — simulates polling):
      Result: {"status": "SUCCEEDED", "output_rows": 9800}
      Next: ValidateOutput

    ValidateOutput (Choice state):
      - If $.output_rows > 1000 → NotifySuccess
      - Else → NotifyFailure

    NotifySuccess (Pass state):
      Result: {"notification": "Pipeline succeeded", "timestamp": "..."}
      End: true

    NotifyFailure (Fail state):
      Error: "PipelineValidationError"
      Cause: "Input or output validation failed"

    Add Catch on ValidateInput and CheckJobStatus:
      States.ALL → NotifyFailure

    Return dict.
    """

def run_pipeline_capstone(client, role_arn: str) -> dict:
    """
    Full run:
      1. Create state machine
      2. Run with valid input {"input_file": "s3://bucket/data.csv", "row_count": 10000}
      3. Wait for completion
      4. Run with invalid input {"input_file": "", "row_count": 0}
      5. Wait for completion (should reach NotifyFailure)
      6. Print summary of both runs
      7. Return { sm_arn, valid_status, invalid_status }
    """

def calculate_cost_report(n_daily_executions: int = 100) -> None:
    """
    Print cost estimate for 100 daily pipeline executions:
      Transitions per execution: ~8 (ValidateInput + Start + Wait + Check + ValidateOutput + Notify)
      Monthly transitions: 100 × 30 × 8 = 24,000
      Monthly cost: (24,000 / 1,000) × $0.025 = $0.60
    Print formatted report. Compare Standard vs Express cost.
    """

def main():
    asl = build_pipeline_asl()
    print("=== PIPELINE ASL ===")
    print(json.dumps(asl, indent=2))

    calculate_cost_report(n_daily_executions=100)

    if not ROLE_ARN:
        print("\nROLE_ARN not set — ASL display only. Set STEP_FUNCTIONS_ROLE_ARN to run.")
        return

    client = get_client()
    sm_arn = None
    try:
        stats = run_pipeline_capstone(client, ROLE_ARN)
        sm_arn = stats["sm_arn"]
        print(f"\nValid run:   {stats['valid_status']}")
        print(f"Invalid run: {stats['invalid_status']}")
    finally:
        if sm_arn:
            cleanup(client, sm_arn)

if __name__ == "__main__":
    main()

===== CAPSTONE FILE: test_capstone.py =====

"""
pytest — 5 tests. Mocks boto3 so no real AWS calls needed.
Run: pytest test_capstone.py -v
"""
import json, pytest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from capstone import (build_pipeline_asl, calculate_cost_report,
                       build_retry_config, build_catch_clause,
                       calculate_standard_cost, recommend_workflow_type)

def test_pipeline_asl_has_required_states():
    """ASL must contain all 7 required state names."""
    asl = build_pipeline_asl()
    states = set(asl["States"].keys())
    required = {"ValidateInput", "StartGlueJob", "WaitForGlue",
                 "CheckJobStatus", "ValidateOutput", "NotifySuccess", "NotifyFailure"}
    assert required.issubset(states), f"Missing: {required - states}"

def test_pipeline_asl_starts_at_validate():
    """StartAt must be ValidateInput."""
    asl = build_pipeline_asl()
    assert asl["StartAt"] == "ValidateInput"

def test_notify_failure_is_fail_state():
    """NotifyFailure must be a Fail state."""
    asl = build_pipeline_asl()
    assert asl["States"]["NotifyFailure"]["Type"] == "Fail"

def test_standard_cost_calculation():
    """10,000 transitions beyond free tier = $0.15."""
    # 4,000 free, 6,000 billable = 6 × $0.025 = $0.15
    cost = calculate_standard_cost(n_state_transitions=10_000)
    assert abs(cost - 0.15) < 0.01, f"Expected ~$0.15, got ${cost:.4f}"

def test_recommend_express_for_high_volume():
    """High-volume, at-least-once, short duration → Express."""
    rec = recommend_workflow_type(
        executions_per_day=500_000,
        requires_exactly_once=False,
        max_duration_s=5)
    assert rec == "Express"

===== GENERATION SEQUENCE =====

Acknowledge these instructions, then wait for me to say "generate file 01".

  "generate file 01"  → 01_state_machine_basics.py
  "generate file 02"  → 02_task_states_and_lambda.py
  "generate file 03"  → 03_parallel_and_map_states.py
  "generate file 04"  → 04_error_handling_and_retry.py
  "generate file 05"  → 05_express_workflows_and_cost.py
  "generate readme"   → README.md
  "generate capstone" → capstone/capstone.py
  "generate tests"    → capstone/test_capstone.py

Each file COMPLETE and FULLY RUNNABLE. No placeholders. No pass statements.

===
