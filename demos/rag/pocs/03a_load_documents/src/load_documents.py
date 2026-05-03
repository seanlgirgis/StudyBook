"""03a load-documents POC flow.

This script performs only the first retrieval-ladder step:
markdown files -> SourceDocument objects -> loaded_documents.json

Intentionally out of scope for 03a:
- no chunking
- no TF-IDF or retrieval/search
- no answer generation
- no AI/model calls

The JSON emitted here is the handoff input for 03b_chunk_documents.
"""

from __future__ import annotations

import json
from pathlib import Path

from schemas import SourceDocument


def find_repo_root(start_path: Path) -> Path:
    """Walk upward until we find repo structure with the 02 docs folder.

    Path discovery keeps this script runnable from the 03a POC directory while
    still locating the canonical synthetic corpus under:
    pocs/02_fake_business_docs/data/home_services_demo
    """

    current = start_path.resolve()
    for candidate in [current, *current.parents]:
        expected_docs = candidate / "pocs" / "02_fake_business_docs" / "data" / "home_services_demo"
        if expected_docs.exists():
            return candidate
    raise FileNotFoundError("Could not locate repo root containing pocs/02_fake_business_docs/data/home_services_demo")


def discover_markdown_files(docs_dir: Path) -> list[Path]:
    """Return sorted markdown files from the target docs directory.

    We fail fast when the directory is missing or no `.md` files exist, because
    later retrieval stages depend on a complete synthetic corpus.
    """

    if not docs_dir.exists():
        raise FileNotFoundError(f"Docs directory not found: {docs_dir}")

    markdown_files = sorted(path for path in docs_dir.glob("*.md") if path.is_file())
    if not markdown_files:
        raise ValueError(f"No markdown files found in: {docs_dir}")

    return markdown_files


def extract_title(markdown_text: str, fallback: str) -> str:
    """Extract first markdown heading as title, otherwise use fallback.

    Title extraction is lightweight in 03a; robust title normalization belongs
    to later quality-refinement stages, not this loader-only step.
    """

    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip()
            if title:
                return title
    return fallback


def load_document(path: Path, root_dir: Path) -> SourceDocument:
    """Load one markdown file and validate it into a SourceDocument.

    The model validation in schemas.py enforces non-empty text and required
    metadata so this stage outputs reliable typed records only.
    """

    raw_text = path.read_text(encoding="utf-8")
    clean_text = raw_text.strip()
    line_count = len(clean_text.splitlines()) if clean_text else 0
    fallback_title = path.stem.replace("_", " ").title()

    return SourceDocument(
        document_id=path.stem,
        source_file=path.name,
        source_path=path.resolve().relative_to(root_dir.resolve()).as_posix(),
        title=extract_title(clean_text, fallback=fallback_title),
        text=clean_text,
        character_count=len(clean_text),
        line_count=line_count,
        synthetic=True,
    )


def load_documents(docs_dir: Path) -> list[SourceDocument]:
    """Load and validate every markdown file in the 02 synthetic docs folder."""

    repo_root = find_repo_root(Path(__file__))
    markdown_files = discover_markdown_files(docs_dir)
    return [load_document(path, repo_root) for path in markdown_files]


def write_loaded_documents(documents: list[SourceDocument], output_path: Path) -> None:
    """Write validated SourceDocument objects to JSON for downstream POCs."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [document.model_dump(mode="json") for document in documents]
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    """CLI entry point for 03a.

    Reads synthetic markdown docs from 02, writes structured JSON in 03a
    outputs, and prints a small human-readable summary.
    """

    script_path = Path(__file__).resolve()
    poc_root = script_path.parents[1]
    repo_root = find_repo_root(script_path)
    docs_dir = repo_root / "pocs" / "02_fake_business_docs" / "data" / "home_services_demo"
    output_path = poc_root / "outputs" / "loaded_documents.json"

    documents = load_documents(docs_dir)
    write_loaded_documents(documents, output_path)

    print(f"Docs directory: {docs_dir}")
    print(f"Markdown files loaded: {len(documents)}")
    print(f"Output path: {output_path}")
    print("Source files:")
    for document in documents:
        print(f"- {document.source_file}")


if __name__ == "__main__":
    main()
