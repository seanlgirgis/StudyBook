# BOA Reference Behavior Review

## 1. Executive Summary
BOA is reference-only in this iteration.
No BOA migration, node extraction, or BOA rebuild was performed.
The goal was to harvest behavior ideas from `legacy/BOA_Terminology_Bubble_Map_v3.html` and compare them against current StudyBubble capabilities.

## 2. Current StudyBubble Baseline
Current StudyBubble engine already includes:
- Topic data files (`.studybubble.json`)
- Topic validator
- Builder workflow
- Multi-file output
- Single-file output
- 7-bubble tiny demo
- Parent/child links in side panel
- External links in side panel
- Parent/back links
- Double-click child navigation (one-child rule)
- Study path list display

## 3. BOA Behaviors Reviewed
| Behavior | Present in BOA? | Already in StudyBubble? | Adopt? | Priority | Notes |
|---|---|---|---|---|---|
| Bubble sizing by concept level | Yes | Partial | Yes | Already Covered | StudyBubble already supports size levels (`core/support/detail`), but visual tuning can improve later. |
| Group color coding | Yes | Yes | Yes | Already Covered | Present in current viewer; keep pattern. |
| Group clustering layout | Yes | Partial | Yes | Later | Current layout is simple row placement; BOA-style cluster spacing could improve readability later. |
| Relationship lines with directional arrows | Yes | Partial | Yes | Later | StudyBubble draws links; directional styling could be incrementally improved. |
| Readability spacing polish | Yes | Partial | Yes | Later | BOA has denser but tuned spacing; current engine intentionally simple. |
| Hover tooltip | Yes | No | Yes | Now | Low-cost usability improvement for quick context. |
| Side panel details | Yes | Yes | Yes | Already Covered | Core side-panel behavior already implemented. |
| Definition popup/modal | Yes | No | Maybe | Skip | Adds UI complexity beyond current small-step goals. |
| Right-click context menu | Yes | No | Maybe | Skip | Useful but non-essential for current learning path. |
| Drag mode (node reposition) | Yes | No | Maybe | Later | Could help exploratory layouts but needs guardrails. |
| Pan/zoom | Yes | No | Maybe | Later | Valuable for bigger maps; current maps still small. |
| Fit/reset controls | Yes | No | Yes | Later | Useful once pan/zoom exists. |
| Minimap | Yes | No | Maybe | Later | Helpful for large graphs, unnecessary for tiny maps now. |
| Study path buttons | Yes | Partial | Yes | Later | Study path list exists; active highlighting controls can be added. |
| Study path highlighting lane | Yes | No | Yes | Now | Strong study value with moderate implementation cost. |
| Connected terms emphasis | Yes | Partial | Yes | Now | Side-panel connected terms polish can be expanded from existing link context. |
| Search | Yes | No | Yes | Now | High value, relatively small implementation. |
| Group filters | Yes | No | Yes | Now | Pairs naturally with search; strong map usability. |
| Legend | Yes | No | Maybe | Later | Good orientation aid once features grow. |
| Keyboard shortcuts | Yes | No | Maybe | Later | Useful but not urgent. |
| Copy behavior | Yes (limited/contextual actions) | No | Maybe | Later | Could map to "copy safe sentence/path" backlog. |
| Print/export mode | Yes (lightweight potential) | No | Maybe | Later | Good for handouts/review packs but not immediate. |

## 4. Recommended Adopt Now (Max 3)
1. Search across node label/definition.
2. Group filters (all/groups toggle).
3. Study path highlighting (visual lane emphasis for selected path).

These three are practical, high-learning-value, and align with current static-first architecture.

## 5. Recommended Adopt Later
- Hover tooltip polish.
- Pan/zoom plus fit/reset.
- Minimap.
- Drag mode (with clear mode toggle and safe defaults).
- Keyboard navigation shortcuts.
- Legend section.
- Optional print/export mode.
- Copy utilities (safe sentence/path) after core navigation UX matures.

## 6. Recommended Skip For Now
- Full right-click context menu.
- Rich modal workflow as primary interaction model.
- Any heavy, app-like interaction layer that pushes beyond small static study-map scope.

## 7. Proposed Future Iteration Sequence
- Iteration 11: Search and group filters.
- Iteration 12: Study path highlighting improvements.
- Iteration 13: Hover tooltip and connected-terms polish.
- Iteration 14: Optional pan/zoom + fit/reset + minimap discussion.

## 8. Risks / Guardrails
- Do not overbuild.
- Do not turn StudyBubble into a full TheBrain clone.
- Keep static-first architecture.
- Keep generated output as disposable build artifact.
- Keep source files as source of truth.
- Preserve one-topic-per-file discipline.

## 9. Final Recommendation
Use Iteration 11 for a small, focused usability win: implement search + group filters in the current viewer while preserving existing output/build flow.
