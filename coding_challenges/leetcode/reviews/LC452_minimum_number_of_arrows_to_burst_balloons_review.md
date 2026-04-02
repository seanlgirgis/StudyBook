# LC452 — Minimum Number of Arrows to Burst Balloons

## Why It Is Priority
- repeat count: 3
- bucket: Intervals
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find minimum arrows needed to burst all balloon intervals
- input shape: list of x-axis intervals `[start, end]` for balloons
- output: minimum number of arrows
- constraints (inferred if needed): one arrow at position `x` bursts all intervals containing `x`

## Core Pattern
- Greedy by earliest end point, same ordering logic as LC435.
- Maintain current arrow position at end of active overlap cluster.
- New arrow only when next interval starts after current arrow reach.

## Recognition Triggers
- Intervals represent hittable ranges, not ranges to merge.
- Objective is minimum resources (arrows), not merged output list.
- Sorting by end creates maximum future compatibility per arrow.
- Overlap means share one arrow; gap forces another arrow.

## Correct Approach Outline
1. Sort balloon intervals by end ascending.
2. Shoot first arrow at end of first interval.
3. For each interval, if `start > arrow_pos`, shoot new arrow at current end.
4. Return total arrow count.

## Complexity
- time: O(n log n)
- space: O(1) extra (excluding sort)
- why: sorting dominates; single linear sweep after sort.

## Common Failure Modes
- sorting by start and losing optimal greedy criterion
- using overlap condition incorrectly (`>=` vs `>`)
- updating arrow position on every overlap instead of keeping earliest end
- confusing with LC056 merge-output behavior

## Implementation Checklist
- [ ] sort intervals by end ascending
- [ ] initialize arrows with first interval when non-empty
- [ ] new arrow only when `start > current_arrow_pos`
- [ ] keep arrow position at current chosen end
- [ ] test nested, disjoint, and boundary-touching intervals

## What To Practice Next
- [LC435 Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)
- [LC056 Merge Intervals](https://leetcode.com/problems/merge-intervals/)
- [LC057 Insert Interval](https://leetcode.com/problems/insert-interval/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: promotion draft completed for end-sorted greedy interval stabbing


## Pattern Links
- Primary: Intervals (merge / greedy)
