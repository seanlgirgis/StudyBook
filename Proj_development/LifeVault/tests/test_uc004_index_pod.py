import csv
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lifevault.schema_v0 import apply_schema_v0
from lifevault.uc004_index_pod import index_pod_to_database


def _make_db(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        apply_schema_v0(conn)


def _make_fake_pod(tmp_path: Path) -> Path:
    pod = tmp_path / "pod_fake"
    (pod / "original_copies" / "nested").mkdir(parents=True, exist_ok=True)
    (pod / "reports").mkdir(parents=True, exist_ok=True)
    (pod / "original_copies" / "a.txt").write_text("alpha", encoding="utf-8")
    (pod / "original_copies" / "nested" / "b.txt").write_text("beta", encoding="utf-8")

    profile = {
        "schema_version": "1.0",
        "pod_id": "pod_uc001_fake",
        "created_at": "2026-05-23T00:00:00Z",
        "source_path": str(tmp_path / "source"),
        "source_proposal_id": "uc001_fake",
        "source_proposal_path": str(pod / "_source_proposal_snapshot.json"),
        "story": "fake",
        "project": "proj",
        "category": "cat",
        "event_name": "event",
        "suggested_vault_path": "LifeVault/01_Knowledge",
        "pod_status": "created",
        "sensitivity_highest_level": "normal",
        "file_count": 2,
        "copied_file_count": 2,
        "failed_copy_count": 0,
        "duplicate_candidate_count": 1,
        "content_scan_status": "not_performed",
        "database_index_status": "not_indexed",
        "vault_publish_status": "not_published",
        "notes": "",
        "warnings": [],
        "errors": [],
    }
    (pod / "_pod_profile.json").write_text(json.dumps(profile), encoding="utf-8")

    with (pod / "_pod_manifest.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "pod_id",
                "source_relative_path",
                "source_absolute_path",
                "pod_relative_path",
                "pod_absolute_path",
                "filename",
                "extension",
                "size_bytes",
                "modified_time",
                "copied_at",
                "filename_sensitivity_level",
                "filename_sensitivity_reasons",
                "duplicate_name_group_id",
                "copy_status",
                "copy_error",
            ],
        )
        w.writeheader()
        w.writerow(
            {
                "pod_id": "pod_uc001_fake",
                "source_relative_path": "a.txt",
                "source_absolute_path": str(tmp_path / "source" / "a.txt"),
                "pod_relative_path": "original_copies/a.txt",
                "pod_absolute_path": str(pod / "original_copies" / "a.txt"),
                "filename": "a.txt",
                "extension": ".txt",
                "size_bytes": 5,
                "modified_time": "2026-05-23T00:00:00Z",
                "copied_at": "2026-05-23T00:00:00Z",
                "filename_sensitivity_level": "normal",
                "filename_sensitivity_reasons": "no_sensitive_rule_match",
                "duplicate_name_group_id": "dup_name_001",
                "copy_status": "copied",
                "copy_error": "",
            }
        )
        w.writerow(
            {
                "pod_id": "pod_uc001_fake",
                "source_relative_path": "nested/b.txt",
                "source_absolute_path": str(tmp_path / "source" / "nested" / "b.txt"),
                "pod_relative_path": "original_copies/nested/b.txt",
                "pod_absolute_path": str(pod / "original_copies" / "nested" / "b.txt"),
                "filename": "b.txt",
                "extension": ".txt",
                "size_bytes": 4,
                "modified_time": "2026-05-23T00:00:00Z",
                "copied_at": "2026-05-23T00:00:00Z",
                "filename_sensitivity_level": "normal",
                "filename_sensitivity_reasons": "no_sensitive_rule_match",
                "duplicate_name_group_id": "dup_name_001",
                "copy_status": "copied",
                "copy_error": "",
            }
        )

    with (pod / "_review.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "pod_id",
                "pod_relative_path",
                "filename",
                "suggested_sensitivity_level",
                "user_sensitivity_level",
                "review_decision",
                "user_notes",
                "approved_for_database_index",
                "approved_for_vault_publish",
            ],
        )
        w.writeheader()
        w.writerow(
            {
                "pod_id": "pod_uc001_fake",
                "pod_relative_path": "original_copies/a.txt",
                "filename": "a.txt",
                "suggested_sensitivity_level": "normal",
                "user_sensitivity_level": "",
                "review_decision": "needs_review",
                "user_notes": "",
                "approved_for_database_index": "false",
                "approved_for_vault_publish": "false",
            }
        )
        w.writerow(
            {
                "pod_id": "pod_uc001_fake",
                "pod_relative_path": "original_copies/nested/b.txt",
                "filename": "b.txt",
                "suggested_sensitivity_level": "normal",
                "user_sensitivity_level": "",
                "review_decision": "needs_review",
                "user_notes": "",
                "approved_for_database_index": "false",
                "approved_for_vault_publish": "false",
            }
        )

    snapshot = {"proposal_id": "uc001_fake", "source_path": str(tmp_path / "source"), "scan_status": "success"}
    (pod / "_source_proposal_snapshot.json").write_text(json.dumps(snapshot), encoding="utf-8")

    (tmp_path / "source" / "nested").mkdir(parents=True, exist_ok=True)
    (tmp_path / "source" / "a.txt").write_text("alpha", encoding="utf-8")
    (tmp_path / "source" / "nested" / "b.txt").write_text("beta", encoding="utf-8")

    return pod


