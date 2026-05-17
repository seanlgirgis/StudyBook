# StudyBubble V1 Release Plan

## Current Frozen Base
- Tag: `studybubble-grandchild-navigation-v1`
- Commit: `cac91de`

Already proven:
- single-file direct-open output
- validator/builder flow
- visible parent/child navigation
- grandchild navigation
- capacity case-study depth
- basic search/filter/sidebar/reset
- readable generated case-study maps

## Release 1: StudyBubble v0.7 - BOA Interaction Parity

Status:
- Completed (manual browser smoke PASS).

Goal:
- Make generated StudyBubble maps feel like the BOA reference prototype.

Scope:
- minimap
- zoom HUD
- pan mode
- fit button
- reset view
- drag mode
- right-click context menu
- focus connections
- filter to group from context menu
- selected-node highlighting
- connected-node highlighting
- study path link highlighting
- keyboard hints/basic keyboard navigation
- cleaner header/back/search layout

Acceptance:
- direct-open `case_capacity_overview.html`
- search works
- filters work
- study paths work
- minimap works
- zoom/pan works
- fit/reset works
- drag mode works
- right-click menu works
- focus connections works
- parent/child/grandchild navigation still works
- console clean

## Release 2: StudyBubble v0.9 - Study Card + Media + Links

Status:
- Completed (manual browser smoke PASS).

Goal:
- Turn the side panel into a real study/rehearsal card.

Scope:
- `note.summary` in side panel
- `commonTrap` in side panel
- `interviewAnswer` in side panel
- `relatedQuestions` in side panel
- `externalLinks` in side panel
- cleaner child-topic section
- cleaner parent-topic section
- copy safe sentence
- copy study path
- image preview from `note.image.src`
- image caption
- graceful missing-image message
- optional stretch: `--embed-images` builder flag

Acceptance:
- build one media-rich sample topic
- side panel shows all study fields
- external links open in new tab
- image preview displays
- missing image does not break page
- copy buttons work
- parent/child/grandchild navigation still works
- search includes useful study text
- console clean

## Release 3: StudyBubble v1.0 - Usable Release Package

Status:
- Completed for package readiness (manual release-folder smoke PASS; freeze commit/tag step pending).

Goal:
- Make StudyBubble usable as a StudyBook visual study system.

Scope:
- generated topic index/home page
- links to all generated StudyBubble maps
- topic title/subtitle/category on index
- build-all command or script
- sample set:
  - `python_overview`
  - `pandas`
  - capacity case study
  - feature table deep dive
  - one BOA-scale generated stress topic
- full release smoke checklist
- packaged zip
- final v1.0 tag

Acceptance:
- `pytest` passes
- build-all passes
- direct-open `index.html` works
- every generated map opens from index
- BOA-scale map is usable
- navigation depth still works
- images/links work
- drag/minimap/fit/reset work
- console clean
- package zip created
- release tag created

## Non-Goals
- no React
- no npm
- no backend
- no database
- no local server dependency
- no multi-file acceptance

## Release Rules
- No minor tags between these release gates unless user explicitly asks.
- Each release gets deep browser smoke, commit, tag, and optional zip.

Post-v1.0 note:
- v1.1 usability increment completed: resizable study panel with persistence (manual smoke PASS).
