"""03b_chunk_documents: convert loaded documents into validated text chunks."""

from __future__ import annotations

import json
from pathlib import Path

from schemas import DocumentChunk, LoadedDocument

TARGET_CHUNK_SIZE = 800
OVERLAP_SIZE = 100


def get_default_paths() -> tuple[Path, Path]:
    """Return input/output paths using repo-relative composition only."""

    poc_root = Path(__file__).resolve().parents[1]
    input_path = (poc_root / ".." / "03a_load_documents" / "outputs" / "loaded_documents.json").resolve()
    output_path = (poc_root / "outputs" / "chunked_documents.json").resolve()
    return input_path, output_path


def load_documents(input_path: Path) -> list[LoadedDocument]:
    """Load and validate 03a JSON payload."""

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Input JSON must be a list")
    documents = [LoadedDocument.model_validate(item) for item in payload]
    if not documents:
        raise ValueError("Input JSON contains zero documents")
    return documents


def _find_preferred_split(text: str, start: int, target_size: int) -> int:
    """Prefer paragraph boundaries so chunks preserve coherent sections."""

    hard_end = min(start + target_size, len(text))
    if hard_end >= len(text):
        return len(text)
    split_at = text.rfind("\n\n", start + 1, hard_end + 1)
    if split_at == -1 or split_at <= start:
        return hard_end
    return split_at


def _next_start(end: int, overlap_size: int) -> int:
    """Apply overlap to keep context continuity across adjacent chunks."""

    return max(0, end - overlap_size)


def chunk_document(
    document: LoadedDocument,
    target_chunk_size: int = TARGET_CHUNK_SIZE,
    overlap_size: int = OVERLAP_SIZE,
) -> list[DocumentChunk]:
    """Chunk one document with paragraph preference and character overlap."""

    if overlap_size >= target_chunk_size:
        raise ValueError("overlap_size must be smaller than target_chunk_size")

    chunks: list[DocumentChunk] = []
    text = document.text
    start = 0
    chunk_index = 0

    while start < len(text):
        end = _find_preferred_split(text, start=start, target_size=target_chunk_size)
        if end <= start:
            end = min(len(text), start + target_chunk_size)

        chunk_text = text[start:end].strip()
        if chunk_text:
            # We preserve source metadata on every chunk so retrieval results can
            # always trace back to original documents and citation sources.
            chunk = DocumentChunk(
                chunk_id=f"{document.document_id}__chunk_{chunk_index:03d}",
                document_id=document.document_id,
                source_file=document.source_file,
                source_path=document.source_path,
                title=document.title,
                chunk_index=chunk_index,
                text=chunk_text,
                character_count=len(chunk_text),
            )
            chunks.append(chunk)

            # chunk_index resets per document and increments per emitted chunk,
            # making chunk IDs stable and predictable for tests/debugging.
            chunk_index += 1

        if end >= len(text):
            break

        next_start = _next_start(end, overlap_size=overlap_size)
        if next_start <= start:
            next_start = end
        start = next_start

    return chunks


def chunk_all_documents(
    documents: list[LoadedDocument],
    target_chunk_size: int = TARGET_CHUNK_SIZE,
    overlap_size: int = OVERLAP_SIZE,
) -> list[DocumentChunk]:
    """Chunk all source documents into a flat list of DocumentChunk records."""

    all_chunks: list[DocumentChunk] = []
    for document in documents:
        all_chunks.extend(chunk_document(document, target_chunk_size, overlap_size))
    return all_chunks


def write_chunks(chunks: list[DocumentChunk], output_path: Path) -> None:
    """Write chunk records as JSON; Pydantic ensures valid chunk contracts."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [chunk.model_dump(mode="json") for chunk in chunks]
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_chunking_pipeline(
    input_path: Path,
    output_path: Path,
    target_chunk_size: int = TARGET_CHUNK_SIZE,
    overlap_size: int = OVERLAP_SIZE,
) -> tuple[int, int]:
    """Read -> chunk -> write pipeline. Returns (document_count, chunk_count)."""

    documents = load_documents(input_path)
    chunks = chunk_all_documents(documents, target_chunk_size=target_chunk_size, overlap_size=overlap_size)
    write_chunks(chunks, output_path)
    return len(documents), len(chunks)


def main() -> None:
    """CLI entrypoint for the 03b chunking POC."""

    input_path, output_path = get_default_paths()
    document_count, chunk_count = run_chunking_pipeline(
        input_path=input_path,
        output_path=output_path,
        target_chunk_size=TARGET_CHUNK_SIZE,
        overlap_size=OVERLAP_SIZE,
    )
    average = chunk_count / document_count if document_count else 0.0

    print(f"Input path: {input_path}")
    print(f"Output path: {output_path}")
    print(f"Input documents: {document_count}")
    print(f"Chunks created: {chunk_count}")
    print(f"Average chunks per document: {average:.2f}")


if __name__ == "__main__":
    main()
