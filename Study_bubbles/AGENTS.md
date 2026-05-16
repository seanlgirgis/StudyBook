# AGENTS.md

## Roles
- Codex is the implementor.
- ChatGPT StudyBubble is the architect and orchestrator.

## Implementor Rules
- Work step by step.
- Do not jump ahead.
- Run from the `study_bubbles` project folder.
- Initialize Python/test environment with `..\env_setter.ps1` from `study_bubbles`.
- Use relative paths inside the project.
- Preserve working artifacts before refactoring.
- Update project memory files after meaningful changes.
- Keep changes aligned to current iteration only.
- Keep one-topic-per-file discipline unless explicitly changed by architect direction.
- BOA artifact is preserved reference-only unless explicitly requested otherwise.
- Do not manually edit generated output as source; edit maintained source files and regenerate outputs.
- Current active direction is single-file-only acceptance for StudyBubble outputs.
- Do not use multi-file output, local HTTP server testing, or fetch-based topic loading as acceptance criteria unless architecture is explicitly reopened later.
- No React, npm, backend, database, or external dependencies for now.
- Tests are required before validators/builders are considered complete.
