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
- Single-file run mode: open pages directly from File Explorer (`file://`) with no `fetch()` requirement because topic data is embedded.
- Parent/child single-file navigation expectation: sibling `.html` topic files must exist under `outputs/single_file`.
- Deprecated/historical only:
  - multi-file output smoke checks
  - multi-file local HTTP-server checks
  - fetch-based topic loading checks
- Single-file structure smoke check for organized sections:
  - metadata
  - styles
  - app shell
  - embedded topic data
  - JavaScript
  - build metadata
