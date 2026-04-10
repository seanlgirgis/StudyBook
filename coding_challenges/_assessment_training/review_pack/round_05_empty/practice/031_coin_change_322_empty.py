# ============================================================================
# File: coin_change_322_empty.py
#
# LeetCode 322: Coin Change (Medium)
# ============================================================================

from typing import Callable, List, Tuple
from functools import lru_cache


# --- TEST CASES ---
# Format: (coins, amount, expected_fewest_coins)
tests: List[Tuple[List[int], int, int]] = [
    ([1, 2, 5], 11, 3),
    ([2], 3, -1),
    ([1], 0, 0),
    ([1], 1, 1),
    ([1], 2, 2),
    ([2, 5, 10, 1], 27, 4),
    ([186, 419, 83, 408], 6249, 20),
    ([3, 7, 405, 436], 8839, 25),
    ([2, 4, 6, 8], 15, -1),
    ([10000], 10000, 1),
]


def harness(func: Callable[[List[int], int], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (coins, amount, expected) in enumerate(tests, 1):
        try:
            got = func(coins.copy(), amount)
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={got} | amount={amount}, coins={coins}")
        except Exception as e:
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | amount={amount}, coins={coins}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


def coinChange(coins: List[int], amount: int) -> int:
    # Optional for pruning behavior in top-down exploration (not required for correctness).
    coins = sorted(coins, reverse=True)
    INF = amount + 1

    @lru_cache(maxsize=None)
    def make_change(rem: int) -> int:
        # Exact change reached.
        if rem == 0:
            return 0
        if rem < 0:
            return INF

        best = INF
        for c in coins:
            coins_needed = make_change(rem - c)
            if coins_needed != INF:
                best = min(best, coins_needed + 1)
        return best

    ans = make_change(amount)
    make_change.cache_clear()  # hygiene for repeated harness calls
    return ans if ans != INF else -1


harness(coinChange)


def coinChange_bottom_up(coins: List[int], amount: int) -> int:
    # Bottom-up DP: often safer under interview pressure (no recursion depth concerns).
    INF = amount + 1
    dp = [INF] * (amount + 1)
    dp[0] = 0

    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], dp[a - c] + 1)

    return dp[amount] if dp[amount] != INF else -1


harness(coinChange_bottom_up)
