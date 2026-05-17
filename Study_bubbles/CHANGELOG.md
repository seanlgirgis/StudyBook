# CHANGELOG

## 2026-05-15 - Iteration 0 Initiation
- Created initial `study_bubbles` project scaffold.
- Added governance and project memory files.
- Added architecture, contract, test plan, roadmap, and decisions docs.
## 2026-05-15 - Iteration 1 Preserve BOA Artifact
- Preserved `BOA_Terminology_Bubble_Map_v3.html` unchanged in:
  - `legacy/BOA_Terminology_Bubble_Map_v3.html`
  - `outputs/baseline/BOA_Terminology_Bubble_Map_v3.html`
- Added preservation proof file at `outputs/baseline/run_proofs/iteration1_preserve_boa_artifact_proof.txt`.
- Verified source, legacy, and baseline copies have matching byte size and SHA256.
## 2026-05-15 - Iteration 2 Roadmap and Contract Pivot
- Updated project direction so BOA is a preserved reference prototype, not the first migration target.
- Repointed next build target to `tiny_capacity_demo.studybubble.json` (3-5-7 staged growth).
- Updated roadmap to validator/builder pipeline iterations (multi-file and single-file outputs).
- Expanded topic contract to include `parentTopic`, `childTopics`, `externalLinks`, and `note` image/summary fields.
- Clarified link behavior distinction: external links open new tab; child topic navigation stays inside StudyBubble.
- Kept this run documentation-only (no viewer/validator/builder/data implementation).
## 2026-05-15 - Iteration 3 Tiny 3-Bubble Topic Data File
- Created `topics/tiny_capacity_demo.studybubble.json` as the first real StudyBubble topic data file.
- Added exactly 3 nodes: Telemetry, Baseline, Forecast.
- Added exactly 2 links: Telemetry -> Baseline, Baseline -> Forecast.
- Added exactly 1 starter path: `Telemetry to Forecast`.
- Kept this iteration data-only (no viewer, validator, or builder implementation).
## 2026-05-15 - Iteration 4 Topic Validator
- Added `src/study_bubbles/validate_topic.py` for structural topic validation with clear PASS/FAIL output.
- Added `tests/test_validate_topic.py` with pytest coverage for valid and invalid topic cases.
- Validated `topics/tiny_capacity_demo.studybubble.json` successfully.
- Added run proof: `outputs/baseline/run_proofs/iteration4_validator_proof.txt`.
- Kept this iteration validator-only (no viewer or builder implementation).
## 2026-05-16 - Iteration 5 Minimal Multi-File Viewer / Builder
- Added builder module `study_bubbles.build_topic` with multifile mode support.
- Added viewer templates under `viewer/` (`bubble_viewer.html`, `bubble_viewer.css`, `bubble_viewer.js`).
- Generated first multifile output at `outputs/multifile/tiny_capacity_demo`.
- Builder now validates topic data before output generation.
- Generated output files: `index.html`, `bubble_viewer.css`, `bubble_viewer.js`, `topic.studybubble.json`, and `run_proof.txt`.
- Confirmed validator and pytest pass in this iteration.
## 2026-05-16 - Direction Cleanup (Docs Only, Post Iteration 5)
- Recorded decision that generated HTML/output files are build artifacts, not source.
- Documented maintained-source vs generated-output split.
- Added local HTTP server guidance for multi-file browser testing (`file://` may block JSON fetch).
- Clarified Iteration 6 single-file output structure expectations (metadata, styles, app shell, embedded topic data, JavaScript, build metadata).
- Added implementor rule to avoid manual edits to generated output.
- Added note to review duplicate `build_topic.py` paths in next implementation step.
## 2026-05-16 - Roadmap Alignment (Docs Only)
- Aligned iteration sequence after Iteration 5 learning.
- Added Iteration 6 as Generated Output Rule and Package Path Cleanup.
- Renumbered future implementation iterations:
  - single-file builder moved to Iteration 7
  - 5/7 bubble expansion moved to Iteration 8
  - parent/child navigation moved to Iteration 9
  - BOA reference behavior review moved to Iteration 10
