#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : soider.py
# @Author: Lizi
# @Date  : 2020/11/16

'''
    需求：
    1、士兵瑞恩有一把AK47
    2、士兵可以扣动扳机，开火
    3、枪能够发射子弹（把子弹发射出去）
    4、枪能装子弹，每装一颗，增加一颗
'''

class Soidler():
    def __init__(self, name, gun_obj=None):
        self.name = name
        self.gun_obj = gun_obj

    def shoot(self):
        print('士兵{}扣动扳机，准备发射！'.format(self.name))
        self.gun_obj.shoot_bultt()


class Gun():
    def __init__(self,name, bultt, max_bultt=20):
        self.name = name
        self.bultt = bultt
        self.max_bultt = max_bultt

    def shoot_bultt(self):
        if self.bultt == 0 :
            print('检查没有子弹，请装填子弹')

        else:
            self.bultt -= 1
            print('发射子弹成功，biubiu~~~')


    def load_bultt(self):
        if self.bultt < self.max_bultt:
            self.bultt += 1


if __name__ == '__main__':
    AK47 = Gun('AK47', 10)
    ruien = Soidler('Ruien',AK47)
    for i in range(15):
        ruien.shoot()

