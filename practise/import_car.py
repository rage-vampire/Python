# -*- coding:utf-8 -*-
# Filename: import_car.py
# Author: Lizi
# Time: 2019/12/21 16:07

from random import randint
x = randint(1,10)
y = randint(1,20)
class Die():
    def __init__(self):
        self.side = 6

    def roll_diex(self):
        print(x)

    def roll_diey(self):
        print(y)

point = Die()
# print(point)
point.roll_diex()
point.roll_diey()