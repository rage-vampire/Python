#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : testcase.py
# @Author: Lizi
# @Date  : 2020/11/30

from selenium import webdriver
import unittest
from POM.home_page import HomePage
from POM.init_browser import Browser
from modules.log.log_demo import Log


class TestCase(unittest.TestCase, HomePage, Browser):

    def setUp(self) -> None:
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.baidu.com')
        # self.home_page = HomePage(driver=self.driver)
        self.browser = Browser(driver=self.driver)
        # self.log = Log('yll', 'file')
        # self.logger = self.log.get_log()

    def tearDown(self) -> None:
        import time
        time.sleep(5)
        self.driver.close()

    def test_search_01(self):
        # self.driver.find_element(*HomePage.search_input).send_keys('python')
        # self.driver.find_element(*HomePage.search_button).click()
        '''
            优化：
                1、把元素定位抽离出来
                2、把元素的定位方式抽离出来，由原来的find_element_by_id编程find_element（By.id,'xxx'）
                3、把元素定位完全抽离出来，只关心这行代码做什么，而不是怎么做
                4、用例用到多个页面
                    a、浏览器对象和浏览器常用操作对象抽离出来
                    b、点击、输入之前自动加上等待时间；
                    c、加日志信息等
        '''
        # self.home_page.search_input('python')
        # self.home_page.click_button_search()
        self.searchInput('python')
        times = self.wait_until_elements_count(self.search_input)
        self.assertEqual(times, 1)
        self.click_button_search()
        # self.logger.debug(self.search_input)


if __name__ == '__main__':
    unittest.main()
