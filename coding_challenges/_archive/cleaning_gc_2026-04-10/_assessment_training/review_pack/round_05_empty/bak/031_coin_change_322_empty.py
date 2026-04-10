# ============================================================================
# File: coin_change_322_empty.py
#
# LeetCode 322: Coin Change (Medium)
#
# PROBLEM STATEMENT:
# You are given an integer array `coins` representing coins of different 
# denominations and an integer `amount` representing a total amount of money.
#
# Return the fewest number of coins that you need to make up that amount. 
# If that amount of money cannot be made up by any combination of the coins, 
# return -1.
#
# You may assume that you have an infinite number of each kind of coin.
#
# EXAMPLES:
# 1) coins = [1, 2, 5], amount = 11 -> Expected: 3 
#    Explanation: 11 = 5 + 5 + 1
# 2) coins = [2], amount = 3 -> Expected: -1
# 3) coins = [1], amount = 0 -> Expected: 0
# ============================================================================

from typing import Callable, List, Tuple
import math
import sys
from functools import lru_cache

# --- TEST CASES ---
# Format: (coins, amount, expected_fewest_coins)
tests: List[Tuple[List[int], int, int]] = [
    ([1, 2, 5], 11, 3),                  # Standard Example 1
    ([2], 3, -1),                        # Standard Example 2 (Impossible)
    ([1], 0, 0),                         # Standard Example 3 (Zero amount)
    ([1], 1, 1),                         # Edge Case: Single coin matches amount
    ([1], 2, 2),                         # Edge Case: Multiple of single coin
    ([2, 5, 10, 1], 27, 4),              # Standard DP case (10+10+5+2)
    ([186, 419, 83, 408], 6249, 20),     # Boundary: Classic case that defeats greedy algorithms
    ([3, 7, 405, 436], 8839, 25),        # Boundary: Large amount with awkward denominations
    ([2, 4, 6, 8], 15, -1),              # Boundary: Even coins, odd amount (Impossible)
    ([10000], 10000, 1),                 # Boundary: Exactly one large coin
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int], int], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (coins, amount, expected) in enumerate(tests, 1):
        try:
            # Pass a copy of coins to prevent accidental mutation by the function
            got = func(coins.copy(), amount)
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                coins_disp = str(coins) if len(coins) <= 10 else f"[{str(coins[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | amount={amount}, coins={coins_disp}")
        except Exception as e:
            coins_disp = str(coins) if len(coins) <= 10 else f"[{str(coins[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | amount={amount}, coins={coins_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def coinChange(coins: List[int], amount: int) -> int:
    # Sean style mental model:
    # "What is the minimum number of coins needed to build the remaining amount rem?"
    # dfs(rem) returns that minimum. We memoize dfs(rem) so each remainder is solved once.

    # Defensive recursion limit for large test amounts in top-down recursion.
    sys.setrecursionlimit(max(10000, amount + 100))

    # Sorting descending is not required for correctness,
    # but can help find good candidates earlier in practice.
    coins = sorted(coins, reverse=True)

    @lru_cache(maxsize=None)
    def dfs(rem: int) -> int:
        # Base case: exact amount reached -> no more coins needed.
        if rem == 0:
            return 0
        # Base case: overshot amount -> impossible path.
        if rem < 0:
            return math.inf

        # Try every coin as the next step; keep the best valid answer.
        best = math.inf
        for c in coins:
            coins_needed = dfs(rem - c)
            if coins_needed != math.inf:
                best = min(best, coins_needed + 1)

        return best

    ans = dfs(amount)
    # Clear cache explicitly to avoid retaining memoized state beyond this call.
    dfs.cache_clear()
    return ans if ans != math.inf else -1


harness(coinChange)
