# GROK_RUNBOOK.md

Operational runbook for Grok Build sessions in `local_memory`.

## Project Root

```
D:\Workarea\StudyBook\local_memory
```

Parent StudyBook repo root:

```
D:\Workarea\StudyBook
```

## Purpose

Small local memory / personal notes vault for things Sean wants to remember:

- Commands and shell one-liners
- Project paths and file locations
- Login steps and connection details
- Learning notes and repeatable how-to answers
- Selected captured reference material

**Architecture:** The repository itself is the memory system — markdown-first, instruction-driven writes. No database, vector store, or app layer. See `LOCAL_MEMORY_HANDOFF.md` for full design decisions.

## Storage Layout

| Location | What goes here |
|----------|----------------|
| `runbooks/` | Main domain memory (postgres, sql, datacamp, rag_foundation, questions_cache, etc.) |
| `locations/` | Project paths and important file URLs |
| `chat_captures/` | External references — `original_reference/` (raw) + `memory/` (summaries, notes, provenance) |
| `agents/shared/` | Agent operating state (not user memories) |
| `GROK_*.md` | Grok-specific notes — kept separate from shared/canonical memory |
| `LOCAL_MEMORY_HANDOFF.md` | Codex design handoff — how the vault works |

**Not in this project:** database, vector storage, embedding pipeline, encryption layer, programmatic memory writers.

## Launch Grok Build

Location-agnostic launcher (run from anywhere):

```powershell
pwsh -ExecutionPolicy Bypass -File "D:\start_grok_local_memory.ps1"
```

The script can live anywhere; it defaults to `D:\Workarea\StudyBook` and `...\local_memory`.

What it does:

1. Opens a new PowerShell window titled `grok_local_memory` (use `-NoNewWindow` to run in the current window)
2. Runs `D:\Workarea\StudyBook\env_setter.ps1`
3. Sets working directory to `local_memory`
4. Starts `grok --cwd <local_memory>` with bootstrap rules for GROK agent files

## Environment Setup

### Python / venv activation (required before Python commands)

Always run this first in PowerShell:

```powershell
D:\Workarea\StudyBook\env_setter.ps1
```

What it does:

- Bootstraps the StudyBook environment via `scripts\env\env_core.ps1`
- Activates the project-local Python venv
- Sets `JAVA_HOME` to Microsoft JDK 17 (for PySpark compatibility)
- Adds `D:\Workarea\StudyBook\scripts` to `PATH`
- Prints machine name, venv path, Python path, and secrets-loaded status

Optional flags (rarely needed):

```powershell
D:\Workarea\StudyBook\env_setter.ps1 -SkipVenvActivation
D:\Workarea\StudyBook\env_setter.ps1 -NonInteractive
```

### Verify Python after activation

```powershell
python --version
where.exe python
```

## Memory Lookup Workflow

1. Search `runbooks/`, `locations/`, `chat_captures/`, and `GROK_MEMORY.md`.
2. Return the stored value exactly as written.
3. Cite the source file path.
4. If not found, say: `I do not have this stored yet.`

## Memory Write Workflow

Triggered by: `remember`, `store`, `save`, `create a memory`, `add a nugget`.

1. Search the repository first (avoid duplicates).
2. Choose the most relevant existing file by topic (see Storage Layout above).
3. Store as a short, searchable entry (Q&A with tags preferred per `MEMORY_RULES.md`; runbook sections also used).
4. Preserve exact commands, names, paths, ports, database names, and special text.
5. Confirm the save location.

## Sensitive Data

See `runbooks/security.md` and `runbooks/secret_registry.md`.

- **Text secrets:** `secrets/vault.secrets.enc.json` (gitignored, AES-encrypted via StudyBook seed/passphrase).
- **Secret files:** `secrets/files/<ID>/` (gitignored; mirrored to `V:\StudyBook_ignored_backup\` via `gitqall.ps1`).
- **Registry:** pointers only in `runbooks/secret_registry.md`.
- **Store:** `scripts/store_text_secret.ps1`, `scripts/store_secret_file.ps1`.
- **Retrieve:** `scripts/get_text_secret.ps1`; never put values in Git markdown.

## Key Repository Files

| Path | Contents |
|------|----------|
| `index.md` | Top-level index |
| `CONTROL_PROTOCOL.md` | Primary agent operating rules |
| `MEMORY_RULES.md` | Memory lookup/write rules |
| `runbooks/postgres.md` | PostgreSQL local lab |
| `runbooks/sql.md` | SQL nuggets |
| `runbooks/rag_foundation.md` | RAG foundation setup |
| `runbooks/questions_cache.md` | Repeated-question cache |
| `locations/project_paths.md` | Project directory paths |
| `locations/important_files.md` | Important file locations |
| `agents/shared/context_index.md` | Agent context map |
| `LOCAL_MEMORY_HANDOFF.md` | Codex design handoff — vault architecture and write model |
| `docs/planning/PLANNING_INDEX.md` | Planning lifecycle — requirements, analysis, architecture, iterations |
| `docs/adr/ADR-INDEX.md` | Accepted architecture decisions |

## GROK_ Files

| File | Role |
|------|------|
| `GROK_AGENTS.md` | Grok agent rules and startup order |
| `GROK_RUNBOOK.md` | This file |
| `GROK_CURRENT_STATE.md` | Active session state |
| `GROK_MEMORY.md` | Grok-specific stored notes |