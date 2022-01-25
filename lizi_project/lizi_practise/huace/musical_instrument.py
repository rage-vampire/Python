#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : musical_instrument.py
# @Author: Lizi
# @Date  : 2020/11/16

'''三、编写程序实现乐手弹奏乐器。乐手可以弹奏不同的乐器从而发出不同的声音。可以弹奏的乐器包括二胡、钢琴和琵琶。
    实现思路及关键代码：
    1)定义乐器类Instrument，包括makeSound()
    方法，此方法中乐器声音："乐器发出美妙的声音！"
    2)定义乐器类的子类：二胡Erhu、钢琴Piano和小提琴Violin
    二胡Erhu声音："二胡拉响人生"
    钢琴Piano声音："钢琴美妙无比"
    小提琴Violin声音："小提琴来啦"
    3）用main类，多态的方式对不同乐器进行切换
'''


class Musical_instrument:
    def __init__(self, name):
        self.name = name

    def instrument_sound(self, obj):
        print("乐器发出美妙的声音！！！")
        obj.make_sound()


class Erhu(Musical_instrument):
    def __init__(self):
        super().__init__(name='二胡')
        # self.name = name

    def make_sound(self):
        print("{}拉响人生".format(self.name))


class Piano(Musical_instrument):
    def __init__(self):
        super().__init__(name='钢琴')

    def make_sound(self):
        print("{}美妙无比".format(self.name))


class Pipa(Musical_instrument):
    def __init__(self):
        super().__init__(name='琵琶')

    def make_sound(self):
        print("{}来啦".format(self.name))


# erhu = Erhu()
# piano = Piano()
# erhu.instrument_sound(erhu)
# piano.instrument_sound(piano)
if __name__ == '__main__':
    instrumnet_list = [Erhu(), Piano(), Pipa()]
    for instrument in instrumnet_list:
        instrument.instrument_sound(instrument)
