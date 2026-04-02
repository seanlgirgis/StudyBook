# LC131 — Palindrome Partitioning

## Why It Is Priority
- repeat count: 3
- bucket: Backtracking
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find all possible partitions of a string where every substring is a palindrome
- input shape: string `s`
- output: list of lists of strings
- constraints (inferred if needed): string length <= 16

## Core Pattern
- recursive backtracking (DFS on string splits)
- step through string, taking prefixes if they are palindromes
- recurse on remaining suffix

## Recognition Triggers
- "all possible partitions", "all combinations"
- string segmentation constraints
- very small input constraints (len <= 16 implies exponential time is expected)

## Correct Approach Outline
1. Initialize `result = []` and `path = []`
2. Define backtrack function starting at `index`
3. Base case: if `index == len(s)`, append `path.copy()` to `result`
4. Iterate `i` from `index` to `len(s) - 1`:
5. Slice `sub = s[index:i+1]`
6. If `sub` is a palindrome, append `sub` to `path`, recurse on `i+1`, then `path.pop()`

## Complexity
- time: O(N * 2^N)
- space: O(N) (for recursion stack and current path, excluding output)
- why: worst case (e.g. "aaaa") has 2^(N-1) partitions, each step checks palindrome in O(N)

## Common Failure Modes
- Storing references to lists rather than deep copies in the base case
- Looping bounds: iteration must cover the end of the string (up to `len(s)`)
- Inefficiency: repeating palindrome checks (can be pre-computed via DP, but often unnecessary for n=16)

## Implementation Checklist
- [ ] helper function `is_palindrome(left, right)` to avoid string slicing overhead
- [ ] base case correctly adds `path[:]` not `path`
- [ ] backtrack template: choose -> recurse -> unchoose (pop)
- [ ] loop correctly extracts substring limits

## What To Practice Next
- LC132 Palindrome Partitioning II (DP optimization for minimum cuts)
- LC46 Permutations (general backtracking structure)
- LC39 Combination Sum (budget-constrained backtracking)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: fundamental backtracking pattern on string segment boundaries

## Pattern Links
- Primary: Backtracking
