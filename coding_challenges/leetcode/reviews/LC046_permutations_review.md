# LC046 — Permutations

## Why It Is Priority
- repeat count: 4
- bucket: Backtracking
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: return all possible permutations of an array of distinct integers
- input shape: array of distinct integers `nums`
- output: list of lists spanning all permutations
- constraints: array length 1 to 6

## Core Pattern
- recursive backtracking (DFS on decision tree)
- iterate over all elements; if an element isn't used yet, add it to the path
- recurse and then remove the element to explore other branches

## Recognition Triggers
- "all possible permutations"
- factorial time complexity bounds (N <= 6 or 10)
- path-building without explicit subsets or combinations

## Correct Approach Outline
1. Initialize `result = []` and `path = []`
2. Define `backtrack()` function that takes `path`
3. Base case: If `len(path) == len(nums)`, append `path.copy()` to `result` and return
4. Iterate over each `num` in `nums`:
5. If `num` is currently in `path`, `continue` (or use a `visited` set for O(1) checks)
6. Else, append `num` to `path`, recurse, then `path.pop()`

## Complexity
- time: O(N * N!)
- space: O(N) (recursion stack + current path)
- why: N! leaves in the recursion tree, O(N) work to copy the path into results

## Common Failure Modes
- Yielding references to the same `path` list instead of appending a copy (`path[:]`)
- Using `O(N)` list lookups (`num in path`) instead of a `visited` array or boolean map (fine for N=6, bad for larger)
- Passing mutated arrays down recursion blindly rather than strictly managing choose/unchoose state

## Implementation Checklist
- [ ] Backtrack structure: Check base case -> Iterate -> Choose -> Recurse -> Unchoose
- [ ] Use `path.copy()` or `path[:]` when appending to `result`
- [ ] Maintain `used` state cleanly (either via explicit boolean array or `in` checks for tiny constraints)

## What To Practice Next
- LC047 Permutations II
- LC078 Subsets
- LC039 Combination Sum

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: foundational backtracking template for total ordering

## Pattern Links
- Primary: Backtracking
