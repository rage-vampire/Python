# -*- coding:utf-8 -*-
# @Filename : ed_log.py
# @Author : Lizi
# @Time : 2020/5/9 13:33 
# @Software: PyCharm

import logging
import logging.config
from test_config import *

global test_logger
test_logger = None


# 普通配置文件方法
def get_log():
    global test_logger
    if test_logger:
        pass
    else:
        if sys.platform == 'win32':
            logging.config.fileConfig(log_path + 'windows_logging.conf')
        else:
            logging.config.fileConfig(log_path + 'linux_logging.conf')
        # test_logger = logging.getLogger('getlog')
        test_logger = logging.getLogger('onlyconsole')
    return test_logger


if __name__ == '__main__':
    get_log()