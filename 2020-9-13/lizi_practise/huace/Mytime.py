#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Mytime.py
# @Author: Lizi
# @Date  : 2020/11/16

import time


class Mytime:
    def __init__(self, hour, minute, second):
        self.__hour = hour
        self.__minute = minute
        self.__second = second

    def set_hour(self, hour):
        if self.__hour != hour:
            self.__hour = hour
            print('时间更新成功！')
        else:
            print('时间未更新！')

    def get_hour(self):
        print(self.__hour)
        return self.__hour

# t1 = time.localtime()
if __name__ == '__main__':

    my_time = Mytime(10, 56, 34)
    my_time.get_hour()


    my_time.set_hour(55)
    my_time.get_hour()
