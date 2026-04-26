# StudyBook — Project State
# Last updated: 2026-04-25
# Update this file at the start/end of every working session.

---

## WHO AND WHY

Owner: Sean Girgis — Senior Data Engineer
Goal: Interview preparation + personal learning system
Active targets: Toyota (IoT/streaming heavy) | Capital One (financial services/compliance heavy)
Website: https://seanlgirgis.github.io/learning/

---

## SYSTEM ARCHITECTURE

```
D:\StudyBook\                        ← main repo
├── prompts\codex_missions\          ← Claude Code / Codex task prompts
├── scripts\                         ← PowerShell pipeline scripts
├── temp\
│   ├── seanlgirgis.github.io\       ← website source (committed + pushed)
│   │   └── learning\*.html          ← all 49 learning pages
│   ├── jobsearch\                   ← job search data
│   └── gap\                         ← ChatGPT prompt files (01-28 topics)
└── tutorials\                       ← tutorial Python files (long-running project)
    └── _manager\                    ← THIS folder — project memory (lives with tutorials)

D:\temp\studybook_audio\             ← MP3 files (OUTSIDE repo, never commit)
C:\Users\shareuser\CrossDevice\
  Pixel 8 Pro\storage\Music\
  StudyBook\                         ← Phone music folder (54 MP3s + 12 playlists)

R2 CDN: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/
```

---

## ✅ COMPLETED

### Learning Website (seanlgirgis.github.io/learning/)
- 49 HTML reference pages — all live
- 54 audio MP3s — all on R2 CDN
- Audio wired into every HTML page
- All pages committed and pushed to GitHub

### Audio Files (D:\temp\studybook_audio\)
- 54 final_*.mp3 files covering all topics
- Copied to Pixel 8 Pro via CrossDevice sync

### Phone Playlists (12 M3U files)
- PL-01 Toyota Interview Prep (18 tracks)
- PL-02 Capital One Interview Prep (18 tracks)
- PL-03 AWS Foundations (9 tracks)
- PL-04 AWS Data Stack (9 tracks)
- PL-05 Streaming & Real-Time (6 tracks)
- PL-06 Python Engineering (11 tracks)
- PL-07 Data Engineering Fundamentals (10 tracks)
- PL-08 Engineering Discipline (8 tracks)
- PL-09 Security & Compliance (6 tracks)
- PL-10 My Story (5 tracks)
- PL-11 Commute Starter (10 tracks)
- PL-12 Local Analytics Stack (5 tracks)
- Sync script: .\scripts\sync_studybook_to_phone.ps1

### Gap Prompts (D:\StudyBook\temp\gap\)
- 28 topic prompt files (01-28) — all in new format
- Project 1 (audio script) + Project 2 (HTML page) per topic
- Topics 01-03 already processed by user

### ChatGPT Projects Configured
- Project 1 — Audio Script Writer (Project-1-Audioscript-Maker.txt)
- Project 2 — HTML Page Generator (Project2_HTML_MAKER.txt)
- Both updated: no rotating bridge phrases, tighter chunk sizes

### Tutorial Directory Structure
- D:\StudyBook\tutorials\ — full tree created (41 topics × setup + capstone)
- _meta\TUTORIAL_STANDARDS.md — coding standards for all generated files
- _meta\MASTER_PROMPT_TEMPLATE.md — reusable ChatGPT prompt skeleton
- _shared\aws_session.py — shared boto3 session helper
- _shared\logger.py — shared structured JSON logger
- _shared\docker\ — existing stack documented (see DOCKER_INVENTORY.md)

### Tutorial Prompt Files Written (prompt.md per topic)
- ✅ 01_aws_kinesis
- ✅ 02_pyspark
- ✅ 03_apache_airflow
- ✅ 04_aws_step_functions
- ✅ 05_delta_lake
- ✅ 06_aws_emr
- ✅ 07_aws_glue
- ✅ 08_aws_s3
- ✅ 09_aws_cloudwatch
- ✅ 10_python_logging
- ✅ 11_dbt
- ✅ 12_parquet
- ✅ 13_python_concurrency
- ⏸ 14-41 (Capital One + Fundamentals + Advanced — NOT STARTED)

### _manager Folder (D:\StudyBook\tutorials\_manager\)
- PROJECT_STATE.md — this file
- DOCKER_INVENTORY.md — all containers, ports, connection strings
- ROADMAP.md — 41-topic status table
- QUICK_REFERENCE.md — one-page cheat sheet
- prompting_workflows/audio_pipeline.md
- prompting_workflows/html_pages.md
- prompting_workflows/tutorials.md
- session_log/SESSION_TEMPLATE.md
- session_log/2026-04-25.md

---

## ⏳ IN PROGRESS

### Tutorial Prompt Files — Capital One Batch (14-23)
- 14_encryption, 15_data_anonymization_pii, 16_aws_iam
- 17_postgresql, 18_sql_patterns, 19_python_testing
- 20_pydantic, 21_aws_redshift, 22_aws_athena, 23_sqlalchemy

### Tutorial Prompt Files — Fundamentals + Advanced (24-41)
- 24-30: pandas, numpy, polars, duckdb, data_stubbing, streamlit, fastapi
- 31-41: aws_lambda, aws_dynamodb, aws_msk_kafka, aws_bedrock, terraform,
         docker, cicd, aws_ecs, aws_cloudformation, opensearch, snowflake_pyiceberg

---

## 🔜 NEXT STEPS (priority order)

1. **Write tutorial prompt files 14-41** (Capital One + rest)
3. **Update tutorial prompts** to reference existing Docker stack (see DOCKER_INVENTORY.md)
4. **Use ChatGPT to generate actual tutorial .py files** — paste prompt.md per topic
5. **Test generated code** natively against AWS + existing Docker containers
6. **Phase 1 audio regeneration** — 8 existing learning pages may need audio refresh
   with new Project 1 prompt (no rotating bridge phrases)
7. **Tutorials index page** on the website linking to all tutorial folders

---

## KEY SCRIPTS

| Script | Command | Purpose |
|---|---|---|
| Sync to phone | `.\scripts\sync_studybook_to_phone.ps1` | Copy new MP3s + playlists to Pixel |
| Sync dry run | `.\scripts\sync_studybook_to_phone.ps1 -DryRun` | Preview what would sync |
| Audio pipeline | `.\scripts\run_mission_audio.ps1 -Slug {slug} -ChunkSize 750` | Generate MP3 |

---

## KEY PATHS

| What | Path |
|---|---|
| Audio MP3s | `D:\temp\studybook_audio\{slug}\final_{slug}.mp3` |
| Website source | `D:\StudyBook\temp\seanlgirgis.github.io\learning\` |
| Gap prompts | `D:\StudyBook\temp\gap\` |
| Tutorials | `D:\StudyBook\tutorials\` |
| Phone music | `C:\Users\shareuser\CrossDevice\Pixel 8 Pro\storage\Music\StudyBook\` |
| ChatGPT P1 prompt | `D:\users\shareuser\Downloads\Project-1-Audioscript-Maker.txt` |
| ChatGPT P2 prompt | `D:\users\shareuser\Downloads\Project2_HTML_MAKER.txt` |
