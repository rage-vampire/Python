#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 02_webdriver_method.py
# @Author: Lizi
# @Date  : 2020/11/19

from selenium import webdriver


# 打开浏览器
driver = webdriver.Chrome()

# 打开网址
driver.get('https://www.baidu.com')
driver.get('https://www.jd.com')

# 回退
driver.back()

# 前进
driver.forward()

# 刷新
driver.refresh()

# 截屏
driver.get_screenshot_as_file('pic.png')

# 关闭浏览器，不会终止进程
driver.close()

# 退出，直接终止进程
driver.quit()