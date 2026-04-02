# LC023 — Merge k Sorted Lists

## Why It Is Priority
- repeat count: 5
- bucket: Heap
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: merge `k` sorted linked lists into one single sorted list
- input shape: array of `k` linked list heads
- output: head of the single merged list
- constraints: k <= 10^4, total nodes <= 10^4

## Core Pattern
- minimum heap (priority queue)
- insert only the *current* head of each list into a size `k` min-heap
- extract min, attach to result, and insert the next node of that list's sequence

## Recognition Triggers
- "merge k sorted"
- dynamic multi-way comparisons
- maintaining a running minimum among multiple distinct sequences

## Correct Approach Outline
1. Initialize a `dummy` node, a `curr` pointer, and an empty min-heap
2. Iterate over the input lists, pushing `(head.val, index, head)` for valid heads into the heap
3. While the heap is not empty:
4. Pop the smallest node tuple
5. Attach the node to `curr.next`, and advance `curr`
6. If the popped node has a `.next`, push `(node.next.val, index, node.next)` into the heap
7. Return `dummy.next`

## Complexity
- time: O(N log k) (N is total nodes across all lists, k is number of lists)
- space: O(k) (max size of the heap)
- why: every node is pushed and popped exactly once from a heap of max size `k`

## Common Failure Modes
- Attempting to put all nodes into a giant array, sort it, and rebuild a list (slower, O(N log N) time, O(N) space)
- Pushing the actual `ListNode` directly into python's `heapq` without tying ties with a unique `index` (causes `TypeError` on unorderable nodes)
- Pushing `None` nodes into the heap during initialization or traversal

## Implementation Checklist
- [ ] `dummy = ListNode()` initialization
- [ ] handle custom tie-breakers in Python `heapq` via `enumerate` to provide unique integer indices
- [ ] ensure only `node is not None` elements enter the heap
- [ ] enqueue `node.next` after unwiring/processing `node`

## What To Practice Next
- LC378 Kth Smallest Element in a Sorted Matrix
- LC215 Kth Largest Element in an Array

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: archetype for k-way merges via Priority Queue

## Pattern Links
- Primary: Heap (k-way merge)
- Secondary: Divide and Conquer
