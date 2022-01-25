# -*- coding: utf-8 -*-
# @Date : 2021/12/17 19:14
# @File : Two_Sum.py
# @Author : Lizi
from typing import List

"""
题目：
    给定一个整数数组 nums和一个整数目标值 target，请你在该数组中找出 和为目标值 target 的那两个整数，并返回它们的数组下标。
    你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。你可以按任意顺序返回答案。

解题思路：
    最容易想到的方法是枚举数组中的每一个数 x，寻找数组中是否存在 target - x。
    当我们使用遍历整个数组的方式寻找 target - x 时，需要注意到每一个位于 x 之前的元素都已经和 x 匹配过，因此不需要再进行匹配。
    而每一个元素不能被使用两次，所以我们只需要在 x 后面的元素中寻找 target - x
"""


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []


if __name__ == "__main__":
    result = Solution()
    aa = result.twoSum([1, 2, 3, 4, 5], 4)
    print(aa)
    # print(result.two_sum([1,2,35,6],8))
