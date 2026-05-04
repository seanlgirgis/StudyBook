from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

POC_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = POC_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from load_fixtures import load_labeled_retrieval_fixture  # noqa: E402
from schemas import LabeledRetrievalFixture  # noqa: E402


def _base_payload() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "cases": [
            {
                "case_id": "case_001",
                "query": "ac blowing warm air",
                "normalized_query": "ac blowing warm air",
                "expected_chunk_id": "faq__chunk_000",
                "expected_decision_label": "ambiguous_match",
                "expected_recommended_route": "clarification_path",
            },
            {
                "case_id": "case_002",
                "query": "water heater leaking",
                "normalized_query": "water heater leaking",
                "expected_chunk_id": "water_heater_policy__chunk_000",
                "expected_decision_label": "strong_match",
                "expected_recommended_route": "answer_candidate_path",
            },
        ],
    }


def _write_payload(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_valid_fixture_loads_from_repo_fixture_file() -> None:
    fixture_path = POC_ROOT / "fixtures" / "labeled_retrieval_cases.json"
    loaded = load_labeled_retrieval_fixture(fixture_path)
    assert isinstance(loaded, LabeledRetrievalFixture)
    assert loaded.schema_version == "1.0"
    assert len(loaded.cases) >= 1


def test_duplicate_case_id_fails(tmp_path: Path) -> None:
    payload = _base_payload()
    cases = payload["cases"]
    assert isinstance(cases, list)
    cases[1]["case_id"] = "case_001"  # type: ignore[index]
    fixture_path = tmp_path / "duplicate_case_id.json"
    _write_payload(fixture_path, payload)

    with pytest.raises(ValidationError, match="duplicate case_id"):
        load_labeled_retrieval_fixture(fixture_path)


def test_blank_query_fails(tmp_path: Path) -> None:
    payload = _base_payload()
    cases = payload["cases"]
    assert isinstance(cases, list)
    cases[0]["query"] = "   "  # type: ignore[index]
    fixture_path = tmp_path / "blank_query.json"
    _write_payload(fixture_path, payload)

    with pytest.raises(ValidationError, match="required string fields cannot be blank"):
        load_labeled_retrieval_fixture(fixture_path)


def test_blank_expected_chunk_id_fails(tmp_path: Path) -> None:
    payload = _base_payload()
    cases = payload["cases"]
    assert isinstance(cases, list)
    cases[0]["expected_chunk_id"] = " "  # type: ignore[index]
    fixture_path = tmp_path / "blank_expected_chunk_id.json"
    _write_payload(fixture_path, payload)

    with pytest.raises(ValidationError, match="required string fields cannot be blank"):
        load_labeled_retrieval_fixture(fixture_path)


def test_blank_expected_decision_label_fails(tmp_path: Path) -> None:
    payload = _base_payload()
    cases = payload["cases"]
    assert isinstance(cases, list)
    cases[0]["expected_decision_label"] = ""  # type: ignore[index]
    fixture_path = tmp_path / "blank_expected_decision_label.json"
    _write_payload(fixture_path, payload)

    with pytest.raises(ValidationError, match="required string fields cannot be blank"):
        load_labeled_retrieval_fixture(fixture_path)


def test_blank_expected_recommended_route_fails(tmp_path: Path) -> None:
    payload = _base_payload()
    cases = payload["cases"]
    assert isinstance(cases, list)
    cases[0]["expected_recommended_route"] = ""  # type: ignore[index]
    fixture_path = tmp_path / "blank_expected_recommended_route.json"
    _write_payload(fixture_path, payload)

    with pytest.raises(ValidationError, match="required string fields cannot be blank"):
        load_labeled_retrieval_fixture(fixture_path)


def test_blank_normalized_query_fails_when_present(tmp_path: Path) -> None:
    payload = _base_payload()
    cases = payload["cases"]
    assert isinstance(cases, list)
    cases[0]["normalized_query"] = "   "  # type: ignore[index]
    fixture_path = tmp_path / "blank_normalized_query.json"
    _write_payload(fixture_path, payload)

    with pytest.raises(ValidationError, match="normalized_query cannot be blank"):
        load_labeled_retrieval_fixture(fixture_path)


def test_missing_file_fails_clearly(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_fixture.json"
    with pytest.raises(FileNotFoundError) as exc_info:
        load_labeled_retrieval_fixture(missing_path)

    assert "missing_fixture.json" in str(exc_info.value)
