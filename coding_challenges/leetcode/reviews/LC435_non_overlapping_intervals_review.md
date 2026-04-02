# LC435 - Non-overlapping Intervals

## Why It Is Priority
- repeat count: 5
- bucket: Intervals
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: minimize removals so remaining intervals are non-overlapping
- input shape: list of intervals `[start, end]`
- output: minimum number of intervals removed
- constraints (inferred if needed): prefer greedy after sorting

## Core Pattern
- greedy by earliest finishing time
- sort intervals by end
- keep interval with smallest end to maximize future compatibility

## Recognition Triggers
- maximize number kept or minimize number removed
- overlapping intervals
- scheduling / compatibility language
- local best choice affects future room

## Correct Approach Outline
1. Sort intervals by end ascending.
2. Track the end of the last kept interval.
3. If current interval overlaps, count one removal.
4. If no overlap, keep interval and update tracked end.

## Complexity
- time: O(n log n)
- space: O(1) extra (excluding sort behavior)
- why: sorting dominates; scan is linear.

## Common Failure Modes
- sorting by start instead of end
- counting kept vs removed incorrectly
- replacing the wrong active interval on overlap
- missing why greedy is valid

## Implementation Checklist
- [ ] sort by end, not by start
- [ ] initialize with first interval end after sort
- [ ] increment removals on overlap (`start < active_end`)
- [ ] update active end only when interval is kept
- [ ] test exact-touch boundaries (`end == start`) as non-overlap

## What To Practice Next
- LC056 Merge Intervals
- LC057 Insert Interval
- LC452 Minimum Number of Arrows to Burst Balloons

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: second promotion draft from pooled index


## Pattern Links
- Primary: Intervals (merge / greedy)
- Secondary: Intervals (merge / greedy)
