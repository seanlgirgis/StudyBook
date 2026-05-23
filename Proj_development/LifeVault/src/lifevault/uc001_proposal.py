from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import load_paths_example

SENSITIVITY_ORDER = ["unknown", "public", "normal", "private", "sensitive", "highly_sensitive"]

FORBIDDEN_ACTIONS = [
    "copy_files",
    "write_database",
    "call_onedrive_or_rclone",
    "delete_files",
    "move_files",
    "rename_files",
    "extract_full_content",
    "write_text_cache",
    "ai_classify_full_text",
]


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _proposal_id(source_path: Path) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    stem = re.sub(r"[^a-zA-Z0-9_-]", "_", source_path.name.lower())[:40]
    return f"uc001_{ts}_{stem or 'source'}"


def _default_output_root() -> Path:
    cfg = load_paths_example()
    lab_root = Path(cfg["lab_root"])
    proposals_dir = Path(cfg["proposals_dir"])
    return lab_root / proposals_dir


def normalize_duplicate_name(filename: str) -> str:
    name = filename.strip().lower()
    name = re.sub(r"\s*\(\d+\)(?=\.[^.]+$|$)", "", name)
    name = re.sub(r"[_\-]+copy(?=\.[^.]+$|$)", "", name)
    name = re.sub(r"\s+", " ", name)
    return name


def detect_filename_sensitivity(filename: str, relative_path: str | None = None, story: str | None = None) -> Dict[str, Any]:
    text = " ".join(filter(None, [filename, relative_path or "", story or ""])).lower()

    highly = [
        "w4",
        "w-4",
        "i9",
        "i-9",
        "direct deposit",
        "direct_deposit",
        "ddep",
        "payroll",
        "bank",
        "banking",
        "ssn",
        "social security",
        "passport",
        "driver license",
        "tax",
    ]
    sensitive = [
        "hipaa",
        "medical",
        "insurance",
        "legal",
        "agreement",
        "release",
        "privacy notice",
        "applicant statement",
    ]
    private = [
        "onboarding",
        "new hire",
        "policy",
        "policies",
        "manual",
        "helpmanual",
        "password reset",
        "employee",
        "employer",
        "career",
    ]

    reasons: List[str] = []
    level = "normal"

    for token in highly:
        if token in text:
            level = "highly_sensitive"
            reasons.append(f"matched:{token}")
    if level != "highly_sensitive":
        for token in sensitive:
            if token in text:
                level = "sensitive"
                reasons.append(f"matched:{token}")
    if level == "normal":
        for token in private:
            if token in text:
                level = "private"
                reasons.append(f"matched:{token}")

    if not reasons:
        reasons.append("no_sensitive_rule_match")

    return {"level": level, "reasons": reasons}


