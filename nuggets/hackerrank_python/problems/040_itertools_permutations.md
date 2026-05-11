# 040. itertools.permutations()

## Source
HackerRank Python - Itertools

## Problem Summary
Given a string `S` and integer `k`, print all permutations of length `k` from `S` in lexicographic order, one permutation per line.

## Accepted Solution
```python
from itertools import permutations

S, sk = input().strip().split()
k = int(sk)

result = permutations(S, k)

for s in sorted(result):
    print("".join(s))
```

## Alternative Solution
```python
from itertools import permutations

S, k = input().split()
k = int(k)

for item in permutations(sorted(S), k):
    print("".join(item))
```

## Provided Solution Reviewed
The provided solution is correct and should pass.

What is good:
- `from itertools import permutations` imports the required utility.
- `input().strip().split()` reads `S` and `k` from one line.
- `int(sk)` converts `k` to integer.
- `permutations(S, k)` creates ordered arrangements of length `k`.
- `sorted(result)` ensures lexicographic order.
- `"".join(s)` converts each character tuple into output string.

## Plain-English Explanation
A permutation is an ordered arrangement.

Example:
- `AC` and `CA` are different permutations.

`permutations(S, k)` returns tuples of characters.

Example:
- `permutations("ABC", 2)` includes tuples like `('A', 'B')`, `('A', 'C')`, `('B', 'A')`.

HackerRank expects string output, so use:
- `"".join(('A', 'B'))` -> `AB`

Output must be lexicographic, so sort before printing (or sort input first in the alternative form).

## Sample Inputs and Outputs
- Input: `HACK 2`
- Output:
  - `AC`
  - `AH`
  - `AK`
  - `CA`
  - `CH`
  - `CK`
  - `HA`
  - `HC`
  - `HK`
  - `KA`
  - `KC`
  - `KH`

## Important Learning Notes
- `permutations` comes from `itertools`.
- Order matters in permutations.
- `permutations(S, k)` returns tuples.
- Use `"".join(...)` to convert tuple to string.
- `sorted(...)` gives lexicographic order.
- Convert `k` to `int` before calling permutations.

## Mistakes or Reminders
- Do not print tuples directly.
- Do not forget `int(k)` conversion.
- Do not confuse permutations with combinations.
- Permutations include both `AC` and `CA`.
- Each output line must have exactly `k` characters.
- Keep output lexicographically ordered.
