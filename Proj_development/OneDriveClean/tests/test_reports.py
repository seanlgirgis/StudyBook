import csv
from pathlib import Path

from onedriveclean.reports import build_reports


def _read_csv(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_build_reports(tmp_path: Path) -> None:
    batch = tmp_path / "hydrated" / "batch1"
    batch.mkdir(parents=True)
    (batch / "a").mkdir()
    (batch / "b").mkdir()

    (batch / "a" / "report.docx").write_bytes(b"x" * 10)
    (batch / "b" / "report.docx").write_bytes(b"y" * 20)
    (batch / "b" / "video.mp4").write_bytes(b"z" * 200)

    out = tmp_path / "reports" / "batch1"
    paths = build_reports(batch, out, large_file_threshold_bytes=100)

    assert paths["file_inventory"].exists()
    assert paths["extension_summary"].exists()
    assert paths["large_files"].exists()
    assert paths["folder_sizes"].exists()
    assert paths["same_filename_candidates"].exists()

    large_rows = _read_csv(paths["large_files"])
    assert len(large_rows) == 1
    assert large_rows[0]["relative_path"].endswith("video.mp4")

    same_name = _read_csv(paths["same_filename_candidates"])
    assert len(same_name) == 2
    assert all(row["filename"].lower() == "report.docx" for row in same_name)
