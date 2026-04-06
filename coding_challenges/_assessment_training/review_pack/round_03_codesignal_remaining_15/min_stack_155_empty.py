# LeetCode 155: Min Stack
#
# PROBLEM STATEMENT
# Design a stack that supports push, pop, top, and retrieving minimum element
# in constant time.
#
# EXAMPLE FLOW
# push(-2), push(0), push(-3), getMin() -> -3, pop(), top() -> 0, getMin() -> -2
#
# WHAT TO IMPLEMENT
# Implement class `MinStack` with O(1) operations.

from typing import Any, List, Tuple





# --- TEST CASES ---
# Format: (operations_list, arguments_list, expected_returns)
min_stack_tests: List[Tuple[List[str], List[List[int]], List[Any]]] = [
    (
        ["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"],
        [[], [-2], [0], [-3], [], [], [], []],
        [None, None, None, None, -3, None, 0, -2],
    ),
    (
        ["MinStack", "push", "push", "getMin", "getMin", "push", "getMin", "getMin", "top", "getMin", "pop", "push", "push", "getMin", "pop", "getMin", "pop", "getMin"],
        [[], [-10], [14], [], [], [-20], [], [], [], [], [], [10], [-7], [], [], [], [], []],
        [None, None, None, -10, -10, None, -20, -20, -20, -20, None, None, None, -10, None, -10, None, -10],
    ),
    (
        ["MinStack", "push", "getMin"],
        [[], [5], []],
        [None, None, 5],
    ),
    (
        ["MinStack", "push", "push", "push", "getMin", "pop", "getMin", "pop", "getMin"],
        [[], [5], [4], [3], [], [], [], [], []],
        [None, None, None, None, 3, None, 4, None, 5],
    ),
    (
        ["MinStack", "push", "push", "push", "getMin", "pop", "getMin", "pop", "getMin"],
        [[], [3], [4], [5], [], [], [], [], []],
        [None, None, None, None, 3, None, 3, None, 3],
    ),
    (
        ["MinStack", "push", "push", "push", "getMin", "pop", "getMin"],
        [[], [2], [2], [2], [], [], []],
        [None, None, None, None, 2, None, 2],
    ),
]


# --- RICH HARNESS ---
def test_harness(stack_class: type, test_cases: List[Tuple[List[str], List[List[int]], List[Any]]]) -> None:
    print(f"--- Running Tests for: {stack_class.__name__} ---")
    passed = 0
    for i, (operations, arguments, expected) in enumerate(test_cases, 1):
        try:
            results: List[Any] = []
            obj = None
            for op, arg in zip(operations, arguments):
                if op == "MinStack":
                    obj = stack_class()
                    results.append(None)
                else:
                    method = getattr(obj, op)
                    result = method(*arg) if arg else method()
                    results.append(result)

            if results == expected:
                print(f"Test {i}: PASSED ({len(operations)} operations)")
                passed += 1
            else:
                print(f"Test {i}: FAILED | {len(operations)} operations")
                print(f"    Expected: {expected}")
                print(f"    Got:      {results}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.")


def exception_harness() -> None:
    print("\n--- Running Exception Tests ---")
    checks = [
        ("pop", lambda s: s.pop()),
        ("top", lambda s: s.top()),
        ("getMin", lambda s: s.getMin()),
    ]
    passed = 0
    for i, (name, call) in enumerate(checks, 1):
        s = MinStack()
        try:
            call(s)
            print(f"Exception Test {i}: FAILED | {name} did not raise")
        except IndexError:
            print(f"Exception Test {i}: PASSED")
            passed += 1
        except Exception as e:
            print(f"Exception Test {i}: FAILED | Unexpected {type(e).__name__}: {e}")
    print(f"\nException Summary: {passed}/{len(checks)} tests passed.")

class MinStack:
    def __init__(self) -> None:
        self.stack: List[int] = []
        self.min_stack: List[int] = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        if not self.stack:
            raise IndexError("pop from empty MinStack")
        value = self.stack.pop()
        if value == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        if not self.stack:
            raise IndexError("top from empty MinStack")
        return self.stack[-1]

    def getMin(self) -> int:
        if not self.min_stack:
            raise IndexError("getMin from empty MinStack")
        return self.min_stack[-1]
        
        
test_harness(MinStack, min_stack_tests)
exception_harness()
