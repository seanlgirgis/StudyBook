# 002. Write a Function - Leap Year

## Source
HackerRank Python Introduction

## Problem Summary
Write a function `is_leap(year)` that returns `True` if the year is a leap year, otherwise `False`.

Leap year rules:
- If divisible by `400`, it is a leap year.
- Else if divisible by `100`, it is not a leap year.
- Else if divisible by `4`, it is a leap year.
- Otherwise, it is not a leap year.

## Final Accepted Solution
```python
def is_leap(year):
    leap = False

    if year % 400 == 0:
        leap = True
    elif year % 100 == 0:
        leap = False
    elif year % 4 == 0:
        leap = True

    return leap

year = int(input())
print(is_leap(year))
```

## Plain-English Explanation
- `year % 400 == 0` checks if the year divides evenly by `400`.
- `2000` is leap because it is divisible by `400`.
- `1900` is not leap because it is divisible by `100` but not `400`.
- `1990` is not leap because it is not divisible by `4`.
- The safest order is checking `400` and `100` before `4`.

## Sample Inputs and Outputs
- Input: `1990`
- Output: `False`

- Input: `2000`
- Output: `True`

## Mistakes or Reminders
- Do not check `% 4` first, or century years can be misclassified.
- Return a boolean (`True`/`False`), not strings.

## Review Checklist
- [ ] I can state leap-year rules in the correct order.
- [ ] I can explain why `1900` is not a leap year.
- [ ] I can write and return a boolean function cleanly.
