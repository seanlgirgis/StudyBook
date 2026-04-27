# ============================================================
# Topic   : AWS Step Functions
# File    : 05_express_workflows_and_cost.py
# Covers  : Standard vs Express workflows, cost calculator, workflow selection rules
# Prereqs : pip install boto3 | AWS credentials | IAM role for Step Functions
# Run     : python 05_express_workflows_and_cost.py
# ============================================================

"""
Environment variables:
  AWS_REGION              — default "us-east-1"
  AWS_PROFILE             — default "study"
  STEP_FUNCTIONS_ROLE_ARN — REQUIRED to create real Step Functions resources
  SNS_TOPIC_ARN           — optional, not used in this file

If STEP_FUNCTIONS_ROLE_ARN is not set:
  - runs cost calculations
  - prints workflow recommendations
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
STANDARD_FREE_TRANSITIONS_PER_MONTH = 4_000

EXPRESS_REQUEST_PRICE_PER_MILLION = 1.00
EXPRESS_FREE_REQUESTS_PER_MONTH = 1_000_000
EXPRESS_DURATION_PRICE_PER_GB_SECOND = 0.00001


def get_client():
    return boto3.Session(
        profile_name=AWS_PROFILE,
        region_name=AWS_REGION,
    ).client("stepfunctions")


def calculate_standard_cost(n_state_transitions: int) -> float:
    """
    Standard workflow pricing:
      $0.025 per 1,000 state transitions.
      First 4,000 transitions per month are free.

    Returns:
      Monthly cost in USD.
    """
    billable_transitions = max(
        0,
        n_state_transitions - STANDARD_FREE_TRANSITIONS_PER_MONTH,
    )

    cost = (
        billable_transitions / 1000
    ) * STANDARD_TRANSITION_PRICE_PER_1000

    print("\nStandard Workflow Cost")
    print("----------------------")
    print(f"Total transitions/month:    {n_state_transitions:,}")
    print(f"Free transitions/month:     {STANDARD_FREE_TRANSITIONS_PER_MONTH:,}")
    print(f"Billable transitions/month: {billable_transitions:,}")
    print(f"Rate:                       $0.025 per 1,000 transitions")
    print(f"Estimated monthly cost:     ${cost:.4f}")

    return cost


def calculate_express_cost(
    n_executions: int,
    avg_duration_ms: int,
    avg_memory_gb: float = 0.064,
) -> float:
    """
    Express workflow pricing, simplified for us-east-1:

      Requests:
        $1.00 per 1,000,000 executions
        first 1,000,000 requests/month are free

      Duration:
        $0.00001 per GB-second

    Formula:
      duration_gb_seconds =
          (avg_duration_ms / 1000) * avg_memory_gb * n_executions

    Returns:
      Monthly cost in USD.
    """
    billable_requests = max(
        0,
        n_executions - EXPRESS_FREE_REQUESTS_PER_MONTH,
    )

    request_cost = (
        billable_requests / 1_000_000
    ) * EXPRESS_REQUEST_PRICE_PER_MILLION

    duration_gb_seconds = (
        avg_duration_ms / 1000
    ) * avg_memory_gb * n_executions

    duration_cost = duration_gb_seconds * EXPRESS_DURATION_PRICE_PER_GB_SECOND
    total_cost = request_cost + duration_cost

    print("\nExpress Workflow Cost")
    print("---------------------")
    print(f"Executions/month:           {n_executions:,}")
    print(f"Free requests/month:        {EXPRESS_FREE_REQUESTS_PER_MONTH:,}")
    print(f"Billable requests/month:    {billable_requests:,}")
    print(f"Average duration:           {avg_duration_ms:,} ms")
    print(f"Average memory:             {avg_memory_gb:.3f} GB")
    print(f"Duration GB-seconds:        {duration_gb_seconds:,.4f}")
    print(f"Request cost:               ${request_cost:.4f}")
    print(f"Duration cost:              ${duration_cost:.4f}")
    print(f"Estimated monthly cost:     ${total_cost:.4f}")

    return total_cost


def recommend_workflow_type(
    executions_per_day: int,
    requires_exactly_once: bool,
    max_duration_s: int,
) -> str:
    """
    Decision rules:
      max_duration_s > 300          -> Standard
      requires_exactly_once is True -> Standard
      executions_per_day > 100,000  -> Express
      otherwise                     -> Standard

    Returns:
      "Standard" or "Express".
    """
    print("\nWorkflow Recommendation")
    print("-----------------------")
    print(f"Executions/day:        {executions_per_day:,}")
    print(f"Requires exactly once: {requires_exactly_once}")
    print(f"Max duration seconds:  {max_duration_s:,}")

    if max_duration_s > 300:
        print("Recommendation: Standard")
        print("Reason: Express workflows have a 5-minute maximum duration.")
        return "Standard"

    if requires_exactly_once:
        print("Recommendation: Standard")
        print("Reason: Standard supports exactly-once execution semantics.")
        return "Standard"

    if executions_per_day > 100_000:
        print("Recommendation: Express")
        print("Reason: High-volume short workflows are usually cheaper on Express.")
        return "Express"

    print("Recommendation: Standard")
    print("Reason: Lower-volume workflows benefit from simpler execution history.")
    return "Standard"


def compare_all_scenarios() -> None:
    """
    Compare real-world Step Functions scenarios.

    Scenario 1:
      Daily ETL pipeline
      1 execution/day, 50 transitions, 10 minutes, exactly-once required

    Scenario 2:
      IoT event processing
      1,000,000 executions/day, 5 transitions each, 2 seconds, at-least-once OK

    Scenario 3:
      Microservice orchestration
      500,000 executions/day, 3 transitions, 0.5 seconds, at-least-once OK
    """
    scenarios = [
        {
            "name": "Daily ETL pipeline",
            "executions_per_day": 1,
            "transitions_per_execution": 50,
            "duration_ms": 10 * 60 * 1000,
            "requires_exactly_once": True,
            "max_duration_s": 10 * 60,
            "memory_gb": 0.064,
        },
        {
            "name": "IoT event processing",
            "executions_per_day": 1_000_000,
            "transitions_per_execution": 5,
            "duration_ms": 2_000,
            "requires_exactly_once": False,
            "max_duration_s": 2,
            "memory_gb": 0.064,
        },
        {
            "name": "Microservice orchestration",
            "executions_per_day": 500_000,
            "transitions_per_execution": 3,
            "duration_ms": 500,
            "requires_exactly_once": False,
            "max_duration_s": 1,
            "memory_gb": 0.064,
        },
    ]

    for scenario in scenarios:
        executions_per_month = scenario["executions_per_day"] * 30
        transitions_per_month = (
            executions_per_month * scenario["transitions_per_execution"]
        )

        print("\n" + "=" * 70)
        print(f"Scenario: {scenario['name']}")
        print("=" * 70)

        standard_cost = calculate_standard_cost(transitions_per_month)
        express_cost = calculate_express_cost(
            n_executions=executions_per_month,
            avg_duration_ms=scenario["duration_ms"],
            avg_memory_gb=scenario["memory_gb"],
        )

        recommendation = recommend_workflow_type(
            executions_per_day=scenario["executions_per_day"],
            requires_exactly_once=scenario["requires_exactly_once"],
            max_duration_s=scenario["max_duration_s"],
        )

        print("\nScenario Summary")
        print("----------------")
        print(f"Standard estimate: ${standard_cost:.4f}/month")
        print(f"Express estimate:  ${express_cost:.4f}/month")
        print(f"Recommended:       {recommendation}")


def demonstrate_execution_difference() -> None:
    """
    Print key behavioral differences.
    """
    print(
        """
