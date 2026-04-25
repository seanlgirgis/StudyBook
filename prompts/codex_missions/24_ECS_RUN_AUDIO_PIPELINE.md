# MISSION 24 — Run Audio Pipeline: Amazon ECS
# Working directory: D:\StudyBook\
# Prerequisite: Mission 23 complete
# Output root: C:\temp\studybook_audio\aws-ecs\

---

## RUN

```powershell
cd D:\StudyBook
.\scripts\run_mission_audio.ps1 "temp\jobsearch\data\interview_prep\audio_prep\aws-ecs\audio_script_aws-ecs.md" -ChunkSize 750 -RequestTimeoutSeconds 120
```

---

## VERIFY

```powershell
Test-Path "C:\temp\studybook_audio\aws-ecs\final_aws-ecs.mp3"
Get-Item "C:\temp\studybook_audio\aws-ecs\final_aws-ecs.mp3" | Select-Object Length
ffprobe -v quiet -show_entries format=duration -of csv=p=0 "C:\temp\studybook_audio\aws-ecs\final_aws-ecs.mp3"
```

Expected:
- exists = True
- size > 5,000,000 bytes
- duration between 500 and 900 seconds

---

## UPLOAD INSTRUCTIONS FILE

Confirm:

```powershell
Test-Path "C:\temp\studybook_audio\aws-ecs\UPLOAD_INSTRUCTIONS.md"
```

If missing, create it manually with slug `aws-ecs` and filename `final_aws-ecs.mp3`.

---

## REPORT

`MISSION 24 COMPLETE — final_aws-ecs.mp3 ready — [X]s duration — [size] MB — see UPLOAD_INSTRUCTIONS.md`

Do not run Mission 25 until user confirms:

`ECS audio uploaded — run Mission 25`
