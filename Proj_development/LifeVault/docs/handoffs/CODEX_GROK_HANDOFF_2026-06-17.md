# CODEX_GROK_HANDOFF_2026-06-17

## 1. One-line summary

LifeVault currently has one proven v0 vertical slice for local folder lifecycle (`SUC_006`, `UC_001` through `UC_009`) plus a read-only Streamlit help console and note-related code/docs that are partially ahead of the 1000-foot tracker.

## 2. Purpose vs local_memory vs ALOK vs learning

- `Purpose` on disk is consistent: LifeVault is a personal knowledge memory and file-governance system that ingests mixed sources into controlled onboarding pods, records provenance/governance metadata, and publishes only approved content into a trusted clean vault.
- `local_memory` is not defined by that term in the repo. The closest on-disk concept is `SUC_005 Notes and Knowledge Memory`, where notes and note folders are first-class `vault_item`s with portable markdown-backed storage.
- `ALOK` is not defined anywhere found under the repo search.
- `learning` is not defined as a separate subsystem anywhere found under the repo search.
- Explicit boundary from current files: do not let Grok infer extra registries or agent-memory systems into LifeVault without a new checked-in spec. The repo currently defines vault items, notes, pods, DB metadata, and guided workflows; it does not define `ALOK` or a separate `learning` store.

## 3. Two-root layout

- Dev repo root: `D:\Workarea\StudyBook\Proj_development\LifeVault`
  - Intended contents: code, scripts, docs, templates, tests.
- Operational root: `D:\AI_Lab\LifeVault`
  - Intended contents: onboarding pods, proposals, databases, logs, reports, text cache, exports.
- Primary operational DB: `D:\AI_Lab\LifeVault\db\lifevault.sqlite`
- Must never go in Git:
  - real personal data
  - tokens, secrets, credentials, rclone tokens
  - real DB files
  - real DB backups
  - real exports
  - reports
  - logs
  - pod manifests
  - text cache artifacts

## 4. Core safety laws

- AI suggests; human approves.
- No delete by default.
- No move by default.
- No rename by default.
- Copy only in early phases unless explicitly approved otherwise.
- No rclone sync operations.
- No upload or publish to clean vault without explicit publish workflow.
- No file enters the clean vault outside LifeVault.
- The database is the searchable map.
- The clean vault is the final file source of truth.
- Onboarding pods are controlled working copies.
- Metadata/filename sensitivity and content sensitivity are separate stages.
- Writer model is v0 one-writer/many-reader; do not imply multi-writer live DB use.
- `UC_009` is quarantine-only in v0; no permanent delete.

## 5. Implemented today

### SUC status from tracker/index files

- `SUC_006 File and Folder Lifecycle`: `implemented_v0 / validated_once`
- `SUC_013 Backup, Restore, Portability, and Multi-Machine`: `implemented_v0 / partial`
- `SUC_005 Notes and Knowledge Memory`: `in_design` in the tracker, even though note-related code/tests and Streamlit status text exist
- `SUC_015 Streamlit Control Center / Agent Console`: `in_design`

### UC status from `docs/use_cases/USE_CASE_INDEX.md`

- `LV_INGEST_FOLDER_V0`: implemented (temp-only)
- `UC_001`: implemented / real-folder validated
- `UC_002`: partially implemented through `UC_001 v0`
- `UC_003`: implemented (temp-only)
- `UC_004`: implemented (temp-only)
- `UC_005`: implemented
- `UC_006`: implemented
- `UC_007`: implemented (temp-only)
- `UC_008`: implemented (temp-only)
- `UC_009`: implemented (temp-only quarantine-only v0; blocked by `UC_008` pass)
- `UC_010`: planned
- `UC_011`: planned / future gated content scan
- `UC_012`: designed

### Tests visible on disk

- Local folder lifecycle tests exist for `UC_001`, `UC_003`, `UC_004`, `UC_005`, `UC_006`, `UC_007`, `UC_008`, `UC_009`.
- Supporting tests exist for foundation/config/migration/notes/ingest-folder/Streamlit static checks.
- No fresh test run is claimed in this handoff; this section is file-based only.

