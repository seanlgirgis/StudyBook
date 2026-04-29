# StudyBook Audio System — Handoff Guide
**Generated:** 2026-04-26  
**Full path:** `D:\Workarea\StudyBook\tutorials\_manager\AUDIO_HANDOFF.md`

---

## 1. What This System Is

A set of **56 MP3 interview-prep audio files** — one per DE/cloud topic — organized as
podcast-style conversations (HOST asks, SEAN answers). The files live locally on your
Windows machine and sync to your **Pixel 8 Pro** for commute listening.

**Three delivery channels:**
1. **Phone** — synced via PowerShell script to Music app
2. **Cloudflare R2** — public CDN URLs for web/HTML page playback
3. **Local playback** — play directly from `D:\temp\studybook_audio\`

---

## 2. Directory Structure

### Root — Audio Library
```
D:\temp\studybook_audio\
│
├── PL-01 Toyota Interview Prep.m3u        ← 18 tracks
├── PL-02 Capital One Interview Prep.m3u   ← 18 tracks
├── PL-03 AWS Foundations.m3u              ← 9 tracks
├── PL-04 AWS Data Stack.m3u               ← 9 tracks
├── PL-05 Streaming & Real-Time.m3u        ← 6 tracks
├── PL-06 Python Engineering.m3u           ← 11 tracks
├── PL-07 Data Engineering Fundamentals.m3u← 10 tracks
├── PL-08 Engineering Discipline.m3u       ← 8 tracks
├── PL-09 Security & Compliance.m3u        ← 6 tracks
├── PL-10 My Story.m3u                     ← 5 tracks
├── PL-11 Commute Starter.m3u              ← 10 tracks (best high-signal picks)
├── PL-12 Local Analytics Stack.m3u        ← 5 tracks
│
├── apache-airflow/
│   ├── final_apache-airflow.mp3           ← THE file that gets synced to phone
│   ├── audio_clips/                       ← individual HOST/SEAN clip files
│   │   ├── 01a_HOST.mp3
│   │   ├── 02a_SEAN.mp3
│   │   └── ...
│   └── UPLOAD_INSTRUCTIONS.md            ← R2 upload steps for this topic
│
├── aws-kinesis/
│   ├── final_aws-kinesis.mp3
│   ├── audio_clips/                       ← 40 clips (01a–40a)
│   │   ├── filelist.txt                   ← ffmpeg concat order
│   │   └── *.mp3
│   └── UPLOAD_INSTRUCTIONS.md
│
└── <slug>/                                ← same structure for every topic
```

### One Topic = One Subfolder Pattern
```
D:\temp\studybook_audio\<slug>\
  final_<slug>.mp3          ← concatenated final audio (synced to phone + uploaded to R2)
  audio_clips\              ← individual exchange clips
    01a_HOST.mp3            ← HOST question/intro
    02a_SEAN.mp3            ← SEAN answer
    02b_SEAN.mp3            ← SEAN continuation (if long)
    03a_HOST.mp3
    ...
    filelist.txt            ← ffmpeg concat list
  UPLOAD_INSTRUCTIONS.md    ← R2 bucket upload guide for this topic
