# local_memory Handoff

Generated from repository contents on 2026-06-15.

## What this project is

`local_memory` is a local, repository-based memory vault for Sean. It is not a database-backed app and it is not using a separate memory service. The repository itself is the memory system.

Its stated purpose across the repo is to store:

- commands
- project paths
- login steps
- file locations
- learning notes
- repeatable how-to answers
- selected captured reference material

Primary source files:

- `README.md`
- `CONTROL_PROTOCOL.md`
- `MEMORY_RULES.md`

## The short answer: how memories are being saved

Memories are being saved directly into files inside this repository, mostly as Markdown.

The dominant storage pattern is:

- topic-based runbooks in `runbooks/`
- location/path references in `locations/`
- agent operating context in `agents/shared/`
- assistant-specific notes in `GROK_*.md`
- captured external reference material in `chat_captures/`

There is no evidence in this repository of:

- a database
- vector storage for this project
- automatic embedding/indexing pipeline
- encryption layer
- secret manager integrated into `local_memory`
- application code that writes memories programmatically

The write behavior is instruction-driven: when the user says things like `remember`, `store`, `save`, `create a memory`, or `add a nugget`, the agent is supposed to place that information into the most relevant repository file.

Source basis:

- `CONTROL_PROTOCOL.md`
- `MEMORY_RULES.md`
- `AGENTS.md`
- `agents/shared/context_index.md`

## Where the memories live

Project root:

```text
D:\Workarea\StudyBook\local_memory
```

### Canonical memory files

#### `runbooks/`

These are the main domain memory files.

- `runbooks/postgres.md`
  Stores PostgreSQL login details, `psql` usage, shell escapes inside `psql`, and SQL-file execution notes.
- `runbooks/sql.md`
  Stores SQL nuggets like `search_path`, schema inspection, and named-window explanations.
- `runbooks/windows.md`
  Stores Windows shell notes such as `cls`.
- `runbooks/datacamp.md`
  Stores DataCamp workflow memories, especially screenshot extraction commands and script usage.
- `runbooks/rag_foundation.md`
  Stores a large operational memory for the RAG foundation project, including paths, environment setup, and secret-handling notes for that separate project.
- `runbooks/questions_cache.md`
  Stores repeated-question answers in direct Q/A form for fast reuse.
- `runbooks/security.md`
  System of record for the secret vault: encryption, gitignore, E: backup, store/retrieve scripts, agent rules.
- `runbooks/secret_registry.md`
  Pointer table for stored secrets (IDs, purpose, load commands — no values).
- `runbooks/docker.md`
  Exists but is currently empty.
- `runbooks/git.md`
  Exists but is currently empty.

#### `locations/`

- `locations/important_files.md`
  Stores important file URLs/locations.
- `locations/project_paths.md`
  Exists but is currently empty.

#### `chat_captures/`

This folder stores richer captured memory artifacts. Right now there is one YouTube capture:

```text
chat_captures\youtube\BqBsT6ZjurA\
```

It contains two groups of files:

- `original_reference/`
  Raw reference material such as transcripts, subtitles, thumbnail, description, source URL, and metadata JSON.
- `memory/`
  Derived memory artifacts such as summaries, memory notes, provenance, and an availability history JSONL file.

This is the clearest example in the repo of memory being stored as both raw source material and interpreted notes.

#### Agent and control files

These files do not store user memories in the same way as `runbooks/`, but they do store operating state and instructions:

- `AGENTS.md`
- `CONTROL_PROTOCOL.md`
- `MEMORY_RULES.md`
- `agents/shared/context_index.md`
- `agents/shared/open_loops.md`
- `agents/shared/approval_matrix.md`
- `agents/shared/command_allowlist.md`
- `agents/shared/agent_status.md`
- `agents/shared/decision_log.md`
- `agents/shared/parking_lot.md`
- `docs/adr/ADR-INDEX.md`

#### Grok-specific files

These are explicitly separated so Grok notes do not mix with shared/canonical memory:

- `GROK_AGENTS.md`
- `GROK_RUNBOOK.md`
- `GROK_CURRENT_STATE.md`
- `GROK_MEMORY.md`

## How the project wants memory writes to work

The intended write model is simple and manual:

1. Search the repository first.
2. Choose the most relevant existing file by topic.
3. Save the new memory as a short, searchable entry.
4. Preserve exact values for commands, usernames, paths, ports, database names, and special text.
5. Confirm the save location.

There are two slightly different formatting conventions present:

- `MEMORY_RULES.md` says to store new information as question-and-answer entries and use tags.
- `CONTROL_PROTOCOL.md` says to persist in the most relevant repository file and preserve values exactly.

In practice, the repo currently uses a mix of formats:

- question/answer entries
- runbook sections with commands and notes
- location entries
- captured reference folders with summaries and provenance

## How I operate in this project

