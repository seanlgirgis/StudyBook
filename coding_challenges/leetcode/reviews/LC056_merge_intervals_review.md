# LC056 — Merge Intervals

## Why It Is Priority
- repeat count: 3
- bucket: Intervals
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: merge all overlapping intervals into disjoint coverage ranges
- input shape: list of intervals `[start, end]`
- output: merged list of non-overlapping intervals covering same ranges
- constraints (inferred if needed): input may be unsorted; touching/overlapping boundaries matter

## Core Pattern
- Sort intervals by start coordinate first.
- Sweep once while maintaining current merged interval window.
- Overlap extends current end; gap flushes current window and starts new one.

## Recognition Triggers
- Input is interval ranges with overlap consolidation requirement.
- Goal is canonical non-overlapping representation.
- Order in input is arbitrary, hinting sort-then-scan.
- Pairwise merge attempts suggest O(n^2) trap to avoid.

## Correct Approach Outline
1. Sort intervals by `start` ascending.
2. Initialize merged list with first interval as active window.
3. For each next interval, merge if `start <= active_end`, else append new window.
4. Return merged windows after full sweep.

## Complexity
- time: O(n log n)
- space: O(n)
- why: sorting dominates; scan is linear and output can hold all intervals.

## Common Failure Modes
- forgetting to sort by start before merging
- using strict `<` when boundary-touch should merge (`start <= end`)
- appending both intervals instead of expanding active end
- missing final flush of active interval

## Implementation Checklist
- [ ] sort intervals by start ascending
- [ ] track active interval as last item in output
- [ ] on overlap, set `active_end = max(active_end, curr_end)`
- [ ] on gap, append a fresh interval to output
- [ ] test nested, disjoint, touching, and single-interval inputs

## What To Practice Next
- [LC057 Insert Interval](https://leetcode.com/problems/insert-interval/)
- [LC435 Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)
- [LC452 Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: promotion draft completed for sort-and-sweep interval merge pattern


## Pattern Links
- Primary: Intervals (merge / greedy)
