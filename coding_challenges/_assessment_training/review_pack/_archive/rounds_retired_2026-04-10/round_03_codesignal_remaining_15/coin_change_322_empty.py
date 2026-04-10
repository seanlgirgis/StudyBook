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
# Implement `coinChange(coins, amount)` (bottom-up amountsArray is common).
# LeetCode 322: Coin Change

from typing import Callable, List, Tuple
from collections import deque
import sys

# --- TEST CASES ---
# Format: (coins_array, amount, expected_fewest_coins)
coin_change_tests: List[Tuple[List[int], int, int]] = [
    ([1, 2, 5], 11, 3),                        # 1. Standard LC Example 1 (5 + 5 + 1)
    ([2], 3, -1),                              # 2. Standard LC Example 2 (Impossible)
    ([1], 0, 0),                               # 3. Standard LC Example 3 (Zero amount)
    ([1, 3, 4], 6, 2),                         # 4. Anti-Greedy Test (amountsArray: 3+3=2, Greedy: 4+1+1=3)
    ([186, 419, 83, 408], 6249, 20),           # 5. Large unsorted denominations (Classic LC trap)
    ([2], 1, -1),                              # 6. Target smaller than smallest coin
    ([2, 5, 10, 1], 27, 4),                    # 7. Unordered coins (10 + 10 + 5 + 2)
    ([5, 10], 12, -1),                         # 8. Impossible gaps
    ([1], 100, 100),                           # 9. Max out single small coin
    ([3, 7, 405, 436], 8839, 25)               # 10. Complex large number combination
]

# --- TEST HARNESS ---
def test_harness(func: Callable[[List[int], int], int], test_cases: List[Tuple[List[int], int, int]]) -> None:
    """
    Test harness for LeetCode #322: Coin Change.
    Validates Bottom-Up 1D Dynamic Programming optimizations.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0
    for i, (coins, amount, expected) in enumerate(test_cases):
        try:
            # Deep copy just in case the implementation mutates the input
            test_coins = coins.copy()
            
            # Strict typed execution
            result: int = func(test_coins, amount)
            
            if result == expected:
                display_coins = f"{coins[:4]}..." if len(coins) > 4 else f"{coins}"
                print(f"Test {i+1}: PASSED (amount={amount}, coins={display_coins})")
                passed += 1
            else:
                display_coins = f"{coins[:4]}..." if len(coins) > 4 else f"{coins}"
                print(f"Test {i+1}: FAILED | amount={amount}, coins={display_coins}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
        except Exception as e:
            display_coins = f"{coins[:4]}..." if len(coins) > 4 else f"{coins}"
            print(f"Test {i+1}: ERROR  | amount={amount}, coins={display_coins} | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
import math
def coinChange(coins: List[int], amount: int) -> int:
    amountsArray = [math.inf] * (amount +1)
    amountsArray[0] = 0
    for curAmount in range(1, amount+1):
        for coin in coins:
            if curAmount - coin >= 0 and amountsArray[curAmount - coin] != math.inf: # valid coin
                amountsArray[curAmount] = min(
                    amountsArray[curAmount],
                    amountsArray [curAmount - coin] + 1
                    )
    return amountsArray[amount] if amountsArray[amount] != math.inf else -1


def coinChange_top_down(coins: List[int], amount: int) -> int:
    # Top-down recursion can exceed default recursion depth for large amounts,
    # especially when small denominations exist. Raise limit safely for training.
    sys.setrecursionlimit(max(10000, amount + 100))

    # Try larger coins first to keep recursion chains shallower in practice.
    coins = sorted(coins, reverse=True)
    memo = {0: 0}

    def dfs(rem: int) -> int:
        if rem in memo:
            return memo[rem]
        if rem < 0:
            return math.inf

        best = math.inf
        for c in coins:
            cand = dfs(rem - c)
            if cand != math.inf:
                best = min(best, cand + 1)
        memo[rem] = best
        return best

    ans = dfs(amount)
    return ans if ans != math.inf else -1


def coinChange_bfs(coins: List[int], amount: int) -> int:
    if amount == 0:
        return 0

    q = deque([(0, 0)])  # (current amount, steps)
    visited = set([0])

    while q:
        cur, steps = q.popleft()
        for c in coins:
            nxt = cur + c
            if nxt == amount:
                return steps + 1
            if 0 <= nxt < amount and nxt not in visited:
                visited.add(nxt)
                q.append((nxt, steps + 1))
    return -1


# Execute harnesses without __main__ block
test_harness(coinChange, coin_change_tests)
print()
test_harness(coinChange_top_down, coin_change_tests)
print()
test_harness(coinChange_bfs, coin_change_tests)
