from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class Proposal:
    source_path: str
    generated_at: str
    file_count: int
    total_size_bytes: int
    extensions: dict[str, int]
    filenames_sample: list[str]
    date_range: dict[str, str]
    duplicate_looking_filenames: list[str]
    same_size_candidates: list[dict[str, Any]]
    likely_document_types_by_filename: list[str]
    suggested_pod_name: str
    suggested_project: str
    suggested_category: str
    suggested_event_name: str
    suggested_vault_path: str
    confidence: str
    reason: str
    questions_for_user: list[str]


def _norm_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def analyze_source_folder(source: Path) -> Proposal:
    if not source.exists() or not source.is_dir():
        raise ValueError(f"Source path must exist and be a directory: {source}")

    files = sorted(p for p in source.rglob("*") if p.is_file())
    file_count = len(files)
    total_size = sum(p.stat().st_size for p in files)

    ext_counter = Counter((p.suffix.lower() or "(no_ext)") for p in files)
    filenames = [p.name for p in files]

    mts = [datetime.fromtimestamp(p.stat().st_mtime) for p in files] if files else []
    date_range = {
        "min_modified_time": min(mts).isoformat(timespec="seconds") if mts else "",
        "max_modified_time": max(mts).isoformat(timespec="seconds") if mts else "",
    }

    by_norm = defaultdict(list)
    by_size = defaultdict(list)
    for p in files:
        by_norm[_norm_name(p.stem) + p.suffix.lower()].append(str(p))
        by_size[p.stat().st_size].append(str(p))

    dup_names = sorted(k for k, v in by_norm.items() if len(v) > 1)[:30]
    same_size = [
        {"size_bytes": size, "count": len(paths)}
        for size, paths in sorted(by_size.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        if len(paths) > 1
    ][:30]

    likely_doc_types = sorted(
        {ext for ext in ext_counter if ext in {".pdf", ".doc", ".docx", ".md", ".txt", ".rtf", ".xlsx", ".pptx"}}
    )

    base = _norm_name(source.name or "pod") or "pod"
    suggested_pod_name = base
    suggested_project = "General"
    suggested_category = "intake"
    suggested_event_name = f"{base}_intake"
    suggested_vault_path = f"FileStore/90_Inbox/{base.upper()}"

    confidence = "medium" if file_count > 0 else "low"
    reason = "Rules-based metadata inference from filenames/extensions/date range."
    questions = [
        "Confirm project name?",
        "Confirm category?",
        "Confirm suggested vault path?",
        "Any include/exclude constraints before onboarding?",
    ]

    return Proposal(
        source_path=str(source),
        generated_at=datetime.now().isoformat(timespec="seconds"),
        file_count=file_count,
        total_size_bytes=total_size,
        extensions=dict(sorted(ext_counter.items())),
        filenames_sample=filenames[:50],
        date_range=date_range,
        duplicate_looking_filenames=dup_names,
        same_size_candidates=same_size,
        likely_document_types_by_filename=likely_doc_types,
        suggested_pod_name=suggested_pod_name,
        suggested_project=suggested_project,
        suggested_category=suggested_category,
        suggested_event_name=suggested_event_name,
        suggested_vault_path=suggested_vault_path,
        confidence=confidence,
        reason=reason,
        questions_for_user=questions,
    )


def proposal_to_dict(p: Proposal) -> dict[str, Any]:
    return asdict(p)


def save_proposal(proposals_dir: Path, proposal: Proposal) -> Path:
    proposals_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = _norm_name(Path(proposal.source_path).name or "source") or "source"
    out = proposals_dir / f"proposal_{timestamp}_{name}.json"
    out.write_text(json.dumps(proposal_to_dict(proposal), indent=2) + "\n", encoding="utf-8")
    return out
