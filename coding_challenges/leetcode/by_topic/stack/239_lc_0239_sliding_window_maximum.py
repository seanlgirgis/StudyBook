"""
id: lc_0239
title: Sliding Window Maximum
source: leetcode
difficulty: hard
primary: stack
tags: [stack, sliding-window, heap, queue, monotonic-queue]
leetcode_url: https://leetcode.com/problems/sliding-window-maximum/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 239_lc_0239_sliding_window_maximum.py
# LC239: Sliding Window Maximum (Hard)
#
# PROBLEM STATEMENT:
# You are given an array of integers nums, there is a sliding window of size k 
# which is moving from the very left of the array to the very right. You can 
# only see the k numbers in the window. Each time the sliding window moves 
# right by one position.
# Return the max sliding window.
#
# EXAMPLES:
# Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
# Output: [3,3,5,5,6,7]
# Explanation: 
# Window position                Max
# ---------------               -----
# [1  3  -1] -3  5  3  6  7       3
#  1 [3  -1  -3] 5  3  6  7       3
#  1  3 [-1  -3  5] 3  6  7       5
#  1  3  -1 [-3  5  3] 6  7       5
#  1  3  -1  -3 [5  3  6] 7       6
#  1  3  -1  -3  5 [3  6  7]      7
#
# Input: nums = [1], k = 1
# Output: [1]
# ============================================================================

from typing import List, Tuple, Callable
import copy

# Test cases: (nums, k) -> expected_output
tests: List[Tuple[List[int], int, List[int]]] = [
    ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),  # Standard example 1
    ([1], 1, [1]),                                       # Standard example 2
    ([1, -1], 1, [1, -1]),                               # Window size 1
    ([7, 2, 4], 2, [7, 4]),                              # Small array
    ([9, 11], 2, [11]),                                  # Window equals array size
    ([1, 2, 3, 4, 5, 6], 3, [3, 4, 5, 6]),               # Strictly increasing
    ([6, 5, 4, 3, 2, 1], 3, [6, 5, 4, 3]),               # Strictly decreasing
    ([8, 8, 8, 8], 2, [8, 8, 8]),                        # All identical elements
    ([4, -2, -8, 5, -2, 7, 7, 2], 4, [5, 5, 7, 7, 7]),   # Mixed signs and duplicates
    ([-7, -8, -7, 5, 7, 1, 6, 0], 4, [5, 7, 7, 7, 7]),   # Negative starts
    ([1, 3, 1, 2, 0, 5], 3, [3, 3, 2, 5]),               # Peak in middle
]

def harness(func: Callable) -> None:
    passed = 0
    for i, (nums, k, expected) in enumerate(tests):
        # Deep copy to prevent mutation issues
        nums_copy = copy.deepcopy(nums)
        
        try:
            result = func(nums_copy, k)
            if result == expected:
                print(f"Test {i+1}: PASSED")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED")
                print(f"   Input: nums={nums}, k={k}")
                print(f"   Expected: {expected}")
                print(f"   Actual:   {result}")
        except Exception as e:
            print(f"Test {i+1}: ERROR ({type(e).__name__}: {e})")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---
from collections import deque

class MaxWin:
    """
    Monotonic deque-based sliding window maximum tracker.

    The deque stores (index, value) pairs in DECREASING order of value.
    That means the front of the deque is ALWAYS the maximum of the current window.

    Two invariants are maintained on every push:
      1. The window never holds indices that have slid out of range (front eviction).
      2. The deque never holds a value that is useless because a newer bigger
         value exists behind it (back eviction — this is what makes it monotonic).

    k  : window size
    i  : current index (how many elements have been pushed so far, 0-based)
    d  : the deque — entries are (index, value), front = current max
    """

    def __init__(self, k):
        self.k = k    # window size — used to know when front is stale
        self.i = -1   # current index, starts at -1 so first push makes it 0
        self.d = deque()

    def push(self, x):
        # Move the index forward — this is the position of the new element
        self.i += 1

        # FRONT EVICTION — remove indices that are no longer inside the window.
        # The window covers [i-k+1 .. i]. Any index <= i-k is out of range.
        # We only need to check the front because older indices are always there.
        while self.d and self.d[0][0] <= self.i - self.k:
            self.d.popleft()

        # BACK EVICTION — remove anything from the back that is <= x.
        # If a previous value is smaller than the new one, it can NEVER be
        # the window max while x is still in the window (x is newer AND bigger).
        # Keeping it would be pointless, so we throw it away now.
        while self.d and self.d[-1][1] <= x:
            self.d.pop()

        # Push the new element. It goes to the back — youngest entry.
        self.d.append((self.i, x))

    def __bool__(self):
        # The first full window is ready once we have seen at least k elements.
        # i is 0-based, so the k-th element lands at index k-1.
        # Before that point calling max() is meaningless.
        return self.i >= self.k - 1

    def max(self):
        # Front of the deque is always the max of the current window —
        # guaranteed by the two eviction rules in push().
        return self.d[0][1]

             
def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    """
    Implementation Note: Use a monotonic deque to store indices of potential
    maximums. Indices in deque should be in decreasing order of their 
    corresponding values in 'nums'.
    """
    out = []
    maxwin = MaxWin(k)
    for num in nums:
        maxwin.push(num)
        if maxwin:
            out.append(maxwin.max())
    return out
        
        

harness(maxSlidingWindow)