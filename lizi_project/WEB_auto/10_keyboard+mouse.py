#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 10_keyboard+mouse.py
# @Author: Lizi
# @Date  : 2020/11/27

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('https://baidu.com')

ele = driver.find_element_by_id('kw').send_keys("selenium")

# send_keys(Keys.BACK_SPACE)：删除一个字符
ele.send_keys(Keys.BACK_SPACE)



action = ActionChains(driver)
# 鼠标左键单击
action.click(ele).perform()

# 鼠标右键单击
action.context_click(ele).perform()

# 鼠标左键双击
action.double_click(ele).perform()

# 拖到某个元素后放开
action.drag_and_drop(source=None, target=None).perform()

# 鼠标悬停在一个元素上
action.move_to_element(to_element=ele).perform()

# 鼠标左键单击，不松开
action.click_and_hold(ele).perform()

# 在某个元素上松开鼠标左键
action.release(ele).perform()

# 执行鼠标操作
action.perform()