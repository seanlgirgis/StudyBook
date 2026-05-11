# 015. String Validators

## Source
HackerRank Python - Strings

## Problem Summary
Given a string `s`, print five boolean results in this exact order:
1. whether any character is alphanumeric,
2. whether any character is alphabetical,
3. whether any character is a digit,
4. whether any character is lowercase,
5. whether any character is uppercase.

## Final Accepted Solution
```python
if __name__ == '__main__':
    s = input()  # Read the input string once

    # any(...) already returns True or False, so no ternary is needed
    print(any(ch.isalnum() for ch in s))  # 1) Any alphanumeric character?
    print(any(ch.isalpha() for ch in s))  # 2) Any alphabetical character?
    print(any(ch.isdigit() for ch in s))  # 3) Any digit?
    print(any(ch.islower() for ch in s))  # 4) Any lowercase letter?
    print(any(ch.isupper() for ch in s))  # 5) Any uppercase letter?
```

## Plain-English Explanation
- `any(...)` checks if at least one item in a sequence is `True`.
- Each generator expression checks one string rule (`isalnum`, `isalpha`, `isdigit`, `islower`, `isupper`).
- Since `any(...)` already returns `True` or `False`, using `True if ... else False` is unnecessary.
- Output order must match HackerRank’s required five-line sequence.

## Sample Inputs and Outputs
- Input: `qA2`
- Output:
  - `True`
  - `True`
  - `True`
  - `True`
  - `True`

## Mistakes or Reminders
- Keep exact output order of the five checks.
- Avoid extra text in output; print booleans only.
- Do not wrap `any(...)` with redundant ternary expressions.

## Review Checklist
- [ ] I can explain why `any(...)` alone is enough.
- [ ] I can keep the five validator outputs in the required order.
- [ ] I can read and use Python string predicate methods confidently.
