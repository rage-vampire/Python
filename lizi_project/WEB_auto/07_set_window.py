#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 07_set_window.py
# @Author: Lizi
# @Date  : 2020/11/26

from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.baidu.com')


# 设置指定大小的窗口
driver.set_window_size(900, 450)

# 最大化窗口
driver.maximize_window()

# 最小化窗口
driver.minimize_window()