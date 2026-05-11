# 044. itertools.combinations() - Probability

## Source
HackerRank Python - Itertools

## Problem summary
Given `N` lowercase letters and integer `K`, choose `K` positions and compute the probability that at least one chosen position contains `'a'`.

## Accepted solution
```python
from itertools import combinations

n = int(input())
lst = input().split()
k = int(input())

result = list(combinations(lst, k))

cnt = 0
for res in result:
    if 'a' in res:
        cnt += 1

print(cnt / len(result))
```

## Provided solution reviewed
The provided solution is correct and should pass.

Provided solution:
```python
from itertools import combinations

n = int(input())
lst = input().strip().split()
k = int(input())

result = list(combinations(lst, k))

cnt = 0
for res in result:
    if 'a' in res:
        cnt += 1

print(cnt / len(result))
```

What is good:
- `from itertools import combinations` imports the right tool.
- `n` is read to consume the first input line.
- `input().split()` reads letters list correctly.
- `k` is converted to integer.
- `list(combinations(lst, k))` builds all size-`k` selections.
- Loop checks each combination for `'a'`.
- `cnt / len(result)` computes probability correctly.

## Plain-English explanation
Probability is:
- number of combinations containing at least one `'a'`
- divided by total number of combinations.

Sample input:
- `4`
- `a a c d`
- `2`

All size-2 combinations (by position):
- `('a', 'a')`
- `('a', 'c')`
- `('a', 'd')`
- `('a', 'c')`
- `('a', 'd')`
- `('c', 'd')`

Total = `6`, good = `5`.
Probability = `5/6 = 0.833333...`.

## Important learning notes
- `combinations(lst, k)` chooses groups of size `k`.
- Combinations are based on positions, not unique values.
- Duplicate letters count separately when at different positions.
- `'a' in res` checks at least one `'a'` in selected group.
- Probability formula: `good_count / total_count`.
- `n` may be unused logically, but must be read.

## Sample input/output
- Input:
  - `4`
  - `a a c d`
  - `2`
- Output: `0.8333333333333334`

## Mistakes/reminders
- Do not convert `lst` to a set (position info would be lost).
- Do not use permutations.
- Do not count only unique value groups.
- Keep letters as list.
- Print decimal probability.
- Full float output is acceptable.
