# MISSION 12 — Run Audio Pipeline: Amazon Redshift
# Working directory: D:\Workarea\StudyBook\
# Prerequisite: Mission 11 complete
# Output root: C:\temp\studybook_audio\aws-redshift\

---

## RUN

```powershell
cd D:\Workarea\StudyBook
.\scripts\run_mission_audio.ps1 "..\jobsearch\data\interview_prep\audio_prep\aws-redshift\audio_script_aws-redshift.md" -ChunkSize 750 -RequestTimeoutSeconds 120
```

---

## VERIFY

```powershell
Test-Path "C:\temp\studybook_audio\aws-redshift\final_aws-redshift.mp3"
Get-Item "C:\temp\studybook_audio\aws-redshift\final_aws-redshift.mp3" | Select-Object Length
ffprobe -v quiet -show_entries format=duration -of csv=p=0 "C:\temp\studybook_audio\aws-redshift\final_aws-redshift.mp3"
```

Expected:
- exists = True
- size > 5,000,000 bytes
- duration between 500 and 900 seconds

---

## UPLOAD INSTRUCTIONS FILE

Confirm:

```powershell
Test-Path "C:\temp\studybook_audio\aws-redshift\UPLOAD_INSTRUCTIONS.md"
```

If missing, create it manually with slug `aws-redshift` and filename `final_aws-redshift.mp3`.

---

## REPORT

`MISSION 12 COMPLETE — final_aws-redshift.mp3 ready — [X]s duration — [size] MB — see UPLOAD_INSTRUCTIONS.md`

Do not run Mission 13 until user confirms:

`Redshift audio uploaded — run Mission 13`

