# LC057 — Insert Interval

## Why It Is Priority
- repeat count: 3
- bucket: Intervals
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: insert a new interval into sorted non-overlapping intervals and merge if needed
- input shape: sorted non-overlapping interval list and `newInterval`
- output: updated non-overlapping interval list
- constraints (inferred if needed): preserve sorted order after insertion/merge

## Core Pattern
- Three-phase sweep: add left non-overlaps, merge overlaps, add right non-overlaps.
- Merge window expands by `min(start)` and `max(end)` over overlapping intervals.
- Single pass over already-sorted intervals.

## Recognition Triggers
- Input intervals are pre-sorted and non-overlapping.
- Exactly one new interval must be integrated.
- Output must remain sorted and merged.
- Overlap is localized around insertion region.

## Correct Approach Outline
1. Append intervals ending before `newInterval` starts.
2. Merge all intervals overlapping `newInterval`, updating its bounds.
3. Append merged `newInterval`.
4. Append remaining intervals that start after merged end.

## Complexity
- time: O(n)
- space: O(n)
- why: one linear scan; output may contain all intervals.

## Common Failure Modes
- forgetting sorted/non-overlap precondition and overcomplicating logic
- using strict overlap comparisons and missing boundary-touch merges
- appending `newInterval` too early before full merge expansion
- dropping tail intervals after insertion point

## Implementation Checklist
- [ ] process left/merge/right phases in order
- [ ] use overlap rule `curr.start <= new.end`
- [ ] update merged interval bounds before appending
- [ ] append untouched right side intervals at end
- [ ] test empty input, full overlap, and no-overlap insert

## What To Practice Next
- [LC056 Merge Intervals](https://leetcode.com/problems/merge-intervals/)
- [LC435 Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)
- [LC452 Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: promotion draft completed for insert-then-merge interval sweep


## Pattern Links
- Primary: Intervals (merge / greedy)
- Secondary: Intervals (merge / greedy)
