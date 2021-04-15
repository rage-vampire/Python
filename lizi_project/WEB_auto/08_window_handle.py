#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 08_window_handle.py
# @Author: Lizi
# @Date  : 2020/11/26

import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://www.baidu.com')
# driver.get('https://tmall.com')

# 获取当前句柄
baidu_handle = driver.current_window_handle
print("当前句柄：{}".format(baidu_handle))

time.sleep(2)
# 点击新闻
driver.find_element_by_link_text('新闻').click()
new_handle = driver.current_window_handle
print("新闻页句柄：{}".format(new_handle))

# 获取所有的句柄
all_handle = driver.window_handles
print("所有句柄{}".format(all_handle))

time.sleep(3)
# 切换句柄
driver.switch_to.window(all_handle[1])
driver.find_element_by_link_text('国内').click()
if EC.title_contains('百度新闻')(driver):
    print("页面切换成功")
else:
    print("页面切换失败")
driver.close()
driver.switch_to.window(all_handle[0])
if driver.title == "百度一下，你就知道":
    print("切换到首页成功")
else:
    print("切换到首页失败")

# ----------------------------------------------------------------------------------------------------------------------


