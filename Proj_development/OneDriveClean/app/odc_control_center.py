from __future__ import annotations

import json
import subprocess
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_ps(script_rel: str, args: list[str]) -> tuple[int, str, str]:
    script = REPO_ROOT / script_rel
    cmd = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script),
        *args,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def read_paths_config() -> dict:
    local = REPO_ROOT / "config" / "paths.local.json"
    example = REPO_ROOT / "config" / "paths.example.json"
    path = local if local.exists() else example
    return json.loads(path.read_text(encoding="utf-8"))


def parse_pod_id(output: str) -> str:
    lines = [l.strip() for l in output.splitlines() if l.strip()]
    if not lines:
        return ""
    return lines[-1]


st.set_page_config(page_title="ODC Control Center", layout="wide")
st.title("ODC Control Center")
st.subheader("Folder Onboarding")

if "proposal" not in st.session_state:
    st.session_state.proposal = None
if "pod_id" not in st.session_state:
    st.session_state.pod_id = ""
if "status_log" not in st.session_state:
    st.session_state.status_log = []

source_path = st.text_input("Source folder", value=r"D:\Users\shareuser\Downloads\apod")
story = st.text_area("Story / context", value="BOA / LTIMindtree onboarding paperwork from May 2026.")

if st.button("Generate Proposal"):
    rc, out, err = run_ps("scripts/start_pod_intake.ps1", ["-SourcePath", source_path])
    if rc == 0:
        st.session_state.status_log.append("Proposal generated. Review suggested fields below.")
        # Run deterministic proposal directly to avoid parsing interactive output
        from onedriveclean.intake import analyze_source_folder

        p = analyze_source_folder(Path(source_path))
        st.session_state.proposal = p.__dict__
        if story.strip():
            st.session_state.proposal["story"] = story.strip()
    else:
        st.error("Proposal generation failed")
        st.code((out + "\n" + err).strip())

proposal = st.session_state.proposal or {
    "suggested_pod_name": "",
    "suggested_project": "",
    "suggested_category": "",
    "suggested_event_name": "",
    "suggested_vault_path": "",
}

col1, col2 = st.columns(2)
with col1:
    pod_name = st.text_input("PodName", value=proposal.get("suggested_pod_name", ""))
    project = st.text_input("Project", value=proposal.get("suggested_project", "General"))
    category = st.text_input("Category", value=proposal.get("suggested_category", "intake"))
with col2:
    event_name = st.text_input("EventName", value=proposal.get("suggested_event_name", ""))
    vault_path = st.text_input("SuggestedVaultPath", value=proposal.get("suggested_vault_path", "FileStore/90_Inbox"))

if st.button("Create Onboarding Pod"):
    args = [
        "-SourcePath", source_path,
        "-PodName", pod_name,
        "-Project", project,
        "-Category", category,
        "-EventName", event_name,
        "-SuggestedVaultPath", vault_path,
    ]
    rc, out, err = run_ps("scripts/create_onboarding_pod.ps1", args)
    if rc == 0:
        pod_id = parse_pod_id(out)
        st.session_state.pod_id = pod_id
        st.success(f"Pod created: {pod_id}")
        st.session_state.status_log.append(f"Pod created: {pod_id}")
    else:
        st.error("Pod creation failed")
        st.code((out + "\n" + err).strip())

pod_id = st.text_input("Created pod id", value=st.session_state.pod_id)

if st.button("Index Pod"):
    if not pod_id.strip():
        st.warning("Pod id required")
    else:
        rc, out, err = run_ps("scripts/index_onboarding_pod.ps1", ["-PodId", pod_id])
        if rc == 0:
            st.success("Pod indexed")
            st.session_state.status_log.append(f"Indexed pod: {pod_id}")
        else:
            st.error("Index failed")
            st.code((out + "\n" + err).strip())

if st.button("Detect Duplicates"):
    if not pod_id.strip():
        st.warning("Pod id required")
    else:
        rc, out, err = run_ps("scripts/detect_pod_duplicates.ps1", ["-PodId", pod_id])
        if rc == 0:
            st.success("Duplicate detection complete")
            st.session_state.status_log.append(f"Duplicate scan complete: {pod_id}")
        else:
            st.error("Duplicate detection failed")
            st.code((out + "\n" + err).strip())

st.markdown("### Results")
try:
    cfg = read_paths_config()
    pod_folder = str(Path(cfg["lab_root"]) / cfg["pods_dir"] / pod_id) if pod_id else ""
    manifest_path = str(Path(pod_folder) / "_pod_manifest.csv") if pod_folder else ""
    dup_path = str(Path(pod_folder) / "reports" / "duplicate_candidates.csv") if pod_folder else ""
except Exception:
    pod_folder = manifest_path = dup_path = ""

st.text_input("Pod folder path", value=pod_folder)
st.text_input("Manifest path", value=manifest_path)
st.text_input("Duplicate report path", value=dup_path)

st.markdown("### Status Messages")
for msg in st.session_state.status_log:
    st.write(f"- {msg}")

st.info("Safety: copy-only onboarding. No delete/move/rename/sync/upload/text extraction.")
