"""
Problem: Contains Duplicate
Category: Arrays & Hashing
Difficulty: Easy

Given an integer array nums, return true if any value appears at least twice in the array, 
and return false if every element is distinct.

Example 1:
Input: nums = [1,2,3,1]
Output: true

Example 2:
Input: nums = [1,2,3,4]
Output: false

Example 3:
Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true
"""

from typing import List

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False


# Test cases to run locally
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    nums1 = [1, 2, 3, 1]
    print(f"Test Case 1: {nums1} -> {solution.containsDuplicate(nums1)} (Expected: True)")
    
    # Test Case 2
    nums2 = [1, 2, 3, 4]
    print(f"Test Case 2: {nums2} -> {solution.containsDuplicate(nums2)} (Expected: False)")

    # Test Case 3
    nums3 = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
    print(f"Test Case 3: {nums3} -> {solution.containsDuplicate(nums3)} (Expected: True)")
