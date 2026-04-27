# ============================================================
# Topic   : AWS Step Functions
# File    : capstone/capstone.py
# Covers  : full data pipeline orchestrator with validation, simulated Glue, polling, notification
# Prereqs : pip install boto3 | AWS credentials | IAM role for Step Functions
# Run     : python capstone.py
# ============================================================

"""
Data Pipeline Orchestrator — Step Functions Capstone.

Environment variables:
  AWS_REGION              — default "us-east-1"
  AWS_PROFILE             — default "study"
  STEP_FUNCTIONS_ROLE_ARN — REQUIRED to create real Step Functions resources
  SNS_TOPIC_ARN           — optional, for notification demos

State machine:
  ValidateInput
    -> StartGlueJob
      -> WaitForGlue
        -> CheckJobStatus
          -> ValidateOutput
            -> NotifySuccess
            -> NotifyFailure

If STEP_FUNCTIONS_ROLE_ARN is not set:
  - prints ASL only
  - prints cost report
  - does not create AWS resources
  - does not crash
"""

import json
import os
import time
import uuid
from typing import Any

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "study")
ROLE_ARN = os.getenv("STEP_FUNCTIONS_ROLE_ARN")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

STATE_MACHINE_NAME = f"studybook-sf-pipeline-{uuid.uuid4().hex[:8]}"

STANDARD_TRANSITION_PRICE_PER_1000 = 0.025
STANDARD_FREE_TRANSITIONS_PER_MONTH = 4_000

EXPRESS_REQUEST_PRICE_PER_MILLION = 1.00
EXPRESS_FREE_REQUESTS_PER_MONTH = 1_000_000
EXPRESS_DURATION_PRICE_PER_GB_SECOND = 0.00001


def get_client():
    return boto3.Session(
        profile_name=AWS_PROFILE,
        region_name=AWS_REGION,
    ).client("stepfunctions")


def build_retry_config(
    max_attempts: int = 3,
    interval_s: int = 2,
    backoff_rate: float = 2.0,
    error_types: list[str] | None = None,
) -> dict[str, Any]:
    if error_types is None:
        error_types = [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "States.TaskFailed",
        ]

    return {
        "ErrorEquals": error_types,
        "IntervalSeconds": interval_s,
        "MaxAttempts": max_attempts,
        "BackoffRate": backoff_rate,
    }


def build_catch_clause(
    error_types: list[str],
    next_state: str,
    result_path: str = "$.error",
) -> dict[str, Any]:
    return {
        "ErrorEquals": error_types,
        "Next": next_state,
        "ResultPath": result_path,
    }


