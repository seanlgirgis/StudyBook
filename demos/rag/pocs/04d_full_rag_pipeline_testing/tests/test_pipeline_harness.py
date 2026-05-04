from __future__ import annotations

from src.mock_evidence_sets import build_mock_scenarios
from src.pipeline_test_harness import run_pipeline_harness


def test_mock_scenarios_cover_all_categories():
    scenarios = build_mock_scenarios()
    categories = {item.category for item in scenarios}
    assert "standard" in categories
    assert "edge" in categories
    assert "failure" in categories


def test_harness_all_scenarios_pass_against_expected_outcome():
    scenarios = build_mock_scenarios()
    summary = run_pipeline_harness(scenarios)

    assert summary.total == len(scenarios)
    assert summary.failed == 0
    assert summary.passed == summary.total


def test_negative_scenario_is_failure_but_expected():
    scenarios = build_mock_scenarios()
    summary = run_pipeline_harness(scenarios)

    negative = next(item for item in summary.results if item.scenario_id == "negative-bad-citation")
    assert negative.expected_success is False
    assert negative.actual_success is False
    assert negative.status == "pass"
    assert negative.error is not None
