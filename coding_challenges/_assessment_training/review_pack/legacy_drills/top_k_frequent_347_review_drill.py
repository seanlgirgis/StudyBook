# LeetCode 347: Top K Frequent Elements (Review Drill)

from typing import Callable, List, Tuple
from collections import Counter
import heapq
import sys

# --- TEST CASES ---
# Format: (nums_array, k, expected_one_valid_answer)
top_k_tests: List[Tuple[List[int], int, List[int]]] = [
    ([1, 1, 1, 2, 2, 3], 2, [1, 2]),
    ([1], 1, [1]),
    ([4, 4, 4, 6, 6, 2], 1, [4]),
    ([5, 5, 6, 6, 7, 7, 7], 2, [7, 5]),
    ([-1, -1, -2, -2, -2, 3], 2, [-2, -1]),
    ([10, 10, 20, 20, 20, 30, 30, 30, 30], 2, [30, 20]),
    ([1, 2, 3, 4, 4, 4, 5, 5], 3, [4, 5, 1]),
    ([9, 9, 8, 8, 8, 7, 7, 7, 7], 3, [7, 8, 9]),
    ([0, 0, 0, 1, 1, 2], 2, [0, 1]),
    ([100, 200, 100, 300, 200, 100], 2, [100, 200]),
    ([1, 1, 1, 2, 2, 3], 0, []),
    ([1, 2, 2], 5, []),
]


def _is_valid_top_k(nums: List[int], k: int, result: List[int]) -> Tuple[bool, str]:
    freq = Counter(nums)

    if not isinstance(result, list):
        return False, f"Result must be List[int], got {type(result).__name__}"

    # Guard-rail behavior for out-of-spec k values in practice drills.
    if k <= 0:
        if len(result) == 0:
            return True, "ok"
        return False, f"For k={k}, expected empty list, got length {len(result)}"
    if k > len(freq):
        if len(result) == 0:
            return True, "ok"
        return False, (
            f"For k={k} > unique_count={len(freq)}, expected empty list, "
            f"got length {len(result)}"
        )

    if len(result) != k:
        return False, f"Result length must be {k}, got {len(result)}"
    if len(set(result)) != len(result):
        return False, "Result contains duplicate elements"

    for value in result:
        if value not in freq:
            return False, f"Element {value} is not present in input"

    selected = set(result)
    min_selected_freq = min(freq[x] for x in selected)
    for value, count in freq.items():
        if value not in selected and count > min_selected_freq:
            return False, (
                f"Excluded value {value} has higher frequency ({count}) than "
                f"selected boundary frequency ({min_selected_freq})"
            )

    return True, "ok"


# --- TEST HARNESS ---
def test_harness(
    func: Callable[[List[int], int], List[int]],
    test_cases: List[Tuple[List[int], int, List[int]]],
) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0
    for i, (nums, k, expected) in enumerate(test_cases):
        try:
            result: List[int] = func(nums.copy(), k)
            valid, reason = _is_valid_top_k(nums, k, result)
            if valid:
                print(f"Test {i + 1}: PASSED")
                passed += 1
            else:
                print(f"Test {i + 1}: FAILED")
                print(f"    Reason: {reason}")
                print(f"    Expected set: {set(expected)}")
                print(f"    Got set:      {set(result) if isinstance(result, list) else result}")
        except Exception as e:
            print(f"Test {i + 1}: ERROR | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.")


# --- YOUR IMPLEMENTATIONS ---
def topKFrequent_bucket(nums: List[int], k: int) -> List[int]:
    """
    Implement bucket-sort approach.

    Target:
    - Time: O(n)
    - Space: O(n)
    """
    freq = Counter(nums)
    if k == 0 : return []
    if len(freq) < k : return []
    res = []
    bkts = [[]  for _ in range(len(nums)+1 ) ]
    max_freq = 0
    # now we have a bucket for every possible freq from 0 to len of nums
    for n, f in freq.items():
        bkts[f].append(n)
        max_freq = max(max_freq, f)
    for i in range( max_freq, 0 , -1):
        res.extend(bkts[i])
        if len(res) >= k : break
    return res[:k] if len(res) >=k else []



def topKFrequent_minheap(nums: List[int], k: int) -> List[int]:
    """
    Implement min-heap approach.

    Target:
    - Time: O(n log k)
    - Space: O(n)
    """
    freq = Counter(nums)
    if k == 0 : return []
    if len(freq) < k : return []
    heap = []
    for n , f in freq.items():
        heapq.heappush(heap, [f, n])
        if len(heap) > k :  heapq.heappop(heap)
    return [] if len(heap) < k else  [n for _,n in heap]



   

print("\n=== 347 Bucket Review ===")
test_harness(topKFrequent_bucket, top_k_tests)

print("\n=== 347 Min-Heap Review ===")
test_harness(topKFrequent_minheap, top_k_tests)
