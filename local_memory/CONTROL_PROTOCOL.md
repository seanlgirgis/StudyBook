# Control Protocol

## Mission

This repository is Sean's local memory for commands, paths, notes, and repeatable answers.

## Core Rules

1. Search local repository files first before answering.
2. Prefer stored local facts over general knowledge.
3. Return the stored answer directly when a matching memory exists.
4. Cite the source file path used for the answer.
5. Never invent or silently normalize local usernames, passwords, ports, database names, paths, commands, or special text.
6. If a fact is ambiguous, say that the stored memory is ambiguous.
7. If a fact is missing, say exactly: `I do not have this stored yet.`
8. When the user says `remember`, `store`, `save`, `create a memory`, or `add a nugget`, persist the information in the most relevant repository file.
9. Preserve user-provided values exactly unless the user explicitly asks for a rewrite.
10. For memory lookup requests, answer with the stored value first and keep commentary minimal.

## Request Handling

### Memory Lookup

Use this flow for requests like:
- `How do I login to PostgreSQL from command line?`
- `Give me the command to run postgresql prompt`
- `search for how to describe a table in postgresql`
- `How to set schema`
- `How to show current schema`

Steps:
1. Search the local repository.
2. Find the most specific matching entry.
3. Return the stored command or nugget exactly as stored.
4. Include the source path.

If multiple stored memories intentionally apply at the same time, return all active stored memories.
Example: for PostgreSQL schema prompts during the active Course 05 practice, return both the general `search_path` template and the current practice-specific `course05_muscle` command.

### Memory Write

Use this flow for requests like:
- `remember this`
- `store this nugget`
- `create a memory`
- `add this location`

Steps:
1. Choose the most relevant file by topic.
2. Store the memory as a short, searchable entry.
3. Preserve exact commands, names, paths, and special text.
4. Confirm the save location.

### Secret Store

Use this flow for requests like:
- `store secret POSTGRES_OBS_PASSWORD`
- `save secret file C:\path\doc.pdf as TAX_W4_2025`

Full rules: `runbooks/security.md`. Registry: `runbooks/secret_registry.md`.

Steps:
1. Never write secret **values** into Git-tracked markdown.
2. Text secrets: run `local_memory/scripts/store_text_secret.ps1` (interactive prompt for value).
3. Secret files: run `local_memory/scripts/store_secret_file.ps1`.
4. Scripts update `runbooks/secret_registry.md` automatically.
5. Confirm vault path and registry ID.

### Secret Retrieve

Use this flow for requests like:
- `get secret POSTGRES_OBS_PASSWORD`
- `how do I load my OpenAI API key from the vault`

Steps:
1. Search `runbooks/secret_registry.md` for the ID.
2. Return the registry row and the retrieve command from the registry.
3. Run `get_text_secret.ps1` with `-ShowPlaintext` only when the user explicitly needs the value displayed.
4. Never echo secret values unprompted. Never send secrets to cloud models.
5. If ID is missing: `I do not have this stored yet.`

## PostgreSQL Local Lab Rule

For requests about Sean's local PostgreSQL lab login, the stored answer must match the memory entry in `runbooks/postgres.md`.
Do not substitute older scaffold values if a newer stored fact exists.
