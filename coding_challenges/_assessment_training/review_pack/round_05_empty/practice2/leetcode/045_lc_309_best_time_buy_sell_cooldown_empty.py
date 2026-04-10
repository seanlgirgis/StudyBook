# ============================================================================
# File: 030_lc_309_best_time_buy_sell_cooldown_empty.py
#
# LeetCode 309: Best Time to Buy and Sell Stock with Cooldown (Medium)
#
# PROBLEM STATEMENT:
# You are given an array `prices` where `prices[i]` is the price of a given 
# stock on the ith day.
#
# Find the maximum profit you can achieve. You may complete as many transactions 
# as you like (i.e., buy one and sell one share of the stock multiple times) 
# with the following restrictions:
#
# - After you sell your stock, you cannot buy stock on the next day 
#   (i.e., cooldown one day).
# - You may not engage in multiple transactions simultaneously (i.e., you 
#   must sell the stock before you buy again).
#
# STATE MACHINE EXPLANATION:
# On any given day, your portfolio can be in exactly one of three states:
# 1. `held`: You currently own a stock. 
#    - How to get here: You rested while already holding, OR you just bought 
#      a stock today (from the `reset` state).
# 2. `sold`: You just sold your stock today.
#    - How to get here: You were `held` yesterday, and you sold today. 
#      (This state forces you into `reset` tomorrow).
# 3. `reset`: You do not own a stock, and you are free to buy.
#    - How to get here: You rested while in `reset`, OR you rested for one 
#      day after being in the `sold` state (the cooldown period).
#
# EXAMPLES:
# 1) prices = [1,2,3,0,2] -> Expected: 3
#    Explanation: transactions = [buy, sell, cooldown, buy, sell]
# 2) prices = [1] -> Expected: 0
# ============================================================================


from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (prices, expected_max_profit)
tests: List[Tuple[List[int], int]] = [
    ([1, 2, 3, 0, 2], 3),                                 # Standard Example 1
    ([1], 0),                                             # Standard Example 2 (Single day)
    ([], 0),                                              # Edge Case: Empty list
    ([1, 2], 1),                                          # Edge Case: Two days, simple profit
    ([2, 1], 0),                                          # Edge Case: Two days, decreasing (do nothing)
    ([1, 2, 3, 4, 5], 4),                                 # Boundary: Strictly increasing (Buy day 0, Sell day 4)
    ([5, 4, 3, 2, 1], 0),                                 # Boundary: Strictly decreasing (No profit possible)
    ([3, 2, 6, 5, 0, 3], 7),                              # Complex: Buy 2/Sell 6 (p=4), CD 5, Buy 0/Sell 3 (p=3) -> 7
    ([1, 4, 2, 7, 0, 5], 8),                              # Complex: Buy 1/Sell 4 (p=3), CD 2, Buy 0/Sell 5 (p=5) -> 8
    ([2, 1, 4, 5, 2, 9, 7], 10),                          # Complex: Buy 1/Sell 4 (p=3), CD 5, Buy 2/Sell 9 (p=7) -> 10
    ([3, 3, 3, 3, 3], 0),                                 # Boundary: Flat plateau (No profit)
    ([6, 1, 3, 2, 4, 7], 6),                              # Complex: Better to hold through dip (Buy 1, Sell 7 -> 6)
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], int]) -> None:
    """
    Test harness for LeetCode #309: Best Time to Buy and Sell Stock with Cooldown.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (prices, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation by the user's function
            got = func(prices.copy())
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                prices_disp = str(prices) if len(prices) <= 10 else f"[{str(prices[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | prices={prices_disp}")
        except Exception as e:
            prices_disp = str(prices) if len(prices) <= 10 else f"[{str(prices[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | prices={prices_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def maxProfit_dp(prices: List[int]) -> int:
    """
    Iterative DP (state machine), O(n) time and O(1) extra space.
    """
    if not prices:
        return 0

    profit_while_holding = -prices[0]
    profit_if_just_sold = float("-inf")
    profit_if_ready_to_buy = 0

    for current_price in prices[1:]:
        prev_profit_while_holding = profit_while_holding
        prev_profit_if_just_sold = profit_if_just_sold
        prev_profit_if_ready_to_buy = profit_if_ready_to_buy

        profit_while_holding = max(
            prev_profit_while_holding,
            prev_profit_if_ready_to_buy - current_price,
        )
        profit_if_just_sold = prev_profit_while_holding + current_price
        profit_if_ready_to_buy = max(
            prev_profit_if_ready_to_buy,
            prev_profit_if_just_sold,
        )

    return int(max(profit_if_just_sold, profit_if_ready_to_buy))


from functools import lru_cache
def maxProfit_recursive(prices: List[int]) -> int:
    """
    Top-down recursion + memoization via @lru_cache.
    solve_from_day(day, can_buy_now):
    - day: current day index in prices
    - can_buy_now: True means we are not holding a stock and may buy today
    """
    total_days = len(prices)

    @lru_cache(maxsize=None)
    def solve_from_day(day: int, can_buy_now: bool) -> int:
        if day >= total_days:
            return 0

        if can_buy_now:
            profit_if_buy_today = -prices[day] + solve_from_day(day + 1, False)
            profit_if_skip_today = solve_from_day(day + 1, True)
            return max(profit_if_buy_today, profit_if_skip_today)

        profit_if_sell_today = prices[day] + solve_from_day(day + 2, True)  # cooldown day
        profit_if_hold_today = solve_from_day(day + 1, False)
        return max(profit_if_sell_today, profit_if_hold_today)

    return solve_from_day(0, True)


def maxProfit(prices: List[int]) -> int:
    """Default implementation used by harness."""
    return maxProfit_dp(prices)


# Execute harness without __main__ block
harness(maxProfit_dp)
harness(maxProfit_recursive)
