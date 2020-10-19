#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : selection_sort.py
# @Author: Lizi
# @Date  : 2020/10/14



'''选择排序，首先在未排序序列中找到最小元素，存放到排序序列的起始位置，然后，再从剩余未排序元素中继续寻找最小元素，
然后放到已排序序列的末尾。以此类推，直到所有元素均排序完毕'''
def selection_sort(arr):
    for i in range(len(arr)):
        mini = i
        for j in range(i+1, len(arr)):
            if arr[mini] > arr[j]:
                arr[mini], arr[j] = arr[j], arr[mini]
    print(arr)


if __name__ == '__main__':
    arr = [10, 7, 8, 9, 1, 5]
    print(selection_sort(arr))

