# LC198 — House Robber

## Why It Is Priority
- repeat count: 3
- bucket: DP
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: maximize money robbed without taking adjacent houses
- input shape: integer array `nums` where each value is cash in a house
- output: maximum obtainable amount
- constraints (inferred if needed): adjacent picks are forbidden

## Core Pattern
- 1D DP with include/exclude decision at each index.
- Recurrence: best at `i` is `max(best[i-1], best[i-2] + nums[i])`.
- Track rolling previous states to optimize space.

## Recognition Triggers
- Linear array of choices with local adjacency conflict.
- Objective is global maximum under non-adjacent constraint.
- Greedy local pick can break future optimality.
- Prompt asks for best value, not path reconstruction.

## Correct Approach Outline
1. Handle small lengths (`0`, `1`) directly.
2. Initialize DP state for first one or two houses.
3. Iterate forward using `curr = max(prev1, prev2 + nums[i])`.
4. Shift states and return final best.

## Complexity
- time: O(n)
- space: O(1)
- why: one pass with constant rolling state.

## Common Failure Modes
- using greedy largest-neighbor pick instead of DP recurrence
- wrong base cases for arrays of size 0/1/2
- allowing adjacent houses by incorrect state transition
- off-by-one errors when shifting rolling variables

## Implementation Checklist
- [ ] handle empty and single-house inputs first
- [ ] compute `max(skip, take)` each index
- [ ] preserve previous two states before update
- [ ] avoid full DP array unless clarity is preferred
- [ ] test alternating high/low and all-equal values

## What To Practice Next
- [LC213 House Robber II](https://leetcode.com/problems/house-robber-ii/)
- [LC740 Delete and Earn](https://leetcode.com/problems/delete-and-earn/)
- [LC337 House Robber III](https://leetcode.com/problems/house-robber-iii/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: promotion draft completed for linear include/exclude DP pattern


## Pattern Links
- Primary: DP (1D / knapsack)
