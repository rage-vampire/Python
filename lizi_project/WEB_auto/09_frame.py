#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 09_frame.py
# @Author: Lizi
# @Date  : 2020/11/26

from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get('http://mial.163.com/')

# 先定位到frame元素
frame_ele = driver.find_elements_by_tag_name('iframe')[0]

# switch_to.frame(frame_ele)切换到frame框架中
driver.switch_to.frame(frame_ele)

driver.find_element_by_name('email').send_keys('rage_vampire0626')
driver.find_element_by_name('password').send_keys('123456')
driver.find_element_by_xpath('//*[@id="dologin"]').click()

time.sleep(3)
# switch_to.default_content()退出frame框架
driver.switch_to.default_content()
driver.find_element_by_partial_link_text('企业邮箱').click()
