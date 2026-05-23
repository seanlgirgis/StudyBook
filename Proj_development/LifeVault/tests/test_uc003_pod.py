import csv
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lifevault.uc003_pod import create_onboarding_pod


def _write_fake_proposal(tmp_path: Path, source_dir: Path, rel_paths: list[str]) -> Path:
    file_preview = []
    for rel in rel_paths:
        p = source_dir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("fake", encoding="utf-8")
        file_preview.append(
            {
                "relative_path": rel,
                "filename": p.name,
                "extension": p.suffix.lower(),
                "size_bytes": p.stat().st_size,
                "modified_time": "2026-05-23T00:00:00Z",
                "file_kind": "document",
                "filename_sensitivity_level": "normal",
                "filename_sensitivity_reasons": ["no_sensitive_rule_match"],
                "duplicate_name_group_id": None,
                "included_in_preview": True,
            }
        )

    proposal = {
        "schema_version": "1.0",
        "proposal_id": "uc001_fake_001",
        "created_at": "2026-05-23T00:00:00Z",
        "source_path": str(source_dir),
        "source_exists": True,
        "scan_mode": "metadata_only",
        "scan_status": "success",
        "is_partial": False,
        "story": "fake story",
        "folder_summary": {},
        "file_preview": file_preview,
        "filename_sensitivity_summary": {"highest_level": "normal", "candidate_count": 0, "candidates_by_level": {}, "rule_version": "v1", "note": ""},
        "content_scan_status": "not_performed",
        "content_scan_reason": "UC_001 does not extract file contents by default.",
        "content_sensitivity_summary": "not_scanned",
        "duplicate_name_summary": {"duplicate_name_candidate_count": 0, "groups": []},
        "suggested_metadata": {
            "suggested_pod_name": "pod_fake",
            "suggested_project": "Proj",
            "suggested_category": "Cat",
            "suggested_event_name": "Evt",
            "suggested_vault_path": "LifeVault/01_Knowledge",
            "confidence": 0.5,
            "reason": "fake",
            "questions_for_user": [],
        },
        "recommended_next_action": "proceed_to_uc_003_after_approval",
        "allowed_next_actions": ["create_pod_after_approval"],
        "forbidden_actions_in_uc_001": [],
        "warnings": [],
        "errors": [],
    }
    proposal_path = tmp_path / "outside_repo" / "proposal.json"
    proposal_path.parent.mkdir(parents=True, exist_ok=True)
    proposal_path.write_text(json.dumps(proposal, indent=2), encoding="utf-8")
    return proposal_path


def test_approval_required(tmp_path: Path) -> None:
    src = tmp_path / "src"
    proposal_path = _write_fake_proposal(tmp_path, src, ["a.txt"])
    with pytest.raises(ValueError):
        create_onboarding_pod(proposal_path, approved=False, output_root=tmp_path / "out")


def test_creates_full_pod_structure_and_copies_files(tmp_path: Path) -> None:
    src = tmp_path / "src"
    proposal_path = _write_fake_proposal(tmp_path, src, ["a.txt", "nested/b.txt"])
    out = tmp_path / "safe_outside_repo"
    result = create_onboarding_pod(proposal_path, approved=True, output_root=out, approved_pod_name="pod_test")

    pod_dir = Path(result["pod_dir"])
    assert (pod_dir / "original_copies").exists()
    assert (pod_dir / "reports").exists()
    for name in ["_pod_profile.json", "_pod_manifest.csv", "_review.csv", "_notes.md", "_source_proposal_snapshot.json"]:
        assert (pod_dir / name).exists()

    assert (pod_dir / "original_copies" / "a.txt").exists()
    assert (pod_dir / "original_copies" / "nested" / "b.txt").exists()
    assert (src / "a.txt").exists()
    assert (src / "nested" / "b.txt").exists()


def test_manifest_and_review_defaults(tmp_path: Path) -> None:
    src = tmp_path / "src"
    proposal_path = _write_fake_proposal(tmp_path, src, ["a.txt", "nested/b.txt"])
    out = tmp_path / "safe_outside_repo"
    result = create_onboarding_pod(proposal_path, approved=True, output_root=out)
    pod_dir = Path(result["pod_dir"])

    with (pod_dir / "_pod_manifest.csv").open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert all(r["copy_status"] in {"copied", "failed"} for r in rows)

    with (pod_dir / "_review.csv").open("r", encoding="utf-8") as f:
        rrows = list(csv.DictReader(f))
    assert len(rrows) == 2
    for r in rrows:
        assert r["review_decision"] == "needs_review"
        assert r["approved_for_database_index"] == "false"
        assert r["approved_for_vault_publish"] == "false"


def test_refuses_existing_destination(tmp_path: Path) -> None:
    src = tmp_path / "src"
    proposal_path = _write_fake_proposal(tmp_path, src, ["a.txt"])
    out = tmp_path / "safe_outside_repo"
    create_onboarding_pod(proposal_path, approved=True, output_root=out, approved_pod_name="pod_test")
    with pytest.raises(FileExistsError):
        create_onboarding_pod(proposal_path, approved=True, output_root=out, approved_pod_name="pod_test")


def test_refuses_path_traversal_entry(tmp_path: Path) -> None:
    src = tmp_path / "src"
    proposal_path = _write_fake_proposal(tmp_path, src, ["a.txt"])
    proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
    proposal["file_preview"].append(
        {
            "relative_path": "..\\evil.txt",
            "filename": "evil.txt",
            "extension": ".txt",
            "size_bytes": 1,
            "modified_time": "2026-05-23T00:00:00Z",
            "file_kind": "document",
            "filename_sensitivity_level": "normal",
            "filename_sensitivity_reasons": ["no_sensitive_rule_match"],
            "duplicate_name_group_id": None,
            "included_in_preview": True,
        }
    )
    proposal_path.write_text(json.dumps(proposal), encoding="utf-8")

    with pytest.raises(ValueError):
        create_onboarding_pod(proposal_path, approved=True, output_root=tmp_path / "safe_outside_repo")


def test_no_database_or_real_path_touched(tmp_path: Path) -> None:
    src = tmp_path / "src"
    proposal_path = _write_fake_proposal(tmp_path, src, ["a.txt"])
    out = tmp_path / "safe_outside_repo"
    create_onboarding_pod(proposal_path, approved=True, output_root=out)
    assert not any(p.name == "lifevault.sqlite" for p in tmp_path.rglob("*"))
    assert "D:\\AI_Lab\\LifeVault" not in str(tmp_path)


def test_reads_utf8_bom_proposal_json(tmp_path: Path) -> None:
    src = tmp_path / "src"
    proposal_path = _write_fake_proposal(tmp_path, src, ["a.txt"])
    proposal_text = proposal_path.read_text(encoding="utf-8")
    proposal_path.write_bytes(b"\xef\xbb\xbf" + proposal_text.encode("utf-8"))

    out = tmp_path / "safe_outside_repo"
    result = create_onboarding_pod(proposal_path, approved=True, output_root=out)
    assert Path(result["pod_dir"]).exists()
