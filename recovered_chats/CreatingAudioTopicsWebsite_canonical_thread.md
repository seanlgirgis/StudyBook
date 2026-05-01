# CreatingAudioTopicsWebsite - Canonical Stand-In Thread

Purpose: readable operational stand-in for the original chat so future runs in `D:\Workarea\StudyBook` can treat this as the canonical thread.

Source transcript: [CreatingAudioTopicsWebsite.md](D:/Workarea/StudyBook/recovered_chats/CreatingAudioTopicsWebsite.md)

## Scope and Intent

This thread ran the "provided-files runner mode" pipeline for StudyBook website topics:
- generate topic audio from a provided script,
- keep generated media outside repo (`C:\temp\studybook_audio\` or `D:\temp\studybook_audio\`),
- after R2 upload, wire only website links/cards/status,
- keep cards clickable with `Open Reference`, `🎧 Live`, and `🎬 N/A`.

## Core Operating Rules Captured

- Startup protocol must read control files in required order from `AGENTS.md`.
- `env_setter.ps1` is run before pipeline commands.
- Audio generation output must never be written inside repo paths.
- User runs terminal commands; assistant provides numbered one-command blocks.
- Wiring phase starts only after user confirms upload URL.
- Card policy: clickable card + `Open Reference` + `🎧 Live` + `🎬 N/A` (unless a video exists).
- Assistant must report exact section, component file, page path, and verification lines.

## Stable Command Pattern (Reusable)

1. `cd D:\Workarea\StudyBook; .\env_setter.ps1`
2. Set vars (`$HTML_FILE`, `$AUDIO_SCRIPT_FILE`, `$TOPIC_SLUG`, `$PAGE_FILE`)
3. Preflight: `Test-Path` for HTML + script
4. Run audio: `./scripts/run_mission_audio.ps1 ... -TempRoot <temp-root>`
5. Verify MP3 exists and metadata
6. Verify duration via `ffprobe`
7. Guard repo cleanliness for generated audio artifacts
8. Verify HTML `audio/mpeg` source line
9. Detect component candidates (`components/*.html`)
10. Inspect wiring status lines (`Open Reference`, `Live`, `Planned`, etc.)

## Timeline Summary

- 2026-04-26: Runner-mode protocol established and repeatedly executed for topic batches.
- 2026-04-26 to 2026-04-29: Multiple topic pages/cards wired after upload confirmations.
- 2026-04-29: Naming conflict surfaced for `learning-design`; normalized toward `system-design` naming.
- 2026-04-29: Legacy routing cleaned so `learning/learning-design.html` redirects to `learning/system-design.html`.
- 2026-04-29: `system-design.html` audio URL corrected to `final_system-design-for-data-engineers.mp3`.

## Key Decisions and Outcomes

- Adopted strict two-phase flow: run/verify audio first, wire site second.
- Standardized status language for cards (`Live` vs `Upload pending` vs planned).
- Treated naming clarity as UX-critical; moved from ambiguous `learning-design` label to explicit `system-design` topic naming.
- Preserved backward compatibility with redirect for old slug.

## Canonical Paths and Artifacts

- Repo root: `D:\Workarea\StudyBook`
- Website working repo path (during thread): `D:\Workarea\StudyBook\temp\seanlgirgis.github.io`
- Audio script source root: `D:\Workarea\jobsearch\data\interview_prep\audio_prep`
- Audio output root: `C:\temp\studybook_audio\` (and later `D:\temp\studybook_audio\` for specific run)
- R2 public pattern: `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_<slug>.mp3`

## Final Mapping Clarifications Captured

- `components/learning-nav.html` is hub navigation (layer cards), not a topic section page.
- `components/learning-design.html` is the system-design section component.
- `components/learning-data-architecture.html` is data-architecture section component.
- `learning/system-design.html` is the cleaned primary topic page replacing ambiguous `learning-design` naming.

## Known Pain Points Logged

- Topic/card naming drift caused user confusion when card titles/URLs did not match section semantics.
- 404 and stale-page confusion occurred when card state changed before page availability or before cache/Pages refresh.
- Consistent verification output lines reduced ambiguity and should be preserved in future runs.

## Reuse Guidance for Future Runs

- Always request/confirm exact R2 URL before wiring.
- Treat slug/name consistency as a hard gate before card updates.
- If renaming a topic slug, update page links, component links, and redirects in one pass.
- Report where the user can find the card in site hierarchy (hub -> section -> card -> page URL).

## Transcript Authority

For full turn-by-turn detail, commands, and exact user/assistant wording, use:
- [CreatingAudioTopicsWebsite.md](D:/Workarea/StudyBook/recovered_chats/CreatingAudioTopicsWebsite.md)