def test_dry_run_writes_no_rows(tmp_path: Path) -> None:
    pod = _make_fake_pod(tmp_path)
    db = tmp_path / "db.sqlite"
    _make_db(db)

    out = index_pod_to_database(pod, db, dry_run=True)
    assert out["mode"] == "dry_run"

    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM pods").fetchone()[0] == 0


def test_approved_index_writes_expected_rows_and_sha(tmp_path: Path) -> None:
    pod = _make_fake_pod(tmp_path)
    db = tmp_path / "db.sqlite"
    _make_db(db)

    out = index_pod_to_database(pod, db, approved=True)
    assert out["mode"] == "approved"

    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM pods").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM files").fetchone()[0] == 2
        assert conn.execute("SELECT COUNT(*) FROM file_instances").fetchone()[0] == 2
        assert conn.execute("SELECT COUNT(*) FROM review_decisions").fetchone()[0] == 2
        assert conn.execute("SELECT COUNT(*) FROM duplicate_groups").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM duplicate_group_members").fetchone()[0] == 2
        sha_rows = conn.execute("SELECT sha256 FROM files").fetchall()
        assert all(len(r[0]) == 64 for r in sha_rows)
        dup_note = conn.execute(
            "SELECT note FROM duplicate_groups WHERE duplicate_group_id = 'dup_name_001'"
        ).fetchone()[0]
        assert "instance_count=2" in dup_note
        assert "unique_file_count=2" in dup_note


def test_duplicate_pod_refused(tmp_path: Path) -> None:
    pod = _make_fake_pod(tmp_path)
    db = tmp_path / "db.sqlite"
    _make_db(db)
    index_pod_to_database(pod, db, approved=True)
    with pytest.raises(ValueError):
        index_pod_to_database(pod, db, approved=True)


def test_missing_manifest_fails(tmp_path: Path) -> None:
    pod = _make_fake_pod(tmp_path)
    (pod / "_pod_manifest.csv").unlink()
    db = tmp_path / "db.sqlite"
    _make_db(db)
    with pytest.raises(FileNotFoundError):
        index_pod_to_database(pod, db, dry_run=True)


def test_missing_review_fails(tmp_path: Path) -> None:
    pod = _make_fake_pod(tmp_path)
    (pod / "_review.csv").unlink()
    db = tmp_path / "db.sqlite"
    _make_db(db)
    with pytest.raises(FileNotFoundError):
        index_pod_to_database(pod, db, dry_run=True)


def test_invalid_db_without_migration_fails(tmp_path: Path) -> None:
    pod = _make_fake_pod(tmp_path)
    db = tmp_path / "db.sqlite"
    with sqlite3.connect(db):
        pass
    with pytest.raises(ValueError):
        index_pod_to_database(pod, db, dry_run=True)


def test_real_db_path_rejected(tmp_path: Path) -> None:
    pod = _make_fake_pod(tmp_path)
    with pytest.raises(ValueError):
        index_pod_to_database(pod, Path(r"D:\AI_Lab\LifeVault\db\lifevault.sqlite"), dry_run=True)


def test_real_db_path_accepts_confirmation_in_dry_run_without_touching_real_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    pod = _make_fake_pod(tmp_path)
    db = tmp_path / "db.sqlite"
    _make_db(db)

    import lifevault.uc004_index_pod as uc004_mod

    monkeypatch.setattr(uc004_mod, "REAL_DB_PATH", db)
    out = uc004_mod.index_pod_to_database(pod, db, dry_run=True, real_db_confirm=True)
    assert out["mode"] == "dry_run"


def test_no_real_path_touch_and_no_db_created_elsewhere(tmp_path: Path) -> None:
    pod = _make_fake_pod(tmp_path)
    db = tmp_path / "db.sqlite"
    _make_db(db)
    index_pod_to_database(pod, db, dry_run=True)
    assert "D:\\AI_Lab\\LifeVault" not in str(tmp_path)
