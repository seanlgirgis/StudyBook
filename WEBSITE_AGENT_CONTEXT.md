# Website Maintenance Agent Context

Use this file when the user says the focus is `WebsiteMaintenance` or `Website`.

## Context Key

- Key: `WebsiteMaintenance`
- Repository: `temp/seanlgirgis.github.io`
- Primary Goal: maintain learning pages (clean special characters, update audio/video media, and keep media naming/bucket rules consistent).

## Startup Rules for Website Work

1. Enter repo:
   - `cd temp/seanlgirgis.github.io`

2. Initialize Python environment (when needed for scripts):
   - `..\..\env_setter.ps1 -NonInteractive`
   - If interactive session is required: `..\..\env_setter.ps1`

3. Use relative paths only:
   - Correct: `learning/aws-ec2.html`
   - Avoid absolute paths unless user explicitly asks.

4. Encoding safety (Windows shell):
   - Before any script or bulk replacement:
     - `$env:PYTHONIOENCODING='utf-8'`

## Cloudflare Media Bucket

- Base URL: `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/`
- All audio and video sources should reference this base.

## Media File Naming Rules

1. Audio (m4a):
   - Pattern: `<Descriptive_Title_With_Underscores>_small.m4a`
   - Example: `Senior_Engineering_Rules_for_Amazon_EC2_small.m4a`
   - Use title-case words separated by underscores.

2. Video (mp4):
   - Pattern: `<ServiceName>__Deep_Dive_small.mp4`
   - Example: `EC2__Engineering_Deep_Dive_small.mp4`
   - Use a double underscore between service name and the rest of the title.

## Standard Media Block Snippet

Use this exact block inside the `.audio-box` section of learning pages:

```
<div class="audio-box">
  <div class="audio-label">AI-Generated Audio Overview</div>
  <audio controls preload="metadata" style="width:100%;margin-top:6px;">
    <source src="https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/<AUDIO_FILE>" type="audio/mp4">
  </audio>
  <div class="video-hint" style="margin-top:10px;">AI-Generated Video Overview</div>
  <video controls preload="metadata" style="width:100%;max-width:100%;border-radius:4px;margin-top:8px;">
    <source src="https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/<VIDEO_FILE>" type="video/mp4">
  </video>
</div>
```

## Special Character Cleanup

If headings or section titles show garbled characters (for example replacement symbols), normalize them:

- Preferred: replace em/en dashes with ASCII hyphens (`-`).
- Avoid non-ASCII punctuation to reduce rendering issues across systems.

## Update Workflow (Single Page)

1. Open the target file under `learning/`.
2. Replace the `.audio-box` contents with the standard media block.
3. Update `<AUDIO_FILE>` and `<VIDEO_FILE>` using the naming rules above.
4. Scan the page for garbled punctuation and normalize to ASCII hyphens.
5. Save the file and report the updated paths.
