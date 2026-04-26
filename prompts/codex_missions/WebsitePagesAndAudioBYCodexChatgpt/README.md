# Website Pages + Audio Prompt Pack

This folder contains the prompt/runbook system for generating:
- interview-style audio scripts,
- learning HTML pages,
- audio pipeline execution + website wiring.

Owner workflow target: `D:\Workarea\StudyBook`

## Files In This Folder

### 1) `Project-1-Audioscript-Maker.txt`
Use this as the **system instruction** for ChatGPT Project 1.

Purpose:
- Generate full HOST/SEAN dialogue script markdown files.
- Enforce voice labels, pacing rules, phonetic normalization, and output format.

Output expected:
- `audio_script_{slug}.md`
- Save under:
  `..\jobsearch\data\interview_prep\audio_prep\{slug}\audio_script_{slug}.md`

Use when:
- You need a new script for a new topic (before running audio generation).

---

### 2) `Project2_HTMl_Maker.txt`
Use this as the **system instruction** for ChatGPT Project 2.

Purpose:
- Generate full, self-contained HTML learning pages with the site CSS contract.
- Include audio player source, sections, Q&A, and quick reference block.

Output expected:
- `{slug}.html`
- Save under:
  `..\seanlgirgis.github.io\learning\{slug}.html`

Use when:
- You need a brand-new learning page or complete page replacement.

---

### 2b) `Project2_ShortPrompt_Template.md`
Use this as the **short per-topic prompt** when reusable rules are persisted in:
- `..\..\..\seanlgirgis.github.io\AGENTS.md`
- `..\..\..\seanlgirgis.github.io\learning\_page-template.html`

Purpose:
- Faster Project 2 runs with smaller prompt payload.
- Keep topic-specific details only (topic, slug, audio URL, emphasis).

---

### 3) `Existing_work_pipeline_execution_master.md`
Main runbook for **full triplet mission flow**:
1. Generate script mission
2. Run audio pipeline mission
3. Update HTML mission
4. Validate in browser

Use when:
- You are doing end-to-end topic creation from scratch.

---

### 4) `Existing_work_pipeline_execution_provided_files_master.md`
Runbook for **provided-files mode** (HTML + script already exist).

Purpose:
- Run pipeline from existing script,
- wait for R2 upload,
- update HTML/card wiring,
- verify final state.

Use when:
- You already have both files and want fast completion.

---

### 5) `Existing_work_pipeline_execution_provided_files_runner_mode_master.md`
Runbook for **runner mode** (manual terminal by user).

Purpose:
- Codex provides numbered commands only,
- user runs commands,
- Codex performs wiring edits only after R2 confirmation.

Use when:
- You want strict manual command execution control.

---

## Recommended Workflow Patterns

## A) New Topic (No Script Yet)
1. Use `Project-1-Audioscript-Maker.txt` in ChatGPT Project 1.
2. Generate and save `audio_script_{slug}.md`.
3. Run audio pipeline:
   `.\scripts\run_mission_audio.ps1 "..\jobsearch\data\interview_prep\audio_prep\{slug}\audio_script_{slug}.md" -ChunkSize 750 -RequestTimeoutSeconds 120`
4. Upload `final_{slug}.mp3` to R2.
5. Use `Project2_HTMl_Maker.txt` in ChatGPT Project 2 to create/update `{slug}.html`.
6. Wire section/component card to live status.

## B) Provided Files (Fast Path)
1. Use `Existing_work_pipeline_execution_provided_files_master.md` (or runner-mode file).
2. Run audio pipeline from existing script.
3. Upload MP3 to R2.
4. Wire component card (`Open Reference`, clickable card, `🎧 Live`, `🎬 N/A`).

## C) Runner Mode (Manual Commands)
1. Use `Existing_work_pipeline_execution_provided_files_runner_mode_master.md`.
2. Execute numbered commands manually.
3. After upload confirmation, let Codex do wiring edits only.

## Path + Safety Rules

- Keep generated audio binaries **outside repo**:
  `D:\temp\studybook_audio\{slug}\`
- Keep only text artifacts in repo:
  - script markdown
  - HTML/component files
- Always verify audio source in page:
  `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_{slug}.mp3`

## Notes

- Some older runbook text may mention `D:\temp\studybook_audio\...`.
- Current active pipeline standard is `D:\temp\studybook_audio\...` for generated audio output.



