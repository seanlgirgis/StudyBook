# 003. Print Function

## Source
HackerRank Python Introduction

## Problem Summary
Given `n`, print numbers from `1` through `n` as one continuous string without spaces.

## Final Accepted Solution
```python
if __name__ == '__main__':
    n = int(input())

    for i in range(1, n + 1):
        print(i, end="")
```

## Plain-English Explanation
- `range(1, n + 1)` means start at `1` and include `n`.
- Python `range` stops before the ending number, so use `n + 1`.
- `print(i, end="")` prints values without new lines.
- For `n = 3`, output is `123`.

## Sample Inputs and Outputs
- Input: `3`
- Output: `123`

- Input: `5`
- Output: `12345`

## Mistakes or Reminders
- If `end=""` is forgotten, each number prints on a new line.
- Ensure loop starts at `1`, not `0`.

## Review Checklist
- [ ] I can explain why `n + 1` is needed in `range`.
- [ ] I can use `print(..., end="")` correctly.
- [ ] I can produce exact formatting output for coding platforms.
