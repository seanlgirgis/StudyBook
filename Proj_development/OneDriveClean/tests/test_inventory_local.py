from pathlib import Path

from onedriveclean.inventory_local import guess_category, scan_folder


def test_guess_category() -> None:
    assert guess_category(".jpg") == "photo"
    assert guess_category(".mp4") == "video"
    assert guess_category(".pdf") == "document"
    assert guess_category(".xlsx") == "spreadsheet"
    assert guess_category(".pptx") == "presentation"
    assert guess_category(".zip") == "archive"
    assert guess_category(".py") == "code"
    assert guess_category(".wav") == "audio"
    assert guess_category(".unknown") == "other"


def test_scan_folder_rows(tmp_path: Path) -> None:
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "photo.jpg").write_bytes(b"1")
    (tmp_path / "a" / "doc.pdf").write_bytes(b"12")

    rows = scan_folder(tmp_path)
    assert len(rows) == 2
    names = {row["filename"] for row in rows}
    assert names == {"photo.jpg", "doc.pdf"}
    assert all("relative_path" in row for row in rows)
