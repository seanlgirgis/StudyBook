"""
id: lc_0901
title: Online Stock Span
source: leetcode
difficulty: medium
primary: stack
tags: [stack, design, monotonic-stack, data-stream]
leetcode_url: https://leetcode.com/problems/online-stock-span/
status: draft
last_updated: 2026-04-11
notes:
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 0901_lc_901_online_stock_span.py
# LeetCode 901: Online Stock Span (Medium)
#
# PROBLEM STATEMENT:
# Design an algorithm that collects daily price quotes for some stock and 
# returns the span of that stock's price for the current day.
#
# The span of the stock's price in one day is the maximum number of consecutive 
# days (starting from today and going backward) for which the stock price was 
# less than or equal to the price of that day.
#
# For example, if the prices of the stock in the last four days is [7, 2, 1, 2] 
# and the price of the stock today is 2, then the span of today is 4 because 
# starting from today, the price of the stock was less than or equal 
# to 2 for 4 consecutive days.
#
# If the prices of the stock in the last four days is [1, 2, 3, 4] and the 
# price of the stock today is 1, then the span of today is 1.
#
# Implement the StockSpanner class:
# - StockSpanner() Initializes the object of the class.
# - int next(int price) Returns the span of the stock's price given that 
#   today's price is price.
#
# EXAMPLES:
# Input: ["StockSpanner", "next", "next", "next", "next", "next", "next", "next"]
#        [[], [100], [80], [60], [70], [60], [75], [85]]
# Output: [null, 1, 1, 1, 2, 1, 4, 6]
# ============================================================================

from typing import List, Tuple, Any

# Test cases: List of (calls, arguments, expected_outputs)
# Note: null in LeetCode translates to None in Python
tests = [
    (
        ["StockSpanner", "next", "next", "next", "next", "next", "next", "next"],
        [[], [100], [80], [60], [70], [60], [75], [85]],
        [None, 1, 1, 1, 2, 1, 4, 6]
    ), # Example 1: General monotonic behavior
    (
        ["StockSpanner", "next", "next", "next", "next"],
        [[], [10], [10], [10], [10]],
        [None, 1, 2, 3, 4]
    ), # Edge Case: All identical prices
    (
        ["StockSpanner", "next", "next", "next", "next"],
        [[], [10], [20], [30], [40]],
        [None, 1, 2, 3, 4]
    ), # Boundary: Strictly increasing
    (
        ["StockSpanner", "next", "next", "next", "next"],
        [[], [40], [30], [20], [10]],
        [None, 1, 1, 1, 1]
    ), # Boundary: Strictly decreasing
    (
        ["StockSpanner", "next", "next", "next", "next", "next"],
        [[], [31], [41], [48], [59], [79]],
        [None, 1, 2, 3, 4, 5]
    ), # Complex: Linear accumulation
    (
        ["StockSpanner", "next", "next", "next", "next", "next"],
        [[], [90], [10], [20], [30], [100]],
        [None, 1, 1, 2, 3, 5]
    ), # Complex: Large jump after small values
    (
        ["StockSpanner", "next"],
        [[], [5]],
        [None, 1]
    ), # Edge Case: Single element
    (
        ["StockSpanner", "next", "next", "next", "next"],
        [[], [50], [1], [1], [50]],
        [None, 1, 1, 2, 4]
    ), # Edge Case: Return to initial high
]

def harness(cls_obj: Any) -> None:
    passed = 0
    for i, (calls, args, expected) in enumerate(tests):
        try:
            obj = None
            results = []
            for call, arg in zip(calls, args):
                if call == "StockSpanner":
                    obj = cls_obj()
                    results.append(None)
                elif call == "next":
                    # Prices are ints, no deepcopy needed, but following pattern
                    val = arg[0]
                    res = obj.next(val)
                    results.append(res)
            
            if results == expected:
                print(f"Test Case {i+1}: PASSED")
                passed += 1
            else:
                print(f"Test Case {i+1}: FAILED")
                print(f"  Expected: {expected}")
                print(f"  Actual:   {results}")
        except Exception as e:
            print(f"Test Case {i+1}: ERROR ({type(e).__name__}: {e})")
            
    print(f"\nSummary: {passed}/{len(tests)} cases passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---


class StockSpanner:
    # Monotonic DECREASING stack — prices decrease from bottom to top.
    # Each entry is (price, span).
    # span = how many consecutive days THIS entry speaks for, including itself
    #        and everything it already swallowed when it was pushed.
    #
    # When a new price arrives:
    #   - Pop everything from the top whose price <= new price.
    #     They are dead — the new price is bigger AND newer, so they can
    #     never be a blocker for any future query. Inherit their spans.
    #   - Push (new_price, accumulated_span).
    #
    # Example after Day 4 (price=70):
    #   stack = [(100,1), (80,1), (70,2)]
    #   The 2 on (70,2) means: "I am 70 and I speak for today + the 60 I swallowed."
    #   Any future price > 70 will grab that 2 in one pop, no re-scanning needed.

    def __init__(self):
        self.stack = []   # stores (price, span) pairs

    def next(self, price: int) -> int:
        span = 1          # today always counts as at least 1

        # Pop every entry whose price is <= today's price.
        # Those days are now covered by today — absorb their spans.
        while self.stack and self.stack[-1][0] <= price:
            _, s = self.stack.pop()
            span += s     # inherit everything that entry was speaking for

        # Push today. The span stored here is the full count we just built.
        # Future prices bigger than today will grab this whole span in one pop.
        self.stack.append((price, span))

        return span


harness(StockSpanner)