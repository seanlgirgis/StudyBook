# LC143 — Reorder List

## Why It Is Priority
- repeat count: 3
- bucket: LinkedList
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: interleave the first half of a linked list with the reversed second half
- input shape: head of singly linked list
- output: in-place modification, return None
- constraints (inferred if needed): O(1) extra space, linear time

## Core Pattern
- fast/slow pointers to find middle
- reverse the second half in-place
- weave the two halves together alternatingly

## Recognition Triggers
- symmetric list folding or combining ends
- in-place Linked List manipulation required
- O(N) space via arrays/stacks is forbidden or suboptimal

## Correct Approach Outline
1. Use fast/slow pointers to reach the middle. `slow` will point to end of first half.
2. Sever the two halves (`second = slow.next`, `slow.next = None`)
3. Reverse the `second` half using `prev`, `curr`, `next` template
4. Merge lists `first` and `reversed_second` by updating `next` pointers alternatingly

## Complexity
- time: O(N)
- space: O(1)
- why: exact 3 independent linear passes (find mid, reverse, merge)

## Common Failure Modes
- Creating a cycle (forgetting to set the tail of the first half's `.next` to `None`)
- Mishandling odd vs even length lists during the severing phase
- Losing references during the interleave phase by overwriting `.next` too early

## Implementation Checklist
- [ ] fast/slow pointer iteration (`fast` and `fast.next` checked)
- [ ] explicitly sever the halves: `slow.next = None`
- [ ] linked list reversal template on the second half
- [ ] store `tmp1` and `tmp2` before rewiring next pointers in the merge step

## What To Practice Next
- LC876 Middle of the Linked List (fast/slow foundation)
- LC206 Reverse Linked List (reversal foundation)
- LC234 Palindrome Linked List (exact same steps, but compares instead of weaves)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: culmination of fast/slow, reversal, and merging skills

## Pattern Links
- Primary: Linked List (fast/slow + reverse)
