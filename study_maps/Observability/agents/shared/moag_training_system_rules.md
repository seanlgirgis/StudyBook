# MOAG Training System Rules (Local Extract)

Source:
- `D:/users/shareuser/Downloads/MOAG_STUDYBUBBLE_TRAINING_SYSTEM_GUIDE_v2_05172026.2120.md`

Non-negotiable architecture:
- `study_maps/**/<Topic>` = learning product and course brain.
- `tutorials/**/<Topic>` = runnable labs and hands-on execution.
- `Study_bubbles/` = engine only.
- `scripts/` = shared command layer only.

Placement guardrails:
- Course home, study pages, Q&A, flashcards, glossary, safety notes, checklists -> `study_maps`.
- Runnable code, command walkthroughs, expected outputs, troubleshooting -> `tutorials`.
- Do not place real topic content under `Study_bubbles`.
- Do not hand-edit generated map HTML outputs.

Workflow rules:
- Teach first, design second, implement third, validate fourth.
- One focused cluster at a time; avoid oversized first-pass maps.
- Run placement audit before declaring completion.

Map/container rules:
- Active container is the folder containing `bubbles.ini`.
- Build from active container root with `bubbles build`.

Safety and positioning:
- Keep interview language accurate and overclaim-safe.
- Do not claim production ownership of tools not actually used.
