# Study Day Generation Workflow
# 3-step process: Claude Pre → Gemini → Claude Post

---

## THE LOOP

```
D:\Workspace\outbox\study-plan-day-NN.md   (raw)
         │
         ▼  STEP 1: CLAUDE (Pre-Gemini)
         │  Prompt: CLAUDE_PRE_GEMINI_PROMPT.md
         │  Takes ~5 min, uses ~5% of 5hr allocation
         │
D:\Workspace\study-plan-day-NN.md   (enhanced — written to workspace root)
         │
         ▼  STEP 2: GEMINI
         │  Prompt: ENHANCED_MASTERPROMPT.md  (paste to Gemini)
         │  Input:  enhanced study-plan-day-NN.md
         │  Output: D:\Workspace\DaysStudy\Day-NN\  (~35 files)
         │  Quality: ~90-94%
         │
D:\Workspace\DaysStudy\Day-NN\      (Gemini output, ~90% quality)
         │
         ▼  STEP 3: CLAUDE (Post-Gemini)
         │  Prompt: CLAUDE_POST_GEMINI_PROMPT.md
         │  Fixes gaps, adds missing content, corrects naming
         │  Takes ~15-20 min, uses ~15% of 5hr allocation
         │
D:\Workspace\DaysStudy\Day-NN\      (closed, ~99% quality)
```

---

## STEP-BY-STEP INSTRUCTIONS

### STEP 1 — Claude Pre-Gemini (5 min)

Start a new Claude Code session. Paste:
```
prompt > "D:\Workspace\CLAUDE_PRE_GEMINI_PROMPT.md"
inputFile > "D:\Workspace\outbox\study-plan-day-NN.md"
```

Replace `NN` with the day number (e.g., `04`).

Claude will:
- Read the study plan
- Extract all metadata (LC numbers, slugs, capstone design)
- Add `## GENERATION METADATA` block to the study plan
- Enrich LeetCode problems with bonus variants
- Add capstone connection table
- Expand any short Q&A answers
- Write enhanced file to `D:\Workspace\study-plan-day-NN.md`

Confirm Claude printed: `ENHANCEMENT COMPLETE` before proceeding.

---

### STEP 2 — Gemini Generation (20-40 min)

Open Gemini (or Gemini Advanced). Start a new conversation.

Paste the entire contents of:
`D:\Workspace\ENHANCED_MASTERPROMPT.md`

At the very end, replace the placeholder with:
```
D:\Workspace\study-plan-day-NN.md
```

Gemini should print `GENERATION PLAN:` before starting.
If it does not, prompt: *"Print the GENERATION PLAN before writing any files."*

Wait for Gemini to complete all 18 steps and print `SELF-CHECK RESULTS`.

**If Gemini times out or stops early:** Note which file it stopped at, start a new conversation, and ask it to continue from that file.

---

### STEP 3 — Claude Post-Gemini (15-20 min)

Start a new Claude Code session. Paste:
```
prompt > "D:\Workspace\CLAUDE_POST_GEMINI_PROMPT.md"
inputDir > "D:\Workspace\DaysStudy\Day-NN"
```

Claude will:
- Audit all files against 18 rules
- Print a gap report
- Fix every fixable gap directly (rename files, add content, fix logging, add tests, etc.)
- Print a final score

The day is complete when the score is printed.

---

## COST ESTIMATES

| Step | Who | Time | Token cost (approx) |
|------|-----|------|---------------------|
| Pre-Gemini | Claude | 5 min | ~5% of 5hr budget |
| Generation | Gemini | 20-40 min | Low (Gemini pricing) |
| Post-Gemini | Claude | 15-20 min | ~15-20% of 5hr budget |
| **Total Claude** | | | **~20-25% of 5hr budget** |
| **vs. Claude solo** | | | ~~65%~~ |
| **Saving** | | | **~40-45%** |

---

## FILES AT WORKSPACE ROOT (D:\Workspace\)

| File | Purpose |
|------|---------|
| `ENHANCED_MASTERPROMPT.md` | Paste to Gemini. Contains all 18 quality rules. |
| `CLAUDE_PRE_GEMINI_PROMPT.md` | Paste to Claude before running Gemini. Enriches the study plan. |
| `CLAUDE_POST_GEMINI_PROMPT.md` | Paste to Claude after Gemini finishes. Audits and fixes gaps. |
| `TRACKER.md` | 90-day progress tracker (PRE / GEMINI / POST / Percent). |
| `WORKFLOW.md` | This file. |
| `study-plan-day-NN.md` | Enhanced study plans (output of PRE step, input to Gemini). |

## STUDY DAY FOLDERS (D:\Workspace\DaysStudy\)

| Folder | Contents |
|--------|---------|
| `Day-NN/` | Gemini output, audited and fixed by POST step. |

---

## QUALITY CHECKPOINTS

After each step, verify:

**After Step 1 (Claude Pre):**
- [ ] `## GENERATION METADATA` block appears at top of study plan
- [ ] All LC numbers are listed with zero-padded IDs and slugs
- [ ] `capstone_integration` has 4 entries, each naming a specific feature
- [ ] `design_pattern` is specified

**After Step 2 (Gemini):**
- [ ] `GENERATION PLAN` was printed before first file
- [ ] All expected files exist in `Day-NN/`
- [ ] `SELF-CHECK RESULTS` was printed at the end
- [ ] No obvious failures in self-check

**After Step 3 (Claude Post):**
- [ ] Final score printed
- [ ] Score ≥ 95/100
- [ ] "REMAINING FOR USER REVIEW" list is short (0-2 items)
