class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        quadruplets = []
        nums.sort()
        for i in range(len(nums) - 3):
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            for j in range(i + 1, len(nums) - 2):
                if j > i + 1 and nums[j] == nums[j - 1]:
                    continue

                two_sum_target = target - nums[i] - nums[j]
                l = j + 1
                r = len(nums) - 1

                while l < r:
                    current_sum = nums[l] + nums[r]
                    if current_sum < two_sum_target:
                        l += 1
                    elif current_sum > two_sum_target:
                        r -= 1
                    else:
                        quadruplets.append([nums[i], nums[j], nums[l], nums[r]])
                        while l < r and nums[l] == nums[l + 1]:
                            l += 1
                        while l < r and nums[r] == nums[r - 1]:
                            r -= 1

                        l += 1
                        r -= 1

        return quadruplets
