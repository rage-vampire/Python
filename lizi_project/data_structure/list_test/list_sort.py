#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : list_sort.py
# @Author: Lizi
# @Date  : 2020/9/9

def list_sort_string():
    L = ["delphi","Delphi","python","Python","c++","C++","c","C","golang","Golang"]
    L.sort()
    print('升序:', L)
    L.sort(reverse=True)
    print('降序:', L)


def list_sort_num():
    L = [30,40,10,50,50.1,80,60,100,90]
    L.sort()
    print('升序:', L)
    L.sort(reverse=True)
    print('降序:', L)

def list_sort_by_length():
    L = ["delphi","Delphi","python","Python","c++","C++","c","C","golang","Golang"]
    L.sort(key=lambda ele:len(ele))
    print('升序:', L)
    L.sort(key=lambda ele:len(ele), reverse=True)
    print('降序:', L)


def two_d_list_sort():
    L = [["1", "c++", "demo"],
            ["1", "c", "test"],
            ["2", "java", ""],
            ["8", "golang", "google"],
            ["4", "python", "gil"],
            ["5", "swift", "apple"]
        ]
    L.sort(key=lambda ele:ele[1])  # 根据第二个元素来排序
    print('升序:', L)
    L.sort(key=lambda ele:len(ele[1]))   # 根据第二个元素的长度来排序
    print('升序:', L)


def two_d_list_sort2(sort_index):
    L = [["1", "c++", "demo"],
            ["1", "c", "test"],
            ["2", "java", ""],
            ["8", "golang", "google"],
            ["4", "python", "gil"],
            ["5", "swift", "apple"]
        ]
    key_set = ''
    for item in sort_index.split(','):
        key_set += "ele[" + item + "]+"

    key_set = key_set.rstrip('+')
    L.sort(key=lambda ele:eval(key_set))
    print('排序索引：',sort_index,L)


if __name__ == '__main__':
    list_sort_string()
    list_sort_num()
    list_sort_by_length()
    two_d_list_sort()
    two_d_list_sort2('0')
    two_d_list_sort2('1')
    two_d_list_sort2('2')
    two_d_list_sort2('0,1')