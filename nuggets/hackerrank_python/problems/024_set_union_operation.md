# 024. Set .union() Operation

## Source
HackerRank Python - Sets

## Problem Summary
Given two sets of student roll numbers (English subscribers and French subscribers), find how many students subscribed to at least one newspaper. Duplicates across sets should be counted once.

## Final Accepted Solution
```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

n1 = int(input())
s1 = set(map(int, input().split()))

n2 = int(input())
s2 = set(map(int, input().split()))

print(len(s1.union(s2)))
```

## Plain-English Explanation
- Read both groups as sets.
- `s1.union(s2)` combines all unique roll numbers from both sets.
- `len(...)` gives total number of unique subscribers.
- Using sets automatically removes duplicates.

## Sample Inputs and Outputs
- Input:
  - `9`
  - `1 2 3 4 5 6 7 8 9`
  - `9`
  - `10 1 2 3 11 21 55 6 8`
- Output: `13`

## Mistakes or Reminders
- Convert lists to sets before union.
- Do not add lengths directly (`len(s1) + len(s2)`) because overlap would be double-counted.
- `union` can be called as `s1.union(s2)` or `s1 | s2`.

## Review Checklist
- [ ] I can explain what set union means.
- [ ] I can explain why duplicates are counted once.
- [ ] I can compute unique totals with `len(set.union(...))`.
