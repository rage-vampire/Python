# -*- coding: utf-8 -*-
# @Date : 2021/7/19 13:58
# @File : 01_twoSum.py
# @Author : Lizi

"""给定一个整数数组 nums和一个整数目标值 target，请你在该数组中找出 和为目标值 target 的那两个整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。
"""



def twoSum(nums, target_sum):
    """使用for循环便利，时间复杂度为O(n²)"""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if target_sum == nums[i] + nums[j]:

                return [i, j]
    # else:
    #     print("未找到这两个数")
    return [None, None]


# def twoSum(nums, target_sum):
#     """使用哈希表"""
#     hashtable = dict()
#     for i, num in enumerate(nums):
#         if (target_sum - num) in hashtable:
#             return [hashtable[target_sum - num], i]
#         hashtable[nums[i]] = i
#     return [None, None]


if __name__ == "__main__":
    num = [1, 2, 3, 4, 5, 6, 7]
    target = 5
    sum = twoSum(num, target)
    print(f"第一个数的索引值为:{sum[0]}, 第二个数的索引值为:{sum[1]}")
