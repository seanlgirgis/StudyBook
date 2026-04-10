# ============================================================================
# File: lc_295_find_median_from_data_stream.py
#
# LeetCode 295: Find Median from Data Stream (Hard)
#
# PROBLEM STATEMENT:
# The median is the middle value in an ordered integer list. If the size of 
# the list is even, there is no middle value, and the median is the mean of 
# the two middle values.
# 
# - For example, for arr = [2,3,4], the median is 3.
# - For example, for arr = [2,3], the median is (2 + 3) / 2 = 2.5.
#
# Implement the MedianFinder class:
# - MedianFinder() initializes the MedianFinder object.
# - void addNum(int num) adds the integer num from the data stream to the data structure.
# - double findMedian() returns the median of all elements so far. Answers 
#   within 10^-5 of the actual answer will be accepted.
# ============================================================================

from typing import List, Optional, Any

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

import heapq
class MinHeap:
    def __init__(self):
        self._heap = []
 
    def push(self, val):
        heapq.heappush(self._heap , val)
        
    def peek(self):
        return self._heap[0]
        
    def pop(self):
        return heapq.heappop(self._heap)
        
    def __len__(self):
        return len(self._heap)
        
    def __bool__(self):
        return bool(self._heap)

class MaxHeap:
    def __init__(self):
        self._heap = []
 
    def push(self, val):
        heapq.heappush(self._heap , -val)
        
    def peek(self):
        return -self._heap[0]
        
    def pop(self):
        return -heapq.heappop(self._heap)
        
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
        self.small = MaxHeap()
        self.big = MinHeap()



    def addNum(self, num: int) -> None:
        self.small.push(num)
        if self.small and self.big and self.small.peek() > self.big.peek():
            self.big.push(self.small.pop())
        if len(self.small) > len(self.big) + 1:
            self.big.push(self.small.pop())
        if len(self.big) > len(self.small) + 1:
            self.small.push(self.big.pop())


    def findMedian(self) -> float:
        if len(self.small) == len(self.big):
            return (self.small.peek() + self.big.peek())/2
        if len(self.small) > len(self.big):
            return float(self.small.peek())
        return float(self.big.peek())
            


# Execute harness without __main__ block
test_harness(MedianFinder, median_finder_tests)
