#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : home_page.py
# @Author: Lizi
# @Date  : 2020/11/30
from selenium.webdriver.common.by import By
from selenium import webdriver
from POM.init_browser import Browser

class HomePage(Browser):
    '''
    进入网页需要定位的元素
    '''
    search_input = (By.ID, 'kw')
    search_button = (By.ID, 'su')

    # def __init__(self, driver):
    #     '''__init__需要什么参数，实例化对象时就必须传什么参数'''
    #     self.driver = driver

    def searchInput(self, value):
        '''
        搜索框输入方法
        '''
        # self.driver.find_element(*HomePage.search_input).send_keys(value)
        self.send_keys_my(HomePage.search_input, value)

    def click_button_search(self):
        '''
        搜索之后点击方法
        '''
        # self.driver.find_element(*HomePage.search_button).click()
        self.click_my(HomePage.search_input)


    def baidu_home_page_search(self,val):
        '''
        首页搜索框
        '''
        self.searchInput(value=val)