```

---

## 3. All 56 Final MP3 Files

| Slug | Final MP3 | R2 URL |
|---|---|---|
| apache-airflow | `final_apache-airflow.mp3` | `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_apache-airflow.mp3` |
| apache-flink | `final_apache-flink.mp3` | `…/final_apache-flink.mp3` |
| apache-kafka | `final_apache-kafka.mp3` | `…/final_apache-kafka.mp3` |
| aws-athena | `final_aws-athena.mp3` | `…/final_aws-athena.mp3` |
| aws-bedrock | `final_aws-bedrock.mp3` | `…/final_aws-bedrock.mp3` |
| aws-cloudformation | `final_aws-cloudformation.mp3` | `…/final_aws-cloudformation.mp3` |
| aws-cloudwatch | `final_aws-cloudwatch.mp3` | `…/final_aws-cloudwatch.mp3` |
| aws-dynamodb | `final_aws-dynamodb.mp3` | `…/final_aws-dynamodb.mp3` |
| aws-ec2 | `final_aws-ec2.mp3` | `…/final_aws-ec2.mp3` |
| aws-ecs | `final_aws-ecs.mp3` | `…/final_aws-ecs.mp3` |
| aws-emr | `final_aws-emr.mp3` | `…/final_aws-emr.mp3` |
| aws-eventbridge | `final_aws-eventbridge.mp3` | `…/final_aws-eventbridge.mp3` |
| aws-glue | `final_aws-glue.mp3` | `…/final_aws-glue.mp3` |
| aws-iam | `final_aws-iam.mp3` | `…/final_aws-iam.mp3` |
| aws-kinesis | `final_aws-kinesis.mp3` | `…/final_aws-kinesis.mp3` |
| aws-lambda | `final_aws-lambda.mp3` | `…/final_aws-lambda.mp3` |
| aws-msk-kafka | `final_aws-msk-kafka.mp3` | `…/final_aws-msk-kafka.mp3` |
| aws-redshift | `final_aws-redshift.mp3` | `…/final_aws-redshift.mp3` |
| aws-s3 | `final_aws-s3.mp3` | `…/final_aws-s3.mp3` |
| aws-step-functions | `final_aws-step-functions.mp3` | `…/final_aws-step-functions.mp3` |
| aws-vpc | `final_aws-vpc.mp3` | `…/final_aws-vpc.mp3` |
| cicd-data-engineering | `final_cicd-data-engineering.mp3` | `…/final_cicd-data-engineering.mp3` |
| cicd-github-ecs | `final_cicd-github-ecs.mp3` | `…/final_cicd-github-ecs.mp3` |
| citi-telemetry | `final_citi-telemetry.mp3` | `…/final_citi-telemetry.mp3` |
| data-anonymization-pii | `final_data-anonymization-pii.mp3` | `…/final_data-anonymization-pii.mp3` |
| data-modeling | `final_data-modeling.mp3` | `…/final_data-modeling.mp3` |
| data-stubbing-synthetic | `final_data-stubbing-synthetic.mp3` | `…/final_data-stubbing-synthetic.mp3` |
| dbt | `final_dbt.mp3` | `…/final_dbt.mp3` |
| de-miscellany | `final_de-miscellany.mp3` | `…/final_de-miscellany.mp3` |
| delta-lake | `final_delta-lake.mp3` | `…/final_delta-lake.mp3` |
| docker-data-engineering | `final_docker-data-engineering.mp3` | `…/final_docker-data-engineering.mp3` |
| duckdb | `final_duckdb.mp3` | `…/final_duckdb.mp3` |
| encryption-data-engineering | `final_encryption-data-engineering.mp3` | `…/final_encryption-data-engineering.mp3` |
| fastapi | `final_fastapi.mp3` | `…/final_fastapi.mp3` |
| g6-appmon | `final_g6-appmon.mp3` | `…/final_g6-appmon.mp3` |
| git-data-engineering | `final_git-data-engineering.mp3` | `…/final_git-data-engineering.mp3` |
| horizon-scale | `final_horizon-scale.mp3` | `…/final_horizon-scale.mp3` |
| interview-master | `final_interview-master.mp3` | `…/final_interview-master.mp3` |
| job-search-ai | `final_job-search-ai.mp3` | `…/final_job-search-ai.mp3` |
| numpy | `final_numpy.mp3` | `…/final_numpy.mp3` |
| opensearch | `final_opensearch.mp3` | `…/final_opensearch.mp3` |
| pandas | `final_pandas.mp3` | `…/final_pandas.mp3` |
| parquet | `final_parquet.mp3` | `…/final_parquet.mp3` |
| pipeline-design | `final_pipeline-design.mp3` | `…/final_pipeline-design.mp3` |
| polars | `final_polars.mp3` | `…/final_polars.mp3` |
| postgresql | `final_postgresql.mp3` | `…/final_postgresql.mp3` |
| pydantic | `final_pydantic.mp3` | `…/final_pydantic.mp3` |
| pyspark | `final_pyspark.mp3` | `…/final_pyspark.mp3` |
| python-concurrency | `final_python-concurrency.mp3` | `…/final_python-concurrency.mp3` |
| python-logging-observability | `final_python-logging-observability.mp3` | `…/final_python-logging-observability.mp3` |
| python-testing-pipelines | `final_python-testing-pipelines.mp3` | `…/final_python-testing-pipelines.mp3` |
| snowflake-pyiceberg | `final_snowflake-pyiceberg.mp3` | `…/final_snowflake-pyiceberg.mp3` |
| sql-patterns | `final_sql-patterns.mp3` | `…/final_sql-patterns.mp3` |
| sqlalchemy | `final_sqlalchemy.mp3` | `…/final_sqlalchemy.mp3` |
| streamlit | `final_streamlit.mp3` | `…/final_streamlit.mp3` |
| terraform | `final_terraform.mp3` | `…/final_terraform.mp3` |

> R2 base URL: `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/`  
> ⚠️ `Snowflake/` folder has `audio_script_snowflake-pyiceberg.md` but no `final_*.mp3` yet.

---

## 4. The 12 Playlists

Playlist files live flat in `D:\temp\studybook_audio\`. They reference `final_*.mp3` by
filename only (no path prefix) — this works on phone because all MP3s are in the same
Music/StudyBook folder.

| File | Playlist Name | Tracks | Best used for |
|---|---|---|---|
| `PL-01 Toyota Interview Prep.m3u` | Toyota Interview Prep | 18 | Toyota interview cycle |
| `PL-02 Capital One Interview Prep.m3u` | Capital One Interview Prep | 18 | Capital One interview cycle |
| `PL-03 AWS Foundations.m3u` | AWS Foundations | 9 | Cloud fundamentals refresh |
| `PL-04 AWS Data Stack.m3u` | AWS Data Stack | 9 | AWS data services deep dive |
| `PL-05 Streaming & Real-Time.m3u` | Streaming & Real-Time | 6 | Kafka / Kinesis focus sessions |
| `PL-06 Python Engineering.m3u` | Python Engineering | 11 | Python library skills |
| `PL-07 Data Engineering Fundamentals.m3u` | DE Fundamentals | 10 | Core DE patterns |
| `PL-08 Engineering Discipline.m3u` | Engineering Discipline | 8 | DevOps/testing mindset |
| `PL-09 Security & Compliance.m3u` | Security & Compliance | 6 | PCI/GDPR/IAM focus |
| `PL-10 My Story.m3u` | My Story | 5 | Personal narrative & past projects |
| `PL-11 Commute Starter.m3u` | Commute Starter | 10 | ⭐ Best high-signal picks for daily commute |
| `PL-12 Local Analytics Stack.m3u` | Local Analytics Stack | 5 | DuckDB/Polars/Pandas modern stack |

---

## 5. Sync Script — Phone

### File
```
D:\Workarea\StudyBook\scripts\sync_studybook_to_phone.ps1
```

### What It Does
1. Supports targeted sync (recommended) for only requested `final_*.mp3` files
2. Can load named file sets from `config/audio/phone_sync_registry.json` (`-RegistryProfile`)
3. Can prune phone destination to exactly the selected set (`-PruneDestination`)
4. Can sync selected playlists to `Music\pl` (`-SyncPlaylists`)
5. Auto-normalizes synced playlists to `#EXTM3U + #EXTINF + relative path` format
6. Smart mode: skips files where destination already has same byte size
7. Prints a summary: copied / skipped / failed counts + total MB transferred