- Reconfirmed generated HTML/output as rebuildable artifacts, not source.
- Reconfirmed local HTTP server testing recommendation for multifile output.
- Updated revised iterations tracker file.
## 2026-05-16 - Iteration 7 Minimal Single-File Builder
- Extended `study_bubbles.build_topic` to support `--mode single-file`.
- Generated `outputs/single_file/tiny_capacity_demo.html` with organized sections:
  - Metadata
  - Styles
  - App Shell
  - Embedded Topic Data
  - JavaScript
  - Build Metadata
- Updated viewer JavaScript to support both modes:
  - embedded JSON (single-file)
  - fetched `topic.studybubble.json` (multifile)
- Kept multifile behavior unchanged and verified build regression command passes.
- Added single-file proof file: `outputs/single_file/run_proofs/iteration7_single_file_proof.txt`.
- Inspected duplicate builder paths and kept both in sync for compatibility (`src/study_bubbles/build_topic.py` and `study_bubbles/build_topic.py`).
## 2026-05-16 - Iteration 8 Expand Tiny Demo to 5/7 Bubbles
- Expanded `topics/tiny_capacity_demo.studybubble.json` from 3 nodes to 7 nodes.
- Added support nodes: Dashboard, Decision, Threshold, Owner.
- Expanded relationships to 6 links and study paths to 3 paths.
- Revalidated topic, reran pytest, and rebuilt both multifile and single-file outputs.
- Added run proof: `outputs/baseline/run_proofs/iteration8_expand_tiny_demo_proof.txt`.
- Confirmed output growth came from data changes only (no manual HTML surgery).
## 2026-05-16 - Iteration 9 Parent/Child Topic Navigation Spike
- Added new topics:
  - `topics/python_overview.studybubble.json`
  - `topics/pandas.studybubble.json`
- Updated viewer side panel behavior to render:
  - node external links (new tab)
  - node child topic links
  - top-level parent topic/back link
- Added mode-aware topic link mapping:
  - single-file: links point to sibling `.html` files
  - multifile: links point to sibling `../<topic_id>/index.html`
- Validated all three topics and reran pytest.
- Built multifile and single-file outputs for python_overview and pandas.
- Rebuilt tiny_capacity_demo outputs as regression check.
- Added run proof: `outputs/baseline/run_proofs/iteration9_parent_child_navigation_proof.txt`.
## 2026-05-16 - UX Enhancement: Double-Click Child Navigation
- Added bubble double-click navigation behavior for nodes with exactly one child topic.
- Kept single-click behavior unchanged for inspect/study side-panel updates.
- Added side-panel hint for one-child nodes: "Double-click this bubble to open ...".
- Added tooltip/title text on one-child bubbles: "Double-click to open ...".
- Preserved parent/back link visibility in side panel.
- Revalidated topics, reran pytest, and rebuilt multifile/single-file outputs.
- Added run proof: `outputs/baseline/run_proofs/ux_double_click_child_navigation_proof.txt`.
## 2026-05-16 - Iteration 10 BOA Reference Behavior Review
- Reviewed `legacy/BOA_Terminology_Bubble_Map_v3.html` as reference prototype behavior source.
- No BOA data extraction or migration was performed.
- Added `docs/BOA_REFERENCE_BEHAVIOR_REVIEW.md` with behavior matrix, adopt-now/later/skip guidance, and guardrails.
- Recommended next small implementation: search + group filters.
## 2026-05-16 - Iteration 11 Search + Group Filters
- Added a top toolbar to the viewer with:
  - search input
  - match count
  - data-driven group filter buttons
  - reset/clear action
- Implemented case-insensitive search across `label`, `definition`, `whyItMatters`, `safeSentence`, and `note.summary`.
- Implemented data-driven group filters generated from topic groups (no hardcoded BOA groups).
- Implemented combined search + filter behavior with clear reset semantics.
- Preserved existing behavior:
  - single-click side-panel inspect
  - double-click one-child navigation
  - parent/back link behavior
  - external links opening in a new tab
