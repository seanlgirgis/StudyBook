# 018. String Formatting

## Source
HackerRank Python - Strings

## Problem Summary
Given an integer `n`, print numbers from `1` to `n` in four formats on each line: decimal, octal, hexadecimal uppercase, and binary. Right-align each column using the width of `n` in binary.

## Final Accepted Solution
```python
if __name__ == '__main__':
    n = int(input())
    width = len(bin(n)) - 2

    for i in range(1, n + 1):
        print(f"{i:>{width}d} {i:>{width}o} {i:>{width}X} {i:>{width}b}")
```

## Plain-English Explanation
- `bin(n)` returns strings like `0b101`; subtract `2` to ignore `0b`.
- That binary length is used as a common column width.
- The loop prints each number in four bases.
- Format specifiers:
  - `d` decimal
  - `o` octal
  - `X` uppercase hexadecimal
  - `b` binary
- `:>{width}` right-aligns each value to the same width.

## Sample Inputs and Outputs
- Input: `5`
- Output:
  - `  1   1   1   1`
  - `  2   2   2  10`
  - `  3   3   3  11`
  - `  4   4   4 100`
  - `  5   5   5 101`

## Mistakes or Reminders
- Use uppercase `X` for uppercase hex.
- Width must come from binary length of `n`, not current `i`.
- Keep exact spacing/alignment for judge output matching.

## Review Checklist
- [ ] I can explain base format specifiers (`d`, `o`, `X`, `b`).
- [ ] I can compute dynamic column width from binary length.
- [ ] I can produce aligned multi-column output with f-strings.
