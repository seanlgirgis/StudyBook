# MISSION 07 — Update HTML: Amazon Athena
# Working directory: D:\StudyBook\
# Touches: temp\seanlgirgis.github.io\learning\aws-athena.html (read then write)
# Prerequisite: Mission 06 complete AND Sean has confirmed R2 upload is live

---

## WORKING DIRECTORY REMINDER

```powershell
Get-Location   # must show D:\StudyBook
```
All paths are relative to D:\StudyBook\. Use no absolute paths.

---

## THREE REPOSITORIES INVOLVED IN THIS MISSION

```
D:\StudyBook\                                       ← ROOT (working directory)
└── temp\seanlgirgis.github.io\                    ← REPO 3 — HTML update happens here
        learning\
            aws-athena.html                         ← TARGET FILE

D:\temp\studybook_audio\aws-athena\                 ← Audio artifacts (outside repo)
    UPLOAD_INSTRUCTIONS.md                          ← confirm R2 URL from here
    final_aws-athena.mp3                            ← uploaded to R2 by Sean
```

---

## STOP — CONFIRM R2 UPLOAD BEFORE TOUCHING HTML

Read the upload instructions:
```
D:\temp\studybook_audio\aws-athena\UPLOAD_INSTRUCTIONS.md
```

The expected R2 URL is:
`https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-athena.mp3`

Do NOT proceed until Sean explicitly confirms: "Athena audio uploaded — run Mission 07"
If not confirmed: STOP. Report "Waiting for R2 upload confirmation."

---

## STEP 1 — READ THE CURRENT HTML FILE

Read the full file:
```
temp\seanlgirgis.github.io\learning\aws-athena.html
```

Locate and record the following before making any changes:

1. The `<div class="audio-box">` block — copy it verbatim (rollback reference)
2. The exact existing `<audio>` `src` URL (the old .m4a NotebookLM URL)
3. The exact existing `<video>` `src` URL — this must NOT change
4. The exact subtitle text
5. The current `.cheat-row` CSS column width (expected to be `160px 1fr` — audit confirmed)

---

## STEP 2 — REPLACE THE AUDIO-BOX

Replace the ENTIRE `<div class="audio-box">...</div>` block — opening div to closing div, inclusive.

New block:
```html
  <div class="audio-box">
    <div class="audio-label">&#127911; Audio Overview</div>
    <audio controls preload="metadata" style="width:100%;margin-top:6px;">
      <source src="https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-athena.mp3" type="audio/mpeg">
      Your browser does not support the audio element.
    </audio>
    <div class="video-hint" style="margin-top:10px;">&#127916; Video Overview (NotebookLM)</div>
    <video controls preload="metadata" style="width:100%;max-width:100%;border-radius:4px;margin-top:8px;">
      <source src="KEEP_EXISTING_VIDEO_URL" type="video/mp4">
    </video>
  </div>
```

CRITICAL: Replace `KEEP_EXISTING_VIDEO_URL` with the ACTUAL video URL you copied in Step 1.
Do not invent or guess the video URL. Use the exact URL from the existing file.

The existing video URL (from audit) is:
`https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/Amazon_Athena__Deep_Dive_small.mp4`

What changes:
- `<audio>` src → new R2 URL for final_aws-athena.mp3
- `<audio>` type → `audio/mpeg` (was `audio/mp4`)
- Added fallback text inside `<audio>` tag
- `audio-label` text → simplified with emoji entity
- `video-hint` text → clarified as NotebookLM

What does NOT change:
- `<video>` src URL — IDENTICAL to existing
- Everything else in the file

---

## STEP 3 — FIX THE CHEAT-ROW CSS

**This is an extra fix bundled into this mission. Do NOT skip it.**

The audit found that `aws-athena.html` has `.cheat-row` set to `160px 1fr` instead of the standard `170px 1fr`.

Find the CSS rule. It will look like one of these forms:
```css
.cheat-row { grid-template-columns: 160px 1fr; }
```
or
```css
.cheat-row{grid-template-columns:160px 1fr}
```

Replace the column width value only:
- Change: `160px`
- To:     `170px`

Do not touch any other part of the `.cheat-row` rule or any surrounding CSS.

After the change, verify the fix:
```powershell
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-athena.html" -Pattern '160px'
# Expected: NO matches — 160px must not appear anywhere
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-athena.html" -Pattern '170px'
# Expected: found — the corrected cheat-row value
```

---

## STEP 4 — UPDATE THE SUBTITLE DATE

Find the `.subtitle` paragraph. It will look similar to:
```html
<p class="subtitle">Engineering reference &nbsp;&middot;&nbsp; Senior Data Engineer &nbsp;&middot;&nbsp; Last updated April 2026 &nbsp;&middot;&nbsp; 25–35 min read</p>
```

