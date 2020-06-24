# -*- coding:utf-8 -*-
# @Filename : Insertion Sort.py 
# @Author : Lizi
# @Time : 2020/6/22 11:29 
# @Software: PyCharm

'''它的工作原理是通过构建有序序列，对于未排序数据，在已排序序列中从后向前扫描，找到相应位置并插入。'''
#
def insertionSort(arr):

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


arr = [12, 11, 13, 5, 6]
insertionSort(arr)
print("排序后的数组:")
for i in range(len(arr)):
    print("%d" % arr[i])

