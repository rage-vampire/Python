#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : setting.py
# @Author: Lizi
# @Date  : 2021/3/26


class Settings:
    def __init__(self):
        """初始化游戏的设置"""
        self.bg_color = (230, 230, 230)          # 屏幕的背景色
        self.screen_width, self.screen_heigth = 1200, 800      # 屏幕的尺寸
        self.ship_speed_factor = 1.5             # 飞船移动的速度

        # 子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.buttle_color = (60, 60, 60)

