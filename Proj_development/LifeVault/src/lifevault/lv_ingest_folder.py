from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .uc001_proposal import build_folder_proposal, write_proposal_package
from .uc003_pod import create_onboarding_pod


def run_lv_ingest_folder(
    source_path: str | Path,
    story: str | None = None,
    output_root: str | Path | None = None,
    auto_approve_pod: bool = False,
    approved_pod_name: str | None = None,
    max_preview_files: int = 200,
) -> Dict[str, Any]:
    proposal = build_folder_proposal(source_path, story=story, output_root=output_root, max_preview_files=max_preview_files)

    proposal_root = Path(output_root) if output_root else Path(proposal["output_root"])
    proposal_dir = proposal_root / proposal["proposal_id"]
    write_proposal_package(proposal, proposal_dir)

    proposal_path = proposal_dir / "proposal.json"
    summary = {
        "proposal_path": str(proposal_path),
        "file_count": proposal.get("folder_summary", {}).get("file_count", 0),
        "highest_sensitivity": proposal.get("filename_sensitivity_summary", {}).get("highest_level", "unknown"),
        "duplicate_candidate_count": proposal.get("duplicate_name_summary", {}).get("duplicate_name_candidate_count", 0),
        "recommended_next_action": proposal.get("recommended_next_action"),
        "suggested_metadata": proposal.get("suggested_metadata", {}),
    }

    result: Dict[str, Any] = {
        "proposal": summary,
        "auto_approved": auto_approve_pod,
        "next_uc003_command": f'python -m lifevault.uc003_cli --proposal-path "{proposal_path}" --approved',
    }

    if auto_approve_pod:
        pod = create_onboarding_pod(
            proposal_path=proposal_path,
            approved=True,
            output_root=output_root,
            approved_pod_name=approved_pod_name,
        )
        pod_dir = Path(pod["pod_dir"])
        profile = json.loads((pod_dir / "_pod_profile.json").read_text(encoding="utf-8"))
        result["pod"] = {
            "pod_path": str(pod_dir),
            "file_count": profile.get("file_count", 0),
            "copied_count": profile.get("copied_file_count", 0),
            "failed_count": profile.get("failed_copy_count", 0),
            "review_csv_path": str(pod_dir / "_review.csv"),
            "next_safe_action": "Review _review.csv and plan UC_004 index approval.",
        }

    return result