The repo instructs me to operate repository-first, not memory-first.

My required operating behavior here is:

1. Read startup control files before doing work.
2. Treat repository files as the source of truth.
3. Search local files before answering.
4. Prefer stored local facts over general knowledge.
5. Return stored answers directly for lookup-style questions.
6. Cite the source file path used.
7. Never invent or silently normalize local usernames, passwords, ports, database names, paths, commands, or special text.
8. If a fact is ambiguous, say it is ambiguous.
9. If a fact is missing, say exactly: `I do not have this stored yet.`
10. Execute one scoped task per run.
11. Park unrelated findings in `agents/shared/parking_lot.md`.

The startup order in `AGENTS.md` requires reading:

1. `CONTROL_PROTOCOL.md`
2. `agents/shared/context_index.md`
3. `agents/shared/open_loops.md`
4. `agents/shared/approval_matrix.md`
5. `agents/shared/command_allowlist.md`
6. `docs/adr/ADR-INDEX.md`
7. `agents/shared/pending_task.md` if present
8. `agents/shared/agent_status.md` if present
9. `agents/shared/decision_log.md` if present

Important approval rules:

- allowed without extra approval: reading/searching repo files, updating markdown memory entries requested by the user, creating missing agent-control files in this repo
- pause and clarify: deleting memory, rewriting an existing stored fact when replacement is unclear, changing files outside this repo

Command preferences:

- `rg` for search
- `rg --files` for file listing
- `Get-Content -Raw` for file reads
- `tree /F` for tree output

## What is currently stored

### PostgreSQL memory

`runbooks/postgres.md` stores:

- local PostgreSQL login command
- known host/port/user/database values
- special text `obs_pass`
- how to run shell commands from inside `psql`
- how to run a SQL file from inside `psql`

This means at least some connection-related information is intentionally stored in the repo as plain text.

### SQL memory

`runbooks/sql.md` stores:

- general `SET search_path TO <SchemaA, SchemaB>;`
- current practice override `SET search_path TO intermediate_sql, public;`
- `SHOW search_path;`
- table structure query via `information_schema.columns`
- a long explanation of PostgreSQL named windows

### Windows memory

`runbooks/windows.md` stores:

- `cls`

### DataCamp workflow memory

`runbooks/datacamp.md` stores:

- `PySceneDetect` commands
- threshold/scene-detection notes
- multi-file extraction loop
- `extract_slide_frames.py` usage
- expected outputs and workflow notes

### RAG foundation memory

`runbooks/rag_foundation.md` stores a large amount of operational knowledge for another project, including:

- foundation path
- current lab path
- Python version choice
- venv path
- shared library path
- activation command
- test commands
- model name
- architecture notes
- backup guidance
- explicit mention that the OpenAI API key is stored in a plain-text PowerShell file outside Git

### Repeated question cache

`runbooks/questions_cache.md` stores direct answers for likely repeat questions, including:

- how to load the RAG environment
- how to get to the RAG code folder
- where the shared library lives
- which Coursera program is current
- which program to look at next

### Important file locations

`locations/important_files.md` stores:

- local file URL for a SQL Windowing Field Guide HTML file
- local file URL for a Course 05 practice SQL workbook

### Chat capture memory

The YouTube capture currently stores:

- source metadata
- raw transcripts/subtitles
- thumbnail
- source URL
- summaries in English and Arabic
- memory notes in English and Arabic
- provenance notes
- availability history JSONL

This indicates the project can also function as a structured archive for external references that the user wants remembered.

## Sensitive information: current state

**System of record:** `runbooks/security.md`  
**Pointer registry:** `runbooks/secret_registry.md`

### Implemented secret vault (2026-06-15)

