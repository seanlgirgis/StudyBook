# LC020 — Valid Parentheses

## Why It Is Priority
- repeat count: 3
- bucket: Stack
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: validate whether bracket string is properly balanced and nested
- input shape: string containing bracket chars `()[]{}` 
- output: boolean validity result
- constraints (inferred if needed): closing bracket must match most recent unmatched opener

## Core Pattern
- Stack tracks unmatched opening brackets in order.
- On closing bracket, pop and verify expected opener type.
- Valid if all closes match and stack is empty at end.

## Recognition Triggers
- Must enforce proper nesting, not just equal counts.
- LIFO dependency: most recent opener must close first.
- Multiple bracket types with strict matching rules.
- Single left-to-right validation requested.

## Correct Approach Outline
1. Initialize empty stack and closing-to-opening map.
2. Iterate characters left to right.
3. Push openers; for closers, fail if stack empty or top mismatches.
4. Return true only if stack is empty after scan.

## Complexity
- time: O(n)
- space: O(n)
- why: each character is pushed/popped at most once.

## Common Failure Modes
- checking counts only and ignoring ordering/nesting
- popping without stack-empty guard on early closer
- comparing against wrong expected opener mapping
- forgetting final non-empty stack invalidation

## Implementation Checklist
- [ ] define opener set and closer->opener map
- [ ] push only openers onto stack
- [ ] on closer, validate stack top before pop
- [ ] return false immediately on mismatch/underflow
- [ ] test odd length, early closer, and fully nested valid strings

## What To Practice Next
- [LC155 Min Stack](https://leetcode.com/problems/min-stack/)
- [LC150 Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/)
- [LC394 Decode String](https://leetcode.com/problems/decode-string/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: promotion draft completed for stack-based nesting validation pattern


## Pattern Links
- Primary: Monotonic stack
