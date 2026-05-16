# DESIGN

## Intended Simple Architecture

1. Topic data layer
- One topic is normally represented by one `.studybubble.json` file.
- Example: `topics/tiny_capacity_demo.studybubble.json`.

2. Validator layer (Python)
- Validates topic schema, references, and field integrity.

3. Builder layer (Python)
- Repeatable engine that transforms topic data into deployable static artifacts.
- Codex prompting is not the builder; Python code is the builder.
- Active acceptance mode is single-file output.

4. Viewer source layer
- Maintained source files for UI shell and behavior.
- Source files remain small and readable.

5. Output layer
- Builder-generated single-file outputs for active acceptance.
- Multi-file outputs are deprecated historical/debug artifacts.
- Generated files are artifacts, not hand-maintained source.

## Maintained Source vs Generated Output

Maintained source:
- `topics/*.studybubble.json`
- `viewer/bubble_viewer.html`
- `viewer/bubble_viewer.css`
- `viewer/bubble_viewer.js`
- `src/study_bubbles/*.py`

Generated output:
- `outputs/single_file/**`
- `outputs/multifile/**` (deprecated historical/debug only)

Generated output can be replaced by newer validated builds.

## Output Targets

Single-file output (active):
- `outputs/single_file/<topic_id>.html`
- Single-file structure target:
  - metadata
  - styles
  - app shell
  - embedded topic data
  - JavaScript
  - build metadata
- Parent/child navigation uses sibling topic `.html` files.

Deprecated/historical:
- `outputs/multifile/**` may remain in repo for reference/debug only.
- It is not part of active acceptance testing.

## BOA Prototype Role
`BOA_Terminology_Bubble_Map_v3.html` is a preserved reference prototype for behavior patterns (filters, search, minimap, side panel, study paths, drag mode, fit/reset).
It is not the first required migration target.

## First Build Path
- First real target: `tiny_capacity_demo.studybubble.json`.
- Growth stages: 3 bubbles -> 5 bubbles -> 7 bubbles.
- Purpose: prove data-driven growth without manual HTML surgery.
