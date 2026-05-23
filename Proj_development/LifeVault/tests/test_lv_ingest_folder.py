import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lifevault.lv_ingest_folder import run_lv_ingest_folder


def _make_source(tmp_path: Path) -> Path:
    src = tmp_path / "src"
    (src / "nested").mkdir(parents=True, exist_ok=True)
    (src / "a.txt").write_text("a", encoding="utf-8")
    (src / "nested" / "b.txt").write_text("b", encoding="utf-8")
    return src


def test_default_mode_proposes_only(tmp_path: Path) -> None:
    src = _make_source(tmp_path)
    out = tmp_path / "out"
    result = run_lv_ingest_folder(source_path=src, story="fake", output_root=out, auto_approve_pod=False)

    assert "proposal" in result
    assert "pod" not in result
    assert "next_uc003_command" in result
    assert Path(result["proposal"]["proposal_path"]).exists()


def test_auto_approve_creates_pod(tmp_path: Path) -> None:
    src = _make_source(tmp_path)
    out = tmp_path / "out"
    result = run_lv_ingest_folder(source_path=src, story="fake", output_root=out, auto_approve_pod=True)

    pod = result["pod"]
    pod_path = Path(pod["pod_path"])
    assert pod_path.exists()
    assert (pod_path / "_review.csv").exists()

    with (pod_path / "_review.csv").open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows
    for r in rows:
        assert r["review_decision"] == "needs_review"
        assert r["approved_for_database_index"] == "false"
        assert r["approved_for_vault_publish"] == "false"


def test_no_db_or_real_path_touch(tmp_path: Path) -> None:
    src = _make_source(tmp_path)
    out = tmp_path / "out"
    run_lv_ingest_folder(source_path=src, output_root=out, auto_approve_pod=True)
    assert not any(p.name == "lifevault.sqlite" for p in tmp_path.rglob("*"))
    assert "D:\\AI_Lab\\LifeVault" not in str(tmp_path)


def test_source_files_remain_untouched(tmp_path: Path) -> None:
    src = _make_source(tmp_path)
    before = sorted([p.relative_to(src).as_posix() for p in src.rglob("*") if p.is_file()])
    run_lv_ingest_folder(source_path=src, output_root=tmp_path / "out", auto_approve_pod=True)
    after = sorted([p.relative_to(src).as_posix() for p in src.rglob("*") if p.is_file()])
    assert before == after


def test_output_includes_next_command(tmp_path: Path) -> None:
    src = _make_source(tmp_path)
    result = run_lv_ingest_folder(source_path=src, output_root=tmp_path / "out", auto_approve_pod=False)
    assert "python -m lifevault.uc003_cli" in result["next_uc003_command"]