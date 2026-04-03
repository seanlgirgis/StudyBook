# Decision Log

Use this file for durable technical decisions that affect future runs.

## Entry Template

- Date: YYYY-MM-DD
- Decision ID: DEC-###
- Task ID: TB-YYYYMMDD-XX
- Decision: one-line statement
- Rationale: why this was selected
- Alternatives considered: short list
- Impacted files: relative paths

## Entries

- Date: 2026-04-01
- Decision ID: DEC-001
- Task ID: TB-20260401-02
- Decision: default from strict one-file control to bounded-autonomy control
- Rationale: reduce stalls from over-constrained execution while preserving safety gates
- Alternatives considered: keep strict one-file workflow; fully open autonomy
- Impacted files: CONTROL_PROTOCOL.md, AGENTS.md, agents/shared/context_index.md, agents/shared/open_loops.md

- Date: 2026-04-01
- Decision ID: DEC-002
- Task ID: TB-20260401-03
- Decision: codify explicit approval matrix and command allowlist as durable policy files
- Rationale: improve trust and velocity by making autonomy boundaries explicit
- Alternatives considered: implicit policy only in protocol text
- Impacted files: agents/shared/approval_matrix.md, agents/shared/command_allowlist.md

- Date: 2026-04-01
- Decision ID: DEC-003
- Task ID: TB-20260401-04
- Decision: move environment bootstrap to config-driven machine profiles with passphrase-based encrypted secret files
- Rationale: keep project portable across machines while preserving secure secret sync via encrypted artifacts
- Alternatives considered: single hardcoded env_setter only; machine-local plaintext secrets
- Impacted files: env_setter.ps1, scripts/env/env_core.ps1, config/env/base.psd1, config/machines/*.psd1, docs/PORTABLE_ENV.md

- Date: 2026-04-01
- Decision ID: DEC-004
- Task ID: TB-20260401-05
- Decision: provide single guided bootstrap entrypoint for machine profile + secrets + validation
- Rationale: reduce setup friction and enforce consistent portability workflow across machines
- Alternatives considered: keep separate manual scripts only
- Impacted files: scripts/env/bootstrap_all.ps1, docs/PORTABLE_ENV.md, README.md

- Date: 2026-04-01
- Decision ID: DEC-005
- Task ID: TB-20260401-06
- Decision: adopt ADR governance for architecture-level decision tracking with immutable history and supersession
- Rationale: enable architecture-grade auditability and reduce decision drift across sessions
- Alternatives considered: continue with decision_log only
- Impacted files: docs/adr/*, scripts/adr/new_adr.ps1, CONTROL_PROTOCOL.md, README.md

- Date: 2026-04-01
- Decision ID: DEC-006
- Task ID: TB-20260401-07
- Decision: import legacy workspace credentials into a local gitignored StudyBook secrets bundle before encryption rollout
- Rationale: centralize migration inputs while avoiding accidental commit of plaintext secrets
- Alternatives considered: manual copy/paste from each source file; direct write into encrypted bundle without staging
- Impacted files: config/secrets/workspace-import.secrets.json, config/secrets/workspace-import.sources.md, agents/shared/open_loops.md

- Date: 2026-04-01
- Decision ID: DEC-007
- Task ID: TB-20260401-08
- Decision: store migrated credentials as shared encrypted secrets plus per-machine encrypted overlays, then delete plaintext staging files
- Rationale: support cross-machine portability while reducing plaintext secret exposure on disk
- Alternatives considered: keep plaintext shared secrets; keep import staging JSON indefinitely
- Impacted files: config/secrets/shared.secrets.enc.json, config/secrets/asuspc.secrets.enc.json, config/secrets/dell-laptop.secrets.enc.json, config/secrets/workspace-import.secrets.json

- Date: 2026-04-01
- Decision ID: DEC-008
- Task ID: TB-20260401-09
- Decision: maintain an explicit operations runbook folder for recurring commands instead of relying on chat recall
- Rationale: reduce repeated Q&A and improve self-service execution consistency
- Alternatives considered: keep instructions only in README or chat history
- Impacted files: docs/operations/README.md, docs/operations/env_startup.md, docs/operations/secrets_workflow.md, README.md

- Date: 2026-04-02
- Decision ID: DEC-009
- Task ID: TB-20260402-01
- Decision: track subscription renewal dates and cancel/review actions in operations runbooks
- Rationale: avoid missed renewals and keep billing reminders in durable project docs
- Alternatives considered: keep reminders in chat only; external personal notes
- Impacted files: docs/operations/subscription_tracker.md, docs/operations/README.md

- Date: 2026-04-02
- Decision ID: DEC-010
- Task ID: TB-20260402-02
- Decision: adopt an infra-first, batch-tracked migration system for ZeroToHero with explicit no-scaffold and create-only-when-missing rules
- Rationale: reduce rebuild risk, keep work traceable, and allow any incoming code agent to continue with minimal ambiguity
- Alternatives considered: big-bang regeneration; ad-hoc migration without a durable board
- Impacted files: docs/programs/zero_to_hero/EXECUTION_SYSTEM.md, docs/programs/zero_to_hero/MIGRATION_BOARD.md, agents/shared/context_index.md, agents/shared/open_loops.md
- Date: 2026-04-02
- Decision ID: DEC-011
- Task ID: TB-20260402-04
- Decision: adopt a transcript-derived shift/lift placement map as mandatory pre-migration input before moving workspace assets into ZeroToHero
- Rationale: reduce migration ambiguity, preserve proven assets, and prevent accidental secret or duplicate artifact carryover
- Alternatives considered: migrate ad-hoc from memory; defer extraction and discover paths during implementation
- Impacted files: docs/programs/zero_to_hero/TALKS_WITH_CLAUDE_EXTRACT_AND_SHIFT_LIFT_PLAN.md, docs/programs/zero_to_hero/MIGRATION_BOARD.md, agents/shared/context_index.md, agents/shared/open_loops.md

- Date: 2026-04-02
- Decision ID: DEC-012
- Task ID: TB-20260402-06
- Decision: standardize StudyBook infra reproducibility on a script-driven contract (`infra_up/down/seed/health`) plus a non-secret cloud account registry
- Rationale: make infra rebuildable from repository files, remove path ambiguity after target correction, and ensure cloud metadata is trackable without exposing secrets
- Alternatives considered: rely on manual docker commands only; keep cloud metadata scattered in prompts/docs
- Impacted files: _infra/scripts/infra_up.ps1, _infra/scripts/infra_down.ps1, _infra/scripts/infra_seed.ps1, _infra/scripts/infra_health.ps1, _infra/README.md, docs/programs/zero_to_hero/CLOUD_ACCOUNT_REGISTRY.md, docs/programs/zero_to_hero/MIGRATION_BOARD.md, docs/programs/zero_to_hero/TALKS_WITH_CLAUDE_EXTRACT_AND_SHIFT_LIFT_PLAN.md, docs/programs/zero_to_hero/EXECUTION_SYSTEM.md

- Date: 2026-04-02
- Decision ID: DEC-013
- Task ID: TB-20260402-08
- Decision: store Docker service purpose documentation under `docs/operations` as a stable agent-friendly dictionary
- Rationale: keep infrastructure semantics discoverable in a single durable location without requiring compose-file deep reads
- Alternatives considered: keep only comments in compose; keep service notes only in `_infra/README.md`
- Impacted files: docs/operations/docker_service_dictionary.md, docs/operations/README.md, _infra/README.md

- Date: 2026-04-02
- Decision ID: DEC-014
- Task ID: TB-20260402-09
- Decision: store provided MongoDB Atlas credential in local ignored env overlay and keep only non-secret metadata in tracked docs
- Rationale: enable immediate runtime access while preserving repository secret hygiene and push-protection compliance
- Alternatives considered: commit credential to docs (rejected); defer capture until encrypted secret passphrase flow is run
- Impacted files: _infra/env/.env.local (ignored), docs/programs/zero_to_hero/CLOUD_ACCOUNT_REGISTRY.md, docs/programs/zero_to_hero/MIGRATION_BOARD.md

- Date: 2026-04-02
- Decision ID: DEC-015
- Task ID: TB-20260402-10
- Decision: treat GCP `citi-de-learning` as project-defined but key-not-ready until a real service-account JSON replaces workspace placeholders
- Rationale: avoid false readiness assumptions that would break notebook execution while keeping migration tracking factual and reproducible
- Alternatives considered: assume project unavailable; postpone status update until notebook migration step
- Impacted files: docs/programs/zero_to_hero/CLOUD_ACCOUNT_REGISTRY.md, docs/programs/zero_to_hero/MIGRATION_BOARD.md, agents/shared/open_loops.md, agents/shared/task_register.md

- Date: 2026-04-02
- Decision ID: DEC-016
- Task ID: TB-20260402-11
- Decision: store real GCP service-account key in a protected user-local folder and reference it by path in local env, instead of placing key JSON in tracked project paths
- Rationale: reduces accidental git exposure and keeps credential handling aligned with local-secret overlay model
- Alternatives considered: store key directly under workspace setup path as canonical source; embed key content in encrypted project JSON now
- Impacted files: _infra/env/.env.local (ignored), docs/programs/zero_to_hero/CLOUD_ACCOUNT_REGISTRY.md, docs/programs/zero_to_hero/MIGRATION_BOARD.md, agents/shared/open_loops.md, agents/shared/task_register.md

- Date: 2026-04-02
- Decision ID: DEC-017
- Task ID: TB-20260402-20
- Decision: adopt encrypted-secrets-as-system-of-record handling for sensitive values with seed-backed direct update command
- Rationale: preserve sensitive data hygiene while removing repeated confirmation friction; enables fast local secret updates without plaintext drift
- Alternatives considered: continue manual plaintext secret files then encrypt; keep passing secrets only via transient shell env variables
- Impacted files: scripts/env/env_core.ps1, scripts/env/set_secret.ps1, docs/operations/secrets_workflow.md, docs/programs/zero_to_hero/CLOUD_ACCOUNT_REGISTRY.md, docs/programs/zero_to_hero/MIGRATION_BOARD.md, agents/shared/context_index.md

- Date: 2026-04-02
- Decision ID: DEC-018
- Task ID: TB-20260402-32
- Decision: execute M-002 coding migration as script-driven copy-validate-delete workflow with short-term backup snapshot
- Rationale: enables deterministic large-scale migration with reproducible artifacts and immediate source decommission while preserving rollback safety
- Alternatives considered: copy-only without deletion; ad-hoc manual move; direct move without backup
- Impacted files: scripts/migration/run_m002_coding_assets.ps1, docs/programs/zero_to_hero/CODING_ASSETS_MIGRATION_SOLUTION.md, docs/programs/zero_to_hero/MIGRATION_BOARD.md, coding_challenges/_migration_meta/run_20260402_113935/*

- Date: 2026-04-02
- Decision ID: DEC-019
- Task ID: TB-20260402-33
- Decision: treat `coding_challenges` manifests and v1 docs as canonical planning inputs for next study-manual/roadmap generation cycles
- Rationale: ensures future agents regenerate plans from deterministic migration artifacts instead of ad-hoc assumptions
- Alternatives considered: generate roadmaps directly from chat-only context; defer manual/roadmap drafting
- Impacted files: coding_challenges/INDEX.md, coding_challenges/ROADMAP_INPUT_MANIFEST.md, coding_challenges/leetcode/TOPIC_COVERAGE.md, coding_challenges/STUDY_MANUAL_V1.md, coding_challenges/ROADMAP_DRAFT_V1.md, agents/shared/context_index.md

- Date: 2026-04-02
- Decision ID: DEC-020
- Task ID: TB-20260402-34
- Decision: execute M-012 as copy-and-sanitize migration (no source deletion) with deterministic run artifacts under tracks/08_databases/_migration_meta
- Rationale: preserves reversible migration while enforcing secret-safe legacy prompt ingestion into StudyBook
- Alternatives considered: direct source move/delete in same run; ad-hoc manual copy without evidence artifacts
- Impacted files: scripts/migration/run_m012_databases_assets.ps1, docs/programs/zero_to_hero/MIGRATION_BOARD.md, tracks/08_databases/*, _prompts/legacy/databases/*, tracks/08_databases/_migration_meta/run_20260402_120828/*

- Date: 2026-04-02
- Decision ID: DEC-021
- Task ID: TB-20260402-36
- Decision: execute a combined migration wave for Technologies notebooks/prompts and DE interview assets with deterministic conflict-safe naming, and decommission `D:\Workspace\ML_AI` immediately after validated move
- Rationale: reduces migration latency by batching tightly-coupled sources while preserving auditability and safe cutover through run artifacts, backup snapshot, and secret-scan gate
- Alternatives considered: run each item as separate waves; overwrite conflicts in-place; defer ML_AI source deletion to a later cleanup run
- Impacted files: scripts/migration/run_m011_m013_m008_mlai.ps1, docs/programs/zero_to_hero/MIGRATION_BOARD.md, agents/shared/open_loops.md, agents/shared/task_register.md, temp/migration_meta/run_20260402_121903/*

- Date: 2026-04-02
- Decision ID: DEC-022
- Task ID: TB-20260402-37
- Decision: use migration move-map as the only delete authority for source decommission of Technologies and DE interview assets, including `conflict_renamed` records
- Rationale: guarantees deletions remain restricted to explicitly migrated items and avoids accidental removal of non-migrated workspace content
- Alternatives considered: delete entire source folders; delete only `copied` rows and leave conflict-renamed prompt sources
- Impacted files: temp/migration_meta/run_20260402_121903/delete_tech_deinterview_report.json, docs/programs/zero_to_hero/MIGRATION_BOARD.md, agents/shared/task_register.md, agents/shared/open_loops.md

- Date: 2026-04-02
- Decision ID: DEC-023
- Task ID: TB-20260402-40
- Decision: `infra_up.ps1` must auto-clean conflicting legacy containers created from `D:\Workspace` compose projects before starting StudyBook services
- Rationale: prevents cross-project container-name collisions and stale host bind paths from breaking portable startup on machines without legacy drive/path layouts
- Alternatives considered: manual docker rm cleanup each time; keep legacy and StudyBook service names divergent only
- Impacted files: _infra/scripts/infra_up.ps1, _infra/README.md, agents/shared/task_register.md, agents/shared/agent_status.md

- Date: 2026-04-02
- Decision ID: DEC-024
- Task ID: TB-20260402-41
- Decision: Seed-backed passphrase entered ONCE per machine during seed registration - NEVER ask user for passphrase again
- Rationale: DPAPI-encrypted seed file (`config/secrets/.local/studybook.secret.seed.dpapi.json`) auto-provides passphrase to env_setter.ps1 on every run; re-prompting violates the seed-backed security model and creates unnecessary friction
- Alternatives considered: continue prompting for passphrase each session; store passphrase in plaintext env var
- Impacted files: agents/QWEN_AGENT_HANDOFF.md, agents/AGENT_CHEATSHEET.md, agents/shared/context_index.md, scripts/env/env_core.ps1
