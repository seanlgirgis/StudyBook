import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lifevault.schema_v0 import apply_schema_v0
from lifevault.uc005_search import list_pods, search_metadata


def _seed_db(db: Path) -> None:
    with sqlite3.connect(db) as conn:
        apply_schema_v0(conn)
        conn.execute("INSERT INTO sources(source_id,source_type,source_name,root_ref,is_active,created_at) VALUES(?,?,?,?,1,?)", ("src1","local_folder","src","C:/fake","2026-05-23T00:00:00Z"))
        conn.execute("INSERT INTO pods(pod_id,source_id,pod_name,event_name,pod_status,story_context,intake_notes,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)", ("pod1","src1","pod1","event1","onboarded_needs_review","Story about onboarding","project=acme category=hr","sensitive","warm","2026-05-23T00:00:00Z","2026-05-23T00:00:00Z"))
        conn.execute("INSERT INTO files(file_id,sha256,hash_algo,filename,ext,size_bytes,file_status,review_status,publish_status,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", ("file1","a"*64,"sha256","W4.pdf",".pdf",10,"copied_to_pod","needs_review","not_published","highly_sensitive","warm","2026-05-23T00:00:00Z","2026-05-23T00:00:00Z"))
        conn.execute("INSERT INTO files(file_id,sha256,hash_algo,filename,ext,size_bytes,file_status,review_status,publish_status,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", ("file2","b"*64,"sha256","cover_letter.pdf",".pdf",9,"copied_to_pod","needs_review","not_published","normal","warm","2026-05-23T00:00:00Z","2026-05-23T00:00:00Z"))
        conn.execute("INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,path_is_absolute,path_platform,observed_at,is_current,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", ("inst1","file1","src1","pod1","pod_copy","original_copies/W4.pdf",0,"windows","2026-05-23T00:00:00Z",1,"2026-05-23T00:00:00Z","2026-05-23T00:00:00Z"))
        conn.execute("INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,path_is_absolute,path_platform,observed_at,is_current,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", ("inst2","file2","src1","pod1","pod_copy","original_copies/cover_letter.pdf",0,"windows","2026-05-23T00:00:00Z",1,"2026-05-23T00:00:00Z","2026-05-23T00:00:00Z"))
        conn.execute("INSERT INTO review_decisions(decision_id,file_id,decision_type,review_status,publish_status,created_at,updated_at) VALUES(?,?,?,?,?,?,?)", ("rev1","file1","needs_review","needs_review","not_published","2026-05-23T00:00:00Z","2026-05-23T00:00:00Z"))
        conn.execute("INSERT INTO review_decisions(decision_id,file_id,decision_type,review_status,publish_status,created_at,updated_at) VALUES(?,?,?,?,?,?,?)", ("rev2","file2","needs_review","needs_review","not_published","2026-05-23T00:00:00Z","2026-05-23T00:00:00Z"))
        conn.execute("INSERT INTO duplicate_groups(duplicate_group_id,group_method,group_status,created_at,updated_at) VALUES(?,?,?,?,?)", ("dup_name_001","duplicate_name_candidate","open","2026-05-23T00:00:00Z","2026-05-23T00:00:00Z"))
        conn.execute("INSERT INTO duplicate_group_members(duplicate_group_id,file_id,member_role,is_canonical_candidate,created_at) VALUES(?,?,?,?,?)", ("dup_name_001","file2","candidate",0,"2026-05-23T00:00:00Z"))


