# MISSION 06 — Run Audio Pipeline: Amazon Athena
# Working directory: D:\StudyBook\
# Touches: temp\jobsearch\ (read script), C:\temp\studybook_audio\ (write clips/final)
# Prerequisite: Mission 05 complete — audio_script_aws-athena.md must exist

---

## WORKING DIRECTORY REMINDER

```powershell
Get-Location   # must show D:\StudyBook
```
All commands below are relative to D:\StudyBook\. Use no absolute paths.

---

## THREE REPOSITORIES INVOLVED IN THIS MISSION

```
D:\StudyBook\                                         ← ROOT (working directory)
├── env_setter.ps1                                    ← run this first — loads OPENAI_API_KEY
└── temp\jobsearch\                                   ← REPO 2 — all activity in this mission
        scripts\
            generate_audio_generic.py                 ← TTS pipeline script
        data\interview_prep\audio_prep\aws-athena\
            audio_script_aws-athena.md               ← INPUT (from Mission 05)
        scripts\run_mission_audio.ps1                 ← fail-fast mission runner

C:\temp\studybook_audio\aws-athena\                   ← OUTPUT ROOT (outside repo)
    audio_clips\                                      ← generated clips
    final_aws-athena.mp3                              ← stitched final output
    UPLOAD_INSTRUCTIONS.md                            ← R2 upload guide for Sean
```

REPO 3 (temp\seanlgirgis.github.io\) is NOT touched in this mission.

---

## STEP 1 — VERIFY INPUT SCRIPT EXISTS AND IS VALID

Check the file exists:
```powershell
Test-Path "temp\jobsearch\data\interview_prep\audio_prep\aws-athena\audio_script_aws-athena.md"
```
Expected: `True`. If `False`: STOP — run Mission 05 first.

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

## STEP 3 — RUN FAIL-FAST MISSION RUNNER

```powershell
.\scripts\run_mission_audio.ps1 `
  "temp\jobsearch\data\interview_prep\audio_prep\aws-athena\audio_script_aws-athena.md" `
  -ChunkSize 750 `
  -RequestTimeoutSeconds 120
```

The runner:
- Loads `env_setter.ps1 -NonInteractive` (no hanging prompt path)
- Calls `generate_audio_generic.py` with fail-fast behavior
- Uses chunking at natural sentence boundaries
- Target chunk size is `750` chars, with slight over/under allowed to preserve sentence stops
- Never cuts mid-sentence or across speaker blocks
- Writes all generated artifacts to `C:\temp\studybook_audio\aws-athena\...` (repo stays clean)
- Exits non-zero immediately on generation or stitch failure

Watch for these errors:
- `OPENAI_API_KEY not found` → Step 2 failed — re-run env_setter.ps1
- `No speaker blocks found` → Script format is wrong — return to Mission 05
- `Both models failed for chunk XX` → API/model issue — run again after fixing key/model state
- non-zero exit from runner → STOP and report exact error

---

## STEP 4 — VERIFY OUTPUTS

```powershell
Test-Path "C:\temp\studybook_audio\aws-athena\final_aws-athena.mp3"
Get-Item "C:\temp\studybook_audio\aws-athena\final_aws-athena.mp3" | Select-Object Length
ffprobe -v quiet -show_entries format=duration -of csv=p=0 "C:\temp\studybook_audio\aws-athena\final_aws-athena.mp3"
```

Expected:
- file exists
- size > 5,000,000 bytes
- duration between 500 and 900 seconds

---

## STEP 5 — CONFIRM OR CREATE UPLOAD INSTRUCTIONS

Check if the runner created an upload instructions file:
```powershell
Test-Path "C:\temp\studybook_audio\aws-athena\UPLOAD_INSTRUCTIONS.md"
```

If it exists, read and confirm the content is correct.

If it does NOT exist, create it manually:
```powershell
New-Item -ItemType Directory -Force -Path "C:\temp\studybook_audio\aws-athena"
```

Then write `C:\temp\studybook_audio\aws-athena\UPLOAD_INSTRUCTIONS.md` with this content
(fill in actual size and duration from Step 4):

```markdown
# R2 Upload Instructions — Amazon Athena Audio

## File to upload
C:\temp\studybook_audio\aws-athena\final_aws-athena.mp3

## Validated stats
- Size:     [actual bytes] bytes (~[X] MB)
- Duration: [actual seconds] seconds (~[X] minutes)
- Chunks:   [actual chunk count]

## Target filename on R2
final_aws-athena.mp3

## Public URL after upload
https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-athena.mp3

## Upload steps
1. Open Cloudflare R2 dashboard
2. Navigate to bucket: pub-174bd65326be4562b4618ccf6a4a8864
3. Upload: final_aws-athena.mp3
4. Open the URL in a browser — confirm audio plays and is on-topic (Athena content)
5. Tell Codex: "Athena audio uploaded — run Mission 07"

## What Mission 07 will do
File:    temp\seanlgirgis.github.io\learning\aws-athena.html
Change:  Replace <audio src> from old NotebookLM .m4a to:
         https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-athena.mp3
Also:    Update subtitle date to today's date
Also:    Fix .cheat-row column width from 160px to 170px
Keep:    Existing <video> src UNCHANGED
```

---

## VERIFICATION CHECKLIST

- [ ] Working directory is D:\StudyBook\ throughout
- [ ] Input script verified — all format checks passed
- [ ] OPENAI_API_KEY loaded (printed True)
- [ ] Runner command completed with zero exit code
- [ ] All generated clips/final are in `C:\temp\studybook_audio\aws-athena\`
- [ ] Chunking used `--chunk-size 750`
- [ ] Chunk splits happen only at natural sentence stops (no mid-sentence cuts)
- [ ] No chunk crosses speaker boundaries
- [ ] No block reported "Both models failed"
- [ ] final_aws-athena.mp3 exists at `C:\temp\studybook_audio\aws-athena\`
- [ ] File size > 5 MB
- [ ] Duration between 500–900 seconds
- [ ] UPLOAD_INSTRUCTIONS.md created at `C:\temp\studybook_audio\aws-athena\`

Report: "MISSION 06 COMPLETE — final_aws-athena.mp3 ready — [X]s duration — [size] MB — see UPLOAD_INSTRUCTIONS.md"
Or:     "MISSION 06 BLOCKED at Step [N] — [exact error message]"

---

## AFTER THIS MISSION

Sean uploads `final_aws-athena.mp3` to R2, then confirms:
"Athena audio uploaded — run Mission 07"

Do NOT run Mission 07 until that confirmation is received.
