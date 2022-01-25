#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : house.py
# @Author: Lizi
# @Date  : 2020/11/16

'''
    需求：
    1、房子有户型、总面积、家具名称列表
    新房子没有任何家具
    2、家具有名称和占地面积，其中：
        床：占4平米
        桌子：占地1.5平米
        衣柜：占地2平米
    3、将以上三种家具添加到房子中
    4、打印房子时要求输出户型、总面积、剩余面积、家具名称列表
'''


class House:
    def __init__(self, hu_xing, all_area):
        self.hu_xing = hu_xing
        self.all_area = all_area
        self.free_area = all_area
        self.furniture_list = []

    def add_furn(self, furniture_obj):    # 将实例化对象作为参数传给函数
        if furniture_obj.area < self.free_area:
            self.free_area -=furniture_obj.area
            self.furniture_list.append(furniture_obj.name)
            print('{}能放下'.format(furniture_obj.name))
        else:
            print('{}放不下'.format(furniture_obj.name))

    def house_info(self):
        print('房子户型：{}，房子总面积；{}，剩余面积；{}，家具名称：{}'.format(self.hu_xing, self.all_area, self.free_area, self.furniture_list))


class Furniture:
    def __init__(self, name, area):
        self.name = name
        self.area = area

    def info(self):
        print("家具的名称：{}".format(self.name))


house = House('三居室', 120)
bed = Furniture('床', 5)
desk = Furniture('桌子', 2)
house.add_furn(bed)
house.add_furn(desk)
house.house_info()