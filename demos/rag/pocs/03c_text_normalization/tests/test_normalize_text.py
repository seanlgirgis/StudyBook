from __future__ import annotations

import json
import sys
from pathlib import Path

POC_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = POC_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from normalize_text import (  # noqa: E402
    get_default_paths,
    load_chunks,
    normalize_text,
    run_normalization_pipeline,
)


def test_normalize_text_lowercases_text() -> None:
    assert normalize_text("Hello HVAC TEAM") == "hello hvac team"


def test_repeated_whitespace_is_collapsed() -> None:
    assert normalize_text("alpha\n\n\tbeta   gamma") == "alpha beta gamma"


def test_smart_punctuation_and_long_dashes_are_handled() -> None:
    raw = "\u201cTune-up\u201d\u2014it\u2019s needed"
    assert normalize_text(raw) == "tune up it s needed"


def test_ac_variants_normalize_to_ac() -> None:
    assert normalize_text("A/C and a/c service") == "ac and ac service"


def test_air_conditioning_hyphen_variant_normalizes() -> None:
    assert normalize_text("air-conditioning check") == "air conditioning check"


def test_pipeline_preserves_original_text_and_chunk_ids() -> None:
    input_path, _ = get_default_paths()
    source_chunks = load_chunks(input_path)
    output_path = POC_ROOT / "outputs" / "normalized_chunks.test.json"

    try:
        input_count, output_count, _, _ = run_normalization_pipeline(input_path=input_path, output_path=output_path)

        assert input_count == len(source_chunks)
        assert output_count == len(source_chunks)

        payload = json.loads(output_path.read_text(encoding="utf-8"))
        assert len(payload) == len(source_chunks)

        source_by_id = {chunk.chunk_id: chunk for chunk in source_chunks}

        for item in payload:
            chunk_id = item["chunk_id"]
            assert chunk_id in source_by_id
            assert item["text"] == source_by_id[chunk_id].text
            assert item["normalized_text"].strip()
            assert item["normalized_character_count"] == len(item["normalized_text"])
    finally:
        if output_path.exists():
            output_path.unlink()
