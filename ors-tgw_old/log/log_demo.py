#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : log_demo.py
# @Author: Lizi
# @Date  : 2020/11/17

import logging
import time
import os


class Log:
    def __init__(self, log_model_name, style='console'):
        self.log_model_name = log_model_name
        self.style = style

        self.logger = logging.getLogger(self.log_model_name)
        self.logger.setLevel(level=logging.DEBUG)

    def get_path(self):
        rp = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        path = os.path.dirname(os.path.abspath('xx.py'))
        all_log_path = os.path.join(path, 'ALL_logs/')
        error_log_path = os.path.join(path, 'ERROR_logs/')
        # print(all_log_path)

        if not os.path.exists(all_log_path):
            os.mkdir(all_log_path)
        if not os.path.exists(error_log_path):
            os.mkdir(error_log_path)

        all_log_name = all_log_path + rp + '_all_log.txt'
        error_log_name = error_log_path + rp + '_error_log.txt'
        # print(all_log_name)
        return all_log_name, error_log_name

    def set_formatter(self):
        self.all_log_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
        self.error_log_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(module)s-%(message)s')
        return self.all_log_formatter, self.error_log_formatter

    def set_handle(self):
        if self.style == 'console':
            self.all_log_handle = logging.StreamHandler()
            self.all_log_handle.setLevel(logging.DEBUG)
            self.logger.addHandler(self.all_log_handle)
            self.all_log_handle.setFormatter(self.all_log_formatter)

            self.error_log_handle = logging.StreamHandler()
            self.error_log_handle.setLevel(logging.ERROR)
            self.logger.addHandler(self.error_log_handle)
            self.error_log_handle.setFormatter(self.set_formatter()[1])
        else:
            self.all_log_handle = logging.FileHandler(self.get_path()[0])
            self.all_log_handle.setLevel(logging.DEBUG)
            self.logger.addHandler(self.all_log_handle)
            self.all_log_handle.setFormatter(self.set_formatter()[0])

            self.error_log_handle = logging.FileHandler(self.get_path()[1])
            self.error_log_handle.setLevel(logging.ERROR)
            self.logger.addHandler(self.error_log_handle)
            self.error_log_handle.setFormatter(self.set_formatter()[1])

    def get_log(self):
        self.set_formatter()
        self.set_handle()
        return self.logger


# logger = Log('yll', 'file').get_log()

"""
    其他文件调用：
        from log_demo import logger
"""

# if __name__ == '__main__':
    # log = Log('yll', 'file')
    # log.main()
    # logger = log.get_log()
    # logger.critical('cirtical级别的日志')
    # logger.error('error级别的日志')
    # logger.warning('warning级别的日志')
    # logger.info('info级别的日志')
    # logger.debug('debug级别的日志')
