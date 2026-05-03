from __future__ import annotations

import sys
from pathlib import Path

import joblib
import pytest
from pydantic import ValidationError
from sklearn.feature_extraction.text import TfidfVectorizer

POC_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = POC_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from hybrid_retrieval import (  # noqa: E402
    hybrid_search,
    load_index_artifact,
    merge_retrieval_results,
    search_index_artifact,
)
from schemas import HybridRetrievalConfig, HybridSearchResponse  # noqa: E402


def _make_metadata(chunk_id: str, title: str, text: str) -> dict[str, str | None]:
    return {
        "chunk_id": chunk_id,
        "source_file": f"{chunk_id}.md",
        "title": title,
        "section": None,
        "text": text,
        "normalized_text": text.lower(),
    }


def _build_artifact(rows: list[tuple[str, str, dict[str, str | None]]]) -> dict:
    chunk_ids = [row[0] for row in rows]
    corpus = [row[1] for row in rows]
    metadata = [row[2] for row in rows]

    vectorizer = TfidfVectorizer(analyzer="word", ngram_range=(1, 2), lowercase=False, min_df=1, max_df=1.0)
    matrix = vectorizer.fit_transform(corpus)

    return {
        "vectorizer": vectorizer,
        "matrix": matrix,
        "chunk_ids": chunk_ids,
        "metadata": metadata,
    }


def test_missing_artifact_file_fails_clearly(tmp_path: Path) -> None:
    missing = tmp_path / "missing.joblib"
    with pytest.raises(FileNotFoundError, match="Index artifact file not found"):
        load_index_artifact(missing)


def test_missing_artifact_keys_fail_clearly(tmp_path: Path) -> None:
    artifact_path = tmp_path / "bad.joblib"
    joblib.dump({"vectorizer": object()}, artifact_path)

    with pytest.raises(ValueError, match="Artifact missing required keys"):
        load_index_artifact(artifact_path)


def test_search_index_artifact_returns_ranked_candidates() -> None:
    artifact = _build_artifact(
        [
            ("a__chunk_000", "ac repair emergency", _make_metadata("a__chunk_000", "A", "ac repair emergency")),
            ("b__chunk_000", "water heater leak", _make_metadata("b__chunk_000", "B", "water heater leak")),
        ]
    )

    results = search_index_artifact(query="ac repair", artifact=artifact, top_k=2)

    assert len(results) == 2
    assert results[0]["chunk_id"] == "a__chunk_000"
    assert results[0]["score"] >= results[1]["score"]


def test_merge_combines_word_char_and_both_sources() -> None:
    config = HybridRetrievalConfig()

    word_results = [
        {"chunk_id": "both__chunk_000", "score": 0.6, "metadata": _make_metadata("both__chunk_000", "Both", "both text")},
        {"chunk_id": "word__chunk_000", "score": 0.9, "metadata": _make_metadata("word__chunk_000", "Word", "word text")},
    ]
    char_results = [
        {"chunk_id": "both__chunk_000", "score": 0.4, "metadata": _make_metadata("both__chunk_000", "Both", "both text")},
        {"chunk_id": "char__chunk_000", "score": 0.8, "metadata": _make_metadata("char__chunk_000", "Char", "char text")},
    ]

    merged = merge_retrieval_results(word_results=word_results, char_results=char_results, config=config)

    by_id = {item.chunk_id: item for item in merged}
    assert by_id["both__chunk_000"].retrieval_sources == ["word", "char"]
    assert by_id["word__chunk_000"].retrieval_sources == ["word"]
    assert by_id["char__chunk_000"].retrieval_sources == ["char"]


def test_hybrid_score_uses_default_weights() -> None:
    config = HybridRetrievalConfig()
    merged = merge_retrieval_results(
        word_results=[{"chunk_id": "x__chunk_000", "score": 0.8, "metadata": _make_metadata("x__chunk_000", "X", "x text")}],
        char_results=[{"chunk_id": "x__chunk_000", "score": 0.2, "metadata": _make_metadata("x__chunk_000", "X", "x text")}],
        config=config,
    )

    expected = (0.65 * 0.8) + (0.35 * 0.2)
    assert merged[0].hybrid_score == pytest.approx(expected)


def test_final_ranking_sorts_by_hybrid_score_descending() -> None:
    config = HybridRetrievalConfig()
    merged = merge_retrieval_results(
        word_results=[
            {"chunk_id": "a__chunk_000", "score": 0.9, "metadata": _make_metadata("a__chunk_000", "A", "a text")},
            {"chunk_id": "b__chunk_000", "score": 0.1, "metadata": _make_metadata("b__chunk_000", "B", "b text")},
        ],
        char_results=[
            {"chunk_id": "a__chunk_000", "score": 0.1, "metadata": _make_metadata("a__chunk_000", "A", "a text")},
            {"chunk_id": "b__chunk_000", "score": 0.9, "metadata": _make_metadata("b__chunk_000", "B", "b text")},
        ],
        config=config,
    )

    scores = [item.hybrid_score for item in merged]
    assert scores == sorted(scores, reverse=True)


def test_hybrid_search_returns_response_object(tmp_path: Path) -> None:
    word_artifact = _build_artifact(
        [
            ("ac__chunk_000", "ac repair emergency service", _make_metadata("ac__chunk_000", "AC", "ac repair emergency service")),
            ("water__chunk_000", "water heater leak", _make_metadata("water__chunk_000", "Water", "water heater leak")),
        ]
    )
    char_artifact = _build_artifact(
        [
            ("ac__chunk_000", "ac repiar emergency service", _make_metadata("ac__chunk_000", "AC", "ac repair emergency service")),
            ("water__chunk_000", "watr heater leak", _make_metadata("water__chunk_000", "Water", "water heater leak")),
        ]
    )

    word_path = tmp_path / "word.joblib"
    char_path = tmp_path / "char.joblib"
    joblib.dump(word_artifact, word_path)
    joblib.dump(char_artifact, char_path)

    response = hybrid_search(query="ac repiar", word_index_path=word_path, char_index_path=char_path)

    assert isinstance(response, HybridSearchResponse)
    assert response.query == "ac repiar"
    assert response.normalized_query != ""
    assert len(response.results) <= response.config.top_k


def test_no_customer_answer_text_generated(tmp_path: Path) -> None:
    artifact = _build_artifact(
        [
            ("one__chunk_000", "maintenance plan", _make_metadata("one__chunk_000", "One", "maintenance plan details")),
        ]
    )
    word_path = tmp_path / "word.joblib"
    char_path = tmp_path / "char.joblib"
    joblib.dump(artifact, word_path)
    joblib.dump(artifact, char_path)

    response = hybrid_search(query="maintenance plan", word_index_path=word_path, char_index_path=char_path)
    dumped = response.model_dump(mode="json")

    assert "answer" not in dumped
    assert "final_intent" not in dumped
