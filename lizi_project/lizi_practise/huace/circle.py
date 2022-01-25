#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : circle.py
# @Author: Lizi
# @Date  : 2020/11/16

import math

'''定义一“圆”Cirlcle类，圆心为“点”Point类，构造一圆，求圆的周长和面积，并判断某点与圆的关系。'''
class Circle:
    def __init__(self, R):
        self.r = R

    def area(self):
        return math.pi * (self.r ** 2)


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def check(self, circle_obj):
        res = self.x ** 2 + self.y ** 2
        if math.sqrt(res) == circle_obj.r:
            print('点在圆上')
        elif math.sqrt(res) > circle_obj.r:
            print('点在圆外')
        elif math.sqrt(res) < circle_obj.r:
            print('点在圆内')
        print(math.sqrt(res))


circle = Circle(5)

p1 = Point(1, 2)
p2 = Point(3, 4)

p1.check(circle)
p2.check(circle)

area = circle.area()
print('圆的半径为：{},圆的面积为：{:.3f}'.format(circle.r, area))
