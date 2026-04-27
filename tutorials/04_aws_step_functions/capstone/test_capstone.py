# ============================================================
# Topic   : AWS Step Functions
# File    : capstone/test_capstone.py
# Covers  : pytest validation for capstone ASL, costs, and recommendations
# Prereqs : pip install pytest boto3
# Run     : pytest test_capstone.py -v
# ============================================================

"""
pytest tests for the Step Functions capstone.

These tests do not make real AWS calls.
They validate local ASL generation and helper logic.
"""

import sys
from pathlib import Path

import pytest


sys.path.insert(0, str(Path(__file__).parent))

from capstone import (  # noqa: E402
    build_catch_clause,
    build_pipeline_asl,
    build_retry_config,
    calculate_cost_report,
    calculate_standard_cost,
    recommend_workflow_type,
)


def test_pipeline_asl_has_required_states():
    """ASL must contain all required state names."""
    asl = build_pipeline_asl()
    states = set(asl["States"].keys())

    required = {
        "ValidateInput",
        "StartGlueJob",
        "WaitForGlue",
        "CheckJobStatus",
        "ValidateOutput",
        "NotifySuccess",
        "NotifyFailure",
    }

    assert required.issubset(states), f"Missing states: {required - states}"


def test_pipeline_asl_starts_at_validate_input():
    """Capstone workflow should start with input validation."""
    asl = build_pipeline_asl()

    assert asl["StartAt"] == "ValidateInput"


def test_notify_failure_is_fail_state():
    """NotifyFailure must terminate the workflow as a Fail state."""
    asl = build_pipeline_asl()

    assert asl["States"]["NotifyFailure"]["Type"] == "Fail"
    assert asl["States"]["NotifyFailure"]["Error"] == "PipelineValidationError"


def test_wait_for_glue_uses_wait_state():
    """The capstone must include a polling delay using a Wait state."""
    asl = build_pipeline_asl()
    wait_state = asl["States"]["WaitForGlue"]

    assert wait_state["Type"] == "Wait"
    assert wait_state["Seconds"] == 10
    assert wait_state["Next"] == "CheckJobStatus"


def test_validate_input_routes_valid_data_to_start_glue_job():
    """Valid input should route to StartGlueJob."""
    asl = build_pipeline_asl()
    validate_state = asl["States"]["ValidateInput"]

    assert validate_state["Type"] == "Choice"
    assert validate_state["Default"] == "NotifyFailure"
    assert validate_state["Choices"][0]["Next"] == "StartGlueJob"


def test_validate_output_routes_success_to_notify_success():
    """Valid output should route to NotifySuccess."""
    asl = build_pipeline_asl()
    validate_state = asl["States"]["ValidateOutput"]

    assert validate_state["Type"] == "Choice"
    assert validate_state["Default"] == "NotifyFailure"
    assert validate_state["Choices"][0]["Next"] == "NotifySuccess"


def test_retry_config_defaults():
    """Default retry config should use exponential backoff."""
    retry = build_retry_config()

    assert retry["IntervalSeconds"] == 2
    assert retry["MaxAttempts"] == 3
    assert retry["BackoffRate"] == 2.0
    assert "States.TaskFailed" in retry["ErrorEquals"]


def test_catch_clause_routes_to_expected_state():
    """Catch clause should route errors to the requested next state."""
    catch = build_catch_clause(
        error_types=["States.ALL"],
        next_state="NotifyFailure",
        result_path="$.error",
    )

    assert catch == {
        "ErrorEquals": ["States.ALL"],
        "Next": "NotifyFailure",
        "ResultPath": "$.error",
    }


def test_standard_cost_calculation_includes_free_tier():
    """10,000 transitions: 4,000 free, 6,000 billable = $0.15."""
    cost = calculate_standard_cost(n_state_transitions=10_000)

    assert abs(cost - 0.15) < 0.01


def test_standard_cost_for_capstone_24k_transitions():
    """24,000 transitions: 4,000 free, 20,000 billable = $0.50."""
    cost = calculate_standard_cost(n_state_transitions=24_000)

    assert abs(cost - 0.50) < 0.01


def test_recommend_standard_for_long_running_pipeline():
    """Long-running orchestration should use Standard."""
    rec = recommend_workflow_type(
        executions_per_day=100,
        requires_exactly_once=True,
        max_duration_s=600,
    )

    assert rec == "Standard"


def test_recommend_express_for_high_volume_short_workflow():
    """High-volume, at-least-once, short duration should use Express."""
    rec = recommend_workflow_type(
        executions_per_day=500_000,
        requires_exactly_once=False,
        max_duration_s=5,
    )

    assert rec == "Express"


def test_cost_report_prints_expected_summary(capsys):
    """Cost report should print monthly transitions and recommendation."""
    calculate_cost_report(n_daily_executions=100)

    captured = capsys.readouterr()
    output = captured.out

    assert "Monthly executions:        3,000" in output
    assert "Monthly transitions:       24,000" in output
    assert "Recommended workflow:      Standard" in output