# ============================================================
# Topic   : AWS Step Functions
# File    : 01_state_machine_basics.py
# Covers  : basic Standard workflow creation, execution, polling, history, cleanup
# Prereqs : pip install boto3 | AWS credentials | IAM role for Step Functions
# Run     : python 01_state_machine_basics.py
# ============================================================

"""
Environment variables:
  AWS_REGION              — default "us-east-1"
  AWS_PROFILE             — default "study"
  STEP_FUNCTIONS_ROLE_ARN — REQUIRED to create real Step Functions resources

If STEP_FUNCTIONS_ROLE_ARN is not set:
  - prints: "STEP_FUNCTIONS_ROLE_ARN not set — showing ASL definitions only"
  - shows generated ASL JSON
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


STATE_MACHINE_NAME = f"studybook-sf-basics-{uuid.uuid4().hex[:8]}"

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "study")
ROLE_ARN = os.getenv("STEP_FUNCTIONS_ROLE_ARN")

STANDARD_TRANSITION_PRICE_PER_1000 = 0.025


def get_client():
    return boto3.Session(
        profile_name=AWS_PROFILE,
        region_name=AWS_REGION,
    ).client("stepfunctions")


def build_simple_asl() -> dict[str, Any]:
    """
    Build a simple ASL definition.

    States:
      ProcessData -> Validate -> Done

    WHY Pass state:
      A Pass state is a no-op state. It is useful for scaffolding a pipeline
      before replacing states with real Task states.

    WHY Succeed state:
      A Succeed state explicitly marks successful completion.
    """
    return {
        "Comment": "StudyBook: basic state machine",
        "StartAt": "ProcessData",
        "States": {
            "ProcessData": {
                "Type": "Pass",
                "Comment": "Pass state: input flows through unchanged",
                "Next": "Validate",
            },
            "Validate": {
                "Type": "Pass",
                "Comment": "Adds validation metadata to the execution input",
                "Result": {"validated": True},
                "ResultPath": "$.validation",
                "Next": "Done",
            },
            "Done": {
                "Type": "Succeed",
                "Comment": "Terminal success state",
            },
        },
    }


def calculate_demo_cost(n_state_transitions: int) -> float:
    """
    Calculate Standard workflow cost.

    Step Functions Standard:
      $0.025 per 1,000 state transitions.

    This small demo usually stays far below meaningful cost.
    """
    cost = (n_state_transitions / 1000) * STANDARD_TRANSITION_PRICE_PER_1000
    print("\n=== COST ESTIMATE ===")
    print(f"Estimated transitions: {n_state_transitions}")
    print("Standard workflow price: $0.025 per 1,000 state transitions")
    print(f"Estimated cost: ${cost:.6f}")
    return cost


def create_state_machine(
    client,
    name: str,
    asl: dict[str, Any],
    role_arn: str,
) -> str:
    """
    Create a Standard workflow state machine.

    Returns:
      State machine ARN.
    """
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
    """
    Start a Step Functions execution.

    input must be sent as a JSON string.
    """
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
    """
    Poll describe_execution until terminal status.

    Terminal statuses:
      SUCCEEDED, FAILED, TIMED_OUT, ABORTED
    """
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


def _extract_relevant_event_data(event: dict[str, Any]) -> dict[str, Any]:
    """
    Return the useful detail field from a Step Functions history event.
    """
    ignored_keys = {"timestamp", "type", "id", "previousEventId"}

    for key, value in event.items():
        if key not in ignored_keys:
            return {key: value}

    return {}


def get_execution_history(client, execution_arn: str) -> list[dict[str, Any]]:
    """
    Read full execution history.

    WHY history:
      Step Functions logs every state transition. This is the audit trail
      a data engineering team would use to trace exactly what happened in
      a failed pipeline run.
    """
    events: list[dict[str, Any]] = []
    next_token: str | None = None

    while True:
        kwargs = {
            "executionArn": execution_arn,
            "reverseOrder": False,
        }

        if next_token:
            kwargs["nextToken"] = next_token

        response = client.get_execution_history(**kwargs)
        events.extend(response["events"])

        next_token = response.get("nextToken")
        if not next_token:
            break

    for event in events:
        timestamp = event["timestamp"]
        event_type = event["type"]
        event_id = event["id"]
        details = _extract_relevant_event_data(event)

        print(f"[{event_id}] {timestamp} | {event_type}")

        if details:
            print(json.dumps(details, indent=2, default=str))

    return events


def delete_state_machine(client, arn: str) -> None:
    """
    Delete a state machine.

    Idempotent cleanup:
      StateMachineDoesNotExist is treated as success.
    """
    try:
        client.delete_state_machine(stateMachineArn=arn)
        print(f"Deleted state machine: {arn}")
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code", "")

        if error_code == "StateMachineDoesNotExist":
            return

        raise


def cleanup(client, state_machine_arn: str) -> None:
    """
    Delete resources created by this file.
    """
    delete_state_machine(client, state_machine_arn)
    print("✅ Cleanup complete. No ongoing charges.")


def main() -> None:
    asl = build_simple_asl()

    if not ROLE_ARN:
        print("STEP_FUNCTIONS_ROLE_ARN not set — showing ASL definitions only")
        print(json.dumps(asl, indent=2))
        calculate_demo_cost(n_state_transitions=3)
        return

    client = get_client()
    sm_arn: str | None = None

    try:
        print("\n=== CREATE STATE MACHINE ===")
        sm_arn = create_state_machine(
            client=client,
            name=STATE_MACHINE_NAME,
            asl=asl,
            role_arn=ROLE_ARN,
        )

        print("\n=== START EXECUTION ===")
        exec_arn = start_execution(
            client=client,
            state_machine_arn=sm_arn,
            input_dict={
                "sensor_id": "s001",
                "value": 72.5,
                "source": "studybook-demo",
            },
        )

        print("\n=== WAIT FOR COMPLETION ===")
        result = wait_for_completion(client=client, execution_arn=exec_arn)

        print(f"Final status: {result['status']}")
        print(f"Output: {result.get('output', 'N/A')}")

        print("\n=== EXECUTION HISTORY ===")
        history = get_execution_history(client=client, execution_arn=exec_arn)
        print(f"Total events: {len(history)}")

        calculate_demo_cost(n_state_transitions=len(history))

    finally:
        if sm_arn:
            cleanup(client, sm_arn)


if __name__ == "__main__":
    main()