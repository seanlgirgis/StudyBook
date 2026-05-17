# Task Register

Track active and completed tasks to avoid losing continuity.

## Status Values

- `planned`
- `in_progress`
- `done`
- `blocked`

## Tasks

| Task ID | Summary | Status | Updated On | Notes |
|---|---|---|---|---|
| TB-20260401-01 | Bootstrap control protocol and continuity files | done | 2026-04-01 | Initial setup |
| TB-20260401-02 | Rebalance controls for bounded autonomy and durable memory | done | 2026-04-01 | Added context index and open loops |
| TB-20260401-03 | Add approval matrix and command allowlist controls | done | 2026-04-01 | Closed LOOP-001 |
| TB-20260401-04 | Implement portable machine profiles and encrypted secret bootstrap | done | 2026-04-01 | Added env core scripts and docs |
| TB-20260401-05 | Add guided one-command portable bootstrap script | done | 2026-04-01 | Added `scripts/env/bootstrap_all.ps1` and docs updates |
| TB-20260401-06 | Add architecture-grade ADR governance and tooling | done | 2026-04-01 | Added ADR index, ADR records, and generator script |
| TB-20260401-07 | Import credential inventory from legacy `D:\workspace` into local StudyBook secrets bundle | done | 2026-04-01 | Created source manifest and staging import |
| TB-20260401-08 | Encrypt imported credentials and remove plaintext secret files | done | 2026-04-01 | Created encrypted secret files and deleted plaintext |
| TB-20260401-09 | Add operations runbook folder for self-service usage | done | 2026-04-01 | Added operations guides |
| TB-20260402-01 | Add Claude subscription renewal tracker in operations docs | done | 2026-04-02 | Added subscription runbook |
| TB-20260402-02 | Create ZeroToHero infra-first migration execution system and tracking board | done | 2026-04-02 | Added execution system and migration board |
| TB-20260402-03 | Execute BATCH-INFRA-01 (compose contract and env/startup scripts) | done | 2026-04-02 | Implemented as part of `_infra` baseline completion |
| TB-20260402-04 | Extract TalksWithClaude value and create workspace-to-target shift/lift placement plan | done | 2026-04-02 | Added extraction doc + placement map |
| TB-20260402-05 | Execute infra shift-lift from workspace setup assets into target `_infra` | done | 2026-04-02 | Completed in StudyBook after canonical target correction |
| TB-20260402-06 | Finalize reproducible infra script pack, cloud registry baseline, and StudyBook-only planning retarget | done | 2026-04-02 | Added `_infra/scripts`, cloud registry doc, board/path retarget, health validation |
| TB-20260402-07 | Shift/lift validated Technologies notebooks into canonical StudyBook track paths | done | 2026-04-02 | Completed in combined wave via `scripts/migration/run_m011_m013_m008_mlai.ps1 -Execute`; run_20260402_121903 |
| TB-20260402-08 | Add Docker service dictionary doc and cross-links for agent discoverability | done | 2026-04-02 | Added operations dictionary and linked from infra/operations readmes |
| TB-20260402-09 | Capture MongoDB Atlas credentials into local secure env flow and add provider mapping docs | done | 2026-04-02 | Stored in ignored _infra/env/.env.local; registry updated without plaintext secrets |
| TB-20260402-10 | Verify GCP key readiness and register missing-real-key status in StudyBook tracking docs | done | 2026-04-02 | Confirmed all workspace GCP key files are placeholders; documented exact next action |
| TB-20260402-11 | Ingest real GCP SA key securely and wire StudyBook local env to protected key path | done | 2026-04-02 | Key stored under user-protected folder; .env.local updated with path/project metadata |
| TB-20260402-12 | Create connection proofs POC folder with MongoDB and GCP sample scripts | done | 2026-04-02 | Added read-only proof scripts under poc/connection_proofs/python and updated proof README |
| TB-20260402-13 | Improve MongoDB connection proof diagnostics for Atlas TLS handshake troubleshooting | done | 2026-04-02 | Added SSL/OpenSSL/PyMongo diagnostics and TLS options to mongo proof script |
| TB-20260402-14 | Resolve GitHub push protection block by removing leaked token from local commit history and repushing | done | 2026-04-02 | Rebuilt two local commits without 	emp/TalksWithClaude.md, kept backup branch, push succeeded |
| TB-20260402-15 | Improve GCP connection proof semantics for partial API availability and strict mode fallback | done | 2026-04-02 | Default success now accepts any successful read-only probe; added --require-project-lookup strict mode and clearer diagnostics |
| TB-20260402-16 | Add AWS credential portability workflow and AWS STS connection proof | done | 2026-04-02 | AWS STS check succeeded with local `study`; encrypted bundle created; proof now auto-resolves profiles to avoid hardcoded defaults |
| TB-20260402-17 | Add machine-local DPAPI seed flow for passphrase-free secret decrypt across agent runs | done | 2026-04-02 | Added local seed register/remove scripts, env_core auto-seed passphrase resolution, and validated noninteractive env load |
| TB-20260402-18 | Polish Azure proof wiring across README/env template/registry status | done | 2026-04-02 | Added Azure proof docs, AZURE_* env placeholders, fixed gitignore so `_infra/env/.env.example` is tracked, and updated cloud registry to proof_verified_local |
| TB-20260402-19 | Add Databricks connection proof and wire registry/env/readme metadata | done | 2026-04-02 | Databricks host/email captured, proof script added; blocked for live success until PAT is generated and stored as DATABRICKS_TOKEN |
| TB-20260402-20 | Enforce encrypted-secrets system-of-record flow and add direct seed-backed secret update command | done | 2026-04-02 | Added `set_secret.ps1`, updated secrets workflow/memory, and captured Databricks workspace ID in registry |
| TB-20260402-21 | Fix Databricks proof credential resolution by adding encrypted-secret fallback and validate host autoload | done | 2026-04-02 | Proof now reads host/token from seed-backed encrypted secrets; host injected into asuspc encrypted file; remaining blocker is PAT token value |
| TB-20260402-22 | Add secure prompt mode for seed-backed secret updates and validate Databricks token-missing root cause | done | 2026-04-02 | `set_secret.ps1` now supports `-PromptSecretKey`; validated `DATABRICKS_HOST` present and `DATABRICKS_TOKEN` missing in encrypted secrets |
| TB-20260402-23 | Persist Databricks PAT in encrypted secret records and normalize shared-machine resolution | done | 2026-04-02 | PAT saved to encrypted `asuspc` and `shared` secret files; remaining validation depends on local shell/network reachability |
| TB-20260402-24 | Close Databricks connectivity loop after successful proof and sync registry/board statuses | done | 2026-04-02 | Databricks proof returned `ok: true`; C-005 marked done and LOOP-016 closed |
| TB-20260402-25 | Ingest Snowflake creds into encrypted flow, add Snowflake proof, and scrub plaintext from workspace markdown | done | 2026-04-02 | Encrypted SNOWFLAKE_* captured, proof script added, plaintext scrubbed in target files; connectivity currently blocked on Snowflake backend connect error 250001 |
| TB-20260402-26 | Close Snowflake validation blocker after successful owner-shell proof and sync tracking | done | 2026-04-02 | Snowflake proof now `ok: true`; C-003 marked done and LOOP-017 closed |
| TB-20260402-27 | Add grouped Docker connection POC scripts for all local infra services with simple operations | done | 2026-04-02 | Added core/streaming/pipeline/observability Docker proof scripts + master runner and README mapping |
| TB-20260402-28 | Add individual Python Docker proof scripts per service under poc/connection_proofs/python | done | 2026-04-02 | Added 15 per-service Python Docker proof wrappers plus shared common module and README usage section |
| TB-20260402-29 | Add portable JupyterLab Docker service with StudyBook bind-mount and proof wiring | done | 2026-04-02 | Added jupyterlab to pipeline/full compose with ../../ bind mount, env/doc updates, and Docker proof scripts |

