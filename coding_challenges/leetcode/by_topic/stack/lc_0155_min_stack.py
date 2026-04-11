"""
id: lc_0155
title: Min Stack
source: leetcode
difficulty: easy
primary: stack
tags: [stack, design]
leetcode_url: https://leetcode.com/problems/min-stack/
status: draft
last_updated: 2026-04-11
notes:
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: lc_0155_min_stack.py
# LC155: Min Stack (Easy)
#
# Design a stack that supports push, pop, top, and retrieving the minimum 
# element in constant time.
#
# Implement the MinStack class:
# - MinStack() initializes the stack object.
# - void push(int val) pushes the element val onto the stack.
# - void pop() removes the element on the top of the stack.
# - int top() gets the top element of the stack.
# - int getMin() retrieves the minimum element in the stack.
#
# You must implement a solution with O(1) time complexity for each function.
#
# Example 1:
# Input:
# ["MinStack","push","push","push","getMin","pop","top","getMin"]
# [[],[-2],[0],[-3],[],[],[],[]]
#
# Output:
# [null,null,null,null,-3,null,0,-2]
# ============================================================================

from typing import List, Optional, Any

# Test cases: (Operations, Arguments, Expected Outputs)
tests = [
    (
        ["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"],
        [[], [-2], [0], [-3], [], [], [], []],
        [None, None, None, None, -3, None, 0, -2]
    ), # Standard Example 1
    (
        ["MinStack", "push", "getMin", "pop"],
        [[], [5], [], []],
        [None, None, 5, None]
    ), # Single element logic
    (
        ["MinStack", "push", "push", "getMin", "push", "getMin", "pop", "getMin"],
        [[], [10], [20], [], [5], [], [], []],
        [None, None, None, 10, None, 5, None, 10]
    ), # Descending then ascending minimums
    (
        ["MinStack", "push", "push", "push", "getMin", "pop", "getMin", "pop", "getMin"],
        [[], [2], [2], [2], [], [], [], [], []],
        [None, None, None, None, 2, None, 2, None, 2]
    ), # Handling duplicate minimum values
    (
        ["MinStack", "push", "push", "top", "getMin", "pop", "getMin"],
        [[], [-10], [10], [], [], [], []],
        [None, None, None, 10, -10, None, -10]
    ), # Negative values and positive mix
    (
        ["MinStack", "push", "push", "push", "push", "getMin", "pop", "getMin", "pop", "getMin", "pop", "getMin"],
        [[], [1], [2], [3], [4], [], [], [], [], [], [], []],
        [None, None, None, None, None, 1, None, 1, None, 1, None, 1]
    ), # Strictly increasing (min stays same)
    (
        ["MinStack", "push", "push", "push", "push", "getMin", "pop", "getMin", "pop", "getMin", "pop", "getMin"],
        [[], [4], [3], [2], [1], [], [], [], [], [], [], []],
        [None, None, None, None, None, 1, None, 2, None, 3, None, 4]
    ), # Strictly decreasing (min changes every pop)
    (
        ["MinStack", "push", "push", "getMin", "push", "getMin", "push", "getMin", "pop", "getMin", "pop", "getMin"],
        [[], [0], [1], [], [0], [], [-1], [], [], [], [], []],
        [None, None, None, 0, None, 0, None, -1, None, 0, None, 0]
    ), # Complex pattern with zero

    # -------------------------------------------------------------------------
    # BUG EXPOSURE TESTS — target the data[0] vs data[-1] flaw in push()
    # All scenarios: push a value AFTER the minimum was established by a
    # middle element. data[0][1] is the first element's min (stale);
    # data[-1][1] is the running min at the top (correct).
    # -------------------------------------------------------------------------

    (
        ["MinStack", "push", "push", "push", "pop", "push", "getMin"],
        [[], [5], [3], [7], [], [4], []],
        [None, None, None, None, None, None, 3]
    ), # push high-low-high, pop high, push mid — min must still be 3

    (
        ["MinStack", "push", "push", "push", "pop", "push", "getMin"],
        [[], [5], [3], [1], [], [4], []],
        [None, None, None, None, None, None, 3]
    ), # push high-low-lowest, pop lowest, push mid — min must revert to 3

    (
        ["MinStack", "push", "push", "push", "pop", "push", "getMin"],
        [[], [10], [5], [8], [], [6], []],
        [None, None, None, None, None, None, 5]
    ), # push 10-5-8, pop 8, push 6 — min must still be 5 not 6

    (
        ["MinStack", "push", "push", "push", "push", "pop", "getMin"],
        [[], [2], [0], [3], [0], [], []],
        [None, None, None, None, None, None, 0]
    ), # push 2-0-3-0, pop top 0 — min of [2,0,3] must still be 0

    (
        ["MinStack", "push", "push", "push", "push", "pop", "push", "getMin"],
        [[], [3], [5], [1], [7], [], [4], []],
        [None, None, None, None, None, None, None, 1]
    ), # push 3-5-1-7, pop 7, push 4 — min of [3,5,1,4] must be 1

    (
        ["MinStack", "push", "push", "push", "pop", "push", "getMin"],
        [[], [4], [2], [6], [], [5], []],
        [None, None, None, None, None, None, 2]
    ), # push 4-2-6, pop 6, push 5 — stack [4,2,5], min must be 2 not 4

    (
        ["MinStack", "push", "push", "push", "push", "pop", "pop", "push", "getMin"],
        [[], [6], [3], [8], [1], [], [], [5], []],
        [None, None, None, None, None, None, None, None, 3]
    ), # push 6-3-8-1, pop 1, pop 8 — stack [6,3], push 5 → [6,3,5], min=3
]

def harness():
    passed = 0
    for i, (ops, args, expected) in enumerate(tests):
        print(f"Test Case {i+1}: ", end="")
        try:
            obj = None
            results = []
            for op, arg in zip(ops, args):
                if op == "MinStack":
                    obj = MinStack()
                    results.append(None)
                elif op == "push":
                    results.append(obj.push(arg[0]))
                elif op == "pop":
                    results.append(obj.pop())
                elif op == "top":
                    results.append(obj.top())
                elif op == "getMin":
                    results.append(obj.getMin())
            
            if results == expected:
                print("PASSED")
                passed += 1
            else:
                print(f"FAILED\n  Expected: {expected}\n  Actual:   {results}")
        except Exception as e:
            print(f"ERROR: {e}")
    
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

class MinStack:

    def __init__(self):
        self.data = []

    def push(self, val: int) -> None:
        if self.data:
            self.data.append((val,min(val, self.data[-1][1])))
        else:
            self.data.append((val, val))
        
    def pop(self) -> None:
        if self.data :
            self.data.pop()
          
            
    def top(self) -> int:
        if self.data :
            return self.data [-1][0]

    def getMin(self) -> int:
        if self.data :
            return self.data [-1][1]

harness()

