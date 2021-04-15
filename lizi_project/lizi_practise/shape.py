#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : shape.py
# @Author: Lizi
# @Date  : 2020/9/21

from abc import abstractmethod
from math import pi
import sys


class Shape():
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def area(self):
        pass


class Square(Shape):
    def __init__(self, width, hight):
        super().__init__(name='正方形')
        self.width = width
        self.hight = hight

    def area(self):
        return self.width * self.hight


class Circle(Shape):
    def __init__(self, r):
        super().__init__(name='圆形')
        self.r = r * r

    def area(self):
        return pi * self.r


class Triangle(Shape):
    def __init__(self, width, hight):
        super().__init__(name='三角形')
        self.width = width
        self.hight = hight

    def area(self):
        return (self.width * self.hight) / 2


if __name__ == '__main__':
    # square = Square(2,3)
    # print('正方形的面积为：', square.area())
    # circle = Circle(3)
    # print('圆的面积为：', circle.area())
    # triangle = Triangle(3,4)
    # print("三角形的面积为：", triangle.area())

    list_shape = [Square(2, 3), Circle(3), Triangle(3, 4)]
    sum = 0
    for item in list_shape:
        sum += item.area()
        print('{}的面积为：'.format(item.name), item.area())
    print(sum)


# aa = [Square(), Circle(), Triangle()]
    # bb = {'square':Square(),'circle':Circle(),'triangle':Triangle()}
    # class_shape = []
    # sum = 0
    # for item in bb.keys():
    #     item = item.val
    #     print(item.area())