| TB-20260402-32 | Execute M-002 coding assets migration with immediate Workspace decommission | done | 2026-04-02 | Ran scripts/migration/run_m002_coding_assets.ps1 -Execute -DeleteSource; run_20260402_113935 created manifests, backup, and removed scoped D:\Workspace sources |
| TB-20260402-33 | Create first coding challenges study manual and roadmap draft from migrated manifests | done | 2026-04-02 | Added coding_challenges/STUDY_MANUAL_V1.md and coding_challenges/ROADMAP_DRAFT_V1.md based on INDEX/ROADMAP_INPUT_MANIFEST/TOPIC_COVERAGE |
| TB-20260402-34 | Execute M-012 Databases notebook+prompt migration into StudyBook tracks/prompts legacy | done | 2026-04-02 | Ran scripts/migration/run_m012_databases_assets.ps1 -Execute; run_20260402_120828 with 74 moved entries and secret_hits=0 |
| TB-20260402-36 | Execute combined M-011/M-013/M-008 wave and migrate ML_AI pack with source decommission | done | 2026-04-02 | Ran `scripts/migration/run_m011_m013_m008_mlai.ps1 -Execute -DeleteMlAiSource`; run_20260402_121903, move_map_entries=277, secret_hits=0, ML_AI source deleted |
| TB-20260402-37 | Delete migrated Technologies and DE interview sources using move-map safe decommission | done | 2026-04-02 | Deleted 163 mapped files (`copied` + `conflict_renamed`) from `D:\Workspace\Technologies` + `D:\Workspace\Basics\DE_Interview`; report: `temp/migration_meta/run_20260402_121903/delete_tech_deinterview_report.json` |
| TB-20260402-38 | Run second-pass migration inventory audit versus roadmap and identify remaining gaps | done | 2026-04-02 | Audited board statuses vs live Workspace/StudyBook paths; confirmed Databases source fully cleared, Technologies residuals remain, and listed outstanding roadmap items |
| TB-20260402-39 | Register Snowflake micro-nuggets lane in durable memory/system-of-record files | done | 2026-04-02 | Confirmed and recorded `D:\StudyBook\tracks\08_databases\micro_nuggets\snowflake` structure (00_setup, 02_ddl_basics, 03_dml_basics, helper + summary) |
| TB-20260402-40 | Fix de_postgres legacy Workspace bind failure and enforce path-agnostic StudyBook infra startup cleanup | done | 2026-04-02 | Updated `_infra/scripts/infra_up.ps1` to auto-remove legacy Workspace compose containers; validated `de_postgres` now uses `de_postgres_data` volume from `D:\StudyBook\_infra\docker\core.yml` |
| TB-20260402-41 | Resolve GitHub push rejection caused by oversized runtime artifacts in tracked paths | done | 2026-04-02 | Rebuilt local commit without `tracks/08_databases/_setup/volumes` and `_artifacts`, added ignore guards, and pushed `main` successfully (`d7fe08b`) |
| TB-20260403-01 | Review MongoDB micro-nuggets coverage and record fixes in durable memory files | done | 2026-04-03 | Verified lane breadth/depth, added coverage review doc, and updated context/open-loop/status continuity artifacts |

| TB-20260403-02 | Add MongoDB lane runner script with one-line pass/fail output and validate execution | done | 2026-04-03 | Added run_all_mongodb_nuggets.py; validated output format; sandbox run failed on Atlas DNS resolution (not script logic) |
| TB-20260403-03 | Fix Mongo lane runner Windows decode crash on subprocess output | done | 2026-04-03 | Switched runner to byte capture and UTF-8 decode with replacement to prevent cp1252 decode thread crash |
| TB-20260403-04 | Test Mongo lane runner end-to-end and fix Windows console encoding crash | done | 2026-04-03 | Reproduced UnicodeEncodeError on cp1252, patched safe console printing, reran stop-on-fail and full-loop timeout sweep successfully |
| TB-20260403-05 | Harden PostgreSQL micro-nuggets for idempotency, portability, and runner reliability | done | 2026-04-03 | Fixed seed idempotency, runner encoding safety, capstone rerun safety, path/credential source portability; validated full run (16/16 PASS) |

| TB-20260403-06 | Harden Airflow micro-nuggets lane for setup resiliency, API compatibility, and accurate runner status | done | 2026-04-03 | Fixed setup skip-vs-fail semantics, added retries, improved portability, and validated full run (14 pass, 2 skip, 0 fail) |
| TB-20260403-07 | Review and harden Kafka micro-nuggets lane for poisoned/non-JSON payload resilience | done | 2026-04-03 | Added safe deserializer and updated failing scripts; full run passed (29/29) |
| TB-20260403-08 | Harden Spark Structured Streaming micro-nuggets for Windows-safe execution and remove noisy NativeIO failure paths | done | 2026-04-03 | Added fallback batch paths and compatibility fixes; user-validated scripts 01-08 passed |
| TB-20260403-09 | Disable Spark Structured Streaming run-all and replace with one-by-one guidance script | done | 2026-04-03 | Replaced runner with explicit non-run-all guard message and safe execution order |
| TB-20260403-10 | Add possible micro-nuggets listing docs under track micro_nuggets roots plus master catalog | done | 2026-04-03 | Added 4 catalog docs covering databases/streaming/orchestration ideas and priority order |
| TB-20260403-11 | Assess C:\jobsearch and decide keep-vs-lift into StudyBook with documented recommendation | done | 2026-04-03 | Added operations decision memo; recommended federated single-launchpad model |
| TB-20260403-12 | Add machine-configurable JobSearch root and StudyBook launcher wrappers | done | 2026-04-03 | Added STUDYBOOK_JOBSEARCH_ROOT to machine configs, open/run wrapper scripts, and launchpad runbook |
| TB-20260403-13 | Parse JobSearch source_of_truth.json and document durable JobSearch+website context for future resume/site support | done | 2026-04-03 | Updated user_profile.md with source-backed profile; added docs/operations/JOBSEARCH_SOURCE_OF_TRUTH_AND_WEBSITE_CONTEXT.md |
| TB-20260403-14 | Register daily DE job-search operating plan (5-10 apps/day) with tithe training loop and trigger phrase | done | 2026-04-03 | Added docs/operations/JOB_SEARCH_DAILY_ENGINE.md and standardized start command |
| TB-20260403-15 | Start Job Search Engine daily run for target 10 and create dated execution sheet | done | 2026-04-03 | Added docs/operations/job_search_sessions/2026-04-03_engine_run.md with scoring tracker + tithe log |
| TB-20260404-01 | Nuke JobSearch springboard mode and switch StudyBook to assistant-driven direct mode with relative-path contract | done | 2026-04-04 | Rewrote direct-mode playbook and replaced process_job_direct.ps1 with local scaffold runner (no external model/script calls) |
| TB-20260404-02 | Simplify JobSearch artifacts to fixed names (resume.md, cover.md, resume.docx, cover.docx) and remove versioned render args | done | 2026-04-04 | Updated render scripts, wrapper, playbook; validated outputs for 00051_5ade9538 |
| TB-20260404-03 | Add 2-stage JobSearch gate (triage before processing) with scripts and playbook commands | done | 2026-04-04 | Added scripts/jobsearch/job_triage.ps1 and process_job_if_apply.ps1; updated playbook |


