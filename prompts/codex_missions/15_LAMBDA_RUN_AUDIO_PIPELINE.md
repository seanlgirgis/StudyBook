# MISSION 15 — Run Audio Pipeline: AWS Lambda
# Working directory: D:\StudyBook\
# Prerequisite: Mission 14 complete
# Output root: D:\temp\studybook_audio\aws-lambda\

---

## RUN

```powershell
cd D:\StudyBook
.\scripts\run_mission_audio.ps1 "temp\jobsearch\data\interview_prep\audio_prep\aws-lambda\audio_script_aws-lambda.md" -ChunkSize 750 -RequestTimeoutSeconds 120
```

---

## VERIFY

```powershell
Test-Path "D:\temp\studybook_audio\aws-lambda\final_aws-lambda.mp3"
Get-Item "D:\temp\studybook_audio\aws-lambda\final_aws-lambda.mp3" | Select-Object Length
ffprobe -v quiet -show_entries format=duration -of csv=p=0 "D:\temp\studybook_audio\aws-lambda\final_aws-lambda.mp3"
```

Expected:
- exists = True
- size > 5,000,000 bytes
- duration between 500 and 900 seconds

---

## UPLOAD INSTRUCTIONS FILE

Confirm:

```powershell
Test-Path "D:\temp\studybook_audio\aws-lambda\UPLOAD_INSTRUCTIONS.md"
```

If missing, create it manually with slug `aws-lambda` and filename `final_aws-lambda.mp3`.

---

## REPORT

`MISSION 15 COMPLETE — final_aws-lambda.mp3 ready — [X]s duration — [size] MB — see UPLOAD_INSTRUCTIONS.md`

Do not run Mission 16 until user confirms:

`Lambda audio uploaded — run Mission 16`
