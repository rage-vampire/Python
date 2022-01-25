# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/4/14
# @Software: PyCharm

import os
import sys

env = 'SIT'

"""Returns the base application path."""
if hasattr(sys, 'frozen'):
    # Handles PyInstaller
    SETUP_DIR = os.path.dirname(sys.executable)
else:
    SETUP_DIR = os.path.dirname(__file__)

if sys.platform == 'win32':
    txt_file_save_folder = SETUP_DIR + '\\zmq_py3\\zmq_save_files\\Txt\\'
    db_save_folder = SETUP_DIR + '\\zmq_py3\\zmq_save_files\\db\\'
    report_folder = SETUP_DIR + '\\report\\'
    log_path = SETUP_DIR + '\\common\\test_log\\'
    allure_result_folder = report_folder + 'allure\\allure_result\\'
    allure_report_folder = report_folder + 'allure\\allure_report\\'
else:
    txt_file_save_folder = SETUP_DIR + '/zmq_py3/zmq_save_files/Txt/'
    db_save_folder = SETUP_DIR + '/zmq_py3/zmq_save_files/db/'
    report_folder = SETUP_DIR + '/report/'
    log_path = SETUP_DIR + '/common/test_log/'
    allure_result_folder = report_folder + 'allure/allure_result/'
    allure_report_folder = report_folder + 'allure/allure_report/'
    test_instr_info = SETUP_DIR + '/test_instr_info.xlsx'
    rocksdb_path = '/mnt/test_rocksdb'      # 需加载映射磁盘


pub_table = 'pub_sub_info'
deal_table = 'deal_router_info'
subscribe_table = 'subscribe_info'
time_analysis_base_table = 'time_analysis_base_info'
statistical_analysis_table = 'statistical_analysis'
cal_table = 'cal_sub_info'

delay_minute = 15
tolerance_time = 0  # 容忍误差时间 ms

if env == 'SIT':
    pub_address = 'tcp://*:56789'
    router_address = 'tcp://*:5555'

    '''行情源IP'''
    # sub_address = 'tcp://192.168.80.27:5556'
    # sub_address = 'tcp://192.168.80.149:5558' # morning star 行情源
    sub_address = 'tcp://192.168.80.149:5556'  # FIU行情源
    cal_sub_address = 'tcp://192.168.80.149:7556'
    # sub_address = 'tcp://192.168.80.109:5556'  # shen huihai
    # sub_address = 'tcp://192.168.1.66:5558'

    # dealer_address = 'tcp://47.106.33.83:8031'
    dealer_address = 'tcp://192.168.80.149:5557'    # morning star 行情源
    # dealer_address = 'tcp://192.168.80.149:5555'  # FIU行情源
    # dealer_address = 'tcp://192.168.1.66:5557'

    delay_ws_url = 'ws://192.168.80.211:12512'      # PC延时
    # delay_ws_url = 'ws://192.168.80.183:12512'

    union_url = 'ws://192.168.80.211:12511'    # APP、PC实时订阅地址
    redis_host = '192.168.80.211'
    redis_port = 6379

    dbPath = db_save_folder + env + '_market_test.db'
