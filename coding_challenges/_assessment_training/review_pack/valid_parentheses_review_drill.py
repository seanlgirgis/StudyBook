# LeetCode 20: Valid Parentheses (Review Drill)

from typing import Callable, List, Tuple


# --- TEST CASES ---
# Format: (input_string, expected_bool)
valid_parentheses_tests: List[Tuple[str, bool]] = [
    ("()", True),
    ("()[]{}", True),
    ("(]", False),
    ("([)]", False),
    ("{[]}", True),
    ("((()))", True),
    (")", False),
    ("(", False),
    ("[", False),
    ("", True),
    ("(((((((((())))))))))", True),
    ("(((())))]", False),
]


# --- TEST HARNESS ---
def test_harness(
    func: Callable[[str], bool],
    test_cases: List[Tuple[str, bool]],
) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0
    for i, (s, expected) in enumerate(test_cases):
        try:
            result: bool = func(s)
            if result == expected:
                print(f"Test {i + 1}: PASSED (s='{s}')")
                passed += 1
            else:
                print(f"Test {i + 1}: FAILED (s='{s}')")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
        except Exception as e:
            print(f"Test {i + 1}: ERROR | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.")


# --- YOUR IMPLEMENTATION ---
def isValid(s: str) -> bool:
    """
    Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
    determine if the input string is valid.

    An input string is valid if:
    1) Open brackets are closed by the same type of brackets.
    2) Open brackets are closed in the correct order.
    3) Every close bracket has a corresponding open bracket.
    """
    if len(s) == 0 : return True
    if len(s)% 2 != 0 : return False 
    phash = {'}':'{' , ']':'[' , ')':'('}
    stack = []
    for ch in s:
        if ch not in phash:    # it is an open for a pair
            stack.append(ch)
        else:                  #it is a closing 
            if not stack or stack[-1] != phash[ch]:
                return False
            else:
                stack.pop()
    return not stack
            


test_harness(isValid, valid_parentheses_tests)