Feature                | Standard Workflow        | Express Workflow
-----------------------|--------------------------|------------------------------
Max duration           | 1 year                   | 5 minutes
Execution semantics    | Exactly-once             | At-least-once
Execution history      | Yes, 90 days             | CloudWatch Logs only
Max state transitions  | Unlimited                | Unlimited
Pricing model          | Per state transition     | Per execution + duration
Best use case          | ETL, approvals, audits   | IoT, events, high-volume APIs

WHY exactly-once matters for ETL:
  If a Glue job or load step runs twice for the same input, the data lake may
  contain duplicate records. Standard workflows reduce that risk.

WHY Express fits IoT:
  Millions of small sensor events can be processed cheaply. For telemetry,
  occasional duplicate handling is usually managed downstream with idempotency
  keys or timestamps.

Rule of thumb:
  Use Standard when correctness, audit history, or long duration matters.
  Use Express when volume is very high and each execution is short.
""".strip()
    )


def build_express_demo_asl() -> dict[str, Any]:
    """
    Build a minimal ASL that can run as an Express workflow.
    """
    return {
        "Comment": "StudyBook: minimal Express workflow demo",
        "StartAt": "Process",
        "States": {
            "Process": {
                "Type": "Pass",
                "Result": {
                    "processed": True,
                    "workflow_type": "EXPRESS",
                },
                "ResultPath": "$.result",
                "End": True,
            }
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
    print(f"Type: {workflow_type}")
    print(f"State machine ARN: {state_machine_arn}")

    if workflow_type == "STANDARD":
        print("⚠️  COST: Standard workflow charges $0.025/1000 state transitions.")
    else:
        print(
            "⚠️  COST: Express workflow charges per request and GB-second duration."
        )

    return state_machine_arn


def start_execution(
    client,
    state_machine_arn: str,
    input_dict: dict[str, Any],
    workflow_type: str = "STANDARD",
    execution_name: str | None = None,
) -> str:
    """
    Start Standard or Express execution.

    Standard supports named executions.
    Express also supports start_execution, but execution history is not available
    the same way Standard execution history is.
    """
    kwargs: dict[str, Any] = {
        "stateMachineArn": state_machine_arn,
        "input": json.dumps(input_dict),
    }

    if execution_name is None:
        execution_name = f"exec-{uuid.uuid4().hex[:8]}"

    kwargs["name"] = execution_name

    response = client.start_execution(**kwargs)

    execution_arn = response["executionArn"]
    print(f"Started {workflow_type} execution: {execution_name}")
    print(f"Execution ARN: {execution_arn}")

    return execution_arn


def wait_for_completion(
    client,
    execution_arn: str,
    poll_interval: int = 2,
    timeout: int = 30,
) -> dict[str, Any]:
    """
    Poll describe_execution for Standard workflow completion.

    Note:
      Express workflow execution details are not available through
      describe_execution in the same way Standard workflows are. Express
      observability primarily uses CloudWatch Logs.
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


