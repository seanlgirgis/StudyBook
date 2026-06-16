# Planning Index

Where requirements, analysis, architecture, planning, and development thinking live for `local_memory`.

## Principle

Separate **thinking** from **decided truth** from **operational memory**.

| Stage | Location | Status | Purpose |
|-------|----------|--------|---------|
| Exploration | `docs/planning/iterations/` | Draft / may be wrong | Dated thinking sessions, opinions, what-if |
| Requirements | `docs/planning/requirements/` | Draft until accepted | What we need, constraints, success criteria |
| Analysis | `docs/planning/analysis/` | Draft | Options, tradeoffs, research, comparisons |
| Architecture | `docs/planning/architecture/` | Proposed | Designs before commitment |
| Development plan | `docs/planning/development/` | Proposed | Phases, milestones, implementation order |
| Decided | `docs/adr/` | Accepted | Architecture Decision Records (ADR-NNN) |
| Operational | `runbooks/`, `locations/` | Active | Stored facts, commands, paths |
| Design handoff | `LOCAL_MEMORY_HANDOFF.md` | Snapshot | Point-in-time vault description |

## Document lifecycle

```text
iteration (explore)
    → requirements (clarify need)
    → analysis (compare options)
    → architecture (propose design)
    → development plan (how to build)
    → ADR (record decision)
    → runbooks / code (operate)
```

Not every idea needs every stage. Small ideas can stay in `iterations/` until they mature.

## Naming conventions

- **Iterations:** `YYYY-MM-DD_short_topic_slug.md`
- **Requirements:** `REQ_short_topic.md` or `YYYY-MM-DD_short_topic.md`
- **Analysis:** `ANALYSIS_short_topic.md`
- **Architecture:** `ARCH_short_topic.md`
- **Development:** `DEV_short_topic.md` or `PHASE_N_short_topic.md`
- **ADRs:** `ADR-NNN_title.md` (see `docs/adr/ADR-INDEX.md`)

## Rules

- Planning docs are allowed to be speculative, incomplete, and superseded.
- Do not treat planning drafts as operational memory.
- When a decision is accepted, write an ADR and link back to the source iteration.
- When something becomes a repeatable how-to, promote it to `runbooks/`.
- Preserve exact paths and canonical names; avoid `_final` / `_updated` suffixes.

## Current planning artifacts

### Iterations

- [2026-06-15_tiered_second_brain_enhancement.md](iterations/2026-06-15_tiered_second_brain_enhancement.md) — tiered multimodal second brain, model routing, sensitive-data boundary, phased roadmap

### Requirements

_None yet._

### Analysis

_None yet._

### Architecture

_None yet._

### Development

_None yet._