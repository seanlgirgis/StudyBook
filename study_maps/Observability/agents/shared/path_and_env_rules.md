# Path And Environment Rules

Path convention:
- Prefer relative paths within the active project/container.
- Use absolute paths only when disambiguation is required.

Python/setup bootstrap:
1. `cd D:\Workarea\StudyBook`
2. `.\env_setter.ps1`
3. Return to target container, for example:
   - `cd .\study_maps\Observability`

StudyBubble build pattern:
- From container root (folder with `bubbles.ini`):
  - `bubbles build`
- Optional layout sync flow:
  - `bubbles sync-layout`
  - `bubbles build`

Execution guardrails:
- Do not rely on deep `..\..\` command chains unless debugging fallback.
- Validate links after structural changes.
- Keep generated outputs machine-generated; edit sources then rebuild.
