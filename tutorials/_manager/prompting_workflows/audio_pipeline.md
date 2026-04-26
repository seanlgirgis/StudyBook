# Prompting Workflow — Audio Script → MP3
# Last updated: 2026-04-25

---

## Overview

Gap prompt file → ChatGPT Project 1 → audio script → run_mission_audio.ps1 → R2 upload → HTML wired

---

## Step 1 — Write the Gap Prompt (if not done)

Gap files live in: `D:\StudyBook\temp\gap\NN_topic_prompts.md`
Format: Project 1 section uses `- ` bullet list with rich detail + SCOPE FENCE bullets.
Reference any completed file (e.g., 04_aws_kinesis_prompts.md) for format.

---

## Step 2 — Generate Audio Script in ChatGPT Project 1

**Project:** "Project 1 — Audio Script Writer"
**Prompt file:** `D:\users\shareuser\Downloads\Project-1-Audioscript-Maker.txt`

1. Open ChatGPT → switch to Project 1
2. Start a new conversation
3. Paste the **Project 1 section** from the gap file (everything between === markers)
4. ChatGPT returns: title, 3 learning objectives, full HOST/SEAN script in chunks
5. Review each chunk — HOST should vary reactions, SEAN should be concise (3-5 sentences)
6. If chunks feel long → ask "shorten SEAN's answers to 3 sentences each"
7. If HOST feels passive → ask "make HOST push back more, ask for specific numbers"

**Quality checks before accepting:**
- No rotating bridge phrases ("So…", "Here's the key insight…", "At a high level…")
- SEAN answers are 3-5 sentences, not paragraphs
- Rapid-fire section has 8-10 tight Q&A pairs
- Script reads naturally when spoken aloud

---

## Step 3 — Save Script to Codex Mission Prompt

Save the generated script into the appropriate codex_missions file.
Pattern: `D:\StudyBook\prompts\codex_missions\NN_topic_RUN_AUDIO_PIPELINE.md`

If that file doesn't exist yet, create it following the pattern of an existing one.

---

## Step 4 — Run Audio Pipeline

```powershell
cd D:\StudyBook
.\scripts\run_mission_audio.ps1 -Slug {slug} -ChunkSize 750
```

Where `{slug}` matches the HTML file name (e.g., `aws-kinesis`).

The script:
1. Splits script into ~750-char chunks
2. Calls TTS API per chunk
3. Concatenates → `D:\temp\studybook_audio\{slug}\final_{slug}.mp3`

---

## Step 5 — Upload MP3 to R2 CDN

1. Open Cloudflare R2 dashboard
2. Navigate to bucket: `pub-174bd65326be4562b4618ccf6a4a8864`
3. Upload: `final_{slug}.mp3`
4. Verify public URL: `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_{slug}.mp3`

---

## Step 6 — Wire Audio into HTML Page

Open: `D:\StudyBook\temp\seanlgirgis.github.io\learning\{slug}.html`

Find the audio section and update the `src`:
```html
<audio controls>
  <source src="https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_{slug}.mp3" type="audio/mpeg">
</audio>
```

---

## Step 7 — Commit and Push

```powershell
cd D:\StudyBook\temp\seanlgirgis.github.io
git add learning/{slug}.html
git commit -m "Wire {slug} audio"
git push
```

---

## Step 8 — Sync to Phone

```powershell
cd D:\StudyBook
.\scripts\sync_studybook_to_phone.ps1
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Script sounds robotic/formulaic | Ask ChatGPT to rewrite with more natural HOST curiosity |
| SEAN answers too long | Ask "limit SEAN to 3 sentences per turn" |
| Rotating bridge phrases appearing | Remind ChatGPT: "No 'So', 'Here's the key insight', etc." |
| Audio pipeline fails mid-chunk | Check chunk size — try -ChunkSize 600 |
| R2 upload fails | Check Cloudflare dashboard permissions, re-upload manually |
