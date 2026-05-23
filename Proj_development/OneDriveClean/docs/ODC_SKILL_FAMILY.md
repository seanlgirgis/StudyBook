# ODC Skill Family

This project uses a family of narrow ODC skills.

## ODC_folder_onboarding
- Purpose: Intake any user-provided local folder into a tracked onboarding pod with proposal, approval, pod creation, indexing, and duplicate detection.
- Inputs: `SourcePath`, optional story/context notes.
- Outputs: proposal JSON, pod profile/manifest/review files, SQLite index entries, duplicate report.
- Allowed commands: `pod.ps1`, `scripts/start_pod_intake.ps1`, `scripts/create_onboarding_pod.ps1`, `scripts/index_onboarding_pod.ps1`, `scripts/detect_pod_duplicates.ps1`.
- Forbidden actions: upload/publish to OneDrive, delete/move/rename source files, sync.
- Current status: active.

## ODC_pod_review
- Purpose: Review pod profile/manifest/review files and finalize metadata quality.
- Inputs: `PodId`.
- Outputs: metadata corrections and review notes.
- Allowed commands: read pod files, update review metadata files.
- Forbidden actions: upload, delete/move/rename source files.
- Current status: planned.

## ODC_dedupe_review
- Purpose: Review duplicate candidates and classify decisions.
- Inputs: `PodId`, duplicate report.
- Outputs: dedupe review decisions.
- Allowed commands: duplicate report generation/read-only analysis.
- Forbidden actions: automatic deletion.
- Current status: planned.

## ODC_text_extraction
- Purpose: Future controlled text extraction pipeline.
- Inputs: approved pod files.
- Outputs: extraction metadata/status only.
- Allowed commands: explicit extraction workflow commands (future).
- Forbidden actions: extraction without approval and privacy controls.
- Current status: future.

## ODC_vault_mapping
- Purpose: Map reviewed files to approved vault paths.
- Inputs: reviewed pod metadata.
- Outputs: approved vault mapping plan.
- Allowed commands: mapping/validation scripts (future).
- Forbidden actions: publishing without approval.
- Current status: planned.

## ODC_vault_publish
- Purpose: Publish approved files to clean vault.
- Inputs: approved mapping plan.
- Outputs: controlled copy/publish logs.
- Allowed commands: copy-only publish workflow (future).
- Forbidden actions: sync, delete/move/rename source data.
- Current status: future.

## ODC_search_assistant
- Purpose: Search indexed pod/file metadata for operator queries.
- Inputs: search query.
- Outputs: matching records and summaries.
- Allowed commands: `scripts/search_file_index.ps1`.
- Forbidden actions: file mutation.
- Current status: planned.

## ODC_cleanup_advisor
- Purpose: Recommend potential cleanup actions for human review.
- Inputs: indexed metadata, duplicate decisions.
- Outputs: advisory-only recommendations.
- Allowed commands: read/report commands.
- Forbidden actions: automatic cleanup execution.
- Current status: future.

## ODC_control_center_gui
- Purpose: Unified operator GUI for intake/review/index/search/publish stages.
- Inputs: source folder, pod selections, review actions.
- Outputs: operator actions and workflow status.
- Allowed commands: GUI wrappers over existing safe scripts.
- Forbidden actions: bypassing approval gates.
- Current status: future.