| Layer | Location | In Git? |
|-------|----------|---------|
| Operational memory | `runbooks/`, `locations/` | Yes |
| Text secrets (encrypted) | `secrets/vault.secrets.enc.json` | No |
| Secret documents | `secrets/files/<ID>/` | No |
| Pointers only | `runbooks/secret_registry.md` | Yes |
| E: backup mirror | `V:\StudyBook_ignored_backup\current\` | No |

**Encryption:** Reuses StudyBook seed file (`config/secrets/.local/studybook.secret.seed.dpapi.json`) or `STUDYBOOK_SECRET_PASSPHRASE`. AES-256-CBC + PBKDF2-SHA256.

**Scripts:** `local_memory/scripts/store_text_secret.ps1`, `get_text_secret.ps1`, `list_text_secrets.ps1`, `remove_text_secret.ps1`, `store_secret_file.ps1`

**Backup:** `C:\scripts\gitqall.ps1` → `StudyBook/scripts/backup_gitignored_to_e.ps1` mirrors git-ignored `local_memory/secrets/` to encrypted `V:` drive.

**Agent rules:** In `CONTROL_PROTOCOL.md` (Secret Store / Secret Retrieve sections) and `GROK_AGENTS.md`.

### Classification model

- **Safe in repo:** commands, paths, notes, learning summaries, file locations, non-secret config, public URLs
- **Caution in repo:** usernames, hostnames, database names, course progress
- **Keep out of repo (use vault):** passwords, API keys, tokens, recovery codes, private keys, secret documents

### Legacy / not yet migrated

- `runbooks/postgres.md` still has plain-text special token `obs_pass` (candidate for vault migration)
- `runbooks/rag_foundation.md` references OpenAI key in `set_env.ps1` outside Git (plain text on disk)

### Not implemented

- Password-manager integration
- OS Credential Manager integration
- Automatic redaction in chat
- Per-chunk sensitivity tags in embeddings (planned in `docs/planning/`)

## What this project is not

Based on the repo contents, `local_memory` is not currently:

- a web app
- a service
- an API
- a database system
- a vector memory engine
- an auto-sync knowledge base

It is a structured folder of local files plus operating rules for assistants.

## Gaps and inconsistencies I noticed

- `runbooks/docker.md` is empty.
- `runbooks/git.md` is empty.
- `locations/project_paths.md` is empty.
- `docs/adr/ADR-INDEX.md` says no ADRs recorded yet.
- `MEMORY_RULES.md` prefers Q/A entries, but some runbooks use broader narrative formats.
- Legacy plain-text tokens (e.g. `obs_pass`) not yet migrated to the secret vault.
- There is no documented schema for `chat_captures/`, though the current example is fairly structured.

## Best single-sentence description

`local_memory` is a local markdown-first memory vault where assistants are instructed to search the repo first, answer from stored facts exactly, and save new memories into topic-specific files inside the repository.

## File inventory snapshot

Current tracked files visible during this handoff:

```text
AGENTS.md
CONTROL_PROTOCOL.md
GROK_AGENTS.md
GROK_CURRENT_STATE.md
GROK_MEMORY.md
GROK_RUNBOOK.md
MEMORY_RULES.md
README.md
index.md
agents/shared/agent_status.md
agents/shared/approval_matrix.md
agents/shared/command_allowlist.md
agents/shared/context_index.md
agents/shared/decision_log.md
agents/shared/open_loops.md
agents/shared/parking_lot.md
chat_captures/youtube/BqBsT6ZjurA/memory/availability_history.jsonl
chat_captures/youtube/BqBsT6ZjurA/memory/memory_note_ar.md
chat_captures/youtube/BqBsT6ZjurA/memory/memory_note_en.md
chat_captures/youtube/BqBsT6ZjurA/memory/source_provenance.md
chat_captures/youtube/BqBsT6ZjurA/memory/summary_ar.md
chat_captures/youtube/BqBsT6ZjurA/memory/summary_en.md
chat_captures/youtube/BqBsT6ZjurA/original_reference/description.txt
chat_captures/youtube/BqBsT6ZjurA/original_reference/source_url.txt
chat_captures/youtube/BqBsT6ZjurA/original_reference/subtitles_ar.md
chat_captures/youtube/BqBsT6ZjurA/original_reference/subtitles_en.md
chat_captures/youtube/BqBsT6ZjurA/original_reference/thumbnail.jpg
chat_captures/youtube/BqBsT6ZjurA/original_reference/transcript_ar.md
chat_captures/youtube/BqBsT6ZjurA/original_reference/transcript_en.md
chat_captures/youtube/BqBsT6ZjurA/original_reference/video_metadata.info.json
docs/adr/ADR-INDEX.md
locations/important_files.md
locations/project_paths.md
runbooks/datacamp.md
runbooks/docker.md
runbooks/git.md
runbooks/postgres.md
runbooks/questions_cache.md
runbooks/security.md
runbooks/secret_registry.md
runbooks/rag_foundation.md
runbooks/sql.md
runbooks/windows.md
```

## Source files used for this handoff

- `AGENTS.md`
- `CONTROL_PROTOCOL.md`
- `README.md`
- `MEMORY_RULES.md`
- `index.md`
- `agents/shared/context_index.md`
- `agents/shared/open_loops.md`
- `agents/shared/approval_matrix.md`
- `agents/shared/command_allowlist.md`
- `agents/shared/agent_status.md`
- `agents/shared/decision_log.md`
- `docs/adr/ADR-INDEX.md`
- `GROK_AGENTS.md`
- `GROK_CURRENT_STATE.md`
- `GROK_MEMORY.md`
- `GROK_RUNBOOK.md`
- `runbooks/postgres.md`
- `runbooks/sql.md`
- `runbooks/windows.md`
- `runbooks/datacamp.md`
- `runbooks/rag_foundation.md`
- `runbooks/questions_cache.md`
- `locations/important_files.md`
- `chat_captures/youtube/BqBsT6ZjurA/memory/source_provenance.md`