### Destination Path (phone must be connected via USB/MTP)
```
C:\Users\shareuser\CrossDevice\Pixel 8 Pro\storage\Music\StudyBook\
```

### How to Run

**Targeted sync from registry profile (recommended):**
```powershell
cd D:\Workarea\StudyBook
.\scripts\sync_studybook_to_phone.ps1 -RegistryProfile tayota1 -PruneDestination -SyncPlaylists
```

Playlist rule (always): playlists live under `Music\pl`, not `Music\StudyBook`.

**Normal full-library sync (opt-in only):**
```powershell
cd D:\Workarea\StudyBook
.\scripts\sync_studybook_to_phone.ps1
```

**Dry run (see what would happen without writing anything):**
```powershell
.\scripts\sync_studybook_to_phone.ps1 -DryRun
```

**Force overwrite everything:**
```powershell
.\scripts\sync_studybook_to_phone.ps1 -Force
```

### Expected Output (normal run)
```
StudyBook → Pixel 8 Pro Sync
Source : D:\temp\studybook_audio
Dest   : C:\Users\shareuser\CrossDevice\Pixel 8 Pro\storage\Music\StudyBook
Files  : 56 found
Mode   : SMART (skip unchanged)

  COPIED  final_apache-airflow.mp3  (18.4 MB)
  skip    final_aws-kinesis.mp3
  skip    final_aws-cloudwatch.mp3
  ...
  M3U     PL-01 Toyota Interview Prep.m3u
  ...

─────────────────────────────────────
Copied : 3 files  (54.2 MB transferred)
Skipped: 53 files  (already up to date)
Total in destination: 56 mp3 files
─────────────────────────────────────
```

### Prerequisites
- Pixel 8 Pro connected via USB cable
- Phone set to **File Transfer / MTP mode** (not Charging Only)
- Phone unlocked while sync runs
- Windows detects phone in File Explorer under `This PC`

### Troubleshooting
| Problem | Fix |
|---|---|
| `ERROR: Source not found: D:\temp\studybook_audio` | The audio folder moved. Update `$Source` in the script |
| Destination path not found | Phone not connected or not in MTP mode. Connect phone → swipe down → tap USB notification → select "File Transfer" |
| `FAILED final_xxx.mp3 — Access to the path is denied` | Phone screen locked mid-copy. Unlock phone and re-run |
| Playlist doesn't show in music app | App needs to scan for new files. Open app → Settings → Rescan / Refresh library |

---

## 6. Cloudflare R2 Upload — Web Playback

Each topic has an `UPLOAD_INSTRUCTIONS.md` that tells you exactly which file to upload
and what URL it will have.

