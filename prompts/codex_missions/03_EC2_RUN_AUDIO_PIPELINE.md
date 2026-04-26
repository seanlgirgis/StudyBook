# MISSION 03 — Run Audio Pipeline: Amazon EC2
# Working directory: D:\StudyBook\
# Touches: temp\jobsearch\ (read script), D:\temp\studybook_audio\ (write clips/final)
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
        scripts\run_mission_audio.ps1               ← fail-fast mission runner

D:\temp\studybook_audio\aws-ec2\                    ← OUTPUT ROOT (outside repo)
    audio_clips\                                    ← generated clips
    final_aws-ec2.mp3                               ← stitched final output
    UPLOAD_INSTRUCTIONS.md                          ← R2 upload guide for Sean
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

## STEP 3 — RUN FAIL-FAST MISSION RUNNER (RECOMMENDED)

```powershell
.\scripts\run_mission_audio.ps1 `
  "temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\audio_script_aws-ec2.md" `
  -ChunkSize 750 `
  -RequestTimeoutSeconds 120
```

The runner:
- Loads `env_setter.ps1 -NonInteractive` (no hanging prompt path)
- Calls `generate_audio_generic.py` with fail-fast behavior
- Uses chunking at natural sentence boundaries
- Target chunk size is `750` chars, with slight over/under allowed to preserve sentence stops
- Never cuts mid-sentence or across speaker blocks
- Writes all generated artifacts to `D:\temp\studybook_audio\aws-ec2\...` (repo stays clean)
- Exits non-zero immediately on generation or stitch failure

Watch for these errors:
- `OPENAI_API_KEY not found` → Step 2 failed — re-run env_setter.ps1
- `No speaker blocks found` → Script format is wrong — return to Mission 02
- `Both models failed for chunk XX` → API/model issue — run again after fixing key/model state
- non-zero exit from runner → STOP and report exact error

---

## STEP 4 — VERIFY OUTPUTS (C:\temp LOCATION)

```powershell
Test-Path "D:\temp\studybook_audio\aws-ec2\final_aws-ec2.mp3"
Get-Item "D:\temp\studybook_audio\aws-ec2\final_aws-ec2.mp3" | Select-Object Length
ffprobe -v quiet -show_entries format=duration -of csv=p=0 "D:\temp\studybook_audio\aws-ec2\final_aws-ec2.mp3"
```

Expected:
- file exists
- size > 5,000,000 bytes
- duration between 600 and 900 seconds

---

## STEP 5 — CONFIRM UPLOAD INSTRUCTIONS EXISTS

Runner should create this file automatically:
```
D:\temp\studybook_audio\aws-ec2\UPLOAD_INSTRUCTIONS.md
```

If missing, create it manually with the same content template from previous mission runs.

---

## VERIFICATION CHECKLIST

- [ ] Working directory is D:\StudyBook\ throughout
- [ ] Input script verified — all format checks passed
- [ ] OPENAI_API_KEY loaded (printed True)
- [ ] Runner command completed with zero exit code
- [ ] All generated clips/final are in `D:\temp\studybook_audio\aws-ec2\`
- [ ] Chunking used `--chunk-size 750`
- [ ] Chunk splits happen only at natural sentence stops (no mid-sentence cuts)
- [ ] No chunk crosses speaker boundaries
- [ ] No block reported "Both models failed"
- [ ] final_aws-ec2.mp3 exists at `D:\temp\studybook_audio\aws-ec2\`
- [ ] File size > 5 MB
- [ ] Duration between 600–900 seconds
- [ ] UPLOAD_INSTRUCTIONS.md created at `D:\temp\studybook_audio\aws-ec2\`

Report: "MISSION 03 COMPLETE — final_aws-ec2.mp3 ready — [X]s duration — [size] MB — see UPLOAD_INSTRUCTIONS.md"
Or:     "MISSION 03 BLOCKED at Step [N] — [exact error message]"
