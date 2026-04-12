# Open Loops

Track incomplete but in-scope work items so sessions resume cleanly.

Last reviewed: 2026-04-12 (seed + decrypt + handoff guide)

## Status Meanings

- `open`
- `in_progress`
- `blocked`
- `closed`

## Items

| Loop ID | Related Task ID | Item | Status | Next Action | Updated On |
|---|---|---|---|---|---|
| LOOP-001 | TB-20260401-01 | Add approval matrix and command allowlist policy files | closed | none | 2026-04-01 |
| LOOP-002 | TB-20260401-04 | Create encrypted secrets files for shared and per-machine profiles | closed | none | 2026-04-01 |
| LOOP-003 | TB-20260401-07 | Promote imported legacy credentials into encrypted StudyBook secret files | closed | none | 2026-04-01 |
| LOOP-004 | TB-20260402-07 | Execute notebook migration backlog for validated Technologies set (`M-011`) | closed | none | 2026-04-02 |
| LOOP-005 | TB-20260402-06 | Complete cloud secret routing + migration secret sanitization gate (`C-002`, `M-014`) | in_progress | Secret-scan gate passed for M-011/M-013/M-008/ML_AI run (`secret_hits=0`); continue provider secret mapping + remaining migration waves | 2026-04-02 |
| LOOP-006 | TB-20260402-08 | Create Docker service dictionary with concise purpose notes per service | closed | none | 2026-04-02 |
| LOOP-007 | TB-20260402-09 | Migrate MongoDB credential from local .env.local into encrypted secret files and rotate Atlas password/token | open | Run bootstrap encryption with passphrase and then rotate MongoDB password | 2026-04-02 |
| LOOP-008 | TB-20260402-11 | Normalize legacy workspace GCP key placeholders after secure key ingestion | in_progress | Decide if legacy hardcoded path is still required; if not, delete placeholder duplicates in `D:\Workspace\Technologies\_setup` | 2026-04-02 |
| LOOP-009 | TB-20260402-12 | Add connection proofs POC scripts for MongoDB and GCP | closed | none | 2026-04-02 |
| LOOP-010 | TB-20260402-13 | Improve Mongo proof diagnostics to troubleshoot Atlas TLS failures | closed | none | 2026-04-02 |
| LOOP-011 | TB-20260402-14 | Clear push-protection secret violation from outgoing commit range | closed | none | 2026-04-02 |
| LOOP-012 | TB-20260402-15 | Align GCP proof pass/fail logic with partial API availability and add strict toggle | closed | none | 2026-04-02 |
| LOOP-013 | TB-20260402-16 | Encrypt AWS profile bundle into StudyBook secrets for cross-machine restore | closed | Bundle created and plaintext removed | 2026-04-02 |
| LOOP-014 | TB-20260402-17 | Enable machine-local seed-backed secret passphrase resolution for noninteractive agent runs | closed | Seed file registered and env bootstrap validated with passphrase env var unset | 2026-04-02 |
| LOOP-015 | TB-20260402-18 | Finish Azure proof documentation and registry status alignment | closed | README/env template/registry updated and validated | 2026-04-02 |
| LOOP-016 | TB-20260402-19 | Complete Databricks proof by generating PAT and storing DATABRICKS_TOKEN in local secret/env flow | closed | none | 2026-04-02 |
| LOOP-017 | TB-20260402-25 | Complete Snowflake proof after backend-connect blocker (`250001`) by validating network/account policy and rerunning read-only proof | closed | none | 2026-04-02 |
| LOOP-018 | TB-20260402-27 | Run Docker exec portions of new group POCs from owner shell (sandbox here has docker API permission limits) and capture any service-specific fixes | closed | none | 2026-04-02 |
| LOOP-019 | TB-20260402-29 | Add portable JupyterLab Docker service and proof coverage | closed | none | 2026-04-02 |

| LOOP-020 | TB-20260402-32 | Execute coding assets shift/lift and decommission migrated D:\Workspace sources | closed | none | 2026-04-02 |
| LOOP-021 | TB-20260402-33 | Produce first manuals/roadmaps-ready docs from coding_challenges manifests | closed | none | 2026-04-02 |
| LOOP-022 | TB-20260402-34 | Complete Databases shift/lift from Workspace into tracks/08_databases and _prompts/legacy/databases | closed | none | 2026-04-02 |
| LOOP-023 | TB-20260402-36 | Reconcile duplicate-suffixed Technologies legacy prompts produced during conflict-safe migration | open | Review `D:\StudyBook\temp\migration_meta\run_20260402_121903\conflicts_report.md` and decide keep-vs-dedupe policy for `__dupNNN` files | 2026-04-02 |
| LOOP-024 | TB-20260402-37 | Decommission migrated Technologies + DE_Interview sources using move-map safe deletion | closed | none | 2026-04-02 |
| LOOP-025 | TB-20260402-38 | Reconcile migration board statuses with completed source-deletion reality for M-003/M-012 and add residual-Technologies decommission plan | open | Decide whether to decommission remaining `D:\Workspace\Technologies` non-migrated assets or retain as legacy runtime island, then update board accordingly | 2026-04-02 |
| LOOP-026 | TB-20260402-41 | Resolve GitHub large-file push rejection for StudyBook main branch | closed | none | 2026-04-02 |
| LOOP-027 | TB-20260403-01 | Validate MongoDB micro-nuggets coverage and record latest fixes/limitations in system-of-record files | closed | none | 2026-04-03 |
| LOOP-028 | TB-20260403-02 | Add MongoDB lane-level runner and verify one-line pass/fail execution output | closed | none | 2026-04-03 |
| LOOP-029 | TB-20260403-03 | Fix Windows cp1252 decode crash in Mongo lane runner subprocess capture | closed | none | 2026-04-03 |
| LOOP-030 | TB-20260403-04 | Validate Mongo runner after cp1252 crash fix with real executions | closed | none | 2026-04-03 |
| LOOP-031 | TB-20260403-05 | Harden PostgreSQL nugget lane after review findings | closed | none | 2026-04-03 |

