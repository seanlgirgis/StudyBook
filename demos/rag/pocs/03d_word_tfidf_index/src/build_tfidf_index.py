"""03d_word_tfidf_index: build and persist a word-level TF-IDF index from normalized chunks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

from schemas import NormalizedChunkRecord

DEFAULT_VECTORIZER_CONFIG: dict[str, Any] = {
    "analyzer": "word",
    "ngram_range": (1, 2),
    "lowercase": False,
    "min_df": 1,
    "max_df": 1.0,
}


def resolve_project_root() -> Path:
    """Resolve repository root by locating AGENTS.md from this script path."""

    current = Path(__file__).resolve()
    for candidate in [current.parent, *current.parents]:
        if (candidate / "AGENTS.md").exists():
            return candidate
    raise RuntimeError("Could not resolve project root (AGENTS.md not found).")


def get_default_paths(project_root: Path) -> tuple[Path, Path, Path]:
    """Return default input/index/metadata paths for this POC."""

    input_path = project_root / "pocs" / "03c_text_normalization" / "outputs" / "normalized_chunks.json"
    index_output = project_root / "pocs" / "03d_word_tfidf_index" / "outputs" / "tfidf_index.joblib"
    metadata_output = project_root / "pocs" / "03d_word_tfidf_index" / "outputs" / "index_metadata.json"
    return input_path, index_output, metadata_output


def resolve_cli_path(project_root: Path, path_text: str) -> Path:
    """Resolve CLI path argument as absolute or repo-relative path."""

    raw_path = Path(path_text)
    return raw_path if raw_path.is_absolute() else project_root / raw_path


def validate_normalized_chunk(record: dict[str, Any]) -> NormalizedChunkRecord:
    """Validate one normalized chunk record using Pydantic."""

    try:
        return NormalizedChunkRecord.model_validate(record)
    except Exception as exc:  # pydantic ValidationError in practice
        raise ValueError(f"Invalid normalized chunk record: {exc}") from exc


def load_normalized_chunks(input_path: Path) -> list[NormalizedChunkRecord]:
    """Load and validate normalized chunk records from JSON file."""

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    payload = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Input JSON must be a list of chunk records")
    if not payload:
        raise ValueError("Input JSON contains zero chunk records")

    chunks: list[NormalizedChunkRecord] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ValueError(f"Invalid chunk record at index {index}: expected object")
        try:
            chunk = validate_normalized_chunk(item)
        except ValueError as exc:
            raise ValueError(f"Invalid chunk record at index {index}: {exc}") from exc
        chunks.append(chunk)

    return chunks


def build_tfidf_index(
    chunks: list[NormalizedChunkRecord],
    vectorizer_config: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build TF-IDF artifact dictionary from validated chunks."""

    if not chunks:
        raise ValueError("Cannot build TF-IDF index from empty chunk list")

    config = dict(DEFAULT_VECTORIZER_CONFIG)
    if vectorizer_config:
        config.update(vectorizer_config)

    corpus = [chunk.normalized_text for chunk in chunks]
    vectorizer = TfidfVectorizer(**config)
    tfidf_matrix = vectorizer.fit_transform(corpus)

    chunk_ids = [chunk.chunk_id for chunk in chunks]
    metadata = [chunk.model_dump(mode="json") for chunk in chunks]

    artifact = {
        "vectorizer": vectorizer,
        "matrix": tfidf_matrix,
        "chunk_ids": chunk_ids,
        "metadata": metadata,
    }
    return artifact, config


def _serialize_vectorizer_config(config: dict[str, Any]) -> dict[str, Any]:
    serialized = dict(config)
    if "ngram_range" in serialized:
        serialized["ngram_range"] = list(serialized["ngram_range"])
    return serialized


def _display_path(path: Path, project_root: Path) -> str:
    resolved_path = path.resolve()
    try:
        return resolved_path.relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return str(resolved_path)


def create_index_metadata(
    artifact: dict[str, Any],
    input_path: Path,
    index_path: Path,
    project_root: Path,
    vectorizer_config: dict[str, Any],
    sample_size: int = 20,
) -> dict[str, Any]:
    """Create human-readable metadata describing the saved TF-IDF catalog."""

    vectorizer = artifact["vectorizer"]
    matrix = artifact["matrix"]
    vocabulary = sorted(vectorizer.vocabulary_.keys())

    return {
        "poc": "03d_word_tfidf_index",
        "input_path": _display_path(input_path, project_root),
        "index_path": _display_path(index_path, project_root),
        "chunk_count": int(matrix.shape[0]),
        "matrix_shape": [int(matrix.shape[0]), int(matrix.shape[1])],
        "vocabulary_size": int(len(vocabulary)),
        "chunk_ids": artifact["chunk_ids"],
        "sample_vocabulary": vocabulary[:sample_size],
        "vectorizer_config": _serialize_vectorizer_config(vectorizer_config),
    }


def save_tfidf_artifact(artifact: dict[str, Any], output_path: Path) -> None:
    """Persist TF-IDF artifact to joblib file."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, output_path)


def save_index_metadata(metadata: dict[str, Any], output_path: Path) -> None:
    """Persist index metadata to human-readable JSON file."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def parse_args(project_root: Path) -> argparse.Namespace:
    """Parse CLI arguments with sensible repo-relative defaults."""

    default_input, default_index, default_metadata = get_default_paths(project_root)

    parser = argparse.ArgumentParser(description="Build a word-level TF-IDF index from normalized chunks.")
    parser.add_argument(
        "--input",
        default=default_input.relative_to(project_root).as_posix(),
        help="Path to normalized chunks JSON (absolute or repo-relative)",
    )
    parser.add_argument(
        "--index-output",
        default=default_index.relative_to(project_root).as_posix(),
        help="Path to output joblib index artifact (absolute or repo-relative)",
    )
    parser.add_argument(
        "--metadata-output",
        default=default_metadata.relative_to(project_root).as_posix(),
        help="Path to output metadata JSON (absolute or repo-relative)",
    )
    return parser.parse_args()


def main() -> None:
    """Thin CLI wrapper for the 03d TF-IDF index build pipeline."""

    project_root = resolve_project_root()
    args = parse_args(project_root)

    input_path = resolve_cli_path(project_root, args.input).resolve()
    index_output_path = resolve_cli_path(project_root, args.index_output).resolve()
    metadata_output_path = resolve_cli_path(project_root, args.metadata_output).resolve()

    chunks = load_normalized_chunks(input_path)
    artifact, vectorizer_config = build_tfidf_index(chunks)

    save_tfidf_artifact(artifact, index_output_path)
    metadata = create_index_metadata(
        artifact=artifact,
        input_path=input_path,
        index_path=index_output_path,
        project_root=project_root,
        vectorizer_config=vectorizer_config,
    )
    save_index_metadata(metadata, metadata_output_path)

    print(f"Input path: {input_path}")
    print(f"Output index path: {index_output_path}")
    print(f"Output metadata path: {metadata_output_path}")
    print(f"Chunks read: {len(chunks)}")
    print(f"TF-IDF matrix shape: {artifact['matrix'].shape}")
    print(f"Vocabulary size: {len(artifact['vectorizer'].vocabulary_)}")
    print(f"Sample vocabulary: {metadata['sample_vocabulary']}")
    print("PASS")


if __name__ == "__main__":
    main()
