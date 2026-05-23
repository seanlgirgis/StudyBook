import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lifevault.uc001_proposal import (  # noqa: E402
    build_folder_proposal,
    detect_duplicate_name_candidates,
    detect_filename_sensitivity,
    normalize_duplicate_name,
    write_proposal_package,
)


REQUIRED_FIELDS = {
    "schema_version",
    "proposal_id",
    "created_at",
    "source_path",
    "source_exists",
    "scan_mode",
    "scan_status",
    "is_partial",
    "story",
    "folder_summary",
    "file_preview",
    "filename_sensitivity_summary",
    "content_scan_status",
    "content_scan_reason",
    "content_sensitivity_summary",
    "duplicate_name_summary",
    "suggested_metadata",
    "recommended_next_action",
    "allowed_next_actions",
    "forbidden_actions_in_uc_001",
    "warnings",
    "errors",
}


def test_valid_small_folder_creates_proposal_package(tmp_path: Path) -> None:
    src = tmp_path / "src"
    out = tmp_path / "out"
    src.mkdir()
    (src / "W4.pdf").write_text("x", encoding="utf-8")
    (src / "cover_letter.pdf").write_text("x", encoding="utf-8")
    proposal = build_folder_proposal(src, story="test", output_root=out)
    pkg = write_proposal_package(proposal, out / proposal["proposal_id"])

    assert (pkg / "proposal.json").exists()
    assert (pkg / "summary.md").exists()
    assert (pkg / "file_preview.csv").exists()
    assert (pkg / "filename_sensitivity_candidates.csv").exists()
    assert (pkg / "duplicate_name_candidates.csv").exists()


def test_missing_folder_fails_safely(tmp_path: Path) -> None:
    proposal = build_folder_proposal(tmp_path / "missing", output_root=tmp_path / "out")
    assert proposal["scan_status"] == "failed"
    assert proposal["source_exists"] is False
    assert proposal["errors"]


def test_duplicate_looking_names_detected() -> None:
    records = [
        {"filename": "cover_letter.pdf", "relative_path": "a/cover_letter.pdf"},
        {"filename": "cover_letter (1).pdf", "relative_path": "b/cover_letter (1).pdf"},
    ]
    dup = detect_duplicate_name_candidates(records)
    assert dup["duplicate_name_candidate_count"] == 1
    assert normalize_duplicate_name("cover_letter.pdf") == normalize_duplicate_name("cover_letter (1).pdf")


def test_sensitive_looking_filenames_flagged() -> None:
    assert detect_filename_sensitivity("W4.pdf")["level"] == "highly_sensitive"
    assert detect_filename_sensitivity("i9form.pdf")["level"] == "highly_sensitive"
    assert detect_filename_sensitivity("direct_deposit.pdf")["level"] == "highly_sensitive"
    assert detect_filename_sensitivity("DDep.pdf")["level"] == "highly_sensitive"
    assert detect_filename_sensitivity("HIPAA Notice of Privacy Practices.pdf")["level"] == "sensitive"
    assert detect_filename_sensitivity("Mutual_Agreement.pdf")["level"] == "sensitive"
    assert detect_filename_sensitivity("onboarding_manual.pdf")["level"] == "private"


def test_story_onboarding_sets_private_baseline_for_generic_filename() -> None:
    level = detect_filename_sensitivity("welcome_packet.pdf", story="new employee onboarding week 1")["level"]
    assert level == "private"


def test_proposal_contains_required_contract_fields(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "sample.txt").write_text("x", encoding="utf-8")
    proposal = build_folder_proposal(src, output_root=tmp_path / "out")
    assert REQUIRED_FIELDS.issubset(set(proposal.keys()))


def test_content_scan_status_default_not_performed(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "sample.txt").write_text("x", encoding="utf-8")
    proposal = build_folder_proposal(src, output_root=tmp_path / "out")
    assert proposal["content_scan_status"] == "not_performed"
    assert proposal["content_sensitivity_summary"] == "not_scanned"


def test_no_database_file_created(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "sample.txt").write_text("x", encoding="utf-8")
    out = tmp_path / "out"
    proposal = build_folder_proposal(src, output_root=out)
    write_proposal_package(proposal, out / proposal["proposal_id"])

    assert not (tmp_path / "lifevault.sqlite").exists()
    assert not any(p.name == "lifevault.sqlite" for p in tmp_path.rglob("*.sqlite"))


def test_output_directed_to_tmp_path(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "sample.txt").write_text("x", encoding="utf-8")
    out = tmp_path / "custom_out"
    proposal = build_folder_proposal(src, output_root=out)
    pkg = write_proposal_package(proposal, out / proposal["proposal_id"])
    assert str(pkg).startswith(str(out))


def test_no_onedrive_or_rclone_needed(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "sample.txt").write_text("x", encoding="utf-8")
    proposal = build_folder_proposal(src, output_root=tmp_path / "out")
    # Validate behavior/policy fields rather than incidental path substrings.
    assert "call_onedrive_or_rclone" in proposal["forbidden_actions_in_uc_001"]
    assert proposal["content_scan_status"] == "not_performed"