| LOOP-032 | TB-20260403-06 | Fix Airflow micro-nuggets lane regressions and setup runner behavior | closed | none | 2026-04-03 |
| LOOP-033 | TB-20260403-07 | Fix Kafka micro-nuggets consumer crashes from invalid payload decoding | closed | none | 2026-04-03 |
| LOOP-034 | TB-20260403-08 | Stabilize Spark Structured Streaming micro-nuggets on Windows (NativeIO + PySpark compatibility) | closed | none | 2026-04-03 |
| LOOP-035 | TB-20260403-09 | Replace Spark lane run-all with explicit guard script | closed | none | 2026-04-03 |
| LOOP-036 | TB-20260403-10 | Create micro-nuggets possible-list docs across active track roots | closed | none | 2026-04-03 |
| LOOP-037 | TB-20260403-11 | Evaluate JobSearch location strategy and write decision memo | closed | none | 2026-04-03 |
| LOOP-038 | TB-20260403-12 | Make JobSearch path configurable per machine and add StudyBook launch wrappers | closed | none | 2026-04-03 |
| LOOP-039 | TB-20260403-13 | Parse and internalize JobSearch resume source-of-truth plus website repo context | closed | none | 2026-04-03 |
| LOOP-040 | TB-20260403-14 | Register daily DE job-search engine protocol and startup phrase | closed | none | 2026-04-03 |
| LOOP-041 | TB-20260404-01 | Replace JobSearch springboard pattern with assistant-driven direct-mode contract using relative paths | closed | none | 2026-04-04 |
| LOOP-042 | TB-20260404-02 | Simplify direct-mode artifact naming to fixed 4-file output plus non-versioned intermediates | closed | none | 2026-04-04 |
| LOOP-043 | TB-20260404-03 | Enforce triage-first job processing gate for JobSearch direct mode | closed | none | 2026-04-04 |


| LOOP-044 | TB-20260404-04 | Generate tailored artifacts for Dynatrace Solutions Engineer posting and render final files | closed | none | 2026-04-04 |

| LOOP-045 | TB-20260404-05 | Build durable job-site login skill to prevent credential-key confusion | closed | none | 2026-04-04 |

| LOOP-046 | TB-20260404-06 | Persist canonical job-site credential workflow in agent files and operations docs | closed | none | 2026-04-04 |

| LOOP-047 | TB-20260404-07 | Record confirmed application submission for Dynatrace job in tracker metadata | closed | none | 2026-04-04 |

| LOOP-048 | TB-20260404-08 | Generate KSA-targeted tailored resume for Dynatrace job with Arabic fluency | closed | none | 2026-04-04 |

| LOOP-049 | TB-20260404-10 | Generate Sigma tailored resume and cover artifacts from intake job | closed | none | 2026-04-04 |

| LOOP-050 | TB-20260404-13 | Remove current Garner Health intake package from tracking system | closed | none | 2026-04-04 |

| LOOP-051 | TB-20260404-18 | Process Inclusion Cloud intake and produce full tailored artifacts | closed | none | 2026-04-04 |

| LOOP-052 | TB-20260404-19 | Build and validate Google Doc secret-message decoder script and run it on provided URL | closed | none | 2026-04-04 |

| LOOP-052 | TB-20260405-01 | Create assessment practice-question document for tomorrow prep | closed | none | 2026-04-05 |

| LOOP-053 | TB-20260405-02 | Create Two Sum training folder and reusable harness with edge cases | closed | none | 2026-04-05 |

| LOOP-054 | TB-20260405-03 | Create heap/min-heap assessment micro-nuggets lane with negation-based max-heap pattern | closed | none | 2026-04-05 |

| LOOP-055 | TB-20260405-04 | Review and harden agent seed-decryption guidance for sandbox/user-context mismatch handling | closed | none | 2026-04-05 |