def build_pipeline_asl() -> dict[str, Any]:
    """
    Build the full capstone pipeline ASL.

    Pipeline:
      ValidateInput
        -> StartGlueJob
          -> WaitForGlue
            -> CheckJobStatus
              -> ValidateOutput
                -> NotifySuccess

    Failure:
      Invalid input or invalid output routes to NotifyFailure.
    """
    return {
        "Comment": "StudyBook Capstone: Data Pipeline Orchestrator",
        "StartAt": "ValidateInput",
        "States": {
            "ValidateInput": {
                "Type": "Choice",
                "Comment": "Require input_file to exist and row_count > 0",
                "Choices": [
                    {
                        "And": [
                            {"Variable": "$.input_file", "IsPresent": True},
                            {"Variable": "$.input_file", "StringMatches": "s3://*"},
                            {"Variable": "$.row_count", "NumericGreaterThan": 0},
                        ],
                        "Next": "StartGlueJob",
                    }
                ],
                "Default": "NotifyFailure",
            },
            "StartGlueJob": {
                "Type": "Pass",
                "Comment": "Simulates starting an AWS Glue job",
                "Result": {
                    "job_run_id": "jr-12345",
                    "status": "RUNNING",
                    "job_name": "studybook-glue-transform",
                },
                "ResultPath": "$.glue_start",
                "Retry": [
                    build_retry_config(
                        max_attempts=3,
                        interval_s=2,
                        backoff_rate=2.0,
                        error_types=["States.TaskFailed"],
                    )
                ],
                "Catch": [
                    build_catch_clause(
                        error_types=["States.ALL"],
                        next_state="NotifyFailure",
                    )
                ],
                "Next": "WaitForGlue",
            },
            "WaitForGlue": {
                "Type": "Wait",
                "Comment": "Simulates polling delay before checking Glue status",
                "Seconds": 10,
                "Next": "CheckJobStatus",
            },
            "CheckJobStatus": {
                "Type": "Pass",
                "Comment": "Simulates Glue job polling result",
                "Result": {
                    "status": "SUCCEEDED",
                    "output_rows": 9800,
                    "output_path": "s3://bucket/curated/output/",
                },
                "ResultPath": "$.glue_status",
                "Retry": [
                    build_retry_config(
                        max_attempts=3,
                        interval_s=2,
                        backoff_rate=2.0,
                        error_types=["States.TaskFailed"],
                    )
                ],
                "Catch": [
                    build_catch_clause(
                        error_types=["States.ALL"],
                        next_state="NotifyFailure",
                    )
                ],
                "Next": "ValidateOutput",
            },
            "ValidateOutput": {
                "Type": "Choice",
                "Comment": "Require enough output rows after simulated Glue processing",
                "Choices": [
                    {
                        "Variable": "$.glue_status.output_rows",
                        "NumericGreaterThan": 1000,
                        "Next": "NotifySuccess",
                    }
                ],
                "Default": "NotifyFailure",
            },
            "NotifySuccess": {
                "Type": "Pass",
                "Comment": "Simulates success notification",
                "Parameters": {
                    "notification": "Pipeline succeeded",
                    "sns_topic_arn": SNS_TOPIC_ARN or "SNS_TOPIC_ARN not configured",
                    "input_file.$": "$.input_file",
                    "job_run_id.$": "$.glue_start.job_run_id",
                    "output_rows.$": "$.glue_status.output_rows",
                    "output_path.$": "$.glue_status.output_path",
                    "timestamp.$": "$$.State.EnteredTime",
                },
                "ResultPath": "$.success_notification",
                "End": True,
            },
            "NotifyFailure": {
                "Type": "Fail",
                "Error": "PipelineValidationError",
                "Cause": "Input or output validation failed",
            },
        },
    }


def calculate_standard_cost(n_state_transitions: int) -> float:
    billable = max(0, n_state_transitions - STANDARD_FREE_TRANSITIONS_PER_MONTH)
    return (billable / 1000) * STANDARD_TRANSITION_PRICE_PER_1000


def calculate_express_cost(
    n_executions: int,
    avg_duration_ms: int,
    avg_memory_gb: float = 0.064,
) -> float:
    billable_requests = max(0, n_executions - EXPRESS_FREE_REQUESTS_PER_MONTH)
    request_cost = (billable_requests / 1_000_000) * EXPRESS_REQUEST_PRICE_PER_MILLION
    gb_seconds = (avg_duration_ms / 1000) * avg_memory_gb * n_executions
    duration_cost = gb_seconds * EXPRESS_DURATION_PRICE_PER_GB_SECOND
    return request_cost + duration_cost


def recommend_workflow_type(
    executions_per_day: int,
    requires_exactly_once: bool,
    max_duration_s: int,
) -> str:
    if max_duration_s > 300:
        return "Standard"
    if requires_exactly_once:
        return "Standard"
    if executions_per_day > 100_000:
        return "Express"
    return "Standard"


def calculate_cost_report(n_daily_executions: int = 100) -> None:
    transitions_per_execution = 8
    monthly_executions = n_daily_executions * 30
    monthly_transitions = monthly_executions * transitions_per_execution

    standard_cost = calculate_standard_cost(monthly_transitions)
    express_cost = calculate_express_cost(
        n_executions=monthly_executions,
        avg_duration_ms=10_000,
        avg_memory_gb=0.064,
    )

    recommendation = recommend_workflow_type(
        executions_per_day=n_daily_executions,
        requires_exactly_once=True,
        max_duration_s=600,
    )

    print("\n=== CAPSTONE COST REPORT ===")
    print(f"Daily executions:          {n_daily_executions:,}")
    print(f"Monthly executions:        {monthly_executions:,}")
    print(f"Transitions per execution: {transitions_per_execution}")
    print(f"Monthly transitions:       {monthly_transitions:,}")
    print(f"Standard monthly cost:     ${standard_cost:.4f}")
    print(f"Express monthly cost:      ${express_cost:.4f}")
    print(f"Recommended workflow:      {recommendation}")
    print(
        "Reason: This pipeline simulates ETL orchestration with polling, "
        "auditability, and exactly-once preference."
    )


