#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : WebDriverWait_demo.py
# @Author: Lizi
# @Date  : 2020/11/20

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

driver = webdriver.Chrome()
driver.get('https://www.baidu.com')
driver.find_element(by=By.ID, value='kw').send_keys('华测教育')
driver.find_element_by_id('su').click()

"""
    对WebDriverWait类进行实例对象操作
    WebDriverWait(driver, timeout, poll_frequency=0.5, ignored_exceptions=None)
        driver: 浏览器驱动
        timeout：最大等待时间
        poll_frequency：检测的时间间隔，默认0.5s
        signored_exceptions：超时后的异常信息，默认抛出NoSuchElementException        
"""
# 定位到第一个查询结果的元素
xpath = '/html/body/div[1]/div[3]/div[1]/div[3]/div[1]/h3/a'

# 使用显示等待
# # 方式一：实例化WebDriverWait，再调用用unit()方法等待
# wait = WebDriverWait(driver, 10, poll_frequency=0.5)
# 判断某个元素是否在页面上，结果为True则结束等待，否则继续等待，直至超时抛出TimeoutException异常
# wait.until(lambda x:  x.find_element_by_xpath(xpath), message='元素没有找到')

# # 方式二：一起写，实例化对象后面直接调用until方法
# WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath(xpath), message='元素没有找到')


# # 方式三：在lambda表达式中判断元素是否显示，使用is_displayed()
# WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath(xpath).is_displayed())

# 方式四：lambda表达式中判断元素组定位此元素的返回列表的长度是否为1；长度=1，则表示元素存在，长度=0,则表示元素不存在
WebDriverWait(driver, 10).until(lambda x: len(x.find_elements_by_xpath(xpath)) == 1)

driver.find_element_by_xpath(xpath).click()

"""
    ele.is_displayed()：判断某个元素是否显示页面上
    ele.is_selected()：判断某个元素是否被选中
    ele.is_enables()：判断某个元素是否可以操作，如判断input、select等元素的可编辑状态，如按钮是否可以点击  
"""
# ele = driver.find_element_by_xpath(xpath).is_displayed()
# ele = driver.find_element_by_xpath(xpath).is_enabled()
# ele = driver.find_element_by_xpath(xpath).is_selected()
# print(ele)



time.sleep(2)
driver.quit()



