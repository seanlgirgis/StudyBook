# Codex Operator Workflow

Use `ODC_folder_onboarding`.

Source folder:
`D:\Users\shareuser\Downloads\apod`

Story:
BOA / LTIMindtree onboarding paperwork from May 2026.

Workflow:
1. Build and display deterministic proposed pod metadata.
2. Show command and wait for human approval.
3. Create pod after approval.
4. Index pod in SQLite.
5. Run duplicate detection for pod.
6. Stop. Do not upload to OneDrive.

Suggested commands:
```powershell
.\pod.ps1 "D:\Users\shareuser\Downloads\apod"
# then if pod created, index/dedupe with returned PodId:
.\scripts\index_onboarding_pod.ps1 -PodId "<pod_id>"
.\scripts\detect_pod_duplicates.ps1 -PodId "<pod_id>"
```