- Revalidated all active topics, reran pytest, and rebuilt multi-file/single-file outputs.
- Added run proof: `outputs/baseline/run_proofs/iteration11_search_group_filters_proof.txt`.
## 2026-05-16 - Iteration 11 Regression Fix (Single-File Topic Loading)
- Fixed regression where `outputs/single_file/pandas.html` stayed on `Loading topic...`.
- Root cause: single-file builder app shell did not include toolbar elements expected by updated viewer JS, causing an early runtime error before embedded JSON load.
- Updated single-file builder template in both package paths:
  - `src/study_bubbles/build_topic.py`
  - `study_bubbles/build_topic.py`
  to include `search-input`, `search-count`, `group-filters`, and `clear-filters` in the generated HTML app shell.
- Added defensive null-checks in `viewer/bubble_viewer.js` so missing toolbar elements do not crash legacy outputs.
- Revalidated topics, reran pytest, and rebuilt all multifile/single-file outputs.
- Added run proof: `outputs/baseline/run_proofs/iteration11_single_file_loading_fix_proof.txt`.
## 2026-05-16 - Iteration 11 Regression Fix (Parent-Topic Double-Click Navigation)
- Fixed regression where child-topic screens (example: `pandas`) did not navigate back via bubble double-click when `parentTopic` was configured.
- Root cause: bubble `dblclick` handler only attempted single-child navigation and had no fallback path to `parentTopic`.
- Updated `viewer/bubble_viewer.js`:
  - if node has exactly one child topic, dblclick still opens that child (unchanged);
  - otherwise, if current topic has `parentTopic`, dblclick navigates to parent topic;
  - updated side-panel hint/tooltip text so behavior is explicit and not silent.
- Added validator-positive tests in `tests/test_validate_topic.py`:
  - parentTopic with `label` + `topic` passes;
  - childTopics entry with `label` + `topic` passes.
- Revalidated and rebuilt:
  - multifile: `python_overview`, `pandas`
  - single-file: `python_overview.html`, `pandas.html`
- Note: multifile fetch still depends on local HTTP serving; direct `file://` may block JSON fetch in browser security mode.
## 2026-05-16 - Iteration 11 Documentation Direction Correction (Single-File First)
- Corrected stale project guidance that over-emphasized multi-file local-server smoke testing.
- Updated project memory/docs to state that primary acceptance target is single-file output:
  - `outputs/single_file/python_overview.html`
  - `outputs/single_file/pandas.html`
- Clarified acceptance behavior:
  - single-file pages are opened directly from File Explorer;
  - single-file embeds topic data and should not require `fetch()`;
  - parent/child single-file navigation depends on sibling `.html` files in `outputs/single_file`.
- Clarified multi-file role:
  - still supported, but secondary development/debug artifact;
  - local HTTP server guidance applies only when explicitly testing multi-file fetch behavior.
- Updated:
  - `PROJECT_STATE.md`
  - `TASK_BOARD.md`
  - `HANDOFF.md`
  - `docs/TEST_PLAN.md`
  - `docs/ROADMAP.md`
  - `docs/DECISIONS.md`
## 2026-05-16 - Constitution Amendment: Single-File-Only Active Direction
- Amended project direction so active development acceptance is single-file-only.
- Reclassified multi-file architecture/testing references as deprecated historical/debug context, not active acceptance.
- Added required top-of-file active-direction note to:
  - `PROJECT_STATE.md`
  - `HANDOFF.md`
- Updated active guidance across:
  - `README.md`
  - `AGENTS.md`
  - `TASK_BOARD.md`
  - `docs/DESIGN.md`
  - `docs/CONTRACT.md`
  - `docs/TEST_PLAN.md`
  - `docs/ROADMAP.md`
  - `docs/DECISIONS.md`
- Kept multi-file code paths in builder/viewer intact for now to avoid risky code churn; documented as deprecated for current acceptance.
## 2026-05-16 - Manual Single-File Browser Smoke Recorded (PASS)
- Recorded successful manual primary-acceptance smoke for:
  - `outputs/single_file/python_overview.html`
  - `outputs/single_file/pandas.html`
- Confirmed:
  - topic pages open directly from file path
  - parent/child double-click navigation roundtrip works
  - browser console has no runtime error
  - search, group filters, sidebar, and reset behavior still work
