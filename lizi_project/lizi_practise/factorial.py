#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : factorial.py
# @Author: Lizi
# @Date  : 2020/9/8

'''N个数的阶乘'''


# def factorial():
#     x = 1
#     for i in range(1,10):
#         # x = 1
#         x *= i
#     print('阶乘为：',x)
#     return x
# print(factorial())



def factorial(i):
    if i == 1:
        return 1
    else:
        return i * factorial(i-1)


print(factorial(11))