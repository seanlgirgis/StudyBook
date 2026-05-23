# LV_INGEST_FOLDER_V0.md

## Purpose

`LV_ingest_folder v0` is a safe operator workflow that orchestrates UC_001 + UC_003 only.

## Operator Flow

1. Operator provides `SourcePath` and optional `Story`.
2. Run UC_001 proposal generation.
3. Show proposal summary.
4. Stop and require explicit approval before UC_003.
5. If approved, run UC_003 pod creation.
6. Show pod summary.
7. Stop.

## Inputs

- `SourcePath`
- optional `Story`
- optional `AutoApprovePod` (default false)

## Outputs

- UC_001 proposal package
- UC_003 onboarding pod package (only when explicitly approved)

## Approval Gates

- Default behavior stops after UC_001.
- UC_003 runs only when explicit approval is provided (`AutoApprovePod`).

## Safety Boundaries

- No database writes.
- No OneDrive/rclone calls.
- No upload/publish.
- No content extraction.
- No text cache.
- No source cleanup.
- No move/delete/rename/sync.
- UC_003 remains copy-only.
- Source remains untouched.

## Relationship to Use Cases

- UC_001: proposal + metadata/filename sensitivity hints (UC_002-lite)
- UC_003: copy-only pod creation
- UC_011: not part of v0 workflow

## What It Does Not Do

- Does not index DB (UC_004).
- Does not publish vault (UC_006).
- Does not verify vault copy (UC_007).
- Does not cleanup source (UC_008).

## Future Extensions

- richer UC_002 standalone review command
- explicit include/exclude file selection before UC_003
- post-pod review assistant actions