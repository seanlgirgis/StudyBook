# DECISIONS

## Initial Decisions

- Static-first implementation.
- Data separated from viewer code.
- Single-file output is the active direction for current development.
- No React/npm/backend/database for now.
- Codex implements; ChatGPT StudyBubble orchestrates.

## Pivot Decisions (Iteration 2)

- BOA downgraded from first migration target to preserved reference prototype.
- Tiny 3-5-7 demo is the first real build target.
- Python builder is the repeatable engine.
- One topic data file per topic.
- External links open in a new browser tab.
- Child topic links stay inside StudyBubble.
- Linked image paths first; no base64 image embedding yet.

## Direction Cleanup Decisions (Post Iteration 5)

- Generated HTML is output, not source.
- Source files are maintained by humans in small readable pieces.
- Generated outputs are disposable and rebuildable after testing.
- Large generated single-file HTML should not be manually edited.
- Maintained source files are:
  - `viewer/bubble_viewer.html`
  - `viewer/bubble_viewer.css`
  - `viewer/bubble_viewer.js`
  - `topics/*.studybubble.json`
  - `src/study_bubbles/*.py`
- Generated outputs are:
  - `outputs/single_file/**`
  - `outputs/multifile/**` (historical/deprecated only)
- Primary acceptance target is single-file output:
  - `outputs/single_file/python_overview.html`
  - `outputs/single_file/pandas.html`
- Primary acceptance smoke should run by opening single-file pages directly from File Explorer.
- Single-file output embeds topic JSON data and should not require runtime `fetch()`.
- Parent/child navigation in single-file mode depends on sibling `.html` files existing in `outputs/single_file`.
- Multi-file output is historical/deprecated for current development and not part of active acceptance.
- Local HTTP server notes apply only to historical/deprecated multi-file testing, where `file://` can block `fetch()` loading local JSON.
- Single-file output should be assembled in organized sections:
  - metadata
  - styles
  - app shell
  - embedded topic data
  - JavaScript
  - build metadata

## ADR: Single-file-only active direction

Why:
- Easiest to open, share, and test by double-clicking a file.
- No local HTTP server requirement for primary acceptance.
- Reduces acceptance confusion between fetch-based and embedded-data paths.

Consequences:
- Parent/child topic navigation depends on sibling `.html` files existing in `outputs/single_file`.
- Topic JSON, CSS, and JS must be embedded into each generated single-file artifact for active acceptance.
- Multi-file output is deprecated for current development and is not an active acceptance criterion.

Reporting Guidance:
- Deprecated implementation residue may remain from earlier multi-file work.
- Do not treat deprecated residue as an active concern in normal task status reports.
- Mention deprecated residue only when:
  - it causes a failing test/runtime issue, or
  - the user explicitly requests a cleanup/removal task.
- Active acceptance remains direct-open `outputs/single_file/*.html`.
