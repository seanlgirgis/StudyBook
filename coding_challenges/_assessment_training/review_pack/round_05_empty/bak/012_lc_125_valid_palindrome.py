# ============================================================================
# File: lc_125_valid_palindrome.py
#
# LeetCode 125: Valid Palindrome (Easy)
#
# PROBLEM STATEMENT:
# A phrase is a palindrome if, after converting all uppercase letters into 
# lowercase letters and removing all non-alphanumeric characters, it reads 
# the same forward and backward. Alphanumeric characters include letters and numbers.
# 
# Given a string s, return true if it is a palindrome, or false otherwise.
#
# EXAMPLES:
# - s = "A man, a plan, a canal: Panama" -> Expected: True
#   Explanation: "amanaplanacanalpanama" is a palindrome.
# - s = "race a car" -> Expected: False
#   Explanation: "raceacar" is not a palindrome.
# - s = " " -> Expected: True
#   Explanation: s is an empty string "" after removing non-alphanumeric 
#   characters. Since an empty string reads the same forward and backward, 
#   it is a palindrome.
# ============================================================================

from typing import List, Callable

# --- TEST CASES ---
# Format: {"kwargs": {...}, "expected": ...}
valid_palindrome_tests: List[dict] = [
    {
        # Standard Example 1 (Mixed case and punctuation)
        "kwargs": {"s": "A man, a plan, a canal: Panama"},
        "expected": True
    },
    {
        # Standard Example 2 (Not a palindrome)
        "kwargs": {"s": "race a car"},
        "expected": False
    },
    {
        # Standard Example 3 / Boundary (Whitespace only)
        "kwargs": {"s": " "},
        "expected": True
    },
    {
        # Boundary: Empty string
        "kwargs": {"s": ""},
        "expected": True
    },
    {
        # Boundary: All non-alphanumeric characters
        "kwargs": {"s": ".,,!!@#"},
        "expected": True
    },
    {
        # Boundary: Single character
        "kwargs": {"s": "a"},
        "expected": True
    },
    {
        # Edge case: Numbers only (Valid)
        "kwargs": {"s": "12321"},
        "expected": True
    },
    {
        # Edge case: Mixed letters and numbers (Valid)
        "kwargs": {"s": "1b1"},
        "expected": True
    },
    {
        # Edge case: Mixed letters and numbers (Invalid)
        "kwargs": {"s": "0P"},
        "expected": False
    }
]

# --- TEST HARNESS ---
def test_harness(func: Callable, test_cases: List[dict]) -> None:
    """
    Test harness for LeetCode #125: Valid Palindrome.
    Validates boolean output against expected true/false validity.
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
                # Formatting the output to stay readable if strings are very long
                s_display = kwargs['s']
                if len(s_display) > 30:
                    s_display = s_display[:27] + "..."
                print(f"Test {i+1}: PASSED (s='{s_display}')")
                passed += 1
            else:
                s_display = kwargs['s']
                if len(s_display) > 20:
                    s_display = s_display[:17] + "..."
                print(f"Test {i+1}: FAILED | Got {result}, Expected {expected} (s='{s_display}')")
                        
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {type(e).__name__}: {e}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def isPalindrome(s: str) -> bool:
    # 2 Pointers algorithm
    # if not isalphanum() skip
    # if isalphanum .. compare lower case both.. if not equal return False
    # use l < r to naturally skip middle char in odd-length filtered strings
    
    l, r = 0, len(s) -1
    
    while l < r:
        #First prune
        while l < r and not s[l].isalnum():
            l += 1
        while l < r and not s[r].isalnum():
            r -= 1
        
        if s[l].lower() != s[r].lower():
            return False
        l += 1
        r -= 1
        
    return True
         
        


# Execute harness without __main__ block
test_harness(isPalindrome, valid_palindrome_tests)