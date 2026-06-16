# GROK_MEMORY.md

Grok-specific stored notes and session memories for `local_memory`.

For shared domain memories, prefer the canonical runbooks (`runbooks/`) and `locations/` files. Use this file for Grok Build session context that should not mix with Claude/ChatGPT artifacts.

---

## local_memory Vault — Design & Write Model (summary)

**Source:** `LOCAL_MEMORY_HANDOFF.md` (Codex handoff, 2026-06-15)

**Q:** What is `local_memory`?

**A:** A local, repository-based memory vault. The repo itself is the memory system — not a database, app, vector store, or separate memory service. Markdown-first, instruction-driven writes.

**Tags:** `local_memory`, `architecture`, `design`

---

**Q:** How are memories saved in `local_memory`?

**A:** Directly into Markdown files when the user says `remember`, `store`, `save`, `create a memory`, or `add a nugget`. The agent picks the most relevant file by topic, writes a short searchable entry, preserves exact values, and confirms the save location.

**Write flow:** search first → pick file by topic → short entry → preserve exact values → confirm location.

**Tags:** `local_memory`, `write-model`, `memory`

---

**Q:** Where do different types of memories go?

**A:**

| Location | Contents |
|----------|----------|
| `runbooks/` | Main domain memory (postgres, sql, datacamp, rag_foundation, questions_cache, windows, docker, git) |
| `locations/` | Project paths (`project_paths.md`) and important file URLs (`important_files.md`) |
| `chat_captures/` | External references — `original_reference/` (raw) + `memory/` (summaries, notes, provenance) |
| `agents/shared/` | Agent operating state, not user memories |
| `GROK_*.md` | Grok-specific notes, separated from shared/canonical memory |

**Tags:** `local_memory`, `storage`, `paths`

---

**Q:** How should agents operate in `local_memory`?

**A:** Repository-first. Search local files before answering. Return stored facts exactly. Cite source path. Never invent or normalize local credentials/paths/commands. If missing: `I do not have this stored yet.` One scoped task per run. Park side findings in `agents/shared/parking_lot.md`.

**Tags:** `local_memory`, `agent-rules`, `operating-model`

---

**Q:** What is the sensitive-data practice in `local_memory`?

**A:** Secret vault implemented. System of record: `runbooks/security.md`. Text secrets in gitignored `secrets/vault.secrets.enc.json` (AES, StudyBook seed). Documents in `secrets/files/<ID>/`. Pointers in `runbooks/secret_registry.md`. E: backup via `gitqall.ps1`. Store with `scripts/store_text_secret.ps1`; retrieve with `get_text_secret.ps1`. Never put values in Git markdown.

**Tags:** `local_memory`, `security`, `sensitive-data`, `vault`

---

**Q:** What is `local_memory` NOT?

**A:** Not a web app, service, API, database, vector memory engine, or auto-sync knowledge base. It is a structured folder of local files plus operating rules for assistants.

**Tags:** `local_memory`, `architecture`, `scope`

---

**Q:** Where is the full vault design documented?

**A:** `LOCAL_MEMORY_HANDOFF.md` — Codex handoff covering architecture, file inventory, current stored content, gaps, and suggested sensitive-data policy.

**Tags:** `local_memory`, `handoff`, `reference`

---

## Collaboration Preference — Honest Opinion (2026-06-15)

**Q:** How should Grok respond when Sean asks for an opinion?

**A:** Give an honest assessment, not blind agreement. Push back when there are gaps, risks, or simpler alternatives. Do not implement something questionable just because Sean suggested it. Separate **recommendation** from **requested action**. If Sean chooses a path after hearing tradeoffs, execute that choice.

**Tags:** `sean`, `collaboration`, `agent-behavior`

---

## Planning Artifacts Location (2026-06-15)

**Q:** Where do requirements, analysis, architecture, planning, and development thinking go?

**A:** Under `docs/planning/`:

| Subfolder | Purpose |
|-----------|---------|
| `iterations/` | Dated exploratory thinking (may be wrong) |
| `requirements/` | What we need, constraints |
| `analysis/` | Options and tradeoffs |
| `architecture/` | Proposed designs (pre-ADR) |
| `development/` | Phases and implementation order |

Lifecycle: iteration → requirements → analysis → architecture → development → **ADR** (`docs/adr/`) → **runbooks** (operational). Index: `docs/planning/PLANNING_INDEX.md`.

First iteration saved: `docs/planning/iterations/2026-06-15_tiered_second_brain_enhancement.md`.

**Tags:** `local_memory`, `planning`, `architecture`

---

## Full Context Export (reference)

**Source:** `sean_girgis_memory_context_export_2026-06-15.md`  
**Exported:** 2026-06-15

That file is the complete durable context export (~24 sections). Use it for full detail on job-search history, course progress, project paths, RemNote rules, library modules, and standing constraints. Treat time-sensitive items (employment, interviews, compensation, course status) as **verify before use**.

---

## Sean Girgis — Key Profile (summary)

Loaded from `sean_girgis_memory_context_export_2026-06-15.md` on 2026-06-15.

### Identity

- **Name:** Sean Girgis
- **Email:** seanlgirgis@gmail.com
- **Handle:** @seanlgirgis
- **DOB:** June 21, 1968 (age ~57–58)
- **Location:** Richardson, Texas (Dallas–Fort Worth area)
- **Work location preference:** Remote preferred; Dallas, Houston, Austin, NYC also acceptable
- **Horizon:** Plans to work at least 15 more years; near-term income need alongside longer-term technical development

