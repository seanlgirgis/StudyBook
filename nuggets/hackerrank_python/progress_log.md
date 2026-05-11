# Progress Log

## 2026-05-09

- 036 Mod Divmod

Learning notes:
- modulo operator `%`
- `if / elif / else`
- chained comparisons like `2 <= n <= 5`
- functions and return values
- `for` loops and `range`
- `print(end="")`
- classes and custom methods (`__sub__`, `dot`, `cross`)
- vector math basics (dot product, cross product, magnitude)
- radians to degrees and two-decimal formatting
- list comprehensions for generating and filtering combinations
- lexicographic output order from nested loop structure
- one-pass max and runner-up tracking
- handling duplicate highest values correctly
- grouping students by score with dictionary of lists
- sorting unique scores, then sorting names for stable output
- parsing name + variable-length scores with `*line`
- formatting numeric output with f-strings like `:.2f`
- command-driven list operations (`append`, `insert`, `remove`, `sort`, `reverse`, `pop`)
- difference between removing by value (`remove`) and by position (`pop`)
- tuple creation from iterable input
- using `hash()` on immutable tuple values
- using string method `swapcase()` for fast case conversion
- transforming delimiters with `split()` and `join()`
- string slicing for one-character replacement
- Python string immutability in practice
- counting overlapping substring matches with sliding slices
- why `string.count()` is not enough for overlap cases
- direct `any(...)` already returns boolean (no ternary needed)
- preserve strict output order in multi-line validator problems
- using `rjust`, `ljust`, and `center` to control visual text layout
- wrapping lines with `textwrap.wrap` and joining with newline characters
- symmetric top/middle/bottom pattern construction with controlled width
- f-string formatting for decimal/octal/hex/binary aligned columns
- mirrored alphabet pattern generation with dynamic width and padding
- preserving original spaces with `split(" ")` and `" ".join(...)`
- set command behavior differences: `pop`, `remove`, `discard`
- set union gives unique members from either set
- set intersection gives common members in both sets
- set difference gives members in first set but not second
- set symmetric difference gives members in either set but not both
- in-place set mutation methods update one base set across multiple commands
- `Counter` helps detect the single unique frequency quickly
- Updated strict superset solution to explicitly check both subset inclusion and larger set size.
- chunk-based deduplication with per-chunk seen tracking while preserving character order
- divmod returns quotient and remainder together as a tuple
- pow(a, b, m) performs modular exponentiation directly
- repeated-1 arithmetic trick for printing repeated digits without strings
- permutations return tuples that must be joined into strings for output
- combinations_with_replacement allows repeated choices while keeping combination order rules
- groupby handles consecutive runs, not global frequency counts
- combination probability uses favorable outcomes over total position-based combinations
- zip(*rows) transposes subject-wise input into student-wise groups for averaging

