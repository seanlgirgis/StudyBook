import sqlite3
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lifevault.schema_v0 import EXPECTED_INDEXES, EXPECTED_TABLES, MIGRATION_ID


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = dict()
    env.update({"PYTHONPATH": str(SRC)})
    return subprocess.run(
        [sys.executable, "-m", "lifevault.migrate", *args],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        env=env,
    )


def test_migration_creates_expected_tables_and_indexes(tmp_path: Path) -> None:
    db_path = tmp_path / "lv" / "test.sqlite"
    result = _run_cli("--db-path", str(db_path), "--apply", MIGRATION_ID)
    assert result.returncode == 0, result.stdout + result.stderr

    with sqlite3.connect(db_path) as conn:
        tables = {
            r[0]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        indexes = {
            r[0]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index'"
            ).fetchall()
        }

    for name in EXPECTED_TABLES:
        assert name in tables
    for name in EXPECTED_INDEXES:
        assert name in indexes


def test_schema_migrations_contains_migration_id_and_idempotent(tmp_path: Path) -> None:
    db_path = tmp_path / "idempotent.sqlite"
    first = _run_cli("--db-path", str(db_path), "--apply", MIGRATION_ID)
    second = _run_cli("--db-path", str(db_path), "--apply", MIGRATION_ID)
    assert first.returncode == 0
    assert second.returncode == 0
    assert "already applied" in second.stdout.lower()

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            "SELECT migration_id FROM schema_migrations WHERE migration_id = ?",
            (MIGRATION_ID,),
        ).fetchall()
    assert len(rows) == 1


def test_validate_passes_after_migration(tmp_path: Path) -> None:
    db_path = tmp_path / "validate.sqlite"
    _run_cli("--db-path", str(db_path), "--apply", MIGRATION_ID)
    result = _run_cli("--db-path", str(db_path), "--validate")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Validation passed" in result.stdout


def test_foreign_keys_reject_invalid_references(tmp_path: Path) -> None:
    db_path = tmp_path / "fk.sqlite"
    _run_cli("--db-path", str(db_path), "--apply", MIGRATION_ID)

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                """
                INSERT INTO pods (pod_id, source_id, pod_name, pod_status, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                ("pod_x", "missing_src", "pod", "proposed", "2026-05-23T00:00:00Z"),
            )


def test_check_constraints_reject_invalid_enum(tmp_path: Path) -> None:
    db_path = tmp_path / "check.sqlite"
    _run_cli("--db-path", str(db_path), "--apply", MIGRATION_ID)

    with sqlite3.connect(db_path) as conn:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                """
                INSERT INTO sources (source_id, source_type, source_name, created_at)
                VALUES (?, ?, ?, ?)
                """,
                ("src_bad", "bad_type", "Bad", "2026-05-23T00:00:00Z"),
            )


def test_fake_lifecycle_insert_read(tmp_path: Path) -> None:
    db_path = tmp_path / "lifecycle.sqlite"
    _run_cli("--db-path", str(db_path), "--apply", MIGRATION_ID)

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute(
            "INSERT INTO sources(source_id,source_type,source_name,created_at) VALUES(?,?,?,?)",
            ("src1", "local_folder", "Temp Source", "2026-05-23T00:00:00Z"),
        )
        conn.execute(
            "INSERT INTO pods(pod_id,source_id,pod_name,pod_status,created_at) VALUES(?,?,?,?,?)",
            ("pod1", "src1", "Pod", "proposed", "2026-05-23T00:01:00Z"),
        )
        conn.execute(
            """
            INSERT INTO files(file_id,sha256,created_at,file_status,review_status,publish_status,sensitivity_level,storage_temperature)
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                "file1",
                "abc123",
                "2026-05-23T00:02:00Z",
                "observed",
                "needs_review",
                "not_published",
                "unknown",
                "unknown",
            ),
        )
        conn.execute(
            """
            INSERT INTO file_instances(instance_id,file_id,source_id,pod_id,instance_role,instance_path,created_at)
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                "inst1",
                "file1",
                "src1",
                "pod1",
                "pod_copy",
                "tmp/pod/file1.txt",
                "2026-05-23T00:03:00Z",
            ),
        )
        conn.execute(
            """
            INSERT INTO review_decisions(decision_id,file_id,decision_type,review_status,publish_status,created_at)
            VALUES(?,?,?,?,?,?)
            """,
            (
                "rev1",
                "file1",
                "publish_approved",
                "approved",
                "publish_approved",
                "2026-05-23T00:04:00Z",
            ),
        )
        row = conn.execute(
            """
            SELECT s.source_name, p.pod_name, f.file_id, i.instance_path, r.decision_type
            FROM sources s
            JOIN pods p ON p.source_id = s.source_id
            JOIN file_instances i ON i.pod_id = p.pod_id
            JOIN files f ON f.file_id = i.file_id
            JOIN review_decisions r ON r.file_id = f.file_id
            WHERE f.file_id = 'file1'
            """
        ).fetchone()
    assert row is not None


def test_dry_run_does_not_create_db_file(tmp_path: Path) -> None:
    db_path = tmp_path / "dry" / "dry.sqlite"
    result = _run_cli("--db-path", str(db_path), "--dry-run")
    assert result.returncode == 0
    assert not db_path.exists()


def test_real_db_path_rejected_without_confirm() -> None:
    db_path = r"D:\AI_Lab\LifeVault\db\lifevault.sqlite"
    result = _run_cli("--db-path", db_path, "--status")
    assert result.returncode != 0
    assert "Unsafe path rejected" in result.stdout


def test_path_inside_repo_rejected(tmp_path: Path) -> None:
    db_path = ROOT / "tmp_should_fail.sqlite"
    result = _run_cli("--db-path", str(db_path), "--status")
    assert result.returncode != 0
    assert "Unsafe path rejected" in result.stdout


def test_tests_do_not_touch_ai_lab_path(tmp_path: Path) -> None:
    # Confirms test-owned paths stay in pytest tmp dirs.
    db_path = tmp_path / "owned.sqlite"
    assert "D:\\AI_Lab\\LifeVault" not in str(db_path)


import pytest