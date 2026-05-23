# UC_005_search_memory_without_hydration.md

## Goal

Search LifeVault metadata map without hydrating full OneDrive content locally.

## Safety Boundaries

- Metadata query only.
- No remote copy/sync operations.

## Dependencies

UC_004 indexed metadata, query interface.

## Acceptance Criteria

- Query returns relevant file/pod/source pointers and statuses.
- No file hydration required.

## Workflow Spec Reference

- `docs/use_cases/UC_005_SEARCH_MEMORY_WITHOUT_HYDRATION_WORKFLOW_SPEC.md`

## Command Reference

- `python -m lifevault.uc005_cli --db-path "<db>" --query "W4"`
- `python -m lifevault.uc005_cli --db-path "<db>" --sensitivity highly_sensitive`
- `python -m lifevault.uc005_cli --db-path "<db>" --pod-id "<pod_id>"`
- `python -m lifevault.uc005_cli --db-path "<db>" --duplicates-only`
- `python -m lifevault.uc005_cli --db-path "<db>" --list-pods`
- `powershell -ExecutionPolicy Bypass -File .\\scripts\\run_uc005_search.ps1 -Query "W4"`
