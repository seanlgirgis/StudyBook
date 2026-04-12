"""
id: lc_1475
title: Final Prices With a Special Discount in a Shop
source: leetcode
difficulty: easy
primary: stack
tags: [stack, monotonic-stack, arrays]
leetcode_url: https://leetcode.com/problems/final-prices-with-a-special-discount-in-a-shop/
status: draft
last_updated: 2026-04-12
notes: 
- key idea: Use a monotonic increasing stack to find the first element to the right that is less than or equal to the current price.
- time: O(n)
- space: O(n)
"""

# ============================================================================
# File: 1475_lc_1475_final_prices_with_special_discount_empty.py
# Problem 1475: Final Prices With a Special Discount in a Shop (Easy)
# 
# PROBLEM STATEMENT:
# You are given an integer array prices where prices[i] is the price of the 
# ith item in a shop.
#
# There is a special discount for items in the shop. If you buy the ith item, 
# then you will receive a discount equivalent to prices[j] where j is the 
# minimum index such that j > i and prices[j] <= prices[i]. Otherwise, you 
# will not receive any discount at all.
#
# Return an integer array answer where answer[i] is the final price you will 
# pay for the ith item of the shop, considering the special discount.
#
# EXAMPLES:
# Input: prices = [8,4,6,2,3]
# Output: [4,2,4,2,3]
# Explanation: 
# For item 0 with price[0]=8 you will receive a discount equivalent to prices[1]=4.
# For item 1 with price[1]=4 you will receive a discount equivalent to prices[3]=2.
# For item 2 with price[2]=6 you will receive a discount equivalent to prices[3]=2.
# For items 3 and 4 you will not receive any discount at all.
# ============================================================================

from typing import List, Tuple, Callable

# Test Cases: List[Tuple[prices, expected]]
tests: List[Tuple[List[int], List[int]]] = [
    ([8, 4, 6, 2, 3], [4, 2, 4, 2, 3]),    # Standard Example 1
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),    # Standard Example 2 (No discounts)
    ([10, 1, 1, 6], [9, 0, 1, 6]),         # Standard Example 3
    ([5], [5]),                            # Edge Case: Single element
    ([5, 5, 5, 5], [0, 0, 0, 5]),          # Edge Case: All identical (discount is the same value)
    ([1, 10, 1], [0, 9, 1]),               # Gap in price jump
    ([10, 9, 8, 7, 6], [1, 1, 1, 1, 6]),   # Boundary: Strictly decreasing
    ([2, 3, 1, 2, 4, 1], [1, 2, 0, 1, 3, 1]), # Complex sequence
    ([100, 50, 25, 12, 6], [50, 25, 13, 6, 6]), # Rapid halving
    ([3, 4, 5, 1, 2], [2, 3, 4, 1, 2]),    # Late discount for early items
    ([0, 0, 0], [0, 0, 0]),                # Boundary: Zero prices
    ([1000, 1, 1000, 1], [999, 0, 999, 1]), # Large alternating values
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0
    
    print(f"\n--- Testing: {func.__name__} ---")
    
    for i, (prices, expected) in enumerate(tests):
        # Deep copy the input to prevent user mutation
        prices_copy = list(prices)
        
        try:
            result = func(prices_copy)
            
            display_input = str(prices) if len(str(prices)) < 50 else f"{str(prices)[:47]}..."
            
            if result == expected:
                print(f"Test {i+1}: PASSED | Input: {display_input}")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Input: {display_input}")
                print(f"   Expected: {expected}, Got: {result}")
                failed += 1
        except Exception as e:
            print(f"Test {i+1}: ERROR  | Input: {display_input}")
            print(f"   Exception: {e}")
            failed += 1
            
    print(f"\nResults: {passed} Passed, {failed} Failed\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def finalPrices(prices: List[int]) -> List[int]:
    """
    Returns the final prices after applying the special discount.
    """
    res = prices[:]
    stack = []
    for i, p in enumerate (prices):
        while stack and p <= prices[stack[-1]]:
            pi = stack.pop()
            res[pi] = prices[pi] - p
            
        stack.append(i)
    return res
    
    

harness(finalPrices)