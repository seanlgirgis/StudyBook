# ============================================================
# Topic   : AWS Step Functions
# File    : 02_task_states_and_lambda.py
# Covers  : Task states, Lambda integration patterns, retry config, safe simulated execution
# Prereqs : pip install boto3 | AWS credentials | IAM role for Step Functions
# Run     : python 02_task_states_and_lambda.py
# ============================================================

"""
Environment variables:
  AWS_REGION              — default "us-east-1"
  AWS_PROFILE             — default "study"
  STEP_FUNCTIONS_ROLE_ARN — REQUIRED to create real Step Functions resources
  SNS_TOPIC_ARN           — optional, not used in this file

If STEP_FUNCTIONS_ROLE_ARN is not set:
  - prints ASL definitions only
  - does not create AWS resources
  - does not crash

Important:
  This file demonstrates Lambda Task state ASL using mock Lambda ARNs.
  It creates and executes only a SAFE Pass-state simulation when ROLE_ARN is set.
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


def build_lambda_task_state(
    lambda_arn: str,
    timeout_s: int = 300,
    heartbeat_s: int = 60,
) -> dict[str, Any]:
    """
    Build an ASL Task state dict for Lambda integration.

    Resource:
      arn:aws:states:::lambda:invoke

    WHY Task state:
      A Task state calls external compute or AWS services. For data engineers,
      common targets include Lambda, Glue, EMR, ECS, Batch, SNS, and SQS.

    WHY timeout:
      Prevents a workflow from waiting forever.

    WHY heartbeat:
      Detects stalled long-running work.

    NOTE:
      Lambda itself has a maximum runtime of 15 minutes.
    """
    return {
        "Type": "Task",
        "Resource": "arn:aws:states:::lambda:invoke",
        "Parameters": {
            "FunctionName": lambda_arn,
            "Payload.$": "$",
        },
        "TimeoutSeconds": timeout_s,
        "HeartbeatSeconds": heartbeat_s,
        "Retry": [
            {
                "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                ],
                "IntervalSeconds": 2,
                "MaxAttempts": 3,
                "BackoffRate": 2.0,
            }
        ],
    }


def build_lambda_wait_for_task_token_state(
    lambda_arn: str,
    timeout_s: int = 900,
    heartbeat_s: int = 60,
) -> dict[str, Any]:
    """
    Build a Lambda callback-pattern Task state.

    Resource:
      arn:aws:states:::lambda:invoke.waitForTaskToken

    WHY waitForTaskToken:
      Step Functions gives Lambda a task token. Lambda or another worker can do
      async work and later call SendTaskSuccess or SendTaskFailure.

    Data engineering example:
      Start an external vendor ingestion job, wait for the vendor callback,
      then continue the pipeline.
    """
    return {
        "Type": "Task",
        "Resource": "arn:aws:states:::lambda:invoke.waitForTaskToken",
        "Parameters": {
            "FunctionName": lambda_arn,
            "Payload": {
                "taskToken.$": "$$.Task.Token",
                "input.$": "$",
            },
        },
        "TimeoutSeconds": timeout_s,
        "HeartbeatSeconds": heartbeat_s,
    }


def build_pipeline_asl(lambda_arns: list[str]) -> dict[str, Any]:
    """
    Build a 3-step data pipeline ASL:

      ExtractData -> TransformData -> LoadData -> PipelineSucceeded

    Each Task state:
      - calls a Lambda function
      - passes workflow input as Lambda payload
      - retries transient Lambda errors

    WHY retry on Lambda.ServiceException:
      Lambda can occasionally hit transient service errors or SDK/network issues.
      Automatic retry with exponential backoff handles many temporary failures.
    """
    if len(lambda_arns) != 3:
        raise ValueError("lambda_arns must contain exactly 3 Lambda ARNs")

    extract_state = build_lambda_task_state(lambda_arns[0])
    transform_state = build_lambda_task_state(lambda_arns[1])
    load_state = build_lambda_task_state(lambda_arns[2])

    extract_state["ResultSelector"] = {
        "processed_rows.$": "$.Payload.processed_rows",
        "source.$": "$.Payload.source",
    }
    extract_state["ResultPath"] = "$.extract_result"
    extract_state["Next"] = "TransformData"

    transform_state["ResultSelector"] = {
        "transformed_rows.$": "$.Payload.transformed_rows",
        "quality_score.$": "$.Payload.quality_score",
    }
    transform_state["ResultPath"] = "$.transform_result"
    transform_state["Next"] = "LoadData"

    load_state["ResultSelector"] = {
        "loaded_rows.$": "$.Payload.loaded_rows",
        "target.$": "$.Payload.target",
    }
    load_state["ResultPath"] = "$.load_result"
    load_state["Next"] = "PipelineSucceeded"

    return {
        "Comment": "StudyBook: Lambda Task state ETL pipeline",
        "StartAt": "ExtractData",
        "States": {
            "ExtractData": extract_state,
            "TransformData": transform_state,
            "LoadData": load_state,
            "PipelineSucceeded": {
                "Type": "Succeed",
                "Comment": "ETL pipeline completed successfully",
            },
        },
    }


def build_safe_pass_pipeline_asl() -> dict[str, Any]:
    """
    Build a runnable simulation using only Pass states.

    WHY:
      Mock Lambda ARNs cannot be invoked. This ASL lets students create and
      execute a real state machine without needing Lambda functions yet.
    """
    return {
        "Comment": "StudyBook: safe Pass-state simulation of Lambda pipeline",
        "StartAt": "ExtractData",
        "States": {
            "ExtractData": {
                "Type": "Pass",
                "Result": {
                    "source": "mock-lambda-extract",
                    "processed_rows": 1000,
                },
                "ResultPath": "$.extract_result",
                "Next": "TransformData",
            },
            "TransformData": {
                "Type": "Pass",
                "Result": {
                    "transformed_rows": 995,
                    "quality_score": 0.99,
                },
                "ResultPath": "$.transform_result",
                "Next": "LoadData",
            },
            "LoadData": {
                "Type": "Pass",
                "Result": {
                    "loaded_rows": 995,
                    "target": "mock-data-warehouse",
                },
                "ResultPath": "$.load_result",
                "Next": "Done",
            },
            "Done": {
                "Type": "Succeed",
            },
        },
    }


def demonstrate_sync_patterns() -> None:
    """
    Print comparison of Lambda integration patterns.
    """
    print(
        """
