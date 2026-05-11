# 036. Mod Divmod

## Source
HackerRank Python - Math

## Problem Summary
Given two integers `a` and `b` on separate input lines, print `a // b`, `a % b`, and the tuple result of `divmod(a, b)`.

## Accepted Solution
```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

n1 = int(input())
n2 = int(input())

t = divmod(n1, n2)

print(t[0])
print(t[1])
print(t)
```

## Alternative Solution
```python
a = int(input())
b = int(input())

quotient, remainder = divmod(a, b)

print(quotient)
print(remainder)
print((quotient, remainder))
```

## Provided Solution Reviewed
The provided solution is correct and should pass.

What is good:
- `n1` and `n2` are read as integers.
- `divmod(n1, n2)` correctly returns a tuple.
- `t[0]` correctly gives the quotient.
- `t[1]` correctly gives the remainder.
- `print(t)` correctly prints the tuple in required format.

## Plain-English Explanation
`divmod` calculates integer division and remainder together.

Example:
- `divmod(177, 10)` returns `(17, 7)`.

The first value is quotient:
- `177 // 10 = 17`

The second value is remainder:
- `177 % 10 = 7`

So:
- `t[0]` is `17`
- `t[1]` is `7`
- `t` is `(17, 7)`

## Sample Inputs and Outputs
- Input:
  - `177`
  - `10`
- Output:
  - `17`
  - `7`
  - `(17, 7)`

## Important Learning Notes
- `//` means integer division.
- `%` means remainder.
- `divmod(a, b)` returns both as a tuple.
- Tuple index `0` is quotient.
- Tuple index `1` is remainder.
- No import is needed for `divmod`.

## Mistakes or Reminders
- Read `a` and `b` from separate input lines.
- Do not print normal division `a / b`.
- Print exactly three lines.
- Third line must be the tuple.
- `divmod` returns `(a // b, a % b)`.
