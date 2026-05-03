"""Reusable hybrid retrieval core for 03f.

This module intentionally provides library-style functions only.
It does not include CLI runner behavior or output-file writing.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import joblib
from sklearn.metrics.pairwise import cosine_similarity

from schemas import HybridRetrievalConfig, HybridSearchQuery, HybridSearchResponse, HybridSearchResult

REQUIRED_ARTIFACT_KEYS = {"vectorizer", "matrix", "chunk_ids", "metadata"}


def _load_project_normalizer() -> Any:
    """Load 03c normalize_text function so query normalization stays consistent."""

    project_root = Path(__file__).resolve().parents[3]
    src_03c = project_root / "pocs" / "03c_text_normalization" / "src"
    schemas_03c_path = src_03c / "schemas.py"
    normalizer_path = project_root / "pocs" / "03c_text_normalization" / "src" / "normalize_text.py"
    if not normalizer_path.exists():
        raise FileNotFoundError(f"03c normalization module not found: {normalizer_path}")
    if not schemas_03c_path.exists():
        raise FileNotFoundError(f"03c schemas module not found: {schemas_03c_path}")

    schemas_spec = importlib.util.spec_from_file_location("poc03c_schemas", schemas_03c_path)
    if schemas_spec is None or schemas_spec.loader is None:
        raise RuntimeError("Failed to load 03c schemas module spec")
    schemas_module = importlib.util.module_from_spec(schemas_spec)
    schemas_spec.loader.exec_module(schemas_module)

    spec = importlib.util.spec_from_file_location("poc03c_normalize_text", normalizer_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load 03c normalization module spec")

    module = importlib.util.module_from_spec(spec)
    existing_schemas = sys.modules.get("schemas")
    sys.modules["schemas"] = schemas_module
    try:
        spec.loader.exec_module(module)
    finally:
        if existing_schemas is None:
            sys.modules.pop("schemas", None)
        else:
            sys.modules["schemas"] = existing_schemas

    if not hasattr(module, "normalize_text"):
        raise AttributeError("03c normalization module is missing normalize_text")
    return module.normalize_text


def normalize_query(query: str) -> str:
    """Normalize query text using the existing 03c normalization behavior."""

    normalizer = _load_project_normalizer()
    return str(normalizer(query))


def load_index_artifact(path: Path) -> dict[str, Any]:
    """Load and validate a TF-IDF index artifact from joblib."""

    resolved_path = path.resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(f"Index artifact file not found: {resolved_path}")

    artifact = joblib.load(resolved_path)
    if not isinstance(artifact, dict):
        raise ValueError(f"Invalid artifact format at {resolved_path}: expected dict")

    missing = REQUIRED_ARTIFACT_KEYS.difference(artifact.keys())
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"Artifact missing required keys at {resolved_path}: {missing_text}")

    chunk_ids = artifact["chunk_ids"]
    metadata = artifact["metadata"]
    matrix = artifact["matrix"]

    if not isinstance(chunk_ids, list) or not isinstance(metadata, list):
        raise ValueError("Artifact chunk_ids and metadata must both be lists")
    if len(chunk_ids) != len(metadata):
        raise ValueError("Artifact chunk_ids and metadata length mismatch")
    if matrix.shape[0] != len(chunk_ids):
        raise ValueError("Artifact matrix row count must match chunk_ids length")

    return artifact


def search_index_artifact(query: str, artifact: dict[str, Any], top_k: int) -> list[dict[str, Any]]:
    """Search one artifact and return ranked candidate matches."""

    if top_k < 1:
        raise ValueError("top_k must be >= 1")

    vectorizer = artifact["vectorizer"]
    matrix = artifact["matrix"]
    chunk_ids: list[str] = artifact["chunk_ids"]
    metadata: list[dict[str, Any]] = artifact["metadata"]

    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, matrix).ravel()

    ranked_indexes = sorted(enumerate(scores), key=lambda item: item[1], reverse=True)[:top_k]
    results: list[dict[str, Any]] = []

    for row_index, score in ranked_indexes:
        results.append(
            {
                "chunk_id": chunk_ids[row_index],
                "score": float(score),
                "metadata": dict(metadata[row_index]),
            }
        )

    return results


def merge_retrieval_results(
    word_results: list[dict[str, Any]],
    char_results: list[dict[str, Any]],
    config: HybridRetrievalConfig,
) -> list[HybridSearchResult]:
    """Merge word/char retrieval candidates and compute hybrid ranking."""

    merged: dict[str, dict[str, Any]] = {}

    for item in word_results:
        chunk_id = item["chunk_id"]
        merged[chunk_id] = {
            "chunk_id": chunk_id,
            "word_score": float(item["score"]),
            "char_score": 0.0,
            "metadata": dict(item["metadata"]),
            "retrieval_sources": {"word"},
        }

    for item in char_results:
        chunk_id = item["chunk_id"]
        if chunk_id not in merged:
            merged[chunk_id] = {
                "chunk_id": chunk_id,
                "word_score": 0.0,
                "char_score": float(item["score"]),
                "metadata": dict(item["metadata"]),
                "retrieval_sources": {"char"},
            }
        else:
            merged[chunk_id]["char_score"] = float(item["score"])
            merged[chunk_id]["retrieval_sources"].add("char")

    ranked = sorted(
        merged.values(),
        key=lambda item: (config.word_weight * item["word_score"]) + (config.char_weight * item["char_score"]),
        reverse=True,
    )

    response_rows: list[HybridSearchResult] = []
    for rank, item in enumerate(ranked, start=1):
        metadata = item["metadata"]
        word_score = item["word_score"]
        char_score = item["char_score"]
        hybrid_score = (config.word_weight * word_score) + (config.char_weight * char_score)

        retrieval_sources = ["word", "char"]
        if item["retrieval_sources"] == {"word"}:
            retrieval_sources = ["word"]
        elif item["retrieval_sources"] == {"char"}:
            retrieval_sources = ["char"]

        response_rows.append(
            HybridSearchResult(
                rank=rank,
                chunk_id=item["chunk_id"],
                hybrid_score=float(hybrid_score),
                word_score=float(word_score),
                char_score=float(char_score),
                word_weight=config.word_weight,
                char_weight=config.char_weight,
                retrieval_sources=retrieval_sources,
                source_file=metadata["source_file"],
                title=metadata["title"],
                section=metadata.get("section"),
                text=metadata["text"],
                normalized_text=metadata["normalized_text"],
            )
        )

    return response_rows


def hybrid_search(
    query: str,
    word_index_path: Path,
    char_index_path: Path,
    config: HybridRetrievalConfig | None = None,
) -> HybridSearchResponse:
    """Run hybrid retrieval across word and char artifacts and return structured response."""

    validated_query = HybridSearchQuery(query=query)
    effective_config = config or HybridRetrievalConfig()
    normalized_query = normalize_query(validated_query.query)

    word_artifact = load_index_artifact(word_index_path)
    char_artifact = load_index_artifact(char_index_path)

    word_results = search_index_artifact(query=normalized_query, artifact=word_artifact, top_k=effective_config.top_k)
    char_results = search_index_artifact(query=normalized_query, artifact=char_artifact, top_k=effective_config.top_k)

    merged = merge_retrieval_results(word_results=word_results, char_results=char_results, config=effective_config)
    final_results = merged[: effective_config.top_k]

    return HybridSearchResponse(
        query=validated_query.query,
        normalized_query=normalized_query,
        config=effective_config,
        results=final_results,
    )
