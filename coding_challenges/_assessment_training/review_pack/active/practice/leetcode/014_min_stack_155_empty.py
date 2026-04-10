# ============================================================================
# File: 014_min_stack_155_empty.py
#
# LeetCode 155: Min Stack (Medium)
#
# PROBLEM STATEMENT:
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
# EXAMPLES:
# Input
# ["MinStack","push","push","push","getMin","pop","top","getMin"]
# [[],[-2],[0],[-3],[],[],[],[]]
# Output
# [null,null,null,null,-3,null,0,-2]
# ============================================================================

from typing import List, Tuple, Any, Optional

# --- TEST CASES ---
# Format: (commands, args, expected_outputs)
tests: List[Tuple[List[str], List[List[int]], List[Optional[int]]]] = [
    (
        # 1. Standard LC Example
        ["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"],
        [[], [-2], [0], [-3], [], [], [], []],
        [None, None, None, None, -3, None, 0, -2]
    ),
    (
        # 2. Boundary: Duplicate minimums
        ["MinStack", "push", "push", "getMin", "pop", "getMin"],
        [[], [1], [1], [], [], []],
        [None, None, None, 1, None, 1]
    ),
    (
        # 3. Boundary: Strictly increasing elements (min stays the same)
        ["MinStack", "push", "push", "push", "getMin", "pop", "getMin", "pop", "getMin"],
        [[], [1], [2], [3], [], [], [], [], []],
        [None, None, None, None, 1, None, 1, None, 1]
    ),
    (
        # 4. Boundary: Strictly decreasing elements (min changes every pop)
        ["MinStack", "push", "push", "push", "getMin", "pop", "getMin", "pop", "getMin"],
        [[], [3], [2], [1], [], [], [], [], []],
        [None, None, None, None, 1, None, 2, None, 3]
    ),
    (
        # 5. Edge Case: Single element push/pop sequence
        ["MinStack", "push", "getMin", "top", "pop", "push", "getMin"],
        [[], [5], [], [], [], [10], []],
        [None, None, 5, 5, None, None, 10]
    )
]

# --- TEST HARNESS ---
def test_harness(target_class: type, test_cases: List[Tuple[List[str], List[List[int]], List[Optional[int]]]]) -> None:
    """
    Test harness for LeetCode #155: Min Stack.
    Validates sequential state execution and correct return values.
    """
    print(f"--- Running Tests for: {target_class.__name__} ---")
    passed: int = 0
    
    for i, (commands, args, expected) in enumerate(test_cases, 1):
        obj = None
        results: List[Optional[int]] = []
        test_passed: bool = True
        error_msg: str = ""
        
        try:
            # Execute commands
            for step, (cmd, arg) in enumerate(zip(commands, args)):
                if cmd == "MinStack":
                    obj = target_class()
                    results.append(None)
                elif cmd == "push":
                    obj.push(arg[0])
                    results.append(None)
                elif cmd == "pop":
                    obj.pop()
                    results.append(None)
                elif cmd == "top":
                    results.append(obj.top())
                elif cmd == "getMin":
                    results.append(obj.getMin())
                else:
                    raise ValueError(f"Unknown command: {cmd}")
            
            # Validate results
            for step, (res, exp) in enumerate(zip(results, expected)):
                if res != exp:
                    test_passed = False
                    error_msg = f"Mismatch at step {step} ({commands[step]}{args[step]}): Got {res}, Expected {exp}"
                    break
                        
        except Exception as e:
            test_passed = False
            error_msg = f"{type(e).__name__}: {e}"
            
        if test_passed:
            print(f"Test {i}: PASSED ({len(commands)} operations)")
            passed += 1
        else:
            print(f"Test {i}: FAILED | {error_msg}")
            cdcd 
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")



# --- USER TO IMPLEMENT SOLUTION BELOW ---
class MinStack:
    def __init__(self):
        self._data = []                      # store types (val, min_so_far)
        
    def push(self, val: int) -> None:
        if not self._data :
            self._data.append((val, val))
        else:
            self._data.append((val, min(self.getMin(), val)))
 
    def pop(self) -> None:
        self._data.pop()

    def top(self) -> int:
        return self._data[-1][0]

    def getMin(self) -> int:
        return self._data[-1][1]


# Execute harness without __main__ block
test_harness(MinStack, tests)