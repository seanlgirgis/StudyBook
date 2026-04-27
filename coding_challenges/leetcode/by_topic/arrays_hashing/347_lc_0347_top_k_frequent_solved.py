"""
Top K Frequent - Optimization Explanation

Your solution:
    freq = Counter(nums)
    return [num for num, _ in freq.most_common(k)]
    
    Complexity: O(N log K). 
    - Counting is O(N).
    - most_common(k) uses a heap to find the top k, which takes O(N log K).
    - This is excellent and usually accepted in interviews.

Optimized Approach (Bucket Sort):
    Complexity: O(N) Time, O(N) Space.
    
    Concept:
    - We know the frequency of any number cannot exceed N (length of array).
    - Create an array of lists called 'buckets' where the index represents the frequency.
    - buckets[5] = [list of numbers that appear 5 times].
    - Iterate backwards from N to 1. Collect numbers until we have k of them.
    
    Data Transform:
    [1,1,1,2,2,3] -> Counts: {1:3, 2:2, 3:1}
    Buckets (Index=Freq):
    0: []
    1: [3]
    2: [2]
    3: [1]
    4: []
    5: []
    6: []
    
    Iterate back: Get 1 from bucket[3], get 2 from bucket[2]. Done.
"""

from typing import List
from collections import Counter

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # User Implementation (O(N log K)) - Very good!
        freq = Counter(nums)
        return [num for num, _ in freq.most_common(k)]

    def topKFrequentBucketSort(self, nums: List[int], k: int) -> List[int]:
        # O(N) Implementation
        count = Counter(nums)
        freq = [[] for i in range(len(nums) + 1)]
        
        for n, c in count.items():
            freq[c].append(n)
            
        res = []
        for i in range(len(freq) - 1, 0, -1):
            for n in freq[i]:
                res.append(n)
                if len(res) == k:
                    return res
        return []

# Test cases to run locally
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    nums1, k1 = [1,1,1,2,2,3], 2
    print(f"Test Case 1: nums={nums1}, k={k1} -> {solution.topKFrequent(nums1, k1)} (Expected: [1, 2])")
    
    # Test Case 2
    nums2, k2 = [1], 1
    print(f"Test Case 2: nums={nums2}, k={k2} -> {solution.topKFrequent(nums2, k2)} (Expected: [1])")
