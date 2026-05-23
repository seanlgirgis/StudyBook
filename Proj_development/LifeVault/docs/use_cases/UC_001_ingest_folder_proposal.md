# UC_001_ingest_folder_proposal.md

## Use Case ID

UC_001

## Name

Ingest Folder Proposal

## Goal

Given a source folder and optional story/context, produce an investigation/proposal JSON that describes candidate files, metadata summary, sensitivity hints, and recommended next actions without copying files, writing DB records, or uploading to OneDrive.

## Primary Actor

Sean

## Supporting Actors

ChatGPT, Codex, future Streamlit control center

## Trigger

Operator requests intake assessment for a local folder.

## Preconditions

- Source folder path is provided.
- Project config is available.
- Operator confirms proposal-only mode.

## Main Success Path

1. Validate source path exists and is readable.
2. Enumerate folder structure and file-level basic metadata.
3. Derive initial summary stats (counts, extensions, sizes, age buckets).
4. Collect optional story/context note.
5. Produce proposal JSON in proposal output location.
6. Present summary + explicit next-step options (review, sensitivity pass, pod creation).

## Alternate Paths

- If source path is large, run scoped/depth-limited preview and mark as partial.
- If story/context is omitted, proceed with metadata-only proposal.

## Failure Paths

- Path missing/inaccessible -> return actionable error and no side effects.
- Permission denied -> return partial results and flagged status.

## Safety Rules

- No file copy.
- No DB write.
- No OneDrive/rclone operation.
- No delete/move/rename.

## Data Created/Updated

- Proposal JSON artifact only (synthetic summary + candidate metadata pointers).

## Database Impact

- None in UC_001.

## File-System Impact

- Read-only scan of provided source folder.
- Write proposal file into designated proposal workspace only.

## Git/Privacy Impact

- Proposal artifacts with real data must stay outside Git-tracked repo paths.

## OneDrive/Vault Impact

- None.

## Local AI Role

- Suggest metadata interpretation and possible sensitivity concerns.

## Codex Role

- Implement scanner/proposal generator and tests in proposal-only mode.

## Streamlit Role

- Future UI for folder selection and proposal review.

## Approval Gates

- Human approval required before transitioning from proposal to pod creation.

## Acceptance Criteria

- Produces proposal JSON from valid source path.
- Does not copy files.
- Does not write DB.
- Does not call OneDrive/rclone.
- Emits clear summary and next-step recommendation.

## Test Cases

- Valid small folder yields proposal JSON.
- Missing folder yields failure without writes.
- Deep folder can run in preview mode.
- Output contains required metadata summary fields.

## Out of Scope

- Pod creation.
- Database indexing.
- Publishing to vault.

## Related Use Cases

UC_002, UC_003, UC_004, UC_009