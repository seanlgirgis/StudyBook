import csv
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lifevault.schema_v0 import apply_schema_v0
from lifevault.uc008_verify_publish import verify_local_publish


def _seed(db: Path, pod_id: str, source_file: Path) -> None:
    now = "2026-05-23T00:00:00Z"
    with sqlite3.connect(db) as conn:
        apply_schema_v0(conn)
        conn.execute("INSERT INTO sources(source_id,source_type,source_name,root_ref,is_active,created_at) VALUES(?,?,?,?,1,?)", ("src1", "local_folder", "source", str(source_file.parent), now))
        conn.execute("INSERT INTO pods(pod_id,source_id,pod_name,event_name,pod_status,story_context,intake_notes,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (pod_id, "src1", pod_id, "event", "onboarded_needs_review", "story", "", "normal", "warm", now, now))
        conn.execute("INSERT INTO files(file_id,sha256,hash_algo,filename,ext,size_bytes,file_status,review_status,publish_status,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", ("f1", "a"*64, "sha256", source_file.name, ".pdf", source_file.stat().st_size, "published", "approved", "published", "normal", "warm", now, now))
        conn.execute("INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,path_is_absolute,path_platform,observed_at,is_current,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", ("inst1", "f1", "src1", pod_id, "pod_copy", str(source_file), 1, "windows", now, 1, now, now))


def _write_publish_manifest(vault_pod_dir: Path, pod_id: str, src: Path, dst: Path) -> None:
    vault_pod_dir.mkdir(parents=True, exist_ok=True)
    with (vault_pod_dir / "_publish_manifest.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "pod_id",
                "instance_id",
                "filename",
                "pod_relative_path",
                "source_path",
                "destination_path",
                "copy_status",
                "copy_error",
                "copied_at",
            ],
        )
        w.writeheader()
        w.writerow(
            {
                "pod_id": pod_id,
                "instance_id": "inst1",
                "filename": src.name,
                "pod_relative_path": "original_copies/" + src.name,
                "source_path": str(src),
                "destination_path": str(dst),
                "copy_status": "copied",
                "copy_error": "",
                "copied_at": "2026-05-23T00:00:00Z",
            }
        )


def test_dry_run_writes_no_db_changes(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_id = "pod1"
    src = tmp_path / "src.pdf"
    dst = tmp_path / "vault" / pod_id / "src.pdf"
    src.write_text("abc", encoding="utf-8")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("abc", encoding="utf-8")
    _seed(db, pod_id, src)
    _write_publish_manifest(tmp_path / "vault" / pod_id, pod_id, src, dst)
    before = sqlite3.connect(db).execute("SELECT publish_status FROM files WHERE file_id='f1'").fetchone()[0]
    out = verify_local_publish(pod_id, db, tmp_path / "vault", dry_run=True)
    after = sqlite3.connect(db).execute("SELECT publish_status FROM files WHERE file_id='f1'").fetchone()[0]
    assert out["mode"] == "dry_run"
    assert before == after


def test_approved_verify_marks_verified_and_writes_artifacts(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_id = "pod1"
    src = tmp_path / "src.pdf"
    dst = tmp_path / "vault" / pod_id / "src.pdf"
    src.write_text("abc", encoding="utf-8")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("abc", encoding="utf-8")
    _seed(db, pod_id, src)
    _write_publish_manifest(tmp_path / "vault" / pod_id, pod_id, src, dst)
    out = verify_local_publish(pod_id, db, tmp_path / "vault", approved_verify=True)
    assert out["summary"]["verified_count"] == 1
    assert (tmp_path / "vault" / pod_id / "_verify_manifest.csv").exists()
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT publish_status FROM files WHERE file_id='f1'").fetchone()[0] == "verified"
        assert conn.execute("SELECT COUNT(*) FROM audit_log WHERE event_type='uc008_verify_publish'").fetchone()[0] == 1


def test_size_mismatch_fails(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_id = "pod1"
    src = tmp_path / "src.pdf"
    dst = tmp_path / "vault" / pod_id / "src.pdf"
    src.write_text("abc", encoding="utf-8")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("abcd", encoding="utf-8")
    _seed(db, pod_id, src)
    _write_publish_manifest(tmp_path / "vault" / pod_id, pod_id, src, dst)
    out = verify_local_publish(pod_id, db, tmp_path / "vault", approved_verify=True)
    assert out["summary"]["failed_count"] == 1


def test_hash_mismatch_fails(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_id = "pod1"
    src = tmp_path / "src.pdf"
    dst = tmp_path / "vault" / pod_id / "src.pdf"
    src.write_text("abc", encoding="utf-8")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("xyz", encoding="utf-8")
    _seed(db, pod_id, src)
    _write_publish_manifest(tmp_path / "vault" / pod_id, pod_id, src, dst)
    out = verify_local_publish(pod_id, db, tmp_path / "vault", approved_verify=True)
    assert out["summary"]["failed_count"] == 1


def test_missing_destination_fails(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_id = "pod1"
    src = tmp_path / "src.pdf"
    dst = tmp_path / "vault" / pod_id / "src.pdf"
    src.write_text("abc", encoding="utf-8")
    _seed(db, pod_id, src)
    _write_publish_manifest(tmp_path / "vault" / pod_id, pod_id, src, dst)
    out = verify_local_publish(pod_id, db, tmp_path / "vault", approved_verify=True)
    assert out["summary"]["failed_count"] == 1


def test_missing_source_fails(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    pod_id = "pod1"
    src = tmp_path / "src.pdf"
    dst = tmp_path / "vault" / pod_id / "src.pdf"
    src.write_text("abc", encoding="utf-8")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("abc", encoding="utf-8")
    _seed(db, pod_id, src)
    _write_publish_manifest(tmp_path / "vault" / pod_id, pod_id, src, dst)
    src.unlink()
    out = verify_local_publish(pod_id, db, tmp_path / "vault", approved_verify=True)
    assert out["summary"]["failed_count"] == 1


def test_real_db_guard_exists(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db = tmp_path / "db.sqlite"
    pod_id = "pod1"
    src = tmp_path / "src.pdf"
    dst = tmp_path / "vault" / pod_id / "src.pdf"
    src.write_text("abc", encoding="utf-8")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("abc", encoding="utf-8")
    _seed(db, pod_id, src)
    _write_publish_manifest(tmp_path / "vault" / pod_id, pod_id, src, dst)
    import lifevault.uc008_verify_publish as mod

    monkeypatch.setattr(mod, "REAL_DB_PATH", db)
    with pytest.raises(ValueError):
        mod.verify_local_publish(pod_id, db, tmp_path / "vault", dry_run=True, real_db_confirm=False)
