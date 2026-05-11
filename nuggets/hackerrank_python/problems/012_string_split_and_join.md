# 012. String Split and Join

## Source
HackerRank Python - Strings

## Problem Summary
Given a string of space-separated words, split the string on spaces and join the words back together using hyphens.

## Final Accepted Solution
```python
def split_and_join(line):
    words = line.split(" ")
    return "-".join(words)

if __name__ == '__main__':
    line = input()
    result = split_and_join(line)
    print(result)
```

## Plain-English Explanation
- `split(" ")` breaks the input string into a list of words.
- `"-".join(words)` combines those words with `-` between each one.
- Returning the transformed string keeps the function reusable.

## Sample Inputs and Outputs
- Input: `this is a string`
- Output: `this-is-a-string`

- Input: `python is fun`
- Output: `python-is-fun`

## Mistakes or Reminders
- Use `join` on the delimiter string (`"-"`), not on the list.
- Keep delimiter exactly as a single space in `split(" ")` to match prompt.
- Return the result from the function before printing.

## Review Checklist
- [ ] I can explain how `split` and `join` work together.
- [ ] I can transform delimiters between words.
- [ ] I can write a clean input -> function -> print pattern.
