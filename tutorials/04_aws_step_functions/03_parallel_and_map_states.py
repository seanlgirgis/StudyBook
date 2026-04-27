# ============================================================
# Topic   : AWS Step Functions
# File    : 03_parallel_and_map_states.py
# Covers  : Parallel state, Map state, fan-out/fan-in, collection processing
# Prereqs : pip install boto3 | AWS credentials | IAM role for Step Functions
# Run     : python 03_parallel_and_map_states.py
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


def build_parallel_asl() -> dict[str, Any]:
    """
    Build an ASL with a Parallel state running 3 branches simultaneously.

    Branches:
      1. ExtractFromDB
      2. ExtractFromAPI
      3. ExtractFromFiles

    WHY Parallel:
      Step Functions runs all branches simultaneously and waits for ALL branches
      to complete before proceeding. This is ideal when a pipeline needs to
      extract from independent sources at the same time.

    Output:
      The Parallel state's output is an array containing each branch's final
      output in branch order.
    """
    return {
        "Comment": "StudyBook: Parallel state fan-out/fan-in demo",
        "StartAt": "ExtractAllSources",
        "States": {
            "ExtractAllSources": {
                "Type": "Parallel",
                "Comment": "Run DB, API, and file extraction branches at the same time",
                "Branches": [
                    {
                        "StartAt": "ExtractFromDB",
                        "States": {
                            "ExtractFromDB": {
                                "Type": "Pass",
                                "Result": {
                                    "source": "db",
                                    "rows": 1000,
                                    "status": "SUCCEEDED",
                                },
                                "End": True,
                            }
                        },
                    },
                    {
                        "StartAt": "ExtractFromAPI",
                        "States": {
                            "ExtractFromAPI": {
                                "Type": "Pass",
                                "Result": {
                                    "source": "api",
                                    "rows": 500,
                                    "status": "SUCCEEDED",
                                },
                                "End": True,
                            }
                        },
                    },
                    {
                        "StartAt": "ExtractFromFiles",
                        "States": {
                            "ExtractFromFiles": {
                                "Type": "Pass",
                                "Result": {
                                    "source": "files",
                                    "rows": 200,
                                    "status": "SUCCEEDED",
                                },
                                "End": True,
                            }
                        },
                    },
                ],
                "ResultPath": "$.extract_results",
                "Next": "MergeResults",
            },
            "MergeResults": {
                "Type": "Pass",
                "Comment": "In a real pipeline, this could combine branch outputs",
                "Parameters": {
                    "message": "All extraction branches completed",
                    "branch_outputs.$": "$.extract_results",
                },
                "Next": "PipelineSucceeded",
            },
            "PipelineSucceeded": {
                "Type": "Succeed",
            },
        },
    }


def build_map_asl() -> dict[str, Any]:
    """
    Build an ASL with a Map state processing each item in an array.

    Expected input:
      {
        "files": ["file1.csv", "file2.csv", "file3.csv"]
      }

    WHY Map:
      Map processes each element of an array with the same workflow logic.

    WHY MaxConcurrency:
      MaxConcurrency limits simultaneous iterations. This is important when
      each iteration calls Lambda, Glue, APIs, databases, or other resources
      that can be throttled.

    MaxConcurrency:
      0 = unlimited
      5 = at most 5 iterations running at once
    """
    return {
        "Comment": "StudyBook: Map state collection-processing demo",
        "StartAt": "ProcessFiles",
        "States": {
            "ProcessFiles": {
                "Type": "Map",
                "Comment": "Process each file in $.files using the same iterator logic",
                "ItemsPath": "$.files",
                "MaxConcurrency": 5,
                "Iterator": {
                    "StartAt": "ProcessFile",
                    "States": {
                        "ProcessFile": {
                            "Type": "Pass",
                            "Parameters": {
                                "file_name.$": "$",
                                "processed": True,
                                "rows_read": 100,
                            },
                            "End": True,
                        }
                    },
                },
                "ResultPath": "$.processed_files",
                "Next": "WriteResults",
            },
            "WriteResults": {
                "Type": "Pass",
                "Comment": "Simulates writing all processed file results",
                "Parameters": {
                    "message": "All files processed",
                    "processed_files.$": "$.processed_files",
                },
                "Next": "PipelineSucceeded",
            },
            "PipelineSucceeded": {
                "Type": "Succeed",
            },
        },
    }


