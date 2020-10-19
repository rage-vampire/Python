#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : list_sort.py
# @Author: Lizi
# @Date  : 2020/10/10

# li = [1, 2, 5, 4, 3, 6, 7]
# list1 = []
# li.sort()
# list1.append(li.pop(0))
# list1.append(li.pop(0))
# print(list1)
#
# for index, item in enumerate(list1):
#     print(index, item)
#     li.append(list1[index])
# print(li)

'''实例1：数组翻转指定个数的元素'''
def leftrotatebyone(arr, n):
    temp = arr[0]
    for i in range(n-1):
        arr[i] = arr[i+1]
    arr[n-1] = temp


def leftrotate(arr, d, n):
    for i in range(d):
        leftrotatebyone(arr, n)


def printarry(arr, size):
    for i in range(size):
        print('{}'.format(arr[i]), end='')
    print('')

arr = [1, 2, 3, 4, 5, 6, 7]
leftrotate(arr, 2, 7)
printarry(arr, 7)



'''将列表中的首尾元素对换位置'''
list1 = [1, 2, 3, 4]
# for i in list1:
list1[0], list1[-1] = list1[-1], list1[0]
print('转换后的列表：', list1)


'''将列表中的指定位置的元素元素对换位置'''
def swapPositions(list, index1, index2):
    list[index1], list[index2] = list[index2], list[index1]
    print('转换后的列表：', list1)


list1 = [11, 22, 33, 44]
swapPositions(list1,0,2)