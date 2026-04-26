# PIPELINE EXECUTION MASTER — PROVIDED FILES (RUNNER MODE)
# Working directory: D:\Workarea\StudyBook\
# Purpose: Token-efficient mode where Sean runs all commands manually and Codex only provides/validates commands.
# Created: 2026-04-25

---

## WHEN TO USE THIS RUNBOOK

Use this runbook when all of these are true:
- HTML page already exists
- Audio script already exists
- Sean wants to run every command manually (no autonomous tool execution by Codex)

---

## REQUIRED INPUTS (FROM SEAN)

- Mission file path (this file)
- `html_file` absolute path
- `audio_script_file` absolute path
- Optional: note if page is direct URL only (no nav link)

---

## OPERATING CONTRACT (MANDATORY)

Codex must:
- Not run terminal commands unless Sean explicitly asks.
- Return commands only.
- Return one command per fenced code block.
- Put a short numbered title before each command block.
- Default to PowerShell-compatible commands.
- Prefer PowerShell fallback checks (do not assume `rg` exists).
- Wait for Sean's pasted output before advancing to the next troubleshooting step.
- Enforce correct site wiring by identifying the proper site section/component for the topic.
- Return final discoverability info: section name + component file + page path (or explicit direct URL only note).

Sean will:
- Execute each command.
- Paste output back.
- Upload final MP3 to R2 and share final URL.

---

## STANDARD COMMAND SET (COPY/PASTE TEMPLATE)

### 1. Load Environment
```powershell
cd D:\Workarea\StudyBook; .\env_setter.ps1
```

### 2. Preflight File Check
```powershell
Test-Path "<HTML_FILE_RELATIVE_OR_ABS>"; Test-Path "<AUDIO_SCRIPT_FILE_RELATIVE_OR_ABS>"
```

### 3. Run Audio Pipeline
```powershell
.\scripts\run_mission_audio.ps1 "<AUDIO_SCRIPT_FILE_RELATIVE_OR_ABS>" -ChunkSize 750 -RequestTimeoutSeconds 120
```

### 4. Verify Final MP3 Exists
```powershell
Test-Path "C:\temp\studybook_audio\<TOPIC_SLUG>\final_<TOPIC_SLUG>.mp3"; Get-Item "C:\temp\studybook_audio\<TOPIC_SLUG>\final_<TOPIC_SLUG>.mp3" | Select-Object FullName,Length,LastWriteTime
```

### 5. Verify Duration
```powershell
ffprobe -v quiet -show_entries format=duration -of csv=p=0 "C:\temp\studybook_audio\<TOPIC_SLUG>\final_<TOPIC_SLUG>.mp3"
```

### 6. Repo Cleanliness Guard (PowerShell fallback)
```powershell
Get-ChildItem "..\jobsearch\data\interview_prep\audio_prep" -Recurse -File | Where-Object { $_.Name -match '<TOPIC_SLUG>.*(\.mp3|\.m4a|filelist\.txt)$' } | Select-Object FullName
```

### 7. Verify HTML Audio Binding
```powershell
Select-String -Path "<HTML_FILE_RELATIVE_OR_ABS>" -Pattern "final_<TOPIC_SLUG>.mp3|audio/mpeg" | ForEach-Object { "{0}:{1}" -f $_.LineNumber, $_.Line.Trim() }
```

### 8. Optional Direct-URL Reminder (No Nav Link)
```powershell
Write-Host "Direct URL only: https://seanlgirgis.github.io/<PAGE_FILE_NAME>.html"
```

### 9. Detect Existing Section/Card Wiring
```powershell
Select-String -Path "..\seanlgirgis.github.io\components\*.html" -Pattern "<TOPIC_SLUG>|<PAGE_FILE_NAME>.html|<TOPIC_KEYWORD_1>|<TOPIC_KEYWORD_2>" | ForEach-Object { "{0}:{1}:{2}" -f $_.Path, $_.LineNumber, $_.Line.Trim() }
```

### 10. Verify Section Wiring State
```powershell
Select-String -Path "<COMPONENT_FILE_FROM_STEP_9>" -Pattern "<PAGE_FILE_NAME>.html|Open Reference|View Project|Coming soon|Live|Case Study|Active" | ForEach-Object { "{0}:{1}" -f $_.LineNumber, $_.Line.Trim() }
```

---

## R2 HANDOFF

After Sean uploads audio, Sean sends:
- `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_<TOPIC_SLUG>.mp3`

Codex then returns one verification command:

```powershell
Select-String -Path "<HTML_FILE_RELATIVE_OR_ABS>" -Pattern "https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_<TOPIC_SLUG>.mp3|audio/mpeg" | ForEach-Object { "{0}:{1}" -f $_.LineNumber, $_.Line.Trim() }
```

---

## DEFINITION OF DONE (RUNNER MODE)

- [ ] Sean ran pipeline successfully.
- [ ] Final MP3 exists in `C:\temp\studybook_audio\<TOPIC_SLUG>\`.
- [ ] Duration and file size validated.
- [ ] No generated binary artifacts in repo audio_prep path.
- [ ] HTML points to final MP3 with `audio/mpeg`.
- [ ] R2 URL verified in page source.
- [ ] Correct site section wiring verified (or explicit direct URL only confirmed).
- [ ] Final user-facing location summary provided.

---

## REQUIRED FINAL RESPONSE FORMAT (FROM CODEX)

Codex must end with this summary block:

- `Section:` `<SECTION_NAME or Direct URL only>`
- `Page Path:` `<repo-relative page path>`
- `Component File:` `<repo-relative component path or N/A>`
- `Card Status:` `<Live / Case Study / Active / Planned / N/A>`
- `Direct URL:` `https://seanlgirgis.github.io/<PAGE_FILE_NAME>.html`

---

## BINARY FILE RULE

Never place generated MP3/M4A into `D:\Workarea\StudyBook`.

Allowed in repo:
- audio script markdown
- html/component text files

Generated binary output location:
- `C:\temp\studybook_audio\<TOPIC_SLUG>\audio_clips\`
- `C:\temp\studybook_audio\<TOPIC_SLUG>\final_<TOPIC_SLUG>.mp3`

