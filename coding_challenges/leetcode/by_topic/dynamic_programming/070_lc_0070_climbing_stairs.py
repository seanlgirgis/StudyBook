"""
id: lc_0070
title: Climbing Stairs
source: leetcode
difficulty: easy
primary: dynamic-programming
tags: [dynamic-programming, math, recursion]
leetcode_url: https://leetcode.com/problems/climbing-stairs/
status: draft
last_updated: 2026-04-16
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 070_lc_0070_climbing_stairs.py
# LeetCode 70: Climbing Stairs (Easy)
#
# PROBLEM STATEMENT:
# You are climbing a staircase. It takes n steps to reach the top.
# Each time you can either climb 1 or 2 steps. In how many distinct ways 
# can you climb to the top?
#
# EXAMPLES:
# Input: n = 2
# Output: 2
# Explanation: There are two ways to climb to the top.
# 1. 1 step + 1 step
# 2. 2 steps
#
# Input: n = 3
# Output: 3
# Explanation: There are three ways to climb to the top.
# 1. 1 step + 1 step + 1 step
# 2. 1 step + 2 steps
# 3. 2 steps + 1 step
# ============================================================================

from typing import Callable, List, Tuple
import copy

# Test cases: (n, expected_output, description)
tests: List[Tuple[int, int, str]] = [
    (1, 1, "Smallest valid input"),
    (2, 2, "Standard Example 1"),
    (3, 3, "Standard Example 2"),
    (4, 5, "N=4: (1,1,1,1), (1,1,2), (1,2,1), (2,1,1), (2,2)"),
    (5, 8, "Fibonacci sequence verification"),
    (6, 13, "Fibonacci sequence verification"),
    (10, 89, "Medium size input"),
    (20, 10946, "Larger input to check iterative efficiency"),
    (30, 1346269, "Constraint testing (n <= 45)"),
    (45, 1836311903, "Maximum constraint boundary"),
]

def harness(func: Callable) -> None:
    print(f"\n--- Running Harness for: {func.__name__} ---")
    passed = 0
    
    for n, expected, desc in tests:
        # Create a copy in case of mutation (though n is immutable here)
        input_arg = copy.deepcopy(n)
        
        try:
            result = func(input_arg)
            if result == expected:
                print(f"✅ PASSED | Case: {desc} (n={n})")
                passed += 1
            else:
                print(f"❌ FAILED | Case: {desc}")
                print(f"   Input: {n}")
                print(f"   Expected: {expected}, Got: {result}")
        except Exception as e:
            print(f"🔥 ERROR  | Case: {desc}")
            print(f"   Input: {n}")
            print(f"   Exception: {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(tests)} cases passed.")
    print("-" * 40)

# --- USER TO IMPLEMENT SOLUTION BELOW ---

# DP Confidence Reps (Do now, no tomorrow)
# Solve all 3, then paste your answers.

# -------------------------------------------------
# Q1) Climbing Stairs
# You can climb 1 or 2 steps. How many distinct ways to reach step n?
def climb_stairs(n: int) -> int:

    if n <= 2:
        return n
    prevprev = 1
    prev = 2
    for _ in range(3, n+1):
        prev , prevprev = prev + prevprev, prev
    return prev

print(climb_stairs(2))  # 2
print(climb_stairs(3))  # 3
print(climb_stairs(5))  # 8

harness(climb_stairs)