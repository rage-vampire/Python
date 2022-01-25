#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : WuMingFen.py
# @Author: Lizi
# @Date  : 2020/11/16

class WuMingFen():
    def __init__(self, theMa, qauntity, likeSoup=True):
        self.theMa = theMa
        self.quantity = qauntity
        self.likeSoup = likeSoup

    def check_info(self):
        print('面的种类为：{}，面分分量：{}两，是否带汤：{}'.format(self.theMa, self.quantity, self.likeSoup))

suan_la_fen = WuMingFen('细粉', 3, False)
suan_la_fen.check_info()