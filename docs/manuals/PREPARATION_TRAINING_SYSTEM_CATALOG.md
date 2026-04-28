# Preparation & Training System Catalog

Last updated: 2026-04-28

This catalog maps the full preparation/training ecosystem across StudyBook, website, audio pipeline, and jobsearch script assets.

## 1) Core Surfaces

These are the main surfaces you actively use for prep/training content creation and delivery.

1. Tutorials workspace
- Absolute: `D:\Workarea\StudyBook\tutorials`
- Relative from StudyBook root: `./tutorials`
- Purpose: Tutorial/topic workspaces, manager workflows, tutorial pipeline, per-topic folders.

2. Published learning pages (website)
- Absolute: `D:\Workarea\seanlgirgis.github.io\learning`
- Relative from StudyBook root: `../seanlgirgis.github.io/learning`
- Purpose: Public technical reference pages consumed on website.

3. Project pages (website)
- Absolute: `D:\Workarea\seanlgirgis.github.io\projects`
- Relative from StudyBook root: `../seanlgirgis.github.io/projects`
- Purpose: Project case studies and portfolio storytelling.

4. Audio output library (binary)
- Absolute: `D:\temp\studybook_audio`
- Relative from StudyBook root: `../../temp/studybook_audio`
- Purpose: Final MP3s, per-topic clip folders, playlist `.m3u` files for phone + listening.

5. Audio script source repo (text)
- Absolute: `D:\Workarea\jobsearch\data\interview_prep\audio_prep`
- Relative from StudyBook root: `../jobsearch/data/interview_prep/audio_prep`
- Purpose: Script markdown source (`audio_script_{slug}.md`) used to generate audio.

6. Playground
- Absolute: `D:\Workarea\StudyBook\playground`
- Relative from StudyBook root: `./playground`
- Purpose: Practice notebooks, coding drills, study experiments.

## 2) Control Plane (How the system runs)

1. Mission prompts and orchestration
- Path: `./prompts/codex_missions`
- Includes Project 1/2 prompt packs and runbooks.

2. Scripts
- Path: `./scripts`
- Key scripts:
  - `./scripts/run_mission_audio.ps1`
  - `./scripts/sync_studybook_to_phone.ps1`

3. Website wiring layer
- Path: `../seanlgirgis.github.io/components`
- Purpose: Category cards/nav discoverability for `learning/*.html` pages.

4. Persisted manuals (SOPs)
- Path: `./docs/manuals`
- Key files:
  - `INTERVIEW_AUDIO_HTML_MASTER_GUIDE.md`
  - `WEBSITE_REMAINING_WORK_TRACKER.md`
  - `AUDIO_PLAYLIST_SYNC_METHOD.md`

## 3) Audio System Notes

1. Binary audio root standard
- `D:\temp\studybook_audio` (outside repos)

2. Playlist location standard
- Playlists are flat files at root of `D:\temp\studybook_audio` (not a `playlists/` subfolder).

3. Phone sync destination
- `C:\Users\shareuser\CrossDevice\Pixel 8 Pro\storage\Music\StudyBook`

4. Sync command
```powershell
cd D:\Workarea\StudyBook
.\scripts\sync_studybook_to_phone.ps1
```

## 4) Hidden Generic Interview Page (Confirmed)

A hidden/generic interview page exists at:
- `D:\Workarea\seanlgirgis.github.io\interview-master.html`
- Relative from StudyBook root: `../seanlgirgis.github.io/interview-master.html`

Related training assets also exist:
- Script/source folder: `../jobsearch/data/interview_prep/audio_prep/interview-master`
- Audio output folder: `../../temp/studybook_audio/interview-master`

Current catalog note:
- This page is not part of normal Learning Hub category-card routing in `components/learning-*.html`.
- Treat it as a special/standalone training page unless you intentionally wire it into site navigation.

## 5) Content Lifecycle Summary

1. Draft and refine topic in tutorials/prompts.
2. Generate audio script (`audio_prep` text source in jobsearch repo).
3. Run audio pipeline to create final MP3 (`D:\temp\studybook_audio`).
4. Upload MP3 to R2.
5. Generate HTML page and save to website `learning/`.
6. Wire category card in website `components/`.
7. Update tracker/manuals.
8. Update playlists (if needed) and sync phone.

## 6) Current State Snapshot (High level)

- Tutorials: active multi-topic workspace (`tutorials` with many numbered topic folders).
- Website learning pages: active and expanding (`learning/`).
- Website project pages: active (`projects/`).
- Audio library: active with topic folders and playlists in `D:\temp\studybook_audio`.
- Script sources: active in `jobsearch/data/interview_prep/audio_prep`.
- Practice notebooks: active in `playground`.

## 7) Maintenance Rule

When adding a new topic, update all relevant layers:
1. `audio_prep/{slug}` script source
2. `D:\temp\studybook_audio/{slug}` final audio
3. `learning/{slug}.html`
4. category card in `components/learning-*.html`
5. `WEBSITE_REMAINING_WORK_TRACKER.md`
6. playlist files (if topic should be on phone study rotation)
