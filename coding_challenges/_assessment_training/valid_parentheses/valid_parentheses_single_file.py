# LeetCode 20: Valid Parentheses

from typing import Callable, List, Tuple

# --- PROBLEM STATEMENT ---
# Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
# determine if the input string is valid.
#
# An input string is valid if:
# 1) Open brackets are closed by the same type of brackets.
# 2) Open brackets are closed in the correct order.
# 3) Every close bracket has a corresponding open bracket.
#
# Constraints:
# - 1 <= len(s) <= 10^4
# - s consists of parentheses only '()[]{}'

# --- TEST CASES ---
# Format: (input_string, expected_bool)
valid_parentheses_tests: List[Tuple[str, bool]] = [
    ("()", True),                 # 1. Simple pair
    ("()[]{}", True),             # 2. Multiple valid types
    ("(]", False),                # 3. Mismatched pair
    ("([)]", False),              # 4. Wrong order nesting
    ("{[]}", True),               # 5. Proper nested mixed types
    ("((()))", True),             # 6. Deep same-type nesting
    (")", False),                 # 7. Starts with close
    ("(", False),                 # 8. Unclosed open
    ("[", False),                 # 9. Unclosed open bracket
    ("", False),                  # 10. Out-of-constraint empty string (robustness)
    ("(((((((((())))))))))", True), # 11. Long balanced sequence
    ("(((())))]", False),         # 12. Extra closing bracket
]

# --- TEST HARNESS ---
def test_harness(func: Callable[[str], bool], test_cases: List[Tuple[str, bool]]) -> None:
    """
    Test harness for LeetCode #20: Valid Parentheses.
    Validates stack-based bracket matching logic.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0

    for i, (s, expected) in enumerate(test_cases):
        try:
            result: bool = func(s)

            if result == expected:
                display_s = s if len(s) <= 20 else s[:20] + "..."
                print(f"Test {i+1}: PASSED (s='{display_s}')")
                passed += 1
            else:
                display_s = s if len(s) <= 20 else s[:20] + "..."
                print(f"Test {i+1}: FAILED | s='{display_s}'")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
        except Exception as e:
            display_s = s if len(s) <= 20 else s[:20] + "..."
            print(f"Test {i+1}: ERROR  | s='{display_s}' | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def isValid(s: str) -> bool:
    """
    LC 20 — Valid Parentheses

    PROBLEM:
    Given a string `s` containing only brackets, return `True` if valid, else `False`.

    HINT / APPROACH:
    1. Pattern: Stack.
    2. Push opening brackets onto stack.
    3. For each closing bracket:
       - stack must not be empty
       - top of stack must be matching opening bracket
       - then pop
    4. At end, stack must be empty for valid string.

    Time:  O(n)
    Space: O(n)
    
    """
    if len(s) < 1: return False
    pmap = {'}':'{',']':'[',')':'('}
    stack=[]
    for ch in s:
        if ch in pmap:
            if stack and stack.pop() == pmap[ch]:
                pass
            else:
                return False
        else:
            stack.append(ch)
    return not stack

            
        
    


# Execute harness without __main__ block
test_harness(isValid, valid_parentheses_tests)