| TB-20260404-04 | Generate tailored resume/cover artifacts for Dynatrace Solutions Engineer intake and render final md/docx files | done | 2026-04-04 | Created intermediates + rendered resume.md/resume.docx/cover.md/cover.docx for 00054_5d3df4ad; installed python-docx dependency |

| TB-20260404-05 | Create repo skill to standardize job-site credential save/retrieve and prevent key mismatches | done | 2026-04-04 | Added agents/skills/jobsite-login-secrets with SKILL.md, helper scripts, troubleshooting reference, and validated structure |

| TB-20260404-06 | Persist canonical job-site credential workflow in agent files and create operations doc | done | 2026-04-04 | Updated AGENT_CHEATSHEET/QWEN_AGENT_HANDOFF/context_index and added docs/operations/jobsite_credentials_workflow.md with README index link |

| TB-20260404-07 | Sync job tracker after confirmed Dynatrace application submission | done | 2026-04-04 | Updated data/jobs/00054_5d3df4ad/metadata.yaml to APPLIED with company-site method and history entry |

| TB-20260404-08 | Generate KSA-targeted Dynatrace resume with Arabic fluency framing | done | 2026-04-04 | Created job 00055_ab1ea5aa via override and generated tailored resume_intermediate + resume.md/resume.docx |

| TB-20260404-09 | Generate KSA-tailored Dynatrace cover letter artifacts for 00055_ab1ea5aa | done | 2026-04-04 | Created cover_intermediate.json and rendered cover.md/cover.docx with clean audit |

| TB-20260404-10 | Generate Sigma observability-role tailored resume and cover artifacts | done | 2026-04-04 | Created job 00056_64c2ec47 and generated resume/cover intermediates plus final md/docx artifacts |

| TB-20260404-11 | Generate Datadog logs-PSA tailored resume and cover artifacts | done | 2026-04-04 | Created job 00057_7ab6dd61 and generated resume/cover intermediates plus final md/docx outputs |

| TB-20260404-12 | Generate Inspiren Senior Data Engineer tailored resume and cover artifacts | done | 2026-04-04 | Created job 00058_b0233987 and generated resume/cover intermediates plus final md/docx outputs |

| TB-20260404-13 | Remove Garner Health job package 00059_98f8ee28 from system on user request | done | 2026-04-04 | Deleted data/jobs/00059_98f8ee28 and verified path no longer exists |

| TB-20260404-14 | Generate K Anand Data Engineer full tailored package from intake | done | 2026-04-04 | Created job 00059_f3d14aeb with resume/cover intermediates and rendered md/docx outputs |

| TB-20260404-15 | Generate Openmind Data Analyst/Data Engineer full tailored package | done | 2026-04-04 | Created job 00060_978574a5 and generated resume/cover intermediates plus final md/docx outputs |

| TB-20260404-16 | Generate Acunor Databricks Data Engineer full package from intake | done | 2026-04-04 | Created job 00061_c96be38b and generated resume/cover intermediates plus final md/docx outputs |

| TB-20260404-17 | Process HUMAC Dynatrace Administrator intake (override) and generate full package | done | 2026-04-04 | Created job 00062_8df84ee0 and generated resume/cover intermediates plus final md/docx outputs |

| TB-20260404-18 | Process Inclusion Cloud Data Engineer intake and generate full package | done | 2026-04-04 | Created job 00063_6b2db598 and generated resume/cover intermediates plus final md/docx outputs |

| TB-20260404-19 | Build and validate Google Doc secret-message decoder script and run against provided URL | done | 2026-04-04 | Added scripts/secret_message/decode_google_doc_secret.py; fixed column-mapping + UTF-8 console handling; executed successfully against target doc |

| TB-20260404-19 | Generate CGI Senior Python Developer full tailored package | done | 2026-04-04 | Created job 00064_47a35392 and generated resume/cover intermediates plus final md/docx outputs |

| TB-20260405-01 | Create CodeSignal practice question document for assessment prep | done | 2026-04-05 | Added docs/operations/codesignal_practice_set_2026-04-05.md with 20-question checklist and progress log |

| TB-20260405-02 | Create Two Sum training folder with formal prompt and reusable test harness | done | 2026-04-05 | Added problem statement, solution stub, test_harness, and run_tests in coding_challenges/_assessment_training/two_sum |

| TB-20260405-03 | Create heap/min-heap micro-nuggets study lane with max-heap-by-negation patterns | done | 2026-04-05 | Added coding_challenges/_assessment_training/heaps_min_heap with 5 focused Python nuggets + README; validated via explicit interpreter path |

| TB-20260405-04 | Review agent files and enforce seed-context diagnostics (no passphrase re-ask policy) | done | 2026-04-05 | Updated AGENT_CHEATSHEET + QWEN_AGENT_HANDOFF; documented DPAPI CurrentUser mismatch diagnosis via whoami |

