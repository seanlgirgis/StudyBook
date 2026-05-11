# 037. Power - Mod Power

## Source
HackerRank Python - Math

## Problem Summary
Given three integers `a`, `b`, and `m` on separate lines, print `a` raised to `b`, then print `a` raised to `b` modulo `m`.

## Accepted Solution
```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

a = int(input())
b = int(input())
m = int(input())

print(pow(a, b))
print(pow(a, b, m))
```

## Alternative Solution
```python
a = int(input())
b = int(input())
m = int(input())

print(a ** b)
print((a ** b) % m)
```

## Provided Solution Reviewed
The provided solution is correct and should pass.

What is good:
- `a`, `b`, and `m` are read as integers.
- `pow(a, b)` correctly computes power.
- `pow(a, b, m)` correctly computes modular power.
- Output order is correct: full power first, modulo second.
- No import is required.

## Plain-English Explanation
`pow` has two useful forms.

Two-argument form:
- `pow(a, b)` means `a ** b`

Example:
- `pow(3, 4) = 81`

Three-argument form:
- `pow(a, b, m)` means `(a ** b) % m`

Example:
- `pow(3, 4, 5) = 1`
- because `3 ** 4 = 81` and `81 % 5 = 1`

## Sample Inputs and Outputs
- Input:
  - `3`
  - `4`
  - `5`
- Output:
  - `81`
  - `1`

## Important Learning Notes
- `pow(a, b)` is the same idea as `a ** b`.
- `pow(a, b, m)` is efficient modular exponentiation.
- `%` means remainder/modulo.
- Problem requires two output lines.
- Read `a`, `b`, and `m` from separate input lines.

## Mistakes or Reminders
- Do not read all numbers from one line for this prompt.
- Do not print only the modulo line.
- Do not reverse output order.
- `pow(a, b, m)` already includes modulo.
- No `math` import is needed.
