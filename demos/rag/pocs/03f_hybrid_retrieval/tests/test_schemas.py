from __future__ import annotations

import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

POC_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = POC_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from schemas import (  # noqa: E402
    HybridRetrievalConfig,
    HybridSearchQuery,
    HybridSearchResponse,
    HybridSearchResult,
)


def _valid_result() -> dict[str, object]:
    return {
        "rank": 1,
        "chunk_id": "heating_repair_overview__chunk_000",
        "hybrid_score": 0.7421,
        "word_score": 0.6815,
        "char_score": 0.8548,
        "word_weight": 0.65,
        "char_weight": 0.35,
        "retrieval_sources": ["word", "char"],
        "source_file": "heating_repair_overview.md",
        "title": "Heating Repair Services",
        "section": "Common Heating Issues",
        "text": "Our technicians diagnose and repair heater issues.",
        "normalized_text": "our technicians diagnose and repair heater issues",
    }


def test_default_config_values() -> None:
    config = HybridRetrievalConfig()

    assert config.word_weight == 0.65
    assert config.char_weight == 0.35
    assert config.top_k == 5


def test_invalid_weights_fail() -> None:
    with pytest.raises(ValidationError):
        HybridRetrievalConfig(word_weight=1.1)

    with pytest.raises(ValidationError):
        HybridRetrievalConfig(char_weight=-0.1)


def test_weights_not_totaling_one_fails() -> None:
    with pytest.raises(ValidationError, match="must equal 1.0"):
        HybridRetrievalConfig(word_weight=0.7, char_weight=0.35)


def test_empty_query_fails() -> None:
    with pytest.raises(ValidationError, match="query cannot be empty"):
        HybridSearchQuery(query="   ")


def test_valid_result_object_passes() -> None:
    result = HybridSearchResult(**_valid_result())

    assert result.rank == 1
    assert result.chunk_id == "heating_repair_overview__chunk_000"


def test_invalid_retrieval_sources_fail() -> None:
    payload = _valid_result()
    payload["retrieval_sources"] = ["word_tfidf"]

    with pytest.raises(ValidationError):
        HybridSearchResult(**payload)


def test_empty_text_fails() -> None:
    payload = _valid_result()
    payload["text"] = "   "

    with pytest.raises(ValidationError, match="text fields cannot be empty"):
        HybridSearchResult(**payload)


def test_valid_response_passes() -> None:
    response = HybridSearchResponse(
        query="heater repaid",
        normalized_query="heater repaid",
        config=HybridRetrievalConfig(),
        results=[HybridSearchResult(**_valid_result())],
    )

    assert response.query == "heater repaid"
    assert len(response.results) == 1