def main() -> None:
    print("=== COST CALCULATOR ===")
    standard_cost = calculate_standard_cost(n_state_transitions=10_000)
    express_cost = calculate_express_cost(
        n_executions=100_000,
        avg_duration_ms=500,
    )

    print(f"\nStandard (10k transitions/month): ${standard_cost:.4f}")
    print(f"Express  (100k executions/month): ${express_cost:.4f}")

    print("\n=== WORKFLOW RECOMMENDATION ===")
    recommend_workflow_type(
        executions_per_day=1,
        requires_exactly_once=True,
        max_duration_s=600,
    )
    recommend_workflow_type(
        executions_per_day=500_000,
        requires_exactly_once=False,
        max_duration_s=5,
    )

    print("\n=== SCENARIO COMPARISON ===")
    compare_all_scenarios()

    print("\n=== BEHAVIORAL DIFFERENCES ===")
    demonstrate_execution_difference()

    express_asl = build_express_demo_asl()

    print("\n=== EXPRESS DEMO ASL ===")
    print(json.dumps(express_asl, indent=2))

    if not ROLE_ARN:
        print("\nSTEP_FUNCTIONS_ROLE_ARN not set — ASL display only")
        print("Skipping state machine creation.")
        return

    client = get_client()
    sm_arn: str | None = None

    try:
        print("\n=== CREATE EXPRESS STATE MACHINE ===")
        sm_arn = create_state_machine(
            client=client,
            name=f"studybook-sf-express-{uuid.uuid4().hex[:8]}",
            asl=express_asl,
            role_arn=ROLE_ARN,
            workflow_type="EXPRESS",
        )

        print("\n=== START EXPRESS EXECUTION ===")
        exec_arn = start_execution(
            client=client,
            state_machine_arn=sm_arn,
            input_dict={
                "event": "iot_reading",
                "sensor_id": "s001",
                "value": 72.5,
            },
            workflow_type="EXPRESS",
        )

        print("\nExpress execution started.")
        print("For Express workflows, inspect CloudWatch Logs for execution details.")
        print(f"Execution ARN: {exec_arn}")

    finally:
        if sm_arn:
            cleanup(client, sm_arn)


if __name__ == "__main__":
    main()