### Example (apache-airflow)
```
D:\temp\studybook_audio\apache-airflow\UPLOAD_INSTRUCTIONS.md

  File to upload: C:\temp\studybook_audio\apache-airflow\final_apache-airflow.mp3
  Target filename on R2: final_apache-airflow.mp3
  Public URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_apache-airflow.mp3
```

### Upload Steps
1. Go to Cloudflare R2 dashboard (dash.cloudflare.com → R2)
2. Open the `learning hub media` bucket
3. Click **Upload** → select `final_<slug>.mp3`
4. After upload, open the public URL in a browser to confirm playback
5. Tell the HTML page system the upload is done (update the `<audio src="">` tag)

### R2 Base URL
```
https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/
```

All files use the pattern: `final_<slug>.mp3` where slug matches the folder name in
`D:\temp\studybook_audio\`.

---

## 7. How Audio Files Are Made (Production Workflow)

When a new topic needs an audio file, the workflow is:

```
Step 1 — Script
  Ask Claude to generate an audio_script_<slug>.md
  Format: HOST/SEAN alternating exchanges
  Stored in: D:\Workarea\StudyBook\tutorials\_manager\prompting_workflows\audio_pipeline.md

Step 2 — Generate clips
  Each HOST line → generate HOST MP3 clip (text-to-speech or ElevenLabs)
  Each SEAN line → generate SEAN MP3 clip
  Name: 01a_HOST.mp3, 02a_SEAN.mp3, 02b_SEAN.mp3, 03a_HOST.mp3 ...
  Save to: D:\temp\studybook_audio\<slug>\audio_clips\

Step 3 — Concatenate with ffmpeg
  Create filelist.txt:
    file '01a_HOST.mp3'
    file '02a_SEAN.mp3'
    ...
  Run:
    ffmpeg -f concat -safe 0 -i filelist.txt -c copy final_<slug>.mp3

Step 4 — Add to playlist(s)
  Add entry to relevant .m3u files in D:\temp\studybook_audio\
  Format:
    #EXTINF:-1,Topic Display Name
    final_<slug>.mp3

Step 5 — Sync to phone
  Run: .\scripts\sync_studybook_to_phone.ps1

Step 6 — Upload to R2 (for web)
  Follow UPLOAD_INSTRUCTIONS.md in the topic folder
```

---

## 8. What Is Missing / Not Yet Done

| Item | Status | Action needed |
|---|---|---|
| `Snowflake/` topic | Script exists (`audio_script_snowflake-pyiceberg.md`) but no MP3 | Generate clips → ffmpeg concat → add to PL-04 |
| New tutorial topics (Pandas, Polars, DuckDB, Docker, Kafka) | No audio yet | Generate scripts and audio for the 5 new READY_TO_PASTE topics |
| AWS Lambda, Terraform, PyIceberg audio | No audio yet | Generate as prep continues |
| `.m3u` playlists on phone | Currently only work if phone music app supports M3U | Test in Poweramp or VLC on phone |

---

## 9. On-Phone Playback Setup

**Recommended app: Poweramp** (best M3U playlist support on Android)

```
1. Install Poweramp from Play Store
2. Open Poweramp → Settings → Library → Music Folders
3. Add: /storage/emulated/0/Music/StudyBook
4. Settings → Library → Playlists → Enable "Scan for .m3u files"
5. Tap the refresh icon → all 12 playlists appear
6. Tap PL-11 Commute Starter → play
```

**Alternative: VLC for Android** (free, plays M3U directly)
```
1. Install VLC from Play Store
2. Open VLC → Browse → Local Storage → Music → StudyBook
3. Long-press any .m3u file → Add to playlist
```

---

## 10. Quick Reference

| Task | Command / Location |
|---|---|
| Sync to phone | `.\scripts\sync_studybook_to_phone.ps1` |
| Sync dry run | `.\scripts\sync_studybook_to_phone.ps1 -DryRun` |
| Audio files root | `D:\temp\studybook_audio\` |
| Sync script | `D:\Workarea\StudyBook\scripts\sync_studybook_to_phone.ps1` |
| Phone destination | `C:\Users\shareuser\CrossDevice\Pixel 8 Pro\storage\Music\StudyBook\` |
| R2 dashboard | `dash.cloudflare.com → R2 → learning hub media` |
| R2 base URL | `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/` |
| ffmpeg concat | `ffmpeg -f concat -safe 0 -i filelist.txt -c copy final_<slug>.mp3` |
| Audio pipeline doc | `D:\Workarea\StudyBook\tutorials\_manager\prompting_workflows\audio_pipeline.md` |
| Total MP3 files | **56 final MP3s** + 1 missing (Snowflake) |
| Total playlists | **12 M3U files** |

---

*End of audio handoff guide.*
