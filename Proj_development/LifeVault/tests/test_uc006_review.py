import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lifevault.schema_v0 import apply_schema_v0
from lifevault.uc006_review import (
    list_duplicate_items,
    list_publish_readiness,
    list_review_items,
    update_review_item,
)


def _seed_uc006_db(db: Path) -> None:
    with sqlite3.connect(db) as conn:
        apply_schema_v0(conn)
        now = "2026-05-23T00:00:00Z"
        conn.execute(
            "INSERT INTO sources(source_id,source_type,source_name,root_ref,is_active,created_at) VALUES(?,?,?,?,1,?)",
            ("src1", "local_folder", "source", "C:/fake", now),
        )
        conn.execute(
            "INSERT INTO pods(pod_id,source_id,pod_name,event_name,pod_status,story_context,intake_notes,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            ("pod1", "src1", "pod1", "event", "onboarded_needs_review", "story", "", "normal", "warm", now, now),
        )
        conn.execute(
            "INSERT INTO files(file_id,sha256,hash_algo,filename,ext,size_bytes,file_status,review_status,publish_status,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("file_shared", "a" * 64, "sha256", "cover_letter.pdf", ".pdf", 10, "copied_to_pod", "needs_review", "not_published", "normal", "warm", now, now),
        )
        conn.execute(
            "INSERT INTO files(file_id,sha256,hash_algo,filename,ext,size_bytes,file_status,review_status,publish_status,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("file2", "b" * 64, "sha256", "W4.pdf", ".pdf", 20, "copied_to_pod", "needs_review", "not_published", "highly_sensitive", "warm", now, now),
        )
        conn.execute(
            "INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,path_is_absolute,path_platform,observed_at,is_current,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            ("inst1", "file_shared", "src1", "pod1", "pod_copy", "original_copies/cover_letter.pdf", 0, "windows", now, 1, now, now),
        )
        conn.execute(
            "INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,path_is_absolute,path_platform,observed_at,is_current,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            ("inst2", "file_shared", "src1", "pod1", "pod_copy", "original_copies/cover_letter (1).pdf", 0, "windows", now, 1, now, now),
        )
        conn.execute(
            "INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,path_is_absolute,path_platform,observed_at,is_current,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            ("inst3", "file2", "src1", "pod1", "pod_copy", "original_copies/W4.pdf", 0, "windows", now, 1, now, now),
        )
        conn.execute(
            "INSERT INTO duplicate_groups(duplicate_group_id,group_method,group_status,created_at,updated_at) VALUES(?,?,?,?,?)",
            ("dup1", "duplicate_name_candidate", "open", now, now),
        )
        conn.execute(
            "INSERT INTO duplicate_group_members(duplicate_group_id,file_id,member_role,is_canonical_candidate,created_at) VALUES(?,?,?,?,?)",
            ("dup1", "file_shared", "candidate", 0, now),
        )


