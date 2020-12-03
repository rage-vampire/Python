#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : login.py
# @Author: Lizi
# @Date  : 2020/11/27

from selenium import webdriver


class Location:

    def iframe(self, driver):
        self.frame_ele = driver.find_elements_by_tag_name('iframe')[0]
        # switch_to.frame(frame_ele)切换到frame框架中
        driver.switch_to.frame(self.frame_ele)

    def login(self, driver, username, pwd):
        # 先定位到frame元素
        # self.frame_ele = driver.find_elements_by_tag_name('iframe')[0]
        # # switch_to.frame(frame_ele)切换到frame框架中
        # driver.switch_to.frame(self.frame_ele)
        driver.find_element_by_name('email').send_keys(username)
        driver.find_element_by_name('password').send_keys(pwd)
        driver.find_element_by_xpath('//*[@id="dologin"]').click()

# def login(driver, username, pwd):
#     # 先定位到frame元素
#     frame_ele = driver.find_elements_by_tag_name('iframe')[0]
#     # switch_to.frame(frame_ele)切换到frame框架中
#     driver.switch_to.frame(frame_ele)
#     driver.find_element_by_name('email').send_keys(username)
#     driver.find_element_by_name('password').send_keys(pwd)
#     driver.find_element_by_xpath('//*[@id="dologin"]').click()
