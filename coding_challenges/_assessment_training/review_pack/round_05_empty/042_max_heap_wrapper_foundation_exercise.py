# ============================================================================
# File: 042_max_heap_wrapper_foundation_exercise.py
#
# Foundation Exercise: MaxHeap Wrapper (using heapq with negation)
# ============================================================================

import heapq
from typing import Any, List


class MaxHeap:
    def __init__(self):
        self._heap: List[int] = []

    def push(self, val: int) -> None:
        # heapq is min-heap, so store negative to emulate max-heap.
        heapq.heappush(self._heap, -val)

    def pop(self) -> int:
        if not self._heap:
            raise IndexError("pop from empty MaxHeap")
        return -heapq.heappop(self._heap)

    def peek(self) -> int:
        if not self._heap:
            raise IndexError("peek from empty MaxHeap")
        return -self._heap[0]

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def size(self) -> int:
        return len(self._heap)

    def to_sorted_desc_list(self) -> List[int]:
        # Non-destructive descending snapshot.
        return sorted((-x for x in self._heap), reverse=True)


# Format:
# (commands, args, expected_returns, expected_final_desc)
tests = [
    (
        ["MaxHeap", "push", "push", "push", "peek", "pop", "peek", "size"],
        [[], [5], [2], [9], [], [], [], []],
        [None, None, None, None, 9, 9, 5, 2],
        [5, 2],
    ),
    (
        ["MaxHeap", "push", "push", "push", "pop", "pop", "pop", "is_empty"],
        [[], [3], [3], [1], [], [], [], []],
        [None, None, None, None, 3, 3, 1, True],
        [],
    ),
    (
        ["MaxHeap", "push", "push", "push", "to_sorted_desc_list"],
        [[], [-1], [4], [0], []],
        [None, None, None, None, [4, 0, -1]],
        [4, 0, -1],
    ),
]

exception_tests = [
    (["MaxHeap", "pop"], [[], []], "IndexError"),
    (["MaxHeap", "peek"], [[], []], "IndexError"),
]


def test_harness() -> None:
    print("--- Running Tests for: MaxHeap ---")
    passed = 0

    for i, (commands, args, expected, final_desc) in enumerate(tests, 1):
        heap = None
        results: List[Any] = []
        ok = True
        err = ""

        try:
            for cmd, arg in zip(commands, args):
                if cmd == "MaxHeap":
                    heap = MaxHeap()
                    results.append(None)
                elif cmd == "push":
                    heap.push(arg[0])
                    results.append(None)
                elif cmd == "pop":
                    results.append(heap.pop())
                elif cmd == "peek":
                    results.append(heap.peek())
                elif cmd == "size":
                    results.append(heap.size())
                elif cmd == "is_empty":
                    results.append(heap.is_empty())
                elif cmd == "to_sorted_desc_list":
                    results.append(heap.to_sorted_desc_list())
                else:
                    raise ValueError(f"Unknown command: {cmd}")

            if results != expected:
                ok = False
                err = f"Return mismatch | expected={expected}, got={results}"

            if ok and heap.to_sorted_desc_list() != final_desc:
                ok = False
                err = f"Final heap mismatch | expected={final_desc}, got={heap.to_sorted_desc_list()}"

        except Exception as e:
            ok = False
            err = f"{type(e).__name__}: {e}"

        if ok:
            print(f"Test {i}: PASSED ({len(commands)} operations)")
            passed += 1
        else:
            print(f"Test {i}: FAILED | {err}")

    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


def exception_harness() -> None:
    print("--- Running Exception Tests for: MaxHeap ---")
    passed = 0
    for i, (commands, args, expected_exc) in enumerate(exception_tests, 1):
        heap = None
        ok = False
        try:
            for cmd, arg in zip(commands, args):
                if cmd == "MaxHeap":
                    heap = MaxHeap()
                elif cmd == "pop":
                    heap.pop()
                elif cmd == "peek":
                    heap.peek()
        except Exception as e:
            ok = type(e).__name__ == expected_exc

        if ok:
            print(f"Exception Test {i}: PASSED")
            passed += 1
        else:
            print(f"Exception Test {i}: FAILED")

    print(f"\nException Summary: {passed}/{len(exception_tests)} tests passed.\n")


test_harness()
exception_harness()

