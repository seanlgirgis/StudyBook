# 042. itertools.combinations_with_replacement()

## Source
HackerRank Python - Itertools

## Problem Summary
Given a string `S` and integer `k`, print all combinations of `S` of length `k` in lexicographic order, allowing repeated characters.

## Accepted Solution
```python
from itertools import combinations_with_replacement

S, sk = input().strip().split()
k = int(sk)

S = "".join(sorted(S))

result = combinations_with_replacement(S, k)

for s in result:
    print("".join(s))
```

## Provided Solution Reviewed
The provided solution is correct and should pass.

What is good:
- `from itertools import combinations_with_replacement` imports the correct tool.
- `input().strip().split()` reads `S` and `k` from one line.
- `int(sk)` converts `k` to integer.
- `sorted(S)` ensures lexicographic order.
- `combinations_with_replacement(S, k)` allows repeated characters.
- `"".join(s)` converts tuple output to string.

## Plain-English Explanation
Combination with replacement means order does not matter, but repeating values is allowed.

Example with `S = "ABC"`, `k = 2`:
- `AA, AB, AC, BB, BC, CC`

Unlike normal combinations, repeated pairs like `AA` are included.

The function returns tuples, so join them into strings before printing.

## Sample Inputs and Outputs
- Input: `HACK 2`
- Output:
  - `AA`
  - `AC`
  - `AH`
  - `AK`
  - `CC`
  - `CH`
  - `CK`
  - `HH`
  - `HK`
  - `KK`

## Important Learning Notes
- `combinations_with_replacement` is from `itertools`.
- Replacement means same choice can be reused.
- Order does not matter: `AB` appears, `BA` does not.
- Repeats like `AA` are valid.
- Sort `S` first for lexicographic output.
- Convert tuple outputs using `"".join(...)`.

## Mistakes or Reminders
- Do not confuse with permutations.
- Do not confuse with normal combinations.
- Normal combinations do not include `AA`.
- Do not print tuples directly.
- Do not forget to sort `S`.
- Do not forget to convert `k` to `int`.
