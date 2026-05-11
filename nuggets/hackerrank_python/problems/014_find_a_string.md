# 014. Find a string

## Source
HackerRank Python - Strings

## Problem Summary
Given an original string and a substring, count how many times the substring occurs in the original string. Count overlapping matches while searching from left to right. Comparison is case-sensitive.

## Final Accepted Solution
```python
def count_substring(string, sub_string):
    count = 0
    n1, n2 = len(string), len(sub_string)

    for i in range(n1):
        if i + n2 > n1:
            break

        if string[i:i + n2] == sub_string:
            count += 1

    return count


if __name__ == '__main__':
    string = input().strip()
    sub_string = input().strip()

    count = count_substring(string, sub_string)
    print(count)
```

## Plain-English Explanation
This problem asks us to count how many times a substring appears inside a larger string.

The important detail is that overlapping matches count.

Example:
Original string:
`ABCDCDC`

Substring:
`CDC`

The substring `CDC` appears starting at index 2:
`AB[CDC]DC`

It also appears starting at index 4:
`ABCD[CDC]`

So the answer is `2`.

The line `n1, n2 = len(string), len(sub_string)` stores:
- `n1` as the length of the full string
- `n2` as the length of the substring

The loop `for i in range(n1):` checks each possible starting index in the original string.

The slice `string[i:i + n2]` takes a piece of the original string with the same length as `sub_string`.

Example:
- `string = "ABCDCDC"`
- `sub_string = "CDC"`
- `n2 = 3`

At `i = 2`, `string[2:5]` gives `"CDC"`.
At `i = 4`, `string[4:7]` gives `"CDC"`.

The condition `if string[i:i + n2] == sub_string:` means:
if the current slice matches the substring, increase `count`.

The condition `if i + n2 > n1: break` prevents checks when there are not enough characters left.

Important learning notes:
- `len(string)` gives the number of characters.
- `range(n1)` loops from `0` to `n1 - 1`.
- Slicing uses `string[start:end]`.
- The end index is excluded.
- `string[i:i + n2]` gives a window the same size as the substring.
- This method counts overlapping matches.
- String comparison is case-sensitive.

## Sample Inputs and Outputs
- Input:
  - `ABCDCDC`
  - `CDC`
- Output: `2`

## Mistakes or Reminders
- Do not use `string.count(sub_string)` when overlapping matches matter.
- Search left to right using window slices.
- Remember Python slice end index is excluded.
- Keep function name `count_substring` for HackerRank compatibility.
- Return `count`; do not print inside the function.

## Review Checklist
- [ ] I can explain why overlapping matches require manual scanning.
- [ ] I can use slicing windows to compare substrings.
- [ ] I can explain `i + n2 > n1` as a boundary guard.
- [ ] I can describe why `count()` is insufficient for overlap cases.
