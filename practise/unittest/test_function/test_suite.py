# -*- coding:utf-8 -*-
# @Filename : test_suite.py 
# @Author : Lizi
# @Time : 2020/4/11 11:55 
# @Software: PyCharm

import unittest
from unittest import TestLoader
import test_function_demo
from test_function_demo import Test_function_demo
from BeautifulReport import BeautifulReport
import HTMLTestRunner

if __name__ == '__main__':
    # 创建测试用例集
    suites = unittest.TestSuite()
    # test = [Test_function_demo('setUp'),Test_function_demo('tearDown'),Test_function_demo('test_add_int'),
    #         Test_function_demo('test_sub_int'),Test_function_demo('test_sub_float'),
    #         Test_function_demo('test_sub_float2'),Test_function_demo('test_multi_list'),
    #         Test_function_demo('test_multi_str'),Test_function_demo('test_div_int'),
    #         Test_function_demo('test_div_float'),Test_function_demo('test_div_float2'),
    #         Test_function_demo('test_div_exception')]
    # 运行类里面的所有用例
    test = unittest.TestLoader().loadTestsFromTestCase(testCaseClass=Test_function_demo)
    #
    # 运行模块里的所有用例
    # test = unittest.TestLoader().loadTestsFromModule(module=test_function_demo)
    #
    # 运行单个测试用例
    # test = unittest.TestLoader().loadTestsFromName
    # (name='Test_function_demo.test_multi_list', module=test_function_demo)

    # 运行多个测试用例
    #  test = unittest.TestLoader().loadTestsFromNames(names=['Test_function_demo.test_multi_list',
    #                                                        'Test_function_demo.test_div_exception'],
    #                                                 module=test_function_demo)

    # 将测试用例添加到测试用例集
    suites.addTests(test)
    print(unittest.TestLoader().getTestCaseNames(testCaseClass=Test_function_demo))


    # 生成本地文件测试报告
    # with open('function_test.txt', 'a') as file:
    #     # 创建一个运行器，运行测试用例集，并输出测试报告
    #     runner = unittest.TextTestRunner(stream=file, descriptions='测试报告', verbosity=2)
    #     runner.run(suites)


    # 生成HTML测试报告
    # with open("function_test.html", 'w', encoding='utf-8') as file:
    #     runner = HTMLTestRunner.HTMLTestRunner(stream=file, title='测试报告',  description='这是第一次执行用例的测试报告！', verbosity=2)
    #     runner.run(suites)

    result = BeautifulReport(suites)
    result.report(filename="测试报告.excel", description="函数测试报告", report_dir='./', theme='theme_cyan')
