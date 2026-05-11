# 019. Alphabet Rangoli

## Source
HackerRank Python - Strings

## Problem Summary
Given an integer `size`, print an alphabet rangoli pattern. The center contains `a`, the outer letters go up to the size-th alphabet letter, rows are hyphen-separated, and lines are padded with hyphens.

## Final Accepted Solution
```python
def print_rangoli(size):
    width = (size - 1) * 4 + 1
    last_char = chr(ord('a') + size - 1)

    for i in range(2 * size - 1):
        lett = abs((size - 1) - i)
        start_char = chr(ord('a') + lett)

        word = start_char

        for code in range(ord(start_char) + 1, ord(last_char) + 1):
            word = chr(code) + '-' + word + '-' + chr(code)

        print(word.center(width, '-'))


if __name__ == '__main__':
    n = int(input())
    print_rangoli(n)
```

## Plain-English Explanation
- Total line width is `(size - 1) * 4 + 1` to fit letters and hyphens symmetrically.
- Pattern has `2 * size - 1` rows (top half + middle + bottom half).
- `lett` computes how far each row is from center.
- Build each row outward from a starting letter up to the outer boundary letter.
- Use `center(width, '-')` to pad each row with hyphens.

## Sample Inputs and Outputs
- Input: `3`
- Output:
  - `----c----`
  - `--c-b-c--`
  - `c-b-a-b-c`
  - `--c-b-c--`
  - `----c----`

## Mistakes or Reminders
- Keep exact hyphen padding width.
- Ensure top and bottom halves mirror each other.
- Use lowercase letters only.

## Review Checklist
- [ ] I can compute rangoli width from size.
- [ ] I can build mirrored rows using loops and character codes.
- [ ] I can explain why there are `2 * size - 1` rows.
