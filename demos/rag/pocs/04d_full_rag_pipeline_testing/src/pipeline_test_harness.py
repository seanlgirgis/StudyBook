from __future__ import annotations

import sys
from pathlib import Path

from pydantic import ValidationError

SCHEMAS_DIR = Path(__file__).resolve().parents[2] / "04b_answer_contract_schemas" / "src"
if str(SCHEMAS_DIR) not in sys.path:
    sys.path.insert(0, str(SCHEMAS_DIR))

from schemas import AnswerAssemblyOutcome, AnswerAssemblyRequest, validate_outcome_against_request

from .schemas import PipelineRunSummary, PipelineScenario, ScenarioResult


def _evaluate_scenario(scenario: PipelineScenario) -> ScenarioResult:
    actual_success = False
    error: str | None = None

    try:
        request = AnswerAssemblyRequest.model_validate(scenario.request_payload)
        outcome = AnswerAssemblyOutcome.model_validate(scenario.outcome_payload)
        validate_outcome_against_request(request, outcome)
        actual_success = True
    except (ValidationError, ValueError) as exc:
        actual_success = False
        error = str(exc)

    status = "pass" if actual_success == scenario.expected_success else "fail"

    return ScenarioResult(
        scenario_id=scenario.scenario_id,
        category=scenario.category,
        expected_success=scenario.expected_success,
        actual_success=actual_success,
        status=status,
        error=error,
    )


def run_pipeline_harness(scenarios: list[PipelineScenario]) -> PipelineRunSummary:
    results = [_evaluate_scenario(item) for item in scenarios]
    passed = sum(1 for item in results if item.status == "pass")
    failed = len(results) - passed
    return PipelineRunSummary(
        total=len(results),
        passed=passed,
        failed=failed,
        results=results,
    )
