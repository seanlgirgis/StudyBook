# PROJECT_STATE

Current active direction:
StudyBubble is single-file-only for current development.
Do not use multi-file output, local HTTP server testing, or fetch-based
topic loading as acceptance criteria unless the user explicitly reopens that
architecture later.
Deprecated implementation residue:
Some old non-active code paths may still exist from earlier multi-file work.
Do not treat them as active concerns or repeat them in normal reports unless
they cause a failing test or the user explicitly opens a cleanup task.
Active acceptance remains direct-open outputs/single_file/*.html.

- Project Name: study_bubbles
- Project Purpose: Build a small, static, reusable study bubble system that generates study maps from topic data files.
- Current Phase: Iteration 14 - Grandchild Navigation Spike (implementation complete, manual browser smoke pending in this run)
- Completed: Toolbar search and data-driven group filters were added to the viewer; Iteration 11 regression fixes restored single-file topic loading and parent-topic double-click fallback navigation; Iteration 12 adds visible parent/back and child-topic navigation buttons while preserving double-click shortcuts; Iteration 13 adds a four-screen capacity forecasting case-study path and repairs dense-layout readability with improved sizing/spacing/label/link rendering; Iteration 14 adds a grandchild topic for three-level navigation proof.
- Outputs: Single-file outputs are the active acceptance artifacts (`outputs/single_file/*.html`); multi-file outputs are deprecated historical/debug artifacts.
- BOA Migration Status: No BOA migration or data extraction was performed.
- Review Artifact: `docs\BOA_REFERENCE_BEHAVIOR_REVIEW.md`
- Source/Output Rule: generated HTML is output, not source; generated outputs are disposable/rebuildable artifacts.
- BOA Status: Preserved safely as a reference prototype.
- Known Local Path: `D:\Workarea\StudyBook\study_bubbles`
- Environment Bootstrap Command: From `study_bubbles`, run `..\env_setter.ps1`
- Relationship: ChatGPT StudyBubble is architect/orchestrator; Codex is implementor.
- Primary Acceptance Smoke Target: `outputs/single_file/python_overview.html` and `outputs/single_file/pandas.html`, opened directly from File Explorer.
- Manual Smoke Status: PASS (single-file browser smoke completed for `python_overview.html` -> `pandas.html` -> back to `python_overview.html`; visible child-topic button PASS; visible parent/back button PASS; double-click shortcut PASS; console clean; search/filters/sidebar/reset PASS).
- Iteration 13 Visual Smoke Status: First review FAILED (overlap/crowding/readability); repair implemented; rerun pending.
- Iteration 13 Visual Polish Status: Vertical centering adjusted to better use map area; browser smoke rerun PASS.
- Iteration 13 Manual Smoke Status: PASS (`case_capacity_overview`/`evidence`/`forecast`/`decision` direct-open screens; readable non-overlapping bubbles; clear size contrast; visible links; left/center/right flow; parent/child buttons and double-click shortcut PASS; search/filters/sidebar/reset PASS; console clean).
- Iteration 14 Navigation Status: Grandchild topic wired (`overview -> evidence -> feature_table -> evidence -> overview`) with topic-declared parent/back links; manual browser smoke pending.
- Multi-file Note: local HTTP server applies only to deprecated multi-file fetch testing and is not part of active acceptance.
- Next Intended Step: run Iteration 14 manual browser smoke and record PASS/FAIL before any commit/tag.
