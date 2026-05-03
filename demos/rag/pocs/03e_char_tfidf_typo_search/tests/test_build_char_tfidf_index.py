from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib

POC_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = POC_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from build_char_tfidf_index import (  # noqa: E402
    build_char_tfidf_index,
    create_index_metadata,
    create_sample_typo_search_results,
    load_normalized_chunks,
    save_char_tfidf_artifact,
    save_index_metadata,
    save_sample_results,
    search_char_tfidf,
    validate_normalized_chunk,
)


def _make_chunk(chunk_id: str, normalized_text: str, text: str | None = None) -> dict[str, object]:
    original_text = text if text is not None else normalized_text
    return {
        "chunk_id": chunk_id,
        "document_id": chunk_id.split("__")[0],
        "source_file": f"{chunk_id}.md",
        "source_path": f"pocs/demo/{chunk_id}.md",
        "title": "Synthetic Demo Document",
        "chunk_index": 0,
        "text": original_text,
        "character_count": len(original_text),
        "normalized_text": normalized_text,
        "normalized_character_count": len(normalized_text),
    }


def test_load_normalized_chunks_reads_records(tmp_path: Path) -> None:
    input_path = tmp_path / "normalized_chunks.json"
    payload = [
        _make_chunk("a__chunk_000", "ac repair emergency service"),
        _make_chunk("b__chunk_000", "water heater replacement"),
    ]
    input_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    records = load_normalized_chunks(input_path)

    assert len(records) == 2
    assert records[0].chunk_id == "a__chunk_000"
    assert records[0].normalized_text == "ac repair emergency service"


def test_missing_normalized_text_fails_validation() -> None:
    invalid = _make_chunk("a__chunk_000", "ac repair")
    invalid.pop("normalized_text")

    try:
        validate_normalized_chunk(invalid)
        assert False, "Expected ValueError for missing normalized_text"
    except ValueError as exc:
        assert "normalized_text" in str(exc)


def test_char_tfidf_matrix_has_one_row_per_chunk() -> None:
    chunks = [
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair cooling emergency")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater tank leak")),
        validate_normalized_chunk(_make_chunk("c__chunk_000", "maintenance plan seasonal tune up")),
    ]

    artifact, _ = build_char_tfidf_index(chunks)

    assert artifact["matrix"].shape[0] == 3


def test_chunk_ids_preserve_input_order() -> None:
    chunks = [
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair cooling emergency")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater tank leak")),
        validate_normalized_chunk(_make_chunk("c__chunk_000", "maintenance plan seasonal tune up")),
    ]

    artifact, _ = build_char_tfidf_index(chunks)

    assert artifact["chunk_ids"] == ["a__chunk_000", "b__chunk_000", "c__chunk_000"]


def test_vectorizer_uses_character_analyzer() -> None:
    chunks = [
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair cooling emergency")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater tank leak")),
    ]

    artifact, _ = build_char_tfidf_index(chunks)
    params = artifact["vectorizer"].get_params()

    assert params["analyzer"] == "char_wb"
    assert params["ngram_range"] == (3, 5)
    assert params["lowercase"] is False


def test_save_char_tfidf_index_creates_joblib_file(tmp_path: Path) -> None:
    chunks = [
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair cooling emergency")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater tank leak")),
    ]
    artifact, _ = build_char_tfidf_index(chunks)

    output_path = tmp_path / "char_tfidf_index.joblib"
    save_char_tfidf_artifact(artifact, output_path)

    assert output_path.exists()
    loaded = joblib.load(output_path)
    assert "vectorizer" in loaded
    assert "matrix" in loaded
    assert "chunk_ids" in loaded
    assert "metadata" in loaded


def test_save_char_index_metadata_creates_json_file(tmp_path: Path) -> None:
    chunks = [
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair cooling emergency")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater tank leak")),
    ]
    artifact, config = build_char_tfidf_index(chunks)

    input_path = tmp_path / "normalized_chunks.json"
    index_path = tmp_path / "char_tfidf_index.joblib"
    sample_path = tmp_path / "sample_typo_search_results.json"
    metadata = create_index_metadata(
        artifact=artifact,
        input_path=input_path,
        index_path=index_path,
        sample_results_path=sample_path,
        project_root=tmp_path,
        vectorizer_config=config,
    )

    output_path = tmp_path / "char_index_metadata.json"
    save_index_metadata(metadata, output_path)

    assert output_path.exists()
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    for key in {
        "poc",
        "input_path",
        "index_path",
        "sample_results_path",
        "chunk_count",
        "matrix_shape",
        "vocabulary_size",
        "chunk_ids",
        "sample_vocabulary",
        "vectorizer_config",
    }:
        assert key in payload


def test_artifact_metadata_preserves_original_and_normalized_text() -> None:
    chunks = [
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair cooling emergency", text="A/C Repair Cooling Emergency")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater tank leak", text="Water Heater Tank Leak")),
    ]

    artifact, _ = build_char_tfidf_index(chunks)

    assert all("text" in record for record in artifact["metadata"])
    assert all("normalized_text" in record for record in artifact["metadata"])


def test_typo_query_ranks_related_chunk_higher() -> None:
    chunks = [
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair cooling emergency")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater tank leak")),
        validate_normalized_chunk(_make_chunk("c__chunk_000", "maintenance plan seasonal tune up")),
    ]

    artifact, _ = build_char_tfidf_index(chunks)
    result = search_char_tfidf(artifact, "ac repiar", top_k=3)
    top_scores = {match["chunk_id"]: match["score"] for match in result["top_matches"]}

    assert top_scores["a__chunk_000"] > top_scores["b__chunk_000"]
    assert top_scores["a__chunk_000"] > top_scores["c__chunk_000"]


def test_water_heater_typo_query_ranks_related_chunk_higher() -> None:
    chunks = [
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair cooling emergency")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater tank leak")),
        validate_normalized_chunk(_make_chunk("c__chunk_000", "maintenance plan seasonal tune up")),
    ]

    artifact, _ = build_char_tfidf_index(chunks)
    result = search_char_tfidf(artifact, "watr heater", top_k=3)
    top_scores = {match["chunk_id"]: match["score"] for match in result["top_matches"]}

    assert top_scores["b__chunk_000"] > top_scores["a__chunk_000"]
    assert top_scores["b__chunk_000"] > top_scores["c__chunk_000"]


def test_sample_typo_search_results_are_created(tmp_path: Path) -> None:
    chunks = [
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair cooling emergency")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater tank leak")),
        validate_normalized_chunk(_make_chunk("c__chunk_000", "maintenance plan seasonal tune up")),
    ]
    artifact, _ = build_char_tfidf_index(chunks)

    results = create_sample_typo_search_results(artifact, queries=["ac repiar", "watr heater"], top_k=2)
    output_path = tmp_path / "sample_typo_search_results.json"
    save_sample_results(results, output_path)

    assert output_path.exists()
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert isinstance(payload, list)
    assert payload
    for item in payload:
        assert "query" in item
        assert "normalized_query" in item
        assert "top_matches" in item
        for match in item["top_matches"]:
            assert "rank" in match
            assert "chunk_id" in match
            assert "title" in match
            assert "score" in match
