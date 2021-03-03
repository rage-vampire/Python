#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 等差数列.py
# @Author: Lizi
# @Date  : 2020/12/23


# def dengcha_seq(first, step, seq_count):
#     list1 = []
#     for index in range(seq_count):
#         if index == 0:
#             list1.append(first)
#         else:
#             res = first + index * step
#             list1.append(res)
#     return list1
#
#
# if __name__ == '__main__':
#     seq = dengcha_seq(first=0, step=2, seq_count=10)
#     for num in seq:
#         print(num, end=' ')
#

def fib(n):
    first = 0
    second = 1
    if n == 0:
        res = first
    elif n == 1:
        res = second
    else:
        first, second = second, first+second
    return second


    # for index in range(n):
    #     if index == 0:
    #         res = first
    #     elif index == 1:
    #         res = second

if __name__ == '__main__':
    f = fib(10)
    print(f)
