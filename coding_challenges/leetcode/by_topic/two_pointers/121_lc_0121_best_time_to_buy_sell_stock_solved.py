"""
Problem: Best Time to Buy and Sell Stock
Category: Sliding Window (Variable Size) / Two Pointers
Difficulty: Easy

You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

Example 1:
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

Example 2:
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.
"""

from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        buy_ind = 0
        sell_ind = len(prices) -1
        profit = -1
        min_price = prices[0]
        for price in prices:
            if price < min_price:
                min_price = price
            profit = max(profit, price - min_price)
        return profit


# Test cases to run locally
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    prices1 = [7, 1, 5, 3, 6, 4]
    print(f"Test Case 1: {prices1} -> {solution.maxProfit(prices1)} (Expected: 5)")
    
    # Test Case 2
    prices2 = [7, 6, 4, 3, 1]
    print(f"Test Case 2: {prices2} -> {solution.maxProfit(prices2)} (Expected: 0)")
    prices = [2, 4, 1, 7]
    print(f"Test Case 3: {prices} -> {solution.maxProfit(prices)} (Expected: 6)")
