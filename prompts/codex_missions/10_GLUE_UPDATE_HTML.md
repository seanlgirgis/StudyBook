# MISSION 10 — Update HTML: AWS Glue
# Working directory: D:\StudyBook\
# Target: temp\seanlgirgis.github.io\learning\aws-glue.html
# Prerequisite: user confirms Glue audio uploaded and live

---

## REQUIRED CHANGES

1. Replace full `<div class="audio-box">...</div>` block:
   - audio src → `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-glue.mp3`
   - audio type → `audio/mpeg`
   - keep existing video src unchanged
   - use entity-safe labels:
     - `&#127911; Audio Overview`
     - `&#127916; Video Overview (NotebookLM)`

2. Fix CSS deviation:
   - `.cheat-row` width `150px 1fr` → `170px 1fr`

3. Update subtitle date only:
   - to `2026-04-24`
   - preserve entity separators (`&nbsp;&middot;&nbsp;`) if present

4. Encoding safety:
   - no mojibake tokens (`�`, `Â`, `Ã`, `â`, `ï`, `ð`)
   - use entities for non-ASCII UI glyphs
   - topnav back arrow must be `&larr;` (not literal arrow glyph)
   - subtitle separator must use `&middot;`
   - read-time range should use ASCII hyphen (`25-35`)

---

## VERIFY

```powershell
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-glue.html" -Pattern 'final_aws-glue.mp3'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-glue.html" -Pattern 'audio/mpeg'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-glue.html" -Pattern 'AWS_Glue__The_Deep_Dive_small.mp4'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-glue.html" -Pattern '\.m4a'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-glue.html" -Pattern '150px'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-glue.html" -Pattern '170px'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-glue.html" -Pattern 'Last updated 2026-04-24'
```

Expected:
- new MP3/audio/mpeg present
- video URL preserved
- `.m4a` absent
- `150px` absent
- `170px` present
- new date present

---

## REPORT

`MISSION 10 COMPLETE — aws-glue.html updated — new audio src confirmed — cheat-row fixed — video unchanged`
