# LC300 — Longest Increasing Subsequence

## Why It Is Priority
- repeat count: {N}
- bucket: DP
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: compute length of the longest strictly increasing subsequence
- input shape: integer array `nums`
- output: integer LIS length
- constraints (inferred if needed): subsequence is not required to be contiguous

## Core Pattern
- Patience-sorting view with `tails`: best (smallest) tail for each subsequence length.
- Binary search to find where current number fits in `tails`.
- Replace to keep future options open; append only when extending longest length.

## Recognition Triggers
- Asks for longest strictly increasing subsequence, not contiguous subarray.
- Brute-force/DFS feels exponential and classic DP O(n^2) may be too slow.
- Need length only, not the actual subsequence reconstruction.
- Prompt hints at optimization beyond pairwise transition DP.

## Correct Approach Outline
1. Track `tails`, where `tails[i]` is the smallest tail for an increasing subsequence of length `i+1`.
2. For each number, binary-search first index in `tails` with value >= current.
3. Replace at found index or append if current is larger than all tails.
4. Final LIS length is `len(tails)`.

## Complexity
- time: O(n log n)
- space: O(n)
- why: each element does one binary search over `tails`.

## Common Failure Modes
- {failure mode 1}
- {failure mode 2}
- {failure mode 3}
- {failure mode 4}

## Implementation Checklist
- [ ] use strictly increasing semantics (`>=` in lower_bound replacement)
- [ ] store minimal tail per length, not actual subsequence reconstruction
- [ ] append only when current > last tail
- [ ] replace in-place on lower_bound index
- [ ] test duplicates and fully descending arrays

## What To Practice Next
- LC### {Related Problem 1}
- LC### {Related Problem 2}
- LC### {Related Problem 3}

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: {draft lineage / decisions}


## Pattern Links
- Primary: DP (1D / knapsack)
