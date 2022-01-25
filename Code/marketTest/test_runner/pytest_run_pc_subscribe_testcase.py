# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/4/26
# @Software: PyCharm

import pytest
import time
from datetime import datetime
from test_config import *
import os
import shutil


if __name__ == '__main__':
    startTime = datetime.now()
    now_time_stamp = int(time.time() * 1000)  # 毫秒级
    fail_rerun_time = 3
    pytest_html_filename = report_folder + 'SubscribeTestCases_PytestReport_' + str(now_time_stamp) + '.html'
    pytest_param_list = []
    pytest_param_list.append(SETUP_DIR + '/testcase/ws_testcase/pc_subscribe_testcase.py')  # 遍历的测试用例文件
    pytest_param_list.append('-v')  # 使得输出信息更详细
    pytest_param_list.append('-l')  # 在测试失败时会打印出局部变量名和他们的值以避免不必要的 print 语句
    pytest_param_list.append('--reruns=%d' % (fail_rerun_time))  # 失败case重跑次数
    pytest_param_list.append('-k=SubscribeTestCases')  # 跑订阅服务用例
    pytest_param_list.append('--html=%s' % (pytest_html_filename))  # 生成pytest原始html报告
    pytest_param_list.append('--alluredir=%s' % allure_result_folder)  # 生成allure报告的原始文件
    shutil.rmtree(allure_result_folder)  # 清掉上次测试的缓存文件
    os.mkdir(allure_result_folder)
    pytest.main(pytest_param_list)
    cmd = 'allure generate %s -o %s --clean' % (allure_result_folder, allure_report_folder)
    os.system(cmd)
    endTime = datetime.now()
    print(u'测试结束!\n开始于%s,结束于%s，测试共耗时：%s' % (startTime, endTime, (endTime - startTime)))
