# ============================================================================
# File: 041_min_heap_wrapper_foundation_exercise.py
#
# Foundation Exercise: MinHeap Wrapper
# ============================================================================

import heapq
from typing import Any, List, Optional, Tuple


class MinHeap:
    def __init__(self):
        self._heap = []


    def push(self, val: int) -> None:
        heapq.heappush(self._heap, val)


    def pop(self) -> int:
        if not self._heap:
            raise IndexError("MinHeap pop . empty heap")
        return heapq.heappop(self._heap)

    def peek(self) -> int:
        if not self._heap:
            raise IndexError("MinHeap peek . empty heap")
        return self._heap[0]

    def __bool__(self) -> bool:
        return bool(self._heap)

    def __len__(self) -> int:
        return len(self._heap)


    def snapshot(self) -> List[int]:
        return self._heap[:]


# Format:
# (commands, args, expected_returns, expected_final_contents)
tests = [
    (
        ["MinHeap", "push", "push", "push", "peek", "pop", "peek", "__len__"],
        [[], [5], [2], [9], [], [], [], []],
        [None, None, None, None, 2, 2, 5, 2],
        [5, 9],
    ),
    (
        ["MinHeap", "push", "push", "push", "pop", "pop", "pop", "__bool__"],
        [[], [3], [3], [1], [], [], [], []],
        [None, None, None, None, 1, 3, 3, False],
        [],
    ),
    (
        ["MinHeap", "push", "push", "push", "snapshot"],
        [[], [-1], [4], [0], []],
        [None, None, None, None, "SNAPSHOT_CHECK"],
        [-1, 0, 4],
    ),
]

# Exception tests:
exception_tests = [
    (["MinHeap", "pop"], [[], []], "IndexError"),
    (["MinHeap", "peek"], [[], []], "IndexError"),
]


def test_harness() -> None:
    print("--- Running Tests for: MinHeap ---")
    passed = 0

    for i, (commands, args, expected, final_contents) in enumerate(tests, 1):
        heap = None
        results: List[Any] = []
        ok = True
        err = ""

        try:
            for cmd, arg in zip(commands, args):
                if cmd == "MinHeap":
                    heap = MinHeap()
                    results.append(None)
                elif cmd == "push":
                    heap.push(arg[0])
                    results.append(None)
                elif cmd == "pop":
                    results.append(heap.pop())
                elif cmd == "peek":
                    results.append(heap.peek())
                elif cmd == "__len__":
                    results.append(len(heap))
                elif cmd == "__bool__":
                    results.append(bool(heap))
                elif cmd == "snapshot":
                    snap = heap.snapshot()
                    if expected[len(results)] == "SNAPSHOT_CHECK":
                        results.append("SNAPSHOT_CHECK" if sorted(snap) == sorted(final_contents) else "SNAPSHOT_MISMATCH")
                    else:
                        results.append(snap)
                else:
                    raise ValueError(f"Unknown command: {cmd}")

            if results != expected:
                ok = False
                err = f"Return mismatch | expected={expected}, got={results}"

            if ok and sorted(heap.snapshot()) != sorted(final_contents):
                ok = False
                err = f"Final heap mismatch | expected elements={final_contents}, got snapshot={heap.snapshot()}"

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
    print("--- Running Exception Tests for: MinHeap ---")
    passed = 0
    for i, (commands, args, expected_exc) in enumerate(exception_tests, 1):
        heap = None
        ok = False
        try:
            for cmd, arg in zip(commands, args):
                if cmd == "MinHeap":
                    heap = MinHeap()
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
