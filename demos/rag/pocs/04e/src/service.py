from __future__ import annotations

import logging
import importlib.util
import sys
import time
import types
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

POCS_ROOT = Path(__file__).resolve().parents[2]
FOUR_D_SRC = POCS_ROOT / "04d" / "src"

logger = logging.getLogger(__name__)

if "poc04d" not in sys.modules:
    pkg = types.ModuleType("poc04d")
    pkg.__path__ = [str(FOUR_D_SRC)]  # type: ignore[attr-defined]
    sys.modules["poc04d"] = pkg


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module {module_name} from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_load_module("poc04d.schemas", FOUR_D_SRC / "schemas.py")
_mock_module = _load_module("poc04d.mock_evidence_sets", FOUR_D_SRC / "mock_evidence_sets.py")
_harness_module = _load_module("poc04d.pipeline_test_harness", FOUR_D_SRC / "pipeline_test_harness.py")

build_mock_scenarios = _mock_module.build_mock_scenarios
run_pipeline_harness = _harness_module.run_pipeline_harness


class ServiceQueryRequest(BaseModel):
    query: str = Field(min_length=1)
    context_documents: list[str] = Field(default_factory=list)
    scenario_ids: list[str] | None = None


class ServiceTiming(BaseModel):
    request_duration_ms: float
    scenario_count: int


class ServiceExecutionResult(BaseModel):
    run_id: str
    total: int
    passed: int
    failed: int
    scenario_results: list[dict[str, Any]]
    timing: ServiceTiming


class ServiceAnswerResult(BaseModel):
    query: str
    answer_text: str
    citations: list[dict[str, Any]]
    decision: str
    route_applied: str
    timing: ServiceTiming


def _select_scenarios(scenario_ids: list[str] | None) -> list[Any]:
    scenarios = build_mock_scenarios()
    if not scenario_ids:
        return scenarios

    scenario_id_set = set(scenario_ids)
    selected = [item for item in scenarios if item.scenario_id in scenario_id_set]
    missing = sorted(scenario_id_set - {item.scenario_id for item in selected})
    if missing:
        raise ValueError(f"Unknown scenario_id values: {', '.join(missing)}")
    return selected


def execute_pipeline(request: ServiceQueryRequest) -> ServiceExecutionResult:
    start = time.perf_counter()
    scenarios = _select_scenarios(request.scenario_ids)
    summary = run_pipeline_harness(scenarios)
    elapsed = (time.perf_counter() - start) * 1000.0
    logger.info("execute_pipeline query=%s scenarios=%d", request.query, len(scenarios))

    return ServiceExecutionResult(
        run_id=summary.run_id,
        total=summary.total,
        passed=summary.passed,
        failed=summary.failed,
        scenario_results=[item.model_dump(mode="json") for item in summary.results],
        timing=ServiceTiming(request_duration_ms=round(elapsed, 3), scenario_count=len(scenarios)),
    )


def retrieve_structured_answer(request: ServiceQueryRequest) -> ServiceAnswerResult:
    start = time.perf_counter()
    scenarios = _select_scenarios(request.scenario_ids)
    summary = run_pipeline_harness(scenarios)

    # pick the first successful deterministic outcome for answer-ready path
    selected_payload: dict[str, Any] | None = None
    for scenario in scenarios:
        if scenario.expected_success and scenario.outcome_payload.get("outcome_type") == "answer_ready":
            selected_payload = scenario.outcome_payload
            break

    if selected_payload is None:
        raise ValueError("No answer_ready scenario available for selected inputs.")

    claims = selected_payload["answer_payload"]["supported_claims"]
    citations = claims[0].get("citation_spans", []) if claims else []
    elapsed = (time.perf_counter() - start) * 1000.0

    logger.info("retrieve_structured_answer query=%s scenarios=%d", request.query, len(scenarios))

    return ServiceAnswerResult(
        query=request.query,
        answer_text=selected_payload["answer_payload"]["answer_text"],
        citations=citations,
        decision=selected_payload["outcome_type"],
        route_applied=selected_payload["route_applied"],
        timing=ServiceTiming(request_duration_ms=round(elapsed, 3), scenario_count=summary.total),
    )
