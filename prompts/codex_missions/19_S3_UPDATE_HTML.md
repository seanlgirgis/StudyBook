# MISSION 19 — Update HTML: Amazon S3
# Working directory: D:\Workarea\StudyBook\
# Target: ..\seanlgirgis.github.io\learning\aws-s3.html
# Prerequisite: user confirms S3 audio uploaded and live

---

## REQUIRED CHANGES

1. Replace full `<div class="audio-box">...</div>` block:
   - audio src -> `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-s3.mp3`
   - audio type -> `audio/mpeg`
   - keep existing video src unchanged
   - labels must be entity-safe:
     - `&#127911; Audio Overview`
     - `&#127916; Video Overview (NotebookLM)`

2. Fix cheat-row width to standard:
   - `.cheat-row` `150px 1fr` -> `170px 1fr`

3. Update subtitle date only:
   - to `2026-04-24`
   - normalize separators to `&middot;`

4. Encoding safety normalization:
   - topnav back arrow `&larr;`
   - avoid literal emoji/glyphs in chrome text
   - read-time range ASCII hyphen (`30-40`)
   - no mojibake tokens (`�`, `Â`, `Ã`, `â`, `ï`, `ð`)

---

## VERIFY

```powershell
Select-String -Path "..\seanlgirgis.github.io\learning\aws-s3.html" -Pattern 'final_aws-s3.mp3'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-s3.html" -Pattern 'audio/mpeg'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-s3.html" -Pattern 'S3__Engine_of_Big_Data_small.mp4'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-s3.html" -Pattern '\.m4a'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-s3.html" -Pattern '150px'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-s3.html" -Pattern '170px'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-s3.html" -Pattern 'Last updated 2026-04-24'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-s3.html" -Pattern '&larr; Learning Hub'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-s3.html" -Pattern '�|Â|Ã|â|ï|ð'
```

Expected:
- new MP3/audio/mpeg present
- video URL preserved
- `.m4a` absent
- `150px` absent, `170px` present
- new date present
- topnav uses `&larr;`
- no corruption tokens

---

## REPORT

`MISSION 19 COMPLETE — aws-s3.html updated — new audio src confirmed — cheat-row fixed — video unchanged — encoding normalized`

