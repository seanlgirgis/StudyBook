# 026. Set .difference() Operation

## Source
HackerRank Python - Sets

## Problem Summary
Given two sets of student roll numbers (English subscribers and French subscribers), find the number of students who subscribed only to the English newspaper.

## Final Accepted Solution
```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

n1 = int(input())
s1 = set(map(int, input().split()))

n2 = int(input())
s2 = set(map(int, input().split()))

print(len(s1.difference(s2)))
```

## Plain-English Explanation
- Read both subscriber lists as sets.
- `s1.difference(s2)` keeps elements present in English set but not in French set.
- `len(...)` gives the total count of English-only subscribers.

## Sample Inputs and Outputs
- Input:
  - `9`
  - `1 2 3 4 5 6 7 8 9`
  - `9`
  - `10 1 2 3 11 21 55 6 8`
- Output: `4`

## Mistakes or Reminders
- Difference is directional: `s1 - s2` is not the same as `s2 - s1`.
- Convert inputs to sets before using set operations.
- Do not count overlap for this problem.

## Review Checklist
- [ ] I can explain why difference depends on order.
- [ ] I can identify English-only values from two sets.
- [ ] I can use `len(set.difference(...))` to get final count.
