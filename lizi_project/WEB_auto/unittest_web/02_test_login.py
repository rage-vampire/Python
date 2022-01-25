#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 02_test_login.py
# @Author: Lizi
# @Date  : 2020/11/27

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from login import Location
import unittest
import time


class Login_Test(unittest.TestCase):
    driver = None   # 也可在下面使用全局变量

    @classmethod
    def setUpClass(cls):
        # global driver
        cls.driver = webdriver.Chrome()


    @classmethod
    def tearDownClass(cls):
        print('回收资源，关闭浏览器')
        cls.driver.quit()

    def setUp(self):
        print("初始化环境，打开浏览器")
        self.driver.get('http://mial.163.com/')
        time.sleep(3)

    def tearDown(self):
        time.sleep(5)

    def test_case01(self):
        print("测试用例test_case01")
        Location().iframe(self.driver)
        Location().login(self.driver, 'rage_vampire0626', '06yangLL26')
        # time.sleep(5)
        xpath = '//*[@id="spnUid"]'
        WebDriverWait(self.driver, 10).until(lambda x: len(x.find_elements_by_xpath(xpath)) == 1)
        self.assertEqual(self.driver.find_element_by_id("spnUid").text, 'rage_vampire0626@163.com')

    # def test_case02(self):
    #     print("测试用例test_case02")
    #     Location().iframe(self.driver)
    #     Location().login(self.driver, 'rage_vampire0626', '123456')
    #     # time.sleep(5)
    #     # Location().iframe(self.driver)
    #     xpath = '//*[@id="nerror"]'
    #     WebDriverWait(self.driver, 20).until(lambda x: len(x.find_elements_by_xpath(xpath)) == 1)
    #     print("1111",self.driver.find_element_by_xpath(xpath).text)
    #     self.assertEqual(self.driver.find_element_by_xpath(xpath).text, '帐号或密码错误')


if __name__ == '__main__':
    unittest.main()
