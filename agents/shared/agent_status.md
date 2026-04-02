## Task ID
- TB-20260402-17

## Topic
- Add machine-local seed-based passphrase workflow for seamless noninteractive secret decryption

## Task Type
- ENHANCEMENT

## Reasoning Depth
- standard

## Risk Level
- medium

## Allowed Scope
- bounded

## Files Read
- AGENTS.md
- CONTROL_PROTOCOL.md
- agents/shared/context_index.md
- agents/shared/open_loops.md
- agents/shared/approval_matrix.md
- agents/shared/command_allowlist.md
- docs/adr/ADR-INDEX.md
- agents/shared/pending_task.md
- agents/shared/agent_status.md
- agents/shared/decision_log.md
- scripts/env/env_core.ps1
- scripts/env/package_aws_credentials.ps1
- scripts/env/restore_aws_credentials.ps1
- env_setter.ps1
- docs/PORTABLE_ENV.md
- docs/operations/secrets_workflow.md
- docs/operations/aws_credentials_workflow.md
- .gitignore
- agents/shared/task_register.md

## Files Modified
- scripts/env/env_core.ps1
- scripts/env/register_secret_seed.ps1
- scripts/env/remove_secret_seed.ps1
- scripts/env/package_aws_credentials.ps1
- scripts/env/restore_aws_credentials.ps1
- .gitignore
- docs/PORTABLE_ENV.md
- docs/operations/secrets_workflow.md
- docs/operations/aws_credentials_workflow.md
- agents/shared/context_index.md
- agents/shared/open_loops.md
- agents/shared/task_register.md
- agents/shared/agent_status.md

## Plan
1. Extend `env_core.ps1` passphrase resolution to support local seed files in addition to env var + prompt.
2. Add seed register/remove helper scripts for one-time setup and rotation.
3. Update docs and gitignore to keep seed local-only.
4. Validate noninteractive secret loading with passphrase env var unset.

## What Was Done
- Added seed functions in `env_core.ps1`:
  - `Get-StudyBookSecretSeedPath`
  - `Protect-StudyBookSecretSeed`
  - `Unprotect-StudyBookSecretSeed`
  - Updated `Get-SecretPassphrase` to resolve in order: env var -> seed file -> prompt.
- Added `scripts/env/register_secret_seed.ps1` to create DPAPI-encrypted local seed from provided passphrase.
- Added `scripts/env/remove_secret_seed.ps1` to remove/rotate local seed.
- Updated AWS package/restore scripts to pass project root into `Get-SecretPassphrase` for deterministic seed path resolution.
- Added `config/secrets/.local/` to `.gitignore` (seed local-only, never synced).
- Updated operational docs (`docs/PORTABLE_ENV.md`, `docs/operations/secrets_workflow.md`, `docs/operations/aws_credentials_workflow.md`).
- Registered seed file locally using the provided passphrase.

## Validation
- command: `. .\scripts\env\env_core.ps1`
- result: success; script loads without parser errors.

- command: `.\scripts\env\register_secret_seed.ps1 -NonInteractive -Force` (with passphrase in env var)
- result: success; seed file created at `config/secrets/.local/studybook.secret.seed.dpapi.json`.

- command: `Remove-Item Env:STUDYBOOK_SECRET_PASSPHRASE; . .\scripts\env\env_core.ps1; Get-SecretPassphrase -NonInteractive -ProjectRoot D:\StudyBook`
- result: success; passphrase resolved from local seed (`SEED_PASSphrase_RESOLVED`).

- command: `.\env_setter.ps1 -NonInteractive -SkipVenvActivation` (with passphrase env var unset)
- result: success; `Secrets Loaded: True`.

- command: `.\scripts\env\package_aws_credentials.ps1 ... -NonInteractive` with escalation
- result: expected failure for seed decrypt in escalated context (`Key not valid for use in specified state`) because DPAPI seed is user-context bound.

- command: `.\scripts\env\package_aws_credentials.ps1` against local mock credentials in repo temp path with passphrase env var unset
- result: success; confirms seed-based noninteractive decrypt works in normal user context.

## Decisions
- Use Windows DPAPI CurrentUser seed as the local passphrase cache mechanism.
- Keep seed under `config/secrets/.local/` and gitignore the folder.
- Treat elevated context mismatch as expected behavior for DPAPI-protected local seed files.

## Assumptions
- Primary execution context for agents and tests is the normal user shell/session (non-elevated), matching seed creation context.

## Issues / Risks
- Seed decrypt will fail if commands are run as a different user/elevation token than the seed creator.
- Seed is machine/user-bound; each machine must register its own local seed once.

## Parking Lot Added
- none

## Open Loops Updated
- Added and closed `LOOP-014`.

## Next Step
- Optional: run `python D:\StudyBook\poc\connection_proofs\python\aws_connection_proof.py` from your shell to confirm end-to-end AWS proof still works with seed mode enabled.
