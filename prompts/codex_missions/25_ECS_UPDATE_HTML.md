# MISSION 25 — Update HTML: Amazon ECS
# Working directory: D:\Workarea\StudyBook\
# Target: ..\seanlgirgis.github.io\learning\aws-ecs.html
# Prerequisite: user confirms ECS audio uploaded and live

---

## REQUIRED CHANGES

1. Replace full `<div class="audio-box">...</div>` block:
   - audio src -> `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-ecs.mp3`
   - audio type -> `audio/mpeg`
   - preserve page's current video status (no embedded video source exists currently)
   - use entity-safe labels:
     - `&#127911; Audio Overview`
     - `&#127916; Video Overview (coming soon)`

2. Keep `.cheat-row` at standard:
   - `170px 1fr`

3. Update subtitle date only:
   - to `2026-04-24`
   - normalize separators to `&middot;`

4. Encoding safety:
   - topnav back arrow must be `&larr;`
   - no mojibake tokens (`�`, `Â`, `Ã`, `â`, `ï`, `ð`)
   - read-time range should use ASCII hyphen (`25-35`)

---

## VERIFY

```powershell
Select-String -Path "..\seanlgirgis.github.io\learning\aws-ecs.html" -Pattern 'final_aws-ecs.mp3'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-ecs.html" -Pattern 'audio/mpeg'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-ecs.html" -Pattern '\.m4a'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-ecs.html" -Pattern '170px'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-ecs.html" -Pattern 'Last updated 2026-04-24'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-ecs.html" -Pattern '&larr; Learning Hub'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-ecs.html" -Pattern '&#127916; Video Overview \(coming soon\)'
Select-String -Path "..\seanlgirgis.github.io\learning\aws-ecs.html" -Pattern '�|Â|Ã|â|ï|ð'
```

Expected:
- new MP3/audio/mpeg present
- old `.m4a` absent
- `170px` present
- new date present
- topnav uses `&larr;`
- no corruption tokens

---

## REPORT

`MISSION 25 COMPLETE — aws-ecs.html updated — new audio src confirmed — video placeholder preserved — encoding normalized`

