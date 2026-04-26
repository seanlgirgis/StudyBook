# MISSION 21 — Run Audio Pipeline: Apache Kafka
# Working directory: D:\StudyBook\
# Prerequisite: Mission 20 complete
# Output root: D:\temp\studybook_audio\apache-kafka\

---

## RUN

```powershell
cd D:\StudyBook
.\scripts\run_mission_audio.ps1 "temp\jobsearch\data\interview_prep\audio_prep\apache-kafka\audio_script_apache-kafka.md" -ChunkSize 750 -RequestTimeoutSeconds 120
```

---

## VERIFY

```powershell
Test-Path "D:\temp\studybook_audio\apache-kafka\final_apache-kafka.mp3"
Get-Item "D:\temp\studybook_audio\apache-kafka\final_apache-kafka.mp3" | Select-Object Length
ffprobe -v quiet -show_entries format=duration -of csv=p=0 "D:\temp\studybook_audio\apache-kafka\final_apache-kafka.mp3"
```

Expected:
- exists = True
- size > 5,000,000 bytes
- duration between 500 and 900 seconds

---

## UPLOAD INSTRUCTIONS FILE

Confirm:

```powershell
Test-Path "D:\temp\studybook_audio\apache-kafka\UPLOAD_INSTRUCTIONS.md"
```

If missing, create it manually with slug `apache-kafka` and filename `final_apache-kafka.mp3`.

---

## REPORT

`MISSION 21 COMPLETE — final_apache-kafka.mp3 ready — [X]s duration — [size] MB — see UPLOAD_INSTRUCTIONS.md`

Do not run Mission 22 until user confirms:

`Kafka audio uploaded — run Mission 22`
