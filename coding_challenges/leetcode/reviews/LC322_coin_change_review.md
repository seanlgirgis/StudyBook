# LC322 — Coin Change

## Why It Is Priority
- repeat count: 4
- bucket: DP
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: return the minimum number of coins needed to make `amount`
- input shape: coin denominations array and integer `amount`
- output: minimum coin count, or `-1` if impossible
- constraints (inferred if needed): unbounded coin reuse; optimize over all sub-amounts up to target

## Core Pattern
- Unbounded knapsack-style 1D DP over amounts `0..target`.
- State `dp[a]` stores minimum coins needed to build amount `a`.
- Transition tries every coin: `dp[a] = min(dp[a], dp[a-c] + 1)`.

## Recognition Triggers
- Need minimum count of reusable items to reach exact target.
- Greedy by largest coin can fail on custom denominations.
- Output asks for optimal minimum, not number of combinations.
- Includes impossible-case requirement (`-1`), signaling reachability DP.

## Correct Approach Outline
1. Initialize DP array `dp[0..amount]` with `inf`, and set `dp[0] = 0`.
2. For each target value `a` from `1` to `amount`, try every coin `c`.
3. If `a - c >= 0` and `dp[a-c]` is reachable, update `dp[a] = min(dp[a], dp[a-c] + 1)`.
4. Return `dp[amount]` if finite; otherwise return `-1`.

## Complexity
- time: O(amount * n_coins)
- space: O(amount)
- why: each sub-amount computes a min over all coin options once.

## Common Failure Modes
- using greedy and missing optimal solution
- not guarding unreachable states before adding `+1`
- wrong DP initialization (missing `dp[0] = 0`)
- returning sentinel `inf` instead of `-1` for impossible amounts

## Implementation Checklist
- [ ] keep `dp[0] = 0` as the base case
- [ ] treat unreachable states as `inf` and guard before `+1`
- [ ] iterate sub-amounts in increasing order for bottom-up correctness
- [ ] return `-1` when final state remains unreachable
- [ ] test `amount = 0`, no-solution cases, and single-coin exact matches

## What To Practice Next
- [LC518 Coin Change II](https://leetcode.com/problems/coin-change-ii/)
- [LC279 Perfect Squares](https://leetcode.com/problems/perfect-squares/)
- [LC139 Word Break](https://leetcode.com/problems/word-break/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: priority pass filled for unbounded-knapsack interview pattern


## Pattern Links
- Primary: DP (1D / knapsack)
