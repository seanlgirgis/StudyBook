# 039. Triangle Quest

## Source
HackerRank Python - Math

## Problem Summary
Given an integer `N`, print `N - 1` rows where row `i` prints digit `i` repeated `i` times. Solve with arithmetic only, no strings, one for-loop, and one print statement.

## Accepted Solution
```python
for i in range(1, int(input())):
    print(i * (10**i - 1) // 9)
```

## Provided Solution Reviewed
The provided solution is correct and should pass.

What is good:
- It follows HackerRank restriction of using no strings.
- It uses only one for-loop.
- It uses only one print statement.
- `range(1, int(input()))` correctly prints rows `1` through `N - 1`.
- It uses arithmetic to create repeated digits.

## Plain-English Explanation
Each row should print digit `i` repeated `i` times.

Examples:
- `i = 1` -> `1`
- `i = 2` -> `22`
- `i = 3` -> `333`
- `i = 4` -> `4444`

The expression `(10**i - 1) // 9` creates repeated `1`s:
- `i = 1` -> `1`
- `i = 2` -> `11`
- `i = 3` -> `111`
- `i = 4` -> `1111`

Multiplying by `i` creates repeated `i` digits:
- `1 * 1 = 1`
- `2 * 11 = 22`
- `3 * 111 = 333`
- `4 * 1111 = 4444`

So `i * (10**i - 1) // 9` prints row `i` correctly.

## Sample Inputs and Outputs
- Input: `5`
- Output:
  - `1`
  - `22`
  - `333`
  - `4444`

## Important Learning Notes
- `10**i` means `10` raised to power `i`.
- `10**i - 1` gives `9, 99, 999, ...`.
- Dividing by `9` gives `1, 11, 111, ...`.
- Multiply by `i` to get repeated `i` digits.
- `range(1, int(input()))` stops before `N`, so output is `N - 1` rows.
- `//` keeps integer math.

## Mistakes or Reminders
- Do not use `str(i) * i` for this restricted challenge.
- Do not use more than one loop.
- Do not add extra blank lines.
- Output stops at `N - 1`.
- Use `//`, not `/`.
- Use `**` for power, not `^`.
