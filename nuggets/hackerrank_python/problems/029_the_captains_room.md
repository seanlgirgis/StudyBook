# 029. The Captain's Room

## Source
HackerRank Python - Sets

## Problem Summary
Given group size `K` and a list of room numbers where each family room appears `K` times and the captain's room appears exactly once, find and print the captain's room number.

## Final Accepted Solution
```python
from collections import Counter

group_size = int(input())
counts = Counter(input().split())

for room, count in counts.items():
    if count == 1:
        print(room)
        break
```

## Plain-English Explanation
- Read `group_size` (used by problem context).
- Count occurrences of each room number with `Counter`.
- Loop through counted values and print the room with count `1`.
- Stop immediately after finding it.

## Sample Inputs and Outputs
- Input:
  - `5`
  - `1 2 3 6 6 5 5 4 4 3 2 1 6`
- Output: `6`

## Mistakes or Reminders
- Room numbers can be treated as strings here since only counting is needed.
- Captain's room appears once; all others appear exactly `K` times.
- Break after printing the unique room.

## Review Checklist
- [ ] I can use `Counter` to count frequencies quickly.
- [ ] I can identify the unique element from frequency counts.
- [ ] I can explain why this works with repeated groups.
