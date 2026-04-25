# Codex Mission Queue — StudyBook Projects
# Working directory for ALL missions: D:\StudyBook\
# All paths in all mission files are relative to D:\StudyBook\

---

## THREE REPOSITORIES

```
D:\StudyBook\                              ← ROOT — always your working directory
├── env_setter.ps1                         ← loads OPENAI_API_KEY — run before any Python
├── playground\                            ← Jupyter notebooks
├── prompts\
│   └── codex_missions\                   ← ALL Codex mission files live here
│
├── temp\jobsearch\                        ← REPO 2: Job search system
│   ├── scripts\                           ← Python tools (audio pipeline, etc.)
│   ├── data\interview_prep\audio_prep\    ← Audio scripts (.md only — no MP3s in repo)
│   └── prompts\                           ← Artifact templates, TTS rules
│
└── temp\seanlgirgis.github.io\           ← REPO 3: Personal website
    └── learning\                          ← HTML learning pages (target of Phase 1 & 2)
```

---

## HOW TO RUN A MISSION

1. Open a new Codex chat
2. Paste `00_CODEX_CONTEXT.md` → "This is your project context. Confirm you understand."
3. Set working directory: `cd D:\StudyBook`
4. Paste the next mission file
5. Wait for COMPLETE or BLOCKED report
6. Fix any BLOCKED issues before the next mission

One mission per Codex session where possible. Never combine missions.

Master reusable runbook:
- `prompts\codex_missions\Existing_work_pipeline_execution_master.md`

---

## AUDIO EXECUTION STANDARD (DO NOT DEVIATE)

### ⚠️ BINARY FILE RULE — NON-NEGOTIABLE
MP3 files and audio clips are binary. They NEVER go inside D:\StudyBook\ or any sub-repo.
Only the text script (.md) is committed. Everything else lives under C:\temp\studybook_audio\.

| What | Where | In repo? |
|------|-------|----------|
| Audio script (.md) | `temp\jobsearch\data\interview_prep\audio_prep\<slug>\audio_script_<slug>.md` | ✅ YES |
| Audio clips (.mp3) | `C:\temp\studybook_audio\<slug>\audio_clips\` | ❌ NO — outside repo |
| Final MP3 | `C:\temp\studybook_audio\<slug>\final_<slug>.mp3` | ❌ NO — outside repo |
| Upload guide | `C:\temp\studybook_audio\<slug>\UPLOAD_INSTRUCTIONS.md` | ❌ NO — outside repo |

- Use `scripts\run_mission_audio.ps1` for mission audio generation and stitching.
- Runner behavior is fail-fast (non-zero exit on generation/stitch failures).
- Default chunk target is `750` chars with natural sentence-boundary splits.
- For HTML updates, use UTF-8 and HTML entities for non-ASCII chrome glyphs (`&middot;`, `&uarr;`, `&micro;`, `&#127911;`, `&#127916;`) to prevent mojibake.

---

## PHASE 0 — ONE-TIME SETUP

| Mission | File | Action | Output |
|---------|------|--------|--------|
| 00 | 00_CODEX_CONTEXT.md | Project context — load every session | (reference) |
| 01 | 01_AUDIT_EXISTING_PAGES.md | Read all 8 HTML files | AUDIT_REPORT.md |

---

## PHASE 1 — FIX AUDIO ON EXISTING 8 PAGES

Pattern per topic: **02-style** (generate script) → **03-style** (run pipeline) → **04-style** (update HTML)

### 🧪 TEST CASE — Amazon EC2

| Mission | File | Action | Output |
|---------|------|--------|--------|
| 02 | 02_EC2_GENERATE_AUDIO_SCRIPT.md | Write HOST+SEAN dialogue | audio_script_aws-ec2.md |
| 03 | 03_EC2_RUN_AUDIO_PIPELINE.md | TTS pipeline + stitch | final_aws-ec2.mp3 |
| 04 | 04_EC2_UPDATE_HTML.md | Patch audio-box in HTML | aws-ec2.html updated |

⚠️ Between Mission 03 and 04: Sean uploads final_aws-ec2.mp3 to R2.
⚠️ After Mission 04: browser test before proceeding to next topic.

### Remaining Files (mission files created after EC2 test passes)

| Topic | Script | Pipeline | HTML | Audio exists? | Extra fix |
|-------|--------|----------|------|--------------|-----------|
| aws-athena | 05 | 06 | 07 | YES — replace | ⚠️ cheat-row 160→170px |
| aws-glue | 08 | 09 | 10 | YES — replace | ⚠️ cheat-row 150→170px |
| aws-redshift | 11 | 12 | 13 | YES — replace | none |
| aws-lambda | 14 | 15 | 16 | YES — replace | none |
| aws-s3 | 17 | 18 | 19 | YES — replace | ⚠️ cheat-row 150→170px |
| apache-kafka | 20 | 21 | 22 | NO — add new | none |
| aws-ecs | 23 | 24 | 25 | NO — add new | none |

