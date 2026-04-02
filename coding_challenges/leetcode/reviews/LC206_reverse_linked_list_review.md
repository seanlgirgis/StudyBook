# LC206 — Reverse Linked List

## Why It Is Priority
- repeat count: 5
- bucket: LinkedList
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: reverse a singly linked list
- input shape: head of singly linked list
- output: new head of reversed list
- constraints (inferred if needed): must reverse in-place with O(1) extra space

## Core Pattern
- pointer reversal / iterative state transition
- maintain three pointers: `prev`, `curr`, `next`
- reverse link direction one node at a time

## Recognition Triggers
- "reverse linked list"
- in-place modification required
- pointer manipulation with no extra structures
- traversal with local pointer updates

## Correct Approach Outline
1. Initialize `prev = None`, `curr = head`
2. While `curr` is not null:
3. Store `next = curr.next`
4. Set `curr.next = prev`
5. Move `prev = curr`, `curr = next`
6. Return `prev` as new head

## Complexity
- time: O(n)
- space: O(1)
- why: single pass, constant pointer usage

## Common Failure Modes
- Losing the next node reference before reversing (`next` not stored)
- Creating cycles by incorrect pointer assignment
- Returning original head instead of new head (`prev`)
- Mishandling empty list or single-node list

## Implementation Checklist
- [ ] store `next` before modifying `curr.next`
- [ ] reverse pointer direction (`curr.next = prev`)
- [ ] move pointers in correct order (`prev`, then `curr`)
- [ ] return `prev` at the end
- [ ] test empty and single-node cases

## What To Practice Next
- LC141 Linked List Cycle (fast/slow pointers)
- LC19 Remove Nth Node From End of List
- LC92 Reverse Linked List II (partial reversal)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: core pointer manipulation baseline for linked list problems

## Pattern Links
- Primary: Linked List (pointer manipulation)
- Related: Two Pointers