# 043. Compress the String!

## Source
HackerRank Python - Itertools

## Problem Summary
Given a string of digits, compress consecutive repeated digits into groups. For each group, print `(count, digit)`. Only consecutive repeats are grouped; the same digit appearing later starts a new group.

## Accepted solution
```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

import itertools

data = input()

for key, group in itertools.groupby(data):
    print((len(list(group)), int(key)), end=" ")
```

## Alternative solution
```python
from itertools import groupby

data = input()

for key, group in groupby(data):
    print((len(list(group)), int(key)), end=" ")
```

## Provided solution reviewed
The provided solution is correct and should pass.

What is good:
- `itertools.groupby(data)` correctly groups consecutive equal digits.
- `key` stores the current digit.
- `group` stores consecutive items for that digit.
- `len(list(group))` correctly counts current group length.
- `int(key)` converts digit character to integer.
- `end=" "` keeps tuples on one line separated by spaces.

## Plain-English explanation
This problem is about consecutive grouping.

Input:
- `1222311`

Consecutive groups:
- `1`
- `222`
- `3`
- `11`

Output:
- `(1, 1) (3, 2) (1, 3) (2, 1)`

Important detail:
`groupby` only groups neighboring equal values. It does not count globally.

Example:
- Input: `121`
- Groups: `1`, `2`, `1`
- Output: `(1, 1) (1, 2) (1, 1)`

## Important learning notes
- `groupby` comes from `itertools`.
- It groups consecutive matching values.
- It does not group all equal values globally.
- Input digits start as strings.
- Convert `key` to `int` for integer tuple output.
- `list(group)` consumes the group iterator and enables `len()`.
- `end=" "` keeps output on one line.

## Sample input/output
- Input: `1222311`
- Output: `(1, 1) (3, 2) (1, 3) (2, 1)`

## Mistakes/reminders
- Do not use `Counter`; it counts globally.
- Do not sort input; sorting breaks consecutive grouping.
- Do not forget `int(key)` conversion.
- Do not print each tuple on a new line.
- `group` is an iterator; convert before counting.
- Same digit can appear in multiple separate groups.
