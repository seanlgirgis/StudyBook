# ============================================================================
# File: 005_lc_020_valid_parentheses.py
#
# LeetCode 20: Valid Parentheses (Easy)
#
# PROBLEM STATEMENT:
# Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
# determine if the input string is valid.
#
# An input string is valid if:
# 1. Open brackets must be closed by the same type of brackets.
# 2. Open brackets must be closed in the correct order.
# 3. Every close bracket has a corresponding open bracket of the same type.
#
# EXAMPLES:
# 1) s = "()" -> Expected: True
# 2) s = "()[]{}" -> Expected: True
# 3) s = "(]" -> Expected: False
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (s, expected_boolean)
tests: List[Tuple[str, bool]] = [
    ("()", True),                          # Standard Example 1
    ("()[]{}", True),                      # Standard Example 2
    ("(]", False),                         # Standard Example 3
    ("", True),                            # Edge Case: Empty string is valid
    ("([)]", False),                       # Interleaved brackets (Invalid)
    ("{[]}", True),                        # Nested brackets (Valid)
    ("[", False),                          # Edge Case: Single opening bracket
    ("]", False),                          # Edge Case: Single closing bracket
    ("((((((", False),                     # Boundary: All opening brackets
    ("))))))", False),                     # Boundary: All closing brackets
    ("((([{()}])))", True),                # Boundary: Deeply nested valid
    ("((([{()}]))]", False),               # Boundary: Deeply nested invalid
    ("()()()()()()()()", True),            # Sequence of independent valid pairs
    ("{[()]}[]({})", True),                # Mixed nested + sequential valid
    ("{[()]}[]({)}", False),               # One mismatched closer in long sequence
    ("abc", False),                        # Robustness: invalid non-bracket chars
]

# --- TEST HARNESS ---
def harness(func: Callable[[str], bool]) -> None:
    """
    Test harness for LeetCode #20: Valid Parentheses.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (s, expected) in enumerate(tests, 1):
        try:
            got = func(s)

            if not isinstance(got, bool):
                raise AssertionError(f"Output must be bool. got={type(got).__name__}")
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                s_disp = f"'{s}'" if len(s) <= 15 else f"'{s[:12]}...'"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | s={s_disp}")
        except Exception as e:
            s_disp = f"'{s}'" if len(s) <= 15 else f"'{s[:12]}...'"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | s={s_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def isValid(s: str) -> bool:
    pair_map = {'}': '{', ']': '[', ')': '('}
    opening = set(pair_map.values())
    stack: List[str] = []

    if len(s) % 2 != 0:
        return False

    for ch in s:
        if ch in opening:
            stack.append(ch)
            continue

        if ch not in pair_map:
            return False

        if stack and stack[-1] == pair_map[ch]:
            stack.pop()
        else:
            return False

    return not stack


# Execute harness without __main__ block
harness(isValid)
