from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_root_files_exist() -> None:
    required = [
        "AGENTS.md",
        "LIFEVAULT_BOOTSTRAP.md",
        "CHATGPT_CONSTITUTION.md",
        "CODEX_CONSTITUTION.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"Missing required root file: {rel}"


def test_required_docs_exist() -> None:
    required_docs = [
        "docs/LIFEVAULT_CHARTER.md",
        "docs/LIFEVAULT_ARCHITECTURE.md",
        "docs/LIFEVAULT_DATA_MODEL.md",
        "docs/LIFEVAULT_SKILL_FAMILY.md",
        "docs/LIFEVAULT_DATA_BOUNDARY.md",
        "docs/LIFEVAULT_SAFETY_RULES.md",
        "docs/LIFEVAULT_VAULT_LAYOUT.md",
        "docs/LIFEVAULT_RENAME_MIGRATION_NOTES.md",
        "docs/LIFEVAULT_CONTROL_CENTER_GUI_PLAN.md",
    ]
    for rel in required_docs:
        assert (ROOT / rel).exists(), f"Missing required doc: {rel}"