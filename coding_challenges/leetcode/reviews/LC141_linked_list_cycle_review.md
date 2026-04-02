# LC141 — Linked List Cycle

## Why It Is Priority
- repeat count: 3
- bucket: LinkedList
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: detect whether a singly linked list contains a cycle
- input shape: head pointer of linked list nodes
- output: boolean indicating cycle presence
- constraints (inferred if needed): prefer O(1) extra space

## Core Pattern
- Floyd's tortoise-hare two-pointer traversal.
- Slow moves one step; fast moves two steps.
- If pointers meet, cycle exists; if fast hits null, no cycle.

## Recognition Triggers
- Linked list may loop back to prior node.
- Need cycle detection without modifying nodes.
- Memory constraint discourages hash-set visited tracking.
- Output is boolean existence of loop.

## Correct Approach Outline
1. Initialize `slow` and `fast` at head.
2. While `fast` and `fast.next` exist, advance `slow` by 1 and `fast` by 2.
3. If `slow == fast` at any step, return `true`.
4. If loop exits, return `false`.

## Complexity
- time: O(n)
- space: O(1)
- why: each pointer traverses at most linear nodes before terminate/meet.

## Common Failure Modes
- missing null checks for `fast` and `fast.next`
- advancing both pointers by one step (never guarantees meeting behavior)
- comparing node values instead of node references
- returning true on head-only list without verifying actual loop

## Implementation Checklist
- [ ] guard loop with `fast` and `fast.next`
- [ ] move `slow` once and `fast` twice per iteration
- [ ] compare node identities, not values
- [ ] return false only when fast-path terminates
- [ ] test empty, one-node no-cycle, and one-node self-cycle

## What To Practice Next
- [LC142 Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/)
- [LC876 Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/)
- [LC19 Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: promotion draft completed for fast-slow pointer cycle detection


## Pattern Links
- Primary: Two pointers