### How to Work With Sean

- Teach in **very small, explicit, bite-sized steps** — one concept or action at a time
- **No large lesson dumps**; study responses usually under one A4 page
- **Interactive rhythm:** small explanation → tiny task → wait for response
- Make hidden assumptions explicit; revisit concepts from multiple angles
- ADD affects how he learns and organizes information
- Theory and meaning first; explain code clearly, don't just list it
- Preserve **exact canonical filenames**; no `_updated` / `_final` / `_new` suffixes
- Prefer relative links, consolidated digests, and continuity docs (`README.md`, `MEMORY.md`, `CURRENT_STATE.md`, `RUNBOOK.md`)
- Sean runs commands manually; Codex-ready prompts need exact paths, files, validation commands, scope limits
- Reusable mechanics go in **shared libraries**; generalize → test → example → replace duplicates

### Career Profile

- **Title:** Senior Data Engineer, 20+ years enterprise experience
- **Recent tenure:** ~8 years at Citigroup; left near end of 2025
- **Primary targets:** Python, PySpark, SQL, ETL/ELT, AWS, data engineering, cloud data platforms, forecasting, RAG/AI apps, vector DBs
- **Secondary strengths:** Observability/APM (Dynatrace, AppMon, Splunk), performance engineering, CI/CD, IaC, ECS, FastAPI, Kubernetes/EKS, S3, cost optimization
- Prefers **practical data engineering and application building** over deep ML research

### Current Employment (verify status)

- **Employer:** LTIMindtree (joined ~May 28–29, 2026)
- **Client context:** Bank of America work
- **Rules:** No invoicing through own LLC during LTM tenure; no dual employment
- **Note:** BOA/LTM work materials live in a separate private repository — out of scope for `local_memory`

### Active Technical Focus (priority order)

1. Developing AI application skills (OpenAI API, function calling, structured output)
2. Coursera IBM RAG specialization (`crs_` prefix under DataCamp root)
3. DataCamp consolidation and certification-prep artifacts
4. RAG Application Builder Foundation
5. Expand shared `rag_foundation` library (`D:\py_libs\rag_foundation`)
6. Add observability, token/cost/budget tracking to AI architecture
7. Maintain employability in Python, PySpark, AWS, ETL, observability
8. RemNote for long-term spaced-repetition review

### Key Project Paths

| Project | Path |
|---------|------|
| StudyBook / DataCamp root | `D:\Workarea\StudyBook\study_maps\DataCamp` |
| RAG foundation | `...\skill_tracks\crs_rag_for_generative_ai_applications\foundation\rag_application_builder_foundation` |
| Shared Python library | `D:\py_libs\rag_foundation` |
| Foundation venv | `D:\py_venv\rag_application_builder_foundation` |
| Job Application Manager | (see export §5) |
| LifeVault | `D:\Workarea\StudyBook\Proj_development\LifeVault` |
| Local memory vault | `D:\Workarea\StudyBook\local_memory` |

### Python Environment

Run before any Python commands in StudyBook:

```powershell
D:\Workarea\StudyBook\env_setter.ps1
```

Central venv root: `C:\py_venv` | Central libs: `D:\py_libs` | Foundation Python: 3.13.11

### Standing Constraints (always apply)

- Small bites; no hidden-step assumptions
- Preserve exact paths and canonical filenames
- No duplicate files or unauthorized root moves
- Shared library for reusable mechanics; production-quality (typed, documented, tested)
- No secrets in Git; do not duplicate private work-repository content in `local_memory`
- OpenAI primary provider; IBM watsonx planned later
- Monitoring and budget visibility required in AI app architecture
- RemNote: multiple-choice primary; numbered `01_...` imports in chapter `Study/` folders

**Tags:** `sean`, `profile`, `career`, `learning-style`, `projects`

---

## Session: Grok Build init (2026-06-15)

**Q:** What is this project?

**A:** Small local memory / personal notes vault at `D:\Workarea\StudyBook\local_memory` for commands, paths, login steps, file locations, learning notes, and repeatable how-to answers.

**Tags:** `grok`, `project`, `purpose`

---

## Session: Grok Build init (2026-06-15)

**Q:** What prefix should Grok use for memory files?

**A:** Always use `GROK_` prefix: `GROK_MEMORY.md`, `GROK_AGENTS.md`, `GROK_RUNBOOK.md`, `GROK_CURRENT_STATE.md`.

**Tags:** `grok`, `naming`, `convention`

---

## Session: Grok Build init (2026-06-15)

**Q:** How do I activate the Python environment before running Python commands?

**A:**

```powershell
D:\Workarea\StudyBook\env_setter.ps1
```

Run this in PowerShell before any Python command in this project.

**Tags:** `grok`, `python`, `venv`, `environment`

---

## Session: Grok launcher script (2026-06-15)

**Q:** How do I start Grok Build for local_memory from anywhere?

**A:**

```powershell
pwsh -ExecutionPolicy Bypass -File "D:\start_grok_local_memory.ps1"
```

Script can live anywhere (defaults: StudyBook `D:\Workarea\StudyBook`, local_memory under it). Runs `env_setter.ps1`, cds to `local_memory`, launches Grok with GROK bootstrap rules. Use `-NoNewWindow` to run in the current shell.

**Dual-copy policy (stable file):**
- **Run:** `D:\start_grok_local_memory.ps1` only
- **Repo archive:** `local_memory\start_grok_local_memory.ps1` (git backup)
- Treat as frozen; keep both identical if a change is ever required

**Tags:** `grok`, `launcher`, `powershell`

---