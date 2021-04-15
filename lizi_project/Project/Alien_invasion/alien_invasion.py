#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alien_invasion.py
# @Author: Lizi
# @Date  : 2021/3/26


import pygame
from setting import Settings
from ship import Ship
import game_funcation as gf


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_heigth))
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(screen, ai_settings)                     # 创建一艘飞船

    while True:              # 开始游戏的主循环
        gf.event_checks(ship)
        ship.update_position()
        gf.update_screen(ai_settings, screen, ship)


if __name__ == '__main__':
    run_game()