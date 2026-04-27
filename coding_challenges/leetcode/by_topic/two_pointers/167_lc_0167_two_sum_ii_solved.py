"""
Problem: Two Sum II - Input Array Is Sorted
Category: Two Pointers
Difficulty: Medium

Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number.

Return the indices of the two numbers, index1 and index2, added by one as an integer array [index1, index2] where 1 <= index1 < index2 <= numbers.length.

The tests are generated such that there is exactly one solution. You may not use the same element twice.
Your solution must use only constant extra space.

Example 1:
Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].

Example 2:
Input: numbers = [2,3,4], target = 6
Output: [1,3]
Explanation: The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].

Example 3:
Input: numbers = [-1,0], target = -1
Output: [1,2]
"""

from typing import List

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1
        while (left < right) :
            s = numbers[left] + numbers[right]
            if s == target:
                return left+1, right+1
            elif s < target:
                left +=1
            else:
                right -= 1
        return

# Test cases to run locally
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    nums1, target1 = [2, 7, 11, 15], 9
    print(f"Test Case 1: nums={nums1}, target={target1} -> {solution.twoSum(nums1, target1)} (Expected: [1, 2])")
    
    # Test Case 2
    nums2, target2 = [2, 3, 4], 6
    print(f"Test Case 2: nums={nums2}, target={target2} -> {solution.twoSum(nums2, target2)} (Expected: [1, 3])")

    # Test Case 3 (Counter Example)
    nums3, target3 = [2, 3, 4], 7
    print(f"Test Case 3: nums={nums3}, target={target3} -> {solution.twoSum(nums3, target3)} (Expected: [2, 3])")