### Streamlit console state

- The Streamlit app is documented as a read-only Help / Operator Console.
- `SUC_015` Phase 1 status says the skeleton is implemented as a read-only help console.
- `SUC_015` Phase 2 status says interactive command builder, read-only notes inventory, and sidebar navigation were added while remaining strictly read-only.
- Static tests assert required sections, Docker files, restart policy, and absence of obvious destructive execution strings.
- Actual runtime state of the console process or Docker stack is unknown from files alone.

## 6. In progress / next 3 safe tasks

- Re-run the proven `SUC_006` slice on a second tiny safe folder, which is explicitly listed in the tracker brainstorm backlog.
- Validate guarded real-mode rollout for `UC_003` and `UC_004` using dry-run-first procedure and existing real-DB guardrails.
- Reconcile `SUC_005` status documents with the existence of `notes.py`, `notes_cli.py`, note scripts, note tests, and Streamlit capability text so the planning docs match the codebase.

## 7. Deferred / do not start without approval

- `UC_011` content extraction or content sensitivity scanning.
- Any OneDrive/cloud publish or rclone-based workflow.
- Any encryption/decryption or secure-view rollout beyond current design docs.
- Any cleanup beyond `UC_009` quarantine-only v0 policy.
- Any destructive, move, rename, upload, or sync workflow not explicitly approved.
- Any live multi-machine concurrent writer workflow for `lifevault.sqlite`.

## 8. Environment

- Initialize environment from project root with `..\..\env_setter.ps1`.
- Common Python entrypoints are `python -m lifevault.<module>`.
- Python modules present under `src/lifevault`:
  - `config.py`
  - `lv_ingest_folder.py`
  - `migrate.py`
  - `notes.py`
  - `notes_cli.py`
  - `schema_v0.py`
  - `uc001_cli.py`
  - `uc001_proposal.py`
  - `uc003_cli.py`
  - `uc003_pod.py`
  - `uc004_cli.py`
  - `uc004_index_pod.py`
  - `uc005_cli.py`
  - `uc005_search.py`
  - `uc006_cli.py`
  - `uc006_review.py`
  - `uc007_cli.py`
  - `uc007_publish_local.py`
  - `uc008_cli.py`
  - `uc008_verify_publish.py`
  - `uc009_cli.py`
  - `uc009_cleanup_quarantine.py`
- Common run scripts:
  - `scripts/run_uc001_proposal.ps1`
  - `scripts/run_uc003_create_pod.ps1`
  - `scripts/run_uc004_index_pod.ps1`
  - `scripts/run_uc005_search.ps1`
  - `scripts/run_uc006_review.ps1`
  - `scripts/run_uc007_publish_local.ps1`
  - `scripts/run_uc008_verify_publish.ps1`
  - `scripts/run_uc009_cleanup_quarantine.ps1`
  - `scripts/run_notes_create.ps1`
  - `scripts/run_notes_search.ps1`
  - `scripts/run_note_folder_create.ps1`
  - `scripts/run_note_folder_list.ps1`
  - `scripts/run_sensitive_note_phase0_create.ps1`
  - `scripts/run_streamlit_help_console.ps1`
- Docker/console helpers:
  - `scripts/start_streamlit_help_console_docker.ps1`
  - `scripts/stop_streamlit_help_console_docker.ps1`
  - `scripts/status_streamlit_help_console_docker.ps1`
  - `scripts/install_streamlit_help_console_startup_task.ps1`
  - `scripts/uninstall_streamlit_help_console_startup_task.ps1`

## 9. Codex session read order vs proposed GROK read order

### Codex session read order on disk

Keep as-is from `AGENTS.md`:

