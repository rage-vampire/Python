#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : bullet.py
# @Author: Lizi
# @Date  : 2021/3/26

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理飞船发射子弹"""
    def __init__(self, ai_setting, screen, ship):
        """在飞船所处的位置创建一个子弹对象"""
        super(Bullet, self).__init__()
        self.screen = screen

        # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_setting.bullet_width, ai_setting.bullet_heigth)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

