# LC739 — Daily Temperatures

## Why It Is Priority
- repeat count: 4
- bucket: Stack
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: compute wait days until a warmer temperature for each day
- input shape: array of daily temperatures
- output: array where each index stores days to next warmer day, else `0`
- constraints (inferred if needed): one-pass monotonic stack preferred over nested scans

## Core Pattern
- Monotonic decreasing stack of unresolved indices.
- When a warmer day appears, pop colder indices and resolve distances.
- Each index is pushed once and popped once (amortized linear scan).

## Recognition Triggers
- Need next greater element to the right for every position.
- Questions ask "how many days until warmer/higher value".
- Brute-force forward scan per index is too slow.
- Output is per-index distance, not just existence of a greater value.

## Correct Approach Outline
1. Maintain a decreasing monotonic stack of indices by temperature.
2. Iterate temperatures left to right.
3. While current temp is warmer than stack-top temp, pop index and set answer distance.
4. Push current index and continue; remaining stack entries default to `0`.

## Complexity
- time: O(n)
- space: O(n)
- why: each index is pushed once and popped at most once.

## Common Failure Modes
- storing temperatures instead of indices, losing distance computation
- using non-strict compare and breaking equal-temperature handling
- forgetting to initialize unresolved days as `0`
- computing distance with reversed subtraction order

## Implementation Checklist
- [ ] stack stores indices, not temperatures directly
- [ ] maintain strictly decreasing temps on stack
- [ ] compute distance as `i - popped_index`
- [ ] leave unresolved indices as `0`
- [ ] test strictly decreasing and strictly increasing temperature arrays

## What To Practice Next
- [LC496 Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/)
- [LC503 Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/)
- [LC901 Online Stock Span](https://leetcode.com/problems/online-stock-span/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: priority pass filled for monotonic-stack interview recognition


## Pattern Links
- Primary: Monotonic stack
