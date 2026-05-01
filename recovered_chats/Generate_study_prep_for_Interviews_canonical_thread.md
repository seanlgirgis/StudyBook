# Generate Study Prep for Interviews — Canonical Stand-In Thread

Purpose: operational stand-in for the recovered chat at `recovered_chats/Generate_study_prep_for_Interviews.md`, so future sessions can treat this file as the canonical thread reference.

## Canonical Source

- Full recovered transcript:
  - `recovered_chats/Generate_study_prep_for_Interviews.md`
- This stand-in is the quick-ops layer; transcript remains turn-level authority.

## Session Identity

- Original thread id: `019dc202-3f8c-77f3-a33b-4899c2f80a7c`
- Recovery date window in transcript: primarily `2026-04-24` to `2026-04-26`
- Runtime root for execution: `D:\Workarea\StudyBook`

## Objective Arc

This thread established and executed a repeatable "existing-work audio pipeline" workflow:

1. Audit existing learning pages and media wiring.
2. Generate or run audio pipelines for provided scripts.
3. Wire published MP3 URLs into learning pages.
4. Activate/patch component cards to clickable `Live` state.
5. Keep outputs out of repo (`C:\temp\studybook_audio`) and preserve repo cleanliness.

## Major Milestones (Chronological)

1. Environment + permission model aligned
- Startup protocol loaded from `AGENTS.md` chain.
- Effort-wide autonomy override was applied to:
  - `agents/shared/approval_matrix.md`
  - `agents/shared/command_allowlist.md`

2. Mission 01 completed (`01_AUDIT_EXISTING_PAGES.md`)
- Audited 8 target pages sequentially with user confirmation gates.
- Produced finalized audit report:
  - `prompts/codex_missions/AUDIT_REPORT.md`
- Findings pattern in thread:
  - Some pages live and clean.
  - Placeholder/none media states identified on specific pages.
  - Occasional text-encoding cleanup needed during audit extraction.

3. Mission 02 completed (`02_EC2_GENERATE_AUDIO_SCRIPT.md`)
- Generated EC2 script artifact:
  - `D:\Workarea\jobsearch\data\interview_prep\audio_prep\aws-ec2\audio_script_aws-ec2.md`

4. Mission 03 attempted then unblocked
- Initial blocker: environment/key loading + Python launcher path issues.
- Resolution path in session:
  - enforce `env_setter.ps1` usage,
  - rely on concrete interpreter path when alias fails,
  - continue with explicit preflight checks.

5. Runner-mode consolidation
- Workflow shifted to provided-files runner mode using master prompt:
  - `prompts/codex_missions/Usable prompts/Existing_work_pipeline_execution_provided_files_runner_mode_master.md`
- Pattern standardized: user runs generation commands, then shares R2 URL, then assistant performs site wiring edits.

6. Repeated content wiring completed for multiple topics
- Confirmed/updated page audio bindings and component-card live states for topics including:
  - `polars`
  - `docker-data-engineering`
  - `python-testing-pipelines`
  - `python-concurrency`
- Cards were patched to clickable `Open Reference` + `🎧 Live` (video `N/A` where appropriate).

7. Handoff prompt created for context-light continuation
- Thread ended with a reusable new-chat starter prompt to continue the exact runner workflow in fresh sessions.

## Canonical Operating Decisions Captured

1. Control and startup discipline
- Always load startup control files in AGENTS order before execution.

2. Environment bootstrap invariant
- Run from StudyBook root and load env first:
- `cd D:\Workarea\StudyBook`
- `./env_setter.ps1`

3. Audio output location invariant
- Generated audio artifacts must live under:
- `C:\temp\studybook_audio\<slug>\...`
- Do not place generated MP3/M4A/filelists inside tracked repo content trees.

4. Runner-mode division of labor
- User executes terminal generation pipeline.
- Assistant applies deterministic HTML/component wiring changes after published R2 URL is provided.

5. Live-card activation rule
- For completed topics: make card clickable, show `Open Reference`, set `🎧 Live`, keep `🎬 N/A` when no video exists.

## Reusable Command Pattern (Condensed)

1. Preflight
- `./env_setter.ps1`
- confirm API key is loaded
- verify script and HTML paths exist

2. Generate
- run `scripts/run_mission_audio.ps1 <script>` with chunk/timeout options

3. Verify artifact
- check final MP3 exists under `C:\temp\studybook_audio\<slug>\final_<slug>.mp3`
- check duration with `ffprobe`

4. Publish and wire
- upload MP3 to R2
- patch `learning/<slug>.html` with final URL + `audio/mpeg`
- patch proper `components/*.html` card(s) to clickable live state

5. Final verify
- grep/select-string for URL, `Open Reference`, and live badge text

## Canonical Path Map

- Root workspace:
  - `D:\Workarea\StudyBook`
- Audio script source root:
  - `D:\Workarea\jobsearch\data\interview_prep\audio_prep`
- Website repo root used in this thread:
  - `D:\Workarea\StudyBook\temp\seanlgirgis.github.io`
- Learning pages:
  - `...\learning\*.html`
- Section card components:
  - `...\components\*.html`
- Generated outputs (non-repo):
  - `C:\temp\studybook_audio`

## What Future Sessions Should Reuse

1. Treat this file as operational quick reference.
2. Use the master provided-files runner prompt for same-type tasks.
3. Keep output-location and live-card rules unchanged unless explicitly superseded.
4. Fall back to recovered transcript for any turn-level ambiguity.

## Notes on Scope

- This stand-in intentionally summarizes stable operating behavior, not every message.
- Authority order remains governed by `CONTROL_PROTOCOL.md`.
