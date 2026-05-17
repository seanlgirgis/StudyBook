# TEST_PLAN

## Planned Validation and Build Tests

Contract/schema tests:
- Topic schema validation
- Required top-level fields validation (`id`, `title`, `nodes`, `links`)
- One topic file identity checks (`topic id` consistency)

Node/link/path integrity tests:
- Duplicate node id detection
- Invalid group detection
- Invalid node size detection
- Link source/target validation
- Study path node validation

New contract behavior tests:
- `parentTopic` format/reference validation
- `externalLinks` structure + URL format validation
- `childTopics` structure + topic id validation
- `note.summary` type validation
- `note.image.src` and `note.image.caption` type validation
- Enforce linked image path strategy (no base64 expected)

Builder/output tests:
- Output folder creation
- Single-file output smoke check (primary and only active acceptance)
- Primary acceptance smoke pages:
  - `outputs/single_file/python_overview.html`
  - `outputs/single_file/pandas.html`
  - `outputs/single_file/case_capacity_overview.html`
  - `outputs/single_file/case_capacity_evidence.html`
  - `outputs/single_file/case_capacity_forecast.html`
  - `outputs/single_file/case_capacity_decision.html`
  - `outputs/single_file/case_capacity_feature_table.html`
- Single-file run mode: open pages directly from File Explorer (`file://`) with no `fetch()` requirement because topic data is embedded.
- Parent/child single-file navigation expectation: sibling `.html` topic files must exist under `outputs/single_file`.
- Visible navigation UI checks:
  - topic-level parent/back button is shown when `parentTopic` exists
  - selected-node child-topic button(s) are shown when `childTopics` exists
  - child/parent buttons navigate to sibling `.html` targets
  - double-click navigation still works as shortcut
- Case-study depth checks:
  - overview screen provides child navigation to evidence, forecast, and decision screens
  - each child screen provides visible parent/back navigation to overview
  - evidence screen provides child navigation from Feature Table node to Feature Table Deep Dive
  - Feature Table Deep Dive provides visible parent/back navigation to Evidence and Features
  - three-level navigation flow works: overview -> evidence -> feature_table -> evidence -> overview
  - search, group filters, sidebar, and reset work on each case-study screen
  - no bubble overlap on case-study screens
  - labels remain readable (including wrapped long labels)
  - core/support/detail size difference is visually clear
  - links remain visible enough to interpret relationships
  - all four case-study screens open directly from file path and pass manual smoke checks
- v0.7 BOA parity checks (manual smoke, direct-open `case_capacity_overview.html`):
  - study path entries are clickable from visible UI
  - clicking a study path highlights path nodes and path links
  - reset clears active study path and highlight state
  - right-click context menu reset view triggers same view reset behavior as toolbar reset view
  - keyboard navigation works while preserving existing navigation behavior
  - accepted non-blocking console notes:
    - `file://` unique-origin warning
    - `aria-hidden` focus warning after context-menu close
- v0.9 study-card checks (manual smoke, direct-open `case_capacity_feature_table.html`):
  - selected node displays optional study fields when present:
    - `commonTrap`, `interviewAnswer`, `relatedQuestions`, `note.summary`, `note.image`, `externalLinks`
  - missing optional fields do not break rendering
  - Copy Safe Sentence works, or shows graceful copy fallback status
  - Copy Study Path works when a study path is active, or shows graceful fallback status
  - `note.image` preview displays when available, otherwise shows non-breaking unavailable message
  - search finds content from rehearsal/study-card fields
  - local image preview resolves from copied output asset path (`outputs/single_file/assets/...`)
  - Copy Study Card works (secondary polish)
  - no `TypeError`, `ReferenceError`, `SyntaxError`, or `ERR_FILE_NOT_FOUND`
  - accepted console note: `file://` unique-origin warning
- Deprecated/historical only:
  - multi-file output smoke checks
  - multi-file local HTTP-server checks
  - fetch-based topic loading checks
- Reporting guidance:
  - deprecated/historical checks are not part of normal acceptance reporting
  - only call them out when they fail and affect runtime/tests, or when explicit cleanup is requested
- Single-file structure smoke check for organized sections:
  - metadata
  - styles
  - app shell
  - embedded topic data
  - JavaScript
  - build metadata
- v1.0 package smoke target:
  - `outputs/releases/studybubble-v1.0/index.html` (or `case_capacity_overview.html` if index is unavailable)
  - release-folder navigation chain:
    - overview -> evidence -> feature table deep dive
  - release asset load check:
    - `outputs/releases/studybubble-v1.0/assets/feature-table-example.svg`
- v1.1 resizable panel checks:
  - drag divider resizes side panel
  - map area responds to panel width change
  - panel content remains scrollable
  - text wraps and image scales correctly in resized panel
  - panel width persists after refresh when localStorage is available
