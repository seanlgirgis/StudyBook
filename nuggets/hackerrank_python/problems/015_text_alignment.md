# 015. Text Alignment

## Source
HackerRank Python - Strings

## Problem Summary
Given an odd integer `thickness`, complete the partial code to print the HackerRank logo by replacing blanks with the correct alignment methods: `rjust`, `ljust`, and `center`.

## Final Accepted Solution
```python
# Replace all ______ with rjust, ljust or center.

thickness = int(input())  # This must be an odd number
c = 'H'

# Top Cone
for i in range(thickness):
    print((c * i).rjust(thickness - 1) + c + (c * i).ljust(thickness - 1))

# Top Pillars
for i in range(thickness + 1):
    print((c * thickness).center(thickness * 2) + (c * thickness).center(thickness * 6))

# Middle Belt
for i in range((thickness + 1) // 2):
    print((c * thickness * 5).center(thickness * 6))

# Bottom Pillars
for i in range(thickness + 1):
    print((c * thickness).center(thickness * 2) + (c * thickness).center(thickness * 6))

# Bottom Cone
for i in range(thickness):
    print(((c * (thickness - i - 1)).rjust(thickness) + c + (c * (thickness - i - 1)).ljust(thickness)).rjust(thickness * 6))
```

## Plain-English Explanation
- `rjust(width)` right-aligns text within a width.
- `ljust(width)` left-aligns text within a width.
- `center(width)` centers text within a width.
- These methods are combined to build each logo section (cone, pillars, belt, and bottom cone).

## Sample Inputs and Outputs
- Input: `5`
- Output: HackerRank `H` logo pattern (multi-line aligned text)

## Mistakes or Reminders
- `thickness` must be odd for correct symmetry.
- Use exact widths shown in the formula.
- Do not remove spaces produced by alignment methods.

## Review Checklist
- [ ] I can explain `rjust`, `ljust`, and `center`.
- [ ] I can identify why each section needs different width values.
- [ ] I can keep formatting exact for pattern-print problems.

## Alternative Modular Learning Solution
```python
def draw_triangle(thickness, char, reverse=False, right_shift=0):
    rows = []
    for i in range(thickness):
        level = thickness - i - 1 if reverse else i
        row = (char * level).rjust(thickness - 1) + char + (char * level).ljust(thickness - 1)
        if right_shift:
            row = row.rjust(right_shift)
        rows.append(row)
    return rows


def draw_pillars(thickness, char):
    return [
        (char * thickness).center(thickness * 2) + (char * thickness).center(thickness * 6)
        for _ in range(thickness + 1)
    ]


def draw_belt(thickness, char):
    return [
        (char * thickness * 5).center(thickness * 6)
        for _ in range((thickness + 1) // 2)
    ]


def print_rows(rows):
    for row in rows:
        print(row)


thickness = int(input())
c = 'H'

# Top Cone
print_rows(draw_triangle(thickness=thickness, char=c))

# Top Pillars
print_rows(draw_pillars(thickness=thickness, char=c))

# Middle Belt
print_rows(draw_belt(thickness=thickness, char=c))

# Bottom Pillars
print_rows(draw_pillars(thickness=thickness, char=c))

# Bottom Cone
print_rows(draw_triangle(
    thickness=thickness,
    char=c,
    reverse=True,
    right_shift=thickness * 6 - 1
))
```
