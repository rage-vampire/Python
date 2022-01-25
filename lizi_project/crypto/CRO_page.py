# -*- coding: utf-8 -*-
# @Date : 2021/12/18 14:08
# @File : CRO_page.py
# @Author : Lizi

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

driver = webdriver.Chrome()
driver.get("https://crypto.com/exchange/markets")     # 打开网址
driver.maximize_window()     # 最大化窗口
time.sleep(2)

"""进入CRO页面"""
cro_ccs = "#app > div.router-container > div > div:nth-child(4) > div.market-title-box.markets-container > div.e-tabs.groups > div > div > div:nth-child(6)"
wait = WebDriverWait(driver, 10)   # 显示等待：实例化WebDriverWait，再调用用unit()方法等待
wait.until(lambda x: x.find_element(by=By.CSS_SELECTOR, value=cro_ccs), message='Element not found')
driver.find_element(by=By.CSS_SELECTOR,value=cro_ccs).click()
time.sleep(2)

js = 'window.scrollTo(0,2700)'   # 向下滚动2700像素
driver.execute_script(js)
time.sleep(2)


"""进入XTZ/CRO的trade页面"""
xtz_ccs='#app > div.router-container > div > div:nth-child(4) > div.trade-list > table > tbody > tr:nth-child(37) > td:nth-child(7) > div > button'
wait = WebDriverWait(driver, 10)
wait.until(lambda x: x.find_element(by=By.CSS_SELECTOR, value=xtz_ccs), message='Element not found')
driver.find_element(by=By.CSS_SELECTOR,value=xtz_ccs).click()
time.sleep(5)
driver.quit()
