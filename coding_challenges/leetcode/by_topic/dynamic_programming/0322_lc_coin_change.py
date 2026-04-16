"""
id: lc_0322
title: Coin Change
source: leetcode
difficulty: medium
primary: dynamic-programming
tags: [dynamic-programming, breadth-first-search, arrays]
leetcode_url: https://leetcode.com/problems/coin-change/
status: draft
last_updated: 2026-04-16
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 0322_lc_coin_change.py
# LC 322: Coin Change (Medium)
#
# PROBLEM STATEMENT:
# You are given an integer array coins representing coins of different 
# denominations and an integer amount representing a total amount of money.
#
# Return the fewest number of coins that you need to make up that amount. 
# If that amount of money cannot be made up by any combination of the 
# coins, return -1.
#
# You may assume that you have an infinite number of each kind of coin.
#
# EXAMPLES:
# Input: coins = [1,2,5], amount = 11 -> Output: 3 (11 = 5 + 5 + 1)
# Input: coins = [2], amount = 3 -> Output: -1
# Input: coins = [1], amount = 0 -> Output: 0
# ============================================================================

from typing import List, Tuple, Callable
import copy

# (coins, amount, expected, description)
tests: List[Tuple[List[int], int, int, str]] = [
    ([1, 2, 5], 11, 3, "Standard Example 1"),
    ([2], 3, -1, "Standard Example 2: Impossible"),
    ([1], 0, 0, "Standard Example 3: Amount 0"),
    ([1], 1, 1, "Edge Case: Single coin, exact match"),
    ([1], 2, 2, "Edge Case: Single coin, multiple used"),
    ([1, 2, 5], 100, 20, "Boundary: Larger amount, exact division"),
    ([3, 5], 7, -1, "Boundary: No combination works"),
    ([186, 419, 83, 408], 6249, 20, "Complex: Large denominations/amount"),
    ([2, 4, 6, 8], 11, -1, "Logic: All even coins, odd amount"),
    ([474, 83, 404, 3], 264, 8, "Logic: Greedy choice fails (need DP)"),
    ([1, 2147483647], 2, 2, "Edge Case: Potential overflow/large coin value"),
    ([2, 5, 10, 1], 27, 4, "Stress: Mixed denominations"),
]

def harness(func: Callable) -> None:
    print(f"\n--- Running Harness for: {func.__name__} ---")
    passed = 0
    
    for i, (coins, amount, expected, desc) in enumerate(tests):
        # Deep copy to protect original test data from mutation
        coins_input = copy.deepcopy(coins)
        
        try:
            result = func(coins_input, amount)
            
            if result == expected:
                print(f"Test {i+1} [PASSED]: {desc}")
                passed += 1
            else:
                print(f"Test {i+1} [FAILED]: {desc}")
                print(f"    Input: coins={coins}, amount={amount}")
                print(f"    Expected: {expected}, Got: {result}")
        
        except Exception as e:
            print(f"Test {i+1} [ERROR]: {desc}")
            print(f"    Input: coins={coins}, amount={amount}")
            print(f"    Exception: {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

from typing import List

def coin_change(coins: List[int], amount: int) -> int:
    """
    Finds the fewest number of coins needed to make up 'amount'.
    """
    inf_amt = amount + 1
    buckets = [inf_amt] * (amount + 1)
    
    buckets[0] = 0
    
    for i in range(1, len(buckets)):
        n = inf_amt
        for coin in coins:
            rem = i - coin
            if 0 <= rem < amount:
                if buckets[rem] != inf_amt:
                    n = min(n, buckets[rem] + 1)
        if n != inf_amt: buckets[i] = n
    return buckets[-1] if buckets[-1] != inf_amt else -1

    
    

harness(coin_change)