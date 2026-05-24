import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lifevault.schema_v0 import apply_schema_v0
from lifevault.uc006_review import update_review_item
from lifevault.uc009_cleanup_quarantine import cleanup_to_quarantine


def _seed(db: Path, pod_id: str, pod_root: Path) -> None:
    now = "2026-05-23T00:00:00Z"
    (pod_root / "original_copies").mkdir(parents=True, exist_ok=True)
    files = [
        ("fkeep", "keep.pdf", "normal"),
        ("fdup", "dup_skip.pdf", "normal"),
        ("fskip", "skip.pdf", "normal"),
        ("farch", "archive.pdf", "normal"),
        ("fneed", "needs.pdf", "normal"),
        ("fsens", "sens.pdf", "sensitive"),
    ]
    for _, name, _ in files:
        (pod_root / "original_copies" / name).write_text(name, encoding="utf-8")
    with sqlite3.connect(db) as conn:
        apply_schema_v0(conn)
        conn.execute("INSERT INTO sources(source_id,source_type,source_name,root_ref,is_active,created_at) VALUES(?,?,?,?,1,?)", ("src1", "local_folder", "source", str(pod_root), now))
        conn.execute("INSERT INTO pods(pod_id,source_id,pod_name,event_name,pod_status,story_context,intake_notes,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (pod_id, "src1", pod_id, "event", "reviewed", "story", "", "normal", "warm", now, now))
        for i, (fid, name, sens) in enumerate(files, 1):
            conn.execute("INSERT INTO files(file_id,sha256,hash_algo,filename,ext,size_bytes,file_status,review_status,publish_status,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (fid, str(i)*64, "sha256", name, ".pdf", 1, "copied_to_pod", "needs_review", "not_published", sens, "warm", now, now))
            conn.execute("INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,path_is_absolute,path_platform,observed_at,is_current,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (f"inst{i}", fid, "src1", pod_id, "pod_copy", str(pod_root / "original_copies" / name), 1, "windows", now, 1, now, now))
        conn.execute("INSERT INTO duplicate_groups(duplicate_group_id,group_method,group_status,created_at,updated_at) VALUES(?,?,?,?,?)", ("dup_g1", "duplicate_name_candidate", "open", now, now))
        conn.execute("INSERT INTO duplicate_group_members(duplicate_group_id,file_id,member_role,is_canonical_candidate,created_at) VALUES(?,?,?,?,?)", ("dup_g1", "fkeep", "candidate", 1, now))
        conn.execute("INSERT INTO duplicate_group_members(duplicate_group_id,file_id,member_role,is_canonical_candidate,created_at) VALUES(?,?,?,?,?)", ("dup_g1", "fdup", "candidate", 0, now))
    update_review_item(db, pod_id, str(pod_root / "original_copies" / "keep.pdf"), decision="duplicate_keep", approved_for_vault_publish=True, approved_update=True, real_db_confirm=True)
    update_review_item(db, pod_id, str(pod_root / "original_copies" / "dup_skip.pdf"), decision="duplicate_skip", approved_update=True, real_db_confirm=True)
    update_review_item(db, pod_id, str(pod_root / "original_copies" / "skip.pdf"), decision="skip", approved_update=True, real_db_confirm=True)
    update_review_item(db, pod_id, str(pod_root / "original_copies" / "archive.pdf"), decision="archive", approved_update=True, real_db_confirm=True)
    update_review_item(db, pod_id, str(pod_root / "original_copies" / "sens.pdf"), decision="skip", approved_update=True, real_db_confirm=True)
    with sqlite3.connect(db) as conn:
        conn.execute("UPDATE files SET publish_status='verified' WHERE file_id='fkeep'")
        conn.commit()


def test_dry_run_moves_nothing(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_root = tmp_path / "pod"
    qroot = tmp_path / "q"
    _seed(db, "pod1", pod_root)
    out = cleanup_to_quarantine("pod1", db, qroot, dry_run=True)
    assert out["mode"] == "dry_run"
    assert not (qroot / "pod1").exists()
    assert (pod_root / "original_copies" / "dup_skip.pdf").exists()


def test_approved_cleanup_moves_eligible_and_writes_manifest(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_root = tmp_path / "pod"
    qroot = tmp_path / "q"
    _seed(db, "pod1", pod_root)
    out = cleanup_to_quarantine("pod1", db, qroot, approved_cleanup=True)
    assert out["moved_count"] >= 2
    assert (qroot / "pod1" / "_cleanup_manifest.csv").exists()
    assert not (qroot / "pod1" / "keep.pdf").exists()
    assert not (pod_root / "original_copies" / "dup_skip.pdf").exists()
    assert (qroot / "pod1" / "dup_skip.pdf").exists()
    assert (pod_root / "original_copies" / "needs.pdf").exists()
    assert (pod_root / "original_copies" / "sens.pdf").exists()
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM audit_log WHERE event_type='uc009_cleanup_quarantine'").fetchone()[0] == 1


def test_include_sensitive_allows_sensitive_candidate(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_root = tmp_path / "pod"
    qroot = tmp_path / "q"
    _seed(db, "pod1", pod_root)
    cleanup_to_quarantine("pod1", db, qroot, approved_cleanup=True, include_sensitive=True)
    assert (qroot / "pod1" / "sens.pdf").exists()


def test_missing_verification_blocks_duplicate_skip(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_root = tmp_path / "pod"
    qroot = tmp_path / "q"
    _seed(db, "pod1", pod_root)
    with sqlite3.connect(db) as conn:
        conn.execute("UPDATE files SET publish_status='not_published' WHERE file_id='fkeep'")
        conn.commit()
    out = cleanup_to_quarantine("pod1", db, qroot, approved_cleanup=True)
    assert (pod_root / "original_copies" / "dup_skip.pdf").exists()
    assert out["candidate_count"] >= 1


def test_overwrite_refused(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_root = tmp_path / "pod"
    qroot = tmp_path / "q"
    _seed(db, "pod1", pod_root)
    (qroot / "pod1").mkdir(parents=True, exist_ok=True)
    (qroot / "pod1" / "dup_skip.pdf").write_text("existing", encoding="utf-8")
    out = cleanup_to_quarantine("pod1", db, qroot, approved_cleanup=True)
    assert out["candidate_count"] >= 1
    assert (pod_root / "original_copies" / "dup_skip.pdf").exists()


def test_real_db_guard_exists(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db = tmp_path / "db.sqlite"
    pod_root = tmp_path / "pod"
    qroot = tmp_path / "q"
    _seed(db, "pod1", pod_root)
    import lifevault.uc009_cleanup_quarantine as mod

    monkeypatch.setattr(mod, "REAL_DB_PATH", db)
    with pytest.raises(ValueError):
        mod.cleanup_to_quarantine("pod1", db, qroot, dry_run=True, real_db_confirm=False)


def test_duplicate_skip_with_verified_keep_peer_is_single_candidate_in_dry_run(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_root = tmp_path / "pod"
    qroot = tmp_path / "q"
    _seed(db, "pod1", pod_root)
    out = cleanup_to_quarantine("pod1", db, qroot, dry_run=True)
    dup = [r for r in out["items"] if r["decision"] == "duplicate_skip"]
    assert len(dup) == 1
    assert dup[0]["filename"] == "dup_skip.pdf"
    assert all(r["filename"] != "keep.pdf" for r in out["items"])


def test_duplicate_skip_with_no_verified_peer_has_no_duplicate_candidate(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_root = tmp_path / "pod"
    qroot = tmp_path / "q"
    _seed(db, "pod1", pod_root)
    with sqlite3.connect(db) as conn:
        conn.execute("UPDATE files SET publish_status='published' WHERE file_id='fkeep'")
        conn.commit()
    out = cleanup_to_quarantine("pod1", db, qroot, dry_run=True)
    assert not any(r["decision"] == "duplicate_skip" for r in out["items"])
