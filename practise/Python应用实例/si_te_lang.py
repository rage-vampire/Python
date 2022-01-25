# -*- coding:utf-8 -*-
# @Filename : si_te_lang.py 
# @Author : Lizi
# @Time : 2020/6/22 15:16 
# @Software: PyCharm

num = int(input('请输入一个正整数：'))
# 初始化sum
sum = 0
# 获取指数
n = len(str(num))

temp = num
while temp > 0:
    digit = temp % 10
    sum += digit ** n
    temp //= 10

if num == sum:
    print(num, '是阿姆斯特朗数')
else:
    print(num, '不是阿姆斯特朗数')
