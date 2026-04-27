
"""
Two Sum - Optimization Explanation

Your solution:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]

Analysis:
- This is the "Brute Force" approach.
- You have nested loops.
- Time Complexity: O(n^2). If the array has 10,000 items, this does ~100,000,000 operations. Too slow!

Optimized Approach (Hash Map):
- We want to find `target - nums[i]`.
- Instead of scanning the rest of the array to find it, what if we could look it up instantly?
- We use a dictionary: `val -> index`.

Example: nums = [2, 7, 11, 15], target = 9
1. i=0, val=2.  Needed=7. Is 7 in map? No. Add {2: 0} to map.
2. i=1, val=7.  Needed=2. Is 2 in map? YES! Return [map[2], 1] -> [0, 1].
- Time Complexity: O(n). We only pass through the list once.
"""

from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Map to store: value -> index
        prevMap = {}  
        
        for i, n in enumerate(nums):
            diff = target - n
            if diff in prevMap:
                return [prevMap[diff], i]
            prevMap[n] = i
        return []

# Test cases to run locally
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    nums1, target1 = [2, 7, 11, 15], 9
    print(f"Test Case 1: {nums1}, target {target1} -> {solution.twoSum(nums1, target1)} (Expected: [0, 1])")
    
    # Test Case 2
    nums2, target2 = [3, 2, 4], 6
    print(f"Test Case 2: {nums2}, target {target2} -> {solution.twoSum(nums2, target2)} (Expected: [1, 2])")
