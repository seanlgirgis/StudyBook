# StudyBook ZeroToHero Migration Board

## Status Values
- `todo`
- `in_progress`
- `blocked`
- `done`

## Priority Values
- `P0` critical path
- `P1` high
- `P2` normal
- `P3` optional

## Item Types
- `infra`
- `security`
- `migration`
- `creation`
- `validation`
- `documentation`

## Master Backlog

| Item ID | Priority | Type | Scope | Source Path | Target Path | Validation | Status | Evidence / Notes |
|---|---|---|---|---|---|---|---|---|
| I-001 | P0 | infra | Compose orchestrator and split files | `D:\Workspace\Technologies\_setup` + `D:\Workspace\Basics\Databases\_setup` | `D:\StudyBook\_infra\docker` | `docker compose config` | done | `core.yml`, `streaming.yml`, `pipeline.yml`, `observability.yml`, `docker-compose.yml` created and render validated |
| I-002 | P0 | infra | Env contract and runtime scripts | n/a | `D:\StudyBook\_infra\env` + `D:\StudyBook\_infra\scripts` | script parse + run checks | done | `.env.example` + `infra_up.ps1`, `infra_down.ps1`, `infra_seed.ps1` added |
| I-003 | P0 | infra | Idempotent seeding layer | `master_seed_data.py` + `seed_tech_telemetry.py` | `D:\StudyBook\_infra\seeds` | seed scripts present and deterministic | done | `seed_core.py` and `seed_tech_telemetry.py` added |
| I-004 | P0 | validation | Infra health verification pack | live Docker stack | `D:\StudyBook\_infra\scripts\infra_health.ps1` | `infra_health.ps1 -AsJson` exits 0 | done | live stack check passed for all configured services |
| I-005 | P0 | security | Remove plaintext credentials from migrated docs/prompts/notebooks | workspace-derived assets | migrated StudyBook artifacts | credential scan and manual review | todo | enforced as migration gate before broad prompt/notebook lift |
| C-001 | P0 | documentation | Cloud account registry baseline (non-secret) | n/a | `D:\StudyBook\docs\programs\zero_to_hero\CLOUD_ACCOUNT_REGISTRY.md` | registry file exists with required fields | done | provider table + env-key mapping added |
| C-002 | P0 | security | Map cloud secrets to encrypted env flow | `config/secrets/*.enc.json` + local `.env.local` overlays | runtime env contract | key presence checks recorded | in_progress | MongoDB Atlas captured locally; GCP real key captured in protected local path and wired in `.env.local`; AWS local profiles discovered; encrypted AWS bundle created (`config/secrets/aws.profiles.secrets.enc.json`) and AWS encrypt/restore scripts added; remaining providers pending |
| C-003 | P1 | validation | Snowflake read-only connectivity check | cloud account metadata + encrypted secrets | `poc/connection_proofs/python/snowflake_connection_proof.py` | command succeeds or records blocker | blocked | 2026-04-02 proof resolves encrypted SNOWFLAKE_* values but returns connector error `250001 Could not connect to Snowflake backend after 2 attempt(s)`; network/account validation needed |
| C-004 | P1 | validation | Redshift read-only connectivity check | cloud account metadata + encrypted secrets | `_infra/scripts` check script | command succeeds or records blocker | todo | gated by C-002 |
| C-005 | P2 | validation | Databricks workspace readiness check | cloud account metadata + encrypted secrets | `poc/connection_proofs/python/databricks_connection_proof.py` | command succeeds or records blocker | done | 2026-04-02 proof run returned `ok: true`; `/api/2.0/current-user/me` returned 404 on this workspace while fallback `/api/2.0/clusters/list` succeeded (200) with encrypted secret-backed host/token |
| M-001 | P0 | migration | Inventory and classify legacy assets | `D:\Workspace` + transcript | StudyBook migration docs | each asset tagged by class | done | extraction + class model documented in placement plan |
| M-002 | P0 | migration | Shift/lift coding challenge roadmaps | workspace challenge assets | `D:\StudyBook\coding_challenges` | spot-check moved files | todo | move only non-duplicate canonical files |
| M-003 | P0 | migration | Shift/lift proven notebooks (Technologies + Databases first) | `D:\Workspace\Technologies` + `D:\Workspace\Basics\Databases` | `D:\StudyBook\tracks` + `D:\StudyBook\interview` | notebook smoke runs | todo | prioritize explicitly validated notebooks |
| M-004 | P1 | migration | Shift/lift prompt packs for active tracks | `D:\Workspace\...\prompts` | `D:\StudyBook\_prompts\legacy` + `D:\StudyBook\_prompts\tracks` | prompt contract checks | todo | migrate legacy first, derive canonical second |
| M-005 | P1 | creation | Create missing R1 prompts (active tracks only) | n/a | `D:\StudyBook\_prompts\tracks\*` | prompt lint/manual review | todo | create only after migration inventory confirms missing |
| M-006 | P1 | creation | Create missing notebooks (active tracks only) | n/a | `D:\StudyBook\tracks\*` | notebook opens + minimal runtime check | todo | no empty scaffolding policy |
| M-007 | P2 | migration | Shift/lift capstone assets | workspace capstone sources | `D:\StudyBook\capstone` | capstone smoke checks | todo | dependency: stable infra + prompt contracts |
| M-008 | P2 | migration | Shift/lift interview assets | workspace interview sources | `D:\StudyBook\interview` | markdown/notebook completeness checks | todo | dependency: M-003 |
| M-009 | P0 | documentation | Extract value from `TalksWithClaude` and produce placement map | `D:\StudyBook\temp\TalksWithClaude.md` | `docs/programs/zero_to_hero/TALKS_WITH_CLAUDE_EXTRACT_AND_SHIFT_LIFT_PLAN.md` | extraction doc complete | done | transcript mined and cross-checked with workspace inventory |
| M-010 | P0 | migration | Shift/lift infra compose + seed assets | workspace setup files | `D:\StudyBook\_infra\docker` + `D:\StudyBook\_infra\seeds` | compose config + health check | done | live stack alignment confirmed via `docker ps` + health script |
| M-011 | P0 | migration | Shift/lift validated Technologies R1/R3 notebooks | `D:\Workspace\Technologies\*.ipynb` | `D:\StudyBook\tracks\10/11/12/22/29/30` + `interview` | notebook smoke runs per track | todo | next migration critical path |
| M-012 | P1 | migration | Shift/lift Databases notebooks + prompt packs | `D:\Workspace\Basics\Databases\*.ipynb` + prompts | `D:\StudyBook\tracks\08_databases` + `_prompts\legacy\databases` | schema/seed precheck + smoke runs | todo | run after M-011 |
| M-013 | P1 | migration | Shift/lift Technologies prompts into legacy archive and derive canonical prompts | `D:\Workspace\Technologies\prompts\R1/R2/R3` | `D:\StudyBook\_prompts\legacy\technologies` + `_prompts\tracks` | prompt contract checks | todo | sanitize secrets before canonical derivation |
| M-014 | P0 | security | Block secret-bearing files from migration and sanitize hardcoded creds | `tech.env`, `gcp_key.json`, prompt/notebook literals | migrated StudyBook artifacts | secret scan + manual review | in_progress | registry + guardrails set; migration-phase scans pending |
| A-001 | P0 | documentation | Agent handoff index and continuity discipline | StudyBook control docs | `agents/shared/*` + program docs | new agent can resume without chat | in_progress | control artifacts active and maintained each run |
| A-002 | P1 | validation | End-to-end dry run from clean shell | infra scripts + seeds + one migrated notebook | `D:\StudyBook` | scripted run transcript | todo | run after M-011 |

