#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : simple_demo.py
# @Author: Lizi
# @Date  : 2020/11/16

"""
    一、日志组件：日志器getLogger()----->处理器FileHandler()、StreamHandler()----->格式器Formatter()；
    二、控制输出日志的级别
        1、日志器设置级别；
        2、处理器设置级别；
        原则：同时设置时，谁设置的级别高，以谁为准
    三、格式器
        1、日志器可以添加多个不同的处理器；
        2、处理器可以添加多个不同的格式器；
"""

import logging

# 创建日志器，产生日志
logger = logging.getLogger()

# 通过日志器设置日志级别
logger.setLevel(level=logging.DEBUG)   # 设置DEBUG级别的日志

# 创建处理器，如：控制台、本地文件
file_handle = logging.FileHandler(filename='./test.log')  # 日志输出到本地文件
stream_handle = logging.StreamHandler()  # 日志输出到控制台上

# 通过处理器设置日志级别
file_handle.setLevel(level=logging.WARNING)
stream_handle.setLevel(level=logging.ERROR)

# 将处理器添加到日志器里面
logger.addHandler(stream_handle)
logger.addHandler(file_handle)

# 设置格式器
log_formatter = logging.Formatter('%(asctime)s  %(filename)s  %(lineno)d  %(message)s')

# 将格式器添加到处理器中
stream_handle.setFormatter(log_formatter)
file_handle.setFormatter(log_formatter)


if __name__ == '__main__':
    logger.critical('cirtical级别的日志')
    logger.error('error级别的日志')
    logger.warning('warning级别的日志')
    logger.info('info级别的日志')
    logger.debug('debug级别的日志')
