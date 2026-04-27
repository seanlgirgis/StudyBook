"""
Problem: Container With Most Water
Category: Two Pointers
Difficulty: Medium

You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

Example 1:
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. 
In this case, the max area of water (blue section) the container can contain is 49.
(Lines at index 1 (height 8) and index 8 (height 7). Width = 8-1 = 7. Height = min(8,7) = 7. Area = 7*7 = 49).

Example 2:
Input: height = [1,1]
Output: 1
"""

from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        """
        Two Pointer Approach:
        - Start with widest container (left=0, right=n-1)
        - Calculate area and track maximum
        - Move the pointer pointing to the shorter line inward
        - Why? Moving the taller pointer can only decrease area
        
        Time Complexity: O(n) - single pass through array
        Space Complexity: O(1) - only using two pointers
        """
        
        left = 0
        right = len(height) - 1
        max_area = 0        
        while left < right:
            # Calculate current area
            # Width: distance between pointers
            # Height: minimum of the two heights (water level)
            width = right - left
            current_height = min(height[left], height[right])
            current_area = width * current_height
            
            # Update maximum area
            max_area = max(max_area, current_area)
            
            # Move the pointer pointing to the shorter line
            # This gives us the best chance to find a larger area
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        
        return max_area            

        
        # TODO: Implement this method
        # Hint: Start with widest container (pointers at 0 and n-1).
        # We want to maximize: (right - left) * min(height[left], height[right])
        # Which side do we shrink? The shorter one! Why?
        pass

# Test cases to run locally
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    h1 = [1,8,6,2,5,4,8,3,7]
    print(f"Test Case 1: {h1} -> {solution.maxArea(h1)} (Expected: 49)")
    
    # Test Case 2
    h2 = [1, 1]
    print(f"Test Case 2: {h2} -> {solution.maxArea(h2)} (Expected: 1)")