def create_state_machine(
    client,
    name: str,
    asl: dict[str, Any],
    role_arn: str,
) -> str:
    response = client.create_state_machine(
        name=name,
        definition=json.dumps(asl),
        roleArn=role_arn,
        type="STANDARD",
    )

    state_machine_arn = response["stateMachineArn"]

    print(f"Created state machine: {name}")
    print(f"State machine ARN: {state_machine_arn}")
    print("⚠️  COST: Standard workflow charges $0.025/1000 state transitions.")

    return state_machine_arn


def start_execution(
    client,
    state_machine_arn: str,
    input_dict: dict[str, Any],
    execution_name: str | None = None,
) -> str:
    if execution_name is None:
        execution_name = f"exec-{uuid.uuid4().hex[:8]}"

    response = client.start_execution(
        stateMachineArn=state_machine_arn,
        name=execution_name,
        input=json.dumps(input_dict),
    )

    execution_arn = response["executionArn"]
    print(f"Started execution: {execution_name}")
    print(f"Execution ARN: {execution_arn}")

    return execution_arn


def wait_for_completion(
    client,
    execution_arn: str,
    poll_interval: int = 2,
    timeout: int = 90,
) -> dict[str, Any]:
    terminal_statuses = {"SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"}
    start_time = time.time()

    while True:
        elapsed = int(time.time() - start_time)

        if elapsed > timeout:
            raise TimeoutError(
                f"Execution did not reach terminal status within {timeout}s: "
                f"{execution_arn}"
            )

        response = client.describe_execution(executionArn=execution_arn)
        status = response["status"]

        if status in terminal_statuses:
            print(f"Status: {status} (elapsed: {elapsed}s)")
            return response

        print(f"Status: {status}... (elapsed: {elapsed}s)")
        time.sleep(poll_interval)


def delete_state_machine(client, arn: str) -> None:
    try:
        client.delete_state_machine(stateMachineArn=arn)
        print(f"Deleted state machine: {arn}")
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code", "")

        if error_code == "StateMachineDoesNotExist":
            return

        raise


def cleanup(client, state_machine_arn: str) -> None:
    delete_state_machine(client, state_machine_arn)
    print("✅ Cleanup complete. No ongoing charges.")


def run_pipeline_capstone(client, role_arn: str) -> dict[str, Any]:
    asl = build_pipeline_asl()

    sm_arn = create_state_machine(
        client=client,
        name=STATE_MACHINE_NAME,
        asl=asl,
        role_arn=role_arn,
    )

    print("\n=== VALID PIPELINE RUN ===")
    valid_exec = start_execution(
        client=client,
        state_machine_arn=sm_arn,
        input_dict={
            "input_file": "s3://bucket/data.csv",
            "row_count": 10_000,
            "pipeline_name": "capstone-valid-demo",
        },
    )
    valid_result = wait_for_completion(client, valid_exec)

    print("\n=== INVALID PIPELINE RUN ===")
    invalid_exec = start_execution(
        client=client,
        state_machine_arn=sm_arn,
        input_dict={
            "input_file": "",
            "row_count": 0,
            "pipeline_name": "capstone-invalid-demo",
        },
    )
    invalid_result = wait_for_completion(client, invalid_exec)

    return {
        "sm_arn": sm_arn,
        "valid_status": valid_result["status"],
        "invalid_status": invalid_result["status"],
        "valid_output": valid_result.get("output", "N/A"),
        "invalid_error": invalid_result.get("error", "N/A"),
        "invalid_cause": invalid_result.get("cause", "N/A"),
    }


def main() -> None:
    asl = build_pipeline_asl()

    print("=== PIPELINE ASL ===")
    print(json.dumps(asl, indent=2))

    calculate_cost_report(n_daily_executions=100)

    if not ROLE_ARN:
        print("\nSTEP_FUNCTIONS_ROLE_ARN not set — ASL display only. Set STEP_FUNCTIONS_ROLE_ARN to run.")
        return

    client = get_client()
    sm_arn: str | None = None

    try:
        stats = run_pipeline_capstone(client, ROLE_ARN)
        sm_arn = stats["sm_arn"]

        print("\n=== CAPSTONE SUMMARY ===")
        print(f"Valid run status:   {stats['valid_status']}")
        print(f"Invalid run status: {stats['invalid_status']}")
        print(f"Invalid error:      {stats['invalid_error']}")
        print(f"Invalid cause:      {stats['invalid_cause']}")

    finally:
        if sm_arn:
            cleanup(client, sm_arn)


if __name__ == "__main__":
    main()