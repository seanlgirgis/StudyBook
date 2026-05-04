from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

POC_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = POC_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from run_evaluation import run_retrieval_evaluation  # noqa: E402
from schemas import EvaluationRunResult  # noqa: E402


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _fixture_payload() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "cases": [
            {
                "case_id": "case_001",
                "query": "sample query",
                "normalized_query": "sample query",
                "expected_chunk_id": "target_chunk",
                "expected_decision_label": "strong_match",
                "expected_recommended_route": "answer_candidate_path",
            }
        ],
    }


def _retrieval_payload() -> dict[str, object]:
    return {
        "queries": [
            {
                "query": "sample query",
                "normalized_query": "sample query",
                "results": [{"rank": 1, "chunk_id": "target_chunk"}],
            }
        ]
    }


def _decision_payload() -> dict[str, object]:
    return {
        "query_decisions": [
            {
                "query": "sample query",
                "normalized_query": "sample query",
                "decision_label": "strong_match",
                "recommended_route": "answer_candidate_path",
            }
        ]
    }


def test_orchestration_returns_typed_result_for_valid_temp_files(tmp_path: Path) -> None:
    fixture_path = tmp_path / "fixture.json"
    retrieval_path = tmp_path / "03f.json"
    decision_path = tmp_path / "03g.json"
    _write_json(fixture_path, _fixture_payload())
    _write_json(retrieval_path, _retrieval_payload())
    _write_json(decision_path, _decision_payload())

    result = run_retrieval_evaluation(fixture_path, retrieval_path, decision_path)
    assert isinstance(result, EvaluationRunResult)


def test_returned_result_has_expected_case_count_and_summary(tmp_path: Path) -> None:
    fixture_path = tmp_path / "fixture.json"
    retrieval_path = tmp_path / "03f.json"
    decision_path = tmp_path / "03g.json"
    _write_json(fixture_path, _fixture_payload())
    _write_json(retrieval_path, _retrieval_payload())
    _write_json(decision_path, _decision_payload())

    result = run_retrieval_evaluation(fixture_path, retrieval_path, decision_path)
    assert len(result.cases) == 1
    assert result.summary.total_cases == 1
    assert result.summary.passed_cases == 1
    assert result.summary.failed_cases == 0


def test_returned_paths_are_preserved(tmp_path: Path) -> None:
    fixture_path = tmp_path / "fixture.json"
    retrieval_path = tmp_path / "03f.json"
    decision_path = tmp_path / "03g.json"
    _write_json(fixture_path, _fixture_payload())
    _write_json(retrieval_path, _retrieval_payload())
    _write_json(decision_path, _decision_payload())

    result = run_retrieval_evaluation(fixture_path, retrieval_path, decision_path)
    assert result.fixture_path == str(fixture_path)
    assert result.retrieval_output_path == str(retrieval_path)
    assert result.decision_output_path == str(decision_path)


def test_missing_fixture_path_fails_clearly(tmp_path: Path) -> None:
    retrieval_path = tmp_path / "03f.json"
    decision_path = tmp_path / "03g.json"
    _write_json(retrieval_path, _retrieval_payload())
    _write_json(decision_path, _decision_payload())

    with pytest.raises(FileNotFoundError):
        run_retrieval_evaluation(tmp_path / "missing_fixture.json", retrieval_path, decision_path)


def test_missing_03f_path_fails_clearly(tmp_path: Path) -> None:
    fixture_path = tmp_path / "fixture.json"
    decision_path = tmp_path / "03g.json"
    _write_json(fixture_path, _fixture_payload())
    _write_json(decision_path, _decision_payload())

    with pytest.raises(FileNotFoundError):
        run_retrieval_evaluation(fixture_path, tmp_path / "missing_03f.json", decision_path)


def test_missing_03g_path_fails_clearly(tmp_path: Path) -> None:
    fixture_path = tmp_path / "fixture.json"
    retrieval_path = tmp_path / "03f.json"
    _write_json(fixture_path, _fixture_payload())
    _write_json(retrieval_path, _retrieval_payload())

    with pytest.raises(FileNotFoundError):
        run_retrieval_evaluation(fixture_path, retrieval_path, tmp_path / "missing_03g.json")


def test_real_local_fixture_and_sample_outputs_run_through_orchestrator() -> None:
    fixture_path = POC_ROOT / "fixtures" / "labeled_retrieval_cases.json"
    retrieval_path = POC_ROOT.parent / "03f_hybrid_retrieval" / "outputs" / "sample_hybrid_search_results.json"
    decision_path = POC_ROOT.parent / "03g_retrieval_decision" / "outputs" / "sample_retrieval_decisions.json"

    result = run_retrieval_evaluation(fixture_path, retrieval_path, decision_path)
    assert result.summary.total_cases == len(result.cases)
    assert result.summary.total_cases > 0
