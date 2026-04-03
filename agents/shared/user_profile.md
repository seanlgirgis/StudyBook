# User Profile

**Last Updated:** 2026-04-02  
**Source:** Claude memory dump

---

## Core Identity

**Role:** Senior Data Engineer & AI Architect, 20+ years enterprise IT  
**Most Recent:** Citi — ML forecasting, ETL pipelines, large-scale telemetry infrastructure  
**Target Roles:** Staff/Principal Data Engineer  
**Location:** Murphy, TX (Dallas metro) | Egyptian heritage

**Active Projects:**
- JobSearch project with RAG-augmented automation
- Grok for resume/cover letter customization
- CloudSage (open-source AWS admin framework) — GitHub: seanlgirgis/CloudSage
- AWS-CapacityForecaster (Cholesky decomposition for server metrics)

---

## Multi-AI Workflow

| AI | Purpose |
|----|---------|
| **Claude** | Strategic thinking, deep reasoning, planning, architecture, debugging |
| **Gemini ("Antigravity")** | Mechanical generation |
| **Grok** | Resume customization |
| **Claude Code (VS Code)** | Agentic file generation |

---

## LeetCode Study System

**Current Position:** Heap (after Stack/Monotonic Stack ✅)  
**Concept Ladder:** Arrays → Hash Map/Set → Queue/Deque → Stack → **Heap** → Graphs (next)

**Active Problems:** LC 496, 503, 739, 84, 853, 901 (Stack/Monotonic Stack)

**Tracker:** `leetcode_tracker_v2.xlsx` — color-coded, confidence ratings, COUNTIF/SUMPRODUCT formulas

**Notebook Structure (14-cell Jupyter):**
1. Problem statement
2. Hand-traced example
3. Visual diagram
4. Pattern guidance
5. Shell code
6. Complexity analysis
7. Citi narrative
8. Closing mantra: *"Simplicity and clarity is Gold"*

**Master Prompt:** `masterprompt.md` → batch-generates study folders (notebooks, SQL, flashcards, capstone projects)

### Hard Constraints for Notebook Prompts

Every Antigravity/Claude Code notebook prompt MUST start with:

> "Before doing anything else, read these files in order:
> 1. prompts/agent_rules.md
> 2. prompts/notebook_master_prompt.md
> 3. prompts/antigravity_notebook_template.md
>
> Follow all rules in those files. HARD CONSTRAINTS below override if there is a conflict."

### Jupyter Notebook Rules

- Jupyter format only
- No `__main__` guards
- Print-based output
- Relative paths only (never absolute)
- No markdown syntax inside code cells — all traces/tables as `#` comments
- Markdown in separate markdown cells
- Test harness: standalone function accepting callable, test cases as list of tuples
- Never hardcode solution call inside harness

---

## Claude Code Workflow Rules

1. **Delegate execution** to Claude Code; Claude handles **planning, architecture, debugging**
2. **Bite-sized tasks:** one file or one script per session, max 2-3 files
3. Always end session with **plan update + gitq**
4. **Long prompts cause drift** — keep it tight

---

## Technical History

**Solved Problems:**
- Sliding Window: LC 3, 76, 239, 424, 567
- Intervals: LC 56, 57, 253, 435, 986
- Heap: LC 703, 215, 973, 295
- Binary Search: LC 33, 153, 704

**Key Patterns Built:**
- `MinHeap`/`MaxHeap` wrapper classes (hiding negation mechanics)
- Deque master notebook: BFS, monotonic deque, 6 practical patterns

**Key Bugs Caught:**
- Stale `max_freq` in LC 424
- `pop()` vs `top()` in LC 295
- Variable shadowing in LC 76

**Architecture Preferences:**
- Floating-point normalization: `Decimal(str(f))`
- Local RAG/NLP knowledge base (considered: NeuroVault/Cerebro)

---

## Communication Style

**Preferences:**
- Humor, directness, invented terminology
- **Short, direct, one concept at a time** (likely dyslexic / possibly on spectrum)
- Visual/spatial analogies preferred (circle for rotated arrays, left/right not top/bottom)
- **No walls of text**
- **No terse definitions without context**

---

## StudyBook Environment

**Canonical Venv:** `C:\py_venv\proj_educate`  
**Machine:** ASUSPC  
**Secrets System:** Seed-backed DPAPI encryption

**CRITICAL:** Passphrase entered ONCE per machine during seed registration.  
**NEVER ask for passphrase again** — `env_setter.ps1` auto-loads from seed file.

**QAuth (Alibaba Cloud Qwen):**
- API Key stored in: `config/secrets/asuspc.secrets.enc.json`
- Endpoint: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
- Models: qwen-turbo, qwen-plus, qwen-max, qwen3.5
- Billing: Alibaba Cloud trial credits → paid

---

## Files to Know

| Purpose | Path |
|---------|------|
| Agent Rules | `prompts/agent_rules.md` |
| Notebook Master Prompt | `prompts/notebook_master_prompt.md` |
| Antigravity Template | `prompts/antigravity_notebook_template.md` |
| LeetCode Tracker | `leetcode_tracker_v2.xlsx` |
| Master Prompt | `masterprompt.md` |
| QAuth Demo | `poc/qauth_alibaba_demo.py` |
| QAuth Docs | `docs/QAUTH_SETUP.md` |

---

**Working Agreements (2026-04-02):**
- Use `Allowed Scope: bounded` by default
- Use `Reasoning Depth: deep` for migration/architecture decisions
- Stop only for high-risk ambiguity, not routine implementation
- Seed-backed secrets: passphrase once per machine, never re-prompt
