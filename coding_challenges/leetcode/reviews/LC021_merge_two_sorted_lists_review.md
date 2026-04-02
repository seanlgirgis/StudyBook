# LC021 — Merge Two Sorted Lists

## Why It Is Priority
- repeat count: 6
- bucket: LinkedList
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: merge two sorted linked lists into one sorted list
- input shape: heads of two sorted singly linked lists, `list1` and `list2`
- output: head of the merged sorted linked list
- constraints: 0 to 50 nodes per list, values between -100 and 100

## Core Pattern
- dummy node and two pointers
- compare heads of both lists iteratively
- attach the smaller node to the end of the merged list and advance

## Recognition Triggers
- "merge two sorted"
- multiple active independent streams of data
- in-place pointer wiring required

## Correct Approach Outline
1. Initialize a `dummy` node and `current` pointer to `dummy`
2. While both `list1` and `list2` are not None:
3. If `list1.val <= list2.val`, `current.next = list1` and `list1 = list1.next`
4. Else, `current.next = list2` and `list2 = list2.next`
5. Advance `current = current.next`
6. Attach any remaining nodes from the non-empty list: `current.next = list1 or list2`
7. Return `dummy.next`

## Complexity
- time: O(N + M) (where N and M are the lengths of the lists)
- space: O(1)
- why: exactly one pass over each node, all wiring done in-place

## Common Failure Modes
- Forgetting the dummy node and artificially complicating the assignment of the new `head`
- Dropping the remainder of a list when one list finishes before the other
- Not advancing the `current` pointer after attaching a node

## Implementation Checklist
- [ ] `dummy = ListNode()` and `curr = dummy`
- [ ] loop condition exactly `while list1 and list2:`
- [ ] correctly advance the chosen list's pointer AND the `curr` pointer
- [ ] simple tail attachment: `curr.next = list1 or list2`
- [ ] return `dummy.next`

## What To Practice Next
- LC023 Merge k Sorted Lists
- LC148 Sort List

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: classic linked list two-pointer merge pattern

## Pattern Links
- Primary: Linked List (merge pointers)
