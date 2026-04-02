# Pending Task

## Task ID
- TB-20260402-07

## Task Type
- MIGRATION

## Goal
- Execute `BATCH-MIG-02A` (item `M-011`) by shift/lifting the explicitly validated Technologies notebooks from `D:\Workspace\Technologies` into canonical `D:\StudyBook\tracks` and `D:\StudyBook\interview` paths, then run smoke checks.

## Non-Goals
- Do not migrate full prompt packs in this run.
- Do not migrate secret-bearing setup files.
- Do not run cloud write operations.

## Files to Read
- CONTROL_PROTOCOL.md
- docs/programs/zero_to_hero/EXECUTION_SYSTEM.md
- docs/programs/zero_to_hero/MIGRATION_BOARD.md
- docs/programs/zero_to_hero/TALKS_WITH_CLAUDE_EXTRACT_AND_SHIFT_LIFT_PLAN.md
- D:\Workspace\Technologies\*.ipynb (validated set)

## Files Allowed to Modify
- D:\StudyBook\tracks\10_streaming\r1\*.ipynb
- D:\StudyBook\tracks\10_streaming\r3\*.ipynb
- D:\StudyBook\tracks\11_batch_processing\r1\*.ipynb
- D:\StudyBook\tracks\11_batch_processing\r3\*.ipynb
- D:\StudyBook\tracks\12_orchestration\r1\*.ipynb
- D:\StudyBook\tracks\22_ml_platform\r1\*.ipynb
- D:\StudyBook\tracks\29_observability\r1\*.ipynb
- D:\StudyBook\tracks\30_system_design\r3\*.ipynb
- D:\StudyBook\interview\*.ipynb
- docs/programs/zero_to_hero/MIGRATION_BOARD.md
- agents/shared/agent_status.md
- agents/shared/task_register.md
- agents/shared/open_loops.md

## Allowed Scope
- bounded

## Autonomy Override (optional)
- extended

## Validation Commands
- `jupyter nbconvert --to notebook --execute <one notebook per migrated track> --output-dir <temp path>` (or equivalent smoke execution)

## Reasoning Depth
- deep

## Risk Level
- medium

## Definition of Done
- `M-011` marked done or blocked with evidence.
- Validated notebook set moved into canonical StudyBook targets.
- Smoke checks executed or exact blockers captured.
- Shared status files updated.

## Notes
- Preserve notebook content; avoid unneeded rewrites.
- Keep hardcoded secret scanning active during migration.
