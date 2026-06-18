from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_grok_root_files_exist() -> None:
    required = [
        "GROK_AGENTS.md",
        "GROK_RUNBOOK.md",
        "GROK_CURRENT_STATE.md",
        "GROK_MEMORY.md",
        "GROK_OPEN_LOOPS.md",
        "GROK_OPERATING_RULES.md",
        "Grok_PROJECT_PROFILE.md",
        "start_grok_lifevault.ps1",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"Missing required Grok root file: {rel}"


def test_codex_agent_files_exist() -> None:
    required = [
        "agents/codex/AGENTS.md",
        "agents/codex/LIFEVAULT_BOOTSTRAP.md",
        "agents/codex/CODEX_CONSTITUTION.md",
        "agents/chatgpt/CHATGPT_CONSTITUTION.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"Missing required agent file: {rel}"


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