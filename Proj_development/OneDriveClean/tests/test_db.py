import csv
import json
from pathlib import Path

from onedriveclean.db import connect_db, ensure_tables, read_manifest_csv, search_files, upsert_files_from_manifest, upsert_pod


def test_db_tables_and_index_search(tmp_path: Path) -> None:
    db = tmp_path / "onedriveclean.sqlite"
    conn = connect_db(db)
    ensure_tables(conn)

    pod = {
        "pod_id": "pod_1",
        "pod_name": "apod",
        "source_path": "C:/src",
        "project": "P",
        "category": "C",
        "event_name": "E",
        "suggested_vault_path": "FileStore/X",
        "status": "onboarded_needs_review",
        "created_at": "2026-05-22T10:00:00",
        "notes": "",
    }
    upsert_pod(conn, pod)

    manifest = tmp_path / "_pod_manifest.csv"
    with manifest.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["pod_id","pod_name","source_path","source_file_path","pod_file_path","filename","extension","size_bytes","modified_time","project","category","event_name","suggested_vault_path","text_extraction_status"])
        w.writeheader()
        w.writerow({"pod_id":"pod_1","pod_name":"apod","source_path":"C:/src","source_file_path":"C:/src/a.pdf","pod_file_path":"C:/pod/a.pdf","filename":"a.pdf","extension":".pdf","size_bytes":"10","modified_time":"2026-05-22T10:00:00","project":"P","category":"C","event_name":"E","suggested_vault_path":"FileStore/X","text_extraction_status":"not_extracted"})

    rows = read_manifest_csv(manifest)
    assert upsert_files_from_manifest(conn, rows) == 1
    matches = search_files(conn, "a.pdf")
    assert len(matches) == 1
    assert matches[0]["pod_id"] == "pod_1"
