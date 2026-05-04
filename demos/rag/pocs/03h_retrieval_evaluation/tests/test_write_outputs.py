from __future__ import annotations

import json
import sys
from pathlib import Path

POC_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = POC_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from run_evaluation import run_retrieval_evaluation  # noqa: E402
from write_outputs import (  # noqa: E402
    write_evaluation_outputs,
    write_evaluation_report,
    write_evaluation_summary_md,
)


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


def _build_result(tmp_path: Path):
    fixture_path = tmp_path / "fixture.json"
    retrieval_path = tmp_path / "03f.json"
    decision_path = tmp_path / "03g.json"
    _write_json(fixture_path, _fixture_payload())
    _write_json(retrieval_path, _retrieval_payload())
    _write_json(decision_path, _decision_payload())
    return run_retrieval_evaluation(fixture_path, retrieval_path, decision_path)


def test_json_report_file_is_written(tmp_path: Path) -> None:
    result = _build_result(tmp_path)
    output_path = tmp_path / "outputs" / "evaluation_report.json"
    written = write_evaluation_report(result, output_path)
    assert written == output_path
    assert output_path.exists()


def test_json_report_has_schema_version_cases_and_summary(tmp_path: Path) -> None:
    result = _build_result(tmp_path)
    output_path = tmp_path / "outputs" / "evaluation_report.json"
    write_evaluation_report(result, output_path)
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "1.0"
    assert isinstance(payload["cases"], list)
    assert isinstance(payload["summary"], dict)


def test_output_parent_directory_is_created_if_missing(tmp_path: Path) -> None:
    result = _build_result(tmp_path)
    output_path = tmp_path / "a" / "deep" / "path" / "evaluation_report.json"
    assert not output_path.parent.exists()
    write_evaluation_report(result, output_path)
    assert output_path.parent.exists()


def test_markdown_summary_file_is_written(tmp_path: Path) -> None:
    result = _build_result(tmp_path)
    output_path = tmp_path / "outputs" / "evaluation_summary.md"
    written = write_evaluation_summary_md(result, output_path)
    assert written == output_path
    assert output_path.exists()


def test_markdown_includes_key_summary_fields(tmp_path: Path) -> None:
    result = _build_result(tmp_path)
    output_path = tmp_path / "outputs" / "evaluation_summary.md"
    write_evaluation_summary_md(result, output_path)
    text = output_path.read_text(encoding="utf-8")
    assert "Retrieval Evaluation Summary" in text
    assert "Schema Version" in text
    assert "Total Cases" in text
    assert "Pass Rate" in text
    assert "Hit@1 Rate" in text
    assert "Decision Label Match Rate" in text


def test_markdown_includes_per_case_table(tmp_path: Path) -> None:
    result = _build_result(tmp_path)
    output_path = tmp_path / "outputs" / "evaluation_summary.md"
    write_evaluation_summary_md(result, output_path)
    text = output_path.read_text(encoding="utf-8")
    assert "| case_id | status | expected_chunk_rank | hit_at_1 | hit_at_3 | hit_at_5 | decision_label_match | recommended_route_match | failure_category |" in text
    assert "case_001" in text


def test_write_evaluation_outputs_writes_both_expected_files(tmp_path: Path) -> None:
    result = _build_result(tmp_path)
    output_dir = tmp_path / "outputs"
    written = write_evaluation_outputs(result, output_dir)
    assert written["evaluation_report"] == output_dir / "evaluation_report.json"
    assert written["evaluation_summary"] == output_dir / "evaluation_summary.md"
    assert written["evaluation_report"].exists()
    assert written["evaluation_summary"].exists()
