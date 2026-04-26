# MISSION 04 — Update HTML: Amazon EC2
# Working directory: D:\Workarea\StudyBook\
# Touches: ..\seanlgirgis.github.io\learning\aws-ec2.html (read then write)
# Prerequisite: Mission 03 complete AND Sean has confirmed R2 upload is live

---

## WORKING DIRECTORY REMINDER

```powershell
Get-Location   # must show D:\Workarea\StudyBook
```
All paths are relative to D:\Workarea\StudyBook\. Use no absolute paths.

---

## THREE REPOSITORIES INVOLVED IN THIS MISSION

```
D:\Workarea\StudyBook\                                       ← ROOT (working directory)
└── ..\seanlgirgis.github.io\                    ← REPO 3 — HTML update happens here
        learning\
            aws-ec2.html                            ← TARGET FILE

C:\temp\studybook_audio\aws-ec2\                    ← Audio artifacts (outside repo)
    UPLOAD_INSTRUCTIONS.md                          ← confirm R2 URL from here
    final_aws-ec2.mp3                               ← uploaded to R2 by Sean
```

---

## STOP — CONFIRM R2 UPLOAD BEFORE TOUCHING HTML

Read the upload instructions:
```
C:\temp\studybook_audio\aws-ec2\UPLOAD_INSTRUCTIONS.md
```

The expected R2 URL is:
`https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-ec2.mp3`

Do NOT proceed until Sean explicitly confirms: "EC2 audio uploaded — run Mission 04"
If not confirmed: STOP. Report "Waiting for R2 upload confirmation."

---

## STEP 1 — READ THE CURRENT HTML FILE

Read the full file:
```
..\seanlgirgis.github.io\learning\aws-ec2.html
```

Locate the `<div class="audio-box">` block.
Copy it verbatim here before making any changes — this is your rollback reference.

Note and record:
- The exact existing `<audio>` `src` URL
- The exact existing `<video>` `src` URL (this must NOT change)
- The exact subtitle text (you will update only the date)

---

## STEP 2 — REPLACE THE AUDIO-BOX

Replace the ENTIRE `<div class="audio-box">...</div>` block — opening div to closing div, inclusive.

New block:
```html
  <div class="audio-box">
    <div class="audio-label">&#127911; Audio Overview</div>
    <audio controls preload="metadata" style="width:100%;margin-top:6px;">
      <source src="https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-ec2.mp3" type="audio/mpeg">
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

What changes:
- `<audio>` src → new R2 URL for final_aws-ec2.mp3
- `<audio>` type → `audio/mpeg` (was `audio/mp4`)
- Added fallback text inside `<audio>` tag
- `audio-label` text → simplified with emoji
- `video-hint` text → clarified as NotebookLM

What does NOT change:
- `<video>` src URL — IDENTICAL to existing
- Everything else in the file

---

## STEP 3 — UPDATE THE SUBTITLE DATE

Find the `.subtitle` paragraph. It will look like:
```html
<p class="subtitle">Engineering reference &middot; Senior Data Engineer &middot; Last updated 2026-04-13 &middot; 25-35 min read</p>
```

Update only the date portion to today's date:
```html
<p class="subtitle">Engineering reference &middot; Senior Data Engineer &middot; Last updated 2026-04-24 &middot; 25-35 min read</p>
```

Change only the date. Do not alter the rest of the subtitle text.

---

## STEP 4 — VERIFY AND SAVE

After making changes, read the file again and confirm:

```powershell
# Quick structural checks
Select-String -Path "..\seanlgirgis.github.io\learning\aws-ec2.html" -Pattern 'audio-box' | Measure-Object
# Expected: Count = 1 (exactly one audio-box div — not two)

Select-String -Path "..\seanlgirgis.github.io\learning\aws-ec2.html" -Pattern 'final_aws-ec2.mp3'
# Expected: found — shows the new audio src

Select-String -Path "..\seanlgirgis.github.io\learning\aws-ec2.html" -Pattern 'audio/mpeg'
# Expected: found

Select-String -Path "..\seanlgirgis.github.io\learning\aws-ec2.html" -Pattern 'EC2.*Deep_Dive.*mp4'
# Expected: found — video URL is still present
```

Also confirm:
- `2026-04-24` appears in the subtitle
- Old `.m4a` URL from NotebookLM does NOT appear anywhere in the file
- No mojibake tokens appear (`�`, `Â`, `Ã`)

Encoding safety rule:
- Use HTML entities for non-ASCII display glyphs in page chrome text:
  - back arrow in topnav: `&larr;` (do not use literal arrow glyph)
  - separator dot: `&middot;`
  - up arrow: `&uarr;`
  - microseconds: `&micro;s`
  - headphone emoji: `&#127911;`
  - clapper-board emoji: `&#127916;`
- Use ASCII hyphen in read-time ranges (`25-35`), not Unicode dash glyphs.

---

## STEP 5 — REPORT CHANGES

Produce a clean diff summary:
```
CHANGES TO ..\seanlgirgis.github.io\learning\aws-ec2.html:

  audio-box:
    <audio> src:  [old .m4a URL]  →  https://...r2.dev/final_aws-ec2.mp3
    <audio> type: audio/mp4       →  audio/mpeg
    <video> src:  UNCHANGED ([existing URL])

  subtitle:
    date: 2026-04-13  →  2026-04-24

  All other content: UNCHANGED
```

---

## VERIFICATION CHECKLIST

- [ ] Working directory confirmed as D:\Workarea\StudyBook\ throughout
- [ ] R2 upload confirmed by Sean before any HTML changes
- [ ] Existing audio-box read and copied verbatim before replacement
- [ ] Existing video URL recorded before replacement
- [ ] New audio src = `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-ec2.mp3`
- [ ] Audio type = `audio/mpeg`
- [ ] Video src = UNCHANGED (exact original URL preserved)
- [ ] Subtitle date updated to 2026-04-24
- [ ] Old `.m4a` URL no longer present in file
- [ ] Exactly one `audio-box` div in the file
- [ ] Diff summary produced and reported

Report: "MISSION 04 COMPLETE — aws-ec2.html updated — new audio src confirmed — video unchanged"
Or:     "MISSION 04 BLOCKED — [reason]"

---

## AFTER THIS MISSION — TEST BEFORE CONTINUING

Before running Missions 05–07 (Athena), Sean should:
1. Open `..\seanlgirgis.github.io\learning\aws-ec2.html` in a browser
2. Confirm the audio player loads and plays (should hear HOST voice, on-topic EC2 content)
3. Confirm the video still plays (NotebookLM video)
4. If both pass: proceed to Mission 05

The remaining Phase 1 files follow the same 3-mission pattern (generate script → run pipeline → update HTML).
Mission files 05–25 will be created after this test case is verified.

