from __future__ import annotations

import json
import re
import sys
from pathlib import Path

POC_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = POC_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from chunk_documents import (  # noqa: E402
    OVERLAP_SIZE,
    TARGET_CHUNK_SIZE,
    chunk_all_documents,
    get_default_paths,
    load_documents,
    run_chunking_pipeline,
)
from schemas import DocumentChunk  # noqa: E402


def test_script_default_input_path_points_to_03a_output() -> None:
    input_path, _ = get_default_paths()
    normalized = input_path.as_posix()
    assert normalized.endswith("pocs/03a_load_documents/outputs/loaded_documents.json")


def test_chunking_creates_at_least_one_chunk_per_source_document() -> None:
    input_path, _ = get_default_paths()
    documents = load_documents(input_path)
    chunks = chunk_all_documents(documents, target_chunk_size=TARGET_CHUNK_SIZE, overlap_size=OVERLAP_SIZE)
    document_ids = {document.document_id for document in documents}
    chunked_document_ids = {chunk.document_id for chunk in chunks}
    assert document_ids.issubset(chunked_document_ids)


def test_all_chunks_have_required_metadata_and_no_empty_text() -> None:
    input_path, _ = get_default_paths()
    documents = load_documents(input_path)
    chunks = chunk_all_documents(documents, target_chunk_size=TARGET_CHUNK_SIZE, overlap_size=OVERLAP_SIZE)
    assert chunks
    assert all(isinstance(chunk, DocumentChunk) for chunk in chunks)
    assert all(chunk.chunk_id for chunk in chunks)
    assert all(chunk.document_id for chunk in chunks)
    assert all(chunk.source_file for chunk in chunks)
    assert all(chunk.source_path for chunk in chunks)
    assert all(chunk.title for chunk in chunks)
    assert all(chunk.text.strip() for chunk in chunks)
    assert all(chunk.character_count == len(chunk.text) for chunk in chunks)


def test_chunk_ids_are_unique_and_follow_expected_naming_pattern() -> None:
    input_path, _ = get_default_paths()
    documents = load_documents(input_path)
    chunks = chunk_all_documents(documents, target_chunk_size=TARGET_CHUNK_SIZE, overlap_size=OVERLAP_SIZE)
    chunk_ids = [chunk.chunk_id for chunk in chunks]
    assert len(chunk_ids) == len(set(chunk_ids))
    pattern = re.compile(r"^[a-z0-9_]+__chunk_\d{3}$")
    assert all(pattern.match(chunk_id) for chunk_id in chunk_ids)


def test_chunk_index_starts_at_zero_and_increments_per_document() -> None:
    input_path, _ = get_default_paths()
    documents = load_documents(input_path)
    chunks = chunk_all_documents(documents, target_chunk_size=TARGET_CHUNK_SIZE, overlap_size=OVERLAP_SIZE)
    chunks_by_document: dict[str, list[DocumentChunk]] = {}
    for chunk in chunks:
        chunks_by_document.setdefault(chunk.document_id, []).append(chunk)

    for document_chunks in chunks_by_document.values():
        sorted_chunks = sorted(document_chunks, key=lambda item: item.chunk_index)
        assert sorted_chunks[0].chunk_index == 0
        expected = list(range(len(sorted_chunks)))
        actual = [chunk.chunk_index for chunk in sorted_chunks]
        assert actual == expected


def test_running_pipeline_writes_output_file() -> None:
    input_path, _ = get_default_paths()
    output_path = POC_ROOT / "outputs" / "chunked_documents.test.json"
    try:
        document_count, chunk_count = run_chunking_pipeline(input_path=input_path, output_path=output_path)
        assert document_count > 0
        assert chunk_count >= document_count
        assert output_path.exists()
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        assert isinstance(payload, list)
        assert payload
    finally:
        if output_path.exists():
            output_path.unlink()
