# LeetCode 295: Find Median from Data Stream (Empty)
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

class MedianFinder:
    def __init__(self): pass
    def addNum(self, num: int) -> None: pass
    def findMedian(self) -> float: pass

def harness() -> None:
    print("--- Running Tests for: MedianFinder ---")
    try:
        mf = MedianFinder()
        mf.addNum(1)
        mf.addNum(2)
        a = mf.findMedian()   # 1.5
        mf.addNum(3)
        b = mf.findMedian()   # 2.0
        mf.addNum(10)
        c = mf.findMedian()   # (2 + 3) / 2 = 2.5
        mf.addNum(-1)
        d = mf.findMedian()   # 2.0
        ok = (a, b, c, d) == (1.5, 2.0, 2.5, 2.0)
        print("Test 1: PASSED" if ok else f"Test 1: FAILED | got={(a,b,c,d)}")
    except Exception as e:
        print(f"Test 1: ERROR | {type(e).__name__}: {e}")

harness()

