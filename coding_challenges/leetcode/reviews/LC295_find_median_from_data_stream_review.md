# LC295 — Find Median from Data Stream

## Why It Is Priority
- repeat count: {N}
- bucket: Heaps
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: support online insertions and return median at any time
- input shape: stream of integers with interleaved `addNum` / `findMedian` calls
- output: median as float (or int when middle value is exact)
- constraints (inferred if needed): must be efficient per update, not re-sort whole stream

## Core Pattern
- Two-heaps partition: max-heap for lower half, min-heap for upper half.
- Maintain ordering invariant: every value in lower half `<=` every value in upper half.
- Maintain size invariant: lower half has equal count or exactly one extra element.

## Recognition Triggers
- Input is a live stream with interleaved insert/query operations.
- Need median repeatedly, not just once after all values are known.
- Re-sorting on each insertion is too expensive for expected scale.
- Problem asks for fast updates and O(1)-style median read.

## Correct Approach Outline
1. Maintain two heaps: max-heap `low` (smaller half) and min-heap `high` (larger half).
2. Insert into `low`, then move top of `low` to `high` to maintain ordering.
3. Rebalance so `len(low)` is either equal to `len(high)` or exactly one larger.
4. Median is top of `low` (odd count) or average of both tops (even count).

## Complexity
- time: O(log n) per insertion, O(1) median query
- space: O(n)
- why: heap push/pop are logarithmic; median reads heap tops only.

## Common Failure Modes
- {failure mode 1}
- {failure mode 2}
- {failure mode 3}
- {failure mode 4}

## Implementation Checklist
- [ ] ensure all values in `low` <= all values in `high`
- [ ] rebalance after each insertion
- [ ] keep size invariant (`len(low) == len(high)` or `len(low) == len(high)+1`)
- [ ] use negation if implementing max-heap via Python min-heap
- [ ] test odd/even counts and negative values

## What To Practice Next
- LC### {Related Problem 1}
- LC### {Related Problem 2}
- LC### {Related Problem 3}

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: {draft lineage / decisions}


## Pattern Links
- Primary: Heap (top-k / streaming)