Pattern                    | Resource suffix              | When to use
---------------------------|------------------------------|----------------------------
Synchronous request/resp   | :invoke                      | Fast Lambda work
Callback with task token   | :invoke.waitForTaskToken     | Long-running async work
Fire and forget            | :invoke + InvocationType     | Background task, no result needed

ResultSelector example:
{
  "ResultSelector": {
    "processed_rows.$": "$.Payload.processed_rows"
  },
  "ResultPath": "$.extract_result"
}

WHY ResultSelector:
  Lambda responses include metadata and a Payload wrapper. ResultSelector lets
  the workflow keep only the fields the pipeline needs.

WHY ResultPath:
  ResultPath controls where task output is stored in the workflow JSON.
  Without careful ResultPath design, each task can overwrite previous input.
""".strip()
    )


def demonstrate_task_token_pattern(lambda_arn: str) -> None:
    """
    Print a task-token example state.
    """
    print("\n=== CALLBACK TASK TOKEN PATTERN EXAMPLE ===")
    print(json.dumps(build_lambda_wait_for_task_token_state(lambda_arn), indent=2))


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


def main() -> None:
    mock_arns = [
        f"arn:aws:lambda:{AWS_REGION}:123456789012:function:mock-extract",
        f"arn:aws:lambda:{AWS_REGION}:123456789012:function:mock-transform",
        f"arn:aws:lambda:{AWS_REGION}:123456789012:function:mock-load",
    ]

    lambda_asl = build_pipeline_asl(mock_arns)

    print("=== 3-STEP LAMBDA PIPELINE ASL ===")
    print(json.dumps(lambda_asl, indent=2))

    print("\n=== SYNC PATTERNS ===")
    demonstrate_sync_patterns()

    demonstrate_task_token_pattern(mock_arns[0])

    calculate_demo_cost(n_state_transitions=4)

    if not ROLE_ARN:
        print("\nSTEP_FUNCTIONS_ROLE_ARN not set — showing ASL definitions only")
        print("Skipping state machine creation.")
        return

    client = get_client()
    sm_arn: str | None = None

    try:
        safe_asl = build_safe_pass_pipeline_asl()

        print("\n=== SAFE RUNNABLE PASS-STATE PIPELINE ASL ===")
        print(json.dumps(safe_asl, indent=2))

        print("\n=== CREATE SAFE STATE MACHINE ===")
        sm_arn = create_state_machine(
            client=client,
            name=f"studybook-sf-pipeline-{uuid.uuid4().hex[:8]}",
            asl=safe_asl,
            role_arn=ROLE_ARN,
        )

        print("\n=== START SAFE EXECUTION ===")
        exec_arn = start_execution(
            client=client,
            state_machine_arn=sm_arn,
            input_dict={
                "batch_id": "B001",
                "source_system": "studybook",
                "requested_by": "data-engineering-demo",
            },
        )

        print("\n=== WAIT FOR COMPLETION ===")
        result = wait_for_completion(client=client, execution_arn=exec_arn)

        print(f"\nPipeline execution: {result['status']}")
        print(f"Output: {result.get('output', 'N/A')}")

    finally:
        if sm_arn:
            cleanup(client, sm_arn)


if __name__ == "__main__":
    main()