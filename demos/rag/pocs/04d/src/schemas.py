from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class PipelineScenario(BaseModel):
    scenario_id: str
    category: Literal["standard", "edge", "failure"]
    expected_success: bool
    request_payload: dict
    outcome_payload: dict


class ScenarioResult(BaseModel):
    scenario_id: str
    category: Literal["standard", "edge", "failure"]
    expected_success: bool
    actual_success: bool
    status: Literal["pass", "fail"]
    execution_time_ms: float
    error: str | None = None


class PipelineRunSummary(BaseModel):
    run_id: str = Field(default="poc-04d-sample-run")
    total: int
    passed: int
    failed: int
    results: list[ScenarioResult]
