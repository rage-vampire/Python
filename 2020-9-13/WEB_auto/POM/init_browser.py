#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : init_browser.py
# @Author: Lizi
# @Date  : 2020/11/30

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging

'''
    创建一个浏览器的类，添加点击、输入、等待时间、日志、截图、切换frame等方法
'''


class Browser:

    def __init__(self, driver):
        self.driver = driver

    def click_my(self, loc):
        '''
        点击方法
        '''
        ele = self.wait_until_element_visible(loc)
        # self.driver.find_element().click()
        ele.click()

    def send_keys_my(self, loc, value):
        '''
        输入方法
        '''
        ele = self.wait_until_element_visible(loc)
        ele.send_keys(value)

    def wait_until_element_visible(self, loc):
        '''
        等待时间
        return:返回元素对象，webelement
        '''
        ele = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
        return ele

    def wait_until_elements_count(self, loc):
        '''
        等待时间
        return:返回元素对象列表，webelement
        '''
        ele = len(WebDriverWait(self.driver, 10).until(lambda x: x.find_elements(*loc)))
        return ele



