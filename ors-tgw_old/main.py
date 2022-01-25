# -*- coding: utf-8 -*-
# @Date : 2021/7/29 17:47
# @File : main.py
# @Author : Lizi

from analyse_data import Convert
from dump_pcap_data import dump
from write_file import *


if __name__ == '__main__':
    dump_data = dump.dump_data  # 获取dump下来的dump_data数据
    dump_timestamp = dump.dump_timestamp  # 获取dump下来的dump_timestamp数据
    convert = Convert(dump_data, dump_timestamp)
    convert.filter_data()
    write_csv()
