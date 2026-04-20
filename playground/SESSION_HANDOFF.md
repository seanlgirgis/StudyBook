# Claude Handoff — Sean's CodeSignal Study Session

## Who is Sean
Preparing for a **Capital One CodeSignal GCA** — 70 min, 4 questions, Python 3.
Recruiter (Sam) flagged: **2D arrays/matrices, HashMaps, DSA**.
Q1/Q2 are warm-ups. Q3/Q4 are medium/hard.

---

## Playground Location
```
D:\StudyBook\playground\
```
JupyterLab runs in Docker — notebooks open in browser. Markdown files must be right-clicked → "Open With → Markdown Preview" to render.

---

## What Exists

### Master Files
| File | Purpose |
|------|---------|
| `STUDY_GUIDE.ipynb` | Clickable index of all notebooks by topic — **start here** |
| `claude_progress.md` | Full problem log with notes per problem |
| `_timer.py` | `%run _timer.py` — every notebook's second cell |

### Basics / Cheat Sheets
```
Basics/linked_list_basics.ipynb
Basics/binary_tree_basics.ipynb
Basics/monotonic_stack_basics.ipynb
```

### Problem Library — 157 notebooks (0001–0157)
All in `D:\StudyBook\playground\`. Naming: `NNNN.problem_name.ipynb`

---

## Topics Covered (23 sections in STUDY_GUIDE.ipynb)

| # | Topic | Key notebooks |
|---|-------|---------------|
| 01 | Arrays & Patterns | 0017 Kadane's, 0023 prefix×suffix, 0067 jump game |
| 02 | HashMap / Counter | 0014 two_sum, 0029 group_anagrams, 0035 subarray_sum_k |
| 03 | Two Pointers | 0038 three_sum, 0039 container_water, 0144 trapping_rain_water 🔴 |
| 04 | Sliding Window | 0030 longest_unique, 0122 char_replacement, 0148 min_window 🔴 |
| 05 | Prefix Sums | 0019 running_sum, 0023 product_except_self, 0035 subarray_k |
| 06 | Binary Search | 0027–0028, 0075 2D matrix, 0105–0106 rotated, 0121 search_rotated |
| 07 | Stack | 0031 valid_parens, 0032 min_stack, 0070 decode_string, 0112 RPN |
| 08 | Monotonic Stack | 0101–0113, 0143 histogram 🔴 |
| 09 | 2D Matrix | 0033 rotate, 0034 spiral, 0066 zeros, 0076 sudoku |
| 09b | Grid DFS/BFS | 0054 islands, 0057 rotting_oranges, 0058 word_search |
| 10 | Linked Lists | 0048–0053, 0126 reorder |
| 11 | Trees | 0077–0087, 0129 LCA general, 0132 subtree |
| 12 | Graphs | 0093 course_sched, 0130 topo_sort, 0154 Bellman-Ford, 0155 Dijkstra |
| 13 | DP 1D | 0040–0042, 0115–0118, 0123 robber_ii, 0137 cooldown |
| 14 | DP 2D | 0043–0044, 0114, 0149 edit_distance 🔴, 0152 LCS |
| 15 | Heap | 0146 last_stone, 0151 meeting_rooms_ii, 0150 median_stream 🔴 |
| 16 | Backtracking | 0094 subsets, 0127 permutations, 0135 combination_sum |
| 17 | Intervals | 0088 merge, 0125 insert, 0134 non_overlapping |
| 18 | Bit Manipulation | 0089–0092, 0096, 0131, 0147 sum_no_plus |
| 19 | Greedy | 0047 stock, 0067 jump, 0119 gas_station, 0136 jump_ii, 0157 hand_straights |
| 20 | String | 0073 anagrams, 0074 palindrome_substr, 0120 encode_decode, 0133 palindromic |
| 21 | Simulation | 0059–0060, 0064, 0071, 0139–0142 circular, 0145 bridge 🔴 |
| 22 | Hard Classics 🔴 | 0143 histogram, 0144 rain_water, 0148 min_window, 0149 edit_dist, 0150 median_stream, 0145 bridge |
| 23 | Trie | 0153 implement_trie |

---

## Sean's Coding Style
- Reaches for the right structure fast (Counter, heapq, set)
- Writes minimal clean code — no scaffolding
- Jumps to O(n) when the pattern clicks
- Does NOT need long explanations — a trace or one example unlocks it
- Submits solution to confirm, doesn't explain it back

## Watchpoints (things to reinforce)
- `sum` shadows builtin — remind when accumulation is involved
- Sliding window off-by-one — `right-left` vs `right-left+1`
- `int(a/b)` vs `a//b` for truncate-toward-zero (RPN problem)
- Two-digit DP check: `10 <= val <= 26`, not just `val <= 26`

