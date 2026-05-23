# UC_003_create_onboarding_pod.md

## Goal

Create a controlled onboarding pod as a copy-first workspace after approval.

## Safety Boundaries

- Copy only.
- No source mutation.
- No source free-space operation in UC_003.
- Pod is a controlled working copy, not final file source of truth.

## Move Workflow Clarification

- Future user-facing move-to-store behavior must be decomposed into copy + verify + approved cleanup.
- Cleanup/removal ownership is UC_008, not UC_003.

## Dependencies

UC_001 approval, folder setup paths, safety rules.

## Acceptance Criteria

- Pod created in configured onboarding path.
- Source files unchanged.

## Workflow Spec Reference

- `docs/use_cases/UC_003_CREATE_ONBOARDING_POD_WORKFLOW_SPEC.md`
- `docs/contracts/UC_003_POD_PROFILE_AND_MANIFEST_CONTRACT.md`

## Command Reference

- `python -m lifevault.uc003_cli --proposal-path "<proposal.json>" --approved`
- `powershell -ExecutionPolicy Bypass -File .\\scripts\\run_uc003_create_pod.ps1 -ProposalPath "<proposal.json>" -Approved`
- Temp-only smoke run:
  - `powershell -ExecutionPolicy Bypass -File .\\scripts\\smoke_uc003_temp.ps1`
