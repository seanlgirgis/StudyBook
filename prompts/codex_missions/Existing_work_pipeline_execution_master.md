# PIPELINE EXECUTION MASTER — Audio + HTML Replacement
# Working directory: D:\StudyBook\
# Purpose: Reusable runbook for every learning topic (Athena, Glue, Redshift, etc.)

---

## INPUTS REQUIRED PER TOPIC

- `topic_slug` (example: `aws-athena`)
- `html_file` (example: `temp\seanlgirgis.github.io\learning\aws-athena.html`)
- mission triplet:
  - script mission (generate dialogue)
  - pipeline mission (run audio generation + stitch)
  - html mission (patch audio src and any CSS fix)

---

## CANONICAL EXECUTION ORDER (DO NOT SKIP)

1. Load context:
   - `prompts\codex_missions\00_CODEX_CONTEXT.md`
2. Run script generation mission (example: `05_...GENERATE_AUDIO_SCRIPT.md`)
3. Run pipeline mission (example: `06_...RUN_AUDIO_PIPELINE.md`)
4. Human upload to R2 and live URL validation
5. Run HTML update mission (example: `07_...UPDATE_HTML.md`)
6. Browser validation of page audio + video

---

## OUTPUT LOCATION STANDARD

- Keep source script in repo:
  - `temp\jobsearch\data\interview_prep\audio_prep\{topic_slug}\audio_script_{topic_slug}.md`
- Keep generated clips/final outside repo:
  - `C:\temp\studybook_audio\{topic_slug}\audio_clips\`
  - `C:\temp\studybook_audio\{topic_slug}\final_{topic_slug}.mp3`
  - `C:\temp\studybook_audio\{topic_slug}\UPLOAD_INSTRUCTIONS.md`

---

## AUDIO RUNNER STANDARD (FAIL-FAST)

```powershell
cd D:\StudyBook
.\scripts\run_mission_audio.ps1 "temp\jobsearch\data\interview_prep\audio_prep\{topic_slug}\audio_script_{topic_slug}.md" -ChunkSize 750 -RequestTimeoutSeconds 120
```

Expected:
- non-zero exit on generation/stitch failure
- sentence-boundary chunking
- no mid-sentence or cross-speaker cuts

---

## R2 HANDOFF CHECKPOINT (HUMAN)

Before HTML patch mission:
- Upload `C:\temp\studybook_audio\{topic_slug}\final_{topic_slug}.mp3` to R2
- Confirm URL plays in browser:
  - `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_{topic_slug}.mp3`
- Then tell Codex:
  - `"{TOPIC} audio uploaded — run Mission XX"`

---

## HTML ENCODING SAFETY STANDARD

When patching HTML:
- Save as UTF-8.
- Use entities for UI glyphs to avoid mojibake:
  - topnav back arrow: `&larr;` (never literal arrow glyph)
  - `&middot;`, `&uarr;`, `&micro;`, `&#127911;`, `&#127916;`
- Prefer ASCII hyphen for chrome text where possible (`25-35`, not en dash variants).
- Verify corruption tokens are absent:
  - `�`, `Â`, `Ã`

---

## FINAL VALIDATION CHECKLIST (PER TOPIC)

- [ ] Script mission completed
- [ ] Pipeline mission completed
- [ ] final MP3 exists in `C:\temp\studybook_audio\{topic_slug}\`
- [ ] Duration in expected range for topic
- [ ] R2 URL confirmed live
- [ ] HTML page updated to new `final_{topic_slug}.mp3`
- [ ] Existing video URL preserved (if applicable)
- [ ] Any audit-required CSS fix applied
- [ ] No mojibake in final HTML

---

## OPERATOR MODE

For every new topic, follow this exact loop:
1. Confirm mission files exist.
2. Execute mission 1.
3. Execute mission 2.
4. Pause for your R2 upload confirmation.
5. Execute mission 3.
6. Report completion and wait for next topic.
