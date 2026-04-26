# MISSION 13 — Update HTML: Amazon Redshift
# Working directory: D:\Workarea\StudyBook\
# Target: ..\seanlgirgis.github.io\learning\aws-redshift.html
# Prerequisite: user confirms Redshift audio uploaded and live

---

## REQUIRED CHANGES

1. Replace full `<div class="audio-box">...</div>` block:
   - audio src -> `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-redshift.mp3`
   - audio type -> `audio/mpeg`
   - keep existing video src unchanged
   - use entity-safe labels:
     - `&#127911; Audio Overview`
     - `&#127916; Video Overview (NotebookLM)`

2. Keep `.cheat-row` width at standard:
   - `170px 1fr`

3. Update subtitle date only:
   - to `2026-04-24`
   - preserve entity separators (`&middot;`) once normalized

4. Encoding safety:
   - no mojibake tokens (`�`, `Â`, `Ã`, `â`, `ï`, `ð`)
   - topnav back arrow must be `&larr;` (not literal arrow glyph)
   - subtitle separator must use `&middot;`
   - read-time range should use ASCII hyphen (`25-35`)

---

## VERIFY

```powershell
Select-String -Path "..\seanlgirgis.github.io\learning\aws-redshift.html" -Pattern 'final_aws-redshift.mp3'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-redshift.html" -Pattern 'audio/mpeg'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-redshift.html" -Pattern 'AWS_Redshift__Deep_Dive_small.mp4'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-redshift.html" -Pattern '\.m4a'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-redshift.html" -Pattern '170px'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-redshift.html" -Pattern 'Last updated 2026-04-24'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-redshift.html" -Pattern '&larr; Learning Hub'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-redshift.html" -Pattern '�|Â|Ã|â|ï|ð'
```

Expected:
- new MP3/audio/mpeg present
- video URL preserved
- `.m4a` absent
- `170px` present
- new date present
- topnav uses `&larr;`
- no corruption tokens

---

## REPORT

`MISSION 13 COMPLETE — aws-redshift.html updated — new audio src confirmed — video unchanged — encoding normalized`

