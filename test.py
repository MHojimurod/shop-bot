
# # for i in nums:
# #     if target-i in nums[nums.index(i)+1:]:
# #         if i == target-i:
# #             print(nums.index(i),nums[nums.index(i)+1:].index(target-i)+len(nums[:nums.index(i)+1]))
# #         else:
# #             print(nums.index(i),nums.index(target-i))
# # s = "MCMXCIV"



# SUM = 0
# symbols = {
#     "I": 1,
#     "V": 5,
#     "X": 10,
#     "L": 50,
#     "C": 100,
#     "D": 500,
#     "M": 1000,

# }
# extra_symbols = {
#     "CM": 900,
#     "XC": 90,
#     "IX": 9,
#     "CD": 400,
#     "XL": 40,
#     "IV": 4
# }
# check_s = [j for j in extra_symbols.keys()]
# for key,value in extra_symbols.items():
#     if key in s:
#         SUM += value
#         s = s.replace(key,"")
# for i in s:
#     SUM += symbols[i]

# print(SUM)




# string = "HEllo   World   "



# string = string.split()
# print(string)
# # print(len(string[-1]))


class Solution:
    def moveZeroes(self, nums: "List[int]") -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        found = 0
        res = []
        i = 0
        while len(nums) > i:
            if nums[i] == 0:found += 1
            else:res.append(nums[i])
            i += 1
        
        for i in range(found): res.append(0)
        (res.append(0) for i in range(found))
        nums[:] = res
        return nums

s = Solution()


print(
s.moveZeroes([0,0,1])
)


# is even

def is_even(n):
    return n % 2 == 0