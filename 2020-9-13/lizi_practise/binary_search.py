#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : binary_search.py
# @Author: Lizi
# @Date  : 2020/10/14

def binary_search(arr, num ,lower=0, upper=None):
    if upper is None:
        upper = len(arr) - 1

    if upper >= lower:
        # middle = int(lower + (upper-1) / 2)
        middle = (lower+upper) // 2
        if num == arr[middle]:
            return middle
        elif num > arr[middle]:
            return binary_search(arr, num, middle+1, upper)
        else:
            return binary_search(arr, num, lower, middle)
    else:
        return -1


if __name__ == '__main__':
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    num = 11
    result = binary_search(arr, num)

    if result != -1:
        print("元素在数组中的索引为{}".format(result))
    else:
        print("元素不在数组中")


