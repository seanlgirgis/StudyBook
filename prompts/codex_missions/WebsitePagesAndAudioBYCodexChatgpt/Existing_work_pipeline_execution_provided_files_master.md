# PIPELINE EXECUTION MASTER — PROVIDED FILES MODE
# Working directory: D:\Workarea\StudyBook\
# Purpose: Use this when Sean provides BOTH files up front and Codex finishes end-to-end.
# Created: 2026-04-25

---

## WHEN TO USE THIS RUNBOOK

Use this runbook only when these already exist:
- HTML page file exists (example: `..\seanlgirgis.github.io\learning\aws-vpc.html`)
- Audio script exists (example: `..\jobsearch\data\interview_prep\audio_prep\aws-vpc\audio_script_aws-vpc.md`)

No script-generation mission is needed in this mode.

---

## REQUIRED INPUTS (FROM SEAN)

- `topic_slug` (example: `aws-vpc`)
- `html_file` path
- `audio_script_file` path
- Optional: component file path for card linking (example: `..\seanlgirgis.github.io\components\learning-aws-security.html`)

---

## EXECUTION FLOW (PROVIDED FILES MODE)

1. Preflight
- Confirm working directory: `D:\Workarea\StudyBook`
- Confirm both files exist (`Test-Path`)
- Confirm script path matches slug naming convention

2. Run audio pipeline from existing script (fail-fast)
```powershell
cd D:\Workarea\StudyBook
.\scripts\run_mission_audio.ps1 "..\jobsearch\data\interview_prep\audio_prep\{topic_slug}\audio_script_{topic_slug}.md" -ChunkSize 750 -RequestTimeoutSeconds 120
```

3. Validate output location (outside repo)
- `D:\temp\studybook_audio\{topic_slug}\audio_clips\`
- `D:\temp\studybook_audio\{topic_slug}\final_{topic_slug}.mp3`
- `D:\temp\studybook_audio\{topic_slug}\UPLOAD_INSTRUCTIONS.md`

4. Repo cleanliness guard
- Ensure no generated MP3/M4A/filelist landed in repo paths
```powershell
rg --files -g "*{topic_slug}*.mp3" -g "*{topic_slug}*.m4a" -g "*{topic_slug}*filelist.txt" ..\jobsearch\data\interview_prep\audio_prep
```
Expected: no matches

5. Wait for R2 upload confirmation from Sean
- Sean uploads: `D:\temp\studybook_audio\{topic_slug}\final_{topic_slug}.mp3`
- Sean provides live URL:
  - `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_{topic_slug}.mp3`

6. Update HTML page file
- Ensure `<audio><source>` points to live R2 URL and `type="audio/mpeg"`
- Preserve CSS system and encoding safety
- Do not add binary assets to repo

7. Activate site linking (if card is still planned)
- Find card in component file (usually under `..\seanlgirgis.github.io\components\...`)
- Convert planned card to clickable live card:
  - title `<a href="learning/{topic_slug}.html">...`
  - `Open Reference →` link
  - optional full-card click `onclick="window.location.href='learning/{topic_slug}.html'"`
- Change badge from planned/upload-pending to live when R2 is confirmed

8. Final verification
- HTML contains correct final MP3 URL
- Card is clickable to `learning/{topic_slug}.html`
- No mojibake tokens (`�`, `Â`, `Ã`, `â`, `ï`, `ð`)

---

## BINARY FILE RULE (NON-NEGOTIABLE)

Never write generated audio files into `D:\Workarea\StudyBook`.

In repo (text only):
- `..\jobsearch\data\interview_prep\audio_prep\{topic_slug}\audio_script_{topic_slug}.md`
- HTML/component files under `..\seanlgirgis.github.io\...`

Outside repo (binary):
- `D:\temp\studybook_audio\{topic_slug}\audio_clips\`
- `D:\temp\studybook_audio\{topic_slug}\final_{topic_slug}.mp3`

---

## QUICK COMMAND SET (COPY/PASTE)

```powershell
cd D:\Workarea\StudyBook

# 1) Preflight
Test-Path "..\seanlgirgis.github.io\learning\{topic_slug}.html"
Test-Path "..\jobsearch\data\interview_prep\audio_prep\{topic_slug}\audio_script_{topic_slug}.md"

# 2) Run pipeline
.\scripts\run_mission_audio.ps1 "..\jobsearch\data\interview_prep\audio_prep\{topic_slug}\audio_script_{topic_slug}.md" -ChunkSize 750 -RequestTimeoutSeconds 120

# 3) Validate output
Test-Path "D:\temp\studybook_audio\{topic_slug}\final_{topic_slug}.mp3"
Get-Item "D:\temp\studybook_audio\{topic_slug}\final_{topic_slug}.mp3" | Select-Object FullName,Length,LastWriteTime

# 4) Guard repo cleanliness
rg --files -g "*{topic_slug}*.mp3" -g "*{topic_slug}*.m4a" -g "*{topic_slug}*filelist.txt" ..\jobsearch\data\interview_prep\audio_prep
```

---

## DEFINITION OF DONE (PROVIDED FILES MODE)

- [ ] Existing script consumed successfully by runner
- [ ] Final MP3 generated in `D:\temp\studybook_audio\{topic_slug}\`
- [ ] R2 live URL confirmed by Sean
- [ ] HTML page points to live URL
- [ ] Site card/link activated and clickable
- [ ] Status badge set to Live
- [ ] No generated binary artifacts inside repo

---

## EXAMPLE (VPC)

Inputs:
- HTML: `..\seanlgirgis.github.io\learning\aws-vpc.html`
- Script: `..\jobsearch\data\interview_prep\audio_prep\aws-vpc\audio_script_aws-vpc.md`

Pipeline result:
- `D:\temp\studybook_audio\aws-vpc\final_aws-vpc.mp3`

Live URL:
- `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-vpc.mp3`

Link activation:
- update `components\learning-aws-security.html` VPC card to clickable live state.



