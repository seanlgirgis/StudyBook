"""
Problem: 3Sum
Category: Two Pointers
Difficulty: Medium

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Example 1:
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].

Example 2:
Input: nums = [0,1,1]
Output: []
"""

from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        if len(nums) < 3:
            return []
            
        result = []
        nums.sort()  # Critical first step!
        
        for i in range(len(nums) - 2):
            # Skip duplicates for the first number
            if i > 0 and nums[i] == nums[i - 1]:
                continue
                
            # Early termination: if smallest number is already > 0 → impossible
            if nums[i] > 0:
                break
                
            # Two pointers for the remaining part
            left = i + 1
            right = len(nums) - 1
            target = -nums[i]
            
            while left < right:
                current_sum = nums[left] + nums[right]
                
                if current_sum == target:
                    # Found a valid triplet
                    result.append([nums[i], nums[left], nums[right]])
                    
                    # Skip duplicates for left and right
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                        
                    left += 1
                    right -= 1
                    
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
                    
        return result

# Test cases to run locally
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    nums1 = [-1, 0, 1, 2, -1, -4]
    print(f"Test Case 1: {nums1} -> {solution.threeSum(nums1)}")
    
    # Test Case 2
    nums2 = [0, 1, 1]
    print(f"Test Case 2: {nums2} -> {solution.threeSum(nums2)}")
