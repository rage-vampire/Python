#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : EC+webdriverwait.py
# @Author: Lizi
# @Date  : 2020/11/25

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get('https://www.baidu.com')

baidu_input = (By.ID, 'kw')
ele1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(baidu_input))
ele1.send_keys('华测教育')


baidu_btn = ('id', 'su')
ele2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(baidu_btn))
ele2.click()

res_link = (By.XPATH,'/html/body/div[1]/div[3]/div[1]/div[3]/div[1]/h3/a')  #元素属性和定位
#等待第一个搜索结果元素是否存在
ele3=WebDriverWait(driver, 10).until(EC.presence_of_element_located(res_link)) #如果结合unitl方法使用，EC调用类后不需要（driver）
# 点击第一个搜索结果
ele3.click()
time.sleep(2)
driver.quit()


