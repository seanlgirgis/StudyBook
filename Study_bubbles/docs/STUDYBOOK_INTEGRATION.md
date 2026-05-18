# StudyBook Integration

StudyBubble is a reusable visual study-map builder for StudyBook topics.

## Role in StudyBook
- Engine location: `D:\Workarea\StudyBook\Study_bubbles`
- Recommended topic workspace location: `D:\Workarea\StudyBook\study_maps`
- Real project output location: `study_maps\<ProjectName>\outputs\`
- Authoring rule: one topic = one `*.studybubble.json` file.
- Container rule: any folder containing `bubbles.ini` is a StudyBubble container.

## Typical Workflow
1. Create or open a project container, for example `study_maps\TerraForm\`.
2. Ensure container structure exists:
   - `bubbles.ini`
   - `topics\`, `layouts\`, `outputs\`, `assets\`
3. Validate engine tests from `Study_bubbles`:
```powershell
..\env_setter.ps1
cd Study_bubbles
python -m pytest -q
```
4. Build from the container folder:
```powershell
cd ..\study_maps\TerraForm
..\..\scripts\bubbles.ps1 build
```
5. Open generated HTML directly from File Explorer.

## Fail-Fast Container Rule
When running container build tooling from a folder without `bubbles.ini`, fail fast with:

```text
ERROR: No bubbles.ini found in the current folder.
Run this command from a StudyBubble project folder, or create bubbles.ini first.
```

## Layout Export/Import Workflow
1. Open generated HTML.
2. Turn on `Drag Mode` and adjust positions.
3. Click `Export Layout`.
4. Use one-command sync/rebuild to import layout JSON and regenerate matching pages.

## One-Command Sync/Rebuild
Run from a container folder (preferred) or from engine demo root:
```powershell
..\..\scripts\bubbles.ps1 sync-layout
```
What it does:
- scans configured downloads folder for `*.layout.json`
- updates `<active-container>\layouts\<topicId>.layout.json` (with backup)
- rebuilds HTML for updated topics in the active container

## Manual Smoke Checklist
1. Open generated topic HTML directly.
2. Confirm map renders and sidebar loads.
3. Confirm search/filter/reset still work.
4. Confirm study paths are clickable/highlight links.
5. Confirm parent/child navigation works when present.
6. Confirm map-level tutorials/labs/neighbor-map links are in **Map Resources** (not forced into random bubble cards).
7. Confirm no serious runtime console errors.

## Authoring Rule: Bubble vs Map Links
- Bubble links are for the selected concept details.
- Map resources are for whole-map learning links (tutorials, labs, setup, glossary, parent/neighbor/next maps).
- Do not force whole-map resources into random bubble cards.

## When to Return to Study_bubbles for Fixes
Return to engine project work when you need:
- viewer behavior fixes (rendering, navigation, controls)
- builder/validator fixes
- layout sync/import improvements
- image handling updates
- schema/extensions for authoring needs