| LOOP-056 | TB-20260405-05 | Add cross-machine seed-context reminder doc for DPAPI CurrentUser mismatch handling | closed | none | 2026-04-05 |
| LOOP-057 | TB-20260405-06 | Build single-file review drill pack (Two Sum, Valid Parentheses, 347 bucket+min-heap) for rapid mock testing | closed | none | 2026-04-05 |
| LOOP-058 | TB-20260405-07 | Fix 347 review harness shape mismatch and tie-handling while preserving practice workflow | closed | none | 2026-04-05 |
| LOOP-059 | TB-20260405-08 | Add next review drill file for ongoing interview training cadence | closed | none | 2026-04-05 |
| LOOP-060 | TB-20260405-09 | Add next practice harness for LeetCode 128 training cadence | closed | none | 2026-04-05 |
| LOOP-061 | TB-20260405-10 | Add next practice harness for LeetCode 238 before full-pack review | closed | none | 2026-04-05 |
| LOOP-062 | TB-20260405-11 | Build first full empty practice round pack for core interview leetcode set | closed | none | 2026-04-05 |
| LOOP-063 | TB-20260405-12 | Build next 4-problem empty training batch to expand interview set to 10 | closed | none | 2026-04-05 |
| LOOP-064 | TB-20260405-13 | Correct mistaken expected output in new Two Sum II training harness | closed | none | 2026-04-05 |
| LOOP-065 | TB-20260405-14 | Provide clean canonical 3Sum reference in separate training file | closed | none | 2026-04-05 |
| LOOP-066 | TB-20260405-15 | Create complete remaining-15 practice pack in one shot per user request | closed | none | 2026-04-05 |
| LOOP-067 | TB-20260406-01 | Improve readability/clarity of round_03 interview drills with richer statement+example headers | closed | none | 2026-04-06 |
| LOOP-068 | TB-20260406-02 | Harden MinStack training file with exception-safe API semantics and richer harness | closed | none | 2026-04-06 |
| LOOP-069 | TB-20260406-03 | Harden LIS training harness to expose incorrect greedy implementations | closed | none | 2026-04-06 |
| LOOP-070 | TB-20260406-04 | Harden round_03 harness quality end-to-end per user request | closed | none | 2026-04-06 |
| LOOP-071 | TB-20260406-05 | Build beginner-friendly graph micro-lessons and practice scaffolds | closed | none | 2026-04-06 |
| LOOP-072 | TB-20260406-06 | Persist preferred YouTube learning channel reminder for future recommendations | closed | none | 2026-04-06 |
| LOOP-073 | TB-20260406-07 | Expand Coin Change training file with multiple solution styles for comparison | closed | none | 2026-04-06 |
| LOOP-074 | TB-20260406-08 | Build single-source index for all tracked LeetCode cases and mapped files | closed | none | 2026-04-06 |
| LOOP-075 | TB-20260406-09 | Expand monotonic-stack practice coverage and index mapping docs | closed | none | 2026-04-06 |

| LOOP-076 | TB-20260406-10 | Review LC496 next-greater implementation quality and edge-safety | closed | none | 2026-04-06 |
| LOOP-077 | TB-20260408-01 | Build guided practice workspace and tracker for repetition coaching | closed | none | 2026-04-08 |
| LOOP-078 | TB-20260410-01 | Stabilize website blog structure visibility and regenerate SEO artifacts | closed | none | 2026-04-10 |
| LOOP-079 | TB-20260410-02 | Persist website search-engine owner-account memory for future submission runs | closed | none | 2026-04-10 |
| LOOP-080 | TB-20260410-03 | Create daily reminder/todo system and seed tomorrow website submission inspection task | closed | none | 2026-04-10 |
| LOOP-081 | TB-20260410-04 | Add day-based LinkedIn posting reminders to daily todo system | closed | none | 2026-04-10 |
| LOOP-082 | TB-20260410-05 | Add multi-channel publishing reminders (X, YouTube, GitHub, Reddit, Medium/Dev.to) to daily todo system | closed | none | 2026-04-10 |
| LOOP-083 | TB-20260411-01 | Switch coding_challenges index output from CSV default to XLSX with deterministic generation | closed | none | 2026-04-11 |
| LOOP-084 | TB-20260411-02 | Preserve manual formatting in coding_challenges/index.xlsx during refresh runs | closed | none | 2026-04-11 |
| LOOP-085 | TB-20260412-01 | Persist durable memory for high-frequency index commands (`refresh_index_and_push.ps1`, `search_index.ps1`) | closed | none | 2026-04-12 |
| LOOP-086 | TB-20260412-02 | Fix PowerShell 5.1 JSON hashtable compatibility in env bootstrap/secret scripts | closed | none | 2026-04-12 |
| LOOP-087 | TB-20260412-03 | Create second-machine Codex handoff doc for seed/env bootstrap recovery | closed | none | 2026-04-12 |
| LOOP-088 | TB-20260409-01 | Restore missing base env config and re-register local seed on new laptop | closed | Added `config/env/base.psd1`; rerun `env_setter.ps1` | 2026-04-12 |
