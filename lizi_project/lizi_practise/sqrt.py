#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : sqrt.py
# @Author: Lizi
# @Date  : 2020/9/8
import math
import cmath

'''输入一个数，计算它的平方'''

# def sqrt(n):
#     try:
#         print(math.sqrt(n))
#     except ValueError:
#         print("被开方数必须大于0")

list1 = []
def sqrt1(a,b,c):
    z =((b**2) - (4*a*c))
    if z > 0:
        x = (-b + math.sqrt(z)) / 2*a
        y = (-b - math.sqrt(z)) / 2*a
        print('第一个实数解为：{:.5f}'.format(x))
        print('第二个实数解为：{}'.format(y))
        print('deta值为：{}'.format(z))
        return x,y
    elif z == 0:
        x = (-b + math.sqrt(z)) / 2 * a
        print(x,z)
        return x,z
    else:
        print('次方程无实数解')


if __name__ == '__main__':
    a = int(input("请输入一个数a："))
    b = int(input("请输入一个数b："))
    c = int(input("请输入一个数c："))
    # sqrt(n)
    # sqrt1(a,b,c)
    print(sqrt1(a,b,c))