# 011. sWAP cASE

## Source
HackerRank Python - Strings

## Problem Summary
Given a string, swap the case of every letter. Lowercase letters become uppercase, and uppercase letters become lowercase. Numbers, spaces, punctuation, and quotes stay unchanged.

## Final Accepted Solution
```python
def swap_case(s):
    return s.swapcase()

if __name__ == '__main__':
    s = input()
    result = swap_case(s)
    print(result)
```

## Plain-English Explanation
- Python strings have a built-in method `swapcase()`.
- It flips each letter's case automatically.
- Non-letter characters are not modified.
- Wrapping it in `swap_case` keeps the solution clean and reusable.

## Sample Inputs and Outputs
- Input: `HackerRank.com presents "Pythonist 2"`
- Output: `hACKERrANK.COM PRESENTS "pYTHONIST 2"`

- Input: `Hello World!`
- Output: `hELLO wORLD!`

## Mistakes or Reminders
- Do not manually loop unless required; `swapcase()` is the simplest approach.
- `swapcase()` returns a new string (strings are immutable).
- Keep spaces, digits, and punctuation unchanged.

## Review Checklist
- [ ] I can explain what `swapcase()` does.
- [ ] I can state why non-letters stay unchanged.
- [ ] I can write a small wrapper function and print the result.
