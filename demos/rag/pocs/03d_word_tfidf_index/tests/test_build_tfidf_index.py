from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import pytest

POC_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = POC_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from build_tfidf_index import (  # noqa: E402
    build_tfidf_index,
    create_index_metadata,
    load_normalized_chunks,
    save_index_metadata,
    save_tfidf_artifact,
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

    with pytest.raises(ValueError, match="normalized_text"):
        validate_normalized_chunk(invalid)


def test_tfidf_matrix_has_one_row_per_chunk() -> None:
    chunks = [
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair emergency service")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater replacement")),
        validate_normalized_chunk(_make_chunk("c__chunk_000", "maintenance plan tune up")),
    ]

    artifact, _ = build_tfidf_index(chunks)

    assert artifact["matrix"].shape[0] == 3


def test_chunk_ids_preserve_input_order() -> None:
    chunks = [
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair emergency service")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater replacement")),
        validate_normalized_chunk(_make_chunk("c__chunk_000", "maintenance plan tune up")),
    ]

    artifact, _ = build_tfidf_index(chunks)

    assert artifact["chunk_ids"] == ["a__chunk_000", "b__chunk_000", "c__chunk_000"]


def test_vocabulary_contains_expected_terms() -> None:
    chunks = [
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair emergency service")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater replacement")),
        validate_normalized_chunk(_make_chunk("c__chunk_000", "maintenance plan tune up")),
    ]

    artifact, _ = build_tfidf_index(chunks)
    vocabulary = set(artifact["vectorizer"].vocabulary_.keys())

    for expected in {
        "ac",
        "repair",
        "water",
        "heater",
        "water heater",
        "maintenance",
        "maintenance plan",
    }:
        assert expected in vocabulary


def test_save_tfidf_index_creates_joblib_file(tmp_path: Path) -> None:
    chunks = [
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair emergency service")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater replacement")),
    ]
    artifact, _ = build_tfidf_index(chunks)

    output_path = tmp_path / "tfidf_index.joblib"
    save_tfidf_artifact(artifact, output_path)

    assert output_path.exists()
    loaded = joblib.load(output_path)
    assert "vectorizer" in loaded
    assert "matrix" in loaded
    assert "chunk_ids" in loaded
    assert "metadata" in loaded


def test_save_index_metadata_creates_json_file(tmp_path: Path) -> None:
    chunks = [
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair emergency service")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater replacement")),
    ]
    artifact, config = build_tfidf_index(chunks)

    input_path = tmp_path / "normalized_chunks.json"
    index_path = tmp_path / "tfidf_index.joblib"
    metadata = create_index_metadata(
        artifact=artifact,
        input_path=input_path,
        index_path=index_path,
        project_root=tmp_path,
        vectorizer_config=config,
    )

    output_path = tmp_path / "index_metadata.json"
    save_index_metadata(metadata, output_path)

    assert output_path.exists()
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    for key in {
        "poc",
        "input_path",
        "index_path",
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
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair emergency service", text="A/C Repair Emergency Service")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater replacement", text="Water Heater Replacement")),
    ]

    artifact, _ = build_tfidf_index(chunks)

    assert all("text" in record for record in artifact["metadata"])
    assert all("normalized_text" in record for record in artifact["metadata"])


def test_tfidf_can_rank_related_chunk_higher_in_tiny_smoke_test() -> None:
    chunks = [
        validate_normalized_chunk(_make_chunk("a__chunk_000", "ac repair cooling emergency")),
        validate_normalized_chunk(_make_chunk("b__chunk_000", "water heater tank leak")),
        validate_normalized_chunk(_make_chunk("c__chunk_000", "maintenance plan seasonal tune up")),
    ]

    artifact, _ = build_tfidf_index(chunks)
    query_vector = artifact["vectorizer"].transform(["ac cooling repair"])
    scores = (artifact["matrix"] @ query_vector.T).toarray().ravel()

    assert scores[0] > scores[1]
    assert scores[0] > scores[2]
