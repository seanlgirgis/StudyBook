# LC139 — Word Break

## Why It Is Priority
- repeat count: 3
- bucket: DP
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: decide if string can be segmented into dictionary words
- input shape: string `s` and word list `wordDict`
- output: boolean indicating segmentability
- constraints (inferred if needed): words can be reused; need global feasibility, not one-step greedy

## Core Pattern
- 1D DP where `dp[i]` means prefix `s[:i]` is segmentable.
- Transition by checking prior valid cut `j` and dictionary match `s[j:i]`.
- Use hash set for O(1) dictionary membership checks.

## Recognition Triggers
- Ask is feasibility of full-string segmentation into known tokens.
- Greedy longest-word choice can fail; need prefix-state exploration.
- Overlapping substring subproblems appear naturally.
- Boolean output with prefix cuts strongly signals DP.

## Correct Approach Outline
1. Convert `wordDict` to hash set and initialize `dp[0] = true`.
2. For each end index `i` from `1..n`, test cut positions `j < i`.
3. If `dp[j]` is true and `s[j:i]` in set, set `dp[i] = true` and break.
4. Return `dp[n]`.

## Complexity
- time: O(n^2) worst case
- space: O(n)
- why: each end index may scan prior cuts once.

## Common Failure Modes
- forgetting base case `dp[0] = true`
- using list lookup for dictionary and slowing transitions
- not breaking after first valid split, adding extra work
- off-by-one slicing errors for `s[j:i]`

## Implementation Checklist
- [ ] initialize boolean DP array of length `n + 1`
- [ ] seed empty-prefix base case as segmentable
- [ ] loop `i` forward and test all `j < i`
- [ ] update `dp[i]` only when both prefix and word checks pass
- [ ] test empty string, impossible split, and repeated-word reuse cases

## What To Practice Next
- [LC140 Word Break II](https://leetcode.com/problems/word-break-ii/)
- [LC472 Concatenated Words](https://leetcode.com/problems/concatenated-words/)
- [LC322 Coin Change](https://leetcode.com/problems/coin-change/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: promotion draft completed for prefix-DP segmentation pattern


## Pattern Links
- Primary: DP (1D / knapsack)
