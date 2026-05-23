# ODC_folder_onboarding

Purpose:
Take any user-provided local source folder, investigate safely, create proposal, request human approval, create onboarding pod, index pod/files, run duplicate detection, and stop before vault upload.

Scope:
- Intake only.
- No vault publishing.
- No deletion/move/rename.
- Metadata only.

Primary commands:
- `pod.ps1 <SourcePath>`
- `scripts/start_pod_intake.ps1 -SourcePath <SourcePath>`
- `scripts/create_onboarding_pod.ps1 ...`
- `scripts/index_onboarding_pod.ps1 -PodId <PodId>`
- `scripts/detect_pod_duplicates.ps1 -PodId <PodId>`

Out of scope:
- OneDrive vault publish
- broad OneDrive migration
- source cleanup execution
