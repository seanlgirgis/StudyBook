# HANDOFF

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

Release 1 (StudyBubble v0.7 BOA Interaction Parity) manual browser smoke: PASS.

What was done:
- Added toolbar search in the viewer with case-insensitive matching across:
  - label
  - definition
  - whyItMatters
  - safeSentence
  - note.summary
- Added data-driven group filter buttons from topic groups (no hardcoded BOA groups).
- Search and group filter now work in combination.
- Added Reset/Clear behavior to clear search and restore group filter to All.
- Preserved existing behavior:
  - single-click inspect side panel
  - double-click one-child navigation
  - parent/back link behavior
  - external links opening in a new tab
- Applied Iteration 11 regression fix for single-file loading:
  - Root cause: generated single-file app shell was missing toolbar elements expected by viewer JS, which caused an early JS crash and left `Loading topic...`.
  - Fix: single-file builder now emits toolbar DOM in app shell, and viewer JS now safely handles missing toolbar nodes for backward compatibility.
- Applied Iteration 11 regression fix for parent-topic navigation:
  - Root cause: bubble double-click only handled single-child topic navigation; it did not fallback to `parentTopic`.
  - Fix: bubble double-click now keeps child-topic-open behavior when exactly one child exists, otherwise it navigates to `parentTopic` when configured.
  - Viewer hints/tooltips now explicitly describe this behavior.

Direction correction (current acceptance target):
- Primary acceptance artifact is single-file output (`outputs/single_file/*.html`), and this is the only active acceptance path.
- Primary acceptance smoke targets are:
  - `outputs/single_file/python_overview.html`
  - `outputs/single_file/pandas.html`
- Multi-file mode remains as deprecated historical/debug artifact only.
- Local HTTP server is only needed when explicitly testing deprecated multi-file `fetch("topic.studybubble.json")` behavior.
- Single-file output embeds topic data and should not require runtime `fetch()`.
- Parent/child navigation in single-file mode depends on sibling `.html` files existing under `outputs/single_file`.

Manual smoke checklist (single-file primary):
1. Open `outputs\single_file\python_overview.html` directly.
2. Confirm Python Overview loads.
3. Double-click Pandas bubble.
4. Confirm `outputs\single_file\pandas.html` opens.
5. On Pandas page, double-click a bubble.
6. Confirm it returns to `outputs\single_file\python_overview.html`.
7. Confirm browser console has no runtime error.
8. Confirm search works.
9. Confirm group filters work.
10. Confirm sidebar and reset still work.

Status of manual smoke in this run:
- Automated build/test checks passed.
- Manual single-file browser smoke executed and passed for:
  - `outputs\single_file\python_overview.html`
  - `outputs\single_file\pandas.html`
- Confirmed checklist pass:
  - visible child-topic button works
  - visible parent/back button works
  - parent/child double-click roundtrip works (`python_overview` <-> `pandas`)
  - browser console clean (no runtime error)
  - search, group filters, sidebar, and reset behave as expected
- Limitation reminder: single-file parent/child navigation requires sibling `.html` topic outputs to exist in `outputs/single_file`.

Release 1 PASS details:
- direct-open `case_capacity_overview.html` works
- search works
- group filters work
- study paths are clickable and highlight path nodes/links
- reset clears active study path
- minimap, zoom HUD, wheel zoom, pan, fit, toolbar reset view, drag mode all work
- selected-node and connected-node highlighting works
- focus works
- right-click context menu works
- right-click reset view works
- keyboard navigation works
- parent/child/grandchild navigation works:
  - `case_capacity_overview -> case_capacity_evidence -> case_capacity_feature_table -> case_capacity_evidence -> case_capacity_overview`
- console notes accepted as non-blocking:
  - `file://` unique-origin warning for direct-open local HTML
  - `aria-hidden` focus warning after context-menu close

Release 2 (StudyBubble v0.9 Study Card + Media + Links) manual browser smoke: PASS.