def build_nested_parallel_map_example_asl() -> dict[str, Any]:
    """
    Demonstrate a common advanced pattern:
      Map over data sources, and inside each Map iteration run Parallel checks.

    This is printed for education only. It is not executed in main().
    """
    return {
        "Comment": "StudyBook: nested Map + Parallel pattern",
        "StartAt": "ForEachSource",
        "States": {
            "ForEachSource": {
                "Type": "Map",
                "ItemsPath": "$.sources",
                "MaxConcurrency": 3,
                "Iterator": {
                    "StartAt": "ExtractAndValidateInParallel",
                    "States": {
                        "ExtractAndValidateInParallel": {
                            "Type": "Parallel",
                            "Branches": [
                                {
                                    "StartAt": "ExtractSource",
                                    "States": {
                                        "ExtractSource": {
                                            "Type": "Pass",
                                            "Parameters": {
                                                "source.$": "$",
                                                "extract_status": "SUCCEEDED",
                                            },
                                            "End": True,
                                        }
                                    },
                                },
                                {
                                    "StartAt": "ValidateSourceConfig",
                                    "States": {
                                        "ValidateSourceConfig": {
                                            "Type": "Pass",
                                            "Parameters": {
                                                "source.$": "$",
                                                "config_valid": True,
                                            },
                                            "End": True,
                                        }
                                    },
                                },
                            ],
                            "End": True,
                        }
                    },
                },
                "ResultPath": "$.source_results",
                "Next": "Done",
            },
            "Done": {
                "Type": "Succeed",
            },
        },
    }


def compare_parallel_vs_map() -> None:
    """
    Print a formatted comparison.
    """
    print(
        """
Feature           | Parallel State               | Map State
------------------|------------------------------|------------------------------
Input             | Same input to all branches   | Array — one item per iteration
Branches          | Fixed at design time         | Dynamic — scales with array
Output            | Array of branch outputs      | Array of iteration outputs
MaxConcurrency    | N/A, all branches run        | Configurable, 0 = unlimited
Use case          | Fan-out to different sources | Process collection of items
Example           | Extract from 3 systems       | Process 1000 S3 files

Important:
  Parallel and Map can be nested.

Common data engineering pattern:
  Map over a list of data sources.
  Each Map iteration runs a Parallel state for extract + validate.
""".strip()
    )


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
    print("=== PARALLEL STATE ASL ===")
    parallel_asl = build_parallel_asl()
    print(json.dumps(parallel_asl, indent=2))

    print("\n=== MAP STATE ASL ===")
    map_asl = build_map_asl()
    print(json.dumps(map_asl, indent=2))

    print("\n=== NESTED MAP + PARALLEL EXAMPLE ASL ===")
    nested_asl = build_nested_parallel_map_example_asl()
    print(json.dumps(nested_asl, indent=2))

    print("\n=== PARALLEL vs MAP COMPARISON ===")
    compare_parallel_vs_map()

    calculate_demo_cost(n_state_transitions=8)

    if not ROLE_ARN:
        print("\nSTEP_FUNCTIONS_ROLE_ARN not set — showing ASL definitions only")
        print("Skipping state machine creation.")
        return

    client = get_client()
    sm_arn: str | None = None

    try:
        print("\n=== CREATE RUNNABLE MAP STATE MACHINE ===")
        sm_arn = create_state_machine(
            client=client,
            name=f"studybook-sf-map-{uuid.uuid4().hex[:8]}",
            asl=map_asl,
            role_arn=ROLE_ARN,
        )

        print("\n=== START MAP EXECUTION ===")
        exec_arn = start_execution(
            client=client,
            state_machine_arn=sm_arn,
            input_dict={
                "batch_id": "B003",
                "files": ["file1.csv", "file2.csv", "file3.csv"],
            },
        )

        print("\n=== WAIT FOR COMPLETION ===")
        result = wait_for_completion(client=client, execution_arn=exec_arn)

        print(f"\nMap execution: {result['status']}")
        output = result.get("output", "N/A")
        print(f"Output: {output[:500] if isinstance(output, str) else output}")

    finally:
        if sm_arn:
            cleanup(client, sm_arn)


if __name__ == "__main__":
    main()