def detect_duplicate_name_candidates(file_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    groups: Dict[str, List[str]] = defaultdict(list)
    for rec in file_records:
        norm = normalize_duplicate_name(rec["filename"])
        groups[norm].append(rec["relative_path"])

    out_groups = []
    duplicate_map: Dict[str, str] = {}
    gid = 1
    for norm_name, paths in groups.items():
        if len(paths) > 1:
            group_id = f"dup_name_{gid:03d}"
            gid += 1
            out_groups.append({"group_id": group_id, "name": norm_name, "count": len(paths), "paths": paths})
            for p in paths:
                duplicate_map[p] = group_id

    return {
        "duplicate_name_candidate_count": len(out_groups),
        "groups": out_groups,
        "duplicate_map": duplicate_map,
    }


def build_folder_proposal(source_path: str | Path, story: str | None = None, output_root: str | Path | None = None, max_preview_files: int = 200) -> Dict[str, Any]:
    src = Path(source_path)
    created_at = _now_iso()
    proposal_id = _proposal_id(src)

    source_exists = src.exists() and src.is_dir()
    if output_root is None:
        output_root_path = _default_output_root()
    else:
        output_root_path = Path(output_root)

    warnings: List[Dict[str, str]] = []
    errors: List[Dict[str, str]] = []

    if not source_exists:
        errors.append({"code": "SOURCE_NOT_FOUND", "message": f"Source folder not found: {src}", "severity": "error"})
        return {
            "schema_version": "1.0",
            "proposal_id": proposal_id,
            "created_at": created_at,
            "source_path": str(src),
            "source_exists": False,
            "scan_mode": "metadata_only",
            "scan_status": "failed",
            "is_partial": False,
            "story": story,
            "folder_summary": {
                "file_count": 0,
                "folder_count": 0,
                "total_size_bytes": 0,
                "extension_counts": {},
                "largest_files": [],
                "oldest_modified_time": None,
                "newest_modified_time": None,
                "depth_limited": False,
                "max_depth_used": None,
            },
            "file_preview": [],
            "filename_sensitivity_summary": {
                "highest_level": "unknown",
                "candidate_count": 0,
                "candidates_by_level": {},
                "rule_version": "filename_rules_v1",
                "note": "No scan performed.",
            },
            "content_scan_status": "not_performed",
            "content_scan_reason": "UC_001 does not extract file contents by default.",
            "content_sensitivity_summary": "not_scanned",
            "duplicate_name_summary": {"duplicate_name_candidate_count": 0, "groups": []},
            "suggested_metadata": {
                "suggested_pod_name": f"pod_{proposal_id}",
                "suggested_project": None,
                "suggested_category": None,
                "suggested_event_name": None,
                "suggested_vault_path": None,
                "confidence": 0.0,
                "reason": "Source missing.",
                "questions_for_user": ["Please provide a valid source folder path."],
            },
            "recommended_next_action": "stop_due_to_error",
            "allowed_next_actions": ["save_only", "edit_proposal", "abandon_proposal"],
            "forbidden_actions_in_uc_001": FORBIDDEN_ACTIONS,
            "warnings": warnings,
            "errors": errors,
            "output_root": str(output_root_path),
        }

    all_files = [p for p in src.rglob("*") if p.is_file()]
    all_dirs = [p for p in src.rglob("*") if p.is_dir()]

    file_count = len(all_files)
    folder_count = len(all_dirs)
    extension_counts: Counter[str] = Counter()
    total_size_bytes = 0
    oldest = None
    newest = None

    file_preview: List[Dict[str, Any]] = []

    for p in all_files[:max_preview_files]:
        st = p.stat()
        rel = str(p.relative_to(src))
        ext = p.suffix.lower()
        extension_counts[ext or "<no_ext>"] += 1
        total_size_bytes += st.st_size
        mtime = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
        oldest = mtime if oldest is None or mtime < oldest else oldest
        newest = mtime if newest is None or mtime > newest else newest

        sens = detect_filename_sensitivity(p.name, rel, story)
        file_preview.append(
            {
                "relative_path": rel,
                "filename": p.name,
                "extension": ext,
                "size_bytes": st.st_size,
                "modified_time": mtime.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                "file_kind": "document",
                "filename_sensitivity_level": sens["level"],
                "filename_sensitivity_reasons": sens["reasons"],
                "duplicate_name_group_id": None,
                "included_in_preview": True,
            }
        )

    dup = detect_duplicate_name_candidates(file_preview)
    for rec in file_preview:
        rec["duplicate_name_group_id"] = dup["duplicate_map"].get(rec["relative_path"])

    level_counts = Counter([r["filename_sensitivity_level"] for r in file_preview])
    highest_level = "unknown"
    for level in reversed(SENSITIVITY_ORDER):
        if level_counts.get(level, 0) > 0:
            highest_level = level
            break

    scan_mode = "metadata_only" if file_count <= max_preview_files else "preview_limited"
    is_partial = file_count > max_preview_files
    scan_status = "partial" if is_partial else "success"

    if is_partial:
        warnings.append(
            {
                "code": "PREVIEW_LIMIT_REACHED",
                "message": f"Preview capped at {max_preview_files} files out of {file_count}.",
                "severity": "warning",
            }
        )

    recommendation = "proceed_to_uc_002" if story else "ask_for_story"

    return {
        "schema_version": "1.0",
        "proposal_id": proposal_id,
        "created_at": created_at,
        "source_path": str(src),
        "source_exists": True,
        "scan_mode": scan_mode,
        "scan_status": scan_status,
        "is_partial": is_partial,
        "story": story,
        "folder_summary": {
            "file_count": file_count,
            "folder_count": folder_count,
            "total_size_bytes": total_size_bytes,
            "extension_counts": dict(extension_counts),
            "largest_files": sorted(
                [{"relative_path": r["relative_path"], "size_bytes": r["size_bytes"]} for r in file_preview],
                key=lambda x: x["size_bytes"],
                reverse=True,
            )[:10],
            "oldest_modified_time": oldest.replace(microsecond=0).isoformat().replace("+00:00", "Z") if oldest else None,
            "newest_modified_time": newest.replace(microsecond=0).isoformat().replace("+00:00", "Z") if newest else None,
            "depth_limited": is_partial,
            "max_depth_used": None,
        },
        "file_preview": file_preview,
        "filename_sensitivity_summary": {
            "highest_level": highest_level,
            "candidate_count": sum(v for k, v in level_counts.items() if k in {"private", "sensitive", "highly_sensitive"}),
            "candidates_by_level": dict(level_counts),
            "rule_version": "filename_rules_v1",
            "note": "Filename/folder/extension/story signals only.",
        },
        "content_scan_status": "not_performed",
        "content_scan_reason": "UC_001 does not extract file contents by default.",
        "content_sensitivity_summary": "not_scanned",
        "duplicate_name_summary": {
            "duplicate_name_candidate_count": dup["duplicate_name_candidate_count"],
            "groups": dup["groups"],
        },
        "suggested_metadata": {
            "suggested_pod_name": f"pod_{proposal_id}",
            "suggested_project": src.name,
            "suggested_category": "Uncategorized",
            "suggested_event_name": "initial_intake",
            "suggested_vault_path": "LifeVault/01_Knowledge",
            "confidence": 0.6,
            "reason": "Generated from folder metadata and optional story.",
            "questions_for_user": ["Should this intake be split into smaller pods?"],
        },
        "recommended_next_action": recommendation,
        "allowed_next_actions": [
            "save_only",
            "edit_proposal",
            "run_uc_002_sensitivity_scan",
            "create_pod_after_approval",
            "abandon_proposal",
        ],
        "forbidden_actions_in_uc_001": FORBIDDEN_ACTIONS,
        "warnings": warnings,
        "errors": errors,
        "output_root": str(output_root_path),
    }


def write_proposal_package(proposal: Dict[str, Any], output_dir: str | Path) -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    proposal_json = out / "proposal.json"
    summary_md = out / "summary.md"
    file_preview_csv = out / "file_preview.csv"
    sensitivity_csv = out / "filename_sensitivity_candidates.csv"
    duplicate_csv = out / "duplicate_name_candidates.csv"

    proposal_copy = dict(proposal)
    proposal_copy.pop("output_root", None)
    proposal_json.write_text(json.dumps(proposal_copy, indent=2), encoding="utf-8")

    summary_md.write_text(
        "\n".join(
            [
                f"# UC_001 Proposal: {proposal['proposal_id']}",
                f"- Source: {proposal['source_path']}",
                f"- Scan status: {proposal['scan_status']}",
                f"- Files (preview): {len(proposal['file_preview'])}",
                f"- Recommended next action: {proposal['recommended_next_action']}",
            ]
        ),
        encoding="utf-8",
    )

    preview_fields = [
        "relative_path",
        "filename",
        "extension",
        "size_bytes",
        "modified_time",
        "file_kind",
        "filename_sensitivity_level",
        "filename_sensitivity_reasons",
        "duplicate_name_group_id",
        "included_in_preview",
    ]
    with file_preview_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=preview_fields)
        w.writeheader()
        for rec in proposal["file_preview"]:
            row = dict(rec)
            row["filename_sensitivity_reasons"] = ";".join(row.get("filename_sensitivity_reasons", []))
            w.writerow(row)

    with sensitivity_csv.open("w", newline="", encoding="utf-8") as f:
        fields = ["relative_path", "filename", "filename_sensitivity_level", "filename_sensitivity_reasons"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for rec in proposal["file_preview"]:
            if rec["filename_sensitivity_level"] in {"private", "sensitive", "highly_sensitive"}:
                w.writerow(
                    {
                        "relative_path": rec["relative_path"],
                        "filename": rec["filename"],
                        "filename_sensitivity_level": rec["filename_sensitivity_level"],
                        "filename_sensitivity_reasons": ";".join(rec["filename_sensitivity_reasons"]),
                    }
                )

    with duplicate_csv.open("w", newline="", encoding="utf-8") as f:
        fields = ["group_id", "name", "count", "paths"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for grp in proposal["duplicate_name_summary"]["groups"]:
            w.writerow(
                {
                    "group_id": grp["group_id"],
                    "name": grp["name"],
                    "count": grp["count"],
                    "paths": "|".join(grp.get("paths", [])),
                }
            )

    return out