1. `LIFEVAULT_BOOTSTRAP.md`
2. `CODEX_CONSTITUTION.md`
3. `docs/LIFEVAULT_CHARTER.md`
4. `docs/LIFEVAULT_ARCHITECTURE.md`
5. `docs/LIFEVAULT_DATA_MODEL.md`
6. `docs/LIFEVAULT_SKILL_FAMILY.md`
7. `docs/LIFEVAULT_DATA_BOUNDARY.md`
8. `docs/LIFEVAULT_SAFETY_RULES.md`

### Proposed GROK read order

1. `AGENTS.md`
2. `LIFEVAULT_BOOTSTRAP.md`
3. `CODEX_CONSTITUTION.md`
4. `CHATGPT_CONSTITUTION.md`
5. `docs/LIFEVAULT_CHARTER.md`
6. `docs/LIFEVAULT_ARCHITECTURE.md`
7. `docs/LIFEVAULT_DATA_MODEL.md`
8. `docs/LIFEVAULT_DATA_BOUNDARY.md`
9. `docs/LIFEVAULT_SAFETY_RULES.md`
10. `docs/strategy/LIFEVAULT_1000_FOOT_CAPABILITY_MAP.md`
11. `docs/super_use_cases/SUPER_USE_CASE_INDEX.md`
12. `docs/super_use_cases/SUPER_USE_CASE_TRACKER.md`
13. `docs/use_cases/USE_CASE_INDEX.md`
14. `docs/LIFEVAULT_OPERATIONS_RUNBOOK.md`

## 10. Open loops, decisions, and risks Codex knows from current files

- Open loops from tracker/runbook:
  - final multi-destination storage policy is not settled
  - copied vs moved defaults across capability lanes are not settled
  - `hot/warm/cold` defaults are not settled
  - plaintext-at-rest boundaries before encryption are not settled
  - password-manager vs LifeVault boundary for secrets is not settled
  - Streamlit control center first-priority displays are still an open planning question
- Decisions already reflected on disk:
  - `SUC_006` is the first proven vertical slice, not the whole product
  - search-first architecture is preferred; do not require full OneDrive hydration
  - sensitive metadata/filename handling comes before content extraction
  - publish is copy-first, verify-first, cleanup-later
  - cleanup remains quarantine-only in v0
  - first writer machine is ASUS PC
- Risks and document mismatches:
  - `docs/LIFEVAULT_OPERATIONS_RUNBOOK.md` section `8. Current v0 Status` says no ingestion and no publish are implemented in the new repo, but `docs/use_cases/USE_CASE_INDEX.md` and super-use-case docs show multiple implemented/temp-only workflows.
  - `SUPER_USE_CASE_TRACKER.md` says `SUC_005` is `in_design`, while note code, note tests, note scripts, and Streamlit capability text indicate partial implementation exists.
  - Real operational rollout remains guarded because several workflows are still explicitly temp-only and dry-run-first.

## 11. Files ChatGPT likely holds that are not in the repo

- No checked-in file inventory identifies external ChatGPT-held files.
- `CHATGPT_CONSTITUTION.md` exists in the repo, but no repo file enumerates additional off-repo ChatGPT artifacts.
- Any claim about ChatGPT-only notes, directives, memory, or sidecar files would be `[chat-only, unverified]`.

## 12. Recommendation: application vs knowledge_vault vs hybrid for director registry

- Recommendation: hybrid.
- Reason from current files:
  - the repo already treats notes/note folders as first-class knowledge-memory items under `SUC_005`
  - the repo also treats workflows, approvals, audit trails, and safe command generation as application behavior
  - `SUC_015` is guidance-first and read-only, which fits a director registry that points to both operational commands and knowledge artifacts without becoming an unsafe control plane
- Practical implication:
  - keep director registry definitions in the application/documentation layer in Git
  - let durable human/agent memory records live as LifeVault note or vault-item structures under operational policy
  - do not invent a separate `ALOK` registry until it has an explicit checked-in contract

## Files created for this handoff

- `docs/handoffs/CODEX_GROK_HANDOFF_2026-06-17.md`
