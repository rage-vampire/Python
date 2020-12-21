#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : HttpTestCase.py
# @Author: Lizi
# @Date  : 2020/12/18

import unittest
import json
from requests_test.HttpRequests import HttpClientRequest
from modules.log.log_demo import logger
from BeautifulReport import BeautifulReport


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.request = HttpClientRequest()

    @classmethod
    def tearDownClass(self) -> None:
        pass

    def testcase_page(self):
        test_data = {"limit": 1}
        res = self.request.send_request('get', 'demo', json=test_data)
        # json_res = json.dumps(res, indent=4)
        self.assertEqual(res['httpstatus'], 200)
        self.assertEqual(len(res['data']), 3)
        # print("首页数据：", res)
        logger.debug(f"首页数据：{res}")

    def testcase_login(self):
        test_data = {"username": "admin", "password": "123456"}
        res = self.request.send_request(method='post', api_url='login', json=test_data, params='token')
        self.assertEqual(res['httpstatus'], 200)
        self.assertEqual(res['msg'], 'success')
        self.assertEqual(res['token'], "huacetest")
        # print("登陆响应数据：", res)
        logger.debug(f"登陆响应数据：{res}")

    def testcase_user_list(self):
        res = self.request.send_request(method='get', api_url='userList')
        # print('用户列表', res)
        logger.debug(f"用户列表：{res}")

    def testcase_vip_list(self):
        res = self.request.send_request(method='get', api_url='userViplist')
        # print("VIP用户列表", res)
        logger.debug(f"VIP用户列表：{res}")

    def testcase_user_info(self):
        head = {'Content-Type': "application/x-www-form-urlencoded"}
        test_data = {"userid": "admin"}
        self.request.init_headers(head)
        res = self.request.send_request(method='post', api_url='userInfo', data=test_data)
        # print("用户信息列表", res)
        logger.debug(f"用户信息列表：{res}")

    def testcase_auth(self):
        head = {'Authorization': 'Basic YWRtaW46aHVhY2UxMjM0NTY='}
        self.request.init_headers(head)
        res = self.request.send_request(method='post', api_url='auth')
        # print("auth鉴权信息", res)
        logger.debug(f"auth鉴权信息：{res}")


if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestSuite()
    # test = unittest.TestLoader().loadTestsFromModule(module=TestCase)
    # suite.addTests(test)
    # with open('./test_report', 'w') as file:
    #     runner = unittest.TextTestRunner(stream=file, descriptions=True, verbosity=2)
    #     runner.run(suite)


