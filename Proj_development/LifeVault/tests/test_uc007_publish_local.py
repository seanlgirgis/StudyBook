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
from lifevault.uc007_publish_local import publish_to_local_vault


def _seed(db: Path, pod_root: Path) -> None:
    pod_id = "pod1"
    (pod_root / "original_copies").mkdir(parents=True, exist_ok=True)
    (pod_root / "original_copies" / "ready.pdf").write_text("r", encoding="utf-8")
    (pod_root / "original_copies" / "dup_skip.pdf").write_text("d", encoding="utf-8")
    (pod_root / "original_copies" / "needs_review.pdf").write_text("n", encoding="utf-8")
    (pod_root / "original_copies" / "sens.pdf").write_text("s", encoding="utf-8")
    now = "2026-05-23T00:00:00Z"
    with sqlite3.connect(db) as conn:
        apply_schema_v0(conn)
        conn.execute("INSERT INTO sources(source_id,source_type,source_name,root_ref,is_active,created_at) VALUES(?,?,?,?,1,?)", ("src1", "local_folder", "source", str(pod_root), now))
        conn.execute("INSERT INTO pods(pod_id,source_id,pod_name,event_name,pod_status,story_context,intake_notes,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (pod_id, "src1", pod_id, "event", "onboarded_needs_review", "story", "", "normal", "warm", now, now))
        files = [
            ("f1", "a"*64, "ready.pdf", "normal", "original_copies/ready.pdf"),
            ("f2", "b"*64, "dup_skip.pdf", "normal", "original_copies/dup_skip.pdf"),
            ("f3", "c"*64, "needs_review.pdf", "normal", "original_copies/needs_review.pdf"),
            ("f4", "d"*64, "sens.pdf", "highly_sensitive", "original_copies/sens.pdf"),
        ]
        for i, (fid, sha, name, sens, rel) in enumerate(files, 1):
            conn.execute("INSERT INTO files(file_id,sha256,hash_algo,filename,ext,size_bytes,file_status,review_status,publish_status,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (fid, sha, "sha256", name, ".pdf", 1, "copied_to_pod", "needs_review", "not_published", sens, "warm", now, now))
            conn.execute("INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,path_is_absolute,path_platform,observed_at,is_current,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (f"inst{i}", fid, "src1", pod_id, "pod_copy", str((pod_root / rel)), 1, "windows", now, 1, now, now))
        conn.execute("INSERT INTO duplicate_groups(duplicate_group_id,group_method,group_status,created_at,updated_at) VALUES(?,?,?,?,?)", ("dup1", "duplicate_name_candidate", "open", now, now))
        conn.execute("INSERT INTO duplicate_group_members(duplicate_group_id,file_id,member_role,is_canonical_candidate,created_at) VALUES(?,?,?,?,?)", ("dup1", "f2", "candidate", 0, now))

    update_review_item(db, "pod1", str((pod_root / "original_copies/ready.pdf")), decision="keep", approved_for_vault_publish=True, approved_update=True, real_db_confirm=True)
    update_review_item(db, "pod1", str((pod_root / "original_copies/dup_skip.pdf")), decision="duplicate_skip", approved_update=True, real_db_confirm=True)
    update_review_item(db, "pod1", str((pod_root / "original_copies/sens.pdf")), decision="keep", approved_for_vault_publish=False, approved_update=True, real_db_confirm=True)


def test_dry_run_copies_nothing(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_root = tmp_path / "pod"
    vault = tmp_path / "vault"
    _seed(db, pod_root)
    out = publish_to_local_vault("pod1", db, vault, dry_run=True)
    assert out["mode"] == "dry_run"
    assert not (vault / "pod1").exists()


def test_approved_publish_only_ready_to_publish(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_root = tmp_path / "pod"
    vault = tmp_path / "vault"
    _seed(db, pod_root)
    out = publish_to_local_vault("pod1", db, vault, approved_publish=True)
    assert out["copied_count"] == 1
    assert (vault / "pod1" / "ready.pdf").exists()
    assert not (vault / "pod1" / "dup_skip.pdf").exists()
    assert not (vault / "pod1" / "needs_review.pdf").exists()
    assert not (vault / "pod1" / "sens.pdf").exists()
    assert (vault / "pod1" / "_publish_manifest.csv").exists()
    assert (pod_root / "original_copies" / "ready.pdf").exists()
    with sqlite3.connect(db) as conn:
        statuses = dict(conn.execute("SELECT file_id,publish_status FROM files").fetchall())
        assert statuses["f1"] == "published"
        assert statuses["f2"] == "not_published"
        assert conn.execute("SELECT COUNT(*) FROM audit_log WHERE event_type='uc007_publish_local'").fetchone()[0] == 1


def test_overwrite_refused(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_root = tmp_path / "pod"
    vault = tmp_path / "vault"
    _seed(db, pod_root)
    (vault / "pod1").mkdir(parents=True, exist_ok=True)
    (vault / "pod1" / "ready.pdf").write_text("already", encoding="utf-8")
    out = publish_to_local_vault("pod1", db, vault, approved_publish=True)
    assert out["copied_count"] == 0


def test_real_db_guard_exists(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db = tmp_path / "db.sqlite"
    pod_root = tmp_path / "pod"
    vault = tmp_path / "vault"
    _seed(db, pod_root)
    import lifevault.uc007_publish_local as mod

    monkeypatch.setattr(mod, "REAL_DB_PATH", db)
    with pytest.raises(ValueError):
        mod.publish_to_local_vault("pod1", db, vault, dry_run=True, real_db_confirm=False)
