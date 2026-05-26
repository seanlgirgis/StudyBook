from pathlib import Path

import streamlit as st

DEFAULT_NOTES_ROOT = r"D:\AI_Lab\LifeVault\notes_hot"
DEFAULT_DB_PATH = r"D:\AI_Lab\LifeVault\db\lifevault.sqlite"
DEFAULT_VAULT_LOCAL = r"D:\AI_Lab\LifeVault\vault_local"

st.set_page_config(page_title="LifeVault Help Console v0", layout="wide")

st.title("LifeVault Help / Operator Console (v0, Read-Only)")
st.caption("Guidance-first console. No command execution. No DB writes. No cloud actions.")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Capability Status", "Command Builder", "Notes Inventory", "Safety", "Next Tasks"],
)


def _list_recent_markdown(root: Path, limit: int = 10):
    if not root.exists():
        return []
    files = list(root.rglob("*.md"))
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files[:limit]


def _list_note_folders(root: Path):
    if not root.exists():
        return []
    return sorted({str(p.parent) for p in root.rglob("_folder_manifest.json")})


def _list_sensitive_phase0_folders(root: Path):
    if not root.exists():
        return []
    out = []
    for p in root.rglob("note.md"):
        parent = p.parent
        protected = parent / "protected"
        if protected.exists() and (protected / "encrypted_body.lvenc").exists() and (protected / "encrypted_body_manifest.json").exists():
            out.append(str(parent))
    return sorted(set(out))


if page == "Home":
    st.header("Start Here")
    st.markdown(
        """
- **What LifeVault is:** a personal AI-assisted memory and file-governance system.
- **What is useful now:** file/folder lifecycle v0, notes v0, note folders v0, sensitive note Phase 0 layout checks.
- **What to try first:** use Command Builder to generate safe PowerShell commands and run them manually.
- **Safety:** this app is read-only and does not execute commands.
"""
    )
    st.subheader("Current Local Paths")
    st.code(
        f"Notes: {DEFAULT_NOTES_ROOT}\nDB: {DEFAULT_DB_PATH}\nVault Local: {DEFAULT_VAULT_LOCAL}",
        language="text",
    )

elif page == "Capability Status":
    st.header("Current Capability Status")
    rows = [
        {
            "Capability": "File/folder lifecycle v0",
            "Status": "Working",
            "How to use": "Use SUC_001 runbook/scripts sequence",
            "Safety level": "Medium (approval-gated)",
        },
        {
            "Capability": "Notes v0",
            "Status": "Working",
            "How to use": "run_notes_create.ps1, run_notes_search.ps1",
            "Safety level": "Low",
        },
        {
            "Capability": "Note folder v0",
            "Status": "Working",
            "How to use": "run_note_folder_create.ps1, run_note_folder_list.ps1",
            "Safety level": "Low",
        },
        {
            "Capability": "Sensitive note Phase 0",
            "Status": "Working (layout-only)",
            "How to use": "run_sensitive_note_phase0_create.ps1",
            "Safety level": "Caution (NOT real encryption)",
        },
        {
            "Capability": "Streamlit Help Console",
            "Status": "Working (read-only)",
            "How to use": "start_streamlit_help_console_docker.ps1",
            "Safety level": "Low",
        },
        {
            "Capability": "Real encryption",
            "Status": "Not implemented",
            "How to use": "Design docs only",
            "Safety level": "High risk if assumed",
        },
        {
            "Capability": "OneDrive/cloud sync",
            "Status": "Not implemented",
            "How to use": "Deferred",
            "Safety level": "High",
        },
        {
            "Capability": "Contacts/email/physical inventory",
            "Status": "Planned",
            "How to use": "Design backlog",
            "Safety level": "N/A",
        },
    ]
    st.table(rows)

