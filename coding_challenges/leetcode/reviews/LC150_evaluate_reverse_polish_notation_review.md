# LC150 — Evaluate Reverse Polish Notation

## Why It Is Priority
- repeat count: 3
- bucket: Stack
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: evaluate mathematical expression given in post-fix notation (RPN)
- input shape: array of strings `tokens`
- output: integer result
- constraints (inferred if needed): valid expression guaranteed, division truncates toward zero

## Core Pattern
- stack for LIFO evaluation
- numbers are pushed to stack
- operators pop top two numbers, evaluate, and push result back

## Recognition Triggers
- "Reverse Polish Notation", post-fix
- elements act immediately on most recently seen available values
- strictly sequential evaluation of delayed operations

## Correct Approach Outline
1. Initialize an empty `stack`
2. Iterate through each `token` in `tokens`
3. If `token` is an operator (`+`, `-`, `*`, `/`):
4. Pop `b` (right operand) and `a` (left operand)
5. Compute `a (op) b` (with integer division truncation toward zero)
6. Push result back to the stack
7. Else (it is a number), push `int(token)` to the stack
8. Return `stack[0]`

## Complexity
- time: O(N)
- space: O(N)
- why: iterates over tokens exactly once, stack holds at most N elements

## Common Failure Modes
- Popping order is wrong (left operand is popped *after* right operand: `b = pop()`, `a = pop()`)
- Integer division in Python (`//`) floors towards negative infinity, not zero (`int(a / b)` fixes this)
- Mishandling negative number parsing when differentiating between minus operators and negative digits

## Implementation Checklist
- [ ] stack strictly stores integers
- [ ] careful with popping order (`let right = pop(), let left = pop()`)
- [ ] use `int(a / b)` for zero-truncating division in Python
- [ ] return the only remaining element in stack

## What To Practice Next
- LC224 Basic Calculator (much harder, requires stack for parentheses, prefix)
- LC739 Daily Temperatures (monotonic stack)
- LC227 Basic Calculator II (stack with operator precedence)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: classic clean stack evaluator

## Pattern Links
- Primary: Stack (expression evaluation)
