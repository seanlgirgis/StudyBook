# ============================================================================
# File: lc_020_valid_parentheses.py
#
# LeetCode 20: Valid Parentheses (Easy)
#
# PROBLEM STATEMENT:
# Given a string s containing just the characters '(', ')', '{', '}', '[' 
# and ']', determine if the input string is valid.
#
# An input string is valid if:
# 1. Open brackets must be closed by the same type of brackets.
# 2. Open brackets must be closed in the correct order.
# 3. Every close bracket has a corresponding open bracket of the same type.
# ============================================================================

from typing import List, Callable

# --- TEST CASES ---
# Format: {"kwargs": {...}, "expected": ...}
valid_parentheses_tests: List[dict] = [
    {
        "kwargs": {"s": "()"},
        "expected": True
    },
    {
        "kwargs": {"s": "()[]{}"},
        "expected": True
    },
    {
        "kwargs": {"s": "(]"},
        "expected": False
    },
    {
        "kwargs": {"s": "([])"},
        "expected": True
    },
    {
        # Edge case: Missing closing bracket
        "kwargs": {"s": "{"},
        "expected": False
    },
    {
        # Edge case: Missing opening bracket
        "kwargs": {"s": "]"},
        "expected": False
    }
]

# --- TEST HARNESS ---
def test_harness(func: Callable, test_cases: List[dict]) -> None:
    """
    Test harness for LeetCode #20: Valid Parentheses.
    Validates boolean output against expected validity.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0
    
    for i, tc in enumerate(test_cases):
        kwargs = tc["kwargs"]
        expected: bool = tc["expected"]
        
        try:
            # Execute the target function directly
            result = func(**kwargs)
            
            if result is None:
                print(f"Test {i+1}: FAILED | Got None, Expected {expected}")
            elif result == expected:
                print(f"Test {i+1}: PASSED (s='{kwargs['s']}')")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Got {result}, Expected {expected} (s='{kwargs['s']}')")
                        
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {type(e).__name__}: {e}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def isValid(s: str) -> bool:
    lookup = {'}': '{', ']': '[', ')': '('}
    stack: List[str] = []
    for ch in s:
        if ch in lookup:  # Closing
            if not stack:
                return False
            if stack[-1] != lookup[ch]:
                return False
            stack.pop()
        else:           #push to stack openings only
            stack.append(ch)
    return not stack
        
        
        


# Execute harness without __main__ block
test_harness(isValid, valid_parentheses_tests)
