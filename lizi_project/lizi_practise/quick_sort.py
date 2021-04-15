#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : quick_sort.py
# @Author: Lizi
# @Date  : 2020/10/14

def partition(arr, begin, end):
    # arr[] --> 排序数组
    # low  --> 起始索引
    # high  --> 结束索引
    i = begin-1
    pivot = arr[end]

    for j in range(begin, end):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[end] = arr[end], arr[i+1]
    return i+1


def quicksort(arr, begin, end):
    if begin < end:
        pi = partition(arr, begin, end)
        quicksort(arr, begin, pi-1)
        quicksort(arr, pi+1, end)

if __name__ == '__main__':
    arr = [10, 7, 8, 9, 1, 5]
    n = len(arr)
    quicksort(arr, 0, n - 1)
    print("排序后的数组:")
    for i in range(n):
        print("{}".format(arr[i]))