from typing import Any, Callable, List, Optional, Tuple

# --- TEST CASES ---
# Format: {"commands": [...], "args": [...], "expected": [...]}
median_finder_tests: List[dict] = [
    {
        "commands": ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"],
        "args": [[], [1], [2], [], [3], []],
        "expected": [None, None, None, 1.5, None, 2.0]
    },
    {
        "commands": ["MedianFinder", "addNum", "findMedian", "addNum", "findMedian", "addNum", "findMedian"],
        "args": [[], [-1], [], [-2], [], [-3], []],
        "expected": [None, None, -1.0, None, -1.5, None, -2.0]
    },
    {
        "commands": ["MedianFinder", "addNum", "findMedian"],
        "args": [[], [5], []],
        "expected": [None, None, 5.0]
    },
    {
        "commands": ["MedianFinder"],
        "args": [[]],
        "expected": [None]
    }
]

# --- TEST HARNESS ---
def test_harness(target_class: type, test_cases: List[dict]) -> None:
    """
    Test harness for LeetCode #295: Find Median from Data Stream.
    Validates sequential state execution and floating-point accuracy.
    """
    print(f"--- Running Tests for: {target_class.__name__} ---")
    passed: int = 0
    
    for i, tc in enumerate(test_cases):
        commands: List[str] = tc["commands"]
        args: List[List[Any]] = tc["args"]
        expected: List[Optional[float]] = tc["expected"]
        
        obj = None
        results: List[Optional[float]] = []
        test_passed: bool = True
        error_msg: str = ""
        
        try:
            # Execute commands
            for cmd, arg in zip(commands, args):
                if cmd == "MedianFinder":
                    obj = target_class()
                    results.append(None)
                elif cmd == "addNum":
                    obj.addNum(arg[0])
                    results.append(None)
                elif cmd == "findMedian":
                    results.append(obj.findMedian())
                else:
                    raise ValueError(f"Unknown command: {cmd}")
            
            # Validate results
            for step, (res, exp) in enumerate(zip(results, expected)):
                if exp is not None:
                    # Floating point safety check
                    if res is None or abs(res - exp) > 1e-5:
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



#
# PROBLEM STATEMENT
# Design a data structure that supports adding numbers and finding the median at any time.
#
# EXAMPLE FLOW
# add 1, add 2, findMedian -> 1.5
# add 3, findMedian -> 2.0
#
# WHAT TO IMPLEMENT
# Implement class `MedianFinder` with `addNum` and `findMedian` efficiently
# (commonly with two heaps).




import heapq

class MaxHeap:
    def __init__(self):
        self._heap = []

    def push(self, val):
        heapq.heappush(self._heap, -val)

    def pop(self):
        return -heapq.heappop(self._heap)

    def peek(self):
        return -self._heap[0]

    def __len__(self):
        return len(self._heap)

    def __bool__(self):
        return bool(self._heap)

class MinHeap:
    def __init__(self):
        self._heap = []

    def push(self, val):
        heapq.heappush(self._heap, val)

    def pop(self):
        return heapq.heappop(self._heap)

    def peek(self):
        return self._heap[0]

    def __len__(self):
        return len(self._heap)

    def __bool__(self):
        return bool(self._heap)        

# --- USER TO IMPLEMENT SOLUTION BELOW ---
class MedianFinder:
    def __init__(self):
        """
        initialize your data structure here.
        """
        self.small, self.large = MaxHeap(), MinHeap()

    def addNum(self, num: int) -> None:
        self.small.push(num)
        #make sure that every num in small is <= every num in large
        if self.small and self.large and self.small.peek() > self.large.peek():
            self.large.push(self.small.pop())
        if len(self.small) > len(self.large) + 1:
            self.large.push(self.small.pop())
        if len(self.large) > len(self.small) + 1:
            self.small.push(self.large.pop())
            

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return self.small.peek()
        if len(self.large) > len(self.small):
            return self.large.peek()
        return (self.small.peek() + self.large.peek()) / 2


# Execute harness without __main__ block
test_harness(MedianFinder, median_finder_tests)
