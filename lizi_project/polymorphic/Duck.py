#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Duck.py
# @Author: Lizi
# @Date  : 2020/10/29

import abc
from abc import ABC


class Animal:

    def __init__(self, kind):
        self.kind = kind
        # self.name = name

    @abc.abstractmethod
    def shout(self):
        pass


class Swim:
    def __init__(self, name):
        self.name = name

    def swim(self):
        print('{}会游泳'.format(self.name))

    def cannot_swim(self):
        print('{}不会游泳'.format(self.name))


class Dog(Animal, Swim):
    def __init__(self):
        super().__init__(kind='dog')
        # super().__init__(name='111')

    def shout(self):
        print('狗是吠吠叫！！！')


class Cats(Animal):
    def __init__(self):
        super().__init__(kind='cat')

    def shout(self):
        print("猫是喵喵叫！！！")


if __name__ == '__main__':
    dog = Dog()
    # dog.shout()
    dog.swim()

    # cat = Cats()
    # cat.shout()
