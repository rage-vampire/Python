#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 06_browse_mode.py
# @Author: Lizi
# @Date  : 2020/11/25

from selenium import webdriver

opt = webdriver.ChromeOptions()

# # 方式一：调用set_headless()
# opt.set_headless()

# # 方式二: 设置headless属性值
# opt.headless = True

# 方法三：opt.add_argument(argument='head') #headless:无头  head :有头
opt.add_argument(argument='headless')

driver = webdriver.Chrome(options=opt)
driver.get('https://www.baidu.com')

if driver.title == '百度一下，你就知道':
    print('打开浏览器成功')
else:
    print('打开浏览器失败')

driver.quit()



