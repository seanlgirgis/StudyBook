# MASTER STUDY DAY GENERATOR PROMPT
# Usage: Paste this entire prompt into Claude Code. Change ONLY the file path on the last line.
# Claude Code will read the study plan and generate the complete study folder.

---

## PROMPT (copy everything below this line)

---

You are a senior Staff-level Data Engineer and AI architect acting as my personal study system generator. I am Sean Girgis — 20+ years enterprise IT, Citi telemetry infrastructure, Python/PySpark/AWS/SQL background, currently preparing for Staff/Principal Data Engineer interviews. I understand systems deeply. Do not simplify or pad. I want density, correctness, and completeness.

**YOUR TASK:**

Read the study plan file at the path I give you at the end of this prompt. Then generate a complete, self-contained study folder for that day at:

`D:\Workspace\DaysStudy\Day-{N}\`

where `{N}` is the day number extracted from the file's frontmatter or filename.

---

## FOLDER STRUCTURE TO CREATE

```
D:\Workspace\DaysStudy\Day-{N}\
│
├── README.md                          # Master navigation guide for the day
├── 00_book_of_the_day.md              # The complete reference book for this day's topics
│
├── leetcode\
│   ├── {LC###}_{slug}_solved.py       # One file per LC problem — complete solution with full test harness
│   ├── {LC###}_{slug}_practice.py     # Same file — solutions REMOVED, prompts and structure left
│   └── {LC###}_{slug}_deep_dive.md    # Concept explanation, why it works, when to use it, gotchas
│
├── sql\
│   ├── 00_setup_database.py           # Python script — creates SQLite DB with realistic sample data
│   ├── {slug}_solved.sql              # Complete SQL with comments
│   ├── {slug}_practice.sql            # SQL with answers removed, structure and hints left
│   └── {slug}_deep_dive.md            # CTE/window/etc concept explanation, engine differences
│
├── python\
│   ├── {slug}_tutorial_zero_to_hero.ipynb    # Jupyter: concept from scratch to advanced
│   ├── {slug}_practice.ipynb                  # Jupyter: exercises without answers
│   └── {slug}_real_world_project\            # Folder: mini-project showing the concept in production context
│       ├── README.md
│       ├── main.py
│       └── (supporting files as needed)
│
├── technology\
│   ├── {tech}_architecture_guide.md           # Deep dive: what it is, how it works, when to use it
│   ├── {tech}_local_simulation\               # Folder: run it locally (moto/LocalStack/SQLite/mock)
│   │   ├── README.md                          # Exact setup steps, zero assumed knowledge
│   │   ├── setup.sh (or setup.ps1)            # Install deps, initialize
│   │   └── demo.py                            # Full working demo
│   └── {tech}_interview_guide.md              # Every likely interview question with complete answers
│
├── flashcards\
│   └── day_{N}_flashcards.md                  # Q&A format, all topics, suitable for spaced repetition
│
└── capstone\
    ├── mini_project_brief.md                  # Project that uses ALL of today's topics together
    ├── solution\
    │   ├── README.md
    │   └── (complete working implementation)
    └── starter\
        ├── README.md
        └── (skeleton with TODOs — no answers)
```

---

## RULES FOR EACH FILE TYPE

### 00_book_of_the_day.md
- This is the complete reference document for the day. Exhaustive.
- Covers every topic in the study plan at depth.
- Include: concept explanation → mechanics → code patterns → complexity analysis → gotchas → interview talking points → when to use → when NOT to use → real-world data engineering context.
- Minimum 2,000 words. No fluff — every word earns its place.
- Use the Citi/telemetry context from my background when giving real-world examples.

### LeetCode — `_solved.py`
Every solved file MUST contain ALL of the following sections. Do not skip any:

```python
"""
LC #{number} — {Title} [{Difficulty}]
Category: {category}
Pattern: {pattern name}

PROBLEM:
{full problem statement}

CONSTRAINTS:
{list all constraints}

APPROACH:
{explain the approach in plain English before any code}
Time: O(?) | Space: O(?)

PATTERN RECOGNITION:
{When you see X in a problem, think Y. How to recognize this pattern in an interview.}
"""

# ============================================================
# SOLUTION 1 — BRUTE FORCE (always include if applicable)
# ============================================================
def solution_brute(params):
    """
    Approach: ...
    Time: O(n²) | Space: O(1)
    """
    pass  # implementation

# ============================================================
# SOLUTION 2 — OPTIMAL
# ============================================================
def solution_optimal(params):
    """
    Approach: ...
    Time: O(n) | Space: O(n)
    Key insight: ...
    """
    pass  # implementation

# ============================================================
# TEST HARNESS — COMPLETE, DO NOT ABBREVIATE
# ============================================================
def test_harness():
    """Run all test cases. Print PASS/FAIL with details."""
    
    test_cases = [
        # (input_args, expected_output, description)
        # ALWAYS include:
        # 1. The example from the problem statement
        # 2. Edge case: empty input
        # 3. Edge case: single element
        # 4. Edge case: all duplicates / all same
        # 5. Edge case: negative numbers (if applicable)
        # 6. Edge case: large n (describe, don't run if slow)
        # 7. The tricky case that breaks naive solutions
    ]
    
    passed = 0
    failed = 0
    for args, expected, desc in test_cases:
        result = solution_optimal(*args if isinstance(args, tuple) else [args])
        status = "PASS" if result == expected else "FAIL"
        if status == "PASS":
            passed += 1
        else:
            failed += 1
            print(f"  FAIL: {desc}")
            print(f"    Input:    {args}")
            print(f"    Expected: {expected}")
            print(f"    Got:      {result}")
    
    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed out of {passed+failed} tests")
    print(f"{'='*40}")

if __name__ == "__main__":
    test_harness()

# ============================================================
# INTERVIEW Q&A
# ============================================================
"""
Q: {question}
A: {complete answer}

Q: {question}
A: {complete answer}
... (minimum 5 Q&A pairs)
"""
```

### LeetCode — `_practice.py`
- Identical structure to `_solved.py`
- Remove ALL solution code from function bodies (replace with `pass` and a `# YOUR CODE HERE` comment)
- Remove ALL answers from the INTERVIEW Q&A section (keep the questions, replace answers with `# YOUR ANSWER:`)
- Keep ALL docstrings, all comments explaining the approach, all test cases
- The test harness stays complete and runnable — it will fail until they implement the solution
- Add a `# HINTS:` section at the top of each function with 2-3 directional hints

### LeetCode — `_deep_dive.md`
Must cover:
1. The pattern name and family (e.g., "Two Pointer Family")
2. How to recognize this pattern in the wild (the trigger conditions)
3. Step-by-step walkthrough of the optimal solution with a worked example (trace through with actual values)
4. Visual ASCII diagram of what's happening in memory/the data structure
5. Common mistakes and how they manifest (what wrong answer they produce)
6. Variations of this problem (what other LeetCode problems use the same pattern)
7. Data engineering real-world analog (where does this pattern appear in production pipelines?)

### SQL — `00_setup_database.py`
```python
"""
SQL Lab Setup — Day {N}
Creates a SQLite database with realistic sample data for all SQL exercises.
Run this FIRST. Then open the .sql files.

Usage: python 00_setup_database.py
Creates: day_{N}_lab.db in the current directory
"""
import sqlite3
import random
from datetime import datetime, timedelta

# Create the DB and all tables with INSERT statements
# Use realistic data that matches the domain (telemetry, servers, finance, etc.)
# Minimum 50-100 rows per table so queries are meaningful
# Include intentional data quality issues where relevant (nulls, duplicates)
```

### SQL — `_solved.sql`
```sql
-- {Title}
-- Concept: {what SQL concept this demonstrates}
-- 
-- PROBLEM:
-- {problem statement}
--
-- SETUP: Run 00_setup_database.py first, then:
--   sqlite3 day_{N}_lab.db < this_file.sql
--
-- APPROACH:
-- {step by step explanation of the query structure}

-- SOLUTION:
{complete query with inline comments on every non-obvious line}

-- EXPECTED OUTPUT:
-- {show what the result set looks like}

-- VARIATIONS:
-- {2-3 alternative ways to write this}

-- ENGINE NOTES:
-- PostgreSQL: {any differences}
-- MySQL: {any differences}  
-- Spark SQL: {any differences}
```

### Python Jupyter Notebooks (`_tutorial_zero_to_hero.ipynb`)
Structure the notebook with these sections as markdown cells:
1. **What is it?** — ELI5 then precise definition
2. **Why does it exist?** — What problem does it solve? What was the alternative?
3. **Mental model** — The analogy or visual that makes it click
4. **Syntax from scratch** — Simplest possible example, then build up
5. **The gotchas** — What trips people up (with broken code that shows the error, then fixed code)
6. **Production patterns** — How this is actually used at scale (Citi/data engineering context)
7. **Performance** — Memory, time, profiling with `%%timeit`
8. **Comparison** — vs the alternatives (e.g., generator vs list comp vs pandas)
9. **Exercises** — 5 exercises with solutions hidden in collapsed cells

Generate as valid `.ipynb` JSON format. Every code cell must be runnable in isolation (imports included). No placeholder cells.

### Python Practice Notebooks (`_practice.ipynb`)
- Same structure, exercises section has solutions removed
- Replace solution cells with `# TODO: Your solution here` cells
- Add assertion cells that will PASS when they get it right:
  ```python
  # Run this to check your work
  assert your_function(test_input) == expected_output, f"Expected {expected_output}"
  print("✓ Correct!")
  ```

### Real-World Project (`_real_world_project\`)
Every project must:
- Solve a realistic data engineering problem (not a toy problem)
- Be runnable with ONLY stdlib + common packages (specify exact pip installs in README)
- Have a README with: Problem Statement → Setup (exact commands) → How to Run → Expected Output → How to Extend
- Be structured with proper OOP where appropriate (classes, not just scripts)
- Include error handling, logging, and at minimum one unit test
- Be sized for 30-60 minutes of study — substantial but completable

### Technology Architecture Guide (`_architecture_guide.md`)
Must cover:
1. What it is (precise, not marketing)
2. Internal mechanics (how it actually works under the hood)
3. The architecture diagram (ASCII)
4. When to use it (specific criteria)
5. When NOT to use it (anti-patterns)
6. Cost model / operational considerations
7. How it connects to the rest of the stack
8. The Citi analog — how this would have applied to the telemetry infrastructure

### Technology Local Simulation (`_local_simulation\`)
Goal: Run the AWS/cloud service locally with zero cloud account needed.

For AWS services use:
- **S3**: `moto` library (pip install moto[s3])
- **Glue**: Simulate with PySpark locally or `moto` 
- **Athena**: Simulate with DuckDB (identical SQL dialect, reads Parquet/CSV)
- **Lambda**: Just run the handler function directly with mock events
- **Kinesis**: `moto` or just use a queue/iterator pattern

The `demo.py` must:
- Set up the simulated service
- Load realistic sample data
- Execute the actual use case from the study plan
- Print results that demonstrate the service working
- Be fully runnable: `python demo.py` → no errors, meaningful output

### Technology Interview Guide (`_interview_guide.md`)
Format:
```
## {Technology} Interview Question Bank

### Fundamentals
Q: {question}
A: {complete answer — not a bullet list, a real explanation you'd give in an interview}
Follow-up: {the next question an interviewer would ask}
Answer: {answer to the follow-up}

### Design Questions  
[System design questions with complete worked answers]

### Gotcha Questions
[The questions designed to catch people who only know the surface]

### "At Scale" Questions
[Questions that separate IC3 from Staff-level thinking]
```
Minimum 15 Q&A pairs per technology.

### Flashcards (`day_{N}_flashcards.md`)
```markdown
## Day {N} Flashcards

### FRONT: {Question}
**BACK:** {Answer}
---
```
Cover every concept, every LeetCode pattern, every SQL feature, every technology point.
Minimum 40 cards.

### Capstone Mini-Project
- Must use ALL of today's topics in a single coherent project
- Example for Day 1 (HashMaps + CTEs + Generators + AWS): 
  "Build a server telemetry aggregator: read raw metrics via a generator, deduplicate with a HashMap, write summary stats to SQLite using CTEs, simulate S3 upload with moto"
- The `solution\` folder is complete working code
- The `starter\` folder has the structure, all function signatures, all docstrings, but bodies replaced with `pass` and `# TODO` comments
- README includes: architecture diagram, what you'll learn, estimated time (should be 45-90 min for starter version)

---

## QUALITY RULES (non-negotiable)

1. **Every code file must be runnable.** No `...`, no `# implement this`, no placeholders in the solved versions. If you write a function, it works.

2. **Test harnesses are complete.** Minimum 7 test cases per LeetCode problem covering: happy path, all examples from the problem, empty/null, single element, all-same values, negative numbers (if applicable), the tricky edge case that breaks naive solutions.

3. **SQL runs against SQLite** unless a feature is SQLite-incompatible (note it, provide the PostgreSQL equivalent). The setup script creates everything needed.

4. **Jupyter notebooks are valid JSON.** Generate actual `.ipynb` format, not markdown with code blocks.

5. **No toy data.** Sample data should look like real telemetry, real transactions, real server logs — whatever fits the domain. Minimum 50 rows in SQL tables.

6. **Burned tokens = burned tokens.** Go deep. Do not truncate. Do not summarize where you could elaborate. I am paying for completeness.

7. **The practice files have NO answers.** Double-check before finishing. Any solved code left in a practice file is a failure.

8. **README.md is the navigation hub.** It must link every file with a one-line description and suggested study order with time estimates.

---

## OUTPUT SEQUENCE

Generate files in this order (so I can start studying while you continue):

1. `README.md` — navigation first so I can orient
2. `00_book_of_the_day.md` — the reference I'll keep open
3. All LeetCode `_solved.py` files
4. All LeetCode `_practice.py` files  
5. All LeetCode `_deep_dive.md` files
6. `sql/00_setup_database.py`
7. All SQL solved + practice + deep dive files
8. All Python notebooks (tutorial then practice)
9. Real-world Python project
10. Technology architecture guide + interview guide
11. Technology local simulation (full working demo)
12. Flashcards
13. Capstone (solution first, then starter)

After each file, print: `✓ Created: {filepath}` so I can track progress.

---

## NOW READ THIS FILE AND BEGIN:

`{PASTE YOUR STUDY PLAN FILE PATH HERE}`

Example: `D:\Workspace\StudyPlans\study-plan-day-01.md`

Replace the path above with your actual file path and run.