- Iteration 12 intentionally not started; stopped at documentation/state recording step.
## 2026-05-16 - Iteration 12 Visible Navigation UI
- Added visible topic-level parent/back navigation button when `parentTopic` exists.
- Added visible child-topic navigation buttons in the side-panel details for selected nodes with `childTopics`.
- Child/parent button navigation opens sibling `.html` topic targets derived from `.studybubble.json` references.
- Preserved existing navigation behavior:
  - double-click child open for exactly one child topic
  - double-click fallback to parent topic when no single child target exists
- Preserved existing viewer behaviors: search, group filters, sidebar details, reset, and study paths.
## 2026-05-16 - Iteration 13 Case Study Depth Demo
- Added four linked case-study topic files under `topics/`:
  - `case_capacity_overview.studybubble.json`
  - `case_capacity_evidence.studybubble.json`
  - `case_capacity_forecast.studybubble.json`
  - `case_capacity_decision.studybubble.json`
- Theme: "How raw telemetry becomes a capacity decision."
- Overview screen acts as hub with child topic navigation:
  - Evidence and Features
  - Forecast and Risk
  - Decision and Governance
- Child screens include `parentTopic` back navigation to the case overview screen.
- Added practical, interview-safe enterprise capacity language with definition, why-it-matters, and safe sentence fields on each concept node.
- Added relationship links and study paths on each case-study screen.
## 2026-05-16 - Iteration 13 Visual Repair (Usability Fix)
- Recorded first visual smoke failure for Iteration 13 case-study screens:
  - dense horizontal crowding
  - node overlap
  - clipped/unreadable labels
  - weak link readability
- Root cause: legacy single-row layout strategy in viewer did not scale to 10-14 node case-study screens.
- Repair implemented:
  - deterministic group-based placement across canvas regions
  - collision relaxation with minimum spacing by radius
  - larger canvas/viewBox and increased map height
  - clearer core/support/detail radius differences
  - wrapped multi-line bubble labels for long terms
  - improved link contrast/visibility
- Content tuning for usability:
  - reduced densest case-study screens to 12 nodes where needed
  - rebalanced core/support/detail assignments.
## 2026-05-16 - Iteration 13 Visual Polish (Vertical Centering)
- Adjusted deterministic layout y-centering in `viewer/bubble_viewer.js` so case-study bubbles sit closer to the visual middle of the map panel.
- Reduced row spacing slightly while preserving collision relaxation and no-overlap safeguards.
- Kept all existing interaction behavior unchanged (navigation buttons, double-click shortcut, search, filters, sidebar, reset, and study paths).
## 2026-05-16 - Iteration 13 Manual Browser Smoke (PASS)
- Recorded PASS for direct-open single-file case-study screens:
  - `case_capacity_overview.html`
  - `case_capacity_evidence.html`
  - `case_capacity_forecast.html`
  - `case_capacity_decision.html`
- Confirmed visual usability:
  - readable bubbles with no one-row crowding
  - readable labels
  - visible core/support/detail size contrast
  - visible enough links to understand relationships
  - clear left/center/right flow
- Confirmed behavior integrity:
  - parent/back button works
  - child navigation buttons work
  - double-click shortcut works
  - search, filters, sidebar, and reset work
  - browser console clean
## 2026-05-16 - Iteration 14 Grandchild Navigation Spike
- Added new grandchild topic:
  - `topics/case_capacity_feature_table.studybubble.json`
- Added new single-file output target:
  - `outputs/single_file/case_capacity_feature_table.html`
- Updated `topics/case_capacity_evidence.studybubble.json`:
  - `feature_table` node now includes child topic navigation to `case_capacity_feature_table.studybubble.json`.
- New grandchild topic includes parentTopic back navigation:
  - label: `Back to Evidence and Features`
  - topic: `case_capacity_evidence.studybubble.json`
- Preserved existing evidence parentTopic back navigation:
  - label: `Back to Case Overview`
  - topic: `case_capacity_overview.studybubble.json`
- Resulting target flow:
  - `overview -> evidence -> feature_table -> evidence -> overview`

