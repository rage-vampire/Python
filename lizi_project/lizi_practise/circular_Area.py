#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : circular_Area.py
# @Author: Lizi
# @Date  : 2020/9/8

import math

def findarea(r):
    if r > 0:
        arr = math.pi * (r**2)
        print("圆的面积为：{:.6f}".format(arr))
    else:
        print('r必须大于0')

def grith(r):
    if r > 0:
        cir = (2*r) * math.pi
        print('圆的周长为：{}'.format(cir))
    else:
        print('r必须大于0')


if __name__ == "__main__":
    r = int(input("请输入圆的半径r: "))
    findarea(r)
    grith(r)