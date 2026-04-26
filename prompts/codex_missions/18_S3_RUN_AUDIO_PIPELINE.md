# MISSION 18 — Run Audio Pipeline: Amazon S3
# Working directory: D:\Workarea\StudyBook\
# Prerequisite: Mission 17 complete
# Output root: C:\temp\studybook_audio\aws-s3\

---

## RUN

```powershell
cd D:\Workarea\StudyBook
.\scripts\run_mission_audio.ps1 "..\jobsearch\data\interview_prep\audio_prep\aws-s3\audio_script_aws-s3.md" -ChunkSize 750 -RequestTimeoutSeconds 120
```

---

## VERIFY

```powershell
Test-Path "C:\temp\studybook_audio\aws-s3\final_aws-s3.mp3"
Get-Item "C:\temp\studybook_audio\aws-s3\final_aws-s3.mp3" | Select-Object Length
ffprobe -v quiet -show_entries format=duration -of csv=p=0 "C:\temp\studybook_audio\aws-s3\final_aws-s3.mp3"
```

Expected:
- exists = True
- size > 5,000,000 bytes
- duration between 500 and 900 seconds

---

## UPLOAD INSTRUCTIONS FILE

Confirm:

```powershell
Test-Path "C:\temp\studybook_audio\aws-s3\UPLOAD_INSTRUCTIONS.md"
```

If missing, create it manually with slug `aws-s3` and filename `final_aws-s3.mp3`.

---

## REPORT

`MISSION 18 COMPLETE — final_aws-s3.mp3 ready — [X]s duration — [size] MB — see UPLOAD_INSTRUCTIONS.md`

Do not run Mission 19 until user confirms:

`S3 audio uploaded — run Mission 19`