---

## How We Work
- Sean says **"next"** → give him a new problem (no preamble)
- Sean submits code → confirm pass/fail, give one-line hint if wrong
- After pass → brief note on the key insight, then offer next
- Never ask "Ready?" — write the next problem immediately

## Format for new problems
```
## Problem Title

<one paragraph — what it's asking, constraints>

def solution(...):
    pass

assert solution(...) == ...
```

---

## Current Status
- **All 157 notebooks complete** with clean solutions
- **STUDY_GUIDE.ipynb** is the navigation hub — 23 topic sections, clickable links
- Sean is in **review / drill mode** — no new topics needed
- Priority drill order: HashMap → Two Pointers → Sliding Window → Binary Search → Trees → DP 1D → Hard Classics

## GCA Game Plan
| Time | Action |
|------|--------|
| 0:00–5:00 | Q1 — string/array/simulation |
| 5:00–15:00 | Q2 — HashMap/counter |
| 15:00–35:00 | Q3 — medium; skip to Q4 if stuck >10 min |
| 35:00–60:00 | Q4 — hard; partial credit counts |
| 60:00–70:00 | Return to skipped Q |

Submit early — check visible test cases before the last minute.

---

## CodeSignal GCA — Test Format & Rules

### Format
- **Platform:** CodeSignal (browser-based IDE)
- **Duration:** 70 minutes
- **Questions:** 4 total
- **Language:** Python 3 (Sean's choice)
- **Scoring:** Each question has multiple test cases — partial credit per case passed
- **Question difficulty curve:** Q1 easy → Q2 easy/medium → Q3 medium → Q4 medium/hard
- **Test cases:** Some visible (you can see input/output), some hidden (run on submit)

### The IDE
- Browser-based code editor — no local setup
- Has a run button to test against visible cases before submitting
- No autocomplete as powerful as a real IDE — know your syntax cold
- Tab switching is monitored — triggers a flag in the proctoring report sent to the recruiter

### What Is Allowed
- **Python standard library** — `collections`, `heapq`, `bisect`, `math`, `itertools`, `functools` — all fair game
- **Python official docs** — `docs.python.org` is safe to look up (e.g. exact heapq API, deque methods)
- **Syntax lookups** — searching "python Counter most_common" or "python heapq nlargest" is fine
- **Your own notes** (if open in another local window — not monitored)

### What Is NOT Allowed
- **Searching the problem statement** — copy-pasting any part of the question into Google
- **LeetCode / GeeksForGeeks / Stack Overflow solutions** — looking up answers to the problem
- **AI tools** — ChatGPT, Claude, Copilot, Gemini — all prohibited
- **Sharing the questions** — NDA; CodeSignal randomises question pools and tracks this
- **Excessive tab switching** — flagged by the proctoring system and included in the recruiter report

### Proctoring
- CodeSignal uses **tab-switch monitoring** — every time you leave the browser tab it is logged
- The recruiter receives a **trust score** alongside your coding score — too many switches = red flag
- There is **no webcam proctoring** for the standard GCA (unlike some company-specific assessments)
- You are allowed to use a second monitor but switching to another application is still logged

### Practical Advice
- Keep `docs.python.org` open in an adjacent tab **before** starting — one switch, not many
- Know `heapq`, `collections.deque`, `Counter`, `defaultdict` cold — these are the most looked-up things
- If you need to check something, do it during a natural pause (after submitting a question), not mid-coding
- The test auto-saves — no need to manually save
- You can run code as many times as you want before final submit
- **Final submit locks the question** — do not hit submit until you're confident

### Syntax to Know Cold (no lookup needed)
| Thing | What to memorise |
|-------|-----------------|
| `heapq` | `heappush(h,x)`, `heappop(h)`, `heapify(h)`, negate for max-heap |
| `collections.deque` | `append`, `appendleft`, `pop`, `popleft`, `rotate(-1)` |
| `collections.Counter` | `Counter(iterable)`, `c.most_common(k)`, `c[x]` returns 0 not KeyError |
| `collections.defaultdict` | `defaultdict(list)`, `defaultdict(int)` |
| `bisect` | `bisect_left(a,x)`, `bisect_right(a,x)` |
| Integer division | `a // b` floors; `int(a/b)` truncates toward zero (matters for negatives) |
| String methods | `s.isalnum()`, `s.lower()`, `s.split()`, `''.join(lst)` |
