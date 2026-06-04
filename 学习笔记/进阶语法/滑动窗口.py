def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        slow=-1
        sum=0
        ans=len(nums)
        for i in nums:
            sum+=i
            while sum>=target:
                ans=min(i-slow,ans)
                slow+=1
                sum-=nums[slow]
        if ans<=len(nums):
             return 
        return ans
