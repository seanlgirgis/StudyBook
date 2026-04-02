# LC070 — Climbing Stairs

## Why It Is Priority
- repeat count: 6
- bucket: DP
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find the number of distinct ways to climb to the top of `n` stairs taking 1 or 2 steps
- input shape: integer `n`
- output: integer
- constraints: 1 <= n <= 45

## Core Pattern
- 1D dynamic programming / Fibonacci sequence
- the number of ways to reach step `i` is the sum of ways to reach `i-1` and `i-2`
- use constant space since only the last two states are needed

## Recognition Triggers
- "distinct ways"
- choices depend entirely on immediate predecessors (1 or 2 steps)
- overlapping subproblems leading to exponential bounds naively

## Correct Approach Outline
1. Handle base cases implicitly: `one_step = 1`, `two_step = 1` (representing ways for n=1 and n=0 conceptually)
2. Loop `i` from 2 to `n`
3. Calculate current step: `temp = one_step + two_step`
4. Shift variables: `two_step = one_step`
5. Shift variables: `one_step = temp`
6. Return `one_step`

## Complexity
- time: O(N)
- space: O(1)
- why: iteratively calculates N steps, holding only two variables at a time

## Common Failure Modes
- Naive recursion causing O(2^N) Time Limit Exceeded
- Creating an O(N) array when only the last two values are needed for the recurrence
- Off-by-one errors when initializing the base cases for n=0, 1, and 2

## Implementation Checklist
- [ ] Initialize two state variables conceptually representing ways to hit `n-1` and `n-2`
- [ ] Iterate `n - 1` times
- [ ] Ensure safe concurrent swapping or accurate sequential swapping (e.g. `a, b = b, a + b`)
- [ ] Return the conceptually "higher" step variable

## What To Practice Next
- LC746 Min Cost Climbing Stairs
- LC198 House Robber
- LC509 Fibonacci Number

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: perfect introduction to state-compressed 1D dynamic programming

## Pattern Links
- Primary: DP (1D / recurrence)
