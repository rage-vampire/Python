#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : game_funcation.py
# @Author: Lizi
# @Date  : 2021/3/26


import sys
import pygame


def check_keydown_events(ship, event):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True


def check_keyup_events(ship, event):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def event_checks(ship):             # ship为实例化对象，也可作为参数传入，可在后面的方法体中直接调用其中的属性和方法
    """响应键盘和鼠标事件"""

    for event in pygame.event.get():  # 遍历所有的事件
        if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(ship, event)

        elif event.type == pygame.KEYUP:
            check_keyup_events(ship, event)


def update_screen(ai_settings, screen, ship):
    """更新屏幕上的图像，并更新到新的屏幕"""
    # 每次循环都重新绘制屏幕
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    # 让最近绘制的屏幕可见
    pygame.display.flip()
