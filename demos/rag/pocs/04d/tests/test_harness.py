import time

from src.mock_evidence_sets import build_mock_scenarios, build_performance_batch
from src.pipeline_test_harness import run_pipeline_harness


def test_harness_passes_expected_matrix():
    scenarios = build_mock_scenarios()
    summary = run_pipeline_harness(scenarios)
    assert summary.total == len(scenarios)
    assert summary.failed == 0


def test_contains_standard_edge_failure():
    cats = {s.category for s in build_mock_scenarios()}
    assert {"standard", "edge", "failure"}.issubset(cats)


def test_contains_new_failure_scenarios():
    scenario_ids = {s.scenario_id for s in build_mock_scenarios()}
    assert "failure-insufficient-evidence" in scenario_ids
    assert "failure-escalation-required" in scenario_ids


def test_results_include_execution_timing():
    summary = run_pipeline_harness(build_mock_scenarios())
    assert all(result.execution_time_ms >= 0 for result in summary.results)


def test_performance_batch_lightweight():
    scenarios = build_performance_batch(batch_size=60)
    start = time.perf_counter()
    summary = run_pipeline_harness(scenarios)
    elapsed_s = time.perf_counter() - start
    assert summary.total == 60
    assert summary.failed == 0
    assert elapsed_s < 2.0