| TB-20260405-05 | Add durable seed context/decryption reminder runbook for cross-machine sessions | done | 2026-04-05 | Added docs/operations/seed_context_and_decryption_reminder.md and linked from operations README |
| TB-20260405-06 | Create one-file-per-problem review drill pack for Two Sum, Valid Parentheses, and Top K Frequent (bucket + min-heap) | done | 2026-04-05 | Added `coding_challenges/_assessment_training/review_pack/*_review_drill.py` files with blank implementations and harnesses |
| TB-20260405-07 | Normalize 347 review harness to 3-tuple tests with tie-safe validation and dual-run execution | done | 2026-04-05 | Updated review_pack/top_k_frequent_347_review_drill.py and removed sys.exit/debug artifacts |
| TB-20260405-08 | Create next single-file LeetCode review drill (Group Anagrams) with harness and blank implementation | done | 2026-04-05 | Added review_pack/group_anagrams_review_drill.py |
| TB-20260405-09 | Create LeetCode 128 single-file review drill harness with blank implementation | done | 2026-04-05 | Added review_pack/longest_consecutive_128_review_drill.py |
| TB-20260405-10 | Create LeetCode 238 single-file review drill harness with blank implementation | done | 2026-04-05 | Added review_pack/product_except_self_238_review_drill.py |
| TB-20260405-11 | Create Round 01 empty practice pack files for LC 1/20/49/128/238/347 | done | 2026-04-05 | Added review_pack/round_01_empty/*.py blank implementations with harnesses |
| TB-20260405-12 | Create Round 02 empty pack with 4 new LeetCode drills to reach 10 total | done | 2026-04-05 | Added round_02_empty for 217/242/125/15 |
| TB-20260405-13 | Fix incorrect expected indices in Two Sum II dual-empty harness test case | done | 2026-04-05 | Updated test case from [1,4] to [1,3] in two_sum_ii_167_dual_empty.py |
| TB-20260405-14 | Add separate canonical reference solution file for LeetCode 15 (3Sum) | done | 2026-04-05 | Added round_02_empty/three_sum_15_canonical_reference.py with standard two-pointer dedup pattern |
| TB-20260405-15 | Generate all 15 remaining CodeSignal-list LeetCode empty practice files in one folder | done | 2026-04-05 | Added review_pack/round_03_codesignal_remaining_15 with 15 single-file harnesses |
| TB-20260406-01 | Upgrade round_03 remaining-15 practice files with strong problem statements and concrete examples | done | 2026-04-06 | Enhanced house_robber first, then all files in round_03_codesignal_remaining_15 |
| TB-20260406-02 | Upgrade MinStack solution: raise exceptions on empty ops and replace with rich operation-sequence harness | done | 2026-04-06 | Updated min_stack_155_empty.py with dual-stack implementation, dynamic harness, and explicit exception tests |
| TB-20260406-03 | Strengthen LIS (LC300) practice harness with edge/counterexample tests and oracle stress checks | done | 2026-04-06 | Updated longest_increasing_subsequence_300_empty.py with deterministic+stress harness |
| TB-20260406-04 | Strengthen harnesses across round_03 remaining-15 practice pack with richer edge/tricky cases | done | 2026-04-06 | Expanded tests and scenario checks in string/interval/binary-search/graph/DP/cache/data-structure files while preserving user implementations |
| TB-20260406-05 | Create bite-by-bite graph lesson folder with runnable drills and quick quiz | done | 2026-04-06 | Added coding_challenges/_assessment_training/graph_bites (README + 6 lesson files) |
| TB-20260406-06 | Add durable reminder for OffByOneCode YouTube channel in project memory/docs | done | 2026-04-06 | Added docs/operations/learning_resources.md, updated operations index, and pinned channel in user_profile |
| TB-20260406-07 | Add top-down and BFS Coin Change alternatives in same file and run harness for all methods | done | 2026-04-06 | Updated coin_change_322_empty.py with coinChange_top_down, coinChange_bfs, and multi-run harness calls |
| TB-20260406-08 | Create formatted markdown index for 26 LeetCode cases with purpose blurbs and file links | done | 2026-04-06 | Added coding_challenges/_assessment_training/LEETCODE_26_INDEX.md |
| TB-20260406-09 | Add monotonic-stack case files (NGE, NSE pattern, Histogram, Rain Water) and update LeetCode index doc | done | 2026-04-06 | Added round_04_monotonic_stack and updated LEETCODE_26_INDEX.md entries |

| TB-20260406-10 | Review next_greater_element_496 solution implementation and confirm code quality | done | 2026-04-06 | Reviewed monotonic-stack logic in next_greater_element_496_empty.py; correctness and complexity are solid, no code changes required |
| TB-20260408-01 | Build guided repetition practice workspace with blank implementations and confidence tracker | done | 2026-04-08 | Created/updated round_05_empty/practice with basics+weak-point files blanked and PRACTICE_TRACKER.md for coached loops |
| TB-20260409-01 | Diagnose env_setter failure after repo transfer and document required fixes | done | 2026-04-09 | Missing config/env/base.psd1; seed file not portable; restore base config and re-register seed |
| TB-20260409-02 | Identify problem solved by provided min-cost consecutive-sequence snippet | done | 2026-04-09 | Interpreted as min-increment transform to arithmetic progression with step +/-1 |
| TB-20260410-01 | Stabilize website blog structure visibility (LeetCode section, sitemap accuracy, article UX cleanup) | done | 2026-04-10 | Added persistent LeetCode category pages (`/blog/leetcode/<category-id>.html`), multi-category post mapping, alias redirects for taxonomy evolution, recursive sitemap coverage for nested pages, duplicate-title handling, blog-list image cleanup, structured articles hub sections, and stale-page pruning |
| TB-20260410-02 | Persist website search-engine owner-account memory for future submission runs | done | 2026-04-10 | Stored Google/Bing site-submission owner accounts in `agents/shared/user_profile.md` under a dedicated Search Engine Ownership section |
| TB-20260410-03 | Create daily reminder/todo system and seed website submission inspection task for tomorrow | done | 2026-04-10 | Added `scripts/ops/daily_todo.ps1`, `agents/shared/daily_todo.json`, operations runbook doc, and seeded TODO-0001 due 2026-04-11 |
| TB-20260410-04 | Add day-based LinkedIn posting reminders to daily todo system | done | 2026-04-10 | Added TODO-0002..TODO-0005 for Mon/Wed/Fri cadence plus optional Sunday bonus post |
| TB-20260410-05 | Add multi-channel publishing reminders (X, YouTube, GitHub, Reddit, Medium/Dev.to) to daily todo system | done | 2026-04-10 | Added TODO-0006..TODO-0019 covering weekly X cadence + thread, YouTube weekly video + community posts, GitHub cadence, Reddit weekly contribution, and monthly long-form article |
| TB-20260411-01 | Update coding_challenges refresh index output to XLSX format | done | 2026-04-11 | Updated refresh_index.py to default to `index.xlsx`, added native XLSX writer, and validated workbook generation |
| TB-20260411-02 | Preserve manual Excel formatting when refreshing coding_challenges index workbook | done | 2026-04-11 | Switched XLSX writes to in-place workbook updates via openpyxl so formatting is retained across refresh runs |
| TB-20260412-01 | Persist durable memory for high-frequency index commands (`refresh_index_and_push.ps1`, `search_index.ps1`) | done | 2026-04-12 | Added command-memory entries to `agents/shared/user_profile.md` and `agents/shared/context_index.md` so startup reads capture them |
| TB-20260409-01 | Diagnose env_setter failure after repo transfer and document required fixes | done | 2026-04-09 | Missing config/env/base.psd1; seed file not portable; restore base config and re-register seed |
| TB-20260409-02 | Identify problem solved by provided min-cost consecutive-sequence snippet | done | 2026-04-09 | Interpreted as min-increment transform to arithmetic progression with step +/-1 |
| TB-20260410-01 | Stabilize website blog structure visibility (LeetCode section, sitemap accuracy, article UX cleanup) | done | 2026-04-10 | Added persistent LeetCode category pages (`/blog/leetcode/<category-id>.html`), multi-category post mapping, alias redirects for taxonomy evolution, recursive sitemap coverage for nested pages, duplicate-title handling, blog-list image cleanup, structured articles hub sections, and stale-page pruning |
| TB-20260410-02 | Persist website search-engine owner-account memory for future submission runs | done | 2026-04-10 | Stored Google/Bing site-submission owner accounts in `agents/shared/user_profile.md` under a dedicated Search Engine Ownership section |
| TB-20260410-03 | Create daily reminder/todo system and seed website submission inspection task for tomorrow | done | 2026-04-10 | Added `scripts/ops/daily_todo.ps1`, `agents/shared/daily_todo.json`, operations runbook doc, and seeded TODO-0001 due 2026-04-11 |
| TB-20260410-04 | Add day-based LinkedIn posting reminders to daily todo system | done | 2026-04-10 | Added TODO-0002..TODO-0005 for Mon/Wed/Fri cadence plus optional Sunday bonus post |
| TB-20260410-05 | Add multi-channel publishing reminders (X, YouTube, GitHub, Reddit, Medium/Dev.to) to daily todo system | done | 2026-04-10 | Added TODO-0006..TODO-0019 covering weekly X cadence + thread, YouTube weekly video + community posts, GitHub cadence, Reddit weekly contribution, and monthly long-form article |
| TB-20260411-01 | Update coding_challenges refresh index output to XLSX format | done | 2026-04-11 | Updated refresh_index.py to default to `index.xlsx`, added native XLSX writer, and validated workbook generation |
| TB-20260411-02 | Preserve manual Excel formatting when refreshing coding_challenges index workbook | done | 2026-04-11 | Switched XLSX writes to in-place workbook updates via openpyxl so formatting is retained across refresh runs |
| TB-20260412-01 | Persist durable memory for high-frequency index commands (`refresh_index_and_push.ps1`, `search_index.ps1`) | done | 2026-04-12 | Added command-memory entries to `agents/shared/user_profile.md` and `agents/shared/context_index.md` so startup reads capture them |
| TB-20260412-02 | Fix PowerShell 5.1 JSON hashtable compatibility in env bootstrap/secret scripts | done | 2026-04-12 | Added JSON compatibility helper in `env_core.ps1` and replaced direct `ConvertFrom-Json -AsHashtable` usage across `scripts/env` callers |
| TB-20260412-03 | Create second-machine Codex handoff doc for seed/env bootstrap recovery | done | 2026-04-12 | Added `docs/operations/CODEX_SECOND_MACHINE_SEED_HANDOFF.md` with exact commands, diagnostics, and recovery flow |
| TB-20260412-04 | Standardize external repo management under StudyBook temp and add cross-machine restore workflow | done | 2026-04-12 | Cloned `temp/jobsearch`, added `restore_managed_repos.ps1`, updated machine/env defaults to `{PROJECT_ROOT}\temp\...`, and refreshed agent/ops docs for relative-path policy |
| TB-20260412-04 | Resolve rebase conflicts in shared status files | done | 2026-04-12 | Resolved conflicts in agent_status/open_loops/task_register during rebase |
| TB-20260412-05 | Fix DPAPI ProtectedData load for seed registration in PowerShell 7 | done | 2026-04-12 | Added assembly load fallback in `scripts/env/env_core.ps1` for ProtectedData |
| TB-20260412-06 | Add secret decrypt error messaging and nonfatal handling when secrets are optional | done | 2026-04-12 | Added try/catch around secret decrypt to surface file path and passphrase mismatch guidance |
| TB-20260412-07 | Update second-machine seed handoff guide with latest fixes and recovery paths | done | 2026-04-12 | Added ProtectedData and padding-error guidance plus re-encrypt steps |
| TB-20260412-08 | Restore managed external repos under temp | done | 2026-04-12 | Ran restore_managed_repos.ps1; cloned jobsearch + website repos |
| TB-20260413-01 | Resolve in-progress StudyBook rebase after refresh_index_and_push | done | 2026-04-13 | Completed rebase; main ahead 18/behind 8 |
| TB-20260413-02 | Resolve binary conflict in coding_challenges index.xlsx | done | 2026-04-13 | Took remote version during rebase and completed rebase |
| TB-20260413-03 | Push AWS Glue media link updates to website repo | done | 2026-04-13 | Committed and pushed updated R2 audio/video links |
| TB-20260413-11 | Resolve StudyBook rebase conflicts (agent_status/open_loops) | done | 2026-04-13 | Cleared conflicts and completed rebase; main ahead 2 |
| TB-20260413-12 | Start Streamlit index UI Docker app | done | 2026-04-13 | Started docker/index_ui compose; container reported running |
| TB-20260413-13 | Prevent duplicate learning-aws-analytics sections | done | 2026-04-13 | Added router load guard to avoid concurrent DOM appends |
| TB-20260413-14 | Update AWS Lambda learning page audio/video media links | done | 2026-04-13 | Added R2 audio/video sources and displayed bucket base path |
| TB-20260413-16 | Update AWS EC2 learning page audio/video media links | done | 2026-04-13 | Added R2 audio/video sources using new EC2 media filenames |
| TB-20260413-17 | Clean EC2 audio label text | done | 2026-04-13 | Removed garbled prefix from audio label |
| TB-20260413-18 | Normalize EC2 headings dash characters | done | 2026-04-13 | Replaced em/en dashes with ASCII hyphens |
| TB-20260413-19 | Add website maintenance agent context | done | 2026-04-13 | Created WEBSITE_AGENT_CONTEXT.md with media rules and update workflow |


| TB-20260413-03 | Resolve StudyBook push rejection and close index.xlsx binary merge conflict on main | done | 2026-04-13 | Kept local `coding_challenges/index.xlsx` during merge conflict resolution and pushed `main` successfully (`50cafff`) |
| TB-20260413-04 | Move coding_challenges index workflow to CSV-first and add index CLI for CRUD/search/open | done | 2026-04-13 | Added `index_cli.py` + `index_cli.ps1`, converted refresh/search scripts to CSV, and untracked binary `index.xlsx` |
| TB-20260413-05 | Add Streamlit CSV index GUI and env_setter-aligned launcher | done | 2026-04-13 | Added `index_ui_streamlit.py` + `run_index_ui.ps1`; launcher now boots through env_setter and serves GUI at localhost:8501 |
| TB-20260413-06 | Redesign index Streamlit UI to compact summary table + popup edit dialog workflow | done | 2026-04-13 | Table now shows id/title/primary/tags with select+edit dialog, add dialog, and explicit save workflow |
| TB-20260413-07 | Enable click-to-select record in Streamlit summary table for edit workflow | done | 2026-04-13 | Table row click now sets selected record used by Edit Selected action |
| TB-20260413-08 | Add index workflow guide and fully remove index.xlsx from active repository workflow | done | 2026-04-13 | Added operations guide and removed local `coding_challenges/index.xlsx`; CSV remains source of truth |
| TB-20260413-09 | Dockerize Streamlit index UI and add compose-based runner script | done | 2026-04-13 | Added Dockerfile/compose/runner + operations guide updates; runner now fails on docker errors |
| TB-20260413-10 | Persist cross-machine Docker-start reminder and refresh index command memory in user profile | done | 2026-04-13 | Added durable note for "create docker and start it" workflow plus current CSV/CLI/Streamlit command set |
| TB-20260413-15 | Bootstrap JobSearch startup context and verify latest pipeline item state | done | 2026-04-13 | Loaded startup + JobSearch context files, ran noninteractive env bootstrap, and confirmed `00051_d7c3a912` is already applied |

| TB-20260417-01 | Run JobSearch force pipeline for Capital One intake and record application status | done | 2026-04-17 | Duplicate gate flagged prior similar role; force pipeline completed with UUID 00078_5ca49264 and application marked applied via Company Website |
| TB-20260420-01 | Expose direct dashboard access to underlying coding_challenges source list | done | 2026-04-20 | Updated Streamlit index UI to show source path, download source CSV, and render raw source list table |
| TB-20260420-02 | Enforce read-only dashboard access for coding_challenges source list | done | 2026-04-20 | Added read-only mode (default ON) and disabled all mutation controls while preserving source view/open/download |
| TB-20260420-03 | Set containerized JupyterLab markdown files to open in Preview by default | done | 2026-04-20 | Added JupyterLab overrides.json and mounted into pipeline/full compose jupyter service |
| TB-20260420-04 | Fix Jupyter markdown preview default mount path and recreate live container | done | 2026-04-20 | Switched to user-settings mount, removed dead overrides file, and recreated `citi_jupyterlab` with verified settings file present |
| TB-20260420-05 | Persist Thursday coding-test prep context, review `playground`, and add durable progress tracker | done | 2026-04-20 | Reviewed `playground` inventory and core study files; created `playground/THURSDAY_CODING_TEST_PROGRESS.md`; updated shared memory files for continuity |
| TB-20260423-01 | Create missing placeholder prefix-sum notebooks referenced in Study Guide (0158-0162) | done | 2026-04-23 | Added five placeholder notebooks under `playground` with markdown + TODO code cells |
| TB-20260423-02 | Clean prefix placeholder notebook presentation and add explicit LeetCode description block | done | 2026-04-23 | Rewrote `0158`-`0162` markdown cells to clean format and added LeetCode-number description in each |
| TB-20260423-03 | Fix unreadable Jupyter JSON for prefix placeholder notebooks by removing UTF-8 BOM | done | 2026-04-23 | Re-encoded `0158`-`0162` to UTF-8 no BOM and validated JSON parse successfully |
| TB-20260423-04 | Fix Dockerized JupyterLab endless loading loop caused by workspace permission denial | done | 2026-04-23 | Added writable workspaces bind mount in compose/pipeline, recreated jupyterlab, verified healthy startup |
| TB-20260424-01 | Add internal TOC/section hyperlinks in `06_BinarySearch.ipynb` | done | 2026-04-24 | Linked TOC numbers to section anchors and added per-section back-to-TOC links while preserving existing file links |
| TB-20260424-02 | Add internal TOC/section hyperlinks in `08.Monotonic Stack.ipynb` | done | 2026-04-24 | Linked TOC numbers to section anchors for implemented entries and added per-section back-to-TOC links |
| TB-20260424-03 | Apply same TOC/section hyperlink pattern across requested study-guide notebooks (01,02,03,04,06,07,020,021,022) | done | 2026-04-24 | Added number-anchor links and back-to-TOC links in all requested notebooks while preserving filename links |
| TB-20260424-04 | Add placeholder sections for 0113 and 0143 in 06_BinarySearch with two-way TOC navigation | done | 2026-04-24 | Added TOC rows + anchors/back-links + code placeholders for 0113 and 0143 |
| TB-20260424-05 | Create section files 10-19 from STUDY_GUIDE with TOC + placeholders and `#TOC_TOP` back links | done | 2026-04-24 | Added 10 new notebooks with per-case anchors, backlinks, and empty code cells |
| TB-20260424-06 | Confirm context bootstrap and apply owner-authorized full-scope approval override for this effort | done | 2026-04-24 | Updated approval_matrix/command_allowlist with active run override for D:\StudyBook and C:\temp |
| TB-20260424-07 | Execute AWS Glue existing-work audio/html pipeline and harden encoding-safe mission standards | done | 2026-04-24 | Generated final_aws-glue.mp3 (628.966s, 5.94MB), updated aws-glue.html, and strengthened HTML encoding rules in mission docs |
| TB-20260424-08 | Execute Amazon Redshift existing-work pipeline (missions 11/12/13) | done | 2026-04-24 | Created Redshift missions, generated final_aws-redshift.mp3 (554.160s), and updated aws-redshift.html with final MP3 + encoding-safe entities |
| TB-20260424-09 | Execute AWS Lambda existing-work pipeline (missions 14/15/16) | done | 2026-04-24 | Created Lambda missions, generated final_aws-lambda.mp3 (551.210s), and updated aws-lambda.html with final MP3 + encoding-safe entities |
| TB-20260424-10 | Execute Amazon S3 existing-work pipeline (missions 17/18/19) | done | 2026-04-24 | Created S3 missions, generated final_aws-s3.mp3 (598.340s), and updated aws-s3.html with final MP3 + cheat-row + encoding-safe entities |
| TB-20260424-11 | Execute Apache Kafka existing-work pipeline (missions 20/21/22) | done | 2026-04-24 | Created Kafka missions, generated final_apache-kafka.mp3 (540.248s), and updated apache-kafka.html with final MP3 + encoding-safe placeholder media block |

| TB-20260424-12 | Create Phase 2 AWS VPC mission pair (28/29) for script+new-page workflow | done | 2026-04-24 | Added 28_VPC_GENERATE_AUDIO_SCRIPT.md and 29_VPC_GENERATE_HTML_PAGE.md aligned to IAM pattern and encoding-safe standards |

| TB-20260424-13 | Enforce C:\temp audio-output policy in VPC missions and sweep repo for stray media artifacts | done | 2026-04-24 | Updated missions 28/29 with explicit out-of-repo output + cleanliness guard; repo sweep moved 0 files |

| TB-20260425-01 | Generate AWS IAM script and run audio pipeline to C:\temp\studybook_audio\aws-iam | done | 2026-04-25 | Created audio_script_aws-iam.md and generated final_aws-iam.mp3 (549.320s, 5,168,205 bytes) |

| TB-20260425-02 | Mission 27: generate new aws-iam.html page with live R2 audio URL | done | 2026-04-25 | Created aws-iam.html with EC2 CSS parity, IAM sections s1-s13, QA, cheat sheet, and encoding-safe entities |

| TB-20260425-03 | Fix non-clickable IAM card in learning-aws-security component | done | 2026-04-25 | Updated IAM card to live link and full-card click navigation to learning/aws-iam.html |

| TB-20260425-04 | Execute VPC audio pipeline from existing script and activate site link to aws-vpc.html | done | 2026-04-25 | Generated final_aws-vpc.mp3 in C:\temp\studybook_audio\aws-vpc and made VPC card clickable in learning-aws-security component |

| TB-20260425-05 | Mark VPC card audio status as Live after R2 confirmation | done | 2026-04-25 | Updated learning-aws-security VPC card badge from Upload pending to Live |

| TB-20260425-06 | Create provided-files master pipeline runbook for two-input execution mode | done | 2026-04-25 | Added Existing_work_pipeline_execution_provided_files_master.md for script+html pre-supplied flow |

| TB-20260425-07 | Execute PostgreSQL provided-files pipeline and activate site linking | done | 2026-04-25 | Generated final_postgresql.mp3 and switched PostgreSQL card to clickable reference mode with upload-pending badge |

| TB-20260425-08 | Mark PostgreSQL card audio status as Live after R2 confirmation | done | 2026-04-25 | Updated learning-databases PostgreSQL card badge from Upload pending to Live |

| TB-20260425-09 | Execute DynamoDB provided-files pipeline and activate site linking | done | 2026-04-25 | Generated final_aws-dynamodb.mp3 and added clickable DynamoDB card in learning-aws-analytics with upload-pending badge |

| TB-20260425-10 | Mark DynamoDB card audio status as Live after R2 confirmation | done | 2026-04-25 | Updated learning-aws-analytics DynamoDB badge from Upload pending to Live |

| TB-20260425-11 | Execute Terraform provided-files pipeline and activate site linking | done | 2026-04-25 | Generated final_terraform.mp3 and switched Terraform card in learning-devops to clickable reference mode with upload-pending badge |

| TB-20260425-12 | Mark Terraform card audio status as Live after R2 confirmation | done | 2026-04-25 | Updated learning-devops Terraform badge from Upload pending to Live |
| TB-20260425-14 | Execute OpenSearch provided-files pipeline finalization and activate site linking | done | 2026-04-25 | Confirmed opensearch.html uses live final_opensearch.mp3 URL and added clickable Live OpenSearch card in learning-cloud-other |
| TB-20260425-13 | Execute Snowflake+PyIceberg provided-files pipeline and activate live site linking | done | 2026-04-25 | Confirmed live MP3 URL in snowflake-pyiceberg.html and updated learning-cloud-other Snowflake card to clickable Live state |
| TB-20260425-15 | Add stable local OpenAI key fallback to prevent DPAPI/seed shell stalls | done | 2026-04-25 | Added set_openai_key_local helper and documented gitignored machine-local fallback in secrets workflow |
| TB-20260425-16 | Harden API key loading path to avoid future audio-run stalls | done | 2026-04-25 | Added env_core fallback loader from config\\secrets\\.local\\openai_api_key.txt and updated helper/runner behavior to skip unnecessary env bootstrap |
| TB-20260425-17 | Execute FastAPI provided-files pipeline and activate site linking | done | 2026-04-25 | Generated final_fastapi.mp3, confirmed live R2 URL, and switched learning-craft FastAPI card badge to Live |
| TB-20260425-18 | Execute CI/CD+ECS provided-files pipeline and activate site linking | done | 2026-04-25 | Generated final_cicd-github-ecs.mp3, confirmed live R2 URL, and switched learning-devops CI/CD card badge to Live |
| TB-20260425-19 | Execute AWS MSK Kafka provided-files pipeline and activate site linking | done | 2026-04-25 | Generated final_aws-msk-kafka.mp3, confirmed live R2 URL, and switched learning-streaming AWS MSK Kafka card badge to Live |
| TB-20260425-20 | Execute AWS CloudFormation provided-files pipeline and activate site linking | done | 2026-04-25 | Generated final_aws-cloudformation.mp3, confirmed live R2 URL, and switched learning-devops CloudFormation card badge to Live |
| TB-20260425-21 | Execute AWS Bedrock provided-files pipeline and activate site linking | done | 2026-04-25 | Generated final_aws-bedrock.mp3, confirmed live R2 URL, and switched learning-cloud-other Bedrock card badge to Live |
| TB-20260425-22 | Execute Apache Kafka provided-files pipeline refresh and normalize card state | done | 2026-04-25 | Regenerated final_apache-kafka.mp3, confirmed live R2 URL, and switched learning-streaming Apache Kafka card badge to Live |
| TB-20260425-23 | Execute Athena provided-files pipeline refresh and normalize card state | done | 2026-04-25 | Re-ran runner for audio_script_aws-athena.md to C:\\temp\\studybook_audio\\aws-athena, verified live MP3 URL in aws-athena.html, and switched Athena card badge to Live |
| TB-20260425-24 | Execute EC2 provided-files pipeline refresh and normalize compute card state | done | 2026-04-25 | Re-ran runner for audio_script_aws-ec2.md to C:\\temp\\studybook_audio\\aws-ec2, verified live MP3 URL in aws-ec2.html, and switched EC2 card badge to Live |
| TB-20260425-25 | Execute ECS provided-files pipeline refresh and normalize compute card state | done | 2026-04-25 | Re-ran runner for audio_script_aws-ecs.md to C:\\temp\\studybook_audio\\aws-ecs, verified live MP3 URL in aws-ecs.html, and switched ECS card badge to Live |
| TB-20260425-26 | Execute pipeline-design provided-files pipeline and normalize craft card state | done | 2026-04-25 | Normalized speaker format in audio_script_pipeline-design.md, generated final_pipeline-design.mp3 in C:\\temp\\studybook_audio\\pipeline-design, verified live URL in pipeline-design.html, and switched card badge to Live |
| TB-20260425-27 | Execute Glue provided-files pipeline refresh and normalize analytics card state | done | 2026-04-25 | Re-ran runner for audio_script_aws-glue.md to C:\\temp\\studybook_audio\\aws-glue, verified live MP3 URL in aws-glue.html, and switched Glue card badge to Live |
| TB-20260425-28 | Wire python-testing-pipelines as live in craft+python section cards after audio publish | done | 2026-04-25 | Updated component cards to clickable/live and verified page MP3 binding |
| TB-20260425-29 | Wire python-concurrency page into learning-python card and mark live | done | 2026-04-25 | Updated planned Python card to clickable live reference |
| TB-20260426-01 | Stabilize new Workarea sibling-repo layout and remove legacy temp fallback paths | done | 2026-04-26 | Updated runtime scripts/config/docs to D:\\Workarea model and removed empty legacy temp mirrors |
| TB-20260426-02 | Persist startup memory to always run env_setter.ps1 first in StudyBook sessions | done | 2026-04-26 | Updated startup note + shared context memory and logged durable decision DEC-028 |
| TB-20260426-03 | Familiarize and persist StudyBook repository footprint in agent memory files after root move | done | 2026-04-26 | Normalized agent memory paths to D:\\Workarea\\StudyBook and added footprint snapshot to shared context index |
| TB-20260426-04 | Ground and bootstrap PySpark Docker tutorial with educational docs and runnable Phase 1 files | done | 2026-04-26 | Rewrote tutorials/02_PySpark_Docker/chat.md as collaboration playbook; created README.md, requirements.txt, common/spark_session.py, and 01_cluster_connection.py |
| TB-20260426-05 | Fix PySpark Docker tutorial runtime failure from driver/cluster version mismatch and verify lesson execution | done | 2026-04-26 | Verified `pyspark 3.5.4` vs Docker `apache/spark:3.5.3` mismatch, aligned to `pyspark==3.5.3`, reran `01_cluster_connection.py` successfully |
| TB-20260426-06 | Implement PySpark Docker lesson 02 (DataFrame operations) and validate end-to-end runtime | done | 2026-04-26 | Added `02_dataframe_operations.py` with select/filter/withColumn/groupBy/agg/orderBy/explain coverage; executed successfully against Docker Spark |
| TB-20260426-07 | Implement PySpark Docker lesson 04 (joins and broadcast) and fix Python worker mismatch in small-dimension construction | done | 2026-04-26 | Added `04_joins_and_broadcast.py`; replaced Python-list DataFrame creation with SQL `VALUES` to avoid Python 3.12 driver vs Python 3.8 worker failure; validated SortMerge vs BroadcastHash plans |
| TB-20260426-08 | Implement PySpark Docker lesson 05 (shuffle/partitions/cache) with skew diagnostics and runtime validation | done | 2026-04-26 | Added `05_shuffle_partitions_cache.py` covering repartition/coalesce/cache/persist plus required skew metrics; executed successfully |
| TB-20260426-09 | Implement final PySpark Docker lesson for Spark UI experiments and validate UI-observable workloads | done | 2026-04-26 | Added `07_spark_ui_experiments.py` with groupBy/join/repartition/cache/count workloads and 30s UI inspection hold; executed successfully |
| TB-20260426-10 | Add concise lesson-by-lesson expected output verification section to PySpark Docker README | done | 2026-04-26 | Added quick-check output expectations for lessons 01-07 and removed stale planned-files subsection |
| TB-20260426-11 | Create Docker teaching subfolder with linked markdown lessons and sample deployment/run files | done | 2026-04-26 | Added `tutorials/02_PySpark_Docker/docker` pack with 7 topic files, index links, compose/dockerfile/env samples, and runner scripts |

| TB-20260426-12 | Bootstrap Apache Airflow Docker tutorial pack from scratch with deploy docs and smoke tests | done | 2026-04-26 | Added tutorials/03_apache_airflow_docker/docker with compose stack, scripts, linked docs, sample DAG, and smoke test script |
| TB-20260426-13 | Rename tutorial Airflow Docker project to docker_airflow and decommission legacy citi_airflow artifacts | done | 2026-04-26 | Set COMPOSE_PROJECT_NAME=docker_airflow, restarted stack, removed citi_airflow container/volumes, smoke test passed |
| TB-20260426-14 | Build beginner zero-to-hero Airflow Docker tutorial pack with grouped compose examples, helper scripts, and tool handoff card | done | 2026-04-26 | Added story-style tutorial folder, compose_groups files, deploy/newbie scripts, TOOL_INFO_CARD, and README links |
| TB-20260426-15 | Add safe destroy option to grouped Airflow deploy helper script | done | 2026-04-26 | Added destroy action with explicit confirmation and -Force override; updated tutorial docs |
| TB-20260426-16 | Create ChatGPT tutorial-project handoff source file in tutorials root with Codex capabilities, session context, and Docker runtime state | done | 2026-04-26 | Added tutorials/Tutorials_project_on_ChatGPT.md with collaboration protocol and live stack details |
| TB-20260426-17 | Generate Docker tutorial bundle 01 files and validate build/run workflow | done | 2026-04-26 | Created six bundle files under tutorials/36_docker, executed python 01_dockerfile_basics.py, fixed Windows encoding issues, and confirmed successful builds plus container run |
| TB-20260427-01 | Add EMR capstone orchestrator and correct Spark entrypoint run guidance | done | 2026-04-27 | Added `tutorials/06_aws_emr/capstone/orchestrate.py` and changed `process_logs.py` run hint to `spark-submit ...`; syntax checks passed |
| TB-20260427-02 | Add AWS profile assistant script for EMR capstone environment setup | done | 2026-04-27 | Added `tutorials/06_aws_emr/capstone/aws_assistant.ps1` to discover profiles/account/region and apply `AWS_PROFILE`, `AWS_REGION`, `EMR_S3_BUCKET`, and `EMR_SERVERLESS_ROLE_ARN` env vars |
| TB-20260427-03 | Add and run EMR Serverless role-fix automation script for study account | done | 2026-04-27 | Added `tutorials/06_aws_emr/capstone/fix_emr_serverless_role.ps1`; created role `StudyBookEMRServerlessExecutionRole` and attached inline S3 access policy for capstone prefixes |
| TB-20260427-04 | Persist StudyBook Springboard as durable intent-first startup memory for future agent sessions | done | 2026-04-27 | Recorded DEC-030 and updated shared context so `SPRINGBOARD.md` is read first for navigation and command/path discovery |
| TB-20260428-01 | Execute CreatingAudioTopicsWebsite flow for planned design topic `high-volume-event-ingestion` | done | 2026-04-28 | Created topic content + audio script + learning page, generated `final_high-volume-event-ingestion.mp3`, and switched `learning-design` card to clickable upload-pending state |
| TB-20260428-02 | Refresh phone audio for selected folders and create new playlist `Tayota` | done | 2026-04-28 | Created `D:\temp\studybook_audio\Tayota.m3u` with pipeline/data-architecture/learning-design tracks and synced to Pixel 8 Pro destination (3 MP3 copied, playlist updated) |
| TB-20260429-01 | Sync FastAPI audio to phone and add it to `tayota1` playlist | done | 2026-04-29 | Updated `D:\temp\studybook_audio\tayota1.m3u` to include `../StudyBook/final_fastapi.mp3`, then ran dry run + live sync to Pixel 8 Pro (56 copied, 3 skipped; playlists synced including `tayota1.m3u`) |
| TB-20260429-02 | Enforce targeted phone sync with registry and prune-to-selection behavior | done | 2026-04-29 | Added registry-driven targeted mode to sync script, set `tayota1` profile (4 tracks), pruned phone audio destination to exactly 4 files, and enforced playlist location under `Music\\pl` only |
| TB-20260430-01 | Create canonical stand-in thread doc for CreatingAudioTopicsWebsite recovered chat | done | 2026-04-30 | Added `recovered_chats/CreatingAudioTopicsWebsite_canonical_thread.md` with timeline, decisions, command pattern, path map, and reuse guidance |
| TB-20260430-02 | Create canonical stand-in thread doc for Generate_study_prep_for_Interviews recovered chat | done | 2026-04-30 | Added recovered_chats/Generate_study_prep_for_Interviews_canonical_thread.md with timeline, decisions, commands, path map, and operating rules |
| TB-20260430-03 | Create canonical stand-in thread doc for Audio Generation recovered chat | done | 2026-04-30 | Added `recovered_chats/Audio_Generation_canonical_thread.md` with timeline, decisions, commands, path map, and operating rules |

| TB-20260515-01 | Initialize study_bubbles Iteration 0 scaffold and governance/memory docs | done | 2026-05-15 | Created requested folder/file scaffold and docs; ran lightweight existence check |

