from pathlib import Path
import csv
import fnmatch
import shutil
from datetime import datetime


def stage_batch(source: Path, stage_dir: Path, batch_name: str, source_name: str, include_globs: list[str], exclude_globs: list[str], project: str, category: str, suggested_clean_remote_path: str) -> Path:
    stage_dir.mkdir(parents=True, exist_ok=True)
    manifest = stage_dir / "_manifest.csv"
    rows = []
    for p in sorted(x for x in source.rglob("*") if x.is_file()):
        rel = p.relative_to(source)
        rel_s = str(rel).replace("\\", "/")
        if not any(fnmatch.fnmatch(p.name, pat) or fnmatch.fnmatch(rel_s, pat) for pat in include_globs):
            continue
        if any(fnmatch.fnmatch(rel_s, pat) for pat in exclude_globs):
            continue
        dst = stage_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)
        st = p.stat()
        rows.append({
            "source_name": source_name,
            "source_path": str(p),
            "staged_path": str(dst),
            "filename": p.name,
            "extension": p.suffix.lower(),
            "size_bytes": int(st.st_size),
            "modified_time": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
            "batch_name": batch_name,
            "project": project,
            "category": category,
            "suggested_clean_remote_path": suggested_clean_remote_path,
        })
    fields = ["source_name", "source_path", "staged_path", "filename", "extension", "size_bytes", "modified_time", "batch_name", "project", "category", "suggested_clean_remote_path"]
    with manifest.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow(row)
    return manifest
