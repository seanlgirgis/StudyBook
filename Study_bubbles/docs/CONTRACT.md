# CONTRACT

## Topic File Rule
- One topic should normally be represented by one data file.
- File naming pattern: `<topic_id>.studybubble.json`.

## Future Topic Schema (Draft)

Top-level fields:
- `id`
- `title`
- `subtitle`
- `parentTopic`
- `groups`
- `nodes`
- `links`
- `paths`

## Node Shape (Planned)
Each node should support:
- `id`
- `label`
- `size`
- `group`
- `definition`
- `whyItMatters`
- `safeSentence`
- `commonTrap`
- `interviewAnswer`
- `relatedQuestions`
- `note.summary`
- `note.image.src`
- `note.image.caption`
- `externalLinks`
- `childTopics`

## Link Behavior Distinction
- `externalLinks`: open outside StudyBubble, normally in a new browser tab.
- `childTopics`: navigate to another StudyBubble topic in the same viewer/tab.
- `parentTopic`: enables return from child topic to parent map.
- Active output contract: parent/child navigation in current direction resolves to sibling single-file topic pages (`outputs/single_file/*.html`).

## Validation Expectations (Planned)
- `id`, `title`, `nodes`, and `links` are required.
- Top-level `id` must match the file topic identity.
- `parentTopic` is optional but must reference a valid topic id format when present.
- Node `id` values must be unique.
- Node `group` must exist in `groups`.
- Node `size` must be within allowed enum/range.
- Link endpoints must reference existing node ids.
- `paths` must reference existing node ids in valid order.
- `externalLinks` entries must include valid URL format and display text.
- `childTopics` entries must include target topic ids (and optional labels).
- `note.summary` is optional short text.
- `note.image.src` uses linked image paths/URLs (no base64 embedding in current direction).
- `note.image.caption` is optional human-readable caption.
- `commonTrap` is optional string.
- `interviewAnswer` is optional string.
- `relatedQuestions` is optional list of strings.

## Active Direction Constraint
- Current development acceptance is single-file-only.
- Topic data is embedded in generated topic HTML.
- Runtime `fetch("topic.studybubble.json")` is not part of active acceptance criteria.
- Multi-file output is deprecated for current acceptance and treated as historical/debug only.
