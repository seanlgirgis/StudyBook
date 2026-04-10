# LeetCode 347: Top K Frequent Elements (Round 01 Empty)
from typing import Callable, List, Tuple
from collections import Counter

tests: List[Tuple[List[int], int, List[int]]] = [
    ([1, 1, 1, 2, 2, 3], 2, [1, 2]),
    ([1], 1, [1]),
    ([5, 5, 6, 6, 7, 7, 7], 2, [7, 5]),
    ([-1, -1, -2, -2, -2, 3], 2, [-2, -1]),
    ([1, 1, 1, 2, 2, 3], 0, []),
]

def _is_valid_top_k(nums: List[int], k: int, result: List[int]) -> bool:
    freq = Counter(nums)
    if not isinstance(result, list):
        return False
    if k <= 0:
        return len(result) == 0
    if k > len(freq):
        return len(result) == 0
    if len(result) != k or len(set(result)) != len(result):
        return False
    for x in result:
        if x not in freq:
            return False
    selected = set(result)
    min_sel = min(freq[x] for x in selected)
    for v, c in freq.items():
        if v not in selected and c > min_sel:
            return False
    return True

def harness(
    func: Callable[[List[int], int], List[int]],
    name: str,
) -> None:
    print(f"--- Running Tests for: {name} ---")
    passed = 0
    for i, (nums, k, _) in enumerate(tests, 1):
        try:
            result = func(nums.copy(), k)
            if _is_valid_top_k(nums, k, result):
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | got={result}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")


def topKFrequent_bucket(nums: List[int], k: int) -> List[int]:
   
    res: list[int] = []
    freq = Counter(nums)
    bckts = [[] for _ in range(len(nums) + 1)]
    max_freq = 0
    for n,f in freq.items():
        max_freq = max(max_freq, f)
        bckts[f].append(n)
    for i in range(max_freq, 0, -1):
        res.extend(bckts[i])
        if len(res) >= k :
            break
    return res[:k] if len(res) >= k else []
    
    
#print(topKFrequent_bucket([5, 5, 6, 6, 7, 7, 7], 2)    )
    
import heapq    
def topKFrequent_minheap(nums: List[int], k: int) -> List[int]:   
    freq = Counter(nums)
    heap = []
    for n,f in freq.items():
        heapq.heappush(heap, (f, n))
        if len(heap) > k:
            heapq.heappop(heap)
    return [n for _,n in heap] if len(heap) == k else []

print("\n=== 347 Bucket ===")
harness(topKFrequent_bucket, "topKFrequent_bucket")

print("\n=== 347 Min-Heap ===")
harness(topKFrequent_minheap, "topKFrequent_minheap")

