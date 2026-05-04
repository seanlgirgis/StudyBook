from __future__ import annotations

import sys
import time
from pathlib import Path

from pydantic import ValidationError

SCHEMAS_DIR = Path(__file__).resolve().parents[2] / "04b_answer_contract_schemas" / "src"
if str(SCHEMAS_DIR) not in sys.path:
    sys.path.insert(0, str(SCHEMAS_DIR))

from schemas import AnswerAssemblyOutcome, AnswerAssemblyRequest, validate_outcome_against_request

from .schemas import PipelineRunSummary, PipelineScenario, ScenarioResult


def run_pipeline_harness(scenarios: list[PipelineScenario]) -> PipelineRunSummary:
    results: list[ScenarioResult] = []
    for scenario in scenarios:
        start = time.perf_counter()
        actual_success = False
        err = None
        try:
            req = AnswerAssemblyRequest.model_validate(scenario.request_payload)
            out = AnswerAssemblyOutcome.model_validate(scenario.outcome_payload)
            validate_outcome_against_request(req, out)
            actual_success = True
        except (ValidationError, ValueError) as exc:
            err = str(exc)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        status = "pass" if actual_success == scenario.expected_success else "fail"
        results.append(
            ScenarioResult(
                scenario_id=scenario.scenario_id,
                category=scenario.category,
                expected_success=scenario.expected_success,
                actual_success=actual_success,
                status=status,
                execution_time_ms=round(elapsed_ms, 3),
                error=err,
            )
        )

    passed = sum(1 for r in results if r.status == "pass")
    return PipelineRunSummary(total=len(results), passed=passed, failed=len(results)-passed, results=results)
