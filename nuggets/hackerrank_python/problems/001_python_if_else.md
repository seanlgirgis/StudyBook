# 001. Python If-Else

## Source
HackerRank Python Introduction

## Problem Summary
Given an integer `n`:
- If `n` is odd, print `Weird`
- If `n` is even and in the inclusive range `2` to `5`, print `Not Weird`
- If `n` is even and in the inclusive range `6` to `20`, print `Weird`
- If `n` is even and greater than `20`, print `Not Weird`

## Final Accepted Solution
```python
if __name__ == '__main__':
    n = int(input().strip())

    if n % 2 == 1:
        print("Weird")
    elif 2 <= n <= 5:
        print("Not Weird")
    elif 6 <= n <= 20:
        print("Weird")
    else:
        print("Not Weird")
```

## Plain-English Explanation
- `n % 2 == 1` means the number is odd.
- `elif` means "otherwise, check this next condition."
- The order matters because odd numbers are handled first.
- `2 <= n <= 5` is Python's clean way to say `n` is between `2` and `5`.

## Sample Inputs and Outputs
- Input: `3`
- Output: `Weird`

- Input: `24`
- Output: `Not Weird`

## Mistakes or Reminders
- Check odd/even first before range checks.
- Remember HackerRank often expects exact output text and capitalization.

## Review Checklist
- [ ] I can explain how `% 2` detects odd/even.
- [ ] I can explain why condition order matters.
- [ ] I can write a chained comparison without hesitation.
