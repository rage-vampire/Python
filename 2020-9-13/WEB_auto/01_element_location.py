#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 01_element_location.py
# @Author: Lizi
# @Date  : 2020/11/20

from selenium import webdriver
from selenium.webdriver.common.by import By

"""
    一、元素定位
        
"""

"""
    elements复数定位方法
    driver.find_elements_by_id('name')
    driver.find_elements_by_name('passwd')
    driver.find_elements_by_class_name()
    driver.find_elements_by_tag_name()
    driver.find_elements_by_link_text()
    driver.find_elements_by_partial_link_text()
    driver.find_elements_by_xpath()
    driver.find_elements_by_css_selector()
    以上方法返回一个列表，通过索引的方式获取对应的元素定位
"""

# 打开浏览器
driver = webdriver.Chrome()

# 打开网址
driver.get('https://mail.163.com/')

# 通过id值定位
driver.find_element_by_id('name').send_keys('XXXX')

# 通过name值定位
driver.find_element_by_name('password').send_keys('XXXX')

# 通过class_name值定位
driver.find_element_by_class_name("j-inputtext dlpwd").send_keys('XXXXX')

# 通过标签名定位，应用比较少
driver.find_element_by_tag_name('input').send_keys('XXXXX')

# 通过定位超链接，即html页面中带<a>标签的
driver.find_element_by_link_text('新闻').click()     # 通过完整超链接文字定位
driver.find_element_by_partial_link_text('闻').click()   # 通过超链接部分文字定位、

# ----------------------------------------------------------------------------------------------------------------------


'''
    通过css定位
    # ：表示 id
    . ：表示class
    > ：表示层级关系
    优点：
        1、速度快
        2、方法灵活
        3、语法简洁
        4、抗变性强
    定位方法
        1、通过id和class定位
        2、通过CSS属性定位
        3、CSS层级和属性结合
        4、CSS爷爷层级和属性结合
'''
# 通过id和class定位
driver.find_element_by_css_selector("#kw")
driver.find_element_by_css_selector(".s_ipt")

# 通过CSS属性定位（万能型）
driver.find_element_by_css_selector("input[id='kw]")

# CSS层级和属性结合
"""
    span#s_ipt:表示父类标签下的id属性值为s_ipt
    >：表示层级关系
    input：表示子标签（即需要定位的标签）
"""
driver.find_element_by_css_selector("span#s_ipt>input")

# CSS爷爷层级和属性结合
driver.find_element_by_css_selector("form#form>span#s_ipt>input")

# ----------------------------------------------------------------------------------------------------------------------


'''
    通过xpath定位
    1、通过绝对路径定位：通过html标签的层级关系定位元素的绝对路径，一般从<html>标签开始依次往下进行查找。
    2、通过元素属性的相对路径定位：
    3、层级和属性相结合的定位
    4、通过逻辑运算符定位

'''
"""
    标签名input可以用*代替，而且只要是该标签内的任意属性都可用来定位
    //:表示相对路径
    input：定位元素所在的标签名
    @：后面紧跟元素的属性id、name、class_name、type...........
    标签名input可以用*代替，而且只要是该标签内的任意属性都可用来定位
    
"""
# 通过相对路径定位
driver.find_elements_by_xpath('//*[@id="auto-id-1605835525254"]')
driver.find_elements_by_xpath('//input[@id="auto-id-1605835525254"]')
driver.find_elements_by_xpath('//input[@id="auto-id-1605835525254"]')

# 通过绝对路径定位
driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/form/div/div[1]/div[2]/input')

# 层级和属性相结合的定位
"""
    //:表示相对路径
    span：父类标签名
    @id：父类id属性的值
    /：代表层级关系
    input:定位元素所在的标签名
"""
driver.find_element_by_xpath("//span[@id='kw']/input").send_keys('XXX')
# 爷爷标签
driver.find_element_by_xpath("//form[@id='form']/span/input")


# 通过逻辑运算符定位
driver.find_element_by_xpath("//input[@id='kw' and @name='wd']")

# ----------------------------------------------------------------------------------------------------------------------

"""
    通过By方法定位
"""
driver.find_element(By.ID, 'email').send_keys('sdfsdsg')
driver.find_element(By.NAME, 'email').send_keys('sdfsdsg')
driver.find_element(By.CLASS_NAME, 's_ipt')
driver.find_element(By.TAG_NAME, 'input')
driver.find_element(By.LINK_TEXT, u'新闻')
driver.find_element(By.PARTIAL_LINK_TEXT, u'新闻')
driver.find_element(By.XPATH, '//*[@id="auto-id-1605835525254"]')
driver.find_element(By.CSS_SELECTOR, '//*[@id="auto-id-1605835525254"]')

