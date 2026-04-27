# ============================================================
# Topic   : AWS Step Functions
# File    : 04_error_handling_and_retry.py
# Covers  : Retry clauses, Catch clauses, Fail states, compensation paths
# Prereqs : pip install boto3 | AWS credentials | IAM role for Step Functions
# Run     : python 04_error_handling_and_retry.py
# ============================================================

"""
Environment variables:
  AWS_REGION              — default "us-east-1"
  AWS_PROFILE             — default "study"
  STEP_FUNCTIONS_ROLE_ARN — REQUIRED to create real Step Functions resources
  SNS_TOPIC_ARN           — optional, for notification demos

If STEP_FUNCTIONS_ROLE_ARN is not set:
  - prints ASL definitions only
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

STANDARD_TRANSITION_PRICE_PER_1000 = 0.025


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
    """
    Build an ASL Retry clause.

    WHY exponential backoff:
      Retrying immediately after a transient failure often hits the same
      overloaded dependency. Backoff gives the system time to recover.

    WHY these error types:
      Lambda service and SDK errors are usually transient.
      States.TaskFailed should be retried only when the task is idempotent.
    """
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
    """
    Build an ASL Catch clause.

    WHY Catch:
      After retries are exhausted, Catch routes execution to a compensating
      state instead of immediately failing the whole workflow.

    Data engineering example:
      If a load step fails, Catch can route to cleanup, alerting, rollback,
      quarantine, or dead-letter handling.
    """
    return {
        "ErrorEquals": error_types,
        "Next": next_state,
        "ResultPath": result_path,
    }


def build_resilient_pipeline_asl() -> dict[str, Any]:
    """
    Build a resilient pipeline ASL with retry + catch.

    Flow:
      ValidateInput
        -> ProcessData
          -> LoadResults
            -> PipelineSucceeded

    Failure path:
      ProcessData Catch
        -> HandleError
          -> SendFailureNotification
            -> PipelineFailed

    Important teaching point:
      A Fail state after compensation is intentional. It tells monitoring that
      the pipeline did not complete normally.
    """
    return {
        "Comment": "StudyBook: resilient Step Functions pipeline with Retry and Catch",
        "StartAt": "ValidateInput",
        "States": {
            "ValidateInput": {
                "Type": "Choice",
                "Comment": "Validate required fields before processing",
                "Choices": [
                    {
                        "And": [
                            {"Variable": "$.valid", "BooleanEquals": True},
                            {"Variable": "$.data", "IsPresent": True},
                        ],
                        "Next": "ProcessData",
                    }
                ],
                "Default": "HandleError",
            },
            "ProcessData": {
                "Type": "Pass",
                "Comment": "Simulates successful processing for valid input",
                "Result": {
                    "processed": True,
                    "records_processed": 3,
                },
                "ResultPath": "$.process_result",
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
                        next_state="HandleError",
                        result_path="$.error",
                    )
                ],
                "Next": "LoadResults",
            },
            "HandleError": {
                "Type": "Pass",
                "Comment": "Simulates compensation or cleanup logic",
                "Result": {
                    "compensated": True,
                    "action": "cleanup_complete",
                },
                "ResultPath": "$.compensation",
                "Next": "SendFailureNotification",
            },
            "SendFailureNotification": {
                "Type": "Pass",
                "Comment": "Simulates SNS/email/Slack notification",
                "Parameters": {
                    "notification": "Pipeline failed",
                    "sns_topic_arn": SNS_TOPIC_ARN or "SNS_TOPIC_ARN not configured",
                    "original_input.$": "$",
                },
                "ResultPath": "$.failure_notification",
                "Next": "PipelineFailed",
            },
            "PipelineFailed": {
                "Type": "Fail",
                "Error": "PipelineError",
                "Cause": "Input validation or processing failed",
            },
            "LoadResults": {
                "Type": "Pass",
                "Comment": "Simulates loading processed results",
                "Result": {
                    "loaded": True,
                    "target": "mock-warehouse",
                },
                "ResultPath": "$.load_result",
                "Next": "PipelineSucceeded",
            },
            "PipelineSucceeded": {
                "Type": "Succeed",
            },
        },
    }


def create_state_machine(
    client,
    name: str,
    asl: dict[str, Any],
    role_arn: str,
    workflow_type: str = "STANDARD",
) -> str:
    response = client.create_state_machine(
        name=name,
        definition=json.dumps(asl),
        roleArn=role_arn,
        type=workflow_type,
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
    timeout: int = 60,
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


def calculate_demo_cost(n_state_transitions: int) -> float:
    cost = (n_state_transitions / 1000) * STANDARD_TRANSITION_PRICE_PER_1000

    print("\n=== COST ESTIMATE ===")
    print(f"Estimated transitions: {n_state_transitions}")
    print("Standard workflow price: $0.025 per 1,000 state transitions")
    print(f"Estimated cost: ${cost:.6f}")

    return cost


def demonstrate_retry_and_catch() -> None:
    print("\n=== RETRY CONFIG EXAMPLE ===")
    print(json.dumps(build_retry_config(), indent=2))

    print("\n=== CATCH CLAUSE EXAMPLE ===")
    print(
        json.dumps(
            build_catch_clause(
                error_types=["States.ALL"],
                next_state="HandleError",
            ),
            indent=2,
        )
    )

    print(
        """
Key idea:
  Retry handles temporary failures.
  Catch handles final failure after retries are exhausted.

Production pattern:
  Task -> Retry transient errors -> Catch permanent failure -> Cleanup/Notify -> Fail

Why still end with Fail?
  Because compensation does not mean success.
  The pipeline recovered safely, but the business process still failed.
""".strip()
    )


def main() -> None:
    asl = build_resilient_pipeline_asl()

    print("=== RESILIENT PIPELINE ASL ===")
    print(json.dumps(asl, indent=2))

    demonstrate_retry_and_catch()
    calculate_demo_cost(n_state_transitions=7)

    if not ROLE_ARN:
        print("\nSTEP_FUNCTIONS_ROLE_ARN not set — ASL display only")
        print("Skipping state machine creation.")
        return

    client = get_client()
    sm_arn: str | None = None

    try:
        print("\n=== CREATE STATE MACHINE ===")
        sm_arn = create_state_machine(
            client=client,
            name=f"studybook-sf-resilient-{uuid.uuid4().hex[:8]}",
            asl=asl,
            role_arn=ROLE_ARN,
        )

        print("\n=== SUCCESSFUL EXECUTION ===")
        exec_ok = start_execution(
            client=client,
            state_machine_arn=sm_arn,
            input_dict={
                "valid": True,
                "data": [1, 2, 3],
                "batch_id": "B004-success",
            },
        )
        result_ok = wait_for_completion(client=client, execution_arn=exec_ok)
        print(f"Status: {result_ok['status']}")
        print(f"Output: {result_ok.get('output', 'N/A')}")

        print("\n=== FAILURE EXECUTION ===")
        exec_fail = start_execution(
            client=client,
            state_machine_arn=sm_arn,
            input_dict={
                "valid": False,
                "batch_id": "B004-failure",
            },
        )
        result_fail = wait_for_completion(client=client, execution_arn=exec_fail)
        print(f"Status: {result_fail['status']}")
        print(f"Error: {result_fail.get('error', 'N/A')}")
        print(f"Cause: {result_fail.get('cause', 'N/A')}")

    finally:
        if sm_arn:
            cleanup(client, sm_arn)


if __name__ == "__main__":
    main()