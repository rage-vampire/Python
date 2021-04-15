#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : ship.py
# @Author: Lizi
# @Date  : 2021/3/26

import pygame


class Ship:
    """管理飞船的行为"""

    def __init__(self, screen, ai_settings):            # ai_settings为实例化对象，也可作为参数传入，可在后面的方法体中直接调用其中的属性和方法
        """初始化飞船，并设置其初始位置"""
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load("images/ship.bmp")          # 加载飞船图像
        self.rect = self.image.get_rect()                          # 获取飞船外接矩形
        self.screen_rect = screen.get_rect()                       # 获取飞船位置的外接矩形

        self.rect.centerx = self.screen_rect.centerx               # 将每艘新飞船放在屏幕底部中央
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)                     # 在飞船的属性center中存储小数值

        self.moving_right = False                                  # 移动标志
        self.moving_left = False

    def update_position(self):
        """根据移动标志调整飞船的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:     # 控制飞船向右移动的范围
            self.center += self.ai_settings.ship_speed_factor             # 更新飞船的center值，而不是rect
        if self.moving_left and self.rect.left > 0:                      # 控制飞船向左移动的范围
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center                                  # 根据self.center更新rect对象

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)                    # 根据self.rect 指定的位置将图像绘制到屏幕上


