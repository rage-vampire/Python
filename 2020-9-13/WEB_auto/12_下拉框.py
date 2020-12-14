#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 12_下拉框.py
# @Author: Lizi
# @Date  : 2020/12/3

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time


'''
    下拉框定位：
        1、Select+Option
        2、ul+li
'''

# # Select+Option下拉框
driver = webdriver.Chrome()
driver.get('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc')
driver.maximize_window()

# # 先定位到下拉框元素
# ele = driver.find_element_by_class_name('select-small')
#
# # 再通过select_by_value定位到具体的值
# Select(ele).select_by_value('00002400')
#
# # 通过索引定位
# Select(ele).select_by_index(1)
#
# # 通过text值定位
# Select(ele).select_by_visible_text('06:00--12:00')


""" 
    定位ul+li的下拉框
        1、先定位到ul，赋值给一个变量
        2、再通过这个变量去找到li
"""

ul_ele = driver.find_element_by_class_name("header-menu")
ul_ele.find_element_by_css_selector('body > div.header > div > div.wrapper > div > div > ul > li:nth-child(1) > a').click()
