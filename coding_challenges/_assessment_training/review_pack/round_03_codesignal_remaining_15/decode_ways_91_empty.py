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
    n = len(s)
    dp = [0] * (n + 1)
    dp[n] = 1

    for i in range(n - 1, -1, -1):
        if s[i] == '0':
            dp[i] = 0
            continue

        dp[i] = dp[i + 1]  # take one digit

        if i + 1 < n and 10 <= int(s[i:i+2]) <= 26:
            dp[i] += dp[i + 2]  # take two digits

    return dp[0]

def numDecodings_forward(s: str) -> int:
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        if s[i - 1] != '0':
            dp[i] += dp[i - 1]

        if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:
            dp[i] += dp[i - 2]

    return dp[n]


harness(numDecodings)

harness(numDecodings_forward)

