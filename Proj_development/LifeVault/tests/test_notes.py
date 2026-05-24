import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lifevault.notes import create_note, search_notes


def test_note_creates_markdown_file_and_frontmatter(tmp_path: Path) -> None:
    out = create_note(
        title="Test LifeVault note",
        story="Testing Notes v0",
        tags="lifevault,notes,test",
        body="This is a searchable markdown note.",
        notes_root=tmp_path,
    )
    p = Path(out["note_path"])
    assert p.exists()
    t = p.read_text(encoding="utf-8")
    assert t.startswith("---\n")
    assert "title: Test LifeVault note" in t
    assert "story: Testing Notes v0" in t
    assert "tags: [lifevault, notes, test]" in t
    assert "This is a searchable markdown note." in t


def test_filename_generated_and_safe(tmp_path: Path) -> None:
    out = create_note("Weird <>:/\\|?* title", "", "", "body", tmp_path)
    name = Path(out["note_path"]).name
    assert name.startswith("note_")
    assert name.endswith(".md")
    for c in '<>:"/\\|?*':
        assert c not in name


def test_search_finds_title_tag_story_body(tmp_path: Path) -> None:
    create_note(
        title="My Searchable Title",
        story="Story needle",
        tags="alpha,beta",
        body="Body needle text",
        notes_root=tmp_path,
    )
    assert any("title" in r["match_type"] for r in search_notes(tmp_path, "searchable"))
    assert any("tag" in r["match_type"] for r in search_notes(tmp_path, "beta"))
    assert any("story" in r["match_type"] for r in search_notes(tmp_path, "needle"))
    assert any("body" in r["match_type"] for r in search_notes(tmp_path, "body needle"))


def test_no_overwrite_collision(tmp_path: Path) -> None:
    out1 = create_note("same", "", "", "a", tmp_path)
    out2 = create_note("same", "", "", "b", tmp_path)
    assert out1["note_path"] != out2["note_path"]


def test_no_real_ai_lab_path_touched(tmp_path: Path) -> None:
    out = create_note("tmp path only", "", "", "x", tmp_path)
    assert "D:\\AI_Lab\\LifeVault" not in out["note_path"]
