import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lifevault.notes import create_note, create_note_folder, list_note_folders, search_notes


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


def test_create_note_folder_layout(tmp_path: Path) -> None:
    out = create_note_folder(
        title="LifeVault Planning Notes",
        story="Folder for design notes",
        tags="lifevault,planning,notes",
        notes_root=tmp_path,
    )
    folder = Path(out["folder_path"])
    assert folder.exists()
    assert (folder / "_folder_manifest.json").exists()
    assert (folder / "README.md").exists()
    assert (folder / "notes").exists()
    readme = (folder / "README.md").read_text(encoding="utf-8")
    assert "vault_item_type: note_folder" in readme


def test_create_note_inside_folder(tmp_path: Path) -> None:
    folder = create_note_folder("Folder A", "", "x", tmp_path)
    note = create_note(
        title="First folder note",
        story="Testing note inside note folder",
        tags="lifevault,folder-note",
        body="This note lives inside a note folder.",
        notes_root=tmp_path,
        note_folder_path=folder["folder_path"],
    )
    p = Path(note["note_path"])
    assert p.exists()
    assert p.parent.name == "notes"


def test_search_finds_folder_note_and_parent(tmp_path: Path) -> None:
    folder = create_note_folder("Parent Folder", "Story", "folder", tmp_path)
    create_note(
        title="Nested Note",
        story="Inside folder story",
        tags="nested,tag",
        body="Body inside folder note",
        notes_root=tmp_path,
        note_folder_path=folder["folder_path"],
    )
    rows = search_notes(tmp_path, "inside folder")
    assert rows
    assert any(r.get("parent_note_folder") == folder["folder_path"] for r in rows)


def test_list_folders_returns_note_count(tmp_path: Path) -> None:
    folder = create_note_folder("Folder List", "Story", "a,b", tmp_path)
    create_note("N1", "", "", "x", tmp_path, note_folder_path=folder["folder_path"])
    create_note("N2", "", "", "x", tmp_path, note_folder_path=folder["folder_path"])
    rows = list_note_folders(tmp_path)
    assert len(rows) == 1
    assert rows[0]["folder_title"] == "Folder List"
    assert rows[0]["note_count"] == 2


def test_weird_folder_title_sanitized(tmp_path: Path) -> None:
    out = create_note_folder("Weird <>:/\\|?* folder", "", "", tmp_path)
    name = Path(out["folder_path"]).name
    assert name.startswith("note_folder_")
    for c in '<>:"/\\|?*':
        assert c not in name
