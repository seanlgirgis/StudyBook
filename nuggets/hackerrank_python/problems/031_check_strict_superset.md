# 031. Check Strict Superset

## Source
HackerRank Python - Sets

## Problem Summary
Given a main set and multiple other sets, determine whether the main set is a strict superset of every other set.

## Accepted Learning Solution
```python
s = set(map(int, input().split()))
ncases = int(input())

ret = True

for _ in range(ncases):
    s1 = set(map(int, input().split()))
    ret = ret and s1.issubset(s) and len(s) > len(s1)

print(ret)
```

## Plain-English Explanation
This solution checks two conditions for every other set:
1. `s1.issubset(s)` confirms every element of the other set exists in the main set.
2. `len(s) > len(s1)` confirms the main set has at least one extra element, which makes it a strict superset.

Important edge-case note:
If `s` and `s1` are equal, then `s1.issubset(s)` is `True`, but `s` is not a strict superset of `s1`. The `len(s) > len(s1)` condition correctly rejects equal sets.

Example:
- `s = {1, 2, 3}`
- `s1 = {1, 2, 3}`

- `s1.issubset(s)` is `True`
- `len(s) > len(s1)` is `False`

Therefore the strict superset check is `False`.

## Shorter Alternative
```python
print(s > s1)
```

Use the explicit `issubset + length` version as the accepted learning solution because it shows the logic clearly.
