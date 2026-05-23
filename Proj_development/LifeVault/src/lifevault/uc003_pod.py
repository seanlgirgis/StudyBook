from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .config import project_root


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _safe_name(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in name).strip("_") or "pod"


def _is_inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except Exception:
        return False


def _assert_no_traversal(rel_path: str) -> None:
    p = Path(rel_path)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError(f"Path traversal/absolute path refused: {rel_path}")


def _build_pod_id(proposal: Dict[str, Any], approved_pod_name: str | None) -> str:
    if approved_pod_name:
        return _safe_name(approved_pod_name)
    return f"pod_{_safe_name(str(proposal.get('proposal_id', 'unknown')))}"


def create_onboarding_pod(
    proposal_path: str | Path,
    approved: bool,
    output_root: str | Path | None = None,
    approved_pod_name: str | None = None,
) -> Dict[str, Any]:
    if not approved:
        raise ValueError("Explicit approval is required for UC_003 pod creation")

    proposal_file = Path(proposal_path)
    if not proposal_file.exists():
        raise FileNotFoundError(f"Proposal not found: {proposal_file}")

    repo_root = project_root()
    if _is_inside(proposal_file, repo_root):
        raise ValueError("Proposal path inside repo root is refused for UC_003")

    proposal = json.loads(proposal_file.read_text(encoding="utf-8-sig"))
    source_path = Path(proposal["source_path"])
    if not source_path.exists() or not source_path.is_dir():
        raise FileNotFoundError(f"Source path missing or not a directory: {source_path}")

    if proposal.get("scan_status") not in {"success", "partial"}:
        raise ValueError("Proposal scan_status must be success or partial")

    if output_root is None:
        pod_root = proposal_file.parent.parent.parent / "pods"
    else:
        output_root_path = Path(output_root)
        pod_root = output_root_path if output_root_path.name.lower() == "pods" else output_root_path / "onboarding" / "pods"

    if _is_inside(pod_root, repo_root):
        raise ValueError("Pod output path inside repo root is refused for UC_003")

    pod_id = _build_pod_id(proposal, approved_pod_name)
    pod_dir = pod_root / pod_id

    if pod_dir.exists():
        raise FileExistsError(f"Destination pod already exists: {pod_dir}")

    if _is_inside(source_path, pod_dir):
        raise ValueError("Source path cannot be inside destination pod path")

    original_copies = pod_dir / "original_copies"
    reports = pod_dir / "reports"
    original_copies.mkdir(parents=True, exist_ok=False)
    reports.mkdir(parents=True, exist_ok=False)

    copied = 0
    failed = 0
    manifest_rows: List[Dict[str, Any]] = []
    review_rows: List[Dict[str, Any]] = []

    created_at = _now_iso()

    for entry in proposal.get("file_preview", []):
        rel = entry.get("relative_path", "")
        _assert_no_traversal(rel)

        src_file = source_path / rel
        dest_rel = Path("original_copies") / rel
        dest_file = pod_dir / dest_rel
        _assert_no_traversal(str(dest_rel))

        if dest_file.exists():
            raise FileExistsError(f"Refusing overwrite of existing pod file: {dest_file}")

        dest_file.parent.mkdir(parents=True, exist_ok=True)

        copy_status = "copied"
        copy_error = ""
        copied_at = _now_iso()

        try:
            shutil.copy2(src_file, dest_file)
            copied += 1
        except Exception as exc:
            copy_status = "failed"
            copy_error = str(exc)
            failed += 1

        manifest_rows.append(
            {
                "pod_id": pod_id,
                "source_relative_path": rel,
                "source_absolute_path": str(src_file),
                "pod_relative_path": str(dest_rel).replace("\\", "/"),
                "pod_absolute_path": str(dest_file),
                "filename": entry.get("filename", src_file.name),
                "extension": entry.get("extension", src_file.suffix.lower()),
                "size_bytes": entry.get("size_bytes", src_file.stat().st_size if src_file.exists() else 0),
                "modified_time": entry.get("modified_time", created_at),
                "copied_at": copied_at,
                "filename_sensitivity_level": entry.get("filename_sensitivity_level", "unknown"),
                "filename_sensitivity_reasons": ";".join(entry.get("filename_sensitivity_reasons", [])),
                "duplicate_name_group_id": entry.get("duplicate_name_group_id"),
                "copy_status": copy_status,
                "copy_error": copy_error,
            }
        )

        review_rows.append(
            {
                "pod_id": pod_id,
                "pod_relative_path": str(dest_rel).replace("\\", "/"),
                "filename": entry.get("filename", src_file.name),
                "suggested_sensitivity_level": entry.get("filename_sensitivity_level", "unknown"),
                "user_sensitivity_level": "",
                "review_decision": "needs_review",
                "user_notes": "",
                "approved_for_database_index": "false",
                "approved_for_vault_publish": "false",
            }
        )

    file_count = len(proposal.get("file_preview", []))
    pod_status = "created" if failed == 0 else "partial_copy"

    profile = {
        "schema_version": "1.0",
        "pod_id": pod_id,
        "created_at": created_at,
        "source_path": str(source_path),
        "source_proposal_id": proposal.get("proposal_id"),
        "source_proposal_path": str(proposal_file),
        "story": proposal.get("story"),
        "project": proposal.get("suggested_metadata", {}).get("suggested_project"),
        "category": proposal.get("suggested_metadata", {}).get("suggested_category"),
        "event_name": proposal.get("suggested_metadata", {}).get("suggested_event_name"),
        "suggested_vault_path": proposal.get("suggested_metadata", {}).get("suggested_vault_path"),
        "pod_status": pod_status,
        "sensitivity_highest_level": proposal.get("filename_sensitivity_summary", {}).get("highest_level", "unknown"),
        "file_count": file_count,
        "copied_file_count": copied,
        "failed_copy_count": failed,
        "duplicate_candidate_count": proposal.get("duplicate_name_summary", {}).get("duplicate_name_candidate_count", 0),
        "content_scan_status": "not_performed",
        "database_index_status": "not_indexed",
        "vault_publish_status": "not_published",
        "notes": "UC_003 pod created from accepted proposal",
        "warnings": proposal.get("warnings", []),
        "errors": proposal.get("errors", []),
    }

    (pod_dir / "_pod_profile.json").write_text(json.dumps(profile, indent=2), encoding="utf-8")

    manifest_fields = [
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
    ]
    with (pod_dir / "_pod_manifest.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=manifest_fields)
        w.writeheader()
        for row in manifest_rows:
            w.writerow(row)

    review_fields = [
        "pod_id",
        "pod_relative_path",
        "filename",
        "suggested_sensitivity_level",
        "user_sensitivity_level",
        "review_decision",
        "user_notes",
        "approved_for_database_index",
        "approved_for_vault_publish",
    ]
    with (pod_dir / "_review.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=review_fields)
        w.writeheader()
        for row in review_rows:
            w.writerow(row)

    (pod_dir / "_source_proposal_snapshot.json").write_text(
        proposal_file.read_text(encoding="utf-8-sig"), encoding="utf-8"
    )

    notes = "\n".join(
        [
            f"# UC_003 Pod Notes: {pod_id}",
            f"- Pod ID: {pod_id}",
            f"- Source Path: {source_path}",
            f"- Story: {proposal.get('story')}",
            f"- Created At: {created_at}",
            "- Safety: source files were copied only; source remains untouched.",
            "- Next safe actions: review _review.csv, then plan UC_004 database indexing approval.",
        ]
    )
    (pod_dir / "_notes.md").write_text(notes, encoding="utf-8")

    # contract sanity
    if copied + failed != file_count:
        raise RuntimeError("Contract violation: copied + failed must equal file_count")

    return {"pod_id": pod_id, "pod_dir": str(pod_dir), "pod_status": pod_status, "file_count": file_count}
