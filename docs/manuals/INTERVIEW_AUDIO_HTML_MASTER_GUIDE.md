# Interview Audio + HTML Master Guide

Last updated: 2026-04-26
Primary owner workflow: Sean Girgis

Related tracker:
- [Website Remaining Work Tracker](./WEBSITE_REMAINING_WORK_TRACKER.md)
- [Audio Playlist + Phone Sync Method](./AUDIO_PLAYLIST_SYNC_METHOD.md)

## 1) Mission

This guide is the single source of truth for producing and publishing interview-prep learning content with:

- ChatGPT Project 1 (audio script generation)
- StudyBook audio runner (clip generation + final MP3 stitch)
- ChatGPT Project 2 (learning HTML generation)
- Website wiring in `seanlgirgis.github.io`

## 2) Repository Layout

Working roots:

- `D:\Workarea\StudyBook` (execution/orchestration root)
- `D:\Workarea\jobsearch` (audio script source repo)
- `D:\Workarea\seanlgirgis.github.io` (website repo)

Use relative paths from `D:\Workarea\StudyBook` whenever possible.

## 3) Storage Rules (Non-Negotiable)

Text in repos:

- `..\jobsearch\data\interview_prep\audio_prep\{slug}\audio_script_{slug}.md`
- `..\seanlgirgis.github.io\learning\{slug}.html`
- `..\seanlgirgis.github.io\components\*.html`

Binary outside repos:

- `D:\temp\studybook_audio\{slug}\audio_clips\`
- `D:\temp\studybook_audio\{slug}\final_{slug}.mp3`

Never commit generated MP3 files.

## 4) Environment Prerequisite

Run this first in any shell session that will run the pipeline:

```powershell
cd D:\Workarea\StudyBook
& .\env_setter.ps1
```

## 5) End-to-End Flow (Default)

1. Pick topic + slug.
2. Use Project 1 prompt:
   - `prompts\codex_missions\WebsitePagesAndAudioBYCodexChatgpt\Project-1-Audioscript-Maker.txt`
3. Save generated script to:
   - `..\jobsearch\data\interview_prep\audio_prep\{slug}\audio_script_{slug}.md`
4. Run audio pipeline:

```powershell
.\scripts\run_mission_audio.ps1 "..\jobsearch\data\interview_prep\audio_prep\{slug}\audio_script_{slug}.md" -ChunkSize 750 -RequestTimeoutSeconds 120
```

5. Confirm final MP3 exists:

```powershell
Test-Path "D:\temp\studybook_audio\{slug}\final_{slug}.mp3"
Get-Item "D:\temp\studybook_audio\{slug}\final_{slug}.mp3" | Select-Object FullName,Length,LastWriteTime
```

6. Upload `final_{slug}.mp3` to R2.
7. Use Project 2 prompt:
   - `prompts\codex_missions\WebsitePagesAndAudioBYCodexChatgpt\Project2_HTMl_Maker.txt`
8. Save HTML page to:
   - `..\seanlgirgis.github.io\learning\{slug}.html`
9. Wire discoverability:
   - Update the right component file under `..\seanlgirgis.github.io\components\`.
   - Convert card from planned to clickable live card when needed.

## 6) Required Output Conventions

- Slug style: lowercase + hyphen
- Script filename: `audio_script_{slug}.md`
- Audio filename: `final_{slug}.mp3`
- HTML filename: `{slug}.html`
- Audio URL format:
  - `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_{slug}.mp3`

## 7) Final Verification Commands

Run from `D:\Workarea\StudyBook`.

```powershell
# Page audio binding
Select-String -Path "..\seanlgirgis.github.io\learning\{slug}.html" -Pattern "final_{slug}.mp3|audio/mpeg|<video"

# Component wiring
Select-String -Path "..\seanlgirgis.github.io\components\*.html" -Pattern "{slug}|learning/{slug}.html|Open Reference|Live|Planned"

# Repo binary guard (jobsearch)
Get-ChildItem "..\jobsearch\data\interview_prep\audio_prep" -Recurse -File |
  Where-Object { $_.Name -match "{slug}.*(\.mp3|\.m4a|filelist\.txt)$" } |
  Select-Object FullName
```

Expected outcomes:

- HTML includes correct R2 `final_{slug}.mp3` with `audio/mpeg`
- Card is discoverable and clickable
- No generated binaries in repo paths

## 8) Common Modes

- Full mode: create script + run pipeline + create/update HTML + wire card
- Provided-files mode: script + HTML already exist; run pipeline + patch/wire
- Runner mode: user executes commands manually; agent validates outputs

## 9) Known Issue + Fix (Important)

Issue observed on 2026-04-26:
- ffmpeg concat failed when `filelist.txt` started with UTF-8 BOM (`unknown keyword '﻿file'`).

Fix in `scripts\run_mission_audio.ps1`:
- file list now written as UTF-8 **without BOM**.

## 10) Topic Discovery Guidance

To pick the next topic:

1. Inspect planned cards in `..\seanlgirgis.github.io\components\learning-*.html`.
2. Prefer topics marked planned but not yet in `..\seanlgirgis.github.io\learning\`.
3. Choose one topic and run this guide exactly.

## 11) Parallel Tutorials Workspace

Parallel tutorial work lives here:

- `D:\Workarea\StudyBook\tutorials`

This is separate from the learning-page publish flow, but can be used to stage tutorial artifacts that later feed learning content.

## 12) Mission Prompt Sources

Main folder:

- `D:\Workarea\StudyBook\prompts\codex_missions\WebsitePagesAndAudioBYCodexChatgpt`

Core files:

- `Project-1-Audioscript-Maker.txt`
- `Project2_HTMl_Maker.txt`
- `Existing_work_pipeline_execution_master.md`
- `Existing_work_pipeline_execution_provided_files_master.md`
- `Existing_work_pipeline_execution_provided_files_runner_mode_master.md`

Faster HTML generation pattern (persisted):

- Website rules file: `..\..\..\seanlgirgis.github.io\AGENTS.md`
- Reusable HTML shell: `..\..\..\seanlgirgis.github.io\learning\_page-template.html`
- Short prompt template: `..\prompts\codex_missions\WebsitePagesAndAudioBYCodexChatgpt\Project2_ShortPrompt_Template.md`

Use a short per-topic prompt that references those two files instead of pasting the full CSS/rules each run.

## 13) One-Page Quick Start

```powershell
cd D:\Workarea\StudyBook
& .\env_setter.ps1
.\scripts\run_mission_audio.ps1 "..\jobsearch\data\interview_prep\audio_prep\{slug}\audio_script_{slug}.md" -ChunkSize 750 -RequestTimeoutSeconds 120
Test-Path "D:\temp\studybook_audio\{slug}\final_{slug}.mp3"
```

Then upload to R2, save `{slug}.html`, wire component card to `learning/{slug}.html`, and run verification checks.
