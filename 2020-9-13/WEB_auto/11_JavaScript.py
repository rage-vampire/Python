#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 11_JavaScript.py
# @Author: Lizi
# @Date  : 2020/11/28

from selenium import webdriver

# driver = webdriver.Chrome()
# driver.get('https://www.baidu.com')

"""
    windows对象
"""
# # 打开一个新窗口
# js = 'window.open("https://www.baidu.com")'
#
# # selenium执行js语句
# driver.execute_script(js)
#
# # window.innerHeight:获取内部高度
# innerheight = driver.execute_script('return window.innerHeight')
#
# # window.innerWidht:获取内部宽度
# innerwidht = driver.execute_script('return window,innerWidth')
#
# # window.outerHeight:获取外部高度
# outerheight = driver.execute_script('return window.outerHeight')
#
# # window.outerHeight:获取外部宽度
# outerwidht = driver.execute_script('return window,outerrWidth')
#
# # window.close():关闭当前窗口
# driver.execute_script('window.close()')


# --------------------------------------------------------------------------------------------------------------------
"""
    Location对象
"""
driver = webdriver.Chrome()

js = 'window.open("https://www.baidu.com")'
driver.execute_script(js)

# location.href:获取当前的URL
all_handles = driver.window_handles
driver.switch_to.window(all_handles[-1])
url = driver.execute_script('return location.href')
print(url)

