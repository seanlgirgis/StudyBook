"""03c_text_normalization: normalize chunk text for later lexical retrieval work."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from schemas import DocumentChunk, NormalizedChunk

SMART_PUNCT_TRANSLATION = str.maketrans(
    {
        "\u2018": "'",
        "\u2019": "'",
        "\u201C": '"',
        "\u201D": '"',
    }
)

LONG_DASH_PATTERN = re.compile(r"[\u2012\u2013\u2014\u2015\u2212]")
AC_PATTERN = re.compile(r"\ba\s*/\s*c\b", flags=re.IGNORECASE)
AIR_CONDITIONING_PATTERN = re.compile(r"\bair[\s\-]+conditioning\b", flags=re.IGNORECASE)
NON_WORD_PATTERN = re.compile(r"[^\w\s]")
WHITESPACE_PATTERN = re.compile(r"\s+")


def get_default_paths() -> tuple[Path, Path]:
    """Return 03b input and 03c output using repo-relative composition only."""

    poc_root = Path(__file__).resolve().parents[1]
    input_path = (poc_root / ".." / "03b_chunk_documents" / "outputs" / "chunked_documents.json").resolve()
    output_path = (poc_root / "outputs" / "normalized_chunks.json").resolve()
    return input_path, output_path


def normalize_text(text: str) -> str:
    """Apply simple, learning-first normalization rules for lexical retrieval."""

    normalized = unicodedata.normalize("NFKC", text)
    normalized = normalized.translate(SMART_PUNCT_TRANSLATION)
    normalized = LONG_DASH_PATTERN.sub(" ", normalized)

    # Normalize AC synonyms before punctuation stripping so slash variants survive.
    normalized = AC_PATTERN.sub("ac", normalized)
    normalized = AIR_CONDITIONING_PATTERN.sub("air conditioning", normalized)

    normalized = normalized.lower()
    normalized = NON_WORD_PATTERN.sub(" ", normalized)
    normalized = WHITESPACE_PATTERN.sub(" ", normalized)
    return normalized.strip()


def load_chunks(input_path: Path) -> list[DocumentChunk]:
    """Load and validate 03b chunk payload."""

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Input JSON must be a list")

    chunks = [DocumentChunk.model_validate(item) for item in payload]
    if not chunks:
        raise ValueError("Input JSON contains zero chunks")
    return chunks


def normalize_chunks(chunks: list[DocumentChunk]) -> list[NormalizedChunk]:
    """Preserve original chunk fields and add normalized text fields."""

    normalized_chunks: list[NormalizedChunk] = []

    for chunk in chunks:
        normalized_text = normalize_text(chunk.text)
        normalized_chunk = NormalizedChunk(
            **chunk.model_dump(mode="python"),
            normalized_text=normalized_text,
            normalized_character_count=len(normalized_text),
        )
        normalized_chunks.append(normalized_chunk)

    return normalized_chunks


def write_normalized_chunks(normalized_chunks: list[NormalizedChunk], output_path: Path) -> None:
    """Write validated normalized chunks as JSON."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [chunk.model_dump(mode="json") for chunk in normalized_chunks]
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_normalization_pipeline(input_path: Path, output_path: Path) -> tuple[int, int, str, str]:
    """Read -> normalize -> write pipeline and return summary data."""

    chunks = load_chunks(input_path)
    normalized_chunks = normalize_chunks(chunks)
    write_normalized_chunks(normalized_chunks, output_path)

    sample_original = chunks[0].text
    sample_normalized = normalized_chunks[0].normalized_text
    return len(chunks), len(normalized_chunks), sample_original, sample_normalized


def _shorten_sample(text: str, width: int = 160) -> str:
    compact = WHITESPACE_PATTERN.sub(" ", text).strip()
    if len(compact) <= width:
        return compact
    return compact[:width].rstrip() + "..."


def main() -> None:
    """CLI entrypoint for the 03c normalization POC."""

    input_path, output_path = get_default_paths()
    input_count, output_count, sample_original, sample_normalized = run_normalization_pipeline(
        input_path=input_path,
        output_path=output_path,
    )

    print(f"Input path: {input_path}")
    print(f"Output path: {output_path}")
    print(f"Chunks read: {input_count}")
    print(f"Chunks written: {output_count}")
    print("Sample before:", _shorten_sample(sample_original))
    print("Sample after:", _shorten_sample(sample_normalized))


if __name__ == "__main__":
    main()
