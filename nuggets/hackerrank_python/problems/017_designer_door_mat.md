# 017. Designer Door Mat

## Source
HackerRank Python - Strings

## Problem Summary
Given two integers `height` and `width`, print a door mat pattern. `height` is odd, `width` is `height * 3`, and the pattern uses `.`, `|`, `-`, plus centered `WELCOME`.

## Final Accepted Solution
```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

if __name__ == '__main__':
    def centered_word(word, width):
        right = (width - len(word)) // 2
        print('-' * right + word + '-' * (width - right - len(word)))

    height, width = map(int, input().split())

    t = (height - 1) // 2

    for i in range(t):
        centered_word(".|." * (1 + 2 * i), width)

    centered_word("WELCOME", width)

    for i in range(t - 1, -1, -1):
        centered_word(".|." * (1 + 2 * i), width)
```

## Plain-English Explanation
- Compute top/bottom half count with `t = (height - 1) // 2`.
- Build top half with increasing repeats of `.|.`.
- Print `WELCOME` in the middle line.
- Build bottom half with decreasing repeats in reverse order.
- `centered_word` handles dash padding to keep every line exactly `width` characters.

## Sample Inputs and Outputs
- Input: `7 21`
- Output:
  - `---------.|.---------`
  - `------.|..|..|.------`
  - `---.|..|..|..|..|.---`
  - `-------WELCOME-------`
  - `---.|..|..|..|..|.---`
  - `------.|..|..|.------`
  - `---------.|.---------`

## Mistakes or Reminders
- Width must be exactly `3 * height`.
- Height must be odd for symmetric top/middle/bottom sections.
- Keep exact spacing and dash counts; pattern problems are strict.

## Review Checklist
- [ ] I can generate symmetric patterns with forward and reverse loops.
- [ ] I can compute dynamic padding from total width.
- [ ] I can build center-focused string formatting without extra spaces.
