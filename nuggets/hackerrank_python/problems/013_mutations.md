# 013. Mutations

## Source
HackerRank Python - Strings

## Problem Summary
Given a string, an index position, and a replacement character, return a new string where the character at that position is replaced. Since strings are immutable in Python, the original string cannot be edited in place.

## Final Accepted Solution
```python
def mutate_string(string, position, character):
    return string[:position] + character + string[position + 1:]

if __name__ == '__main__':
    s = input()
    i, c = input().split()
    s_new = mutate_string(s, int(i), c)
    print(s_new)
```

## Plain-English Explanation
- Use slicing to keep the part before the index: `string[:position]`.
- Add the new character.
- Add the part after the index: `string[position + 1:]`.
- Concatenate all parts to build a brand-new string.

## Sample Inputs and Outputs
- Input:
  - `abracadabra`
  - `5 k`
- Output: `abrackdabra`

- Input:
  - `hello`
  - `0 y`
- Output: `yello`

## Mistakes or Reminders
- Strings cannot be modified directly by index.
- Convert position from string to int before using it.
- Use `position + 1` for the right-side slice to skip old character.

## Review Checklist
- [ ] I can explain Python string immutability.
- [ ] I can replace one character using slicing.
- [ ] I can parse two values from one input line.
