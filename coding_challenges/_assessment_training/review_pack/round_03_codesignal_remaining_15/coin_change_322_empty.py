# LeetCode 322: Coin Change (Empty)
#
# PROBLEM STATEMENT
# Given coin denominations and an amount, return the fewest number of coins needed to make
# that amount. Return -1 if impossible.
#
# EXAMPLES
# coins=[1,2,5], amount=11 -> 3 (5+5+1)
# coins=[2], amount=3 -> -1
#
# WHAT TO IMPLEMENT
# Implement `coinChange(coins, amount)` (bottom-up DP is common).
from typing import Callable, List, Tuple

tests: List[Tuple[List[int], int, int]] = [
    ([1,2,5], 11, 3),
    ([2], 3, -1),
    ([1], 0, 0),
    ([1], 1, 1),
    ([2,5,10,1], 27, 4),
    ([186,419,83,408], 6249, 20),
]

def harness(func: Callable[[List[int], int], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (coins, amount, expected) in enumerate(tests, 1):
        try:
            got = func(coins[:], amount)
            if got == expected: print(f"Test {i}: PASSED"); passed += 1
            else: print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

def coinChange(coins: List[int], amount: int) -> int:
    pass

harness(coinChange)