Release 2 progress note:
- Viewer side panel now renders richer study-card sections (when present):
  - common trap
  - interview answer
  - related questions
  - study note summary
  - image/diagram preview with graceful unavailable fallback
  - external links
- Copy helpers added with graceful fallback:
  - Copy Safe Sentence
  - Copy Study Path (when a path is active)
- Search now includes additional rehearsal text fields.
- Media-rich sample content added to `case_capacity_feature_table` with local SVG asset `assets/feature-table-example.svg`.

Release 2 PASS details:
- `outputs/single_file/case_capacity_feature_table.html` opens directly
- enhanced study card renders
- card fields display: definition, why it matters, safe sentence, common trap, interview answer, related questions, study note, image/diagram, external links, parent topic, and study path
- local SVG image displays from `outputs/single_file/assets/feature-table-example.svg`
- search finds optional card text (`feature drift` -> 1 match)
- external link opens successfully
- parent/back navigation returns to Evidence and Features
- reset clears search and restores normal map
- Copy Safe Sentence works
- Copy Study Card works
- console shows only accepted `file://` unique-origin warning
- no `TypeError`, `ReferenceError`, `SyntaxError`, or `ERR_FILE_NOT_FOUND`

Product direction note:
- StudyBubble is primarily a visual study-map builder.
- Copy buttons are secondary polish, not the core direction.

Release 3 packaging status:
- Created `outputs/releases/studybubble-v1.0/` package folder with:
  - core single-file maps
  - required local image asset under `assets/`
  - `README_RELEASE.md`
  - `MANUAL_SMOKE_CHECKLIST.md`
- simple `index.html` launch page

Next step:
- Manual browser smoke from release folder: PASS.
- Ready for v1.0 freeze commit/tag.

v1.1 Resizable Study Panel smoke:
- PASS
- divider drag resizes panel
- map area adjusts
- text wraps and image scales in card
- panel scroll remains usable
- minimap stays usable
- panel width persistence works after refresh
- no TypeError/ReferenceError/SyntaxError/ERR_FILE_NOT_FOUND

Iteration 13 repair note:
- First visual smoke failed due to dense case-study layout/readability limits.
- Repair completed with improved node sizing, group-based spacing, collision handling, label wrapping, and link visibility.
- Visual polish applied: adjusted vertical centering so maps sit around the middle of the canvas instead of drifting low.
- Manual browser smoke rerun completed and PASS confirmed.

Iteration 13 manual browser smoke checklist (case-study depth demo):
1. Open `outputs\single_file\case_capacity_overview.html` directly.
2. Confirm the overview loads.
3. Select each hub bubble that has a child topic.
4. Confirm visible child-topic buttons appear.
5. Navigate to Evidence and Features.
6. Confirm parent/back button returns to Case Overview.
7. Navigate to Forecast and Risk.
8. Confirm parent/back button returns to Case Overview.
9. Navigate to Decision and Governance.
10. Confirm parent/back button returns to Case Overview.
11. Confirm double-click shortcut still works where there is exactly one child.
12. Confirm search works on each screen.
13. Confirm group filters work on each screen.
14. Confirm sidebar works on each screen.
15. Confirm reset works on each screen.
16. Confirm browser console is clean.

Iteration 13 manual browser smoke result:
- PASS for:
  - `outputs\single_file\case_capacity_overview.html`
  - `outputs\single_file\case_capacity_evidence.html`
  - `outputs\single_file\case_capacity_forecast.html`
  - `outputs\single_file\case_capacity_decision.html`
- Confirmed:
  - bubbles are readable and no longer crowded into one row
  - labels are readable
  - bubble sizes are visibly different
  - links are visible enough to understand relationships
  - case study flow reads left/center/right
  - visible parent/back button works
  - visible child navigation buttons work
  - double-click shortcut still works
  - search, group filters, sidebar, and reset all work
  - browser console is clean