---

## PHASE 2 — NEW LEARNING PAGES

Pattern per topic: generate script → run pipeline → generate HTML page → add audio src

| Topic | Slug | Priority | Script | Pipeline | HTML | Audio |
|-------|------|----------|--------|----------|------|-------|
| Terraform | terraform | 🔴 | 26 | 27 | 28 | 29 |
| FastAPI | fastapi | 🔴 | 30 | 31 | 32 | 33 |
| CI/CD (GitHub Actions+Docker+ECS) | cicd-github-ecs | 🟠 | 34 | 35 | 36 | 37 |
| AWS CloudFormation | aws-cloudformation | 🟠 | 38 | 39 | 40 | 41 |
| AWS MSK / Kafka | aws-msk-kafka | 🟡 | 42 | 43 | 44 | 45 |
| Snowflake + PyIceberg | snowflake-pyiceberg | 🟡 | 46 | 47 | 48 | 49 |
| OpenSearch | opensearch | 🟡 | 50 | 51 | 52 | 53 |

---

## PHASE 3 — TUTORIALS + CAPSTONE PROJECTS

For each Phase 2 topic, two additional artifacts:
- Artifact B: Tutorial + Interview Q&A (Markdown study guide)
- Artifact C: Capstone project spec

Mission files created after Phase 2 begins.

---

## AUDIO FILE NAMING CONVENTION

All audio output paths are relative to `temp\jobsearch\data\interview_prep\audio_prep\`

| Topic | Slug folder | Script filename | Final MP3 |
|-------|------------|-----------------|-----------|
| Amazon EC2 | aws-ec2 | audio_script_aws-ec2.md | final_aws-ec2.mp3 |
| Amazon Athena | aws-athena | audio_script_aws-athena.md | final_aws-athena.mp3 |
| AWS Glue | aws-glue | audio_script_aws-glue.md | final_aws-glue.mp3 |
| Amazon Redshift | aws-redshift | audio_script_aws-redshift.md | final_aws-redshift.mp3 |
| AWS Lambda | aws-lambda | audio_script_aws-lambda.md | final_aws-lambda.mp3 |
| Amazon S3 | aws-s3 | audio_script_aws-s3.md | final_aws-s3.mp3 |
| Apache Kafka | apache-kafka | audio_script_apache-kafka.md | final_apache-kafka.mp3 |
| Amazon ECS | aws-ecs | audio_script_aws-ecs.md | final_aws-ecs.mp3 |
| Terraform | terraform | audio_script_terraform.md | final_terraform.mp3 |
| FastAPI | fastapi | audio_script_fastapi.md | final_fastapi.mp3 |
| CI/CD | cicd-github-ecs | audio_script_cicd-github-ecs.md | final_cicd-github-ecs.mp3 |
| CloudFormation | aws-cloudformation | audio_script_aws-cloudformation.md | final_aws-cloudformation.mp3 |
| MSK/Kafka | aws-msk-kafka | audio_script_aws-msk-kafka.md | final_aws-msk-kafka.mp3 |
| Snowflake+PyIceberg | snowflake-pyiceberg | audio_script_snowflake-pyiceberg.md | final_snowflake-pyiceberg.mp3 |
| OpenSearch | opensearch | audio_script_opensearch.md | final_opensearch.mp3 |

R2 base URL: `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/`

---

## CURRENT STATUS

| Phase | Status |
|-------|--------|
| Phase 0 — Audit | ✅ Complete — AUDIT_REPORT.md finalized |
| Phase 1 — Fix existing audio | 🔄 In progress — EC2 ✅ · Athena next |
| Phase 2 — New pages | ⏳ Not started |
| Phase 3 — Tutorials + Capstone | ⏳ Not started |

### Phase 1 Detail

| # | File | Script | Pipeline | HTML | Browser test |
|---|------|--------|----------|------|-------------|
| 1 | aws-ec2.html | ✅ | ✅ 38 chunks / 696s | ✅ | ⏳ pending |
| 2 | aws-athena.html | ⏳ | ⏳ | ⏳ | ⏳ |
| 3 | aws-glue.html | ⏳ | ⏳ | ⏳ | ⏳ |
| 4 | aws-redshift.html | ⏳ | ⏳ | ⏳ | ⏳ |
| 5 | aws-lambda.html | ⏳ | ⏳ | ⏳ | ⏳ |
| 6 | aws-s3.html | ⏳ | ⏳ | ⏳ | ⏳ |
| 7 | apache-kafka.html | ⏳ | ⏳ | ⏳ | ⏳ |
| 8 | aws-ecs.html | ⏳ | ⏳ | ⏳ | ⏳ |
