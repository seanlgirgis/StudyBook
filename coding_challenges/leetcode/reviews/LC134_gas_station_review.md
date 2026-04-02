# LC134 — Gas Station

## Why It Is Priority
- repeat count: 3
- bucket: Greedy
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find the starting gas station index to complete a circuit
- input shape: two integer arrays `gas` and `cost`
- output: integer index (or -1 if impossible)
- constraints (inferred if needed): guaranteed unique solution if one exists, length up to 10^5

## Core Pattern
- greedy accumulation / single-pass prefix sum
- calculate net gain at each station (`gas[i] - cost[i]`)
- if total gas < total cost, impossible; else, a valid start must exist
- if running gas drops below 0, the start must be *after* the current station

## Recognition Triggers
- "complete a circuit", "starting index"
- net running total cannot dip below zero
- guaranteed unique solution hint

## Correct Approach Outline
1. If `sum(gas) < sum(cost)`, return -1
2. Initialize `current_gas = 0` and `start_index = 0`
3. Iterate `i` through the stations
4. Add `gas[i] - cost[i]` to `current_gas`
5. If `current_gas < 0`, reset `current_gas = 0` and tentatively set `start_index = i + 1`
6. Return `start_index` after the loop

## Complexity
- time: O(N)
- space: O(1)
- why: single pass over the arrays with constant scalar updates

## Common Failure Modes
- Naively running O(N^2) simulating a start from every index (causes TLE)
- Forgetting to confirm global viability (`sum(gas) >= sum(cost)`)
- Resetting `start_index` to `i` instead of `i + 1`

## Implementation Checklist
- [ ] upfront sum check: `sum(gas) < sum(cost) -> return -1`
- [ ] accumulate net gas dynamically
- [ ] reset condition: when accumulator drops below 0, jump `start_index` to next index
- [ ] no need to wrap around the array due to unique solution guarantee and global sum check

## What To Practice Next
- LC53 Maximum Subarray (similar reset-if-negative logic via Kadane's)
- LC846 Hand of Straights (greedy frequency consumption)
- LC763 Partition Labels (greedy interval processing)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: classic O(N) greedy reset accumulator pattern

## Pattern Links
- Primary: Greedy