Update only the date portion to today's date:
```html
<p class="subtitle">Engineering reference &nbsp;&middot;&nbsp; Senior Data Engineer &nbsp;&middot;&nbsp; Last updated 2026-04-24 &nbsp;&middot;&nbsp; 25–35 min read</p>
```

Change only the date text. Do not alter any other part of the subtitle — preserve all `&nbsp;` and `&middot;` entities exactly.

---

## STEP 5 — VERIFY AND SAVE

After making all changes, run these structural checks:

```powershell
# Exactly one audio-box
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-athena.html" -Pattern 'audio-box' | Measure-Object
# Expected: Count = 1

# New audio src present
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-athena.html" -Pattern 'final_aws-athena.mp3'
# Expected: found

# Audio type correct
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-athena.html" -Pattern 'audio/mpeg'
# Expected: found

# Video URL still present (Athena Deep Dive)
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-athena.html" -Pattern 'Amazon_Athena__Deep_Dive_small.mp4'
# Expected: found

# Old .m4a URL gone
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-athena.html" -Pattern '\.m4a'
# Expected: NO matches

# cheat-row fix confirmed
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-athena.html" -Pattern '160px'
# Expected: NO matches

Select-String -Path "temp\seanlgirgis.github.io\learning\aws-athena.html" -Pattern '170px'
# Expected: found
```

Also confirm:
- `2026-04-24` appears in the subtitle
- No mojibake tokens appear (`â`, `Ã`, `ï`, `Â`, `ð`)
- `&middot;`, `&nbsp;`, `&#127911;`, `&#127916;` are used for all non-ASCII UI glyphs

Encoding safety rule:
- Save as UTF-8
- Use HTML entities for non-ASCII display glyphs in page chrome text:
  - back arrow in topnav: `&larr;` (do not use literal arrow glyph)
  - separator dot: `&middot;`
  - non-breaking space: `&nbsp;`
  - headphone emoji: `&#127911;`
  - clapper-board emoji: `&#127916;`
- Use ASCII hyphen in read-time ranges (`25-35`) unless existing file intentionally uses a different style.

---

## STEP 6 — REPORT CHANGES

Produce a clean diff summary:
```
CHANGES TO temp\seanlgirgis.github.io\learning\aws-athena.html:

  audio-box:
    <audio> src:  [old .m4a URL]  →  https://...r2.dev/final_aws-athena.mp3
    <audio> type: audio/mp4       →  audio/mpeg
    <video> src:  UNCHANGED (https://...r2.dev/Amazon_Athena__Deep_Dive_small.mp4)

  cheat-row:
    grid-template-columns: 160px 1fr  →  170px 1fr

  subtitle:
    date: April 2026  →  2026-04-24

  All other content: UNCHANGED
```

---

## VERIFICATION CHECKLIST

- [ ] Working directory confirmed as D:\StudyBook\ throughout
- [ ] R2 upload confirmed by Sean before any HTML changes
- [ ] Existing audio-box read and copied verbatim before replacement
- [ ] Existing video URL recorded before replacement
- [ ] New audio src = `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-athena.mp3`
- [ ] Audio type = `audio/mpeg`
- [ ] Video src = UNCHANGED (Amazon_Athena__Deep_Dive_small.mp4)
- [ ] cheat-row changed from `160px 1fr` to `170px 1fr`
- [ ] `160px` does NOT appear anywhere in the file
- [ ] Subtitle date updated to 2026-04-24
- [ ] Old `.m4a` URL no longer present in file
- [ ] Exactly one `audio-box` div in the file
- [ ] No mojibake tokens (`â`, `Ã`, `ï`, `Â`, `ð`)
- [ ] Diff summary produced and reported

Report: "MISSION 07 COMPLETE — aws-athena.html updated — new audio src confirmed — cheat-row fixed — video unchanged"
Or:     "MISSION 07 BLOCKED — [reason]"

---

## AFTER THIS MISSION — TEST BEFORE CONTINUING

Before running Missions 08–10 (Glue), Sean should:
1. Open `temp\seanlgirgis.github.io\learning\aws-athena.html` in a browser
2. Confirm the audio player loads and plays (should hear HOST voice, on-topic Athena content)
3. Confirm the video still plays (NotebookLM video)
4. Confirm the cheat sheet layout looks correct (label column wider — 170px)
5. If all pass: proceed to Mission 08

The next topic is AWS Glue — missions 08 (script), 09 (pipeline), 10 (HTML + cheat-row fix 150→170px).
