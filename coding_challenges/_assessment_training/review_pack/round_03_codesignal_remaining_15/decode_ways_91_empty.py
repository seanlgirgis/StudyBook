# LeetCode 91: Decode Ways (Empty)
#
# PROBLEM STATEMENT
# A message containing digits can be decoded with mapping 1->A ... 26->Z.
# Return the total number of valid decodings.
#
# EXAMPLES
# "12" -> 2 ("AB", "L")
# "226" -> 3 ("BZ", "VF", "BBF")
# "06" -> 0
#
# WHAT TO IMPLEMENT
# Implement `numDecodings(s)` (DP over positions).
from typing import Callable, List, Tuple

tests: List[Tuple[str, int]] = [
    ("12", 2),
    ("226", 3),
    ("06", 0),
    ("11106", 2),
    ("10", 1),
    ("27", 1),
    ("2101", 1),
    ("10011", 0),
]

def harness(func: Callable[[str], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (s, expected) in enumerate(tests, 1):
        try:
            got = func(s)
            if got == expected: print(f"Test {i}: PASSED"); passed += 1
            else: print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

def numDecodings(s: str) -> int:
    pass

harness(numDecodings)

