# PROJECT_STATE

Current active direction:
StudyBubble is single-file-only for current development.
Do not use multi-file output, local HTTP server testing, or fetch-based
topic loading as acceptance criteria unless the user explicitly reopens that
architecture later.

- Project Name: study_bubbles
- Project Purpose: Build a small, static, reusable study bubble system that generates study maps from topic data files.
- Current Phase: Direction amendment after Iteration 11 (single-file-only active acceptance)
- Completed: Toolbar search and data-driven group filters were added to the viewer; Iteration 11 regression fixes restored single-file topic loading and parent-topic double-click fallback navigation.
- Outputs: Single-file outputs are the active acceptance artifacts (`outputs/single_file/*.html`); multi-file outputs are deprecated historical/debug artifacts.
- BOA Migration Status: No BOA migration or data extraction was performed.
- Review Artifact: `docs\BOA_REFERENCE_BEHAVIOR_REVIEW.md`
- Source/Output Rule: generated HTML is output, not source; generated outputs are disposable/rebuildable artifacts.
- BOA Status: Preserved safely as a reference prototype.
- Known Local Path: `D:\Workarea\StudyBook\study_bubbles`
- Environment Bootstrap Command: From `study_bubbles`, run `..\env_setter.ps1`
- Relationship: ChatGPT StudyBubble is architect/orchestrator; Codex is implementor.
- Primary Acceptance Smoke Target: `outputs/single_file/python_overview.html` and `outputs/single_file/pandas.html`, opened directly from File Explorer.
- Manual Smoke Status: PASS (single-file browser smoke completed for `python_overview.html` -> `pandas.html` -> back to `python_overview.html`; console clean; search/filters/sidebar/reset verified).
- Multi-file Note: local HTTP server applies only to deprecated multi-file fetch testing and is not part of active acceptance.
- Next Intended Step: discussion checkpoint after successful manual smoke; Iteration 12 remains paused.
