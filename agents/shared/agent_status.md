## Task ID
- TB-20260402-18

## Topic
- Polish Azure proof wiring across docs/env template/registry after successful local proof

## Task Type
- ENHANCEMENT

## Reasoning Depth
- standard

## Risk Level
- low

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
- poc/connection_proofs/python/azure_connection_proof.py
- poc/connection_proofs/README.md
- _infra/env/.env.example
- docs/programs/zero_to_hero/CLOUD_ACCOUNT_REGISTRY.md
- .gitignore
- agents/shared/task_register.md

## Files Modified
- poc/connection_proofs/README.md
- _infra/env/.env.example
- docs/programs/zero_to_hero/CLOUD_ACCOUNT_REGISTRY.md
- .gitignore
- agents/shared/open_loops.md
- agents/shared/task_register.md
- agents/shared/agent_status.md

## Plan
1. Confirm Azure proof script quality and real runtime behavior.
2. Add missing Azure proof documentation in connection proofs README.
3. Add missing `AZURE_*` placeholders to env template.
4. Update cloud registry Azure status and verified metadata.
5. Ensure env template file is actually trackable in git.

## What Was Done
- Reviewed `poc/connection_proofs/python/azure_connection_proof.py`; script structure and read-only behavior are sound.
- Updated `poc/connection_proofs/README.md`:
  - Added Azure proof file to folder layout.
  - Added Azure proof usage command (`--mode both`).
  - Added Azure note in behavior section.
- Updated `_infra/env/.env.example` with Azure placeholders:
  - `AZURE_TENANT_ID`
  - `AZURE_SUBSCRIPTION_ID`
  - `AZURE_CLIENT_ID`
  - `AZURE_CLIENT_SECRET`
  - `AZURE_RESOURCE_GROUP`
- Updated `docs/programs/zero_to_hero/CLOUD_ACCOUNT_REGISTRY.md` Azure row from `unknown` to `proof_verified_local` and recorded verified subscription/tenant metadata from successful proof run.
- Added `AZURE_RESOURCE_GROUP` to Azure secret key mapping section.
- Fixed `.gitignore` to unignore `_infra/env/.env.example` (`!_infra/env/` and `!_infra/env/.env.example`) so env-template updates are shareable and no longer silently ignored.

## Validation
- command: `C:\py_venv\proj_educate\Scripts\python.exe -m py_compile D:\StudyBook\poc\connection_proofs\python\azure_connection_proof.py`
- result: success.

- command (sandbox): `... azure_connection_proof.py --mode cli`
- result: expected sandbox permission failure for Azure profile file access.

- command (escalated): `... azure_connection_proof.py --mode cli`
- result: success; `ok=true`, subscription/tenant resolved.

- command (escalated): `... azure_connection_proof.py --mode both`
- result: success; both `cli_probe` and `sdk_probe` returned `ok=true` with matching subscription ID.

- command: `Select-String` checks on README/env/registry
- result: success; Azure entries present and consistent.

- command: `git check-ignore -v _infra/env/.env.example`
- result: now unignored by explicit exception rule and appears as trackable change.

## Decisions
- Keep Azure proof default as read-only `cli+sdk` path for richer diagnostics while avoiding writes.
- Treat sandbox Azure-profile access failure as environment artifact; rely on escalated/user-shell run for real credential validation.

## Assumptions
- Azure account metadata verified during this run remains valid for immediate follow-up tasks.

## Issues / Risks
- Proof script validation requires user-context Azure profile access; sandbox-only validation can produce false negatives.

## Parking Lot Added
- none

## Open Loops Updated
- Added and closed `LOOP-015`.

## Next Step
- Optional: set `AZURE_SUBSCRIPTION_ID` in local `_infra/env/.env.local` to pin proofs to a single subscription context.
