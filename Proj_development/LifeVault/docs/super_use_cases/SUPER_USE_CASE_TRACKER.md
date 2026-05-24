# SUPER_USE_CASE_TRACKER.md

## Purpose

Living planning board for major/super LifeVault capabilities. This tracker is intentionally 1000-foot and does not replace detailed child UC specs.

## Status Legend

- `idea`
- `planned`
- `in_design`
- `implemented_v0`
- `validated_once`
- `accepted_v1`
- `deferred`

## Tracker Table

| ID | Name | Short description | Inputs | Outputs | Current status | Child use cases / related UCs | Priority | Notes / open questions |
|---|---|---|---|---|---|---|---|---|
| SUC_001 | Universal Capture / Ingest | Capture folders/files/notes/URLs/media/code into controlled intake with provenance | source inputs, story/context, approvals | proposals/intake artifacts/pods and intake audit trail | planned / partial | UC_001, UC_003 and future ingest adapters | P0 | Proven vertical exists via folder lifecycle; broaden adapters next |
| SUC_002 | Vault Item Classification, Story, Tags, and Lifecycle | Attach story, tags, sensitivity, lifecycle meaning to any vault_item | item metadata, operator decisions | classification + lifecycle metadata | planned | UC_002-lite, UC_006, UC_006B and future tag workflows | P0 | Add hot/warm/cold defaults and policy objects |
| SUC_003 | Storage Location and Multi-Copy Management | Track where each item/member copy lives across pod/vault/backup/cloud later | file/member records, storage roots | managed location map and copy states | planned | UC_004, UC_007, UC_008, UC_009 | P0 | Multi-destination needs richer storage entity model |
| SUC_004 | Search, Retrieve, Hydrate, and Open | Search metadata and safely retrieve/open with controlled hydration | query, filters, retrieve scope | search results, retrieval/open actions | planned | UC_005 and future retrieve/open workflows | P0 | Hydrate/open policy boundaries pending |
| SUC_005 | Notes and Knowledge Memory | First-class notes/note-folders with portable markdown packages and assets | notes, note folders, assets, metadata | searchable notes memory | in_design | `docs/super_use_cases/SUC_005_NOTES_AND_KNOWLEDGE_MEMORY.md`, note contracts, future note workflows | P1 | v0 design contracts complete; implementation deferred |
| SUC_006 | File and Folder Lifecycle | End-to-end lifecycle from intake to quarantine for file/folder workloads | folder/file inputs, approvals, DB, storage roots | proposals, pods, publish/verify/quarantine artifacts | implemented_v0 / validated_once | UC_001, UC_002-lite, UC_003, UC_004, UC_005, UC_006, UC_006B, UC_007, UC_008, UC_009 | P0 | This is the first proven vertical slice; not the entire product |
| SUC_007 | Images, Scans, OCR, and Visual Memory | Manage image/scan inventory and OCR-later flows | media folders, scan policy | visual metadata, OCR backlog/results | idea | future media/OCR workflows | P2 | OCR privacy/storage policy needed |
| SUC_008 | Code and Project Archive | Ingest code/project folders with secret-safe filters and project metadata | code roots, ignore rules, project story | searchable code archive metadata | planned | UC_010 + future code workflows | P1 | Default ignore and secret heuristics pending |
| SUC_009 | Binary and Media Archive | Govern binaries/installers/archives/media as durable inventory | binary/media inputs, retention policy | archive inventory and location tracking | planned | future binary/media workflows | P1 | Large artifact handling policy pending |
| SUC_010 | Secrets and Sensitive Records | Govern sensitive records and secret references with strict controls | sensitive records, secret references, policy | controlled sensitive records and review states | in_design | UC_011 + `docs/security/LIFEVAULT_SENSITIVE_NOTE_V0_CONTRACT.md` | P1 | v0 sensitive-note contract + unlock policy documented |
| SUC_011 | Job, Career, and Document Records | Organize resumes/forms/offers/certifications with timeline context | job docs, story/timeline metadata | structured career records memory | planned | file lifecycle + future domain flows | P1 | Define domain templates and retention defaults |
| SUC_012 | AI Prompts, Agent Skills, and Config Memory | Store prompts/agent configs/skills as reusable memory assets | prompts, skills, configs | searchable prompt/skill/config catalog | planned / partial | LV skill orchestration and future config workflows | P0 | Establish version/provenance pattern |
| SUC_013 | Backup, Restore, Portability, and Multi-Machine | Operational resilience and safe movement across machines | DB backups, machine configs, restore policy | backups/checksums/restore readiness | implemented_v0 / partial | backup scripts + future restore drills | P0 | Expand formal disaster-recovery drills |
| SUC_014 | Encryption, Decryption, and Secure View | Add encryption layers and controlled decrypt/use sessions | vault files, key policy, secure view policy | encrypted artifacts and secure-view outputs | in_design | `docs/security/LIFEVAULT_ENCRYPTION_V0_DESIGN.md`, `docs/security/LIFEVAULT_UNLOCK_SESSION_POLICY.md` | P1 | v0 target is sensitive notes first; cloud-sensitive lanes remain deferred |
| SUC_015 | Streamlit Control Center / Agent Console | UI layer to guide workflows, display status, and operator actions | DB state, scripts, operator actions | dashboard/workflow console/reports | planned | future Streamlit/control-center workflows | P1 | Start read-only dashboard early |
| SUC_016 | Reporting, Audit, and Governance | Produce governance reports and lifecycle observability | DB filters, report definitions | CSV/JSON/markdown reports and audit summaries | planned | report/export workflows | P1 | Define canonical report pack |
| SUC_017 | Cleanup, Retention, and Space Recovery | Govern quarantine retention and eventual deletion candidates | cleanup decisions, retention policy, verification status | quarantine manifests and recovery actions | planned / partial | UC_009 + future retention/delete workflows | P1 | Permanent delete remains deferred |
| SUC_018 | Physical Storage Inventory | Track physical containers/items with recursive containment | physical item/container entries, location metadata | searchable physical inventory and location map | planned | future physical inventory workflows | P1 | Keep physical containment separate from general item tree |
| SUC_019 | Contacts and People Vault | Import and organize contacts with dedup and notes | contact exports, notes, merge decisions | contacts vault and duplicate review groups | planned | future contacts workflows | P1 | Fast import first, cleanup later |
| SUC_020 | Email and Attachment Vault | Parse/import email sources and promote valuable threads/attachments | mbox/import sources, parsing policy | message/thread/attachment records and summaries | planned | future email workflows | P1 | No mailbox deletion in early phases |
| SUC_021 | Tasks, Projects, and Maintenance Queues | Model project->task group->task with maintenance queues | operator tasks, system-generated maintenance items | actionable task queues and tracking notes | in_design | `docs/super_use_cases/SUC_021_TASKS_PROJECTS_MAINTENANCE_QUEUES.md` and future task/project workflows | P0 | Intake date required; due date optional |

## Brainstorm Backlog

- Should SUC_006 be re-run on a second tiny safe folder before deeper SUC_002/SUC_005 work?
- What is final multi-destination storage policy?
- What should be copied vs moved by default across capability lanes?
- What is `hot` by default across item types?
- Which item types can be plaintext at rest before encryption phase?
- What belongs in LifeVault vs password manager for secrets handling?
- What should Streamlit control center show first?
