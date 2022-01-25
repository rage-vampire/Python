# -*- coding: utf-8 -*-
# @Date : 2021/12/19 17:49
# @File : 05_findMedianSortedArrays.py
# @Author : Lizi
import math


def findMedianSortedArrays(nums1, nums2) -> float:
    nums1.extend(nums2)
    # nums1.sort()
    new_num = sorted(nums1)
    if len(new_num) == 0:
        return 0
    elif len(new_num) == 1:
        return nums1[0]
    elif len(new_num) % 2 == 0:
        mid_index = int(len(new_num) / 2)
        mid_num = (new_num[mid_index - 1] + new_num[mid_index]) / 2
        return mid_num
    elif len(new_num) % 2 != 0:
        mid_index = math.ceil(len(new_num) / 2)
        mid_num = new_num[mid_index-1]
        return mid_num


if __name__ == "__main__":
    result = findMedianSortedArrays([3, 2], [7, 6])
    print('中位数为：{}'.format(result))
