#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : modify_filename.py
# @Author: Lizi
# @Date  : 2020/9/7

import os
def rename():
    path = r'E:\Python_work\lizi_dir\yll'   # 获取文件所在路径
    try:
        filelist = os.listdir(path)   # 该路径下的所有文件和文件夹
        for files in filelist:        # 遍历所有文件和文件夹
            old_dir = os.path.join(path,files)   # 将路径和文件名连接，得到完整问文件目录
            if os.path.isdir(old_dir):   # 如果是文件夹，则跳过，不修改
                continue
            filename = os.path.splitext(old_dir)[0]    # splitext 拆分文件名和后缀名
            filetype = os.path.splitext(old_dir)[1]    # 获取后缀名
            if old_dir.find('_20200822') >= 1:
                new_dir = os.path.join(path,old_dir.replace('_20200822','_20200823'))   # 修改文件制定字符串
                os.rename(old_dir,new_dir) # 重命名文件
            else:
                print(files + "不符合要求！")
    except FileNotFoundError:
        print('路径不存在')


if __name__ == '__main__':
    rename()



