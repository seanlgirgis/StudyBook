import csv
from pathlib import Path

from onedriveclean.staging import stage_batch


def test_stage_batch_manifest(tmp_path: Path) -> None:
    src = tmp_path / "src"
    (src / "Oldies").mkdir(parents=True)
    (src / "a.pdf").write_bytes(b"pdf")
    (src / "b.md").write_text("x", encoding="utf-8")
    (src / "Oldies" / "c.pdf").write_bytes(b"old")

    manifest = stage_batch(
        source=src,
        stage_dir=tmp_path / "stage" / "batch_x",
        batch_name="batch_x",
        source_name="downloads",
        include_globs=["*.pdf", "*.md"],
        exclude_globs=["Oldies/**"],
        project="P",
        category="C",
        suggested_clean_remote_path="FileStore/X",
    )

    rows = list(csv.DictReader(manifest.open("r", encoding="utf-8")))
    assert len(rows) == 2
