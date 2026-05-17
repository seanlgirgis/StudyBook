# StudyBook Integration

StudyBubble is a reusable visual study-map builder for StudyBook topics.

## Role in StudyBook
- Engine location: `D:\Workarea\StudyBook\Study_bubbles`
- Recommended topic workspace location: `D:\Workarea\StudyBook\study_maps`
- Generated output location: `Study_bubbles\outputs\single_file`
- Authoring rule: one topic = one `*.studybubble.json` file.

## Typical Workflow
1. Create a topic file in `Study_bubbles\topics\` (or draft in `study_maps` and copy into `topics`).
2. Validate/build from `Study_bubbles`:
```powershell
..\env_setter.ps1
python -m pytest -q
python -m src.study_bubbles.build_topic --topic topics\<topic_id>.studybubble.json --out outputs\single_file\<topic_id>.html --mode single-file
```
3. Open generated HTML directly from File Explorer.

## Layout Export/Import Workflow
1. Open generated HTML.
2. Turn on `Drag Mode` and adjust positions.
3. Click `Export Layout`.
4. Use one-command sync/rebuild to import layout JSON and regenerate matching pages.

## One-Command Sync/Rebuild
Run from `Study_bubbles`:
```powershell
python tools\sync_layouts_and_rebuild.py
```
What it does:
- scans configured downloads folder for `*.layout.json`
- updates `layouts\<topicId>.layout.json` (with backup)
- rebuilds `outputs\single_file\<topicId>.html` using `--layout`

## Manual Smoke Checklist
1. Open generated topic HTML directly.
2. Confirm map renders and sidebar loads.
3. Confirm search/filter/reset still work.
4. Confirm study paths are clickable/highlight links.
5. Confirm parent/child navigation works when present.
6. Confirm no serious runtime console errors.

## When to Return to Study_bubbles for Fixes
Return to engine project work when you need:
- viewer behavior fixes (rendering, navigation, controls)
- builder/validator fixes
- layout sync/import improvements
- image handling updates
- schema/extensions for authoring needs
