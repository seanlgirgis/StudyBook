# 020. Capitalize!

## Source
HackerRank Python - Strings

## Problem Summary
Given a full name string containing alphanumeric characters and spaces, capitalize the first character of each word while preserving original spacing. Words starting with digits (for example `12abc`) remain unchanged because uppercasing digits has no effect.

## Final Accepted Solution
```python
#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the solve function below.
def solve(s):
    words = s.split(" ")
    fixed_words = []

    for word in words:
        if word:
            fixed_words.append(word[0].upper() + word[1:])
        else:
            fixed_words.append(word)

    return " ".join(fixed_words)


if __name__ == '__main__':
    s = input()

    result = solve(s)
    print(result)
```

## Plain-English Explanation
- Split with `split(" ")` (single-space delimiter) so repeated spaces are preserved as empty strings.
- For each word:
  - if non-empty, uppercase only first character and keep the rest as-is.
  - if empty, keep it unchanged.
- Join back with a single-space delimiter to preserve original spacing layout.

## Sample Inputs and Outputs
- Input: `chris alan`
- Output: `Chris Alan`

- Input: `1 w 2r 3g`
- Output: `1 W 2r 3g`

## Mistakes or Reminders
- Avoid plain `split()` with no argument if spacing must be preserved.
- Capitalize only first character of each word.
- Keep function name `solve` for HackerRank compatibility.

## Review Checklist
- [ ] I can explain why `split(" ")` preserves spacing better here.
- [ ] I can safely handle empty segments caused by repeated spaces.
- [ ] I can capitalize first character without changing the rest.
