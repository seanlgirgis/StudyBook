# ============================================================================
# File: valid_anagram_242_empty.py
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
    ("listen", "silent", True),                    # Standard Example 3
    ("aacc", "ccac", False),                       # Boundary: Same length, different frequencies
    ("a", "a", True),                              # Edge case: Single character (identical)
    ("racecar", "carrace", True),                  # Standard Example 4
    ("ab", "ba", True),                            # Boundary: Small minimal swap
    ("a" * 1000, "a" * 1000, True),                # Boundary: Long identical strings
    ("a" * 1000 + "b", "a" * 1000 + "c", False),   # Boundary: Long strings differing by one char at the end
]

# --- TEST HARNESS ---
def harness(func: Callable[[str, str], bool]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (s, t, expected) in enumerate(tests, 1):
        try:
            result = func(s, t)
            if result == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                s_display = f"'{s}'" if len(s) <= 15 else f"'{s[:12]}...'"
                t_display = f"'{t}'" if len(t) <= 15 else f"'{t[:12]}...'"
                print(f"Test {i}: FAILED | expected={expected}, got={result} | s={s_display}, t={t_display}")
        except Exception as e:
            s_display = f"'{s}'" if len(s) <= 15 else f"'{s[:12]}...'"
            t_display = f"'{t}'" if len(t) <= 15 else f"'{t[:12]}...'"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | s={s_display}, t={t_display}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    lst1, lst2 = [0] * 26, [0] * 26
    for ch in s:
        lst1[ord(ch) - ord('a')] += 1
    
    for ch in t:
        lst2[ord(ch) - ord('a')] += 1
        
    return lst1 == lst2


# Execute harness without __main__ block
harness(isAnagram)


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def isAnagram_with_all(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    lst1 = [0] * 26
    for ch in s:
        lst1[ord(ch) - ord('a')] += 1
    
    for ch in t:
        lst1[ord(ch) - ord('a')] -= 1
        
    return all(x == 0 for x in lst1)


# Execute harness without __main__ block
harness(isAnagram_with_all)
