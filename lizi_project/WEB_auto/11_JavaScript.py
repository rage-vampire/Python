#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 11_JavaScript.py
# @Author: Lizi
# @Date  : 2020/11/28

from selenium import webdriver

# driver = webdriver.Chrome()
# driver.get('https://www.baidu.com')

"""
    windows对象
"""
# # 打开一个新窗口
# js = 'window.open("https://www.baidu.com")'
#
# # selenium执行js语句
# driver.execute_script(js)
#
# # window.innerHeight:获取内部高度
# innerheight = driver.execute_script('return window.innerHeight')
#
# # window.innerWidht:获取内部宽度
# innerwidht = driver.execute_script('return window,innerWidth')
#
# # window.outerHeight:获取外部高度
# outerheight = driver.execute_script('return window.outerHeight')
#
# # window.outerHeight:获取外部宽度
# outerwidht = driver.execute_script('return window,outerrWidth')
#
# # window.close():关闭当前窗口
# driver.execute_script('window.close()')


# --------------------------------------------------------------------------------------------------------------------
"""
    Location对象
"""
driver = webdriver.Chrome()

js = 'window.open("https://www.baidu.com")'
driver.execute_script(js)


all_handles = driver.window_handles
driver.switch_to.window(all_handles[-1])
# location.href:返回当前页面的URL
url = driver.execute_script('return location.href')

# location.hostname:返回web主机的域名
hostname = driver.execute_script('return location.hostname')


# location.pathname:返回当前界面的路径或文件名
print(driver.execute_script("return location.pathname"))

# location.protocol:返回使用的 web 协议
print(driver.execute_script('return location.protocol'))

# location.assign(url): 在当前界面重新载入新的网页，能返回到上个界面
driver.execute_script('location.assign("https://www.tmall.com/")')

# location.reload():重新加载当前页面，刷新
driver.execute_script('location.reload()')


# location.replace(url):输入的url替换当前的url,加载新的页面，不能回到上个界面
driver.execute_script('location.replace("https://www.baidu.com")')

driver.close()

