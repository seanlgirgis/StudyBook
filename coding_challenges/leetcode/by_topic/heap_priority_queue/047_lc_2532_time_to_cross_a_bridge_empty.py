"""
LeetCode 2532 - Time to Cross a Bridge (Hard)

Practice scaffold (empty implementation).

What the input means:
- n: number of boxes to move from right -> left
- k: number of workers
- time[i] for worker i is:
  [left_to_right, pick_old_box, right_to_left, put_new_box]4

Bridge rules:
1) At most one worker can be on the bridge at any time.
2) Workers waiting on the RIGHT side have higher priority than workers waiting
   on the LEFT side.
3) On the same side, the "less efficient" worker crosses first, where:
   efficiency_key(i) = time[i][0] + time[i][2]
   larger key means less efficient; tie breaks by larger index.

Return:
- Elapsed time when the LAST box reaches the left side.
  (Do not wait for the final put_new_box action.)
"""

import heapq
from dataclasses import dataclass
from typing import Callable, List, Tuple


# --- TEST CASES ---
# Format: (n, k, time_matrix, expected)
tests: List[Tuple[int, int, List[List[int]], int]] = [
    (1, 3, [[1, 1, 2, 1], [1, 1, 3, 1], [1, 1, 4, 1]], 6),
    (3, 2, [[1, 9, 1, 8], [10, 10, 10, 10]], 50),
    (1, 1, [[5, 5, 5, 5]], 15),
    (5, 1, [[1, 1, 1, 1]], 19),
    (10, 5, [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4], [5, 5, 5, 5]], 87),
    (2, 2, [[1, 1, 1, 1], [1, 1, 1, 1]], 4),
    (3, 4, [[1, 2, 3, 4], [4, 3, 2, 1], [1, 1, 1, 1], [10, 10, 10, 10]], 32),
    (2, 3, [[3, 1, 1, 1], [1, 1, 3, 1], [2, 1, 2, 1]], 8),
]


def harness(func: Callable[[int, int, List[List[int]]], int]) -> None:
    """Simple harness for local practice."""
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0

    for test_no, (n, k, time_matrix, expected) in enumerate(tests, 1):
        try:
            got = func(n, k, [row[:] for row in time_matrix])  # defensive copy
            if got == expected:
                print(f"Test {test_no}: PASSED")
                passed += 1
            else:
                short_time = str(time_matrix) if len(time_matrix) <= 3 else f"{time_matrix[:2]}..."
                print(
                    f"Test {test_no}: FAILED | expected={expected}, got={got} "
                    f"| n={n}, k={k}, time={short_time}"
                )
        except Exception as exc:
            short_time = str(time_matrix) if len(time_matrix) <= 3 else f"{time_matrix[:2]}..."
            print(
                f"Test {test_no}: ERROR  | {type(exc).__name__}: {exc} "
                f"| n={n}, k={k}, time={short_time}"
            )

    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")
    
    
# Minimum heap that keeps track of a tuples

import heapq
class MinHeapt:
    def __init__(self):
        self._data = []
    def push(self, a, b):
        heapq.heappush(self._data , (a,b))
    def pop(self):
        return heapq.heappop(self._data)
    def peek(self):
        return self._data[0]    
    def __bool__(self):
        return bool(self._data)
    def __len__(self):
        return len(self._data) 
        
# Maximum heap that keeps track of a tuples
class MaxHeapt:
    def __init__(self):
        self._data = []
    def push(self, a, b):
        heapq.heappush(self._data , (-a,-b))
    def pop(self):
        (a,b) = heapq.heappop(self._data)
        return (-a, -b)
    def peek(self):
        (a,b) = self._data[0]
        return (-a, -b)
    def __bool__(self):
        return bool(self._data)
    def __len__(self):
        return len(self._data)  

def findCrossingTime(n: int, k: int, time: List[List[int]]) -> int:
    boxes_crossed_to_left, clock, boxes_available_to_pick_right_to_left = 0, 0 , n
    
    @dataclass(frozen=True)
    class Worker:
        worker_id: int
        left_to_right: int
        pick_box: int
        right_to_left: int
        put_box: int

        @property
        def inefficiency(self) -> int:
            return self.left_to_right + self.right_to_left

        def finish_pick_at_right(self) -> int:
            return clock + self.pick_box

        def finish_put_at_left(self) -> int:
            return clock + self.put_box   
    
    
    workers = [Worker(
            worker_id=i,
            left_to_right=row[0],
            pick_box=row[1],
            right_to_left=row[2],
            put_box=row[3],
        ) for i, row in enumerate(time)]
    for worker in workers: print(worker.worker_id)

harness(findCrossingTime)