from pathlib import Path

from onedriveclean.intake import analyze_source_folder, save_proposal


def test_analyze_source_folder_and_save(tmp_path: Path) -> None:
    src = tmp_path / "apod"
    src.mkdir()
    (src / "a.pdf").write_bytes(b"123")
    (src / "a (copy).pdf").write_bytes(b"123")
    (src / "notes.md").write_text("x", encoding="utf-8")

    proposal = analyze_source_folder(src)
    assert proposal.file_count == 3
    assert proposal.suggested_pod_name == "apod"
    assert proposal.confidence in {"low", "medium"}

    out = save_proposal(tmp_path / "proposals", proposal)
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "suggested_vault_path" in text
