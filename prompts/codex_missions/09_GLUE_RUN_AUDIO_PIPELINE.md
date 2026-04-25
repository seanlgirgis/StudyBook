# MISSION 09 — Run Audio Pipeline: AWS Glue
# Working directory: D:\StudyBook\
# Prerequisite: Mission 08 complete
# Output root: C:\temp\studybook_audio\aws-glue\

---

## RUN

```powershell
cd D:\StudyBook
.\scripts\run_mission_audio.ps1 "temp\jobsearch\data\interview_prep\audio_prep\aws-glue\audio_script_aws-glue.md" -ChunkSize 750 -RequestTimeoutSeconds 120
```

---

## VERIFY

```powershell
Test-Path "C:\temp\studybook_audio\aws-glue\final_aws-glue.mp3"
Get-Item "C:\temp\studybook_audio\aws-glue\final_aws-glue.mp3" | Select-Object Length
ffprobe -v quiet -show_entries format=duration -of csv=p=0 "C:\temp\studybook_audio\aws-glue\final_aws-glue.mp3"
```

Expected:
- exists = True
- size > 5,000,000 bytes
- duration between 500 and 900 seconds

---

## UPLOAD INSTRUCTIONS FILE

Confirm:

```powershell
Test-Path "C:\temp\studybook_audio\aws-glue\UPLOAD_INSTRUCTIONS.md"
```

If missing, create it manually (same template as Athena, slug = `aws-glue`, filename = `final_aws-glue.mp3`).

---

## REPORT

`MISSION 09 COMPLETE — final_aws-glue.mp3 ready — [X]s duration — [size] MB — see UPLOAD_INSTRUCTIONS.md`

Do not run Mission 10 until user confirms:

`Glue audio uploaded — run Mission 10`

