# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/4/24
# @Software: PyCharm


from testcase.ws_testcase.pc_subscribe_testcase import SubscribeTestCases, unittest
import BeautifulReport as bf
from test_config import *
import time
from datetime import datetime

if __name__ == '__main__':
    startTime = datetime.now()
    runner = bf.BeautifulReport(unittest.makeSuite(SubscribeTestCases))
    now_time_stamp = int(time.time() * 1000) # 毫秒级
    filename = report_folder + 'SubscribeTestCases_BeautifulReport_' + str(now_time_stamp) + '.html'
    runner.report(description='订阅服务WebSocketApi测试', filename=filename)
    endTime = datetime.now()
    print(u'测试结束!\n开始于%s,结束于%s，测试共耗时：%s' % (startTime, endTime, (endTime - startTime)))
