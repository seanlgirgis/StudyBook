# ============================================================================
# File: 012_lc_125_valid_palindrome.py
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
# 1) s = "A man, a plan, a canal: Panama" -> Expected: True
#    Explanation: "amanaplanacanalpanama" is a palindrome.
# 2) s = "race a car" -> Expected: False
#    Explanation: "raceacar" is not a palindrome.
# 3) s = " " -> Expected: True
#    Explanation: s is an empty string "" after removing non-alphanumeric characters.
#    Since an empty string reads the same forward and backward, it is a palindrome.
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (s, expected_boolean)
tests: List[Tuple[str, bool]] = [
    ("A man, a plan, a canal: Panama", True),  # Standard Example 1
    ("race a car", False),                     # Standard Example 2
    (" ", True),                               # Standard Example 3
    ("0P", False),                             # Edge Case: Number and letter mismatch
    ("ab_a", True),                            # Edge Case: Underscore is non-alphanumeric
    ("1b1", True),                             # Boundary: Numbers are valid
    (".,", True),                              # Boundary: Only punctuation reduces to empty
    ("a.", True),                              # Boundary: Single character with punctuation
    ("Madam, in Eden, I'm Adam", True),        # Complex standard palindrome
    ("No 'x' in Nixon", True),                 # Complex standard palindrome
    ("Was it a car or a cat I saw?", True),    # Complex standard palindrome
    ("12321", True),                           # Numeric palindrome
    ("123a321", True),                         # Mixed alphanumeric palindrome
    ("abc", False),                            # Boundary: Simple non-palindrome
]

# --- TEST HARNESS ---
def harness(func: Callable[[str], bool]) -> None:
    """
    Test harness for LeetCode #125: Valid Palindrome.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (s, expected) in enumerate(tests, 1):
        try:
            got = func(s)
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                s_disp = f"'{s}'" if len(s) <= 25 else f"'{s[:22]}...'"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | s={s_disp}")
        except Exception as e:
            s_disp = f"'{s}'" if len(s) <= 25 else f"'{s[:22]}...'"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | s={s_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def isPalindrome(s: str) -> bool:
    l, r = 0, len(s) -1
    
    while l < r:
        while l < r and not s[l].isalnum():
            l += 1
        while l < r and not s[r].isalnum():
            r -= 1
        if s[l].lower() != s[r].lower():
            return False
        else:
            l += 1
            r -= 1
    return True
            
            
         


# Execute harness without __main__ block
harness(isPalindrome)