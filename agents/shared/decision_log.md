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
