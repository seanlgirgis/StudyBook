# ============================================================================
# File: decode_ways_091_empty.py
#
# LeetCode 91: Decode Ways (Medium)
#
# PROBLEM STATEMENT:
# A message containing letters from A-Z can be encoded into numbers using the 
# following mapping:
# 'A' -> "1", 'B' -> "2", ..., 'Z' -> "26"
#
# To decode an encoded message, all the digits must be grouped then mapped back 
# into letters using the reverse of the mapping above (there may be multiple ways).
# For example, "11106" can be mapped into:
# - "AAJF" with the grouping (1 1 10 6)
# - "KJF" with the grouping (11 10 6)
#
# Note that the grouping (1 11 06) is invalid because "06" cannot be mapped into 
# 'F' since "6" is different from "06".
#
# Given a string s containing only digits, return the number of ways to decode it.
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (s, expected_ways)
tests: List[Tuple[str, int]] = [
    ("12", 2),                    # 1. Standard example
    ("226", 3),                   # 2. Standard example
    ("06", 0),                    # 3. Leading zero (invalid)
    ("0", 0),                     # 4. Single zero
    ("10", 1),                    # 5. Valid zero mapping (10 -> J)
    ("27", 1),                    # 6. Number > 26 forces single digit decoding
    ("2101", 1),                  # 7. Zero in the middle
    ("11106", 2),                 # 8. LC Example
    ("1001", 0),                  # 9. Consecutive zeros (invalid)
    ("99999", 1),                 # 10. Boundary: All single digit decodings
    ("11111", 8),                 # 11. Boundary: Maximum overlapping decodings (Fibonacci sequence)
    ("26", 2),                    # 12. Exact boundary for 'Z'
    ("121", 3),
]

# --- TEST HARNESS ---
def harness(func: Callable[[str], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (s, expected) in enumerate(tests, 1):
        try:
            got = func(s)
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                s_disp = f"'{s}'" if len(s) <= 15 else f"'{s[:12]}...'"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | s={s_disp}")
        except Exception as e:
            s_disp = f"'{s}'" if len(s) <= 15 else f"'{s[:12]}...'"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | s={s_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def numDecodings(s: str) -> int:
    # SEAN mental model:
    # dp[i] = number of ways to decode prefix ending at index i.
    # We compress DP to O(1) space:
    # - prev1 = dp[i-1] (ways up to previous char)
    # - prev2 = dp[i-2] (ways up to char before previous)
    if not s:
        return 0

    # A message cannot start with '0'.
    if s[0] == '0':
        return 0

    # Base setup for first character:
    # dp[-1] = 1 (empty prefix), dp[0] = 1 (first char is non-zero here).
    prev2 = 1
    prev1 = 1
    
    for i in range(1, len(s)):
        curr = 0

        # Option 1: take one digit s[i] (valid only if not '0').
        if s[i] != '0':
            curr += prev1

        # Option 2: take two digits s[i-1:i+1] if between 10 and 26.
        two_digit = int(s[i - 1 : i + 1])
        if 10 <= two_digit <= 26:
            curr += prev2

        # Shift DP window for next position.
        prev2, prev1 = prev1, curr

    return prev1

# Execute harness without __main__ block
harness(numDecodings)
