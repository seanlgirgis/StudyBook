# Topic Authoring Guide

Use this guide to design practical StudyBubble topics for Terraform, Power BI, Tableau, AWS, SQL, PySpark, Kubernetes, observability, and similar domains.

## Node Size Guidance
- `core`: major concept you must explain clearly.
- `support`: important supporting concept.
- `detail`: trap/tool/example/detail.

## Recommended Node Count
- `7 to 15`: first useful map.
- `20 to 40`: serious topic map.
- Avoid `70+` until topic structure is mature.

## Required Fields per Node
- `id`
- `label`
- `size`
- `group`
- `definition`

## Recommended Fields
- `whyItMatters`
- `safeSentence`
- `commonTrap`
- `interviewAnswer`
- `relatedQuestions`
- `note.summary`
- `note.image`
- `externalLinks`

## Study Path Guidance
- Create `2 to 5` paths.
- Each path should be a rehearsal lane (for example: fundamentals path, troubleshooting path, interview path).
- Keep path order intentional so it can be spoken or taught.

## Image Guidance
- Keep diagrams simple and focused.
- Raster images are resized by builder when oversized.
- SVG files are copied as-is.
- Prefer one useful diagram over many decorative images.

## Common Mistakes to Avoid
- Too many bubbles too early.
- Vague labels.
- Definitions that are too long.
- No study paths.
- No safe sentences.
- No common traps.

## Authoring Sequence
1. Draft concept groups and 7-15 nodes.
2. Add links showing real concept relationships.
3. Add 2-5 rehearsal paths.
4. Add safe interview language and traps.
5. Build, open, and refine layout.
