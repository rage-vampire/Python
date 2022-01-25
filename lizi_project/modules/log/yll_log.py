# -*- coding:utf-8 -*-
# @Filename : yll_log.py 
# @Author : Lizi
# @Time : 2020/5/13 8:37 
# @Software: PyCharm

import logging
import time
import os


def get_log(log_model_name, style='console'):
    """
    :param log_model_name: 要打印日志的模块名
    :param style: 日志打印方式，console：打印到控制台；file：打印到文件中
    :return:
    """
    # 创建一个logger日志器
    logger = logging.getLogger(log_model_name)

    # 通过日志器设置日志级别
    logger.setLevel(level=logging.DEBUG)

    # 设置日志存放路径，日志文件名
    # 获取本地时间，转换为设置的格式
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    # 设置所有日志和错误日志的存放路径
    path = os.path.dirname(os.path.abspath('log_print.py'))
    all_log_path = os.path.join(path, 'All_Logs/')
    error_log_path = os.path.join(path, 'Error_Logs/')
    print(all_log_path)

    # 判断要保存的日志文件夹是否存在，不存在就创建
    if not os.path.exists(all_log_path):
        os.mkdir(all_log_path)
    if not os.path.exists(error_log_path):
        os.mkdir(error_log_path)

    # 设置日志文件名
    all_log_name = all_log_path + rq + '_all.log'
    error_log_name = error_log_path + rq + '_error.log'

    if style == 'console':
        # 创建一个handler输出到控制台
        # 创建一个handler写入所有日志
        all_log = logging.StreamHandler()
        # 通过处理器设置日志级别
        all_log.setLevel(logging.INFO)

        # 创建一个handler写入错误日志
        error_log = logging.StreamHandler()
        error_log.setLevel(logging.ERROR)

        # 定义日志输出格式
        # 以时间-日志名称-日志级别-日志内容的形式展示
        all_log_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')

        # 以时间-日志名称-日志级别-文件名-函数行数-错误内容
        error_log_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(module)s-%(message)s')

        # 给logger添加handler
        logger.addHandler(all_log)
        logger.addHandler(error_log)

        # 将定义好的输出形式添加到handler
        all_log.setFormatter(all_log_formatter)
        error_log.setFormatter(error_log_formatter)
        return logger
    else:
        # 日志写入到文件
        # 创建一个handler写入所有日志
        all_log = logging.FileHandler(all_log_name)
        all_log.setLevel(logging.DEBUG)

        # 创建一个handler写入错误级别以上的日志
        error_log = logging.FileHandler(error_log_name)
        error_log.setLevel(logging.ERROR)

        # 定义日志输出格式
        # 以时间-日志名称-日志级别-日志内容的形式展示
        all_log_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')

        # 以时间-日志名称-日志级别-文件名-函数行数-错误内容
        error_log_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(module)s-%(message)s')

        # 给logger添加handler
        logger.addHandler(all_log)
        logger.addHandler(error_log)

        # 将定义好的输出形式添加到handler
        all_log.setFormatter(all_log_formatter)
        error_log.setFormatter(error_log_formatter)
        return logger


if __name__ == '__main__':
    log = get_log('test', 'file')  # test需要打印日志的项目名称
    log.critical('aaa 1213')
    log.error('bbb dsg')
    log.warning('www.baidu.com')
    log.info('aaa 7890')
    log.debug('ccc ewfsd')