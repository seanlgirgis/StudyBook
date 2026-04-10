# LeetCode 242: Valid Anagram (Round 02 Empty)
from typing import Callable, List, Tuple

tests: List[Tuple[str, str, bool]] = [
    ("anagram", "nagaram", True),
    ("rat", "car", False),
    ("", "", True),
    ("a", "ab", False),
    ("listen", "silent", True),
    ("aacc", "ccac", False),
]


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
                print(f"Test {i}: FAILED | expected={expected}, got={result}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")


def isAnagram(s: str, t: str) -> bool:
    #Soluton is valid only for strings of lower case characters 
    lst1 = [0] * 26
    lst2 = [0] * 26
    for ch in s:
        lst1[ord(ch) - ord('a')] += 1
    for ch in t:
        lst2[ord(ch) - ord('a')] += 1
    
    return lst1 == lst2 


harness(isAnagram)

