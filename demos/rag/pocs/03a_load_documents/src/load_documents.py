from __future__ import annotations

import json
from pathlib import Path

from schemas import SourceDocument


def find_repo_root(start_path: Path) -> Path:
    current = start_path.resolve()
    for candidate in [current, *current.parents]:
        expected_docs = candidate / "pocs" / "02_fake_business_docs" / "data" / "home_services_demo"
        if expected_docs.exists():
            return candidate
    raise FileNotFoundError("Could not locate repo root containing pocs/02_fake_business_docs/data/home_services_demo")


def discover_markdown_files(docs_dir: Path) -> list[Path]:
    if not docs_dir.exists():
        raise FileNotFoundError(f"Docs directory not found: {docs_dir}")

    markdown_files = sorted(path for path in docs_dir.glob("*.md") if path.is_file())
    if not markdown_files:
        raise ValueError(f"No markdown files found in: {docs_dir}")

    return markdown_files


def extract_title(markdown_text: str, fallback: str) -> str:
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip()
            if title:
                return title
    return fallback


def load_document(path: Path, root_dir: Path) -> SourceDocument:
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
    repo_root = find_repo_root(Path(__file__))
    markdown_files = discover_markdown_files(docs_dir)
    return [load_document(path, repo_root) for path in markdown_files]


def write_loaded_documents(documents: list[SourceDocument], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [document.model_dump(mode="json") for document in documents]
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
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