def test_list_items(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    _seed_uc006_db(db)
    rows = list_review_items(db, "pod1")
    assert len(rows) == 3


def test_list_duplicates(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    _seed_uc006_db(db)
    rows = list_duplicate_items(db, "pod1")
    assert len(rows) == 2
    assert all(r["duplicate_group_id"] == "dup1" for r in rows)


def test_update_keep_and_duplicate_decisions_are_instance_aware(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    _seed_uc006_db(db)
    update_review_item(
        db,
        "pod1",
        "original_copies/cover_letter.pdf",
        decision="duplicate_keep",
        approved_update=True,
        real_db_confirm=True,
    )
    update_review_item(
        db,
        "pod1",
        "original_copies/cover_letter (1).pdf",
        decision="duplicate_skip",
        approved_update=True,
        real_db_confirm=True,
    )
    rows = list_duplicate_items(db, "pod1")
    decisions = {r["pod_relative_path"]: r["decision"] for r in rows}
    assert decisions["original_copies/cover_letter.pdf"] == "duplicate_keep"
    assert decisions["original_copies/cover_letter (1).pdf"] == "duplicate_skip"


def test_publish_approval_false_default_and_explicit_update(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    _seed_uc006_db(db)
    update_review_item(
        db,
        "pod1",
        "original_copies/W4.pdf",
        decision="keep",
        approved_for_vault_publish=False,
        approved_update=True,
        real_db_confirm=True,
    )
    with sqlite3.connect(db) as conn:
        status = conn.execute("SELECT publish_status FROM files WHERE file_id = 'file2'").fetchone()[0]
    assert status == "not_published"


def test_approval_flag_required_for_write(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    _seed_uc006_db(db)
    with pytest.raises(ValueError):
        update_review_item(
            db,
            "pod1",
            "original_copies/W4.pdf",
            decision="keep",
            approved_update=False,
            real_db_confirm=True,
        )


def test_real_db_guard_exists(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db = tmp_path / "db.sqlite"
    _seed_uc006_db(db)
    import lifevault.uc006_review as mod

    monkeypatch.setattr(mod, "REAL_DB_PATH", db)
    with pytest.raises(ValueError):
        mod.update_review_item(
            db,
            "pod1",
            "original_copies/W4.pdf",
            decision="keep",
            approved_update=True,
            real_db_confirm=False,
        )


def test_publish_readiness_classification_and_counts(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    _seed_uc006_db(db)

    update_review_item(
        db,
        "pod1",
        "original_copies/cover_letter.pdf",
        decision="duplicate_keep",
        approved_for_vault_publish=True,
        approved_update=True,
        real_db_confirm=True,
    )
    update_review_item(
        db,
        "pod1",
        "original_copies/cover_letter (1).pdf",
        decision="duplicate_skip",
        approved_update=True,
        real_db_confirm=True,
    )
    update_review_item(
        db,
        "pod1",
        "original_copies/W4.pdf",
        decision="keep",
        approved_for_vault_publish=False,
        approved_update=True,
        real_db_confirm=True,
    )
    with sqlite3.connect(db) as conn:
        now = "2026-05-23T01:00:00Z"
        conn.execute(
            "INSERT INTO files(file_id,sha256,hash_algo,filename,ext,size_bytes,file_status,review_status,publish_status,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("file3", "c" * 64, "sha256", "normal_keep.pdf", ".pdf", 12, "copied_to_pod", "needs_review", "not_published", "normal", "warm", now, now),
        )
        conn.execute(
            "INSERT INTO files(file_id,sha256,hash_algo,filename,ext,size_bytes,file_status,review_status,publish_status,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("file4", "d" * 64, "sha256", "skip_me.pdf", ".pdf", 12, "copied_to_pod", "needs_review", "not_published", "normal", "warm", now, now),
        )
        conn.execute(
            "INSERT INTO files(file_id,sha256,hash_algo,filename,ext,size_bytes,file_status,review_status,publish_status,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("file5", "e" * 64, "sha256", "archive_me.pdf", ".pdf", 12, "copied_to_pod", "needs_review", "not_published", "normal", "warm", now, now),
        )
        conn.execute(
            "INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,path_is_absolute,path_platform,observed_at,is_current,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            ("inst4", "file3", "src1", "pod1", "pod_copy", "original_copies/normal_keep.pdf", 0, "windows", now, 1, now, now),
        )
        conn.execute(
            "INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,path_is_absolute,path_platform,observed_at,is_current,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            ("inst5", "file4", "src1", "pod1", "pod_copy", "original_copies/skip_me.pdf", 0, "windows", now, 1, now, now),
        )
        conn.execute(
            "INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,path_is_absolute,path_platform,observed_at,is_current,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            ("inst6", "file5", "src1", "pod1", "pod_copy", "original_copies/archive_me.pdf", 0, "windows", now, 1, now, now),
        )
        conn.commit()

    update_review_item(
        db,
        "pod1",
        "original_copies/normal_keep.pdf",
        decision="keep",
        approved_for_vault_publish=False,
        approved_update=True,
        real_db_confirm=True,
    )
    update_review_item(
        db,
        "pod1",
        "original_copies/skip_me.pdf",
        decision="skip",
        approved_update=True,
        real_db_confirm=True,
    )
    update_review_item(
        db,
        "pod1",
        "original_copies/archive_me.pdf",
        decision="archive",
        approved_update=True,
        real_db_confirm=True,
    )

    before = sqlite3.connect(db).execute("SELECT COUNT(*) FROM review_decisions").fetchone()[0]
    out = list_publish_readiness(db, "pod1")
    after = sqlite3.connect(db).execute("SELECT COUNT(*) FROM review_decisions").fetchone()[0]
    assert before == after

    by_path = {r["pod_relative_path"]: r for r in out["items"]}
    assert by_path["original_copies/cover_letter.pdf"]["readiness_status"] == "ready_to_publish"
    assert by_path["original_copies/cover_letter (1).pdf"]["readiness_status"] == "blocked_duplicate_skip"
    assert by_path["original_copies/W4.pdf"]["readiness_status"] == "blocked_sensitive_review"
    assert by_path["original_copies/normal_keep.pdf"]["readiness_status"] == "blocked_not_approved"
    assert by_path["original_copies/skip_me.pdf"]["readiness_status"] == "blocked_skip"
    assert by_path["original_copies/archive_me.pdf"]["readiness_status"] == "blocked_archive"
    assert out["summary"]["total_items"] == len(out["items"])
    assert out["summary"]["ready_to_publish_count"] == 1
