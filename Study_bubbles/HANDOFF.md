# HANDOFF

Current active direction:
StudyBubble is single-file-only for current development.
Do not use multi-file output, local HTTP server testing, or fetch-based
topic loading as acceptance criteria unless the user explicitly reopens that
architecture later.

Iteration 11 is complete.

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
  - parent/child double-click roundtrip works (`python_overview` <-> `pandas`)
  - browser console clean (no runtime error)
  - search, group filters, sidebar, and reset behave as expected
- Limitation reminder: single-file parent/child navigation requires sibling `.html` topic outputs to exist in `outputs/single_file`.

Next step:
- Discussion checkpoint complete. Do not start Iteration 12 yet.
