# MISSION 16 — Update HTML: AWS Lambda
# Working directory: D:\StudyBook\
# Target: temp\seanlgirgis.github.io\learning\aws-lambda.html
# Prerequisite: user confirms Lambda audio uploaded and live

---

## REQUIRED CHANGES

1. Replace full `<div class="audio-box">...</div>` block:
   - audio src -> `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-lambda.mp3`
   - audio type -> `audio/mpeg`
   - keep existing video src unchanged
   - use entity-safe labels:
     - `&#127911; Audio Overview`
     - `&#127916; Video Overview (NotebookLM)`

2. Keep `.cheat-row` at standard:
   - `170px 1fr`

3. Update subtitle date only:
   - to `2026-04-24`
   - normalize separator entities to `&middot;`

4. Encoding safety:
   - no mojibake tokens (`�`, `Â`, `Ã`, `â`, `ï`, `ð`)
   - topnav back arrow must be `&larr;`
   - read-time range should use ASCII hyphen (`25-35`)

---

## VERIFY

```powershell
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-lambda.html" -Pattern 'final_aws-lambda.mp3'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-lambda.html" -Pattern 'audio/mpeg'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-lambda.html" -Pattern 'AWS_Lambda__Deep_Dive_small.mp4'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-lambda.html" -Pattern '\.m4a'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-lambda.html" -Pattern '170px'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-lambda.html" -Pattern 'Last updated 2026-04-24'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-lambda.html" -Pattern '&larr; Learning Hub'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-lambda.html" -Pattern '�|Â|Ã|â|ï|ð'
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

`MISSION 16 COMPLETE — aws-lambda.html updated — new audio src confirmed — video unchanged — encoding normalized`
