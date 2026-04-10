# ============================================================================
# File: 021_valid_anagram_242_empty.py
#
# LeetCode 242: Valid Anagram (Easy)
#
# PROBLEM STATEMENT:
# Given two strings s and t, return true if t is an anagram of s, and false otherwise.
#
# An Anagram is a word or phrase formed by rearranging the letters of a 
# different word or phrase, typically using all the original letters exactly once.
#
# EXAMPLES:
# 1) s = "anagram", t = "nagaram" -> Expected: True
# 2) s = "rat", t = "car" -> Expected: False
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (s, t, expected_boolean)
tests: List[Tuple[str, str, bool]] = [
    ("anagram", "nagaram", True),                  # Standard Example 1
    ("rat", "car", False),                         # Standard Example 2
    ("", "", True),                                # Edge case: Empty strings
    ("a", "ab", False),                            # Boundary: t is longer than s
    ("ab", "a", False),                            # Boundary: s is longer than t
    ("listen", "silent", True),                    # Standard Valid Anagram
    ("aacc", "ccac", False),                       # Boundary: Same length, different frequencies
    ("a", "a", True),                              # Edge case: Single character (identical)
    ("racecar", "carrace", True),                  # Standard Palindrome Anagram
    ("ab", "ba", True),                            # Boundary: Small minimal swap
    ("a" * 1000, "a" * 1000, True),                # Boundary: Long identical strings
    ("a" * 1000 + "b", "a" * 1000 + "c", False),   # Boundary: Long strings differing by one char at the end
]

# --- TEST HARNESS ---
def harness(func: Callable[[str, str], bool]) -> None:
    """
    Test harness for LeetCode #242: Valid Anagram.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (s, t, expected) in enumerate(tests, 1):
        try:
            got = func(s, t)

            if not isinstance(got, bool):
                raise AssertionError(f"Output must be bool. got={type(got).__name__}")
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                s_disp = f"'{s}'" if len(s) <= 15 else f"'{s[:12]}...'"
                t_disp = f"'{t}'" if len(t) <= 15 else f"'{t[:12]}...'"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | s={s_disp}, t={t_disp}")
        except Exception as e:
            s_disp = f"'{s}'" if len(s) <= 15 else f"'{s[:12]}...'"
            t_disp = f"'{t}'" if len(t) <= 15 else f"'{t[:12]}...'"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | s={s_disp}, t={t_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    freq = [0] * 26
    for ch in s:
        freq[ord(ch) - ord("a")] += 1

    for ch in t:
        idx = ord(ch) - ord("a")
        freq[idx] -= 1
        if freq[idx] < 0:
            return False

    return True

# Execute harness without __main__ block
harness(isAnagram)
