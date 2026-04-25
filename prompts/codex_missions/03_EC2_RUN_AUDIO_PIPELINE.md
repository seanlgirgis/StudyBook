# MISSION 03 — Run Audio Pipeline: Amazon EC2
# Working directory: D:\StudyBook\
# Touches: temp\jobsearch\ (read script, write audio clips)
# Prerequisite: Mission 02 complete — audio_script_aws-ec2.md must exist

---

## WORKING DIRECTORY REMINDER

```powershell
Get-Location   # must show D:\StudyBook
```
All commands below are relative to D:\StudyBook\. Use no absolute paths.

---

## THREE REPOSITORIES INVOLVED IN THIS MISSION

```
D:\StudyBook\                                       ← ROOT (working directory)
├── env_setter.ps1                                  ← run this first — loads OPENAI_API_KEY
└── temp\jobsearch\                                 ← REPO 2 — all activity in this mission
        scripts\
            generate_audio_generic.py               ← TTS pipeline script
        data\interview_prep\audio_prep\aws-ec2\
            audio_script_aws-ec2.md                 ← INPUT (from Mission 02)
            audio_clips\                            ← created by pipeline — clips go here
                01_HOST.mp3
                02_SEAN.mp3
                ...
                filelist.txt
            final_aws-ec2.mp3                       ← OUTPUT — stitched final file
            UPLOAD_INSTRUCTIONS.md                  ← OUTPUT — R2 upload guide for Sean
```

REPO 3 (temp\seanlgirgis.github.io\) is NOT touched in this mission.

---

## STEP 1 — VERIFY INPUT SCRIPT EXISTS AND IS VALID

Check the file exists:
```powershell
Test-Path "temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\audio_script_aws-ec2.md"
```
Expected: `True`. If `False`: STOP — run Mission 02 first.

Read the file and confirm all of these:
- [ ] `## API INSTRUCTIONS` header block is present at the top
- [ ] At least 10 `**[HOST — voice: nova]**` or `**[SEAN — voice: onyx]**` blocks exist
- [ ] `## END OF SCRIPT` marker is at the bottom
- [ ] No block has both speakers merged into one
- [ ] No block is missing the `---` divider

If any check fails: STOP. Report the exact problem. Do not proceed to Step 2.

---

## STEP 2 — LOAD PYTHON ENVIRONMENT

Run from D:\StudyBook\ root:
```powershell
.\env_setter.ps1
```

Verify the API key loaded:
```powershell
python -c "import os; print(bool(os.getenv('OPENAI_API_KEY')))"
```
Expected: `True`
If `False`: STOP — report "OPENAI_API_KEY not loaded. env_setter.ps1 may have failed."

---

## STEP 3 — RUN AUDIO GENERATION

```powershell
python temp\jobsearch\scripts\generate_audio_generic.py `
  --script "temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\audio_script_aws-ec2.md" `
  --output "temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\audio_clips"
```

The script:
- Parses all `**[SPEAKER — voice: voice_name]**` blocks
- Calls gpt-4o-mini-tts per block (auto-falls back to gpt-4o-mini-audio-preview)
- Saves numbered MP3 clips: `01_HOST.mp3`, `02_SEAN.mp3`, `03_HOST.mp3`, ...
- Skips existing files — safe to re-run if interrupted

Watch for these errors:
- `OPENAI_API_KEY not found` → Step 2 failed — re-run env_setter.ps1
- `No speaker blocks found` → Script format is wrong — return to Mission 02
- `Both models failed for block N` → API error — note block number, retry once

Expected terminal output:
```
Script: audio_script_aws-ec2.md
Output: temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\audio_clips
Blocks found: [N]

[01/N] HOST (nova) — [X] chars
         -> Saved: 01_HOST.mp3 (model: gpt-4o-mini-tts)
[02/N] SEAN (onyx) — [X] chars
         -> Saved: 02_SEAN.mp3 (model: gpt-4o-mini-tts)
...
Done. [N] MP3 files in ...audio_clips
```

After completion — list clips directory and confirm no numbering gaps:
```powershell
Get-ChildItem "temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\audio_clips" -Filter "*.mp3" | Select-Object Name
```

---

## STEP 4 — STITCH CLIPS INTO FINAL FILE

Navigate to the clips folder:
```powershell
cd "temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\audio_clips"
```

Create ordered filelist:
```powershell
(Get-ChildItem -Filter "*.mp3" | Sort-Object Name | ForEach-Object { "file '$($_.Name)'" }) | Out-File -Encoding utf8 filelist.txt
```

Verify the list is in correct ascending order:
```powershell
Get-Content filelist.txt
```
Expected (example):
```
file '01_HOST.mp3'
file '02_SEAN.mp3'
file '03_HOST.mp3'
...
```
If order is wrong: do not proceed — re-run the Get-ChildItem command above.

Stitch with ffmpeg:
```powershell
ffmpeg -f concat -safe 0 -i filelist.txt -c copy ..\final_aws-ec2.mp3
```
Expected: ffmpeg processes all clips and exits cleanly (no error — "muxing overhead" line is normal).

Return to root:
```powershell
cd D:\StudyBook
```

Verify output file:
```powershell
Test-Path "temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\final_aws-ec2.mp3"
Get-Item "temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\final_aws-ec2.mp3" | Select-Object Length
```
Expected: file exists, size > 5,000,000 bytes (5 MB minimum — a 10-min MP3 at 64kbps ≈ 5 MB).

Get duration to confirm completeness:
```powershell
ffprobe -v quiet -show_entries format=duration -of csv=p=0 "temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\final_aws-ec2.mp3"
```
Expected: between 600 and 900 (seconds). If under 300, blocks were dropped — investigate.

---

## STEP 5 — CREATE UPLOAD INSTRUCTIONS FOR SEAN

Create this file (Sean uploads manually — Codex cannot push to R2):
```
temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\UPLOAD_INSTRUCTIONS.md
```

Content:
```markdown
# R2 Upload Instructions — Amazon EC2 Audio

## File to upload
Relative path: temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\final_aws-ec2.mp3

## Target filename on R2
final_aws-ec2.mp3

## Expected public URL after upload
https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-ec2.mp3

## Steps
1. Open Cloudflare R2 dashboard
2. Navigate to the learning hub media bucket
3. Upload: final_aws-ec2.mp3
4. Confirm the public URL returns audio (open in browser — should play)
5. Tell Codex: "EC2 audio uploaded — run Mission 04"

## What Mission 04 will do
Update temp\seanlgirgis.github.io\learning\aws-ec2.html
Replace old NotebookLM audio src with:
https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-ec2.mp3
```

---

## VERIFICATION CHECKLIST

- [ ] Working directory is D:\StudyBook\ throughout
- [ ] Input script verified — all format checks passed
- [ ] OPENAI_API_KEY loaded (printed True)
- [ ] All [N] MP3 clips generated — no numbering gaps
- [ ] No block reported "Both models failed"
- [ ] filelist.txt is in ascending order
- [ ] ffmpeg ran cleanly
- [ ] final_aws-ec2.mp3 exists at `temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\`
- [ ] File size > 5 MB
- [ ] Duration between 600–900 seconds
- [ ] UPLOAD_INSTRUCTIONS.md created at correct path
- [ ] Working directory returned to D:\StudyBook\ after cd

Report: "MISSION 03 COMPLETE — final_aws-ec2.mp3 ready — [X]s duration — [size] MB — see UPLOAD_INSTRUCTIONS.md"
Or:     "MISSION 03 BLOCKED at Step [N] — [exact error message]"
