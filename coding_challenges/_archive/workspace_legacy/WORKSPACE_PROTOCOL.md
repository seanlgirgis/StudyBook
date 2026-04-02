# WORKSPACE PROTOCOL (Single Source of Truth)

## 1. PURPOSE

This file defines how ChatGPT and Codex operate within this repository.

Goals:
- eliminate ambiguity
- eliminate memory drift
- enforce deterministic execution
- maintain a closed-loop workflow

This file is the ONLY authority for behavior.


---

## 2. CORE PRINCIPLES

1. The repository is the ONLY source of truth
2. Chat memory is NOT a source of truth
3. Every task is explicitly scoped
4. Only one task is executed per run
5. Only one communication artifact is produced
6. Minimal changes > broad changes
7. Deterministic > clever


---

## 3. AUTHORITY ORDER

1. Direct task prompt (this run)
2. WORKSPACE_PROTOCOL.md (this file)
3. agents/shared/codex_status.md (latest state reference)

Nothing else has authority.


---

## 4. MANDATORY INPUTS (EVERY RUN)

Codex MUST read:

- WORKSPACE_PROTOCOL.md
- agents/shared/codex_status.md (if exists)

Then read any files explicitly listed in the task prompt.

Do NOT assume anything outside these files.


---

## 5. TASK TYPES (MUST DECLARE ONE)

Every task MUST be one of:

- NEW_TOPIC → create new concept + code
- ENHANCEMENT → deepen existing topic
- FIX → correct incorrect behavior
- SYNC → fix repo vs status mismatch
- REFACTOR → improve structure without changing behavior

If task type is unclear → STOP and state ambiguity in codex_status.md


---

## 6. FILE CHANGE RULES

### Allowed:
- Only files explicitly listed in the task prompt

### Forbidden:
- modifying unrelated files
- restructuring directories
- renaming files
- introducing new patterns without instruction

### Rule:
If a change is not explicitly allowed → DO NOT DO IT


---

## 7. RUNTIME VERIFICATION RULE

If the task involves executable code:

- MUST run the code
- MUST capture real output
- MUST NOT fabricate output
- MUST NOT summarize without running

If the code fails on first run:

- MUST attempt to fix and re-run
- MUST retry up to 3 times total
- If still failing after 3 attempts: record all error output in codex_status.md and stop

Runtime output (success or final failure) becomes part of codex_status.md


---

## 8. COMMUNICATION CONTRACT (MANDATORY)

Codex MUST overwrite:

agents/shared/codex_status.md

EVERY RUN.

This is the ONLY output artifact.

No exceptions.


---

## 9. codex_status.md STRUCTURE

It MUST follow this exact structure:

## Topic
- <topic name>

## Task Type
- <NEW_TOPIC | ENHANCEMENT | FIX | SYNC | REFACTOR>

## Files Read
- list

## Files Created
- list or "none"

## Files Modified
- list or "none"

## What Was Done
- factual bullet points

## Why It Matters
- short, direct reasoning

## Runtime Result (if applicable)
- command run
- key outputs
- verified behaviors

## Issues / Risks (if any)
- only if real

## Next Step (optional)
- only if obvious and small


---

## 10. CONTINUITY RULE

codex_status.md is the ONLY memory between runs.

Do NOT rely on:
- previous chat
- assumptions
- unstated context

If context is missing → state it explicitly.


---

## 11. TASK EXECUTION FLOW

For every run:

1. Identify task type
2. Load required files
3. Lock scope (what can change)
4. Execute ONLY the scoped task
5. Run code if required
6. Overwrite codex_status.md
7. Stop

No side work.
No extra improvements.


---

## 12. PROMPT SHAPE TEMPLATE

Every Codex prompt SHOULD follow:

- Task Type
- Topic
- Goal
- Files to read
- Files allowed to modify
- Files forbidden to modify
- Runtime command (if needed)
- Expected facts to verify
- codex_status.md overwrite requirement
- Definition of done

---

## 13. DEFINITION OF DONE

A task is complete ONLY IF:

- codex_status.md is overwritten
- content reflects actual repo state
- runtime (if required) was executed
- no forbidden files were changed
- task scope was respected

If any condition fails → task is NOT complete


---

## 14. FAILURE HANDLING

### Code failures
- Fix and retry up to 3 times (see Section 7)
- After 3 failed attempts: record errors in codex_status.md and stop

### Git push failures
If `gitq` fails:
1. Run: `git add -A`
2. Run: `git commit -m "Quick Update <YYYY-MM-DD>"` (skip if nothing to commit)
3. Run: `git push`
4. Record outcome in codex_status.md under Issues / Risks

### All other blockers
If something is unclear or blocked:

- DO NOT guess
- DO NOT expand scope
- DO NOT improvise

Write in codex_status.md:
- what is missing
- what is blocking
- what is required next

Then STOP.


---

## 15. FINAL RULE

Clarity > intelligence  
Precision > creativity  
Execution > explanation  

Always operate like a controlled system, not a conversation.

---

## 16. AGENT RULES (PATHS & ENVIRONMENTS)

### Paths: ALWAYS Relative
- NEVER use absolute paths in any tool call or command or notebook operations. 
- Always use paths relative to the working directory (`d:/Workspace`) when possible, unless the tool explicitly demands an absolute path.

### Python Environment: env_setter.ps1
- The correct Python interpreter is inside the venv activated by `env_setter.ps1`.
- To activate the environment in a shell session: `powershell.exe -Command "& 'd:/Workspace/env_setter.ps1'"`
- To run any Python script, format it like: `powershell.exe -Command "& 'C:\py_venv\proj_educate\Scripts\python.exe' 'relative/path/to/script.py'"`