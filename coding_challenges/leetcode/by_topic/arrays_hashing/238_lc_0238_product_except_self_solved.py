"""
Product Except Self - Optimization Explanation

Your solution:
    Nested loops: for i ... for j ...
    Complexity: O(N^2). 
    - Functionally correct (it gets the right numbers).
    - But for N=100,000, N^2 is 10,000,000,000 operations. It will timeout.
    - The constraint was O(N).

Optimized Approach (Prefix & Suffix):
    We can't use division. So how do we get product except self?
    Index i = (Product of everything Left) * (Product of everything Right)
    
    1. Create an output array 'res' initialized to 1.
    2. Pass 1 (Prefix): Iterate forward. Accumulate product of elements to the left.
       [1, 2, 3, 4] -> [1, 1, 2, 6] (at index 3, 1*2*3=6)
    3. Pass 2 (Suffix): Iterate backward. Accumulate product of elements to the right.
       Multiply this with the existing value in 'res'.
    
    Complexity: O(N). Two passes. No nested loops.
"""

from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [1] * n
        
        # Pass 1: Prefix products
        # Store the product of all elements to the LEFT of i
        prefix = 1
        for i in range(n):
            res[i] = prefix
            prefix *= nums[i]
            print(f"i={i}, prefix={prefix}, res[i]={res[i]}")
        print('-' * 50)
        # Pass 2: Suffix products
        # Multiply by the product of all elements to the RIGHT of i
        postfix = 1
        for i in range(n - 1, -1, -1):
            res[i] *= postfix
            postfix *= nums[i]
            print(f"i={i}, postfix={postfix}, res[i]={res[i]}")
            
        return res

# Test cases to run locally
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    nums1 = [1, 2, 3, 4]
    print(f"Test Case 1: {nums1} -> {solution.productExceptSelf(nums1)} (Expected: [24, 12, 8, 6])")
    
    # Test Case 2
#    nums2 = [-1, 1, 0, -3, 3]
#    print(f"Test Case 2: {nums2} -> {solution.productExceptSelf(nums2)} (Expected: [0, 0, 9, 0, 0])")
