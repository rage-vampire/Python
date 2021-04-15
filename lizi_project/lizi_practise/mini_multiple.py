#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : mini_multiple.py
# @Author: Lizi
# @Date  : 2020/10/10

def mini_multiple(x, y):
    #  获取最大的数
    if x > y:
        greater = x
    else:
        greater = y

    while (True):
        if ((greater % x == 0) and (greater % y == 0)):
            lcm = greater
            break
        greater += 1

    return lcm

    # 获取用户输入


num1 = int(input("输入第一个数字: "))
num2 = int(input("输入第二个数字: "))

print(num1, "和", num2, "的最小公倍数为", mini_multiple(num1, num2))