## Batch Execution Log

| Batch ID | Focus | Included Item IDs | Entry Criteria | Exit Criteria | Status | Notes |
|---|---|---|---|---|---|---|
| BATCH-INFRA-01 | Compose/env/scripts foundation | I-001, I-002 | source setup assets identified | compose renders + startup scripts available | done | foundation complete in StudyBook `_infra` |
| BATCH-INFRA-02 | Seed and health checks | I-003, I-004 | foundation complete | health check exits 0 on live stack | done | `infra_health.ps1 -AsJson` validated against live containers |
| BATCH-SEC-01 | Credentials and cloud metadata hardening | I-005, C-001, C-002 | infra baseline complete | cloud metadata documented and secret routing verified | in_progress | registry done, key mapping population pending |
| BATCH-MIG-00 | Transcript extraction and placement map | M-009 | transcript available | placement plan completed | done | done in StudyBook docs |
| BATCH-MIG-01A | Infra shift/lift from workspace setup assets | M-010 | setup files confirmed | `_infra` compose + seeds implemented and validated | done | aligned with live Docker stack |
| BATCH-MIG-02A | Validated notebook shift/lift | M-011 | infra baseline passing | validated notebooks moved and smoke-tested | todo | next execution batch |
| BATCH-MIG-03A | Prompt shift/lift and canonical derivation | M-012, M-013, M-014 | notebook migration stable | legacy prompts archived + canonical prompts created + secret gate passed | todo | security gate cannot be skipped |
| BATCH-VERIFY-01 | Rebuildability proof | A-001, A-002 | P0 migration items complete | clean-shell reproducibility proof complete | todo | final acceptance batch |

## Move Map Template

| Move ID | Artifact Type | Source | Target | Class | Batch ID | Validation | Status |
|---|---|---|---|---|---|---|---|
| MOVE-0001 | notebook | `<fill>` | `<fill>` | `migrate_as_is` | `<fill>` | notebook smoke run | todo |
| MOVE-0002 | prompt | `<fill>` | `<fill>` | `migrate_with_adaptation` | `<fill>` | prompt contract check | todo |
| MOVE-0003 | script | `<fill>` | `<fill>` | `create_new` | `<fill>` | script execution | todo |

## Agent Handoff Checklist Per Run
- Confirm current `in_progress` batch items.
- Execute one scoped objective.
- Record command outputs used for validation.
- Update item status + evidence in this board.
- Overwrite `agents/shared/agent_status.md` before ending run.









