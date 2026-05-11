# 028. Set Mutations

## Source
HackerRank Python - Sets

## Problem Summary
Given an initial set of integers and multiple mutation commands (`update`, `intersection_update`, `difference_update`, `symmetric_difference_update`), apply each operation in order and print the sum of the final set.

## Final Accepted Solution
```python
n1 = int(input())
s = set(map(int, input().split()))

n = int(input())

for _ in range(n):
    operation = input().split()[0]
    other_set = set(map(int, input().split()))

    if operation == "update":
        s.update(other_set)
    elif operation == "intersection_update":
        s.intersection_update(other_set)
    elif operation == "symmetric_difference_update":
        s.symmetric_difference_update(other_set)
    elif operation == "difference_update":
        s.difference_update(other_set)

print(sum(s))
```

## Plain-English Explanation
- Start with the initial set `s`.
- For each command, read operation name and the next set.
- Apply the matching in-place mutation method on `s`.
- After all updates, print `sum(s)`.

## Sample Inputs and Outputs
- Input: varies by test case with multiple set operations
- Output: single integer sum of final mutated set

## Mistakes or Reminders
- These methods mutate `s` directly.
- Command line can include extra values; use the first token for operation name.
- Apply operations in exact input order.

## Review Checklist
- [ ] I can explain differences between all four mutation methods.
- [ ] I can parse command-driven set operations from input.
- [ ] I can compute final result after sequential in-place updates.
