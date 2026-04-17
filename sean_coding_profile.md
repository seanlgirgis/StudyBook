# Sean's Coding Style & Collaboration Profile

Use this document to understand how Sean writes code, structures files, and thinks about problems.
Match this style when generating code, explanations, or solutions for him.

---

## Who Sean Is

Sean is a self-directed learner working through LeetCode problems with a focus on
**dynamic programming** and algorithm fundamentals. He is not a beginner — he understands
concepts deeply and asks conceptual questions ("why not the whole zero column = True?").
He wants to **understand**, not just get answers. He codes in Python.

---

## File Structure (always follow this pattern)

Every solution file has four distinct zones:

```
1. YAML frontmatter docstring   — metadata (id, title, difficulty, tags, status)
2. Banner comment block         — problem statement, examples, constraints
3. Test harness                 — reusable, self-contained, runs at bottom of file
4. Solution                     — clearly separated with "USER TO IMPLEMENT" marker
```

**Example of the banner:**
```python
# ============================================================================
# File: 0416_lc_0416_partition_equal_subset_sum.py
# LC 416: Partition Equal Subset Sum (Medium)
#
# PROBLEM STATEMENT:
# ...
# EXAMPLES:
# ...
# CONSTRAINTS:
# ...
# ============================================================================
```

---

## Naming Conventions

Sean names things so they **read like sentences**, not abbreviations.

| Context | Sean's style | Never do |
|---|---|---|
| DP table | `canReach`, `buckets`, `LIS` | `dp`, `arr`, `t` |
| DP sources | `skip`, `take`, `skipSrc`, `takeSrc` | `opt1`, `prev` |
| Loop variable | `i`, `s`, `n` — only when meaning is obvious | `x`, `tmp` |
| Function args | `nums`, `target`, `coins`, `amount` | `a`, `b`, `lst` |
| Sentinels | `inf_amt = amount + 1` | `INF`, `9999` |

The name should tell you **what the value represents**, not what type it is.

---

## Comment Style

Comments explain **WHY**, never WHAT. The code already says what.

**Good (Sean's style):**
```python
canReach[0][0] = True  # base case
arg_copy = copy.deepcopy(nums)  # ensure user logic doesn't mutate test input
if total % 2 != 0: return False  # has to be even
```

**Bad (don't generate these):**
```python
# Loop through items
# Set dp to false
# Return result
```

One short line max. No multi-paragraph docstrings. No narrating the obvious.
Exception: `rob()` uses a docstring for Time/Space complexity — that is acceptable.

---

## Test Harness Pattern

Sean always writes a `harness(func)` function. It is **not** pytest — it is a custom
inline runner that prints human-readable output. Always follow this structure:

```python
# (Input, Expected Output, Description)
tests: List[Tuple[...]] = [
    # Standard Examples    — from the problem statement
    # Edge Cases           — boundary conditions
    # Boundary / Logic     — even-but-impossible, overflow, greedy-fails-DP-wins
    # Complex / Stress     — larger inputs, multi-path cases
]

def harness(func: Callable) -> None:
    print(f"\n--- Running Harness for: {func.__name__} ---")
    passed = 0
    for i, (...) in enumerate(tests):
        arg_copy = copy.deepcopy(input)   # always deepcopy
        try:
            result = func(arg_copy)
            if result == expected:
                print(f"Test {i+1} [PASSED]: {desc}")
                passed += 1
            else:
                print(f"Test {i+1} [FAILED]: {desc}")
                print(f"   Expected: {expected}, Got: {result}")
        except Exception as e:
            print(f"Test {i+1} [ERROR]: {desc}")
            print(f"   Exception: {e}")
    print(f"\nResult: {passed}/{len(tests)} cases passed.")
```

**Rules:**
- Test descriptions are human sentences, not code (`"Edge Case: Two identical elements"`)
- Always `deepcopy` inputs to protect the original test data
- Always catch exceptions separately so one failure doesn't kill the run
- The harness is called at the bottom of the file: `harness(my_function)`

---

## Solution Code Style

Sean's solutions are **intentional and minimal** — not golfed, not over-engineered.

```python
def can_partition(nums: List[int]) -> bool:
    total = sum(nums)
    if total % 2 != 0: return False   # guard first, explain with comment

    target = total // 2
    n = len(nums)

    canReach = [[False] * (target + 1) for _ in range(n + 1)]
    canReach[0][0] = True

    for i in range(1, n + 1):
        for s in range(target + 1):
            skip = canReach[i - 1][s]
            take = s >= nums[i - 1] and canReach[i - 1][s - nums[i - 1]]
            canReach[i][s] = skip or take

    return canReach[n][target]
```

Patterns to follow:
- **Early returns / guards** go at the top with a brief comment
- **Break the recurrence into named variables** (`skip`, `take`) — never collapse to one line
- **No magic numbers** — sentinel values get a name (`inf_amt = amount + 1`)
- **Standard library imports only** — `from typing import List, Callable, Tuple`
- **Type hints on every function signature**
- No `print` statements inside solution logic

---

## How Sean Thinks About DP

Sean thinks in terms of **what the table cell means in English**, then codes from that.
When explaining or generating DP solutions:

1. Name the table to reflect its English meaning (`canReach`, not `dp`)
2. State the recurrence in plain words before writing it in code
3. Explain the **base case** with a sentence ("zero elements can only reach sum 0")
4. Name the two choices (`skip` = don't take it, `take` = use it)
5. Highlight what enforces the 0/1 constraint vs unbounded (which row you read from)

He asks "why" questions frequently. Always be ready to explain the structural reason,
not just the mechanical one.

---

## Visualizations

Sean builds interactive step-by-step HTML visualizations for DP problems.
They live in folders like `416_viz/index.html` next to the solution file.

Style rules for visualizations:
- **Dark theme**: background `#0f1117`, accent purple `#a78bfa`
- **Color semantics**: green = reachable/True, orange = take-source, purple = current cell, red = False/blocked
- **Step-by-step**: one cell filled per step, with Prev/Next/Auto/Reset controls
- **Explain panel**: human-readable sentence per step ("skip = T | take = F → False")
- **Keyboard support**: arrow keys navigate steps
- **Preset picker**: 4–6 curated examples covering True, False, and edge cases
- **Show the recurrence** at the top in styled monospace

---

## What Not To Do

- Do not add comments that describe what the code already says
- Do not rename `canReach` to `dp` — Sean chose that name deliberately
- Do not add `try/except` inside the solution — that belongs in the harness
- Do not add extra abstraction layers or helper functions unless Sean asks
- Do not use `print` inside solution functions
- Do not write long docstrings — one line max, or none
- Do not pad code with blank lines between every statement
- Do not use `i` for a variable that represents a sum — use `s`

---

## Interaction Preferences

- **Explain concepts conversationally** — "the `i-1` is the entire guard" beats a paragraph
- **Short answers** — if the code speaks, let it. Prose only when the WHY is non-obvious
- **Ask "the Sean way"** — when he asks how to understand something, explain it with a
  mental model first, then show the code, then give examples of use
- **He codes in Python** — "Go" means "go ahead and do it", not the Go language
- **He wants to understand deeply** — answer the question behind the question
