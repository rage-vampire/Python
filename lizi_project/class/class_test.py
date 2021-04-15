#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : class_test.py
# @Author: Lizi
# @Date  : 2020/11/12

''''''
'''
    实例方法：可通过实例对象调用。
    类方法：可通过类对象和实例对象调用，cls表示类本身
    静态方法：可通过类对象和实例对象调用，不需要参数self
        在实例方法中能访问静态方法和类方法，但是在静态方法和类方法中不能访问实例方法
    '''


class Myclass:
    name = 'Bill'

    def __init__(self):
        print("Myclassde构造方法被调用")
        self.value = 20

    def do_1(self):
        print('实例方法内访问实例属性:', self.value)
        print('实例方法内访问类属性:', self.name)
        print('实例本身:', self)
        print('在实例方法中调用静态方法：', self.run())

    @staticmethod
    def run():
        # 访问类属性
        print('静态方法中访问类属性:', Myclass.name)
        print('Myclass的静态方法被调用')


    @classmethod
    def do(cls):
        print(cls)
        print('类方法中访问Myclass类中的类属性:', cls.name)
        print('类方法中调用静态方法run:', cls.run())
        print('类方法do被调用')




c = Myclass()

# 通过类对象调用静态方法
Myclass.run()

# 通过类对象调用静态方法
# c.run()
#
# # 通过类对象调用类方法
# Myclass.do()
#
# # 通过实例对象也能调用类方法
# c.do()
#
# c.do_1()



