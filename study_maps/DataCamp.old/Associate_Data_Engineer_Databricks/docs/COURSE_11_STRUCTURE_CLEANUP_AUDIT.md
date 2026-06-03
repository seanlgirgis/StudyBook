# Course 11 Structure Cleanup Audit

## What Was Wrong
- Course 11 lacked a polished local HTML front door under `study_pages/11_intro_pyspark`.
- Map resources were mixed across markdown-target and output-target conventions.
- QA markdown had a duplicated top title/purpose block.

## What Was Fixed
- Created Course 11 HTML front door: `study_pages/11_intro_pyspark/index.html`.
- Created polished HTML study endpoints for start-here, 1000-foot view, Wipro bridge, and QA page.
- Repaired QA markdown duplicate opening block and preserved one canonical header/purpose section.
- Updated both Course 11 topic JSON mapResources from markdown targets to HTML targets.
- Lightly updated track `index.html` with improved Course 11 links.

## Final Course 11 Endpoint
- `study_pages/11_intro_pyspark/index.html`

## Map Endpoints
- `outputs/course_11_intro_pyspark_1000ft.html`
- `outputs/course_11_intro_pyspark_architecture_runtime.html`

## HTML Endpoints Created
- `study_pages/11_intro_pyspark/index.html`
- `study_pages/11_intro_pyspark/00_start_here.html`
- `study_pages/11_intro_pyspark/00_1000ft_pyspark_view.html`
- `study_pages/11_intro_pyspark/00_wipro_bridge.html`
- `study_pages/11_intro_pyspark/QA_01_1000ft_pyspark_opening.html`

## Markdown Sources Preserved
- Existing markdown files remain in place as source content and were not removed.

## Scope Safety Confirmations
- `tutorials` untouched.
- `Study_bubbles` engine untouched.

## Legacy Note
- `Course_01_Introduction_to_SQL` standalone folder remains legacy/inconsistent and should be handled in a future track-level normalization pass.
