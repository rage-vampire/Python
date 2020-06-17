# -*- coding:utf-8 -*-
# @Filename : req_excel.py 
# @Author : Lizi
# @Time : 2020/4/28 21:19 
# @Software: PyCharm

import json, urllib3
import requests
import xlrd
from xlutils.copy import copy
from urllib import parse

# url1 = 'http://apis.juhe.cn/mobile/get'
# url2 = 'http://apis.juhe.cn/ip/ipNew'
# prarms1 = {
#     'phone': '18938896626',
#     'key': '646e09fa62e08de26ec3b5ccd1725acf',
# }
#
# prarms2 = {
#     'ip': '114.253.999.182',
#     'key': '646e09fa62e08de26ec3b5ccd1725acf',
# }
# html = requests.post(url2,prarms2).json()
#
# print(html)

excel_path = 'D:\\Py_file\\venv\\excel_request\\request_case.xlsx'
excel_file = xlrd.open_workbook(excel_path)
# 获取第一个sheet表
sht = excel_file.sheets()[0]

answer = []
pass_or_fail = []
body = {}
headers = {"User-Agent":
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2427.7 Safari/537.36"
}

# 获取Api接口信息
class Api_get:
    def __init__(self,url,parameter_keys,parameter_values):
        self.url = url
        for i in range(len(parameter_keys)):
            body[parameter_keys[i]] = parameter_values[i]

    '''判断是get请求还是post请求'''
    def way_to_requests(self,way):
        if way == 'get':
            return True
        elif way == 'post':
            return False
        else:
            return None

    '''发送post请求'''
    def api_post(self):



class Dispose_excel:
    '''获取所有的case'''
    def get_case_count(self):
        # 获取一共有多少行
        rows_count = sht.nrows
        # 去掉表头，一共有多少个case
        real_count = rows_count - 3
        return real_count

    '''获取URL接口'''
    def get_url(self, rows=None):
        url = rows[2]
        return url

    '''获取请求方式'''
    def get_way(self, way=None):
        way = rows[3]
        return way

    '''获取请求参数'''
    def get_param(self,param):
        param = rows[4]
        return param

    '''获取状态码'''
    def get_status_code(self,resultcode):
        resultcode = rows[5]
        return resultcode

    '''获取预期结果'''

    def get_expected_result(self):
        expected_result = rows[6]
        return expected_result

    # 把结果写入函数
    def