elif page == "Command Builder":
    st.header("Command Builder")
    st.markdown("Generate copyable PowerShell commands only. This app does not execute commands.")

    with st.form("create_note_form"):
        st.subheader("Create note")
        title = st.text_input("Title", "My LifeVault note")
        story = st.text_input("Story", "")
        tags = st.text_input("Tags", "lifevault,notes")
        body = st.text_area("Body", "This is a markdown note.")
        notes_root = st.text_input("NotesRoot", DEFAULT_NOTES_ROOT)
        if st.form_submit_button("Generate create note command"):
            cmd = f'powershell -ExecutionPolicy Bypass -File .\\scripts\\run_notes_create.ps1 -Title "{title}" -Story "{story}" -Tags "{tags}" -Body "{body}" -NotesRoot "{notes_root}"'
            st.code(cmd, language="powershell")

    with st.form("search_notes_form"):
        st.subheader("Search notes")
        query = st.text_input("Query", "needle")
        notes_root = st.text_input("NotesRoot (search)", DEFAULT_NOTES_ROOT)
        if st.form_submit_button("Generate search notes command"):
            cmd = f'powershell -ExecutionPolicy Bypass -File .\\scripts\\run_notes_search.ps1 -Query "{query}" -NotesRoot "{notes_root}"'
            st.code(cmd, language="powershell")

    with st.form("create_folder_form"):
        st.subheader("Create note folder")
        title = st.text_input("Folder Title", "LifeVault Planning Notes")
        story = st.text_input("Folder Story", "")
        tags = st.text_input("Folder Tags", "lifevault,planning,notes")
        notes_root = st.text_input("NotesRoot (folder)", DEFAULT_NOTES_ROOT)
        if st.form_submit_button("Generate create note folder command"):
            cmd = f'powershell -ExecutionPolicy Bypass -File .\\scripts\\run_note_folder_create.ps1 -Title "{title}" -Story "{story}" -Tags "{tags}" -NotesRoot "{notes_root}"'
            st.code(cmd, language="powershell")

    with st.form("list_folder_form"):
        st.subheader("List note folders")
        notes_root = st.text_input("NotesRoot (list folders)", DEFAULT_NOTES_ROOT)
        if st.form_submit_button("Generate list note folders command"):
            cmd = f'powershell -ExecutionPolicy Bypass -File .\\scripts\\run_note_folder_list.ps1 -NotesRoot "{notes_root}"'
            st.code(cmd, language="powershell")

    with st.form("sensitive_create_form"):
        st.subheader("Create sensitive Phase 0 placeholder")
        title = st.text_input("Sensitive Title", "Demo Sensitive Note")
        public_hint = st.text_input("PublicHint", "Demo public hint only")
        story = st.text_input("Sensitive Story", "Testing sensitive note layout only")
        tags = st.text_input("Sensitive Tags", "lifevault,sensitive,demo")
        demo_body = st.text_input("DemoProtectedBody", "DO_NOT_STORE_THIS_AS_PLAINTEXT")
        notes_root = st.text_input("NotesRoot (sensitive)", DEFAULT_NOTES_ROOT)
        if st.form_submit_button("Generate create sensitive Phase 0 command"):
            cmd = f'powershell -ExecutionPolicy Bypass -File .\\scripts\\run_sensitive_note_phase0_create.ps1 -Title "{title}" -PublicHint "{public_hint}" -Story "{story}" -Tags "{tags}" -DemoProtectedBody "{demo_body}" -NotesRoot "{notes_root}"'
            st.code(cmd, language="powershell")

    with st.form("sensitive_search_form"):
        st.subheader("Search sensitive public_hint")
        query = st.text_input("Public hint query", "public hint")
        notes_root = st.text_input("NotesRoot (sensitive search)", DEFAULT_NOTES_ROOT)
        if st.form_submit_button("Generate sensitive public_hint search command"):
            cmd = f'powershell -ExecutionPolicy Bypass -File .\\scripts\\run_notes_search.ps1 -Query "{query}" -NotesRoot "{notes_root}"'
            st.code(cmd, language="powershell")

    st.markdown("File/folder lifecycle docs: `docs/super_use_cases/SUPER_USE_CASE_001_LOCAL_FOLDER_LIFECYCLE.md`")

elif page == "Notes Inventory":
    st.header("Notes Inventory")
    notes_root_raw = st.text_input("Notes root", DEFAULT_NOTES_ROOT)
    notes_root = Path(notes_root_raw)

    md_notes = list(notes_root.rglob("*.md")) if notes_root.exists() else []
    note_folders = _list_note_folders(notes_root)
    sensitive_phase0 = _list_sensitive_phase0_folders(notes_root)
    recent = _list_recent_markdown(notes_root, limit=10)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total markdown notes", len(md_notes))
    c2.metric("Note folders", len(note_folders))
    c3.metric("Sensitive phase0 packages", len(sensitive_phase0))

    st.subheader("Latest 10 markdown items")
    if recent:
        for p in recent:
            st.markdown(f"- `{p}`")
    else:
        st.info("No markdown files found at this path.")

    st.caption("Protected payload files are not read or displayed in this inventory view.")

elif page == "Safety":
    st.header("Safety")
    st.warning("GUI is read-only.")
    st.warning("It generates commands only and does not execute them.")
    st.warning("Sensitive Phase 0 is not real encryption. Do not store real secrets yet.")
    st.warning("No OneDrive sync/upload from this console.")
    st.warning("Destructive scripts require explicit approval gates.")

else:
    st.header("Next Tasks")
    task_seed = Path("docs/tasks/LIFEVAULT_PROJECT_TASK_SEED.md")
    if task_seed.exists():
        st.markdown(task_seed.read_text(encoding="utf-8"))
    else:
        st.info("Task seed file not found. Next bite: review docs/tasks/LIFEVAULT_PROJECT_TASK_SEED.md")
