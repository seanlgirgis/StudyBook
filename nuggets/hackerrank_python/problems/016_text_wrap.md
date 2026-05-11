# 016. Text Wrap

## Source
HackerRank Python - Strings

## Problem Summary
Given a long string and a maximum width, wrap the string into lines of that width and return one string containing newline characters where line breaks should be.

## Final Accepted Solution
```python
import textwrap

def wrap(string, max_width):
    return "\n".join(textwrap.wrap(string, max_width))

if __name__ == '__main__':
    string, max_width = input(), int(input())
    result = wrap(string, max_width)
    print(result)
```

## Plain-English Explanation
- `textwrap.wrap(string, max_width)` splits the string into chunks up to `max_width`.
- It returns a list of wrapped lines.
- `"\n".join(...)` combines those lines into one printable string with line breaks.
- Returning the wrapped string keeps the function reusable and clean.

## Sample Inputs and Outputs
- Input:
  - `ABCDEFGHIJKLIMNOQRSTUVWXYZ`
  - `4`
- Output:
  - `ABCD`
  - `EFGH`
  - `IJKL`
  - `IMNO`
  - `QRST`
  - `UVWX`
  - `YZ`

## Mistakes or Reminders
- Convert `max_width` input to integer.
- Use `"\n".join(...)` to return a single string.
- Keep function name `wrap` for HackerRank checker compatibility.

## Review Checklist
- [ ] I can use Python standard library `textwrap` for line wrapping.
- [ ] I can explain list-to-string joining with newline separators.
- [ ] I can keep input parsing concise and readable.
