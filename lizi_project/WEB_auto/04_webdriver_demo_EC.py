#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 04_webdriver_demo_EC.py
# @Author: Lizi
# @Date  : 2020/11/25

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


"""
    expected_conditions是Selenium的一个模块，主要用于对页面元素的加载进行判断，包括元素是否存在，可点击等等。
    两种使用场景：
        1、直接在断言中使用
        2、与WebDriverWait配合使用，显示等待页面上元素出现或者消失。
    EC模块单独使用语法：
        EC.方法(参数)(driver)
        EC.方法(参数).__call__(driver)
"""

driver = webdriver.Chrome()
driver.get('https://www.baidu.com')

# title_is()判断网页title是否是特定文本（英文区分大小写），若完全相同则返回True，否则返回False
title = EC.title_is('百度一下，你就知道')(driver)
print(title)

# title_contains(title)判断网页title是否包含特定文本（英文区分大小写），若包含则返回True，不包含返回False。
title_con = EC.title_contains('百度一下')(driver)
print(title_con)


"""
presence_of_element_located(locator)（常用）:判断一个元素存在于页面DOM树中，存在则返回元素本身，不存在则报错。
    参数locator：定位器是一个数据类型元组
    ("元素定位方式","方式对应的值")
    ("id","id属性值") 或者（By.ID,'id属性值'）
    
"""
baidu_btn = ('id', 'su')
presence = EC.presence_of_element_located(baidu_btn)(driver)
print(presence)



"""
presence_of_all_elements_located(locator)判断定位的元素范围内，至少有一个元素存在于页面当中，存在则以list形式返回元素本身，不存在则报错。
"""
presence_list = EC.presence_of_all_elements_located((By.TAG_NAME, 'input'))(driver)
print(presence_list)

