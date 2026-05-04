from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

POC_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = POC_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from align_cases import align_fixture_cases_to_upstream  # noqa: E402
from load_fixtures import load_labeled_retrieval_fixture  # noqa: E402
from load_upstream_outputs import load_03f_retrieval_output, load_03g_decision_output  # noqa: E402


def _fixture_payload(query: str, normalized_query: str | None = None) -> dict[str, object]:
    item: dict[str, object] = {
        "case_id": "case_001",
        "query": query,
        "expected_chunk_id": "faq__chunk_000",
        "expected_decision_label": "ambiguous_match",
        "expected_recommended_route": "clarification_path",
    }
    if normalized_query is not None:
        item["normalized_query"] = normalized_query

    return {"schema_version": "1.0", "cases": [item]}


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _upstream_03f_payload(*, query: str, normalized_query: str | None) -> dict[str, object]:
    record: dict[str, object] = {"query": query, "results": []}
    if normalized_query is not None:
        record["normalized_query"] = normalized_query
    return {"queries": [record]}


def _upstream_03g_payload(*, query: str, normalized_query: str | None) -> dict[str, object]:
    record: dict[str, object] = {
        "query": query,
        "decision_label": "ambiguous_match",
        "recommended_route": "clarification_path",
    }
    if normalized_query is not None:
        record["normalized_query"] = normalized_query
    return {"query_decisions": [record]}


def test_matching_by_normalized_query(tmp_path: Path) -> None:
    fixture_path = tmp_path / "fixture.json"
    _write_json(fixture_path, _fixture_payload(query="A", normalized_query="normalized-a"))

    retrieval_path = tmp_path / "03f.json"
    _write_json(retrieval_path, _upstream_03f_payload(query="different A", normalized_query="normalized-a"))

    decision_path = tmp_path / "03g.json"
    _write_json(decision_path, _upstream_03g_payload(query="different A", normalized_query="normalized-a"))

    aligned = align_fixture_cases_to_upstream(
        load_labeled_retrieval_fixture(fixture_path),
        load_03f_retrieval_output(retrieval_path),
        load_03g_decision_output(decision_path),
    )
    assert len(aligned) == 1
    assert aligned[0].alignment_status == "matched"
    assert aligned[0].matched_03f is True
    assert aligned[0].matched_03g is True


def test_fallback_matching_by_query(tmp_path: Path) -> None:
    fixture_path = tmp_path / "fixture.json"
    _write_json(fixture_path, _fixture_payload(query="fallback query"))

    retrieval_path = tmp_path / "03f.json"
    _write_json(retrieval_path, _upstream_03f_payload(query="fallback query", normalized_query=None))

    decision_path = tmp_path / "03g.json"
    _write_json(decision_path, _upstream_03g_payload(query="fallback query", normalized_query=None))

    aligned = align_fixture_cases_to_upstream(
        load_labeled_retrieval_fixture(fixture_path),
        load_03f_retrieval_output(retrieval_path),
        load_03g_decision_output(decision_path),
    )
    assert aligned[0].alignment_status == "matched"


def test_missing_03f_record(tmp_path: Path) -> None:
    fixture_path = tmp_path / "fixture.json"
    _write_json(fixture_path, _fixture_payload(query="target query"))

    retrieval_path = tmp_path / "03f.json"
    _write_json(retrieval_path, {"queries": []})

    decision_path = tmp_path / "03g.json"
    _write_json(decision_path, _upstream_03g_payload(query="target query", normalized_query=None))

    aligned = align_fixture_cases_to_upstream(
        load_labeled_retrieval_fixture(fixture_path),
        load_03f_retrieval_output(retrieval_path),
        load_03g_decision_output(decision_path),
    )
    assert aligned[0].alignment_status == "missing_03f"
    assert aligned[0].matched_03f is False
    assert aligned[0].matched_03g is True


def test_missing_03g_record(tmp_path: Path) -> None:
    fixture_path = tmp_path / "fixture.json"
    _write_json(fixture_path, _fixture_payload(query="target query"))

    retrieval_path = tmp_path / "03f.json"
    _write_json(retrieval_path, _upstream_03f_payload(query="target query", normalized_query=None))

    decision_path = tmp_path / "03g.json"
    _write_json(decision_path, {"query_decisions": []})

    aligned = align_fixture_cases_to_upstream(
        load_labeled_retrieval_fixture(fixture_path),
        load_03f_retrieval_output(retrieval_path),
        load_03g_decision_output(decision_path),
    )
    assert aligned[0].alignment_status == "missing_03g"
    assert aligned[0].matched_03f is True
    assert aligned[0].matched_03g is False


def test_missing_both_records(tmp_path: Path) -> None:
    fixture_path = tmp_path / "fixture.json"
    _write_json(fixture_path, _fixture_payload(query="target query"))

    retrieval_path = tmp_path / "03f.json"
    _write_json(retrieval_path, {"queries": []})

    decision_path = tmp_path / "03g.json"
    _write_json(decision_path, {"query_decisions": []})

    aligned = align_fixture_cases_to_upstream(
        load_labeled_retrieval_fixture(fixture_path),
        load_03f_retrieval_output(retrieval_path),
        load_03g_decision_output(decision_path),
    )
    assert aligned[0].alignment_status == "missing_both"
    assert aligned[0].matched_03f is False
    assert aligned[0].matched_03g is False


def test_duplicate_upstream_query_key_fails_clearly(tmp_path: Path) -> None:
    fixture_path = tmp_path / "fixture.json"
    _write_json(fixture_path, _fixture_payload(query="target query"))

    retrieval_path = tmp_path / "03f.json"
    _write_json(
        retrieval_path,
        {
            "queries": [
                {"query": "A", "normalized_query": "dup-key", "results": []},
                {"query": "B", "normalized_query": "dup-key", "results": []},
            ]
        },
    )

    decision_path = tmp_path / "03g.json"
    _write_json(decision_path, _upstream_03g_payload(query="target query", normalized_query=None))

    with pytest.raises(ValueError, match="duplicate upstream query key\\(s\\) in 03f"):
        align_fixture_cases_to_upstream(
            load_labeled_retrieval_fixture(fixture_path),
            load_03f_retrieval_output(retrieval_path),
            load_03g_decision_output(decision_path),
        )


def test_real_fixture_aligns_to_real_03f_and_03g_outputs() -> None:
    fixture = load_labeled_retrieval_fixture(POC_ROOT / "fixtures" / "labeled_retrieval_cases.json")
    retrieval_output = load_03f_retrieval_output(
        POC_ROOT.parent / "03f_hybrid_retrieval" / "outputs" / "sample_hybrid_search_results.json"
    )
    decision_output = load_03g_decision_output(
        POC_ROOT.parent / "03g_retrieval_decision" / "outputs" / "sample_retrieval_decisions.json"
    )

    aligned = align_fixture_cases_to_upstream(fixture, retrieval_output, decision_output)
    assert len(aligned) == len(fixture.cases)
    assert all(row.matched_03f for row in aligned)
    assert all(row.matched_03g for row in aligned)
    assert all(row.alignment_status == "matched" for row in aligned)
