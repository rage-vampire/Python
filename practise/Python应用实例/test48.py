# -*- coding:utf-8 -*-
# @Filename : test48.py 
# @Author : Lizi
# @Time : 2020/3/31 10:33 
# @Software: PyCharm

from urllib.request import urlopen, urlretrieve
import pprint

webpage = urlopen("https://www.baidu.com/")
# text = webpage.read()
# pprint.pprint(text)
urlretrieve("https://www.baidu.com/",r'd:\\aa.txt')