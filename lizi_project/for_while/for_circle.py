#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : for_circle.py
# @Author: Lizi
# @Date  : 2020/9/13


# for循环结合break和else使用，else在穷尽列表（for循环为例）时才执行，但循环呗break终止是不执行
sites = ["Baidu", "Google","Runoob","Taobao"]
for site in sites:
    if site == 'Runoob':
        print("菜鸟教程")
        break
    print('循环数据', site)
else:
    print('没有循环数据！')
print('循环完成')


def zhi_shu():
    """判断用户输入的数是否为质数"""
    num = int(input("请输入整数："))
    if num>=1:
        for i in range(2, num):
            if num%i == 0:
                print("{}不是质数".format(num))
                print(i, "*", num//i, '=', num)
                break
        else:
            print('{}是质数'.format(num))
    else:
        print("{}不是质数".format(num))


def zhi_shu2():
    lista = [1,2,3]
    for i in range(2, 10):
        for j in range(2, i):
            if i % j == 0:
                print("{}不是质数".format(i))
                print(j, '*', i//j, "=", i)
                break
        else:
            print("{}是质数".format(i))



if __name__ == '__main__':
    zhi_shu2()

