# LC019 — Remove Nth Node From End of List

## Why It Is Priority
- repeat count: 3
- bucket: LinkedList
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: remove the nth node from the end of a linked list
- input shape: head of singly linked list, integer `n`
- output: head of modified list
- constraints: `n` is always valid (1 <= n <= size of list)

## Core Pattern
- fast/slow pointers with gap
- advance `fast` pointer `n` steps ahead of `slow`
- when `fast` reaches the end, `slow` is sitting right before the target node

## Recognition Triggers
- "from end of list"
- single-pass requirement (or implicit "optimize" goal)
- structural deletion needing references to the preceding node

## Correct Approach Outline
1. Create a `dummy` node pointing to `head` (handles edge cases like deleting the root)
2. Initialize `slow` and `fast` pointers at `dummy`
3. Advance `fast` exactly `n + 1` steps
4. While `fast` is not None, advance both `slow` and `fast` by 1 step
5. `slow.next = slow.next.next` to remove the target node
6. Return `dummy.next`

## Complexity
- time: O(L) where L is list length
- space: O(1)
- why: single pass traversal, constant number of pointers

## Common Failure Modes
- Failing to handle the deletion of the `head` node itself (dummy node prevents this)
- Misaligning the gap: `fast` needs to advance `n + 1` steps so `slow` stops exactly ONE node *before* the deletion target
- Null pointer exceptions if `fast` hits None prematurely (though valid `n` constraint helps)

## Implementation Checklist
- [ ] `dummy = ListNode(0, head)` to protect the head
- [ ] move `fast` by `n + 1` safely
- [ ] simultaneous traversal until `fast is None`
- [ ] standard bypass sequence: `slow.next = slow.next.next`
- [ ] return `dummy.next`

## What To Practice Next
- LC141 Linked List Cycle
- LC876 Middle of the Linked List
- LC143 Reorder List

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: classic dummy-node and delayed-pointer linked list pattern

## Pattern Links
- Primary: Two Pointers
- Secondary: Linked List
