# LC215 — Kth Largest Element in an Array

## Why It Is Priority
- repeat count: 4
- bucket: Heaps
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: return the k-th largest value in an unsorted array
- input shape: integer array `nums` and integer `k`
- output: single integer representing rank `k` (1-indexed largest)
- constraints (inferred if needed): duplicates allowed; avoid full sort when possible

## Core Pattern
- Maintain a size-`k` min-heap while scanning unsorted values.
- Heap holds current top `k` largest elements seen so far.
- Root of min-heap is the current k-th largest candidate.

## Recognition Triggers
- Asks for rank statistic (`k`-th largest/smallest), not full ordering.
- Input is unsorted and duplicates may exist.
- Full sort is valid but not preferred for interview optimization.
- Need one value answer, not the entire top-k list.

## Correct Approach Outline
1. Initialize a min-heap.
2. Push each number into heap; if heap size exceeds `k`, pop smallest.
3. Maintain invariant: heap stores current `k` largest elements seen.
4. After scan, heap top is the k-th largest value.

## Complexity
- time: O(n log k)
- space: O(k)
- why: each insert/pop touches heap of size at most `k`.

## Common Failure Modes
- using max-heap incorrectly and returning wrong rank element
- forgetting to trim heap when size exceeds `k`
- off-by-one confusion between `k`-th largest and `k`-th index
- mishandling duplicates by trying to deduplicate values

## Implementation Checklist
- [ ] use min-heap (not max-heap) to keep top-`k` set compact
- [ ] pop only when heap size becomes `k + 1`
- [ ] return heap root after full traversal
- [ ] verify behavior with duplicate values
- [ ] test edge cases `k = 1` and `k = len(nums)`

## What To Practice Next
- [LC703 Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/)
- [LC347 Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)
- [LC973 K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: priority pass filled for heap-based rank-selection recognition


## Pattern Links
- Primary: Heap (top-k / streaming)
