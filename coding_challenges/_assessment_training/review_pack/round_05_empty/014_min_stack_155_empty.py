# ============================================================================
# File: min_stack_155_empty.py
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
# ============================================================================

from typing import List, Optional, Any

# --- TEST CASES ---
# Format: {"commands": [...], "args": [...], "expected": [...]}
min_stack_tests: List[dict] = [
    {
        # Standard Example 1
        "commands": ["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"],
        "args": [[], [-2], [0], [-3], [], [], [], []],
        "expected": [None, None, None, None, -3, None, 0, -2]
    },
    {
        # Boundary: Duplicate minimums (popping one shouldn't lose the other)
        "commands": ["MinStack", "push", "push", "push", "getMin", "pop", "getMin"],
        "args": [[], [1], [2], [1], [], [], []],
        "expected": [None, None, None, None, 1, None, 1]
    },
    {
        # Boundary: Strictly increasing order
        "commands": ["MinStack", "push", "push", "push", "getMin", "pop", "getMin", "pop", "getMin"],
        "args": [[], [1], [2], [3], [], [], [], [], []],
        "expected": [None, None, None, None, 1, None, 1, None, 1]
    },
    {
        # Boundary: Strictly decreasing order
        "commands": ["MinStack", "push", "push", "push", "getMin", "pop", "getMin", "pop", "getMin"],
        "args": [[], [3], [2], [1], [], [], [], [], []],
        "expected": [None, None, None, None, 1, None, 2, None, 3]
    },
    {
        # Edge case: Negative and positive mix, crossing zero
        "commands": ["MinStack", "push", "push", "getMin", "push", "getMin", "pop", "getMin"],
        "args": [[], [5], [-5], [], [10], [], [], []],
        "expected": [None, None, None, -5, None, -5, None, -5]
    }
]

# --- TEST HARNESS ---
def test_harness(target_class: type, test_cases: List[dict]) -> None:
    """
    Test harness for LeetCode #155: Min Stack.
    Validates sequential state execution and correct minimum tracking.
    """
    print(f"--- Running Tests for: {target_class.__name__} ---")
    passed: int = 0
    
    for i, tc in enumerate(test_cases):
        commands: List[str] = tc["commands"]
        args: List[List[Any]] = tc["args"]
        expected: List[Optional[int]] = tc["expected"]
        
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
            print(f"Test {i+1}: PASSED ({len(commands)} operations)")
            passed += 1
        else:
            print(f"Test {i+1}: FAILED | {error_msg}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
class MinStack:
    def __init__(self):
        self.stack: List[int] = []      # Data stack
        self.min_stack: List[int] = []  # Monotonic non-increasing stack for minimum tracking

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
        

    def pop(self) -> None:
        if not self.stack:
            raise IndexError("pop error: Stack is Empty")
        val = self.stack.pop()
        # If popped val is the current minimum, remove it from min_stack as well.
        if val == self.min_stack[-1]:
            self.min_stack.pop()
            

    def top(self) -> int:
        if not self.stack:
            raise IndexError("top error: Stack is Empty")
        return self.stack[-1]

    def getMin(self) -> int:
        if not self.min_stack:
            raise IndexError("getMin error: Stack is Empty")
        return self.min_stack[-1]


# Execute harness without __main__ block
test_harness(MinStack, min_stack_tests)
