# LeetCode 739: Daily Temperatures (Empty)
#
# PROBLEM STATEMENT
# Given an array `temperatures`, return an array `answer` where answer[i] is the number of days
# you must wait after day i to get a warmer temperature. If none exists, answer[i] = 0.
#
# EXAMPLE
# [73,74,75,71,69,72,76,73] -> [1,1,4,2,1,1,0,0]
#
# WHAT TO IMPLEMENT
# Implement `dailyTemperatures(temperatures)` (typically monotonic stack).
from typing import Callable, List, Tuple

tests: List[Tuple[List[int], List[int]]] = [
    ([73,74,75,71,69,72,76,73], [1,1,4,2,1,1,0,0]),
    ([30,40,50,60], [1,1,1,0]),
    ([30,60,90], [1,1,0]),
    ([90,80,70], [0,0,0]),
    ([70,70,70], [0,0,0]),
    ([70], [0]),
]

def harness(func: Callable[[List[int]], List[int]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (temps, expected) in enumerate(tests, 1):
        try:
            got = func(temps[:])
            if got == expected: print(f"Test {i}: PASSED"); passed += 1
            else: print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

def dailyTemperatures(temperatures: List[int]) -> List[int]:
    res = [0] * len(temperatures)
    stack = []
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            popped_ind = stack.pop()
            res[popped_ind] = i - popped_ind
        stack.append(i)
    return res


harness(dailyTemperatures)

