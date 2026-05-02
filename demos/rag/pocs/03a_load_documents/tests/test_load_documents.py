from __future__ import annotations

import json
import sys
from pathlib import Path

POC_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = POC_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from load_documents import discover_markdown_files, load_documents, write_loaded_documents  # noqa: E402
from schemas import SourceDocument  # noqa: E402


REPO_ROOT = POC_ROOT.parents[1]
DOCS_DIR = REPO_ROOT / "pocs" / "02_fake_business_docs" / "data" / "home_services_demo"


def test_discover_markdown_files() -> None:
    files = discover_markdown_files(DOCS_DIR)
    assert files
    assert len(files) == 16
    assert all(path.suffix == ".md" for path in files)


def test_load_documents_validates_source_documents() -> None:
    documents = load_documents(DOCS_DIR)
    assert len(documents) == 16
    assert all(isinstance(document, SourceDocument) for document in documents)
    assert all(document.text.strip() for document in documents)
    assert all(document.character_count > 0 for document in documents)
    assert all(document.line_count > 0 for document in documents)
    assert all(document.source_file.endswith(".md") for document in documents)
    assert all(document.synthetic is True for document in documents)


def test_write_loaded_documents_json_round_trip(tmp_path: Path) -> None:
    documents = load_documents(DOCS_DIR)
    output_path = tmp_path / "loaded_documents.json"
    write_loaded_documents(documents, output_path)

    assert output_path.exists()
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert isinstance(payload, list)
    assert len(payload) == 16
    assert all(item["source_file"].endswith(".md") for item in payload)
