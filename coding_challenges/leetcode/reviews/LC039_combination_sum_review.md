# LC039 — Combination Sum

## Why It Is Priority
- repeat count: 4
- bucket: Mixed
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: return all unique combinations of candidates summing to `target`
- input shape: distinct positive integers `candidates` and integer `target`
- output: list of combinations (each combination can reuse the same candidate)
- constraints (inferred if needed): avoid duplicate combinations by enforcing non-decreasing choice order

## Core Pattern
- Backtracking DFS over candidate choices with running remainder.
- Enforce non-decreasing index progression to avoid permutation duplicates.
- Reuse allowed by recursing with same index after choosing a candidate.

## Recognition Triggers
- Need all combinations that hit exact target, not just one solution.
- Candidate reuse is allowed (unbounded picks).
- Output is a list of paths, signaling search tree enumeration.
- Duplicate combinations must be removed by construction/order.

## Correct Approach Outline
1. Run DFS backtracking with parameters `(start_index, remaining, path)`.
2. If `remaining == 0`, record a copy of `path`; if `remaining < 0`, stop branch.
3. Iterate candidates from `start_index` onward to keep ordering canonical.
4. Recurse with same index (allow reuse), then backtrack by popping last choice.

## Complexity
- time: exponential in number of valid combinations (output-sensitive)
- space: O(target / min(candidates)) recursion/path depth
- why: branch factor from candidate choices, pruned by remaining sum.

## Common Failure Modes
- recursing with `i + 1` and accidentally disallowing reuse
- not enforcing index order, producing permutation duplicates
- forgetting early stop when remainder goes negative
- appending `path` without copy and mutating saved answers

## Implementation Checklist
- [ ] stop branch immediately when `remaining < 0`
- [ ] append result only when `remaining == 0`
- [ ] recurse with same index to allow unlimited reuse
- [ ] iterate from `start_index` to prevent permutation duplicates
- [ ] test with no-solution case and single-candidate exact match

## What To Practice Next
- [LC040 Combination Sum II](https://leetcode.com/problems/combination-sum-ii/)
- [LC216 Combination Sum III](https://leetcode.com/problems/combination-sum-iii/)
- [LC078 Subsets](https://leetcode.com/problems/subsets/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: priority pass filled for backtracking-recognition cues


## Pattern Links
- Primary: Backtracking
