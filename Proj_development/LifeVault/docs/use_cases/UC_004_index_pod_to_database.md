# UC_004_index_pod_to_database.md

## Goal

Index approved pod metadata into LifeVault DB for search/governance.

## Safety Boundaries

- Temp/test DB-first validation.
- No real DB writes until explicitly authorized workflow.

## Dependencies

Migration runner, schema v0, UC_003.

## Acceptance Criteria

- Indexed records map pod/files/instances/review states.
- Validation checks pass.

## Duplicate Modeling Note (v0)

- Duplicate-name candidates originate from pod manifest instances (paths/copies).
- Current DB membership table stores unique file identities (`file_id`) per duplicate group.
- When multiple paths share identical content hash, `duplicate_group_members` may be lower than manifest duplicate instance count.

## Workflow Spec Reference

- `docs/use_cases/UC_004_INDEX_POD_TO_DATABASE_WORKFLOW_SPEC.md`

## Command Reference

- `python -m lifevault.uc004_cli --pod-path "<pod path>" --db-path "<sqlite path>" --dry-run`
- `python -m lifevault.uc004_cli --pod-path "<pod path>" --db-path "<sqlite path>" --approved`
- real DB guarded commands require `--real-db-confirm`:
  - dry-run: `python -m lifevault.uc004_cli --pod-path "<pod path>" --db-path "D:\\AI_Lab\\LifeVault\\db\\lifevault.sqlite" --dry-run --real-db-confirm`
  - approved: `python -m lifevault.uc004_cli --pod-path "<pod path>" --db-path "D:\\AI_Lab\\LifeVault\\db\\lifevault.sqlite" --approved --real-db-confirm`
- `powershell -ExecutionPolicy Bypass -File .\\scripts\\run_uc004_index_pod.ps1 -PodPath "<pod path>" -DbPath "<sqlite path>" -DryRun`
- Temp-only smoke run:
  - `powershell -ExecutionPolicy Bypass -File .\\scripts\\smoke_uc004_temp.ps1`
  - optional temp root override:
    - `powershell -ExecutionPolicy Bypass -File .\\scripts\\smoke_uc004_temp.ps1 -TempRoot "D:\\temp\\lifevault_uc004_smoke"`

## Initialization Note

- Real DB creation/initialization is separate from UC_004 indexing.
- Real pod indexing should only occur after DB schema is initialized.