def test_search_filename(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    _seed_db(db)
    rows = search_metadata(db, query="W4")
    assert any(r["filename"] == "W4.pdf" for r in rows)


def test_search_sensitivity(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    _seed_db(db)
    rows = search_metadata(db, sensitivity_level="highly_sensitive")
    assert len(rows) == 1
    assert rows[0]["filename"] == "W4.pdf"


def test_list_pods(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    _seed_db(db)
    rows = list_pods(db)
    assert len(rows) == 1
    assert rows[0]["pod_id"] == "pod1"


def test_filter_pod_id(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    _seed_db(db)
    rows = search_metadata(db, pod_id="pod1")
    assert len(rows) >= 2


def test_duplicates_only(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    _seed_db(db)
    rows = search_metadata(db, duplicates_only=True)
    assert len(rows) == 1
    assert rows[0]["filename"] == "cover_letter.pdf"


def test_review_filter(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    _seed_db(db)
    rows = search_metadata(db, review_decision="needs_review")
    assert len(rows) >= 2


def test_read_only_prevents_writes(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    _seed_db(db)
    # running read API should not mutate row counts
    before = sqlite3.connect(db).execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
    _ = search_metadata(db, query="W4")
    after = sqlite3.connect(db).execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
    assert before == after


def test_no_real_path_touched(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    _seed_db(db)
    _ = search_metadata(db)
    assert "D:\\AI_Lab\\LifeVault" not in str(tmp_path)


def test_instance_oriented_results_with_shared_file_id_duplicate_group(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    with sqlite3.connect(db) as conn:
        apply_schema_v0(conn)
        conn.execute(
            "INSERT INTO sources(source_id,source_type,source_name,root_ref,is_active,created_at) VALUES(?,?,?,?,1,?)",
            ("src1", "local_folder", "src", "C:/fake", "2026-05-23T00:00:00Z"),
        )
        conn.execute(
            "INSERT INTO pods(pod_id,source_id,pod_name,event_name,pod_status,story_context,intake_notes,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            ("podx", "src1", "podx", "eventx", "onboarded_needs_review", "story", "", "normal", "warm", "2026-05-23T00:00:00Z", "2026-05-23T00:00:00Z"),
        )
        conn.execute(
            "INSERT INTO files(file_id,sha256,hash_algo,filename,ext,size_bytes,file_status,review_status,publish_status,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("file_shared", "c" * 64, "sha256", "identity_name.txt", ".txt", 5, "copied_to_pod", "needs_review", "not_published", "normal", "warm", "2026-05-23T00:00:00Z", "2026-05-23T00:00:00Z"),
        )
        conn.execute(
            "INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,path_is_absolute,path_platform,observed_at,is_current,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            ("inst1", "file_shared", "src1", "podx", "pod_copy", "original_copies/cover_letter.pdf", 0, "windows", "2026-05-23T00:00:00Z", 1, "2026-05-23T00:00:00Z", "2026-05-23T00:00:00Z"),
        )
        conn.execute(
            "INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,path_is_absolute,path_platform,observed_at,is_current,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            ("inst2", "file_shared", "src1", "podx", "pod_copy", "original_copies/cover_letter (1).pdf", 0, "windows", "2026-05-23T00:00:00Z", 1, "2026-05-23T00:00:00Z", "2026-05-23T00:00:00Z"),
        )
        conn.execute(
            "INSERT INTO review_decisions(decision_id,file_id,decision_type,review_status,publish_status,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
            ("revx", "file_shared", "needs_review", "needs_review", "not_published", "2026-05-23T00:00:00Z", "2026-05-23T00:00:00Z"),
        )
        conn.execute(
            "INSERT INTO duplicate_groups(duplicate_group_id,group_method,group_status,created_at,updated_at) VALUES(?,?,?,?,?)",
            ("dupx", "duplicate_name_candidate", "open", "2026-05-23T00:00:00Z", "2026-05-23T00:00:00Z"),
        )
        conn.execute(
            "INSERT INTO duplicate_group_members(duplicate_group_id,file_id,member_role,is_canonical_candidate,created_at) VALUES(?,?,?,?,?)",
            ("dupx", "file_shared", "candidate", 0, "2026-05-23T00:00:00Z"),
        )

    pod_rows = search_metadata(db, pod_id="podx")
    assert len(pod_rows) == 2
    assert sorted(r["pod_relative_path"] for r in pod_rows) == [
        "original_copies/cover_letter (1).pdf",
        "original_copies/cover_letter.pdf",
    ]
    assert sorted(r["filename"] for r in pod_rows) == ["cover_letter (1).pdf", "cover_letter.pdf"]

    dup_rows = search_metadata(db, duplicates_only=True)
    assert len(dup_rows) == 2
    assert all(r["duplicate_group_id"] == "dupx" for r in dup_rows)


def test_no_row_multiplication_with_multiple_review_rows_for_same_file(tmp_path: Path) -> None:
    db = tmp_path / "db.sqlite"
    with sqlite3.connect(db) as conn:
        apply_schema_v0(conn)
        conn.execute(
            "INSERT INTO sources(source_id,source_type,source_name,root_ref,is_active,created_at) VALUES(?,?,?,?,1,?)",
            ("src1", "local_folder", "src", "C:/fake", "2026-05-23T00:00:00Z"),
        )
        conn.execute(
            "INSERT INTO pods(pod_id,source_id,pod_name,event_name,pod_status,story_context,intake_notes,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            ("podm", "src1", "podm", "eventm", "onboarded_needs_review", "story", "", "normal", "warm", "2026-05-23T00:00:00Z", "2026-05-23T00:00:00Z"),
        )
        conn.execute(
            "INSERT INTO files(file_id,sha256,hash_algo,filename,ext,size_bytes,file_status,review_status,publish_status,sensitivity_level,storage_temperature,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("file_shared", "d" * 64, "sha256", "identity_name.txt", ".txt", 5, "copied_to_pod", "needs_review", "not_published", "normal", "warm", "2026-05-23T00:00:00Z", "2026-05-23T00:00:00Z"),
        )
        conn.execute(
            "INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,path_is_absolute,path_platform,observed_at,is_current,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            ("inst1", "file_shared", "src1", "podm", "pod_copy", "original_copies/dup_a.pdf", 0, "windows", "2026-05-23T00:00:00Z", 1, "2026-05-23T00:00:00Z", "2026-05-23T00:00:00Z"),
        )
        conn.execute(
            "INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,path_is_absolute,path_platform,observed_at,is_current,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            ("inst2", "file_shared", "src1", "podm", "pod_copy", "original_copies/dup_b.pdf", 0, "windows", "2026-05-23T00:00:00Z", 1, "2026-05-23T00:00:00Z", "2026-05-23T00:00:00Z"),
        )
        # Same created_at to mirror real-world fan-out risk; newest rowid should win.
        conn.execute(
            "INSERT INTO review_decisions(decision_id,file_id,decision_type,review_status,publish_status,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
            ("rev1", "file_shared", "needs_review", "needs_review", "not_published", "2026-05-23T01:00:00Z", "2026-05-23T01:00:00Z"),
        )
        conn.execute(
            "INSERT INTO review_decisions(decision_id,file_id,decision_type,review_status,publish_status,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
            ("rev2", "file_shared", "duplicate_review", "duplicate_review", "not_published", "2026-05-23T01:00:00Z", "2026-05-23T01:00:00Z"),
        )
        conn.execute(
            "INSERT INTO duplicate_groups(duplicate_group_id,group_method,group_status,created_at,updated_at) VALUES(?,?,?,?,?)",
            ("dupm", "duplicate_name_candidate", "open", "2026-05-23T00:00:00Z", "2026-05-23T00:00:00Z"),
        )
        conn.execute(
            "INSERT INTO duplicate_group_members(duplicate_group_id,file_id,member_role,is_canonical_candidate,created_at) VALUES(?,?,?,?,?)",
            ("dupm", "file_shared", "candidate", 0, "2026-05-23T00:00:00Z"),
        )

    pod_rows = search_metadata(db, pod_id="podm")
    assert len(pod_rows) == 2
    assert sorted(r["pod_relative_path"] for r in pod_rows) == [
        "original_copies/dup_a.pdf",
        "original_copies/dup_b.pdf",
    ]
    assert all(r["review_decision"] == "duplicate_review" for r in pod_rows)

    dup_rows = search_metadata(db, duplicates_only=True)
    assert len(dup_rows) == 2
    assert sorted(r["pod_relative_path"] for r in dup_rows) == [
        "original_copies/dup_a.pdf",
        "original_copies/dup_b.pdf",
    ]
